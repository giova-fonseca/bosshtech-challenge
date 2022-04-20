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
SALESFORCE = DST + "\\salesforce.json"
QUICKBOOKS = DST + "\\quickbooks.json"


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command(name="setup")
def setup():
    """
        copy the `sample_data` into the `output_data` folder.

    Keyword arguments:
    argument -- description
    Return: nothing
    """

    try:
        destination = shutil.copytree(SRC, DST, dirs_exist_ok=True)
        print("Setup completed successfully !")

    except Exception as e:
        print(e)


@app.command(name="reset")
def reset():
    """
        reset the state of the `output_data` folder.

    Keyword arguments:
    argument -- description
    Return: nothing
    """

    try:
        shutil.rmtree(DST)

        if not os.path.exists(DST):
            os.mkdir(DST)

        print("Reset completed successfully !")
    except Exception as e:
        print(e)


@app.command(name="sync")
def sync():
    """
        normalized data model for BOSS.tech customers & companies.

    Keyword arguments:
    argument -- description
    Return: nothing
    """
    list_customers = []
    list_companies = []

    try:
        if os.path.exists(DST):
            if os.path.exists(BOSSTECH):
                with open(BOSSTECH, 'r') as file_dest:
                    jsonDest = json.load(file_dest)
                    list_customers = jsonDest.get("customers")
                    # list_companies = jsonDest.get("companies")
                    list_companies = jsonDest.get("companies")

                    with open(QUICKBOOKS, 'r') as quickbook_source:
                        jsonObject = json.load(quickbook_source)

                        for key, value in jsonObject.items():
                            if type(value) == list:
                                for item in value:
                                    list_customers.append(item)

                                    if item.get("CompanyName") not in list_companies:

                                        if os.path.exists(SALESFORCE):
                                            with open(SALESFORCE, 'r') as salesforce_source:
                                                jsonSalesforce = json.load(
                                                    salesforce_source)

                                                list_temp = jsonSalesforce.get(
                                                    "records")

                                                for element in list_temp:
                                                    # if item.get("CompanyName") not in list_companies:
                                                    if len(list_companies) == 0:
                                                        list_companies.append({
                                                            "name": element.get("name"),
                                                            "phone": element.get("phone"),
                                                            "website": element.get("website"),
                                                            "numberOfEmployees": element.get(
                                                                "numberOfEmployees"),
                                                            "industry": element.get("industry")})
                                                    else:
                                                        # import pdb

                                                        # pdb.set_trace()

                                                        if element.get("name") != list_companies[0].get('name'):
                                                            list_companies.append({
                                                                "name": element.get("name"),
                                                                "phone": element.get("phone"),
                                                                "website": element.get("website"),
                                                                "numberOfEmployees": element.get(
                                                                    "numberOfEmployees"),
                                                                "industry": element.get("industry")})

                with open(BOSSTECH, 'r+') as file_dest:
                    json.dump(jsonDest, file_dest)
                print("Sync completed successfully !")
            else:
                print(f"Error the directory {DST} not exists")
        else:
            print(f"Error the directory {DST} not exists")
    except Exception as e:
        print(e)


@ app.command(name="update")
def update(current_name: str = typer.Argument(...), new_name: str = typer.Argument(...)):
    """
        allow a user to update a customer's name which has been synced to the `boss-tech.json`,
        this update should propagate to all "customer integrations" that have been "synced".

    Keyword arguments:
    argument -- description
    Return: nothing
    """

    if os.path.exists(BOSSTECH):
        with open(BOSSTECH, 'r') as file_dest:
            jsonDest = json.load(file_dest)
            list_customers = jsonDest.get("customers")
            for item in list_customers:
                if item.get("FullyQualifiedName") == current_name:
                    item["FullyQualifiedName"] = new_name
                    item["DisplayName"] = new_name

        with open(BOSSTECH, 'w') as file_dest:
            json.dump(jsonDest, file_dest)
        print("Update completed successfully !")


@ app.callback()
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
