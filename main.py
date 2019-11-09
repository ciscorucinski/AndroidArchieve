from AndroidStudio import AndroidStudioPage
from Release import Release
from storage import LastUpdatedStorage, ReleaseInfoStorage


def organize_releases(studio_releases):
    for release in reversed(list(studio_releases)):
        version, release_type, number, download_link = release
        Release.add(release_type, version, download_link)


def release_info():
    releases = []
    latest = []
    for version in Release.all_versions(include_latest=True):
        for release in reversed(Release):
            data = Release.data(version, release)
            if data is not None:
                if version == "latest":
                    latest.append(tuple([data[0], release.name, data[1]]))
                else:
                    releases.append(tuple([version, release.name, data]))
                    break
            else:
                continue

    return releases, latest


def main():
    webpage = AndroidStudioPage().request_page()
    last_updated_file = LastUpdatedStorage("file/archives.txt")
    release_info_file = ReleaseInfoStorage("file/releases.txt")

    download_url = webpage.get_download_info_url()

    # if download_url in last_updated_file.read().urls:
    #     print("URL already exists:", download_url)
    #     releases = release_info_file.read()
    #
    #     for version, release, download_url in releases:
    #         Release.add(release, version, download_url)
    #
    # else:
    #     last_updated_file.append(download_url)
    #     print("URL appended:", download_url)

    android_studio_download_info = webpage.parse_downloads()
    organize_releases(android_studio_download_info)
    releases, latest = release_info()
    release_info_file.write(releases, latest)


if __name__ == '__main__':
    main()

    print()
    print("All Releases by Version")
    for version in Release.all_versions():
        print(version, Release.releases(version))

    print()
    print("Data by version then release")
    for version in Release.all_versions():
        print("-" * 120)
        for release in Release:
            url = Release.data(version, release)
            if url is not None:
                print(version, "|", release, Release.data(version, release))
