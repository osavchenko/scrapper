import re
import requests
from bs4 import BeautifulSoup

from models import ProductInfo, Review


class Scrapper:
    NUMBER_REGEX_PATTERN = "((?:\d+)(?:,\d+)?)"
    api_key = None

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def __cast_to_int(value):
        return int(value.replace(',', ''))

    @staticmethod
    def __process_attribute(regex_pattern, regex_group, element, default_value = "0"):
        """Get attribute value"""
        if not element:
            return default_value

        result = re.search(regex_pattern, element.text.strip())

        if not result:
            return default_value

        return result[regex_group]

    def get_product_data(self, asin):
        """Get base product data"""
        response = requests.get(
            'https://app.zenscrape.com/api/v1/get',
            headers={"apikey": self.api_key},
            params={
                "url": "https://www.amazon.com/dp/" + asin.asin,
                "location": "us",
                "render": "true"
            })

        if response.status_code is not 200:
            raise Exception("Something worong with product ASIN " + asin.asin)

        soup = BeautifulSoup(response.text, features="html.parser")
        title = soup.find("span", {
            "id": "productTitle"
        }).text.strip()
        rating = re.search(r"(\d(?:\.\d)?) out of 5", soup.find("span", {
            "id": "acrPopover"
        }).attrs["title"].strip())[1]
        ratings_count = self.__process_attribute(self.NUMBER_REGEX_PATTERN, 0, soup.find("span", {
            "id": "acrCustomerReviewText"
        }))

        return ProductInfo(asin, title, rating, self.__cast_to_int(ratings_count))

    def get_review_data(self, asin):
        """Get product review data"""
        response = requests.get(
            'https://app.zenscrape.com/api/v1/get',
            headers={"apikey": self.api_key},
            params={
                "url": "https://www.amazon.com/product-reviews/" + asin.asin,
                "location": "us",
                "render": "true"
            })

        if response.status_code is not 200:
            raise Exception("Something worong with product ASIN " + asin.asin)

        soup = BeautifulSoup(response.text, features="html.parser")
        total_reviews = self.__process_attribute(r"of " + self.NUMBER_REGEX_PATTERN + " review", 1, soup.find("div", {
            "id": "filter-info-section"
        }))

        positive_reviews_wrapper = soup.find("div", {
            "class": "positive-review"
        })

        if not positive_reviews_wrapper:
            positive_reviews = "0"
        else:
            positive_reviews = self.__process_attribute(self.NUMBER_REGEX_PATTERN, 0, positive_reviews_wrapper.find("span", {
                "class": "a-declarative"
            }))

        answered_questions = self.__process_attribute(self.NUMBER_REGEX_PATTERN, 1, soup.find("a", {
            "class": "askSeeAllQuestionsLink"
        }))

        return Review(asin,
                      self.__cast_to_int(total_reviews),
                      self.__cast_to_int(positive_reviews),
                      self.__cast_to_int(answered_questions))
