import minidb
import requests
from bs4 import BeautifulSoup

url = "https://developer.android.com/studio/archive"
# url = "https://developer.android.com/studio/archive_bd7715867e9a28e3960254ccd62bcfe4.frame?hl=en"
# url = "https://developer.android.com/studio/archive_2d8f68c205b31dd880b44bae3f727ffa.frame?hl=en"

database_file = "android-studio-downloads.db"


def extract_download_info(div, start, end, start_sha256, filetype):
    installers_soup = BeautifulSoup(str(div)[start:end], "html.parser")
    sha256_text = str(div)[start_sha256 + 18:end].strip().replace("\n</div>", "")

    sha256_filenames = [sha256_filename.split(" ") for sha256_filename in sha256_text.split("\n")]

    installers = []

    for a in installers_soup.select("a"):
        location = a.attrs['href']
        file_text = a.text

        download_sha256 = [sha256 for sha256, filename in sha256_filenames if filename == file_text][0]

        installers.append((file_text, location, download_sha256, filetype))

    return installers


def extract_installer_info(div):
    start_extract_text = "Installers"
    end_extract_text = "Zip"
    start_sha256_extract_text = "SHA-256 Checksums"

    start = str(div).find(start_extract_text)
    end = str(div).find(end_extract_text)
    start_sha256 = str(div).find(start_sha256_extract_text)

    installers = extract_download_info(div, start, end, start_sha256, "Installer")

    return installers


def extract_zipfile_info(div):
    start_extract_text = "Zip"
    start_sha256_extract_text = "SHA-256 Checksums"

    start = str(div).find(start_extract_text)
    start_sha256 = str(div).find(start_sha256_extract_text, start)

    zipfiles = extract_download_info(div, start, len(str(div)), start_sha256, "Zip Files")

    return zipfiles


class AndroidStudioRelease(minidb.Model):
    date = str
    name = str
    category = str
    release_type = str
    filename = str
    location = str
    sha256 = str
    filetype = str
    platform = str


def extract_android_studio_info(html_sections):
    def get_channel_name(file_name):
        if "Canary" in file_name:
            return "Canary"
        elif "Preview" in file_name:
            return "Canary"
        elif "Beta" in file_name:
            return "Beta"
        elif "RC" in file_name:
            return "RC"
        else:
            return "Stable"

    def get_platform(file_text):
        if "windows32" in file_text:
            return "Windows (32-bit)"
        elif "windows" in file_text:
            return "Windows (64-bit)"
        elif "mac" in file_text:
            return "Mac"
        elif "linux" in file_text:
            return "Linux"
        else:
            return "Unknown"

    def get_release_type(stable):
        return "Stable" if stable else "Preview"

    def is_unique_record(database, where_clause):
        query = AndroidStudioRelease.query(database,
                                           select=AndroidStudioRelease.c.id.count,
                                           where=where_clause)

        return list(query)[0][0] == 0

    db = minidb.Store(database_file)
    db.register(AndroidStudioRelease)

    for section in html_sections:
        date = section.p.span.text.strip()
        name = section.p.text.replace(date, "").strip()

        is_stable = "stable" in section.attrs["class"]

        installers = []

        if is_stable:
            installers = extract_installer_info(section.div)

        zip_files = extract_zipfile_info(section.div)

        for filename, download_location, sha256, filetype in installers + zip_files:

            release_type = get_release_type(is_stable)
            channel = get_channel_name(name)
            platform = get_platform(filename)

            if is_unique_record(db, AndroidStudioRelease.c.sha256 == sha256):
                release = AndroidStudioRelease(date=date, name=name, category=release_type, release_type=channel,
                                               filename=filename, location=download_location, sha256=sha256,
                                               filetype=filetype, platform=platform)
                release.save(db)
                print(f"Added Record with SHA256 of {sha256} to the database. {channel} for {platform}.")
            else:
                print(f"Record with SHA256 of {sha256} is already in the database")

    # for release in AndroidStudioRelease.load(db, (AndroidStudioRelease.c.platform == "Linux") & (AndroidStudioRelease.c.category == "Preview")):
    #     print(release)

    db.close()


archive_tos_html = requests.get(url)
archive_tos_soup = BeautifulSoup(archive_tos_html.content, "html.parser")

android_studio_download_url = archive_tos_soup.find("iframe").attrs['data-src']

archive_all_releases_html = requests.get(android_studio_download_url)
archive_all_releases_soup = BeautifulSoup(archive_all_releases_html.content, "html.parser")

all_downloads = archive_all_releases_soup.select("div.all-downloads section")

extract_android_studio_info(all_downloads)
