import unittest
from ff_scrape.sites.animationsource import AnimationSource
from ff_scrape.storybase import Story
from ff_scrape.errors import URLError
from testfixtures import ShouldRaise
from bs4 import BeautifulSoup
from os.path import dirname, join


class FanfictionTests(unittest.TestCase):

    def setUp(self):
        self.fanfiction = AnimationSource()
        url = "placeholder_url"
        self.fanfiction._url = url
        self.fanfiction._fanfic = Story(url)
        self.dir = dirname(__file__)

    def test_domain(self):
        self.fanfiction.set_domain()
        self.assertEqual(self.fanfiction._fanfic.domain, "Animation Source", "set_domain works as expected")

    def test_can_handle(self):
        url = "https://www.fanfiction.net/s/113445011"
        self.assertEqual(self.fanfiction.can_handle(url), False, "can_handle test case 1 is correct")

        url = "http://ficwad.com/"
        self.assertEqual(self.fanfiction.can_handle(url), False, "can_handle test case 2 is correct")

        url = "https://www.animationsource.org/"
        self.assertEqual(self.fanfiction.can_handle(url), True, "can_handle test case 3 is correct")

        url = "https://www.animationsource.org/balto/en/view_fanfic/An-Unexpected-Future-Aleu-Part-IV/53773.html"
        self.assertEqual(self.fanfiction.can_handle(url), True, "can_handle test case 4 is correct")

        url = "https://www.animationsource.org/balto/en/view_fanfic/Balto-s-Inside-Story-The-Family-Expands/263740.html"
        self.assertEqual(self.fanfiction.can_handle(url), True, "can_handle test case 5 is correct")

        url = "https://www.animationsource.org/balto/en/view_fanfic/Jenna-s-Journey/55497.html&deb=0&nsite=1"
        self.assertEqual(self.fanfiction.can_handle(url), True, "can_handle test case 6 is correct")

    def test_correct_url(self):
        good_checks = [
            ["https://www.animationsource.org/balto/en/view_fanfic/An-Unexpected-Future-Aleu-Part-IV/53773.html", "https://www.animationsource.org/balto/en/view_fanfic/An-Unexpected-Future-Aleu-Part-IV/53773.html"],
            ["https://www.animationsource.org/balto/en/view_fanfic/Balto-s-Inside-Story-The-Family-Expands/263740.html", "https://www.animationsource.org/balto/en/view_fanfic/Balto-s-Inside-Story-The-Family-Expands/263740.html"],
            ["https://www.animationsource.org/balto/en/view_fanfic/Jenna-s-Journey/55497.html&deb=0&nsite=1", "https://www.animationsource.org/balto/en/view_fanfic/Jenna-s-Journey/55497.html"],
        ]
        bad_checks = [
            ["https://www.animationsource.org/balto/en/view_fanfic/Jenna-s-Journey/", "Unknown URL format"],
            ["https://www.animationsource.org/balto/en/view_fanfic/Jenna-s-Journey", "Unknown URL format"],
            ["https://www.animationsource.org/balto/en/view_fanfic/Jenna-s-Journey/55497.html/t", "Unknown URL format"],
        ]

        for check in good_checks:
            fixed_url = self.fanfiction.correct_url(check[0])
            self.assertEqual(fixed_url, check[1], 'Correct URL for ' + check[0])

        for check in bad_checks:
            with ShouldRaise(URLError(check[1])):
                print("Checking " + check[0])
                self.fanfiction.correct_url(check[0])

    def test_check_exists(self):
        file = join(self.dir, 'data', 'missing_story.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        self.assertFalse(self.fanfiction.check_story_exists(), "Missing page shows as not existing")
        page.close()

        file = join(self.dir, 'data', 'good_story.html')
        page = open(file, 'r')
        self.fanfiction._soup = BeautifulSoup(page.read(), features="html.parser")
        self.assertTrue(self.fanfiction.check_story_exists(), "Good page shows as existing")
        page.close()


if __name__ == '__main__':
    unittest.main()
