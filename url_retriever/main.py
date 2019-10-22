from download import AndroidStudioArchive
from file import UrlStorage


def main():
    webpage = AndroidStudioArchive().request_page()
    file_storage = UrlStorage("archive_urls.txt").deserialize()

    download_url = webpage.download_page_url

    if download_url in file_storage.urls:
        print("URL already exists:", download_url)
    else:
        file_storage.serialize(download_url)
        print("URL appended:", download_url)

    # print(file_storage.last_updated, set(zip(file_storage.dates, file_storage.urls)))
    webpage.parse_downloads()


if __name__ == '__main__':
    main()
