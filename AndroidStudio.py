import re
from dateutil.parser import parse

from util.webpage import Webpage

# https://regex101.com/r/yPETBx/3
_parse_download_info = r"^.*(?:<p.+>(Android Studio ([0-9\.]+)(?: (\w+) (\d+))?)|<span>(.+)<\/span>|<section.+expandable(?: (\w*)|)\">|href=\"(.+zips\/(.+)\.(.+)\/.+ide\-(.+)\..+linux(?:\.tar\.gz|\.zip))\")"
_find_download_url = r"((?<=iframe src=\").*(?=\.frame).frame)"


def set_path(path):
    return f"https://developer.android.com{path}"


class AndroidStudioPage(Webpage):
    path = "/studio/archive"
    download_page_url = None

    def request_page(self, **kwargs):
        super().request_page(set_path(self.path))
        self.matches = re.findall(_find_download_url, self.html, re.M)[0]
        self.download_page_url = set_path(self.matches)

        return self

    def get_download_info_url(self):
        if self.download_page_url is None:
            raise RuntimeError("Download URL was not acquired yet. If it was acquired, then no match was found.")
        return self.download_page_url

    def parse_downloads(self):
        # Grabs the next webpage, parses the data, and returns that to the caller
        webpage = DownloadInfo().request_page(self.download_page_url)
        return webpage.parse_download_info()


class DownloadInfo(Webpage):

    def request_page(self, url=None):
        if url is None:
            raise RuntimeError('URL was not defined. Acquire URL from the TOS page first.')

        super().request_page(url)
        self.matches = re.findall(_parse_download_info, self.html, re.M)
        return self

    def parse_download_info(self):
        date_format = "%Y-%m-%d"

        name, version_name, risk_level, risk_level_increment = zip(*[
            (a,
             b if len(b) == 3 else b[0:3],
             c if c != "" else "Stable",
             d)
            for index, (a, b, c, d, *_)
            in enumerate(self.matches)
            if index % 4 == 1
        ])
        date = [
            parse(e).strftime(date_format)
            for index, (_, _, _, _, e, *_)
            in enumerate(self.matches)
            if index % 4 == 2
        ]
        index, stability = zip(*[
            (int((index + 4) / 4),
             f if f != "" else "preview")
            for index, (_, _, _, _, _, f, *_)
            in enumerate(self.matches)
            if index % 4 == 0
        ])
        url, version, version_increment, version_intellij = zip(*[
            (g,
             h,
             i,
             f"20{j[0:2]}.{j[:-1]}")
            for index, (*_, g, h, i, j)
            in enumerate(self.matches)
            if index % 4 == 3
        ])

        android_studio_release = zip(index, date, stability, name, version_name, risk_level, risk_level_increment, url,
                                     version, version_increment, version_intellij)

        return android_studio_release
