#!/usr/bin/env python3
"""Log today's public GitHub contribution count to data/activity.json."""

import json
import os
from datetime import datetime, timezone, timedelta

from contributions import fetch_contributions
from stats import current_streak

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "yukisatodev")
JST = timezone(timedelta(hours=9))
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
    today = datetime.now(JST).date()
    calendar = fetch_contributions(GITHUB_USERNAME)
    count = calendar.get(today.isoformat(), 0)

    data = load_data()
    data[today.isoformat()] = count
    save_data(data)

    streak = current_streak(data, today)
    print(f"{today.isoformat()}: {count} contribution(s) logged for {GITHUB_USERNAME} "
          f"(current streak: {streak} day{'s' if streak != 1 else ''})")


if __name__ == "__main__":
    main()
