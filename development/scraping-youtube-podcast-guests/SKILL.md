---
name: scraping-youtube-podcast-guests
description: "Scrape YouTube podcast episodes, build interviewee/guest lists, extract guest names from titles/descriptions/thumbnails, and match guests to LinkedIn. Use for niche podcast guest prospecting, YouTube interview episode lists, or outreach sheets requiring direct episode URLs and LinkedIn profiles."
---

# scraping-youtube-podcast-guests

## Workflow
1. Confirm the campaign niche, source list, or input file.
2. Read `references/setup.md` if the repo is not configured.
3. Prefer `scripts/run_podcast_intelligence_waterfall.py` for an out-of-the-box guest/interviewee sheet.
4. Use `scripts/build_interviewee_linkedin_list.py` when source URLs are already known.
5. Use lower-level scripts only when debugging or when the user needs just one stage.
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
- `scripts/extract_youtube_urls_from_report.py`
- `scripts/build_interviewee_linkedin_list.py`
- `scripts/run_podcast_intelligence_waterfall.py`
- `scripts/enrich_linkedin_via_apify_serp.py`

## References
- `references/research-report-workflows.md` for turning pasted reports into podcast, episode, and LinkedIn enrichment outputs.

## Guardrails
- Never hardcode API keys.
- Never accept low-confidence LinkedIn matches automatically.
- Do not scrape LinkedIn directly unless the user provides a compliant workflow.
- Keep raw private research reports out of git unless sanitized.
