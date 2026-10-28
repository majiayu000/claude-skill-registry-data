---
name: matching-podcast-owners-linkedin
description: "Find and verify LinkedIn profile URLs for podcast hosts, owners, and guests using Tavily, Exa, and optional Perplexity fallback with evidence scoring. Use when podcast people need to be matched to LinkedIn without scraping LinkedIn directly."
---

# matching-podcast-owners-linkedin

## Workflow
1. Confirm the campaign niche, source list, or input file.
2. Read `references/setup.md` if the repo is not configured.
3. Use deterministic scripts before manual research.
4. Write descriptive outputs under `data/` or `.tmp/`.
5. Preserve evidence and candidate fields for review.

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

## Guardrails
- Never hardcode API keys.
- Never accept low-confidence LinkedIn matches automatically.
- Do not scrape LinkedIn directly unless the user provides a compliant workflow.
- Keep raw private research reports out of git unless sanitized.
