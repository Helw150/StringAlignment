import sys


def default_args(service_description, argparser):
    argparser.add_argument('--port', '-p', type=int,
                           default=service_description.port)

if sys.version_info <= (3, 0):
    print("This program only runs in python3", file=sys.stderr)
    exit(1)
