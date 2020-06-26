import unittest
from ff_scrape.sites.fanfiction import Fanfiction
from ff_scrape.storybase import Story
from ff_scrape.errors import URLError
from testfixtures import ShouldRaise
from bs4 import BeautifulSoup
from os.path import dirname, join


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = Fanfiction()
        url = "placeholder_url"
        self.fanfiction._url = url
        self.fanfiction._fanfic = Story(url)
        self.dir = dirname(__file__)

    def test_domain(self):
        self.fanfiction.set_domain()
        self.assertEqual(self.fanfiction._fanfic.domain, "Fanfiction.net", "set_domain works as expected")

    def test_can_handle(self):
        url = "https://www.fanfiction.net/s/113445011"
        self.assertEqual(self.fanfiction.can_handle(url), True, "can_handle test case 1 is correct")

        url = "https://www.fanfiction.net/s/11344508/1/Hermione-aux-pays-des-vampires"
        self.assertEqual(self.fanfiction.can_handle(url), True, "can_handle test case 2 is correct")

        url = "https://www.fanfiction.net/s/7344530/20/Sealed-Legacy"
        self.assertEqual(self.fanfiction.can_handle(url), True, "can_handle test case 3 is correct")

        url = "http://ficwad.com/"
        self.assertEqual(self.fanfiction.can_handle(url), False, "can_handle test case 4 is correct")

        url = "http://www.hpfanficarchive.com/"
        self.assertEqual(self.fanfiction.can_handle(url), False, "can_handle test case 5 is correct")

    def test_correct_url(self):
        good_checks = [
            ["https://www.fanfiction.net/s/113445011", "https://www.fanfiction.net/s/113445011/1"],
            ["https://www.fanfiction.net/s/11344508/1/Hermione-aux-pays-des-vampires", "https://www.fanfiction.net/s/11344508/1"],
            ["https://www.fanfiction.net/s/7344530/20/Sealed-Legacy", "https://www.fanfiction.net/s/7344530/1"],
        ]
        bad_checks = [
            ["https://www.fanfiction.net/s/", "No Story ID given"],
            ["https://www.fanfiction.net/s/1234/1/1/1", "Unknown URL format"],
            ["https://www.fanfiction.net/s//1/1/1", "No Story ID given"],
            ["https://www.fanfiction.net/", "Unknown URL format"],
        ]

        for check in good_checks:
            fixed_url = self.fanfiction.correct_url(check[0])
            self.assertEqual(fixed_url, check[1], 'Correct URL for ' + check[0])

        for check in bad_checks:
            with ShouldRaise(URLError(check[1])):
                self.fanfiction.correct_url(check[0])

    def test_check_exists(self):
        file = join(self.dir, 'data', 'missing_story.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        self.assertFalse(self.fanfiction.check_story_exists(), "Missing page shows as not existing")
        page.close()

        file = join(self.dir, 'data', 'good_story.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html5lib")
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        self.assertTrue(self.fanfiction.check_story_exists(), "Good page shows as existing")
        page.close()


if __name__ == '__main__':
    unittest.main()
