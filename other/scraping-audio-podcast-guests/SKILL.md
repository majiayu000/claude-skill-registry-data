---
name: scraping-audio-podcast-guests
description: "Scrape Spotify, Apple, and RSS-only podcast episodes in two stages, build interviewee/guest lists, enrich guests to LinkedIn, and use transcript extraction when titles imply guests but omit names. Use for audio podcasts without useful YouTube channels or niche podcast guest prospecting from RSS/audio episodes."
---

# scraping-audio-podcast-guests

## Workflow
1. Confirm the campaign niche, source list, or input file.
2. Read `references/setup.md` if the repo is not configured.
3. Prefer the Apify SERP waterfall for discovery; it can find Apple/Spotify/RSS-only episode pages before transcript spending.
4. Run title-first extraction with `scripts/build_interviewee_linkedin_list.py` or `scripts/scrape_audio_podcast_guests.py`.
5. Use transcript extraction only for important shows where titles/descriptions omit guest names.
6. Write descriptive outputs under `data/` or `.tmp/`.
7. Preserve evidence and candidate fields for review.

## Scripts
- `scripts/discover_podcasts.py`
- `scripts/ingest_research_report.py`
- `scripts/match_linkedin_profiles.py`
- `scripts/resolve_youtube_channels.py`
- `scripts/scrape_youtube_podcast_guests.py`
- `scripts/scrape_audio_podcast_guests.py`
- `scripts/transcribe_audio_episodes.py`
- `scripts/ocr_thumbnails.py`
- `scripts/genspark_assisted.py`
- `scripts/build_interviewee_linkedin_list.py`
- `scripts/run_podcast_intelligence_waterfall.py`

## Guardrails
- Never hardcode API keys.
- Never accept low-confidence LinkedIn matches automatically.
- Do not scrape LinkedIn directly unless the user provides a compliant workflow.
- Keep raw private research reports out of git unless sanitized.
