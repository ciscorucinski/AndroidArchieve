import re


class Regex(object):
    find_download_url = "((?<=iframe src=\").*(?=\\.frame).frame)"

    @classmethod
    def find(cls, regex, text):
        return cls.findall(regex, text)[0]

    @classmethod
    def findall(cls, regex, text):
        return re.findall(regex, text)
