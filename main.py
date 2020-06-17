import argparse
import csv
import sys

from os import environ as env

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Asin
from scrapper import Scrapper

from dotenv import find_dotenv, load_dotenv


def prepare_env():
    """Prepare environment variables"""
    env_file = find_dotenv()

    if env_file:
        load_dotenv(env_file)


def prepare_args():
    """Prepare application arguments and options"""
    parser = argparse.ArgumentParser(description="Grab Amazon product data")
    parser.add_argument("-i", help="ASINs CSV file path", default="asins.csv")

    return parser.parse_args()


def read_asins(filename):
    """Read ASINs from file"""
    asins = []

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            if row[0] not in asins:
                asins.append(row[0])

    return asins


def init_database_connection():
    """Init database connection"""
    engine = create_engine(env.get("DATABASE_URL"))
    Session = sessionmaker(bind=engine)

    return Session()


if __name__ == "__main__":
    prepare_env()
    args = prepare_args()
    db = init_database_connection()

    for asin_id in read_asins(args.i):
        print(asin_id)
        asin = db.query(Asin).filter_by(asin=asin_id).first()

        if not asin:
            asin = Asin(asin_id)
            db.add(asin)

        scrapper = Scrapper(env.get("ZENSCRAPE_API_KEY"))
        try:
            product = scrapper.get_product_data(asin)
            db.add(product)
            review = scrapper.get_review_data(asin)
            db.add(review)
        except Exception as exception:
            print(exception, file=sys.stderr)
            continue

        db.commit()
