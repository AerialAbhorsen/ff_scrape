from .base import Formatter
from ff_scrape.sites.base import Story
import re
from html2bbcode.parser import HTML2BBCode


class BBCode(Formatter):

    @classmethod
    def format(cls, fanfic: Story) -> None:
        new_line_regex = re.compile("\n")
        for chapter in fanfic.chapters:
            story_text = chapter.processed_body
            # remove new lines due to pretty print
            story_text = new_line_regex.sub('', story_text)
            parser = HTML2BBCode()
            chapter.processed_body = parser.feed(story_text)


