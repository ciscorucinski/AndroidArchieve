import re
from enum import Enum

import requests

# https://regex101.com/r/yPETBx/5
_parse_download_info = r"^.*(?:<p.+>Android Studio ([\d.]+)(?: (\w+ \d+))?|href=\"(.+linux(?:\.tar\.gz|\.zip))\")"
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
        version, release, name = zip(*[
            (
                version_code if len(version_code) == 3 else version_code[:3],
                release_name.split(" ")[0] if release_name != "" else "stable",
                f"{version_code} {release_name}" if release_name != "" else version_code
            )
            for index, (version_code, release_name, _)
            in enumerate(self.matches)
            if index % 2 == 0
        ])
        url = [
            url
            for index, (*_, url)
            in enumerate(self.matches)
            if index % 2 == 1
        ]

        return zip(version, release, name, url)


class Releases(Enum):
    PREVIEW = 0
    CANARY = 1
    BETA = 2
    RC = 3
    STABLE = 4

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.current = dict()
        return obj

    @classmethod
    def all_versions(cls, release: "Releases" = None, *, include_preview: bool = True, include_latest: bool = True):
        if type(release) is not Releases:
            release = Releases.CANARY
        keys = set(release.current.keys())
        keys.discard("latest") if not include_latest else None
        keys.add("2.4") if include_preview else None
        return sorted(keys)

    @classmethod
    def data(cls, version, release: "Releases"):
        return release.current.get(version, None)

    @classmethod
    def releases(cls, version):
        release = dict()
        release.update({"stable": cls.STABLE.current.get(version),
                        "rc": cls.RC.current.get(version),
                        "beta": cls.BETA.current.get(version),
                        "canary": cls.CANARY.current.get(version)})
        if version == "2.4":
            release.update({"preview": cls.PREVIEW.current.get(version)})
        return release

    @staticmethod
    def cascading_add(release, version, name, url):
        if type(release) is str:
            release = Releases[release.upper()]
        release.current[version] = (name, url)
        release.current["latest"] = (version, name, url)
        if release.value > Releases.CANARY.value:
            Releases.cascading_add(Releases(release.value - 1), version, name, url)
        return

    @staticmethod
    def all_releases(*, minimize: bool):
        releases = []
        for version in Releases.all_versions(include_latest=False):
            for release in reversed(Releases):
                data = Releases.data(version, release)
                if data is not None:
                    releases.append(tuple([version, release.name, data[0], data[1]]))
                    if minimize:
                        break
        return releases
