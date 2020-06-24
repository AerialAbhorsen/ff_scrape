class URLError(Exception):
    def __init__(self, value):
        self.value = value


class ParameterError(Exception):
    def __init__(self, value):
        self.value = value


class StoryError(Exception):
    def __init__(self, value):
        self.value = value



# http://www.hpfanficarchive.com/stories/viewstory.php?sid=1963
# https://www.fanfiction.net/s/5621051/1/Outcast-s-Alley
# https://crys.fanficauthors.net/The_Morning_After/index/
#
# ficwad_url_good = "http://ficwad.com/story/234643"
# ficwad_url_good_age_good = "http://ficwad.com/story/94194"
# ficwad_url_good_age_fail = "http://ficwad.com/story/228839"
# ficwad_url_fail = "http://ficwad.com/story/941942222"
# fanficauthors_url_good = "http://whydoyouneedtoknow.fanficauthors.net/The_Most_Dangerous_Time_of_the_Year/The_Ousting_of_the_Opposition/"
#
# hpfanficarchive_url_good = "http://www.hpfanficarchive.com/stories/viewstory.php?sid=1345"
# hpfanficarchive_url_fail = "http://www.hpfanficarchive.com/stories/viewstory.php?sid=1345252"
#
# fanfiction_net_url_good = "https://www.fanfiction.net/s/7344530/20/Sealed-Legacy"
# fanfiction_net_url_good_co = "https://www.fanfiction.net/s/11344508/1/Hermione-aux-pays-des-vampires"
# fanfiction_net_url_fail = "https://www.fanfiction.net/s/113445011"