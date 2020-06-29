"""Site logic for parsing fanficauthors.net
fanfiction stories"""
from ff_scrape.storybase import Chapter
from ff_scrape.errors import URLError
from ff_scrape.sites.base import Site
from ff_scrape.standardization import *
import re
from dateutil.parser import parse
import time


class AnimationSource(Site):
    """Provides the logic to parse fanfics from animationsource.org"""
    _fandom: str

    def __init__(self, site_params={}):
        super().__init__(logger_name='ff_scrape.site.AnimationSource',
                         site_params=site_params)
        self.site_url = "https://archiveofourown.org"
        self._fandom = ""

    def set_domain(self) -> None:
        """Sets the domain of the fanfic to AnimationSource"""
        self._fanfic.domain = "Animation Source"

    def can_handle(self, url: str) -> bool:
        if 'animationsource.org/' in url:
            return True
        return False

    @Site.url.setter
    def url(self, value: str) -> None:
        """Allows for the URL to be changed to parse another fanfic"""
        if self._fanfic_set:
            del self._fanfic
            self._got_meta = False
            self.cleanup_custom_vars()
        self._url = ''
        value = self.correct_url(value)

        self.log_debug("Updating URL to: %s" % value)
        self._url = value
        url_split = value.split("/")
        self._fandom = url_split[3]

    def correct_url(self, url: str) -> str:
        """Perform the necessary steps to correct the supplied URL so the parser can work with it"""
        # check if url has "http://" or "https://" prefix
        if "http://" not in url and "https://" not in url:
            url = "http://" + self.url
        url_split = url.split("/")
        # correct URL as needed for script
        if len(url_split) != 8:
            raise URLError('Unknown URL format')
        if url_split[7] == '':
            raise URLError('Unknown URL format')

        temp = url_split[7].split('&')
        url_split[7] = temp[0]
        url = '/'.join(url_split)
        return url

    def cleanup_custom_vars(self):
        self._fandom = ""

    def check_story_exists(self) -> bool:
        """Verify that the fanfic exists"""
        title = self._soup.find_all('div', {'class': 'bhaut2b'})[0]
        if title.text == "The page can't be found!":
            self.log_warn("Story doesn't exist.")
            return False
        return True

    def record_story_metadata(self) -> None:
        """Record the metadata of the fanfic"""

        colon_removal = re.compile("^\\s+:\\s+")

        self._fanfic.raw_index_page = self._soup.prettify()
        self._fanfic.add_universe(standardize_universe(self._fandom))
        self._fanfic.title = self._soup.find_all('div', {'class': 'bhaut2b'})[0].text

        # get top panel with the details
        header = self._soup.find_all('div', {'class', 'ct2'})[0]

        author_text = header.find_all(text='Author')[0]
        author_string = author_text.parent.next_sibling
        author_string = colon_removal.sub('', author_string).strip()

        author_link_search = self._soup.find_all('span', {'class': 'bs2'})
        author_link = ""
        for element in author_link_search:
            if element.text == "Go to the writer's section":
                # we found a link wrapper, see if a link is present
                links = element.find_all('a')
                if len(links) > 0:
                    author_link = links[0].attrs['href']
        self._fanfic.add_author(author_string, author_link)

        # get the dates, due to the way the site it, there is no updates only published dates
        self._fanfic.status = standardize_status("Completed")
        date_text = header.find_all(text='Date sent')[0]
        date_string = date_text.parent.next_sibling
        date_string = colon_removal.sub('', date_string).strip()
        date_time = parse(date_string)
        self._fanfic.updated = date_time
        self._fanfic.published = date_time

        # get the rating
        rating_text = header.find_all(text='Rating')[0]
        rating_string = rating_text.parent.next_sibling.next_sibling.text
        self._fanfic.rating = standardize_rating(rating_string)

        # get the category which we will store as genre
        genre_text = header.find_all(text='Category')
        if len(genre_text) > 0:
            genre_text = genre_text[0]
            genre_string = genre_text.parent.next_sibling
            genre_string = colon_removal.sub('', genre_string).strip()
            self._fanfic.add_genre(standardize_genre(genre_string))

        # get the description which we will store as summary
        description_text = header.find_all(text='Description')[0]
        description_string = description_text.parent.next_sibling
        description_string = colon_removal.sub('', description_string).strip()
        self._fanfic.summary = description_string

        # record the characters listed
        character_text = header.find_all(text='Characters  : ')[0]
        sibling = character_text.next_sibling
        if sibling.name == 'center':
            # then we have characters to parse
            for character in sibling.find_all('center'):
                self._fanfic.add_character(standardize_character(character.text))

    def _extract_chapter(self, chapter: str) -> Chapter:
        chapter_obj = Chapter()

        # get the story container
        fanfic_container = self._soup.find_all('div', {'class': 'fanfic'})[0]
        chapter_obj.raw_body = fanfic_container.prettify()

        # remove the table containing the chapter links at the bottom
        for table in fanfic_container.find_all('table'):
            table.decompose()
        chapter_obj.processed_body = fanfic_container.prettify()
        chapter_obj.word_count = len(fanfic_container.text.split())

        chapter_obj.name = "Chapter {}".format(chapter)
        return chapter_obj

    def record_story_chapters(self) -> None:
        """Record the chapters of the fanfic"""

        # get initial reading link
        link = self._url + "&deb=0&nsite=1"
        self._update_soup(link)

        chapters_raw = self._soup.find_all('span', {'class': 'f9'})
        chapters = []
        # need to iterate chapters first to extract details before decompose
        for chapter in chapters_raw:
            chapter_number = chapter.text.strip()

            # continue if this is the link for the first chapter as that is already captured
            if chapter_number == '1':
                continue

            # find the link
            for link in chapter.find_all('a'):
                chapters.append({'number': chapter_number, 'link': link.attrs['href']})

        self._fanfic.add_chapter(self._extract_chapter('1'))

        for chapter in chapters:
            time.sleep(self._chapter_sleep_time)
            # get page
            self._update_soup(url=chapter['link'])

            self._fanfic.add_chapter(self._extract_chapter(chapter['number']))
