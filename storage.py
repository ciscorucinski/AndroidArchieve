from datetime import datetime


class Storage:
    def __init__(self, file):
        self.filename = file
        create = open(self.filename, "a")  # Ensure file is created and not erased
        create.close()


class ReleaseInfoStorage(Storage):
    releases = []

    def write(self, releases):
        with open(self.filename, "w") as file:
            for version, release_type, name, url in releases:
                file.write(f"{version}, {release_type}, {name}, {url}\n")
        return self

    def read(self):
        with open(self.filename, "r") as file:
            for line in file:
                self.releases.append(tuple(line[:-1].split(", ")))
        return self


class LastUpdatedStorage(Storage):
    urls = []
    _date_format = "%Y-%m-%d %H:%M:%S"

    def read(self):
        with open(self.filename, "r") as file:
            for line in file:
                date, url = line.split(", ")
                self.urls.append(url[:-1])
        return self

    def write(self, url):
        with open(self.filename, "a") as file:
            time = datetime.now().strftime(self._date_format)
            file.write(f"{time}, {url}\n")
        return self
