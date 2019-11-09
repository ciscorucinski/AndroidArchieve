import re

import requests

# https://regex101.com/r/yPETBx/4
_parse_download_info = r"^.*(?:<p.+>Android Studio ([\d.]{3})(?: (\w+) (\d+))?|href=\"(.+linux(?:\.tar\.gz|\.zip))\")"
_find_download_url = r"((?<=iframe src=\").*(?=\.frame).frame)"


def set_path(path):
    return f"https://developer.android.com{path}"


class Webpage:
    html = None
    matches = None

    def request_page(self, url: str = None):
        request = requests.get(url)
        if not request.ok:
            raise RuntimeError(f"\nRequest Status Code: {request.status_code}\nURL: {url}")

        self.html = request.text
        return self


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
        version, release, number = zip(*[
            (
                version,
                release if release != "" else "stable",
                number if number != "" else "1"

            )
            for index, (version, release, number, _)
            in enumerate(self.matches)
            if index % 2 == 0
        ])
        url = [
            url
            for index, (*_, url)
            in enumerate(self.matches)
            if index % 2 == 1
        ]

        return zip(version, release, number, url)
