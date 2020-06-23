"""Site logic for parsing fanficauthors.net
fanfiction stories"""
from ff_scrape.storybase import Chapter
from ff_scrape.errors import URLError
from ff_scrape.fanficsite import Site
from ff_scrape.standardization import *
from urllib.parse import urljoin, urlparse, urlunparse
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
import time
from dateutil.parser import parse

class FanficAuthors(Site):
    """Provides the logic to parse fanfics from fanficauthors.net"""

    def __init__(self, site_params=[]):
        super().__init__(logger_name='ff_scrape.site.FanficAuthors',
                         site_params=site_params)
        self.chapter_list = []
        self._url_obj = None

    def set_domain(self):
        """Sets the domain of the fanfic to Fanfiction.net"""
        self._fanfic.domain = "fanficauthors.net"

    def can_handle(self, url):
        if 'fanficauthors.net/' in url:
            return True
        return False

    @Site.url.setter
    def url(self, value):
        """Allows for the URL to be changed to parse another fanfic"""
        if self._fanfic_set:
            del self._fanfic
            self._got_meta = False
            self.cleanup_custom_vars()
        self._url = ''
        value = self.correct_url(value)

        self.log_debug("Updating URL to: %s" % value)
        self._url = value
        self._url_obj = urlparse(value)

    def correct_url(self, url):
        """Perform the necessary steps to correct the supplied URL so the parser can work with it"""
        # check if url has "http://" or "https://" prefix
        if "http://" not in url and "https://" not in url:
            url = "http://" + self.url
        url_split = url.split("/")
        # correct URL as needed for script
        if len(url_split) <= 4:
            raise URLError('Unknown URL format')
        else:
            while len(url_split) > 5:
                url_split.pop(5)
            url = urljoin('/'.join(url_split), 'index')
        return url

    def check_story_exists(self):
        """Verify that the fanfic exists"""
        title = self._soup.find('title')
        if title.contents == 'Not Found':
            self.log_warn("Story doesn't exist.")
            return False
        return True

    def cleanup_custom_vars(self):
        self.chapter_list = []
        self._url_obj = None

    def record_story_metadata(self):
        """Record the metadata of the fanfic"""

        # get title and author from top center
        header = self._soup.find_all(True, {'class': 'page-header'})[0]
        header_objs = header.find_all(True, {'class': 'text-center'})
        self._fanfic.author = header_objs[1].text
        self._fanfic.title = header_objs[0].text
        self._fanfic.author_url = self._url_obj.scheme + "://" + self._url_obj.netloc

        # get metadata info from story summary div
        metadata_container = self._soup.find_all(True, {'class': 'well'})[0]
        self._fanfic.summary = metadata_container.find('blockquote').text

        paragraphs = metadata_container.find_all('p')
        for group in paragraphs[1].text.split(' - '):
            pair = group.split(':')
            if pair[0].lower() == 'status':
                self._fanfic.status = standardize_status(pair[1])
            elif pair[0].lower() == 'rating':
                self._fanfic.rating = standardize_rating(pair[1])
            elif pair[0].lower() == 'genre':
                self._fanfic.add_genre(standardize_genre(pair[1]))

        # record the updated and uploaded times to attempt to identify published and updated dates
        updated_regex = re.compile("updated|uploaded on", re.IGNORECASE)
        updated_texts = self._soup.find_all(text=updated_regex)

        dates = []
        for date_block in updated_texts:
            date_string = date_block.split('on ')[-1]
            dates.append(parse(date_string))

        self._fanfic.published = min(dates)
        self._fanfic.updated = max(dates)

        container = self._soup.find_all(True, {'class': 'row'})[0]
        links = container.find_all('a')
        for link in links:
            if link.text in ['Epub', 'lit', 'mobi', 'pdf', 'txt']:
                continue
            self.chapter_list.append({'link': link['href'], 'name': link.text})

    def record_story_chapters(self):
        """Record the chapters of the fanfic"""
        # need to add /?bypass=1 to url
        for chapter in self.chapter_list:
            time.sleep(self._chapter_sleep_time)
            self.log_debug("Downloading chapter:" + chapter['name'])
            url_fixed = urlunparse(self._url_obj._replace(path=chapter['link'], query='bypass=1'))

            # get page
            page = requests.get(url_fixed)
            self._soup = BeautifulSoup(page.text, features="html.parser")
            story = self._soup.find(id='story')

            story_container = story.find_all(True, {'class': 'story'})[0]
            # remove the pager elements at the top and bottom
            for element in story_container.find_all(True, {'class': 'pager'}):
                element.decompose()
            # remove the 'well' block at the top
            for element in story_container.find_all(True, {'class': 'well'}):
                element.decompose()

            chapter_object = Chapter()
            chapter_object.raw_body = story_container.prettify()
            chapter_object.word_count = len(story.text.split())
            chapter_object.name = chapter['name']
            self._fanfic.add_chapter(chapter_object)
