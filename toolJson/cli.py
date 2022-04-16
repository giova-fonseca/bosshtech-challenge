"""This module provides the RP To-Do CLI."""
import argparse
import shutil
import os
import sys

import json
import typer
import toolJson

from typing import Optional
from toolJson import __app_name__, __version__

app = typer.Typer()

SRC = os.getcwd() + "\\toolJson\\sample_data"
DST = os.getcwd() + "\\toolJson\\output_data"
BOSSTECH = DST + "\\boss-tech.json"
QUICKBOOKS = DST + "\\quickbooks.json"


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def setup():
    """
        copy the `sample_data` into the `output_data` folder.

    Keyword arguments:
    argument -- description
    Return: nothing
    """

    try:
        destination = shutil.copytree(SRC, DST, dirs_exist_ok=True)
    except Exception as e:
        print(e)


@app.command()
def reset():
    """
        reset the state of the `output_data` folder.

    Keyword arguments:
    argument -- description
    Return: nothing
    """

    shutil.rmtree(DST)

    if not os.path.exists(DST):
        os.mkdir(DST)


@app.command()
def sync():
    """
        normalized data model for BOSS.tech customers & companies.

    Keyword arguments:
    argument -- description
    Return: nothing
    """

    DST = os.getcwd() + "\\toolJson\\output_data"

    if os.path.exists(DST):
        if os.path.exists(BOSSTECH):
            with open(BOSSTECH, 'w') as file_dest:
                with open(QUICKBOOKS, 'r') as file_source:
                    jsonObject = json.load(file_source)
                    file_source.close()
                    json.dump(file_dest, jsonObject)
                    file_dest.close()
        else:
            print(f"Error the directory {DST} not exists")
    else:
        print(f"Error the directory {DST} not exists")


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
