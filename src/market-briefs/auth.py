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
        """Configure the News API key."""
        self.config.read(self.auth_file)
        print("What is your News API key?")
        print("    How to get a key: https://newsapi.org/register")
        api_key = input(": ")
        if not self.config.has_section(self.news_section):
            self.config.add_section(self.news_section)
            self.config.set(self.news_section, "key", api_key)

        with open(self.auth_file, "w", encoding="UTF-8") as file:
            self.config.write(file)

    def configure_stocks(self):
        """Configure the Alpha Vantage API key."""
        self.config.read(self.auth_file)
        print("What is your Alpha Vantage API key?")
        print("    How to get a key: https://www.alphavantage.co/support/#api-key")
        api_key = input(": ")
        if not self.config.has_section(self.stocks_section):
            self.config.add_section(self.stocks_section)
            self.config.set(self.stocks_section, "key", api_key)

        with open(self.auth_file, "w", encoding="UTF-8") as file:
            self.config.write(file)

    def configure_smtp(self):
        """Configure SMTP authentication."""
        self.config.read(self.auth_file)
        print("Provide your SMTP information below.")
        email = input("email: ")
        password = input("password: ")
        smtp = input("SMTP Server: ")
        if not self.config.has_section(self.smtp_section):
            self.config.add_section(self.smtp_section)
            self.config.set(self.smtp_section, "email", email)
            self.config.set(self.smtp_section, "password", password)
            self.config.set(self.smtp_section, "smtp", smtp)

        with open(self.auth_file, "w", encoding="UTF-8") as file:
            self.config.write(file)

    def auth_stocks(self) -> str:
        """Fetch the API key for the stocks service."""
        try:
            stocks_api_key = self.config[self.stocks_section]["key"]
        except KeyError:
            print("Must first configure the stocks API.")
            self.configure_stocks()
        finally:
            stocks_api_key = self.config[self.stocks_section]["key"]
        return stocks_api_key

    def auth_news(self) -> str:
        """Fetch the API key for the news service."""
        try:
            news_api_key = self.config[self.news_section]["key"]
        except KeyError:
            print("Must first configure the news API.")
            self.configure_news()
        finally:
            news_api_key = self.config[self.news_section]["key"]
        return news_api_key

    def auth_email(self) -> tuple:
        """Fetch the API key for the smtp service."""
        try:
            email = self.config[self.smtp_section]["email"]
            password = self.config[self.smtp_section]["password"]
            server = self.config[self.smtp_section]["smtp"]
        except KeyError:
            print("Must first configure an email service.")
            self.configure_smtp()
        finally:
            email = self.config[self.smtp_section]["email"]
            password = self.config[self.smtp_section]["password"]
            server = self.config[self.smtp_section]["smtp"]
        return email, password, server
