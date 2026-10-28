---
name: discovering-niche-podcasts
description: "Discover niche/industry podcasts, podcast owners, interview episode sources, and guest/interviewee LinkedIn outreach lists using pasted reports, Perplexity, Exa, Tavily, and optional assisted Genspark workflows. Use when a user provides a niche and wants relevant podcasts plus owners and guests enriched for LinkedIn connection."
---

# discovering-niche-podcasts

## Workflow
1. Confirm the campaign niche, source list, or input file.
2. Read `references/setup.md` if the repo is not configured.
3. Prompt for the minimum intake fields: niche, audience/ICP, optional seed terms, geography, must-include terms, and exclusions.
4. Run the Apify SERP waterfall first with `scripts/run_podcast_intelligence_waterfall.py`.
5. Use YouTube/RSS/transcript/OCR fallback scripts only for high-value shows whose guest names remain missing.
6. Match both hosts/owners and interviewees to LinkedIn with evidence fields.
7. Write descriptive outputs under `data/` or `.tmp/`.

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
- `scripts/apify_serp.py`
- `scripts/discover_podcast_interviews_serp.py`
- `scripts/enrich_linkedin_via_apify_serp.py`
- `scripts/run_podcast_intelligence_waterfall.py`

## References
- `references/research-report-workflows.md` for turning pasted reports into podcast, episode, and LinkedIn enrichment outputs.

## Guardrails
- Never hardcode API keys.
- Never accept low-confidence LinkedIn matches automatically.
- Do not scrape LinkedIn directly unless the user provides a compliant workflow.
- Keep raw private research reports out of git unless sanitized.
