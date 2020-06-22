from setuptools import find_packages, setup


setup(
    name='ff_scrape',
    version='0.1',

    packages=['ff_scrape', 'ff_scrape.sites'],
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'ff_scrape=ff_scrape.scraper:main'
        ],
        'ff_scrape.sites': [
            'Fanfiction=ff_scrape.sites.fanfiction:Fanfiction',
            'HPFanficArchive=ff_scrape.sites.hpfanficarchive:HPFanficArchive'
        ],
        # 'ff_scrape.formatters': [
        #     'text=ff_scrape.formatters.text:Text'
        # ],
        # 'ff_scrape.recorders': [
        #
        # ]
    }
)
