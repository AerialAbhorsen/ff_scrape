"""Contains central imports for all of the sites package"""
import requests                        # used to get the web page to pass to beautifulsoup
from urllib.parse import urljoin       # used to properly format the web URL
import logging                         # used for logger setup
from bs4 import BeautifulSoup          # used to parse the web page
from ff_scrape.errors import *         # used for custom errors
from os import environ                 # used for environment variable lookups
from ff_scrape.storybase import Story


class Site(object):
    """Creates a logger using a variable formatter"""

    _soup: BeautifulSoup
    _fanfic_set: bool
    _url: str
    _fanfic: Story
    _got_meta: bool
    _chapter_sleep_time: int
    _params: dict
    _logging: logging.Logger

    def __init__(self, loglevel=None, **kwargs):
        defaults = {
            'logger_name': 'ff_scrape.site',
            'site_params': {}
        }
        defaults.update(kwargs)
        self._params = defaults['site_params']
        self._fanfic_set = False
        self._soup = None
        self._url = ''
        self._fanfic = None
        self._got_meta = False

        self._chapter_sleep_time = 3

        self._logger = logging.getLogger(defaults['logger_name'])
        self.setup_site_logger(loglevel=loglevel)

        self.log_debug("Initialized")

    def setup_site_logger(self, loglevel=None) -> None:
        # TODO: fix logger
        # only add handlers if there is none attached to the logger
        # that only happens on first initialization of the class
        if self._logger.hasHandlers():
            return

        formatter = logging.Formatter('%(asctime)-15s - %(name)s - %(url)s - %(levelname)s - %(message)s')

        if 'SCRAPER_LOG_LEVEL' in environ:
            if environ.get('SCRAPER_LOG_LEVEL').lower() == 'debug':
                loglevel = logging.DEBUG
            elif environ.get('SCRAPER_LOG_LEVEL').lower() == 'info':
                loglevel = logging.INFO
            elif environ.get('SCRAPER_LOG_LEVEL').lower() == 'warn':
                loglevel = logging.WARN
            elif environ.get('SCRAPER_LOG_LEVEL').lower() == 'warning':
                loglevel = logging.WARN
            elif environ.get('SCRAPER_LOG_LEVEL').lower() == 'error':
                loglevel = logging.ERROR
            elif environ.get('SCRAPER_LOG_LEVEL').lower() == 'crit':
                loglevel = logging.CRITICAL
            elif environ.get('SCRAPER_LOG_LEVEL').lower() == 'critical':
                loglevel = logging.CRITICAL
        if loglevel is None:
            loglevel = logging.INFO

        if 'SCRAPER_LOG_FILE' in environ:
            handler = logging.FileHandler(environ.get("SCRAPER_LOG_FILE"))
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

            ch = logging.StreamHandler()
            ch.setLevel(logging.ERROR)
            ch.setFormatter(formatter)
            self._logger.addHandler(ch)
        else:
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            ch.setFormatter(formatter)
            self._logger.addHandler(ch)

    def get_story(self) -> None:
        """Perform the necessary steps to download the fanfic"""

        self.log_debug("Starting story")

        if not self._got_meta:
            self.get_meta()

        self.log_debug("Done metadata")
        self.record_story_chapters()

        self.log_info("Done processing story")

    def _update_soup(self, url: str = None, lenient: bool = True, cookie_jar=None) -> None:
        if url is None:
            url = self._url
        page = requests.get(url)
        if lenient:
            self._soup = BeautifulSoup(page.text, features="html.parser", cookies=cookie_jar)
        else:
            # need to use html5lib due to ff.net having broken html in their site
            # most notably the chapter list
            self._soup = BeautifulSoup(page.text, features="html5lib", cookies=cookie_jar)

    def get_meta(self) -> None:
        # get page
        self._update_soup(lenient=False)

        # check to see that the story exists
        if not self.check_story_exists():
            raise StoryError("Story doesn't exist.")

        # create a story and start setting attributes
        self._fanfic = Story(self._url)
        self._fanfic_set = True
        self.set_domain()
        self.log_debug("Recording metadata")
        self.record_story_metadata()
        self._got_meta = True

    def check_story_exists(self) -> bool:
        return True

    def record_story_metadata(self) -> None:
        pass

    def record_story_chapters(self) -> None:
        pass

    def set_domain(self):
        self._fanfic.domain = "Unknown"

    def cleanup_custom_vars(self) -> None:
        pass

    @property
    def url(self) -> str:
        """Get or set the URL. Setting the URL will delete the current
           fanfic"""
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        """Allows for the URL to be changed to parse another fanfic"""
        if self._fanfic_set:
            del self._fanfic
            self._got_meta = False
            self.cleanup_custom_vars()
        self._url = ''
        value = self.correct_url(value)

        self.log_debug("Updating URL to: %s" % value)
        self._url = value

    @property
    def fanfic(self) -> Story:
        return self._fanfic

    def reset_fanfic(self) -> None:
        if self._fanfic_set:
            del self._fanfic
        self._fanfic = Story()

    def can_handle(self, url: str) -> bool:
        return False

    def correct_url(self, url: str) -> str:
        return url

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self):
        return '%s(url:%s)' % (self.__class__.__name__,
                               self._url or "''")

    def log_debug(self, message: str) -> None:
        self._logger.debug(message, extra={'url': self._url})

    def log_info(self, message: str) -> None:
        self._logger.info(message, extra={'url': self._url})

    def log_warn(self, message: str) -> None:
        self._logger.warning(message, extra={'url': self._url})

    def log_error(self, message: str) -> None:
        self._logger.error(message, extra={'url': self._url})

    def log_crit(self, message: str) -> None:
        self._logger.critical(message, extra={'url': self._url})
