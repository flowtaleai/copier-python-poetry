from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from {{cookiecutter.project_slug}} import logs
from {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}} import a_function

logger = logs.get_logger(__name__)


def cli():
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()
    if args.version:
        from . import __version__

        print(__version__)
        return
    logs.configure_logging(args.verbose)

    logger.warning(a_function())


def create_argument_parser() -> ArgumentParser:
    class SortedArgumentDefaultsHelpFormatter(ArgumentDefaultsHelpFormatter):
        def add_arguments(self, actions):
            super().add_arguments(sorted(actions, key=lambda x: x.option_strings))

    arg_parser = ArgumentParser(
        formatter_class=SortedArgumentDefaultsHelpFormatter,
        description="{{ cookiecutter.project_short_description }}",
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase the verbosity of messages: -v for more verbose output and -vv for debug",
    )
    arg_parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="display this application version",
    )
    return arg_parser


if __name__ == "__main__":
    cli()
