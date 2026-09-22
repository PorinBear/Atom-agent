import re
from pathlib import Path


class Workspace:
    def __init__(self, name: str, data_dir: str):
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,48}", name): raise ValueError("Virheellinen työtilan nimi.")
        self.name = name; self.root = (Path(data_dir).resolve() / name).resolve()
        self.profile_dir = self.root / "browser-profile"; self.downloads_dir = self.root / "downloads"
        self.files_dir = self.root / "files"; self.logs_dir = self.root / "logs"
        for folder in (self.profile_dir, self.downloads_dir, self.files_dir, self.logs_dir): folder.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _safe(base: Path, name: str) -> Path:
        candidate = (base / name).resolve()
        if candidate != base.resolve() and base.resolve() not in candidate.parents: raise ValueError("Polku poistuu työtilasta.")
        return candidate

    def safe_input_path(self, name: str) -> Path:
        path = self._safe(self.files_dir, name)
        if not path.is_file(): raise FileNotFoundError(name)
        return path

    def safe_output_path(self, name: str, base: Path) -> Path:
        path = self._safe(base, name); path.parent.mkdir(parents=True, exist_ok=True); return path
