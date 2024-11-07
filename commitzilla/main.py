import os
from pathlib import Path
import shutil
import stat
from typing import Optional
from typing_extensions import Annotated
import typer
from rich import print
import questionary
import keyring

from commitzilla.config import CzConfig, ConfigSchema
from commitzilla.characters import CharacterDict

app = typer.Typer()

DEFAULT_MODEL = "gpt-4o-mini"


@app.command()
def install():
    # TODO: First check if we already have everything installed
    api_key = questionary.password("Enter your OpenAI API key").ask()

    _update_values(api_key=api_key)

    CharacterDict()
    character_name, character_prompt = _input_character()

    config_schema = ConfigSchema(
        model="gpt-4o-mini",
        character_name=character_name,
        character_prompt=character_prompt,
    )
    config = CzConfig()
    config.write(config_schema)

    _move_hook_file()

    print(
        ":white_check_mark: [green]Successfully installed [bold]commitzilla[/bold][/green]!"
    )

    """
    Create a default configuration file (default model should be gpt-4o-mini).
    Move characters file into .git/hooks.
    
    Move prepare-commit-msg hook into .git/hooks.
    """


@app.command()
def uninstall():
    typer.echo("Bye World!")


@app.command()
def configure(
    model: Annotated[str | None, typer.Option(help="OpenAI model to use")] = None,
    api_key: Annotated[str | None, typer.Option(help="OpenAI API key")] = None,
):
    _update_values(model, api_key)

    if updated_values := [
        t[0] for t in zip(("model", "api_key"), (model, api_key)) if t[1]
    ]:
        print(
            f":white_check_mark: [green]Successfully updated [bold]commitzilla[/bold] values: {', '.join(updated_values)}[/green]"
        )
        return
    print(
        ":grey_question: No configuration parameters were specified, try running [bold]commitzilla configure --help[/bold] for more information"
    )


@app.command()
def character():
    character_name, character_prompt = _input_character()

    use_now = questionary.confirm("Do you want to use this character now?").ask()

    if use_now:
        config = CzConfig()
        config.write(
            ConfigSchema(
                character_name=character_name, character_prompt=character_prompt
            )
        )
        print(
            f":white_check_mark: [green]Now using '{character_name}' character[/green]"
        )
        return

    print(f":white_check_mark: [green]Saved '{character_name}' character[/green]")


def _update_values(model: Optional[str] = None, api_key: Optional[str] = None):
    config_schema = ConfigSchema(model=model)
    config = CzConfig()
    config.write(config_schema)

    if api_key:
        keyring.set_password("commitzilla", "api_key", api_key)


def _move_hook_file():
    local_path = Path(__file__).parent.resolve() / "prepare-commit-msg.py"
    hook_path = Path.cwd() / ".git" / "hooks" / "prepare-commit-msg"

    shutil.copy(local_path, hook_path)

    # We need to edit the permissions of the file, so git can execute it
    os.chmod(
        hook_path,
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IXUSR
        | stat.S_IRGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH,
    )


def _input_character():
    choices = ["Preconfigured", "Custom"]
    selection = questionary.select(
        "Do you want to use a preconfigured character, or prompt your own?",
        choices=choices,
    ).ask()

    characters = CharacterDict()
    character_prompt = None

    if selection == choices[0]:
        character_name = questionary.select(
            "Which character do you want to use?",
            choices=sorted(characters.keys()),
        ).ask()

        character_prompt = characters[character_name]

    else:
        character_name = questionary.text(
            "What's the name of this character (does not affect the prompt):"
        ).ask()
        character_prompt = questionary.text(
            f"What's the custom prompt for '{character_name}':"
        ).ask()

        characters[character_name] = character_prompt

    return (character_name, character_prompt)
