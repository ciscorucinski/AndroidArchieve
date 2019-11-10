from AndroidStudio import AndroidStudioPage
from Release import Release
from storage import LastUpdatedStorage, ReleaseInfoStorage


def organize_releases(studio_releases):
    for release in reversed(list(studio_releases)):
        version, release_type, number, download_link = release
        Release.cascading_add(release_type, version, number, download_link)


def release_info():
    releases = []
    latest = []
    for version in Release.all_versions(include_latest=True):
        for release in reversed(Release):
            data = Release.data(version, release)
            if data is not None:
                if version == "latest":
                    latest.append(tuple([data[0], release.name, data[1], data[2]]))
                else:
                    releases.append(tuple([version, release.name, data[0], data[1]]))
                    break
            else:
                continue

    return releases, latest


def main():
    webpage = AndroidStudioPage().request_page()
    last_updated_file = LastUpdatedStorage("file/archives.csv")
    release_info_file = ReleaseInfoStorage("file/releases.csv")

    download_url = webpage.get_download_info_url()

    if download_url in last_updated_file.read().urls:
        acquisition = f"Local File = './{release_info_file.filename}'"
        releases = release_info_file.read()

        for version, release, name, download_url in releases:
            Release.cascading_add(release, version, name, download_url)

    else:
        last_updated_file.append(download_url)
        acquisition = f"Web Page URL = '{download_url}'"

        android_studio_download_info = webpage.parse_downloads()
        organize_releases(android_studio_download_info)
        releases, latest = release_info()
        release_info_file.write(releases, latest)

    print(f"Data Acquisition: {acquisition}")


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
