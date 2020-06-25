from ff_scrape.scraper import ff_scrape
import argparse

def scrape():
    parser = argparse.ArgumentParser(description='Scrape fanfiction websites to obtain the story text.')
    parser.add_argument('--url', type=str, help='URL to obtain the details for', required=True, action='append')
    parser.add_argument('--formatter', type=str, help='Formatter for after scrape processing')

    args = parser.parse_args()
    ff_scrape(args.url, formatter=args.formatter)

