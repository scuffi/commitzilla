import os
from configparser import ConfigParser
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ConfigSchema:
    model: Optional[str] = None
    prefix: Optional[str] = None
    character_name: Optional[str] = None
    character_prompt: Optional[str] = None

    def as_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


class CzConfig:
    def __init__(
        self, working_dir: Path = Path.cwd(), *, config_file_name: str = "cz-config.ini"
    ):
        self._config_file_name = config_file_name
        self._config_path = working_dir / ".git" / "hooks" / config_file_name
        self.config = self._get_or_create_config(working_dir)

    def _get_or_create_config(self, working_dir: Path):
        """
        Checks for the existence of a `.git` directory in the specified working directory and returns a config
        if it exists, if not, it raises a `FileNotFoundError`.

        Args:
          working_dir (Path): The `working_dir` parameter is a `Path` object representing the directory
        where the code is being executed. The function checks if a `.git` directory exists within the
        specified `working_dir`, and if not, it raises a `FileNotFoundError`. It then reads a configuration
        file using `configparser

        Returns:
          a `config` object of type `ConfigParser` after checking for the existence of a `.git` directory in
        the specified `working_dir`, reading a configuration file from `_config_path`, and adding a
        "settings" section if it doesn't already exist in the configuration.
        """
        if not os.path.exists(working_dir / ".git" / "hooks"):
            raise FileNotFoundError(
                f"No .git directory found in the specified working directory: {working_dir}"
            )

        config = ConfigParser()
        config.read(self._config_path)

        if "settings" not in config.sections():
            config.add_section("settings")

        return config

    def write(self, config_data: ConfigSchema):
        """
        Writes the configuration data to the config file.

        Args:
          config_data (ConfigSchema): ConfigSchema object that contains configuration data to be written to
        a file.
        """
        for key, value in config_data.as_dict().items():
            self.config.set("settings", key, value)

        with open(self._config_path, "w") as configfile:
            self.config.write(configfile)

    def get(self, value: str) -> Optional[str]:
        return self.config.get("settings", value, fallback=None)
