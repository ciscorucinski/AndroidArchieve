import requests
from bs4 import BeautifulSoup


class Webpage:
    html = None
    soup = None

    matches = None

    def request_page(self, url: str = None):
        request = requests.get(url)
        request.url

        self.html = request.text
        self.soup = BeautifulSoup(request.content, "html.parser")

        return self

    def match(self, regex: str = None):
        pass
