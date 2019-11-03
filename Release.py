from enum import Enum


class Release(Enum):
    Canary = (1, [])
    Beta = (2, [1])
    RC = (3, [2, 1])
    Stable = (4, [3, 2, 1])
    Preview = (0, [])

    def __new__(cls, value, cascade):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.cascade_releases = cascade
        obj.current = {"latest": (0, None)}     # tuple is (version, payload)
        return obj

    @classmethod
    def all_versions(cls, release: "Release" = Canary, *, include_2_4=True, include_latest=True):
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
        release.update({"stable": cls.Stable.current.get(version),
                        "rc": cls.RC.current.get(version) if not stable_only else None,
                        "beta": cls.Beta.current.get(version) if not stable_only else None,
                        "canary": cls.Canary.current.get(version) if not stable_only else None})
        if version == "2.4":
            release.update({"preview": cls.Preview.current.get(version) if not stable_only else None})
        return release

    @staticmethod
    def add(release_string, version, data):
        for release in Release:
            if release_string.lower() == release.name.lower():
                release.current[version] = data
                release.current["latest"] = (version, data)
                Release._cascade(version, release, data)
                break

    @staticmethod
    def _cascade(version, release, data):
        for ordinal in release.cascade_releases:
            cascade = Release(ordinal)
            if cascade.value < release.value:
                cascade.current[version] = data
                if version == cascade.current.get("latest")[0]:
                    cascade.current["latest"] = (version, data)
            else:
                cascade.current[version] = (0, None)
