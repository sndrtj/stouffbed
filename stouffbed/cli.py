"""
stouffbed.cli
~~~~~~~~~~~~~~
:copyright: (c) 2017 Sander Bollen
:copyright: (c) 2017 Leiden University Medical Center
:license: MIT
"""

import click

from . import __version__
from .stouff import horizontal_stouff, bed_reader, \
    vertical_stouff, bed_to_string

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
@click.option("--output", "-o", type=click.Path(exists=False),
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
    input_filenames = kwargs.get("input")
    output_name = kwargs.get("output")
    readers = [bed_reader(x) for x in input_filenames]
    with open(output_name, "w") as ohandle:
        for item in horizontal_stouff(readers):
            line = bed_to_string(item) + "\n"
            ohandle.write(line)


@click.command(short_help="Within bed files")
@generic_option(shared_options)
@click.option("--output", "-o", type=click.Path(exists=False),
              required=True, help="Path(s) to output bed file(s)")
@click.option("--window-size", "-w", type=int, default=3)
def vertical_cli(**kwargs):
    """
    Calculate Stouffer's zscores within a file

    \b
    Stouffer zscores will be calculate for window size `w`.
    """
    input_files = kwargs.get("input")
    output = kwargs.get("output")
    window = kwargs.get("window_size")

    if len(input_files) > 1:
        raise ValueError("Vertical mode does not support multiple inputs")
    reader = bed_reader(input_files[0])
    with open(output, "w") as ohandle:
        for item in vertical_stouff(reader, window):
            line = bed_to_string(item) + "\n"
            ohandle.write(line)


def main():
    cli.add_command(horizontal_cli, "horizontal")
    cli.add_command(vertical_cli, "vertical")
    cli()


if __name__ == "__main__":
    main()
