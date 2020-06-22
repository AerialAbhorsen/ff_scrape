class URLError(Exception):
    def __init__(self, value):
        self.value = value


class ParameterError(Exception):
    def __init__(self, value):
        self.value = value


class StoryError(Exception):
    def __init__(self, value):
        self.value = value
