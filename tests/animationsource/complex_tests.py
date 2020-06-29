import unittest
from ff_scrape.sites.animationsource import AnimationSource
from ff_scrape.storybase import Story
from bs4 import BeautifulSoup
from os.path import dirname, join


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = AnimationSource()
        url = "placeholder_url"
        self.fanfiction._url = url
        self.fanfiction._fanfic = Story(url)
        self.dir = dirname(__file__)
        self.fanfiction._fandom = 'balto'

    def test_metadata_story1(self):
        self.fanfiction._url = 'https://www.animationsource.org/balto/en/view_fanfic/An-Unexpected-Future-Aleu-Part-IV/53773.html'
        file = join(self.dir, 'data', 'good_story.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Balto'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 24344, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'An Unexpected Future - Aleu: Part IV', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, "Juuchan17", 'Author is correct')
        self.assertEqual(authors[0].url, 'https://www.animationsource.org/balto/en/fanfic/Juuchan17/3746.html', 'Author URL is correct')
        summary = "A mysterious prisoner has been captured, but are Aleu's nervous hunches correct - is it really her father? Aleu's tale has reached a near-climax as a daughter will learn the truth about the one she never knew and the heroic story of how Balto met and won the love of his life. Now, Aleu must discover who she is, but where is she meant to be - the wolf that flows through her veins or the daughter that her father wants back at home? (The Finale is coming soon!)"
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'PG', 'Rating is correct')
        self.assertEqual(fanfic.status, 'Completed', 'Status is correct')
        self.assertEqual(len(fanfic.warnings), 0, "Warning length is correct")

        genres = ["Epic"]
        self.assertEqual(len(fanfic.genres), len(genres), "Category length is correct")
        for genre in genres:
            self.assertIn(genre, fanfic.genres, "'{}' is present".format(genre))

        pairings = []
        self.assertEqual(len(fanfic.pairings), len(pairings), "Warning length is correct")
        for index, pairing in enumerate(pairings, start=0):
            self.assertEqual(len(pairing), len(fanfic.pairings[index]), "Pairing {} length is correct".format(index))
            for person in pairing:
                self.assertIn(person, fanfic.pairings[index], "'{}' is present in pairing {}".format(person, index))

        characters = []
        self.assertEqual(len(fanfic.characters), len(characters), 'There are correct number of characters')
        for character in characters:
            self.assertIn(character, fanfic.characters, "'{}' is present".format(character))
        categories = []
        self.assertEqual(len(fanfic.categories), len(categories), "Category length is correct")
        for category in categories:
            self.assertIn(category, fanfic.categories, "'{}' is present".format(category))

        self.assertEqual(fanfic.updated.isoformat(), '2008-03-06T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2008-03-06T00:00:00', 'Updated timestamp is correct')

    def test_metadata_story2(self):
        self.fanfiction._url = 'https://www.animationsource.org/balto/en/view_fanfic/Balto-s-Inside-Story-The-Family-Expands/263740.html'
        file = join(self.dir, 'data', 'good_story2.html')
        page = open(file, 'r', encoding='utf8')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Balto'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 36104, 'Raw index page length correct')
        self.assertEqual(fanfic.title, "Balto's Inside Story: The Family Expands", 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, "WolfDan", 'Author is correct')
        self.assertEqual(authors[0].url, 'https://www.animationsource.org/balto/en/fanfic/WolfDan/32020.html', 'Author URL is correct')
        summary = """Part of 4 of 7 of my fanfic BIS!
After returning to Nome, Aleu and her friend Kenai were welcome to everyone, but is it everyone? After one team wins the final race, one of the dogs gets badly injured by the opponents, so it's up to the teammate to take care of the injured! How will the others gain the loves of their friends. Easy way of hard way? Just a night before he becomes a grandfather, Balto's visited by someone he did not expect!
Rated G for all audiences!"""
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'G', 'Rating is correct')
        self.assertEqual(fanfic.status, 'Completed', 'Status is correct')
        self.assertEqual(len(fanfic.warnings), 0, "Warning length is correct")

        genres = ["Epic"]
        self.assertEqual(len(fanfic.genres), len(genres), "Category length is correct")
        for genre in genres:
            self.assertIn(genre, fanfic.genres, "'{}' is present".format(genre))

        pairings = []
        self.assertEqual(len(fanfic.pairings), len(pairings), "Warning length is correct")
        for index, pairing in enumerate(pairings, start=0):
            self.assertEqual(len(pairing), len(fanfic.pairings[index]), "Pairing {} length is correct".format(index))
            for person in pairing:
                self.assertIn(person, fanfic.pairings[index], "'{}' is present in pairing {}".format(person, index))

        characters = ['Aleu', 'Jenna', 'Luk', 'Muk', 'Nikki', 'Boris', 'Star', 'Dusty', 'Mr. Simpson', 'Kodi', 'Kaltag',
                      'Balto', 'Duke', 'Kirby', 'Ralph', 'Stella']
        self.assertEqual(len(fanfic.characters), len(characters), 'There are correct number of characters')
        for character in characters:
            self.assertIn(character, fanfic.characters, "'{}' is present".format(character))
        categories = []
        self.assertEqual(len(fanfic.categories), len(categories), "Category length is correct")
        for category in categories:
            self.assertIn(category, fanfic.categories, "'{}' is present".format(category))

        self.assertEqual(fanfic.updated.isoformat(), '2017-01-06T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2017-01-06T00:00:00', 'Updated timestamp is correct')


if __name__ == '__main__':
    unittest.main()
