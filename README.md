# activity-log

Every day at 23:50 JST, a GitHub Actions workflow runs [`logger.py`](logger.py), which:

1. Fetches my public contribution calendar (the same data behind the green squares on my
   GitHub profile: `github.com/users/{username}/contributions`)
2. Reads today's contribution count off it
3. Appends the result to [`data/activity.json`](data/activity.json) and commits it

No token, no external service — just a public GitHub page and the standard library.
[`contributions.py`](contributions.py) holds the shared parser; [`logger.py`](logger.py) and
[`backfill.py`](backfill.py) both build on it.

---

## 🎯 For hiring managers (30-second read)

**What this is**: a small, self-hosted automation — a daily GitHub Actions job that scrapes my own public contribution calendar and commits the result, so the activity heatmap on [my portfolio](https://yukisatodev.github.io/) shows real data instead of a placeholder.

A few things this is meant to show:

- **I don't ship fake data.** The heatmap used to carry an "illustrative only" disclaimer. Rather than leave it, I built the pipeline needed to back it with real numbers.
- **Failure modes are considered, not just the happy path.** This scrapes an undocumented public HTML endpoint rather than an official API, so it *can* break silently. `logger.py` fails soft — it logs `0` and keeps the workflow green — instead of taking down the automation over a source it doesn't control.
- **Scope is kept deliberately narrow.** Only public contributions are counted, on purpose — a portfolio-facing chart shouldn't leak activity on private client repos, even indirectly.
- **No moving parts beyond what's needed.** No token, no third-party service, just the standard library and a scheduled Action — small enough to read end-to-end in a few minutes.

---

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
