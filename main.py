from AndroidStudio import AndroidStudioPage
from Release import Release
from util.file import UrlStorage


def organize_releases(studio_releases):
    for release in reversed(list(studio_releases)):
        version = release[4]
        release_type = release[5]
        download_link = release[7]

        Release.add(release_type, version, download_link)


def main():
    webpage = AndroidStudioPage().request_page()
    file_storage = UrlStorage("archive_urls.txt").read()

    download_url = webpage.get_download_info_url()

    if download_url in file_storage.urls:
        print("URL already exists:", download_url)
    else:
        file_storage.append(download_url)
        print("URL appended:", download_url)

        android_studio_download_info = webpage.parse_downloads()
        organize_releases(android_studio_download_info)


if __name__ == '__main__':
    main()

    print("latest", Release.latest_releases())
    print("latest (Stable)", Release.latest_releases(stable_only=True))
    print("4.0", Release.releases("4.0"))
    print("3.6", Release.releases("3.6"))
    print("3.5", Release.releases("3.5"))
    print("3.4", Release.releases("3.4"))
    print("3.3", Release.releases("3.3"))
    print("3.2", Release.releases("3.2"))
    print("3.1", Release.releases("3.1"))
    print("3.0", Release.releases("3.0"))
    print("2.4", Release.releases("2.4"))   # Note: Has "preview" key
    print("2.3", Release.releases("2.3"))
