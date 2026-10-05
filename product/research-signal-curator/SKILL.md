---
name: research-signal-curator
description: >-
  Curate time-sensitive research signals for PaperTrace, including papers,
  model launches or retirements, tools, Skills, MCP servers, labs, events, and
  public community discussion. Use when adding or ranking Radar, Briefing,
  Frontier, Events, Models, Tools, or Sources content; do not use for evergreen
  paper deep-dives.
---

# Research Signal Curator

Turn a noisy stream into a small, timely, auditable action queue.

## Source ladder

Use social posts, LINUX DO, Hacker News, newsletters, blogs, and media to discover a lead. Verify the publishable claim against the strongest available source:

1. paper, official announcement, documentation, repository, dataset, benchmark, organizer page, or status API;
2. structured indexes such as arXiv, Hugging Face, OpenAlex, or a field-specific database;
3. public community and social discussion for attention and practitioner pain only.

Record a public URL and verification timestamp. Do not scrape private sessions, auto-post to communities, or infer unavailable engagement.

## Separate the signals

- **Impact:** evidence strength, technical consequence, downstream work, credible adoption, or citations.
- **Buzz:** recent, platform-local public attention. Never merge unlike metrics or treat them as scientific impact.
- **Utility:** runnable code, data, model, API, demo, setup cost, and fit to a real task.
- **Attention:** skim, read, or deep dive based on the next decision the reader can make.

Scores are editorial heuristics. Explain them and keep vendor benchmarks labeled. A registry upload is not automatically a launch; a service incident is not a model retirement.

## Inclusion test

Publish only when the item answers all of these:

- What changed, on what date, and on which product/research surface?
- Who should care, and what action can they take before the signal goes stale?
- What primary evidence supports the smallest factual claim?
- What remains uncertain, promotional, preliminary, or unreviewed?
- Does it improve field balance, or is it another duplicate AI story?

For events and roles, require a future action boundary and official URL. For medical or safety-critical content, use discovery language and do not turn preliminary research into advice.

## Failure behavior

Keep source failures visible. Preserve a last-known-good record only when it is clearly labeled stale. Do not silently replace missing data with fabricated counts or remove a previously useful source without explaining the failure.

After editing ingestion or editorial data, run the relevant sync/check command and `npm run build`. Update `docs/PRODUCT_ROADMAP.md` when a product capability materially changes.
