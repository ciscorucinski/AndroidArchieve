from AndroidStudio import AndroidStudioPage, Releases
from storage import LastUpdatedStorage, ReleaseInfoStorage


def add_releases(releases):
    for version, release, name, download_url in releases:
        Releases.cascading_add(release, version, name, download_url)


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
        releases = Releases.all_releases(minimize=True)
        release_info_file.write(releases)

    print(f"Data Acquisition: {acquisition}")


if __name__ == '__main__':
    main()

    print()
    print("Data by version then release")
    for version in Releases.all_versions():
        print("-" * 150)
        for release in Releases:
            url = Releases.data(version, release)
            if url is not None:
                print(version, "|", release, Releases.data(version, release))
