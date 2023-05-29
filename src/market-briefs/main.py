#!/usr/bin/env python3
"""View stock information and receive notifications."""
import argparse
import sys
from auth import Auth
from stocks import Stocks
from notifications import Notifications

auth = Auth()
stocks = Stocks()
notifications = Notifications()

VERSION = "0.0.1"


def get_version():
    """Print the version and exit."""
    print(f"Version: {VERSION}")
    sys.exit(0)


def main(argv=None):
    """Main entrypoint for working with stocks."""
    # Create the parser
    description = 'Stocks!'
    job_options = argparse.ArgumentParser(description=description)

    # Add the arguments
    job_options.add_argument('-v',
                             '--version',
                             default=False,
                             action='store_true',
                             help='Prints the version and exits.')
    job_options.add_argument('-e',
                             '--email',
                             default=False,
                             action='store_true',
                             help='Email alerts for stock changes.')

    args = job_options.parse_args(argv)

    if args.version:
        get_version()
    if args.email:
        notifications.email()


if __name__ == "__main__":
    main()
