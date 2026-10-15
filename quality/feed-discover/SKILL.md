---
name: feed-discover
description: "Find RSS/Atom feed URLs on a web page. Do NOT use to check an existing feed (use feed-validate)."
---

# feed-discover

Performs RSS/Atom autodiscovery from a seed page URL. Returns candidate feed URLs with confidence and discovery method. Used by feed-curator step 2 and reusable by any system expanding its feed catalog.

## Input

```json
{
  "seed_url": "https://www.fldoe.org/academics/standards/",
  "max_candidates": 10,
  "discovery_methods": ["link_tag", "common_paths", "mime_sniff"]
}
```

## Output

```json
{
  "tool": "feed-discover",
  "candidates": [
    {"feed_url": "https://www.fldoe.org/feed.xml", "method": "link_tag", "confidence": 0.95, "title": "FL DOE Updates"},
    {"feed_url": "https://www.fldoe.org/rss/standards.xml", "method": "common_paths", "confidence": 0.6, "title": null}
  ],
  "seed_url": "https://www.fldoe.org/academics/standards/",
  "human_review_required": true
}
```

## Do NOT use this atom for
- Validating existing feeds (use feed-validate)
- Extracting or summarizing feed content
- Crawling beyond the seed page (single-page discovery only)

## Pipeline note
Follows `references/method.md` at the Discovery step (feed autodiscovery). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — discovered feeds must be verified by a human before adding to the catalog.
