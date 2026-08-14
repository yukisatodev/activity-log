#!/usr/bin/env python3
"""Backfill data/activity.json with past GitHub contribution history.

Usage:
    python3 backfill.py               # last 12 months (GitHub's default view)
    python3 backfill.py --years 5     # last 12 months, plus 4 more years back
"""

import argparse
import json
import os
from datetime import date

from contributions import fetch_contributions

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "yukisatodev")
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "activity.json")


def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", type=int, default=1,
                         help="how many trailing years to fetch (default: 1, i.e. last 12 months only)")
    args = parser.parse_args()

    data = load_data()
    today = date.today()

    print(f"Fetching last 12 months for {GITHUB_USERNAME}...")
    data.update(fetch_contributions(GITHUB_USERNAME))

    for i in range(1, args.years):
        to_date = date(today.year - i, today.month, min(today.day, 28))
        from_date = date(to_date.year - 1, to_date.month, to_date.day)
        print(f"Fetching {from_date} to {to_date}...")
        data.update(fetch_contributions(
            GITHUB_USERNAME, from_date.isoformat(), to_date.isoformat()
        ))

    save_data(data)
    nonzero = sum(1 for v in data.values() if v > 0)
    print(f"Done. {len(data)} days on record, {nonzero} with contributions.")


if __name__ == "__main__":
    main()
