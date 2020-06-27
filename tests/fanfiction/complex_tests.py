import unittest
from ff_scrape.sites.fanfiction import Fanfiction
from ff_scrape.storybase import Story
from bs4 import BeautifulSoup
from os.path import dirname, join


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = Fanfiction()
        url = "placeholder_url"
        self.fanfiction._url = url
        self.fanfiction._fanfic = Story(url)
        self.dir = dirname(__file__)

    def test_metadata_story1(self):
        file = join(self.dir, 'data', 'good_story.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Naruto'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 68474, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Naruto Guardian Of The Mist', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, 'SSJ3 Kyuubi Gohan', 'Author is correct')
        self.assertEqual(authors[0].url, 'https://www.fanfiction.net/u/3058796/', 'Author URL is correct')
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

        chapter_list = [
            {'link': '1', 'name': '1. Banishment'},
            {'link': '2', 'name': "2. Naruto's Growth"},
            {'link': '3', 'name': '3. Pain'},
            {'link': '4', 'name': '4. Darkness'},
            {'link': '5', 'name': '5. The Penultimate Battle'},
            {'link': '6', 'name': '6. For Peace or Revenge'},
            {'link': '7', 'name': '7. Burn Once More'},
            {'link': '8', 'name': '8. Changes'},
            {'link': '9', 'name': '9. Half-dozen'},
            {'link': '10', 'name': '10. Intel'},
            {'link': '11', 'name': '11. Blood versus water'},
            {'link': '12', 'name': '12. Foes of tomorrow'}
        ]
        self.assertEqual(chapter_list, self.fanfiction.chapter_list, 'Chapter list is correct')

    def test_metadata_story2(self):
        file = join(self.dir, 'data', 'good_story2.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Harry Potter'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 55730, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Why We fight', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, "W'rkncacnter", 'Author is correct')
        self.assertEqual(authors[0].url, 'https://www.fanfiction.net/u/111583/', 'Author URL is correct')
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

        chapter_list = [
            {'link': '1', 'name': '1. Chapter 1'},
            {'link': '2', 'name': "2. Chapter 2"},
            {'link': '3', 'name': '3. Chapter 3'},
            {'link': '4', 'name': '4. Chapter 4'},
            {'link': '5', 'name': '5. Chapter 5'},
            {'link': '6', 'name': '6. Chapter 6'},
            {'link': '7', 'name': '7. Chapter 7'},
            {'link': '8', 'name': '8. Chapter 8'}
        ]
        self.assertEqual(chapter_list, self.fanfiction.chapter_list, 'Chapter list is correct')

    def test_metadata_story3(self):
        file = join(self.dir, 'data', 'good_story3.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(len(fanfic.universe), 2, "Universe length is correct")
        self.assertIn("Harry Potter", fanfic.universe, "First member is present")
        self.assertIn("Chronicles of Narnia", fanfic.universe, "Second member is present")
        self.assertEqual(len(fanfic.raw_index_page), 53996, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Fifth King, Lost Queen', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, "Pinion King", 'Author is correct')
        self.assertEqual(authors[0].url, 'https://www.fanfiction.net/u/1105550/', 'Author URL is correct')
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

        chapter_list = [
            {'link': '1', 'name': '1. Chapter 1'},
            {'link': '2', 'name': "2. Chapter 2"},
            {'link': '3', 'name': '3. Chapter 3'},
            {'link': '4', 'name': '4. Chapter 4'},
            {'link': '5', 'name': '5. Chapter 5'},
            {'link': '6', 'name': '6. Chapter 6'},
            {'link': '7', 'name': '7. Chapter 7'},
            {'link': '8', 'name': '8. Chapter 8'},
            {'link': '9', 'name': '9. Chapter 9'},
            {'link': '10', 'name': '10. Chapter 10'},
            {'link': '11', 'name': '11. Chapter 11'},
            {'link': '12', 'name': '12. Chapter 12'},
            {'link': '13', 'name': '13. Chapter 13'}
        ]
        self.assertEqual(chapter_list, self.fanfiction.chapter_list, 'Chapter list is correct')

    def test_metadata_story4(self):
        file = join(self.dir, 'data', 'good_story4.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Harry Potter'], "Universe is correct")
        self.assertEqual(len(fanfic.raw_index_page), 66176, 'Raw index page length correct')
        self.assertEqual(fanfic.title, "Harry Potter and the Unicorn's Curse", 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, "Really Frozen Phoenix", 'Author is correct')
        self.assertEqual(authors[0].url, 'https://www.fanfiction.net/u/801129/', 'Author URL is correct')
        summary = "Itâ€™s the end of sixth year at Hogwarts for Harry Potter and he can safely say that itâ€™s been the most relaxed year despite the war with Lord Voldemort. Calm doesnâ€™t last long, however, and he knows that the storm is on itâ€™s way. HP/femBZ. AU."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'M', 'Rating is correct')
        self.assertEqual(fanfic.status, 'WIP', 'Status is correct')
        self.assertEqual(len(fanfic.pairings), 0, "There is no pairings")
        self.assertEqual(len(fanfic.characters), 2, 'There are two characters')
        self.assertIn('Harry P.', fanfic.characters, "First member present")
        self.assertIn('Blaise Z.', fanfic.characters, "Second member present")
        self.assertEqual(fanfic.genres, ['Adventure'], "Genre is correct")
        self.assertEqual(fanfic.published.isoformat(), '2008-04-13T21:43:53', 'Published timestamp is correct')
        self.assertEqual(fanfic.updated.isoformat(), '2008-04-13T21:43:53', 'Updated timestamp is correct')

        chapter_list = [
            {'link': '1', 'name': "Harry Potter and the Unicorn's Curse"}
        ]
        self.assertEqual(chapter_list, self.fanfiction.chapter_list, 'Chapter list is correct')


if __name__ == '__main__':
    unittest.main()
