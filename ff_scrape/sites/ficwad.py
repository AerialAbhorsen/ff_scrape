"""Site logic for parsing ficwad.com
fanfiction stories"""
from ff_scrape.storybase import Chapter
from ff_scrape.errors import URLError, StoryError, ParameterError
from ff_scrape.sites.base import Site
from ff_scrape.standardization import *
from urllib.parse import urljoin, urlparse
import requests
import re
import time
from dateutil.parser import parse
from requests.cookies import RequestsCookieJar


class Ficwad(Site):
    """Provides the logic to parse fanfics from ficwad.com"""
    _index_page: str
    _web_domain: str
    cookie_jar: RequestsCookieJar
    chapter_list: [dict]

    def __init__(self, site_params={}):
        super().__init__(logger_name='ff_scrape.site.Ficwad',
                         site_params=site_params)
        self.chapter_list = []
        self._index_page = None
        self._web_domain = "http://ficwad.com"
        self.cookie_jar = None
        if 'login' in site_params and site_params['login'].upper() == 'TRUE':
            if 'username' in site_params and 'password' in site_params:
                self.login(site_params['user'], site_params['password'])
            else:
                raise ParameterError("No credentials provided")

    def login(self, user: str, password: str) -> None:
        login = requests.post('https://ficwad.com/account/login', files=(
            ('username', (None, user)),
            ('password', (None, password))
        ))
        self.cookie_jar = login.cookies

    def set_domain(self) -> None:
        """Sets the domain of the fanfic to Fanfiction.net"""
        self._fanfic.domain = "Ficwad.com"

    def can_handle(self, url: str) -> bool:
        if 'ficwad.com/' in url:
            return True
        return False

    def correct_url(self, url: str) -> str:
        """Perform the necessary steps to correct the supplied URL so the parser can work with it"""
        # check if url has "http://" prefix
        if "http://" not in url:
            if "https://" not in url:
                url = "http://" + url
        url_split = url.split("/")
        # correct URL as needed for script
        if url_split[4] == '':
            raise URLError('No Story ID given')
        if len(url_split) == 5:
            url_split.append('')
        else:
            raise URLError('Unknown URL format')
        url = '/'.join(url_split)
        url = urljoin(url, ' ')[0:-2]
        return url

    def check_story_exists(self) -> bool:
        """Verify that the fanfic exists"""
        title_check = self.soup.find("title").string
        if title_check == u'FicWad: fresh-picked original and fan fiction':
            return False
        return True

    def cleanup_custom_vars(self) -> None:
        self.chapter_list = []
        self._index_page = None

    def _get_story_chapter_list_non_index(self) -> None:
        chap_list_select = self._soup.find_all(True, {'name': 'chapterlist'})
        if len(chap_list_select) == 0:
            # if there is no select with a chapter list inside, we are in a single chapter story
            url_obj = urlparse(self._url)
            self._index_page = url_obj.path

            title = self._soup.find(href=url_obj.path)
            self.chapter_list.append({'name': title.text, 'link': url_obj.path})
        else:
            chap_list_select = chap_list_select[0]
            options = chap_list_select.find_all('option')
            for page in options:
                if page.text == 'Story Index':
                    self._index_page = page['value']
                else:
                    self.chapter_list.append({'name': page.text, 'link': page['value']})

    def get_story_chapter_list(self) -> None:
        """Create a list of the chapters in the fanfic"""
        # check if it is the story index page
        story_text = self._soup.find(id='storytext')
        if story_text is not None:
            # we are in a index list, we need to see if we can access the story
            self._index_page = self._url

            story_container = self._soup.find_all('ul', {'class': 'storylist'})[0]
            chapter_blocks = story_container.find_all('li')
            for block in chapter_blocks:
                if 'blocked' not in block.attrs['class']:
                    # we found an open chapter
                    links = block.find_all('a')
                    open_url = self._web_domain + links[0]['href']
                    self._update_soup(url=open_url)

                    # now run the get story chapters method on the open page
                    self._get_story_chapter_list_non_index()
            else:
                raise StoryError('Story is age blocked, can not locate an unblocked chapter.')
        else:
            # we are in a chapter, we need to generate the chapter list
            self._get_story_chapter_list_non_index()

    def record_story_metadata(self) -> None:
        """Record the metadata of the fanfic"""

        # need to find an entry point first
        self.get_story_chapter_list()

        # jump to the index page
        index_url = self._web_domain + self._index_page
        self._update_soup(url=index_url)
        self._fanfic.raw_index_page = self._soup.prettify()

        # add author and title
        author_container = self._soup.find_all('span', {'class': 'author'})[0]
        author_element = author_container.find_all('a')[0]
        self._fanfic.author = author_element.text
        self._fanfic.author_url = self._web_domain + author_element['href']

        metadata_container = self._soup.find_all(True, {'class': 'storylist'})[0]
        title_element = metadata_container.find_all('h4')[0]
        self._fanfic.title = title_element.text

        # add summary
        self._fanfic.summary = metadata_container.find_all('block_quote')[0].text

        # add other meta
        meta_block = metadata_container.find_all('p', {'class': 'meta'})[0]
        all_links = meta_block.find_all('a')

        # meta block has complete at the end only if it is complete
        if len(meta_block.find_all(text=re.compile("complete", re.IGNORECASE))) > 0:
            self._fanfic.status = 'Complete'
        else:
            self._fanfic.status = 'WIP'

        universe = all_links[0]
        self._fanfic.add_universe(universe.text)

        rating_block = meta_block.find_all(text=re.compile('rating', re.IGNORECASE))
        block_string = str(rating_block)  # change from BS NavigatableString to str
        block_string = block_string.replace('\xa0', ' ')  # replace &nbsp; with space char

        # header rating seems to always be the highest
        rating_group = block_string.split(' - ')[1]
        pair = rating_group.split(':')
        if pair[0].lower() == 'rating':
            self._fanfic.rating = standardize_rating(pair[1])

        # need to get all genres and dedupe due to top genre not guaranteed to be inclusive
        genre_list = []
        genre_strings = self._soup.find_all(text=re.compile("genres", re.IGNORECASE))
        for string in genre_strings:
            string = string.replace('\xa0', '')  # replace &nbsp; with nothing
            genre_section = string.split(' - ')[2]
            genre_pair = genre_section.split(':')
            for genre in genre_pair[1].split(','):
                if genre not in genre_list:
                    genre_list.append(genre)
        for genre in genre_list:
            self._fanfic.add_genre(standardize_genre(genre))

        # need to get all characters and dedupe due to top character list not guaranteed to be inclusive
        char_list = []
        char_strings = self._soup.find_all(text=re.compile("characters", re.IGNORECASE))
        for string in char_strings:
            string = string.replace('\xa0', '')  # replace &nbsp; with nothing
            char_pair = string.split(':')
            for character in char_pair[1].split(','):
                if character not in char_list:
                    char_list.append(character)
        for character in char_list:
            self._fanfic.add_character(standardize_character(character))

        # header warnings seems to always be inclusive
        for link in all_links:
            if 'title' in link.attrs:
                self._fanfic.add_warning(standardize_warning(link.attrs['title']))

        timestamps = meta_block.find_all('span', title=re.compile('.*'))
        self._fanfic.published = parse(timestamps[0].attrs['title'])
        self._fanfic.updated = parse(timestamps[1].attrs['title'])

    def record_story_chapters(self) -> None:
        """Record the chapters of the fanfic"""
        # get the chapters
        for chapter in self.chapter_list:
            time.sleep(self._chapter_sleep_time)
            self.log_debug("Downloading chapter:" + chapter['name'])
            url_fixed = urljoin(self.url, chapter['link'])

            # get page
            self._update_soup(url=url_fixed)
            story = self._soup.find(id='storytext')

            chapter_object = Chapter()
            chapter_object.processed_body = story.prettify()
            chapter_object.raw_body = self._soup.prettify()
            chapter_object.word_count = len(story.text.split())
            chapter_object.name = chapter['name']
            self._fanfic.add_chapter(chapter_object)
