---
name: feed-validate
description: "Check one RSS/Atom feed URL for liveness, staleness, redirects, and labels. Do NOT use to find new feeds (use feed-discover)."
---

# feed-validate

Validates a single feed URL and returns its health status (live, dead, stale, redirect). Used by feed-curator to check each feed individually and by any system maintaining a feed catalog.

## Input

```json
{
  "feed_url": "https://www.fldoe.org/feed.xml",
  "label": {"category": "standards", "authority": "primary"},
  "last_check_date": "2026-06-15",
  "check_types": ["liveness", "staleness", "redirect"]
}
```

## Output

```json
{
  "tool": "feed-validate",
  "status": "live",
  "http_code": 200,
  "reason": "Feed updated 2 hours ago; last 5 entries recent",
  "redirect_target": null,
  "last_entry_date": "2026-06-27T10:30:00Z",
  "confidence": "high",
  "label_issues": [],
  "human_review_required": true
}
```

## Do NOT use this atom for
- Feed discovery from a seed page (use feed-discover)
- Content extraction or summarization from feeds
- Bulk feed validation (call this atom once per feed URL)

## Pipeline note
Follows `references/method.md` at the Validation step (feed health check). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — feed health is advisory; dead feeds may be temporarily unreachable.
