import unittest
from ff_scrape.sites.archiveofourown import ArchiveofOurOwn
from ff_scrape.storybase import Story
from bs4 import BeautifulSoup
from os.path import dirname, join


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = ArchiveofOurOwn()
        url = "placeholder_url"
        self.fanfiction._url = url
        self.fanfiction._fanfic = Story(url)
        self.dir = dirname(__file__)

    def test_metadata_story1(self):
        file = join(self.dir, 'data', 'good_story.html')
        page = open(file, 'r', encoding='utf8')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Naruto'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 726228, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'An Empire to Conquer Your Heart', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 2, 'Length of authors is correct')
        self.assertEqual(authors[0].name, "celestia193", 'Author is correct')
        self.assertEqual(authors[0].url, 'https://archiveofourown.org/users/celestia193/pseuds/celestia193', 'Author URL is correct')
        self.assertEqual(authors[1].name, "SilverKitsune2017", 'Author is correct')
        self.assertEqual(authors[1].url, 'https://archiveofourown.org/users/SilverKitsune2017/pseuds/SilverKitsune2017', 'Author URL is correct')
        summary = "Long ago, their love of battle drove a wedge between the Chikara and the peaceful Bijin. Now Madara, the Chikara king, seeks to unite a galaxy under his rule, and his first point of conquest is the fertile Bijin homeworld. But the most unexpected part of his conquest? A fearless Bijin with a Chikara’s instincts whose goal is to kill him."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'Explicit', 'Rating is correct')
        self.assertEqual(fanfic.status, 'WIP', 'Status is correct')
        self.assertEqual(len(fanfic.genres), 0, "Genre length is correct")
        self.assertEqual(len(fanfic.warnings), 0, "Warning length is correct")

        pairings = [
            ['Uchiha Izuna', 'Uchiha Madara'],
        ]
        self.assertEqual(len(fanfic.pairings), len(pairings), "Warning length is correct")
        for index, pairing in enumerate(pairings, start=0):
            self.assertEqual(len(pairing), len(fanfic.pairings[index]), "Pairing {} length is correct".format(index))
            for person in pairing:
                self.assertIn(person, fanfic.pairings[index], "'{}' is present in pairing {}".format(person, index))

        characters = ['Uchiha Madara', 'Uchiha Izuna', 'Uchiha Naori']
        self.assertEqual(len(fanfic.characters), len(characters), 'There are correct number of characters')
        for character in characters:
            self.assertIn(character, fanfic.characters, "'{}' is present".format(character))
        categories = ["M/M", "Romance", "Alternate Universe - Science Fiction", "Mpreg", 'Alien Biology',
                      'Tail Sex', 'Alien Culture']
        self.assertEqual(len(fanfic.categories), len(categories), "Category length is correct")
        for category in categories:
            self.assertIn(category, fanfic.categories, "'{}' is present".format(category))

        self.assertEqual(fanfic.updated.isoformat(), '2020-06-27T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2019-11-27T00:00:00', 'Updated timestamp is correct')

    def test_metadata_story2(self):
        file = join(self.dir, 'data', 'good_story2.html')
        page = open(file, 'r', encoding='utf8')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Harry Potter'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 135432, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Freedom Found in Love', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, "babyvfan", 'Author is correct')
        self.assertEqual(authors[0].url, 'https://archiveofourown.org/users/babyvfan/pseuds/babyvfan', 'Author URL is correct')
        summary = "*Future-ish spinoff companion to SensiblyTainted's story, Freedom Found in Defiance* Harry had known, even at the age of eleven, just as he did at the age of six when they first met, that Draco would make his promise, their dream happened. And, hearing the swell of music down below, seeing him dressed in white, it will actually come to be."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'M', 'Rating is correct')
        self.assertEqual(fanfic.status, 'Completed', 'Status is correct')
        self.assertEqual(len(fanfic.genres), 0, "Genre length is correct")
        self.assertEqual(len(fanfic.warnings), 0, "Warning length is correct")

        pairings = [
            ['Draco Malfoy', 'Harry Potter'],
        ]
        self.assertEqual(len(fanfic.pairings), len(pairings), "Warning length is correct")
        for index, pairing in enumerate(pairings, start=0):
            self.assertEqual(len(pairing), len(fanfic.pairings[index]), "Pairing {} length is correct".format(index))
            for person in pairing:
                self.assertIn(person, fanfic.pairings[index], "'{}' is present in pairing {}".format(person, index))

        characters = ['Draco Malfoy', 'Harry Potter', 'Hermione Granger', 'Neville Longbottom',
                      'Narcissa Black Malfoy', 'Andromeda Black Tonks']
        self.assertEqual(len(fanfic.characters), len(characters), 'There are correct number of characters')
        for character in characters:
            self.assertIn(character, fanfic.characters, "'{}' is present".format(character))
        categories = ["M/M", "Weddings", "Wedding Day", "Draco and Harry's wedding", 'True Mates',
                      'Implied/Referenced Child Abuse', 'Past Child Abuse', 'briefly mentioned',
                      "Isn't the main theme of story", "Genderfluid Harry", 'Crossdressing Harry', 'Psychic Bond',
                      'Mating Bond']
        self.assertEqual(len(fanfic.categories), len(categories), "Category length is correct")
        for category in categories:
            self.assertIn(category, fanfic.categories, "'{}' is present".format(category))

        self.assertEqual(fanfic.updated.isoformat(), '2020-06-27T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2020-06-27T00:00:00', 'Updated timestamp is correct')

    def test_metadata_story3(self):
        file = join(self.dir, 'data', 'good_story3.html')
        page = open(file, 'r', encoding='utf8')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Harry Potter'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 429179, 'Raw index page length correct')
        self.assertEqual(fanfic.title, 'Through Your Silver Eyes', 'Title is correct')
        authors = fanfic.authors
        self.assertEqual(len(authors), 1, 'Length of authors is correct')
        self.assertEqual(authors[0].name, "Amora0819", 'Author is correct')
        self.assertEqual(authors[0].url, 'https://archiveofourown.org/users/Amora0819/pseuds/Amora0819', 'Author URL is correct')
        summary = "Everyone sees what they want to see and what they wanted to see was Malfoy and Potter at each other's throats, but they weren't really, but that's a secret that ended the day of the  sectumsempra incident , one that Draco doesn't seem to remember and Harry simply can't forget. What's worse is Jashua Markson and the tight hold he has on Draco, which may explain Draco pushing Harry further away even if it has been 2 years since they last saw each other."
        self.assertEqual(fanfic.summary, summary, 'Summary is correct')
        self.assertEqual(fanfic.rating, 'M', 'Rating is correct')
        self.assertEqual(fanfic.status, 'Completed', 'Status is correct')

        pairings = [
            ['Draco Malfoy', 'Harry Potter'],
            ['Hermione Granger', 'Ron Weasley'],
            ['Draco Malfoy', 'Original Male Character(s)'],
        ]
        self.assertEqual(len(fanfic.pairings), len(pairings), "Warning length is correct")
        for index, pairing in enumerate(pairings, start=0):
            self.assertEqual(len(pairing), len(fanfic.pairings[index]), "Pairing {} length is correct".format(index))
            for person in pairing:
                self.assertIn(person, fanfic.pairings[index], "'{}' is present in pairing {}".format(person, index))

        warnings = ['Graphic Depictions Of Violence', 'Rape/Non-Con']
        self.assertEqual(len(fanfic.warnings), len(warnings), "Warning length is correct")
        for warning in warnings:
            self.assertIn(warning, fanfic.warnings, "'{}' is present".format(warning))
        characters = ['Original Male Character(s)', 'Harry Potter', 'Draco Malfoy', 'Hermione Granger',
                      'Ron Weasley']
        self.assertEqual(len(fanfic.characters), len(characters), 'There are correct number of characters')
        for character in characters:
            self.assertIn(character, fanfic.characters, "'{}' is present".format(character))
        categories = ["M/M", "Abusive Relationships", "Angst with a Happy Ending", "Self Confidence Issues",
                      'Self-Esteem Issues', 'Depression', 'Suicide Attempt', 'Hurt/Comfort', "Mpreg", "Abortion",
                      'Emotional Manipulation', 'Mind Manipulation', 'Protective Harry Potter', 'Possessive Harry',
                      'Obsessive Harry', 'Broken Draco Malfoy']
        self.assertEqual(len(fanfic.categories), len(categories), "Category length is correct")
        for category in categories:
            self.assertIn(category, fanfic.categories, "'{}' is present".format(category))

        self.assertEqual(fanfic.updated.isoformat(), '2020-06-27T00:00:00', 'Published timestamp is correct')
        self.assertEqual(fanfic.published.isoformat(), '2020-06-22T00:00:00', 'Updated timestamp is correct')


if __name__ == '__main__':
    unittest.main()
