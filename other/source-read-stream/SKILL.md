---
name: source-read-stream
description: Market listener source.read_stream for multi-source ingestion
version: 1.0.0
author: PonyBunny
tags: [market-listener, ingestion, source-reading]
phases: [execution]
user-invocable: false
disable-model-invocation: false
---

# Skill — source.read_stream

## Intent
Fetch new items from a configured source using official APIs where possible; otherwise read via Playwright.

## Inputs

```yaml
source_request:
  platform: enum [reddit, github, forum_web]
  source_id: string
  cursor: string|null
  time_window: duration
  max_items: int
```

## Outputs

```yaml
raw_items:
  - platform: string
    source_id: string
    permalink: string
    author: string|null
    created_at: iso8601|null
    raw_text: string
```

## Tools
- reddit.list_new_posts
- reddit.list_new_comments
- github.list_issues
- github.list_issue_comments
- playwright.navigate
- playwright.get_content
- playwright.query_selector_all

## Policy
- Prefer official APIs over scraping.
- Read-only: never post or reply.
- Do not bypass protections or use stealth tooling.
- Return raw text and minimal metadata only.

## Failure Modes
- API/network errors: return error and allow orchestrator backoff.
- Empty results: return empty list with cursor unchanged.
