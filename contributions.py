"""Fetch a GitHub user's public contribution calendar (no auth required).

Scrapes the same HTML calendar that powers the green squares on a GitHub
profile: https://github.com/users/{username}/contributions
"""

import re
import urllib.request
import urllib.error

CELL_RE = re.compile(
    r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*id="([\w-]+)"'
)
TOOLTIP_RE = re.compile(
    r'<tool-tip[^>]*for="([\w-]+)"[^>]*>(\d[\d,]*|No) contributions? on'
)


def fetch_contributions(username, from_date=None, to_date=None):
    """Return {date_str: contribution_count} for the given range.

    With no range given, GitHub returns the trailing 12 months.
    """
    url = f"https://github.com/users/{username}/contributions"
    if from_date and to_date:
        url += f"?from={from_date}&to={to_date}"

    req = urllib.request.Request(url, headers={
        "User-Agent": f"{username}-activity-logger",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            html = res.read().decode()
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"Failed to fetch contributions for {username}: {e}")
        return {}

    cell_id_to_date = dict(
        (cell_id, date) for date, cell_id in CELL_RE.findall(html)
    )
    counts = {}
    for cell_id, count_str in TOOLTIP_RE.findall(html):
        date = cell_id_to_date.get(cell_id)
        if not date:
            continue
        counts[date] = 0 if count_str == "No" else int(count_str.replace(",", ""))
    return counts
