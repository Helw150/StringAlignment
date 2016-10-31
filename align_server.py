#!/usr/bin/env python3
import sys
import argparse
import json
import os
import subprocess

from libs.server.Service import Service
from libs.server.Service import ServiceHandler
from libs.server.Service import ServiceDescription
from libs.server.args import default_args

indices_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../search_server/IndexFiles/")

service_description = ServiceDescription("align", 8400)

class AlignHandler(ServiceHandler):
    def process(self, query):
        print("GOT QUERY")
        line = subprocess.getoutput('go run AlignHandler.go ' + query['source'] + " " + query['target'])
        line = line.split("\t")
        result = {
            "correct": line[0],
            "guess": line[1]
        }
        print(result)
        return {"status": "received", "response": result}


class AlignService(Service):
    def __init__(self, args):
        dependencies = []
        super().__init__(service_description, dependencies, port=args.port)

    def get_routes(self):
        return [
            (r"/", AlignHandler)
        ]


def main():
    args = argparser.parse_args()
    AlignService(args)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Runs a align server which accepts "
                    "queries and index file on disk. Will generate result indices "
                    "of the matches according to our align algorithm ")
    argparser.add_argument('--indexpath', '-f', type=str, default="IndexFile/",
                           help="Index of the file you are aiming to align")
    default_args(service_description, argparser)
    main()
