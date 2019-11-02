from enum import Enum


class Release(Enum):
    Canary = ([],)
    Beta = ([1],)
    RC = ([2, 1],)
    Stable = ([3, 2, 1],)
    Preview = ([],)

    def __new__(cls, cascade):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.cascade_releases = cascade
        obj.current = {"latest": (0, None)}     # tuple is (version, payload)
        return obj

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
        for cascade in release.cascade_releases:
            cascaded_type = Release(cascade)
            if cascaded_type.value < release.value:
                cascaded_type.current[version] = data
                if version == cascaded_type.current.get("latest")[0]:
                    cascaded_type.current["latest"] = (version, data)
            else:
                cascaded_type.current[version] = (0, None)
