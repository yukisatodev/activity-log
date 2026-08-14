"""Small stats derived from data/activity.json."""

from datetime import date, timedelta


def current_streak(data, today):
    """Consecutive active days ending today (or yesterday, if today is still 0)."""
    streak = 0
    day = today
    if data.get(day.isoformat(), 0) == 0:
        day -= timedelta(days=1)
    while data.get(day.isoformat(), 0) > 0:
        streak += 1
        day -= timedelta(days=1)
    return streak


def longest_streak(data):
    best = running = 0
    for day_str in sorted(data):
        if data[day_str] > 0:
            running += 1
            best = max(best, running)
        else:
            running = 0
    return best
