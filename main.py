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

    print()
    print("All Releases by Version")
    for version in Release.all_versions(Release.Canary):
        print(version, Release.releases(version))

    print()
    print("Data by version then release")
    for version in Release.all_versions(Release.Canary):
        print("-" * 120)
        for release in Release:
            print(version, "|", release, Release.data(version, release))


