#!/usr/bin/env python3
"""Gather news and send email notifications."""
import smtplib
from datetime import date, timedelta
import requests
from auth import Auth
from stocks import Stocks

COMPANY_NAME = "Tesla Inc"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
SUBJECT = "Market Briefs"
WATCH_PERCENT = 5


class Notifications:
    """Gather news and send email notifications."""
    def __init__(self):
        self.auth = Auth()
        self.today = date.today()
        self.yesterday = self.today - timedelta(days=1)
        self.stocks = Stocks()
        self.formatted_articles = []

    def news(self) -> list:
        """Gather news for watched stocks."""
        api_key = self.auth.auth_news()
        companies = self.stocks.closing()
        for symbol, company in companies.items():
            if company["Percentage"] > WATCH_PERCENT:
                news_params = {
                    "q": company["Company"],
                    "qInTitle": company["Company"],
                    "from": self.yesterday,
                    "sortBy": "publishedAt",
                    "apiKey": api_key,
                }
                response = requests.get(url=NEWS_ENDPOINT, params=news_params, timeout=5)
                articles = response.json()["articles"]
                three_articles = articles[:3]

                if company["Difference"] > 0:
                    title = f"{symbol}: {company['Percentage']}% 📈"
                else:
                    title = f"{symbol}: {company['Percentage']}% 📉"

                self.formatted_articles += [f"{title}\n" \
                                            f"Headline: {article['title']}\n" \
                                            f"Brief: {article['description']}\n" \
                                            f"Article: {article['url']}"
                                            for article in three_articles]
        return self.formatted_articles

    def email(self) -> None:
        """Send top news articles to your configured email."""
        email, password, server = self.auth.auth_email()
        self.formatted_articles = self.news()
        message = f"Subject:{SUBJECT}\n\n"
        for article in self.formatted_articles:
            message += f"{article}\n\n"
        with smtplib.SMTP(server) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email,
                                to_addrs=email,
                                msg=message.encode("utf-8"))
