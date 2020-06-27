from setuptools import find_packages, setup


setup(
    name='ff_scrape',
    version='0.1',

    packages=['ff_scrape', 'ff_scrape.sites'],
    install_requires=[
        'beautifulsoup4',
        'requests',
        'html5lib',
        'python-dateutil',
        'html2bbcode'
    ],
    entry_points={
        'console_scripts': [
            'ff_scrape=ff_scrape.cli:main'
        ],
        'ff_scrape.sites': [
            'Fanfiction=ff_scrape.sites.fanfiction:Fanfiction',
            'HPFanficArchive=ff_scrape.sites.hpfanficarchive:HPFanficArchive',
            'FanficAuthors=ff_scrape.sites.fanficauthors:FanficAuthors',
            'Ficwad=ff_scrape.sites.ficwad:Ficwad'
        ],
        'ff_scrape.formatters': [
            'text=ff_scrape.formatters.text:Text',
            'bbcode=ff_scrape.formatters.bbcode:BBCode'
        ],
        # 'ff_scrape.recorders': [
        #
        # ]
    }
)
