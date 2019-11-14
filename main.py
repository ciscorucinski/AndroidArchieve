from AndroidStudio import AndroidStudioPage
from release import Release
from storage import LastUpdatedStorage, ReleaseInfoStorage


def add_releases(releases):
    for version, release, name, download_url in releases:
        Release.cascading_add(release, version, name, download_url)


def main():
    webpage = AndroidStudioPage().request_page()
    last_updated_file = LastUpdatedStorage("file/archives.csv")
    release_info_file = ReleaseInfoStorage("file/releases.csv")

    download_url = webpage.get_download_info_url()

    if download_url in last_updated_file.read().urls:
        acquisition = f"Local File = './{release_info_file.filename}'"
        releases = release_info_file.read().releases

        add_releases(releases)

    else:
        last_updated_file.write(download_url)
        acquisition = f"Web Page URL = '{download_url}'"

        android_studio_download_info = reversed(list(webpage.parse_downloads()))
        add_releases(android_studio_download_info)
        releases = Release.all_releases(minimize=True)
        release_info_file.write(releases)

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
