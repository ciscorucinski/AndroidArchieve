from enum import Enum
from typing import Union


class Release(Enum):
    CANARY = 1
    BETA = 2
    RC = 3
    STABLE = 4
    PREVIEW = 0

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.current = {"latest": (0, 0, None)}     # tuple is (version, payload)
        return obj

    @classmethod
    def all_versions(cls, release: "Release" = None, *, include_2_4=True, include_latest=True):
        if type(release) is not Release:
            release = Release.CANARY
        keys = set()
        for enum in Release:
            if enum is release:
                keys = set(enum.current.keys())

        if not include_latest:
            keys.discard("latest")
        if include_2_4:
            keys.add("2.4")

        return sorted(keys)

    @classmethod
    def data(cls, version, release: "Release"):
        return release.current.get(version, None)

    @classmethod
    def latest_releases(cls, stable_only=False):
        return cls._get_releases("latest", stable_only=stable_only)

    @classmethod
    def releases(cls, version):
        return cls._get_releases(version, stable_only=False)

    @classmethod
    def _get_releases(cls, version, stable_only):
        release = dict()
        release.update({"stable": cls.STABLE.current.get(version),
                        "rc": cls.RC.current.get(version) if not stable_only else None,
                        "beta": cls.BETA.current.get(version) if not stable_only else None,
                        "canary": cls.CANARY.current.get(version) if not stable_only else None})
        if version == "2.4":
            release.update({"preview": cls.PREVIEW.current.get(version) if not stable_only else None})
        return release

    @staticmethod
    def cascading_add(release: Union[str, "Release"], version, name, url):
        if type(release) is str:
            release = Release[release.upper()]
        release.current[version] = (name, url)
        release.current["latest"] = (version, name, url)
        if release is not Release.CANARY and release is not Release.PREVIEW:
            Release.cascading_add(Release(release.value - 1), version, name, url)
        return
