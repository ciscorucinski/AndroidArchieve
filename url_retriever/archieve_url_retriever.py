from Webpage import AndroidStudioArchive
from file import UrlStorage


def entry():
    archive_url = AndroidStudioArchive().request_page().download_page_url
    file_storage = UrlStorage("archive_urls.txt").deserialize()

    if archive_url in file_storage.urls:
        print("URL already in file")
    else:
        file_storage.serialize(archive_url)
        print("URL appended to file")

    print(file_storage.last_updated, set(zip(file_storage.dates, file_storage.urls)))


if __name__ == '__main__':
    entry()
