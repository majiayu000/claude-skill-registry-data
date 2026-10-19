---
name: growth
description: Use when the user runs /growth. Renders a metis growth dashboard into the Henneth window — DAU/WAU/MAU with week- and month-over-month deltas, a 12-week active/new-users trend chart, and a 30-day daily sparkline — from the GA4 → BigQuery export. Read-only; queries sit within BigQuery's free 1TB/month tier.
purpose: Renders a metis growth dashboard of active users and trends from the GA4/BigQuery export.
user_invocable: true
stage: watch
composes: henneth:dispatch
---

# Growth

A visual growth dashboard for metis, rendered into the Henneth window: is the app
gaining users? Active users, new users, and the trend that answers it.

## Run

    ~/.claude/hooks/appgrowth.py

It queries the metis GA4 → BigQuery export, renders `metis-growth.html` into the
Henneth previews folder, and prints the headline numbers. The standing Henneth
window picks the page up on its own (boot it with `/henneth` if it isn't running).

## What it shows

- **DAU / WAU / MAU** headline cards, each with a week- or month-over-month delta.
- **Weekly trend** — distinct active and new users per week, last 12 weeks, peak marked.
- **Daily sparkline** — active users per day over the last 30 days.

## Account & config

Pinned to the account that owns metis (derived from `firebase login:list`). The
project, dataset, and account are overridable via `GROWTH_PROJECT`,
`GROWTH_DATASET`, and `GROWTH_ACCOUNT` — the seam for adding other apps later.

## Notes

- **Read-only, within free tier.** Queries are bounded by date and capped at a 1 GB
  scan; metis's data is far under BigQuery's free 1 TB/month.
- **GA4 lag.** Daily tables finalize ~2 days late, so the dashboard anchors on the
  last complete day; the most recent day or two may read low until finalized.
- **metis only.** It is the one app with a GA4 → BigQuery export; others would need
  their export linked before they could be added.
