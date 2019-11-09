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
            for release in releases:
                lines.update({f"{release[0]} {release[1]} {release[2]}\n": None})
            for release in latest:
                lines.update({f"{release[0]} {release[1]} {release[2]}\n": None})
            for line in lines:
                file.write(line)
        return self

    def read(self):
        releases = []
        with open(self.filename, "r") as file:
            for line in file:
                releases.append(tuple(line[:-1].split(" ")))
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
                date, time, url = line.split(" ")
                self.last_updated = datetime.strptime(f"{date} {time}", self.date_format)
                self.dates.append(self.last_updated)
                self.urls.append(url[:-1])
        return self

    def append(self, url):
        with open(self.filename, "a") as file:
            time = datetime.now()
            file.writelines([
                time.strftime(self.date_format),
                " ",
                url,
                "\n"
            ])
            self.last_updated = time
        return self
