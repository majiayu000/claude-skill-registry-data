---
name: managing-loom
description: |
  Use when working with Loom — loom video management covering video library,
  folders, sharing settings, and engagement analytics. Use when auditing Loom
  video usage, managing recordings, analyzing viewer engagement, or organizing
  video content across a Loom workspace.
connection_type: loom
preload: false
---

# Managing Loom

Loom video library management and engagement analytics via the Loom API.

## Discovery Phase

```bash
#!/bin/bash
LOOM_BASE="https://developer.loom.com/v1"

echo "=== Current User ==="
curl -s -H "Authorization: Bearer $LOOM_TOKEN" \
  -H "Content-Type: application/json" \
  "$LOOM_BASE/me" | jq '{id, email, name, account_id}'

echo ""
echo "=== Recent Videos (top 25) ==="
curl -s -H "Authorization: Bearer $LOOM_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "$LOOM_BASE/videos" \
  -d '{"per_page": 25, "sort_by": "created_at", "sort_order": "desc"}' \
  | jq -r '.videos[] | "\(.id)\t\(.name[0:40])\t\(.created_at[0:10])\t\(.duration | round)s\t\(.view_count) views"' \
  | column -t

echo ""
echo "=== Folders ==="
curl -s -H "Authorization: Bearer $LOOM_TOKEN" \
  -H "Content-Type: application/json" \
  "$LOOM_BASE/folders" \
  | jq -r '.folders[]? | "\(.id)\t\(.name)\t\(.video_count // 0) videos"' | column -t

echo ""
echo "=== Workspace Members ==="
curl -s -H "Authorization: Bearer $LOOM_TOKEN" \
  -H "Content-Type: application/json" \
  "$LOOM_BASE/members?per_page=20" \
  | jq -r '.members[]? | "\(.email)\t\(.role)\t\(.status)"' | column -t
```

## Analysis Phase

```bash
#!/bin/bash
LOOM_BASE="https://developer.loom.com/v1"
VIDEO_ID="${1:?Video ID required}"

echo "=== Video Details ==="
curl -s -H "Authorization: Bearer $LOOM_TOKEN" \
  -H "Content-Type: application/json" \
  "$LOOM_BASE/videos/$VIDEO_ID" \
  | jq '{name, description, created_at, duration, view_count, share_url, privacy, owner_id}'

echo ""
echo "=== Video Analytics ==="
curl -s -H "Authorization: Bearer $LOOM_TOKEN" \
  -H "Content-Type: application/json" \
  "$LOOM_BASE/videos/$VIDEO_ID/analytics" \
  | jq '{total_views, unique_views, avg_percent_watched, total_reactions, total_comments}'

echo ""
echo "=== Video Comments ==="
curl -s -H "Authorization: Bearer $LOOM_TOKEN" \
  -H "Content-Type: application/json" \
  "$LOOM_BASE/videos/$VIDEO_ID/comments" \
  | jq -r '.comments[]? | "\(.created_at[0:10])\t\(.author_name)\t\(.body[0:60])"' | column -t
```

## Output Format

```
LOOM WORKSPACE OVERVIEW
User:           [name] ([email])
Total Videos:   [count]
Total Folders:  [count]

TOP VIDEOS BY VIEWS
Video                    Duration  Views  Avg Watch%
[name]                   [n]s      [n]    [pct]%

ENGAGEMENT SUMMARY
Total Views:       [count]
Avg Watch Rate:    [pct]%
Total Reactions:   [count]
Total Comments:    [count]
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

