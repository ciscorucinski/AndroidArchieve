from datetime import datetime


class UrlStorage:
    dates = []
    urls = []
    last_updated = None

    date_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, name):
        self.name = name

    def deserialize(self):
        with open(self.name, "w+") as file:
            for line in file:
                date, time, url = line.split(" ")
                self.last_updated = datetime.strptime(f"{date} {time}", self.date_format)
                self.dates.append(self.last_updated)
                self.urls.append(url[:-1])
        return self

    def serialize(self, url):
        with open(self.name, "w+") as file:
            time = datetime.now()
            file.writelines([
                time.strftime(self.date_format),
                " ",
                url,
                "\n"
            ])
            self.last_updated = time
        return self
