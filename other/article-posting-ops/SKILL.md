---
name: article-posting-ops
description: Create, validate, and publish SCBE articles across social/blog platforms with API-first posting and Playwright browser fallback. Use when the user asks to write articles, post online, run headless browser posting, or move content toward revenue with lead capture.
---

# Article Posting Ops

## Runbook
1. Use existing platform-ready markdown in `content/articles/` when available.
2. Run API-first publisher:
- `python scripts/publish/post_all.py --dry-run`
- `python scripts/publish/post_all.py`
3. If API credentials are missing, run browser fallback:
- `python scripts/publish/post_all.py --browser-fallback --only twitter`
- `python scripts/publish/post_all.py --browser-fallback --browser-publish --only linkedin`
4. If browser flow reports auth required, bootstrap a persistent login profile:
- `python scripts/publish/post_via_browser.py --platform x --user-data-dir .playwright-profile --bootstrap-login --bootstrap-seconds 180 --headed`
5. Re-run publish with the same profile:
- `python scripts/publish/post_via_browser.py --platform x --user-data-dir .playwright-profile --publish`

## Required Outputs
- Save posting evidence under `artifacts/publish_browser/`.
- Keep per-platform status in terminal summary from `post_all.py`.
- For revenue direction, produce a lead list and a one-message outreach draft per lead.

## Guardrails
- Do not claim a post succeeded without URL or artifact evidence.
- Do not include secrets in logs.
- Keep claims about patents and performance factual and traceable to repo docs.
