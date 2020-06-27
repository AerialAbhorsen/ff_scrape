import unittest
from ff_scrape.sites.fanficauthors import FanficAuthors
from ff_scrape.storybase import Story
from bs4 import BeautifulSoup
from os.path import dirname, join
from urllib.parse import urlparse


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = FanficAuthors()
        url = "placeholder_url"
        self.fanfiction._url = url
        self.fanfiction._fanfic = Story(url)
        self.dir = dirname(__file__)
        self.maxDiff = None

    def test_metadata_story1(self):
        self.fanfiction._url = 'https://deluded-musings.fanficauthors.net/A_Matter_of_Perspective/Mirror_Mirror/'
        self.fanfiction._url_obj = urlparse(self.fanfiction._url)
        file = join(self.dir, 'data', 'good_story.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, [], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 8886, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'A Matter of Perspective', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, 'Clell65619', 'Author is correct')
        self.assertEqual(authors[0].url, 'https://deluded-musings.fanficauthors.net', 'Author URL is correct')
        summary = "One of the Magical World's most powerful creations is the Mirror of Erised. Â But that isn't the only magical mirror in the world."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'E', 'Rating is correct')
        self.assertEqual(fanfic.status, 'Completed', 'Status is correct')
        self.assertEqual(fanfic.pairings, [], "There is no pairing")
        self.assertEqual(len(fanfic.characters), 0, 'There is no characters')
        self.assertEqual(fanfic.genres, ['One Shots'], "Genre is correct")
        self.assertEqual(len(fanfic.warnings), 0, "Warning length is correct")
        self.assertEqual(len(fanfic.categories), 0, "Category length is correct")
        self.assertEqual(fanfic.updated.isoformat(), '2013-06-01T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2013-06-01T00:00:00', 'Updated timestamp is correct')

        chapter_list = [
            {'link': '/A_Matter_of_Perspective/Mirror_Mirror/', 'name': 'A Matter of Perspective :: Mirror Mirror'},
        ]
        self.assertEqual(chapter_list, self.fanfiction.chapter_list, 'Chapter list is correct')

    def test_metadata_story2(self):
        self.fanfiction._url = 'https://jeconais.fanficauthors.net/Hope/index/'
        self.fanfiction._url_obj = urlparse(self.fanfiction._url)
        file = join(self.dir, 'data', 'good_story2.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, [], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 14478, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Hope', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, 'Jeconais', 'Author is correct')
        self.assertEqual(authors[0].url, 'https://jeconais.fanficauthors.net', 'Author URL is correct')
        summary = "A man who is lost in his own country.Â  A girl who needs her mate to survive.Â  A tale of Quidditch and romance, of anger and betrayal, of friendship and enmity.Â  A story of the power of hope."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'T', 'Rating is correct')
        self.assertEqual(fanfic.status, 'Completed', 'Status is correct')
        self.assertEqual(fanfic.pairings, [], "There is no pairing")
        self.assertEqual(len(fanfic.characters), 0, 'There is no characters')
        self.assertEqual(fanfic.genres, ['Action/Adventure', 'Fluff'], "Genre is correct")
        self.assertEqual(len(fanfic.warnings), 0, "Warning length is correct")
        self.assertEqual(len(fanfic.categories), 0, "Category length is correct")
        self.assertEqual(fanfic.updated.isoformat(), '2007-05-30T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2005-05-06T00:00:00', 'Updated timestamp is correct')

        chapter_list = [
            {'link': '/Hope/1__Beauxbatons/', 'name': 'Hope :: 1 - Beauxbatons'},
            {'link': '/Hope/2__Paris/', 'name': 'Hope :: 2 - Paris'},
            {'link': '/Hope/3__Normandy/', 'name': 'Hope :: 3 - Normandy'},
            {'link': '/Hope/4__Ilfracombe/', 'name': 'Hope :: 4 - Ilfracombe'},
            {'link': '/Hope/5__Barcelona/', 'name': 'Hope :: 5 - Barcelona'},
            {'link': '/Hope/6__Tintagel/', 'name': 'Hope :: 6 - Tintagel'},
            {'link': '/Hope/7__Milan/', 'name': 'Hope :: 7 - Milan'},
            {'link': '/Hope/8__Hogwarts/', 'name': 'Hope :: 8 - Hogwarts'},
            {'link': '/Hope/9__London/', 'name': 'Hope :: 9 - London'},
            {'link': '/Hope/10__Antwerp/', 'name': 'Hope :: 10 - Antwerp'},
            {'link': '/Hope/11__Sydney/', 'name': 'Hope :: 11 - Sydney'},
            {'link': '/Hope/12__London2/', 'name': 'Hope :: 12 - London(2)'}
        ]
        self.assertEqual(chapter_list, self.fanfiction.chapter_list, 'Chapter list is correct')


if __name__ == '__main__':
    unittest.main()
