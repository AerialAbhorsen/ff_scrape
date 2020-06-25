from .base import Formatter
from ff_scrape.sites.base import Story
import re

class Text(Formatter):

    @classmethod
    def format(cls, fanfic: Story) -> None:
        html_tag_regex = re.compile("<.*?>")
        gt_regex = re.compile('&gt;')
        lt_regex = re.compile('&lt;')
        nbsp_regex = re.compile('\xa0')
        for chapter in fanfic.chapters:
            story_text = chapter.processed_body
            # remove html tags
            story_text = html_tag_regex.sub('', story_text)
            # convert < and > to the symbols
            story_text = gt_regex.sub('>', story_text)
            story_text = lt_regex.sub('<', story_text)
            # fix the whitespace
            story_text = nbsp_regex.sub(' ', story_text)
            chapter.processed_body = story_text
