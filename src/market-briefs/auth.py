#!/usr/bin/env python3
"""Configure and authenticate to the required API endpoints."""
import configparser
from os import path


class Auth:
    """Configure and authenticate to the required API endpoints."""

    def __init__(self):
        self.auth_file = f"{path.expanduser('~')}/.keys"
        self.config = configparser.RawConfigParser()
        self.config.read(self.auth_file)
        self.stocks_section = "alpha-vantage"
        self.news_section = "news"
        self.smtp_section = "stocks"

    def configure_news(self):
        """Configure the new API."""
        pass

    def configure_stocks(self):
        """Configure the stocks API."""
        pass

    def configure_smtp(self):
        """Configure the SMTP service."""
        pass

    def auth_stocks(self) -> str:
        """Fetch the API key for the stocks service."""
        try:
            stocks_api_key = self.config[self.stocks_section]["key"]
            return stocks_api_key
        except KeyError:
            print("Key error.")

    def auth_news(self) -> str:
        """Fetch the API key for the news service."""
        try:
            news_api_key = self.config[self.news_section]["key"]
            return news_api_key
        except KeyError:
            print("Key error.")

    def auth_email(self) -> tuple:
        """Fetch the API key for the smtp service."""
        try:
            email = self.config[self.smtp_section]["email"]
            password = self.config[self.smtp_section]["password"]
            server = self.config[self.smtp_section]["smtp"]
            return email, password, server
        except KeyError:
            print("Key error.")
