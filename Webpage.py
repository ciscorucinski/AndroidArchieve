import requests
from bs4 import BeautifulSoup
from Regex import Regex


class Webpage:
    html = None
    soup = None

    def request_page(self, url):
        request = requests.get(url)

        self.html = request.text
        self.soup = BeautifulSoup(request.content, "html.parser")

        return self


class AndroidStudioArchive(Webpage):
    base = "https://developer.android.com"
    path = "studio/archive"
    download_page_url = None

    def request_page(self, **kwargs):
        super().request_page(f"{self.base}/{self.path}")

        download_path = Regex.find(Regex.find_download_url, self.html)
        self.download_page_url = self.set_path(download_path)

        return self

    def set_path(self, path):
        return f"{self.base}/{path}"

    # url = "https://developer.android.com/studio/archive_bd7715867e9a28e3960254ccd62bcfe4.frame?hl=en"
    # url = "https://developer.android.com/studio/archive_2d8f68c205b31dd880b44bae3f727ffa.frame?hl=en"
