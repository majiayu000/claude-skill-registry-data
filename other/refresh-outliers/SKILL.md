---
name: refresh-outliers
description: Refresh the outlier-tracking dashboards (niche and general, long and short form) and validate the data. Use when the user wants fresh outliers, a dashboard update, or new swipe-file material.
---

# Refresh outlier data

These run weekly on GitHub Actions on Sundays: the niche tracker at 6AM Central, then general curation at 7AM. **Don't run them locally unless the data is stale or the user asks now**, because a local run burns YouTube API quota.

## Steps
1. **Check freshness first:** `git fetch` and look at `git log origin/main -1 -- outlier-tracking/<tab>/data.json`. If the scheduled run already covered it, just `git pull`.
2. **To run it now:** `python outlier-tracking/trigger_workflow.py` triggers the **niche** tracker on Actions (preferred, since secrets live there). There's no trigger script for general curation yet. It would be the same dispatch call against `general_outlier_curation.yml`, so add a `--workflow` flag to `trigger_workflow.py` the first time it's needed. Only use a local run (`youtube_outliers.py` / `curate_general_with_claude.py --tab long-form|short-form`) if Actions is down.
3. **Validate:** `python qa/run_checks.py outlier-tracking/*/data.json`. The `outlier-data` gate covers structure, duplicates and the general tabs' 500K/90-day bar.
4. **Check the Actions result** through the GitHub API (`gh` isn't installed): `curl -s https://api.github.com/repos/thorokafor1-dot/sparked_ai/actions/workflows/<file>.yml/runs?per_page=3`.
5. **Hook research** only needs re-pulling if new high-scoring entries appeared in a content type (`long-form-hook-research/<type>/pull_hook_transcripts.py`).

## Gotchas (keep this list updated)
- **General curation** first runs 2026-09-27. Until then, `general-short-form` holds 58 stale entries, and that run should prune them. Verify with step 3.
- **Date formats differ:** niche tabs use "Mar 28, 2026" and general tabs use ISO dates.
- **`LOOKBACK_DAYS=200` in `common.py` is shared by In-Person and Video Chat search and silently excludes real outliers.** Found 2026-09-26: known strong Video Chat creators (Jameer, Jay Throck, ItsMP3) were missing entirely because their best videos are 268-1336 days old, so they never enter the `publishedAfter`-filtered search. Same root cause as the earlier nightgame gap (see `feedback_wider_lookback_for_thin_niches` memory). Fix used: a one-off supplemental scan with `EXTENDED_LOOKBACK_DAYS=1095` (~3 years) for the affected keyword set, merged into the existing data.json rather than overwriting, then per-channel-capped as normal. Don't raise the shared `LOOKBACK_DAYS` itself, that would balloon quota cost on every regular weekly run; do this per-format supplemental scan instead when a user flags a specific missing creator/niche.
- **Raw search results need a manual relevance pass even after `is_relevant_tags` and the outlier check.** The Video Chat supplemental scan pulled in ~13 false positives despite passing every automated filter: app-review listicles ("Top 3 Free Video Call Apps"), a scripted Dhar Mann skit, a sales-pitch video, a reversed-gender-mismatch video. Spot-check titles by eye before publishing a supplemental scan's results, the automated filters catch the obvious junk but not genre-adjacent noise.
- **Explainer Video likely has the same LOOKBACK_DAYS=200 gap as Video Chat did, unverified as of 2026-09-27.** `common.search_videos()` applies `LOOKBACK_DAYS` globally across In-Person/Video Chat/Explainer, so a strong-but-older explainer creator would be silently excluded the same way Jameer/Jay Throck were. Couldn't test, YouTube quota was exhausted (Sunday's scheduled runs used it before this was even tried). Next time quota's available: run the same extended-lookback (~1095 days) supplemental scan pattern against `EXPLAINER_KEYWORDS` and check for missing known explainer creators.
- **Added `common.is_vertical_format()` 2026-09-27** to flag long-form videos shot in vertical/portrait orientation (phone selfie-cam style, e.g. Steph Speaks), matching the user's own footage. Wired into both niche (`youtube_outliers.py`) and general (`curate_general_with_claude.py`) pipelines as a `"vertical"` field on each row; dashboard has a "Vertical Format Only" toggle on the Niche Long Form and General Long Form tabs. Existing rows default to `false`/missing until the next scan re-populates them, this can't be backfilled without re-fetching each video's thumbnail dimensions (a `videos.list` call per row), so it'll fill in gradually as rows get refreshed rather than all at once.
