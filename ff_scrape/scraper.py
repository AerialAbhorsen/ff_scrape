from pkg_resources import iter_entry_points
from os import environ
from configparser import ConfigParser
import argparse
import logging


cfg = {}
processors = {}
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

def run_scrape(urls, loglevel=None):
    logger = _setup_logger(loglevel=loglevel)
    for url in urls:
        for processor in processors:
            if processors[processor].can_handle(url):
                processors[processor].url = url
                processors[processor].get_story()
                break  # abort processor loop if a match was found
        else:
            logger.error("Unknown URL format for: " + url)


def main():
    parser = argparse.ArgumentParser(description='Scrape fanfiction websites to obtain the story text.')
    parser.add_argument('--url', type=str, help='URL to obtain the details for', required=True, action='append')

    args = parser.parse_args()
    run_scrape(args.url)


if __name__ == "__main__":
    main()

