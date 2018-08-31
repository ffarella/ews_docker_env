#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import yaml
import io
import click
import jinja2
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", verbose=True)

ews_drives_path = os.getenv("EWS_DRIVES_PATH")
if not ews_drives_path:
    raise RuntimeError("EWS_DRIVES_PATH should be set!")

ews_drives_path_separator = os.getenv(
    "EWS_DRIVES_PATH_SEPARATOR")
if not ews_drives_path_separator:
    raise RuntimeError("EWS_DRIVES_PATH_SEPARATOR should be set!")

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template("docker-compose.jinja-yaml")


@click.command()
@click.option('--py2/--no-py2', help='Add Python 2 jupyter', default=True)
@click.option('--py3/--no-py3', help='Add Python 3 jupyter', default=True)
@click.option('--postgres/--no-postgres', help='Add Postgresql', default=True)
@click.option('--pgadmin/--no-pgadmin', help='Add pgadmin interace', default=True)
@click.option('--mongo/--no-mongo', help='Add MongoDB', default=True)
@click.option('--no_mount', help='Add Python 2 jupyter', is_flag=True)
@click.option('--drives', help='Mounted drives (comma separated)', default="f,p,s,t")
def main(no_mount, py2, py3, postgres, pgadmin, mongo, drives):
    if not postgres:
        pgadmin = False
    drives = drives.upper()
    allowed_drives = []
    if no_mount: 
        allowed_drives = [
            r"{}:/".format(c.upper()) for c in drives.split(',')
        ]
    res = []
    for root in allowed_drives:
        root_replace = "/ews_drives/" + root[0].lower()
        container_replace = ews_drives_path + root[0].lower()
        for path in os.listdir(root):
            fullpath = os.path.join(root, path)
            if not os.path.isdir(fullpath):
                continue
            if path.startswith("."):
                continue
            elif path.startswith("$"):
                continue
            elif path.startswith("__"):
                continue
            elif path.startswith("it_support_nicht_loeschen"):
                continue
            elif path.startswith("pip-"):
                continue
            if "dfsr" in path.lower():
                continue
            xy = (
                fullpath.replace(root, root_replace + "/"),
                ews_drives_path_separator.join([container_replace, path])
            )
            res.append(xy)

    output_text = template.render(
        volumes=res, py2=py2, py3=py3, postgres=postgres, pgadmin=pgadmin, mongo=mongo, drives=drives)
    with open("docker-compose.yaml", "w") as fout:
        fout.write(output_text)


if __name__ == '__main__':
    main()
