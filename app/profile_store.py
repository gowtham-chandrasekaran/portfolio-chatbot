from pathlib import Path

class ProfileStore:
    def __init__(self, path: str = "app/content/profile.md"):
        self._path = Path(path)
        self._cache: str | None = None

    def load(self) -> str:
        if self._cache is None:
            self._cache = self._path.read_text(encoding="utf-8").strip()
        return self._cache

    def refresh(self) -> str:
        self._cache = None
        return self.load()

profile_store = ProfileStore()
