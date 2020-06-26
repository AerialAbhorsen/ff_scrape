import unittest
from ff_scrape.sites.hpfanficarchive import HPFanficArchive
from ff_scrape.storybase import Story
from bs4 import BeautifulSoup
from os.path import dirname, join


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = HPFanficArchive()
        url = "placeholder_url"
        self.fanfiction._url = url
        self.fanfiction._fanfic = Story(url)
        self.dir = dirname(__file__)

    def test_metadata_story1(self):
        self.fanfiction._url = 'http://www.hpfanficarchive.com/stories/viewstory.php?sid=270'
        file = join(self.dir, 'data', 'good_story.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
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

        chapter_list = [
            {'link': 'viewstory.php?sid=270&chapter=1', 'name': 'Chapter 1: A Strange Beginning Or Finding The Book'},
            {'link': 'viewstory.php?sid=270&chapter=2', 'name': 'Chapter 2: Shopping again in Knockturn Alley'},
            {'link': 'viewstory.php?sid=270&chapter=3', 'name': 'Chapter 3: Train rides and old friends'},
            {'link': 'viewstory.php?sid=270&chapter=4', 'name': 'Chapter 4: Welcome to Hogwarts'},
            {'link': 'viewstory.php?sid=270&chapter=5', 'name': 'Chapter 5: First Week Away and We Miss You!'},
            {'link': 'viewstory.php?sid=270&chapter=6', 'name': 'Chapter 5 Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=7', 'name': 'Chapter 6: Hallowed Night, Harrowing Fright'},
            {'link': 'viewstory.php?sid=270&chapter=8', 'name': 'Hallowed Night, Harrowing Fright Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=9', 'name': 'Chapter 7: Wakeups, Warnings and Welcomes'},
            {'link': 'viewstory.php?sid=270&chapter=10', 'name': 'Wakeups, Warnings and Welcomes Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=11', 'name': 'Chapter 8:  Hogsmeade Weekend and Hogwarts Reactions'},
            {'link': 'viewstory.php?sid=270&chapter=12', 'name': 'Hogsmeade Weekend and Hogwarts Reactions Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=13', 'name': 'Hogsmeade Weekend and Hogwarts Reactions Part 3'},
            {'link': 'viewstory.php?sid=270&chapter=14', 'name': 'Chapter 9: Downward Spiral and Deviant Dreams'},
            {'link': 'viewstory.php?sid=270&chapter=15', 'name': 'Downward Spiral and Deviant Dreams Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=16', 'name': 'Chapter 10: Darkness Rising, Calls in the Dark and a Rising Witch'},
            {'link': 'viewstory.php?sid=270&chapter=17', 'name': 'Darkness Rising, Calls in the Dark and a Rising Witch Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=18', 'name': 'Darkness Rising, Calls in the Dark and a Rising Witch Part 3'},
            {'link': 'viewstory.php?sid=270&chapter=19', 'name': 'Chapter 11: The Dora proposition, dealing out promises and Dragon Problems'},
            {'link': 'viewstory.php?sid=270&chapter=20', 'name': 'Chapter 12: Explorations and Epiphanies between Holidays'},
            {'link': 'viewstory.php?sid=270&chapter=21', 'name': 'Explorations and Epiphanies between Holidays Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=22', 'name': 'Chapter 13: Winding down to Winter Solstice'},
            {'link': 'viewstory.php?sid=270&chapter=23', 'name': 'Winding down to Winter Solstice Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=24', 'name': 'Chapter 14:  Christmas Part 1: Holiday Departures'},
            {'link': 'viewstory.php?sid=270&chapter=25', 'name': 'Christmas Part 1: Holiday Departures Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=26', 'name': 'Chapter 15: Christmas Part 2: Yule Business'},
            {'link': 'viewstory.php?sid=270&chapter=27', 'name': 'Christmas Part 2: Yule Business Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=28', 'name': 'Chapter 16: Christmas Part 3: Hedonistic Holiday'},
            {'link': 'viewstory.php?sid=270&chapter=29', 'name': 'Christmas Part 3: Hedonistic Holiday Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=30', 'name': 'Chapter 17: Christmas Part 4: Business Discussions and Personal Matters'},
            {'link': 'viewstory.php?sid=270&chapter=31', 'name': 'Christmas Part 4: Business Discussions and Personal Matters Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=32', 'name': 'Christmas Part 4: Business Discussions and Personal Matters Part 3'},
            {'link': 'viewstory.php?sid=270&chapter=33', 'name': 'Chapter 18: Christmas Part 5: Visits to the Vicious and Victims of Vigilance'},
            {'link': 'viewstory.php?sid=270&chapter=34', 'name': 'Christmas Part 5: Visits to the Vicious and Victims of Vigilance Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=35', 'name': 'Christmas Part 5: Visits to the Vicious and Victims of Vigilance Part 3'},
            {'link': 'viewstory.php?sid=270&chapter=36', 'name': 'Chapter 19: Returns and Explorations'},
            {'link': 'viewstory.php?sid=270&chapter=37', 'name': 'Returns and Explorations Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=38', 'name': 'Chapter 20: Reactions and Reflections - Susan'},
            {'link': 'viewstory.php?sid=270&chapter=39', 'name': 'Reactions and Reflections - Penny'},
            {'link': 'viewstory.php?sid=270&chapter=40', 'name': 'Reactions and Reflections - Sarah'},
            {'link': 'viewstory.php?sid=270&chapter=41', 'name': 'Reactions and Reflections - Quirrell'},
            {'link': 'viewstory.php?sid=270&chapter=42', 'name': 'Chapter 21: Sudden Servant and Secret Solicitations'},
            {'link': 'viewstory.php?sid=270&chapter=43', 'name': 'Sudden Servant and Secret Solicitations Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=44', 'name': 'Sudden Servant and Secret Solicitations Part 3'},
            {'link': 'viewstory.php?sid=270&chapter=45', 'name': 'Chapter 22: Springing Further Forward'},
            {'link': 'viewstory.php?sid=270&chapter=46', 'name': 'Springing Further Forward Part 2'},
            {'link': 'viewstory.php?sid=270&chapter=47', 'name': 'Springing Further Forward Part 3'},
            {'link': 'viewstory.php?sid=270&chapter=48', 'name': 'Chapter 23: Preparations for Meetings can be fun'},
            {'link': 'viewstory.php?sid=270&chapter=49', 'name': 'Chapter 24: Penny Wise, Penny Foolish, Penny Lain'},
            {'link': 'viewstory.php?sid=270&chapter=50', 'name': 'Chapter 25: Preparing with a Purpose'},
            {'link': 'viewstory.php?sid=270&chapter=51', 'name': 'Chapter 26: A Purpose in Reaction'},
            {'link': 'viewstory.php?sid=270&chapter=52', 'name': "Chapter 27: Settling Things at Gringott's"},
            {'link': 'viewstory.php?sid=270&chapter=53', 'name': 'Chapter 28: Decision and Romance As They Rush to Summer'},
            {'link': 'viewstory.php?sid=270&chapter=54', 'name': 'Chapter 29: Year End Finals and Feasts'},
            {'link': 'viewstory.php?sid=270&chapter=55', 'name': 'Chapter 30: Train Rides and Pleasurable Discussions'},
            {'link': 'viewstory.php?sid=270&chapter=56', 'name': 'Chapter 31: Pleasurable Rides and Train Discussions'},
            {'link': 'viewstory.php?sid=270&chapter=57', 'name': 'Chapter 32: Platform 9 ï¿½'},
            {'link': 'viewstory.php?sid=270&chapter=58', 'name': 'Chapter 33: In Kingï¿½s Cross'},
            {'link': 'viewstory.php?sid=270&chapter=59', 'name': 'Chapter 34: Dinner Discussions'},
            {'link': 'viewstory.php?sid=270&chapter=60', 'name': 'Chapter 35: Black Business in Surrey'},
            {'link': 'viewstory.php?sid=270&chapter=61', 'name': 'Chapter 36: This Is Your Life'},
            {'link': 'viewstory.php?sid=270&chapter=62', 'name': 'Chapter 37: Black Business'},
            {'link': 'viewstory.php?sid=270&chapter=63', 'name': 'Chapter 38: Repercussions'},
            {'link': 'viewstory.php?sid=270&chapter=64', 'name': 'Chapter 39: Arrivals in Preparation'},
            {'link': 'viewstory.php?sid=270&chapter=65', 'name': 'Chapter 40: Spa Trips and Day Trips'},
            {'link': 'viewstory.php?sid=270&chapter=66', 'name': 'Chapter 41: Catching Up Before the Holiday'},
            {'link': 'viewstory.php?sid=270&chapter=67', 'name': 'Chapter 42: Bon Voyage'},
            {'link': 'viewstory.php?sid=270&chapter=68', 'name': 'Chapter 43: Girls on the Beach, Hot Water and Rocking Waves'},
            {'link': 'viewstory.php?sid=270&chapter=69', 'name': 'Chapter 44: Juneï¿½s Discoveries and Realizations in the Warm Sea Air'},
            {'link': 'viewstory.php?sid=270&chapter=70', 'name': 'Chapter 45: Fleur the Sexy French Tour Guide'},
            {'link': 'viewstory.php?sid=270&chapter=71', 'name': 'Chapter 46: Picking Up Games'},
            {'link': 'viewstory.php?sid=270&chapter=72', 'name': 'Chapter 47: At Chateau Delacour'},
            {'link': 'viewstory.php?sid=270&chapter=73', 'name': 'Chapter 48: Summer Days in Marseilles'},
            {'link': 'viewstory.php?sid=270&chapter=74', 'name': 'Chapter 49: Playful Planning'},
            {'link': 'viewstory.php?sid=270&chapter=75', 'name': 'Chapter 50: The Planned Play'},
            {'link': 'viewstory.php?sid=270&chapter=76', 'name': 'Chapter 51: Departures'},
            {'link': 'viewstory.php?sid=270&chapter=77', 'name': 'Chapter 52: Arrival at the Flamels'},
            {'link': 'viewstory.php?sid=270&chapter=78', 'name': 'Chapter 53: Training at the Flamels'},
            {'link': 'viewstory.php?sid=270&chapter=79', 'name': 'Chapter 54: Realizations of Submissive Witches'},
            {'link': 'viewstory.php?sid=270&chapter=80', 'name': 'Chapter 55: Towards the East, the Orient Encounter'},
            {'link': 'viewstory.php?sid=270&chapter=81', 'name': 'Chapter 56: The House of Li'},
            {'link': 'viewstory.php?sid=270&chapter=82', 'name': 'Chapter 57: Revolutionary Studies'},
            {'link': 'viewstory.php?sid=270&chapter=83', 'name': 'Chapter 58: Carnage in the Name of Progress'},
            {'link': 'viewstory.php?sid=270&chapter=84', 'name': 'Chapter 59: Aftermath of Progress'},
            {'link': 'viewstory.php?sid=270&chapter=85', 'name': 'Chapter 60: Return to Surrey'},
            {'link': 'viewstory.php?sid=270&chapter=86', 'name': 'Chapter 61: Surrey Problems and Other Complications'}
        ]
        self.assertEqual(chapter_list, self.fanfiction.chapter_list, 'Chapter list is correct')

    def test_metadata_story2(self):
        self.fanfiction._url = 'http://www.hpfanficarchive.com/stories/viewstory.php?sid=471'
        file = join(self.dir, 'data', 'good_story2.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        page.close()
        self.fanfiction.record_story_metadata()
        fanfic = self.fanfiction._fanfic

        self.assertEqual(fanfic.universe, ['Harry Potter'], "Universe is correctly set")
        self.assertEqual(len(fanfic.raw_index_page), 19102, 'Raw index page length correct')
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

        chapter_list = [
            {'link': 'viewstory.php?sid=471&chapter=1', 'name': 'Prologue: Rescue from the Infection'},
            {'link': 'viewstory.php?sid=471&chapter=2', 'name': 'Abysmal Beginnings to the Year'},
            {'link': 'viewstory.php?sid=471&chapter=3', 'name': 'Of Poisoning and Hogwarts'}
        ]
        self.assertEqual(chapter_list, self.fanfiction.chapter_list, 'Chapter list is correct')


if __name__ == '__main__':
    unittest.main()
