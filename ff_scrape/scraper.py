from pkg_resources import iter_entry_points
from os import environ
from configparser import ConfigParser
import logging
from ff_scrape.sites.base import Site
from ff_scrape.storybase import Story
from ff_scrape.errors import ParameterError
from ff_scrape.formatters.base import Formatter


cfg = {}
processors: dict[str, Site] = {}
formatters: dict[str, Formatter] = {}

if 'SCRAPER_CONFIG' in environ:
    config = ConfigParser()
    config.read(environ.get('SCRAPER_CONFIG'))

    for section in config.sections():
        cfg[section] = dict(config.items(section))

for site_processor in iter_entry_points('ff_scrape.sites'):
    site_params = []
    if site_processor.name in cfg:
        site_params = cfg[site_processor.name]
    processor_class = site_processor.load()
    processors[site_processor.name] = processor_class(site_params=site_params)

for site_formatters in iter_entry_points('ff_scrape.formatters'):
    formatters[site_formatters.name] = site_formatters.load()


def _setup_logger(loglevel=None):
    logger = logging.getLogger('FanficDownloader')
    formatter = logging.Formatter('%(asctime)-15s - %(name)s - %(levelname)s - %(message)s')

    if 'SCRAPE_LOG_LEVEL' in environ:
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
    logger = logging.getLogger('ff_scrape')

    if 'SCRAPE_LOG_FILE' in environ:
        handler = logging.FileHandler(environ.get("SCRAPER_LOG_FILE"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        ch = logging.StreamHandler()
        ch.setLevel(loglevel)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def ff_scrape(urls: [str], loglevel=None, formatter=None) -> [Story]:
    logger = _setup_logger(loglevel=loglevel)
    stories: [Story] = []
    if formatter is not None:
        if formatter not in site_formatters:
            raise ParameterError("Unknown formatter")

    for url in urls:
        for processor in processors:
            if processors[processor].can_handle(url):
                processors[processor].url = url
                processors[processor].get_story()
                fanfic = processors[processor].fanfic
                if formatter is not None:
                    formatters[formatter].format(fanfic)
                stories.append(fanfic)
                break  # abort processor loop if a match was found
        else:
            logger.error("Unknown URL format for: " + url)
    return stories
