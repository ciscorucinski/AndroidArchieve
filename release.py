from enum import Enum


class Release(Enum):
    PREVIEW = 0
    CANARY = 1
    BETA = 2
    RC = 3
    STABLE = 4

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.current = dict()
        return obj

    @classmethod
    def all_versions(cls, release: "Release" = None, *, include_preview: bool = True, include_latest: bool = True):
        if type(release) is not Release:
            release = Release.CANARY
        keys = set(release.current.keys())
        keys.discard("latest") if not include_latest else None
        keys.add("2.4") if include_preview else None
        return sorted(keys)

    @classmethod
    def data(cls, version, release: "Release"):
        return release.current.get(version, None)

    @classmethod
    def releases(cls, version):
        release = dict()
        release.update({"stable": cls.STABLE.current.get(version),
                        "rc": cls.RC.current.get(version),
                        "beta": cls.BETA.current.get(version),
                        "canary": cls.CANARY.current.get(version)})
        if version == "2.4":
            release.update({"preview": cls.PREVIEW.current.get(version)})
        return release

    @staticmethod
    def cascading_add(release, version, name, url):
        if type(release) is str:
            release = Release[release.upper()]
        release.current[version] = (name, url)
        release.current["latest"] = (version, name, url)
        if release.value > Release.CANARY.value:
            Release.cascading_add(Release(release.value - 1), version, name, url)
        return

    @staticmethod
    def all_releases(*, minimize: bool):
        releases = []
        for version in Release.all_versions(include_latest=False):
            for release in reversed(Release):
                data = Release.data(version, release)
                if data is not None:
                    releases.append(tuple([version, release.name, data[0], data[1]]))
                    if minimize:
                        break
        return releases
