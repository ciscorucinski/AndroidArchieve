import re


class Regex(object):
    find_download_url = r"((?<=iframe src=\").*(?=\.frame).frame)"

    # # https://regex101.com/r/MC8TOv/1/
    # parse_download_info = r"^.*(?:<p.*>(.*)|<span>(.*)<\/span>|<a href=\"(.*linux(?:.tar.gz|.zip))\">(?P<filename>.*)</a>.*\((.*) bytes\))"

    # https://www.debuggex.com/r/W8S6xxo611IXcmFT
    # https://regex101.com/r/yPETBx/2
    # parse_download_info = r"^.*(?:<p.+>(Android Studio ([0-9\.]+)(?: (\w+) (\d+))?)|<span>(.+)<\/span>|<section.+expandable (\w+)|<a href=\"(.+zips\/(.+)\.(.+)\/.+ide\-(.+)\..+linux(?:\.tar\.gz|\.zip)))"

    # parse_download_info = r"^.*(?:<p.+>(Android Studio ([0-9\.]+)(?: (\w+) (\d+))?)|<span>(.+)<\/span>|<section.+expandable(?: (\w*)|)\">|<a href=\"(.+zips\/(.+)\.(.+)\/.+ide\-(.+)\..+linux(?:\.tar\.gz|\.zip)))"

    parse_download_info = r"^.*(?:<p.+>(Android Studio ([0-9\.]+)(?: (\w+) (\d+))?)|<span>(.+)<\/span>|<section.+expandable(?: (\w*)|)\">|<a href=\"(.+zips\/(.+)\.(.+)\/.+ide\-(.+)\..+linux(?:\.tar\.gz|\.zip))\">)"
    @classmethod
    def find(cls, regex, text, flags=re.M):
        return cls.findall(regex, text, flags)[0]

    @classmethod
    def findall(cls, regex, text, flags=re.M):
        return re.findall(regex, text, flags)
