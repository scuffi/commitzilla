import json
import os
import shutil
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
            default_characters_file = Path(__file__).parent.resolve() / file_name
            self._move_default_characters_file(default_characters_file, self.file_path)

    def _move_default_characters_file(
        self, default_characters_file: Path, characters_file: Path
    ):
        print(f"Checking for default characters: {default_characters_file}")

        if os.path.exists(default_characters_file) and not os.path.exists(
            characters_file
        ):
            shutil.copy(default_characters_file, characters_file)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._save()

    def _save(self):
        with self.file_path.open("w") as f:
            json.dump(self, f)
