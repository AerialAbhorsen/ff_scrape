"""Site logic for parsing fanficauthors.net
fanfiction stories"""
from ff_scrape.storybase import Chapter
from ff_scrape.errors import URLError
from ff_scrape.sites.base import Site
from ff_scrape.standardization import *
import re
from dateutil.parser import parse
from bs4.element import Tag
from typing import List

class ArchiveofOurOwn(Site):
    """Provides the logic to parse fanfics from archiveofourown.org"""

    def __init__(self, site_params={}):
        super().__init__(logger_name='ff_scrape.site.ArchiveofOurOwn',
                         site_params=site_params)
        self.site_url = "https://archiveofourown.org"

    def set_domain(self) -> None:
        """Sets the domain of the fanfic to archiveofourown"""
        self._fanfic.domain = "Archive of Our Own"

    def can_handle(self, url: str) -> bool:
        if 'archiveofourown.org/' in url:
            return True
        return False

    def correct_url(self, url: str) -> str:
        """Perform the necessary steps to correct the supplied URL so the parser can work with it"""
        # check if url has "http://" or "https://" prefix
        if "http://" not in url and "https://" not in url:
            url = "http://" + self.url
        url_split = url.split("/")
        # correct URL as needed for script
        if len(url_split) <= 4:
            raise URLError('Unknown URL format')
        if url_split[4] == '':
            raise URLError('Missing story ID')

        while len(url_split) > 5:
            url_split.pop(5)
        story_id = url_split[4].split('?')
        url_split[4] = story_id[0] + "?view_full_work=true"
        url = '/'.join(url_split)
        return url

    def check_story_exists(self) -> bool:
        """Verify that the fanfic exists"""
        errors = self._soup.find_all(True, {'class': 'error-404'})
        if len(errors) > 0:
            self.log_warn("Story doesn't exist.")
            return False
        return True

    def _extract_values(self, tag: Tag) -> List[str]:
        values = []
        links = tag.find_all('a')
        for link in links:
            values.append(link.text)
        return values

    def record_story_metadata(self) -> None:
        """Record the metadata of the fanfic"""

        self._fanfic.raw_index_page = self._soup.prettify()

        # get title and author from top center
        header = self._soup.find_all(True, {'class': 'work meta group'})[0]

        ratings = header.find_all('dd', {'class': 'rating'})[0]
        for value in self._extract_values(ratings):
            self._fanfic.rating = standardize_rating(value)

        warnings = header.find_all('dd', {'class': 'warning'})[0]
        for value in self._extract_values(warnings):
            value = standardize_warning(value)
            if value is not None:
                self._fanfic.add_warning(value)

        universes = header.find_all('dd', {'class': 'fandom'})[0]
        for value in self._extract_values(universes):
            self._fanfic.add_universe(standardize_universe(value))

        categories = header.find_all('dd', {'class': 'category'})[0]
        for value in self._extract_values(categories):
            value = standardize_category(value)
            if value is not None:
                self._fanfic.add_category(value)

        author_categories = header.find_all('dd', {'class': 'freeform'})[0]
        for value in self._extract_values(author_categories):
            value = standardize_category(value)
            if value is not None:
                self._fanfic.add_category(value)

        pairings = header.find_all('dd', {'class': 'relationship'})[0]
        for value in self._extract_values(pairings):
            self._fanfic.add_pairing(value.split('/'))

        characters = header.find_all('dd', {'class': 'character'})[0]
        for value in self._extract_values(characters):
            value = standardize_character(value)
            if value is not None:
                self._fanfic.add_character(value)

        timestamps = []
        published = header.find_all('dd', {'class': 'published'})[0]
        timestamps.append(parse(published.text))

        status = header.find_all(True, {'class': 'status'})
        if len(status) > 0:
            # second entry is timestamp
            timestamps.append(parse(status[1].text))
            status_str = status[0].text.replace(':', '')
            self._fanfic.status = standardize_status(status_str)
        else:
            # if status section is missing, it is a one shot so mark as completed
            self._fanfic.status = standardize_status("Completed")

        self._fanfic.published = min(timestamps)
        self._fanfic.updated = max(timestamps)

        new_line_regex = re.compile('\n')
        title_container = self._soup.find_all('h2', {'class': 'title heading'})[0]
        title = title_container.text
        title = new_line_regex.sub('', title)
        self._fanfic.title = title.strip()

        author_container = self._soup.find_all('h3', {'class': 'byline heading'})[0]
        links = author_container.find_all('a')
        for author in links:
            self._fanfic.add_author(author.text, self.site_url + author['href'])

        summary_container = self._soup.find_all('div', {'class': 'summary module'})[0]
        quote = summary_container.find_all('blockquote')[0]
        summary = quote.text
        summary = new_line_regex.sub('', summary)
        self._fanfic.summary = summary.strip()

    def record_story_chapters(self) -> None:
        """Record the chapters of the fanfic"""

        id_regex = re.compile('chapter')
        new_line_regex = re.compile('\n')
        chapters = self._soup.find_all('div', {'class': 'chapter', 'id': id_regex})

        for chapter in chapters:
            # todo: need to add author notes in as well
            chapter_object = Chapter()

            chap_name_container = chapter.find_all(True, {'class': 'chapter preface group'})[0]
            chap_name = chap_name_container.find_all('h3')[0].text
            chapter_object.name = new_line_regex.sub('', chap_name).strip()

            chap_text = chapter.find_all(True, {'class': 'userstuff'})[0]
            chapter_object.raw_body = chap_text.prettify()

            # remove the invisible heading
            heading = chapter.find_all('h3', {'class': ['landmark', 'heading']})
            for element in heading:
                element.decompose()
            chapter_object.processed_body = chap_text.prettify()
            chapter_object.word_count = len(chap_text.text.split())

            self._fanfic.add_chapter(chapter_object)
