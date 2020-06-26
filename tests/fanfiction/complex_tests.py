import unittest
from ff_scrape.sites.fanfiction import Fanfiction
from ff_scrape.storybase import Story
from bs4 import BeautifulSoup


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = Fanfiction()
        self.fanfiction._fanfic = Story("placeholder_url")

    def test_metadata_story1(self):
        page = open('data/good_story.html', 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Naruto'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 97586, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Naruto Guardian Of The Mist', 'Title is correct')
        self.assertEqual(fanfic.author, 'SSJ3 Kyuubi Gohan', 'Author is correct')
        self.assertEqual(fanfic.author_url, 'https://www.fanfiction.net/u/3058796/', 'Author URL is correct')
        summary = "Banished as soon as Tsunade is brought back to The Leaf, Naruto is at a loss of what to do. However with Kakashi testing his affinities, Naruto finds he has more power than he ever thought. Watch Naruto's journey as he learns about himself and becomes The Guardian Of The Mist. Ice, lava and boil release Naruto and maybe wood later on. Semi-dark, grey smart, and strong Naruto. Harem"
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'M', 'Rating is correct')
        self.assertEqual(fanfic.status, 'WIP', 'Status is correct')
        self.assertEqual(len(fanfic.pairings), 1, "There is one pairing")
        self.assertEqual(len(fanfic.pairings[0]), 3, "Pairing has three members")
        self.assertIn('Naruto U.', fanfic.pairings[0], "First member present")
        self.assertIn('Mei T.', fanfic.pairings[0], "Second member present")
        self.assertIn('Ameyuri R.', fanfic.pairings[0], "Third member present")
        self.assertEqual(len(fanfic.characters), 3, 'There are three characters')
        self.assertIn('Naruto U.', fanfic.characters, "First member present")
        self.assertIn('Mei T.', fanfic.characters, "Second member present")
        self.assertIn('Ameyuri R.', fanfic.characters, "Third member present")
        self.assertEqual(len(fanfic.genres), 2, "Genre length is correct")
        self.assertIn("Adventure", fanfic.genres, "First member is present")
        self.assertIn("Romance", fanfic.genres, "Second member is present")
        self.assertEqual(fanfic.updated.isoformat(), '2020-05-15T23:02:33', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2012-09-08T19:10:27', 'Updated timestamp is correct')

    def test_metadata_story2(self):
        page = open('data/good_story2.html', 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Harry Potter'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 55079, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Why We fight', 'Title is correct')
        self.assertEqual(fanfic.author, "W'rkncacnter", 'Author is correct')
        self.assertEqual(fanfic.author_url, 'https://www.fanfiction.net/u/111583/', 'Author URL is correct')
        summary = "Voldemort Waited two years to attack the Potter's.  Harry has two sister who are twins, the world thinks it was Sarah.  The World is Wrong.  HarryGinny, but only later on."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'T', 'Rating is correct')
        self.assertEqual(fanfic.status, 'WIP', 'Status is correct')
        self.assertEqual(len(fanfic.pairings), 0, "There is no pairings")
        self.assertEqual(len(fanfic.characters), 2, 'There are two characters')
        self.assertIn('Harry P.', fanfic.characters, "First member present")
        self.assertIn('Ginny W.', fanfic.characters, "Second member present")
        self.assertEqual(fanfic.genres, ["Adventure"], "Genre length is correct")
        self.assertEqual(fanfic.published.isoformat(), '2004-04-23T22:51:44', 'Published timestamp is correct')
        self.assertEqual(fanfic.updated.isoformat(), '2005-02-06T01:17:33', 'Updated timestamp is correct')

    def test_metadata_story3(self):
        page = open('data/good_story3.html', 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(len(fanfic.universe), 2, "Universe length is correct")
        self.assertIn("Harry Potter", fanfic.universe, "First member is present")
        self.assertIn("Chronicles of Narnia", fanfic.universe, "Second member is present")
        self.assertEqual(len(fanfic.raw_index_page), 53563, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Fifth King, Lost Queen', 'Title is correct')
        self.assertEqual(fanfic.author, "Pinion King", 'Author is correct')
        self.assertEqual(fanfic.author_url, 'https://www.fanfiction.net/u/1105550/', 'Author URL is correct')
        summary = "The cost of victory over Voldemort was his death. Now Harry starts a new adventure, this one in the land of Narnia where he works with the Pevensie's against a new threat, there is evil forming on the horizon. But first the lost queen must return."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'T', 'Rating is correct')
        self.assertEqual(fanfic.status, 'WIP', 'Status is correct')
        self.assertEqual(len(fanfic.pairings), 0, "There is no pairings")
        self.assertEqual(len(fanfic.characters), 2, 'There are two characters')
        self.assertIn('Harry P.', fanfic.characters, "First member present")
        self.assertIn('Susan Pevensie', fanfic.characters, "Second member present")
        self.assertEqual(len(fanfic.genres), 2, "Genre length is correct")
        self.assertIn("Adventure", fanfic.genres, "First member is present")
        self.assertIn("Romance", fanfic.genres, "Second member is present")
        self.assertEqual(fanfic.published.isoformat(), '2008-05-02T05:18:29', 'Published timestamp is correct')
        self.assertEqual(fanfic.updated.isoformat(), '2015-10-31T21:58:29', 'Updated timestamp is correct')


if __name__ == '__main__':
    unittest.main()
