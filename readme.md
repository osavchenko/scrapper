# Scrapper

## Installation

Generate and activate python virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

Prepare your `.env` file from `.env.dist`

Update database URL in `alembic.ini` (and make it from `alembic.ini.dist`)

Install dependencies:

```sh
pip3 install -r requirements.txt
```

Migrate database:

```sh
alembic upgrade head
```

## Usage

Run application with

```sh
python main.py -i asins_ids.csv
```

Where `i` argument is your path to the `csv` file with ASIN's (by default it's `asins.csv`)
