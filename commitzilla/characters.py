import json
import os
from pathlib import Path


class CharacterDict(dict):
    def __init__(
        self, working_dir: Path = Path.cwd(), *, file_name: str = "cz_characters.json"
    ):
        hooks_dir = working_dir / ".git" / "hooks"
        if not os.path.exists(hooks_dir):
            raise FileNotFoundError(
                f"No .git directory found in the specified working directory: {working_dir}"
            )

        self.file_path = hooks_dir / file_name

        if self.file_path.exists():
            with self.file_path.open("r") as f:
                data = json.load(f)
                super().update(data)
        else:
            self.file_path.write_text("{}")

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._save()

    def _save(self):
        with self.file_path.open("w") as f:
            json.dump(self, f)
