import unittest
from ff_scrape.sites.hpfanficarchive import HPFanficArchive
from ff_scrape.storybase import Story
from bs4 import BeautifulSoup


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = HPFanficArchive()
        url = "placeholder_url"
        self.fanfiction._url = url
        self.fanfiction._fanfic = Story(url)

    def test_metadata_story1(self):
        self.fanfiction._url = 'http://www.hpfanficarchive.com/stories/viewstory.php?sid=270'
        page = open('data/good_story.html', 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Harry Potter'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 62525, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Enter the Silver Flame - Year 1: On Happy Ripples and Unexpected Meetings', 'Title is correct')
        self.assertEqual(fanfic.author, 'SamStone', 'Author is correct')
        self.assertEqual(fanfic.author_url, 'http://www.hpfanficarchive.com/stories/viewuser.php?uid=587', 'Author URL is correct')
        summary = "This story came to mind in the form of two questions: What would it have been like for Harry to have learned of magic before Hogwarts a different magic? What would it have been like for Harry if he had been in a different house? This story explores an alternate view of Harry’s life and one of three choices."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'NC-17', 'Rating is correct')
        self.assertEqual(fanfic.status, 'Complete', 'Status is correct')
        self.assertEqual(len(fanfic.pairings), 3, "There is three pairing")
        self.assertEqual(len(fanfic.pairings[0]), 2, "Pairing has two members")
        self.assertIn('Harry', fanfic.pairings[0], "First member present 1")
        self.assertIn('Hermione', fanfic.pairings[0], "Second member present 1")
        self.assertIn('Harry', fanfic.pairings[1], "First member present 2")
        self.assertIn('OC', fanfic.pairings[1], "Second member present 2")
        self.assertIn('Harry', fanfic.pairings[2], "First member present 3")
        self.assertIn('Tonks', fanfic.pairings[2], "Second member present 3")
        self.assertEqual(len(fanfic.characters), 3, 'There are three characters')
        self.assertIn('Harry James Potter', fanfic.characters, "First member present")
        self.assertIn('Hermione Granger', fanfic.characters, "Second member present")
        self.assertIn('Nymphadora Tonks', fanfic.characters, "Third member present")
        self.assertEqual(len(fanfic.genres), 6, "Genre length is correct")
        self.assertIn("Adult", fanfic.genres, "First member is present")
        self.assertIn("AU", fanfic.genres, "Second member is present")
        self.assertIn("Dark", fanfic.genres, "Third member is present")
        self.assertIn("Erotica", fanfic.genres, "Fourth member is present")
        self.assertIn("Horror", fanfic.genres, "Fifth member is present")
        self.assertIn("Multiple Partners", fanfic.genres, "Sixth member is present")
        self.assertEqual(len(fanfic.warnings), 4, "Warning length is correct")
        self.assertIn("Abuse/Torture", fanfic.warnings, "First member is present")
        self.assertIn("Adult Themes", fanfic.warnings, "Second member is present")
        self.assertIn("Extreme Sexual Situations", fanfic.warnings, "Third member is present")
        self.assertIn("Extreme violence", fanfic.warnings, "Fourth member is present")

        self.assertEqual(len(fanfic.categories), 7, "Category length is correct")
        self.assertIn("Erotica", fanfic.categories, "First member is present")
        self.assertIn("Harem/Multi pairing", fanfic.categories, "Second member is present")
        self.assertIn("Necromancy", fanfic.categories, "Third member is present")
        self.assertIn("Dark or Evil", fanfic.categories, "Fourth member is present")
        self.assertIn("Dark Fic/Character", fanfic.categories, "Fifth member is present")
        self.assertIn("Powerful", fanfic.categories, "Sixth member is present")
        self.assertIn("Cunning, resourceful and ambitious", fanfic.categories, "Seventh member is present")
        self.assertEqual(fanfic.updated.isoformat(), '2012-03-04T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2009-03-29T00:00:00', 'Updated timestamp is correct')

    def test_metadata_story2(self):
        self.fanfiction._url = 'http://www.hpfanficarchive.com/stories/viewstory.php?sid=471'
        page = open('data/good_story2.html', 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Harry Potter'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 19528, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'The Mercenary of Hogwarts', 'Title is correct')
        self.assertEqual(fanfic.author, "DanteTheRaven", 'Author is correct')
        self.assertEqual(fanfic.author_url, 'http://www.hpfanficarchive.com/stories/viewuser.php?uid=1581', 'Author URL is correct')
        summary = "A young Harry is taken in by a street gang and trained in their art. Now a new highly sought after contractor is spreading throughout both the wizarding and muggle world."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'R', 'Rating is correct')
        self.assertEqual(fanfic.status, 'WIP', 'Status is correct')
        self.assertEqual(len(fanfic.pairings), 1, "There is three pairing")
        self.assertEqual(len(fanfic.pairings[0]), 2, "Pairing has two members")
        self.assertIn('Harry', fanfic.pairings[0], "First member present 1")
        self.assertIn('Tonks', fanfic.pairings[0], "Second member present 1")
        self.assertEqual(len(fanfic.characters), 3, 'There are three characters')
        self.assertIn('Harry James Potter', fanfic.characters, "First member present")
        self.assertIn('Daphne Greengrass', fanfic.characters, "Second member present")
        self.assertIn('Nymphadora Tonks', fanfic.characters, "Third member present")
        self.assertEqual(len(fanfic.genres), 5, "Genre length is correct")
        self.assertIn("Adventure/Action", fanfic.genres, "First member is present")
        self.assertIn("AU", fanfic.genres, "Second member is present")
        self.assertIn("Dark", fanfic.genres, "Third member is present")
        self.assertIn("Drama", fanfic.genres, "Fourth member is present")
        self.assertIn("Suspense", fanfic.genres, "Fifth member is present")
        self.assertEqual(len(fanfic.warnings), 2, "Warning length is correct")
        self.assertIn("Adult Themes", fanfic.warnings, "First member is present")
        self.assertIn("Strong Violence", fanfic.warnings, "Second member is present")

        self.assertEqual(len(fanfic.categories), 4, "Category length is correct")
        self.assertIn("Drama", fanfic.categories, "First member is present")
        self.assertIn("Dark or Evil", fanfic.categories, "Second member is present")
        self.assertIn("Dark Fic/Character", fanfic.categories, "Third member is present")
        self.assertIn("Main character at Ravenclaw", fanfic.categories, "Fourth member is present")
        self.assertEqual(fanfic.updated.isoformat(), '2012-06-24T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2011-01-13T00:00:00', 'Updated timestamp is correct')


if __name__ == '__main__':
    unittest.main()
