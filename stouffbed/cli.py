"""
stouffbed.cli
~~~~~~~~~~~~~~
:copyright: (c) 2017 Sander Bollen
:copyright: (c) 2017 Leiden University Medical Center
:license: MIT
"""

import click

from . import __version__

shared_options = [
    click.option("--input", "-i", type=click.Path(exists=True),
                 required=True, help="Path(s) to input bed file(s)",
                 multiple=True)
]


def generic_option(options):
    """
    Decorator to add generic options to Click CLI's
    The group parent should NOT be decorated with this decorator
    :param options: list of click.option
    :return: decorated function
    """
    def __generic_option(func):
        for option in reversed(options):
            func = option(func)
        return func
    return __generic_option


@click.group()
@click.version_option()
def cli(**kwargs):
    """
    Calculate Stouffer's z scores across or within 4-column bed files

    \b

    Two sub-commands are currently supported:

    \b
      - horizontal: Calculate Stouffer's z-scores across bed files
      - vertical: Calculate Stouffer's z-scores within bed files
    """
    pass


@click.command(short_help="Across bed files")
@generic_option(shared_options)
@click.option("--output", "-o", type=click.Path(exists=True),
              required=True, help="Path to output bed file")
def horizontal_cli(**kwargs):
    """
    Calculate Stouffer's zscores across files

    \b
    Output will be a single bed file, with the fourth column
    being the Stouffer's zscore.

    \b
    Input files must have the exact same regions, in exactly the same
    order.
    """
    pass


@click.command(short_help="Within bed files")
@generic_option(shared_options)
@click.option("--output", "-o", type=click.Path(exists=True),
              required=True, help="Path(s) to output bed file(s)",
              multiple=True)
@click.option("--window-size", "-w", type=int, default=3)
def vertical_cli(**kwargs):
    """
    Calculate Stouffer's zscores within files

    \b
    Order of input and output files on command line must be identical.
    E.g.:
      * "stouffbed vertical -i 1.bed -i 2.bed -o 1.out.bed -o 2.out.bed" -> correct
      * "stouffbed vertical -i 1.bed -i 2. bed -o 2.out.bed -o 1.out.bed" -> incorrect

    \b
    Stouffer zscores will be calculate for window size `w`.
    """
    pass


def main():
    cli.add_command(horizontal_cli, "horizontal")
    cli.add_command(vertical_cli, "vertical")
    cli()


if __name__ == "__main__":
    main()
