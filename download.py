import collections
import pprint
from collections import deque

from dateutil.parser import parse

from util.regex import Regex
from util.webpage import Webpage


class AndroidStudioArchive(Webpage):
    base = "https://developer.android.com"
    path = "studio/archive"
    download_page_url = None

    def request_page(self):
        super().request_page(self.set_path(self.path))

        download_path = Regex.find(Regex.find_download_url, self.html)
        self.download_page_url = self.set_path(download_path)

        return self

    def set_path(self, path):
        return f"{self.base}/{path}"

    def parse_downloads(self):
        def print_matches(regex_match):
            for index, match in enumerate(regex_match):
                if index % 4 == 0:
                    print("{:>3s}. {:<10s} ".format(str(int((index + 4) / 4)), match[5]), end="", sep=", ")
                elif index % 4 == 1:
                    print("{:<32s}{:<10s}{:<10s}{:<6s} ".format(match[0], match[1], match[2], match[3]), end="", sep=", ")
                elif index % 4 == 2:
                    print("{:<20s} ".format(match[4]), end="", sep=", ")
                elif index % 4 == 3:
                    print("{:<105s}{:<10s}{:<5s}{:<5}".format(match[6], match[7], match[8], match[9]), sep=", ")

        date_format = "%Y-%m-%d"

        webpage = Webpage.request_page(self, self.download_page_url)
        matches = Regex.findall(Regex.parse_download_info, str(webpage.soup))

        # print_matches(matches)

        name, version_name, risk_level, risk_level_increment = zip(*[
            (a,
             b if len(b) == 3 else b[0:3],
             c if c != "" else "Stable",
             d)
            for index, (a, b, c, d, *_)
            in enumerate(matches)
            if index % 4 == 1
        ])
        date = [
            parse(e).strftime(date_format)
            for index, (_, _, _, _, e, *_)
            in enumerate(matches)
            if index % 4 == 2
        ]
        index, stability = zip(*[
            (int((index + 4) / 4),
             f if f != "" else "preview")
            for index, (_, _, _, _, _, f, *_)
            in enumerate(matches)
            if index % 4 == 0
        ])
        url, version, version_increment, version_intellij = zip(*[
            (g,
             h,
             i,
             f"20{j[0:2]}.{j[:-1]}")
            for index, (*_, g, h, i, j)
            in enumerate(matches)
            if index % 4 == 3
        ])

        android_studio_release = zip(index, date, stability, name, version_name, risk_level, risk_level_increment, url, version, version_increment, version_intellij)

        releases = dict()
        for release in reversed(list(android_studio_release)):
            version = release[4]
            release_type = release[5]

            if releases.get(version) is None:
                releases[version] = dict()

            if releases.get(version).get(release_type) is None:
                releases.get(version).update({release_type: collections.deque([release[3]])})
            else:
                releases.get(version).get(release_type).append(release[3])

        pprint.pprint(releases)
