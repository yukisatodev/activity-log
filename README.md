# activity-log

Every day at 23:50 JST, a GitHub Actions workflow runs [`logger.py`](logger.py), which:

1. Fetches my public GitHub events for the day (`/users/{username}/events/public`)
2. Counts how many commits I pushed that day
3. Appends the result to [`data/activity.json`](data/activity.json) and commits it

No manual input, no external service — just the public GitHub API and the standard library.

## Why

Built to replace the "illustrative, not connected to any live account" disclaimer under the
learning-activity heatmap on [my portfolio](https://yukisatodev.github.io/) with real data.

## Notes

- Only counts **public** activity — private repos aren't visible to the unauthenticated public
  events endpoint. That's a deliberate default: a portfolio-facing heatmap should reflect public
  contribution, not expose client work.
- The GitHub events API only retains roughly the last 90 days, so `data/activity.json` is a
  forward-looking log built up one day at a time, not a historical backfill.

## Run locally

```bash
python3 logger.py
```
