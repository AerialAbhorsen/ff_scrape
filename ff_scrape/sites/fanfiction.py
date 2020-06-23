from ff_scrape.storybase import Chapter
from ff_scrape.errors import URLError
from ff_scrape.fanficsite import Site
from ff_scrape.standardization import *
from urllib.parse import urljoin
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
import time


class Fanfiction(Site):
    """Provides the logic to parse fanfics from fanfiction.net"""

    def __init__(self, site_params=[]):
        super().__init__(logger_name='ff_scrape.site.Fanfiction',
                         site_params=site_params)

    def set_domain(self):
        """Sets the domain of the fanfic to Fanfiction.net"""
        self._fanfic.domain = "Fanfiction.net"

    def can_handle(self, url):
        if 'fanfiction.net/' in url:
            return True
        return False

    def correct_url(self, url):
        """Perform the necessary steps to correct the supplied _url so the parser can work with it"""
        # check if _url has "https://" or "http://" prefix
        if "http://" not in url:
            if "https://" not in url:
                url = "http://%s" % url
        _url_split = url.split("/")
        #correct for https
        if _url_split[0] == 'http:':
            _url_split[0] = "https:"
        # correct for mobile _url
        if _url_split[2] == "m.fanfiction.net":
            _url_split[2] = "www.fanfiction.net"
        # correct _url as needed for script
        if _url_split[4] == '':
            raise URLError('No Story ID given')
        # adds chapter id is 1 and trailing /
        if len(_url_split) == 5:
            _url_split.append('1')
            _url_split.append('')
        # sets chapter id to 1 and trailing /
        elif len(_url_split) == 6:
            _url_split[5] = '1'
            _url_split.append('')
        # sets chapter id to 1 and removes chapter title
        elif len(_url_split) == 7:
            _url_split[5] = '1'
            _url_split[6] = ''
        else:
            raise URLError('Unknown url format')
        url = '/'.join(_url_split)
        tmp = urljoin(url, ' ')[0:-2]
        return tmp

    def check_story_exists(self):
        """Verify that the fanfic exists"""
        warning = self._soup.findAll("div", {"class": "panel_warning"})
        if len(warning) == 1:
            return False
        return True

    def record_story_metadata(self):
        """Record the metadata of the fanfic"""

        # get section of code where the universe is listed
        story_group, universe_tag = self._soup.find('div', {'id': 'pre_story_links'}).find_all('a', href=True)
        # check if it is a crossover type
        universe_str = universe_tag.string.replace(" Crossover", "")
        for universe in universe_str.split(" + "):
            self._fanfic.add_universe(universe)


        top_profile = self._soup.find(id="profile_top")

        # record title and author
        self._fanfic.title = top_profile.b.string
        self._fanfic.author = top_profile.a.string
        author_url = "http://fanfiction.net" + top_profile.a.attrs['href']
        # need to remove author name from url in case author changes their name in the future
        matching = re.match(r'(.*\d+)\/?.*', author_url)
        self._fanfic.author_url = matching.group(1)

        # record summary
        self._fanfic.summary = top_profile.find('div', attrs={'class': 'xcontrast_txt'}).string

        # record published and updated timestamps
        times = top_profile.find_all(attrs={'data-xutime': True})
        self._fanfic.published = datetime.fromtimestamp(int(times[0]['data-xutime']))
        if len(times) == 1:
            self._fanfic.updated = datetime.fromtimestamp(int(times[0]['data-xutime']))
        elif len(times) == 2:
            self._fanfic.updated = datetime.fromtimestamp(int(times[1]['data-xutime']))

        # record rating
        rating_tag = top_profile.find('a', {'target': 'rating'})
        rating_split = rating_tag.string.split(" ")
        self._fanfic.rating = standardize_rating(rating_split[1])

        # the remaining attributes need to be positionally extracted from story meta
        metadata_tags = self._soup.find('span', {'class': 'xgray xcontrast_txt'})
        metadata = [s.strip() for s in metadata_tags.text.split('-')]
        self._fanfic.add_genre(standardize_genre(metadata[2]))
        if 'Complete' in metadata:
            self._fanfic.status = 'Complete'
        else:
            self._fanfic.status = 'WIP'

        # extract people and pairings
        people_str = metadata[3]
        pairing_match = re.compile(r'(\[.*?\])')
        for pairing in pairing_match.findall(people_str):
            pairing = pairing.replace('[', '').replace(']', '')
            pairing_arr = pairing.split(', ')
            for person in pairing_arr:
                self._fanfic.add_character(standardize_character(person))
            self._fanfic.add_pairing(pairing_arr)
        non_pairing = pairing_match.sub('', people_str)
        non_pairing = non_pairing.strip()
        for person in non_pairing.split(', '):
            self._fanfic.add_character(standardize_character(person))

    def record_story_chapters(self):
        """Record the chapters of the fanfic"""
        chapters = self._soup.find(id='chap_select').contents

        # get the chapters
        for chapter in chapters:
            time.sleep(self._chapter_sleep_time)
            chapter_object = Chapter()
            self.log_debug("Downloading chapter: " + chapter.attrs['value'])
            page = requests.get(self._url[0:-1]+chapter['value'])
            self._soup = BeautifulSoup(page.text, features="html.parser")
            chapter_text = ""
            chapter_count = 0
            story_tag = self._soup.find(id="storytextp")
            for content in story_tag.find_all(['p', 'hr']):
                chapter_text += content.prettify()
                chapter_count += len(content.text.split())
            chapter_object.raw_body = chapter_text
            chapter_object.word_count = chapter_count
            chapter_object.name = chapter.text
            self._fanfic.add_chapter(chapter_object)
