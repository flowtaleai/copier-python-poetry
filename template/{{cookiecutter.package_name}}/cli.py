"""{{cookiecutter.package_name}} CLI"""
import click

from {{cookiecutter.package_name}} import __version__
from {{cookiecutter.package_name}}.{{cookiecutter.package_name}} import a_function


@click.command()
@click.version_option(__version__)
def cli():
    """The main way to engange with {{cookiecutter.package_name}} is with this cli"""
    print(a_function())
