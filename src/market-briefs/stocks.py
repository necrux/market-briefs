#!/usr/bin/env python3
"""View stock related information."""
import requests
import yaml
from auth import Auth

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCKS_FILE = "stocks.yaml"


class Stocks:
    """View stock related information."""
    def __init__(self):
        self.auth = Auth()
        self.daily_summary = {}

    def closing(self) -> dict:
        """Gather closing information."""
        stocks = self.parse_stocks()
        api_key = self.auth.auth_stocks()
        for symbol in stocks:
            stock_params = {
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": symbol,
                "apikey": api_key,
            }
            response = requests.get(url=STOCK_ENDPOINT, params=stock_params, timeout=5)
            data = response.json()['Time Series (Daily)']
            data_list = [value for (_, value) in data.items()]
            yesterday_closing_price = float(data_list[0]["4. close"])
            day_before_yesterday_closing_price = float(data_list[1]["4. close"])

            difference = yesterday_closing_price - day_before_yesterday_closing_price
            average = (yesterday_closing_price + day_before_yesterday_closing_price) / 2
            percentage = (abs(difference) / average) * 100
            self.daily_summary[symbol] = {"Company": stocks[symbol],
                                          "Difference": difference,
                                          "Percentage": round(percentage, 2)}
        return self.daily_summary

    @staticmethod
    def parse_stocks() -> dict:
        """Fetch the stocks list and preferences."""
        with open(STOCKS_FILE, encoding="UTF-8") as file:
            stocks = yaml.safe_load(file)["Stocks"]
        return stocks
