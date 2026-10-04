---
name: youtube-sync-review-ops
description: Preview, apply, and score YouTube metadata changes from local JSON plans using the Apollo scripts in SCBE-AETHERMOORE. Use when updating YouTube titles, descriptions, or tags; when running a local sync-and-review loop for channel packaging; or when converting review findings into machine-applied metadata changes.
---

# YouTube Sync Review Ops

Use the repo-local Apollo scripts to manage YouTube packaging from the terminal instead of YouTube Studio.

## Core scripts

- `python scripts/apollo/youtube_metadata_sync.py preview --input <plan.json>`
- `python scripts/apollo/youtube_metadata_sync.py apply --input <plan.json>`
- `python scripts/apollo/youtube_sync_and_review.py preview --input <plan.json>`
- `python scripts/apollo/youtube_sync_and_review.py apply --input <plan.json>`
- `python scripts/apollo/video_review.py review-all`

## Default workflow

1. Keep machine-applied plans in `artifacts/apollo/video_reviews/`.
2. Keep human-readable packs next to the plan for review.
3. Run `preview` first.
4. If the preview looks correct, run `apply`.
5. Rerun `review-all` and report the score change.

## Current plan files

- `artifacts/apollo/video_reviews/youtube_description_updates_2026-03-26.json`
- `artifacts/apollo/video_reviews/youtube_title_tag_updates_2026-03-26.json`
- `artifacts/apollo/video_reviews/youtube_description_pack_2026-03-26.md`
- `artifacts/apollo/video_reviews/youtube_title_tag_pack_2026-03-26.md`

## Auth contract

- Load `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET` from `config/connector_oauth/.env.connector.oauth`.
- Reuse cached token data from `config/connector_oauth/.youtube_tokens.json` or `config/connector_oauth/youtube_token.json`.
- If refresh fails, allow the browser OAuth fallback and continue.

## Guardrails

- Preview before apply when titles are changing.
- Do not invent links or claims in descriptions.
- Preserve existing snippet fields by fetching the live snippet before update.
- Use focused tags, not filler tags.
- Treat `video_review.py` as the scoring surface after every applied change.

## Typical requests

- "Update my YouTube descriptions from the local plan and rerun review"
- "Preview title and tag changes for these videos"
- "Push the metadata pack to YouTube and tell me the score delta"
- "Run the local YouTube packaging pipeline"
