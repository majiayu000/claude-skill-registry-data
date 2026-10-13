---
name: season-ops
description: "MythiStone season lifecycle and deployment: rollover wipe handshake, season snapshot archive, launch-day gating, Blizzard period quirks, build cadence, artifact-only Pages deploy. Use when touching .github/workflows, season_gate.py, seasonInfo.json/periods.json or the wipe procs."
---

# Season Ops domain

## Gotchas

Before changing a file listed below, read its gotcha: `ref/<id>.md` in this skill (or `kb_gotcha <id>`).

| id | rule | files |
|---|---|---|
| `artifact-only-deploy` | Built pages are never committed; the site deploys straight from the Pages artifact and generated paths are gitignored | `.github/workflows/buildPages.yml`, `.gitignore` |
| `blizzard-preseason-period` | Two Blizzard period quirks shift the dashboard week axes or drop a region from the throughput charts, a phantom period that ends at season start and the KR/TW Thursday reset against the Wednesday-only static fetch | `backend_scripts/fetchSeasonAndPeriodInfo.py`, `backend_scripts/generateDashboardPage.py`, `data/static/periods.json`, `.github/workflows/buildPages.yml` |
| `build-cadence-phases` | buildPages schedules daily/every-3-days/weekly by phase, gated on days since the most recent content update (season start or a .5/.7 patch) | `.github/workflows/buildPages.yml`, `backend_scripts/computeBuildPhase.py` |
| `season-launch-day-presentation` | How the social auto-poster and the Discord bot present the pre-season gap vs the season's first 24h, and why launch day needs its own time-based gate | `backend_scripts/season_gate.py`, `backend_scripts/social_posts/pipeline.py`, `backend_scripts/image_generation/season_countdown.py`, `discord_bot/guards.py`, `discord_bot/errors.py`, `discord_bot/embeds.py` |
| `season-rollover-wipe` | The per-season DB wipe is a handshake between a CI workflow, the collector and a MySQL event, and its invariants are documented at each of those sites | `.github/workflows/seasonRolloverWipe.yml`, `backend_scripts/requestSeasonWipe.py`, `backend_scripts/database.sql`, `backend_scripts/collectLeaderboardData.py`, `data/static/seasonInfo.json`, `docker-compose.yml` |
| `season-snapshot-archive` | Each season's built _site is force-pushed to a season-<id> branch in a separate archive repo as cold storage before the DB wipe | `.github/workflows/buildPages.yml` |
