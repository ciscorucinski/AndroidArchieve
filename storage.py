from collections import OrderedDict
from datetime import datetime


class ReleaseInfoStorage:
    versions = []
    releases = []
    download_links = []

    def __init__(self, file):
        self.filename = file

    def write(self, releases, latest):
        lines = OrderedDict()
        with open(self.filename, "w") as file:
            for version, release_type, name, url in releases:
                lines.update({f"{version}, {release_type}, {name}, {url}\n": None})
            for version, release_type, name, url in latest:
                print("\t", version, release_type, name, url)
                lines.update({f"{version}, {release_type}, {name}, {url}\n": None})
            for line in lines:
                file.write(line)
        return self

    def read(self):
        releases = []
        with open(self.filename, "r") as file:
            for line in file:
                releases.append(tuple(line[:-1].split(", ")))
        return releases


class LastUpdatedStorage:
    dates = []
    urls = []
    last_updated = None

    date_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, file):
        self.filename = file

    def read(self):
        with open(self.filename, "r") as file:
            for line in file:
                date, url = line.split(", ")
                self.last_updated = datetime.strptime(f"{date}", self.date_format)
                self.dates.append(self.last_updated)
                self.urls.append(url[:-1])
        return self

    def append(self, url):
        with open(self.filename, "a") as file:
            time = datetime.now()
            file.writelines([
                time.strftime(self.date_format),
                ", ",
                url,
                "\n"
            ])
            self.last_updated = time
        return self
