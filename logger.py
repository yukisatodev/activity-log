#!/usr/bin/env python3
"""Log today's public GitHub commit activity to data/activity.json."""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "yukisatodev")
JST = timezone(timedelta(hours=9))
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "activity.json")


def fetch_public_events(username):
    url = f"https://api.github.com/users/{username}/events/public?per_page=100"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{username}-activity-logger",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        print(f"GitHub API error: {e.code} {e.reason}", file=sys.stderr)
        return []
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        return []


def count_todays_commits(events, today_jst):
    total = 0
    for event in events:
        if event.get("type") != "PushEvent":
            continue
        created_at = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
        if created_at.astimezone(JST).date() != today_jst:
            continue
        total += len(event.get("payload", {}).get("commits", []))
    return total


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
    events = fetch_public_events(GITHUB_USERNAME)
    commit_count = count_todays_commits(events, today)

    data = load_data()
    data[today.isoformat()] = commit_count
    save_data(data)

    print(f"{today.isoformat()}: {commit_count} commit(s) logged for {GITHUB_USERNAME}")


if __name__ == "__main__":
    main()
