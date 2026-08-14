# activity-log

Every day at 23:50 JST, a GitHub Actions workflow runs [`logger.py`](logger.py), which:

1. Fetches my public contribution calendar (the same data behind the green squares on my
   GitHub profile: `github.com/users/{username}/contributions`)
2. Reads today's contribution count off it
3. Appends the result to [`data/activity.json`](data/activity.json) and commits it

No token, no external service — just a public GitHub page and the standard library.
[`contributions.py`](contributions.py) holds the shared parser; [`logger.py`](logger.py) and
[`backfill.py`](backfill.py) both build on it.

## Why

Built to replace the "illustrative, not connected to any live account" disclaimer under the
learning-activity heatmap on [my portfolio](https://yukisatodev.github.io/) with real data.

## Backfilling history

`logger.py` only ever writes *today's* entry, so a fresh repo starts with just one data point.
[`backfill.py`](backfill.py) fills in the rest from the same public contribution calendar:

```bash
python3 backfill.py            # last 12 months (GitHub's default calendar view)
python3 backfill.py --years 5  # last 12 months, plus 4 more years further back
```

Years before the account existed just come back as zeros, which is harmless — safe to pass a
generous `--years` value.

## Notes

- Only counts **public** contributions — a portfolio-facing heatmap should reflect public work,
  not expose private client repos.
- This scrapes a public, undocumented HTML endpoint (the same one that renders profile pages),
  not the official REST/GraphQL API. It could change without notice; `logger.py` fails soft
  (logs `0` and moves on) rather than breaking the workflow.

## Run locally

```bash
python3 logger.py
```
