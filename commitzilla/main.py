import typer
from rich import print

from commitzilla.config import CzConfig, ConfigSchema

app = typer.Typer()


@app.command()
def install():
    typer.echo("Hello World!")


@app.command()
def uninstall():
    typer.echo("Bye World!")


@app.command()
def configure():
    config = CzConfig()
    config.write(ConfigSchema(model="test", prompt="test"))
    print(
        ":white_check_mark: [green]Successfully configured [bold]commitzilla[/bold][/green]"
    )
