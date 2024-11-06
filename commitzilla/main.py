import os
from typing_extensions import Annotated
import typer
from rich import print
import questionary

from commitzilla.config import CzConfig, ConfigSchema
from commitzilla.characters import CharacterDict

app = typer.Typer()


@app.command()
def install():
    typer.echo("Hello World!")


@app.command()
def uninstall():
    typer.echo("Bye World!")


@app.command()
def configure(
    model: Annotated[str | None, typer.Option(help="OpenAI model to use")] = None,
    api_key: Annotated[str | None, typer.Option(help="OpenAI API key")] = None,
):
    config_schema = ConfigSchema(model=model)
    config = CzConfig()
    config.write(config_schema)

    if api_key:
        os.environ["CZ_API_KEY"] = api_key

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
