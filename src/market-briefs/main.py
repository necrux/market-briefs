#!/usr/bin/env python3
"""View stock information and receive notifications."""
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


def main():
    """Main entrypoint for working with stocks."""
    notifications.email()


if __name__ == "__main__":
    main()
