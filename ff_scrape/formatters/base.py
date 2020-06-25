from abc import ABC
from ff_scrape.storybase import Story

class Formatter(ABC):

    @classmethod
    def format(cls, fanfic: Story) -> None:
        pass
