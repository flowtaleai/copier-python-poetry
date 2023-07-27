"""{{cookiecutter.project_slug}} CLI"""
import click

from {{cookiecutter.project_slug}} import __version__
from {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}} import a_function


@click.command()
@click.version_option(__version__)
def cli():
    """The main way to engange with {{cookiecutter.project_slug}} is with this cli"""
    print(a_function())
