#!/usr/bin/env python3

import os
import sys
import http.client
import json
from dataclasses import dataclass
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

try:
    import keyring
except ImportError:
    raise ModuleNotFoundError(
        "commitzilla could not find `keyring`. Please install keyring using: `pip install keyring` and add your OpenAI key using `commitzilla configure`"
    )


@dataclass
class Config:
    model: Optional[str]
    character_name: Optional[str]
    character_prompt: Optional[str]
    openai_api_key: Optional[str]


def _load_config(working_dir: Path = Path.cwd(), config_name: str = "cz-config.ini"):
    config_path = working_dir / ".git" / "hooks" / config_name
    if not os.path.exists(config_path):
        return None

    config = ConfigParser()
    config.read(config_path)

    # TODO: Add validation here, raise value error if any aren't found

    return Config(
        model=config.get("settings", "model", fallback=None),
        character_name=config.get("settings", "character_name", fallback=None),
        character_prompt=config.get("settings", "character_prompt", fallback=None),
        openai_api_key=keyring.get_password("commitzilla", "api_key"),
    )


def generate_commit_message(commit_msg: str, config: Config):
    connection = http.client.HTTPSConnection("api.openai.com")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.openai_api_key}",
    }

    data = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": config.character_prompt},
            {"role": "user", "content": commit_msg},
        ],
        "max_tokens": 100,
    }

    connection.request(
        "POST", "/v1/chat/completions", body=json.dumps(data), headers=headers
    )
    response = connection.getresponse()

    if response.status == 200:
        response_data = response.read()
        completion = json.loads(response_data)
        message = completion["choices"][0]["message"]["content"].strip()
        return message
    else:
        print(f"Error generating commit message: {response.status} - {response.reason}")
        return None


def main():
    commit_msg_filepath = sys.argv[1]

    with open(commit_msg_filepath, "r") as f:
        commit_msg = f.read().strip()

    config = _load_config()

    if not config:
        print("Failed to load configuration. Using the original message.")
        return

    new_commit_msg = generate_commit_message(commit_msg, config)

    if new_commit_msg:
        with open(commit_msg_filepath, "w") as f:
            f.write(new_commit_msg)
    else:
        print("Failed to generate a commit message. Using the original message.")


if __name__ == "__main__":
    main()
