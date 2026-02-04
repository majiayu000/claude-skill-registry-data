---
name: fetch-public-notes
description: Extract content from the public notes website at notes.dsebastien.net. Use when fetching MoCs, notes, or any content from the Obsidian Publish site.
allowed-tools: WebFetch, Bash, Read, Grep, Glob
---

# Fetching Content from Public Notes

**Site**: `https://notes.dsebastien.net/` (Obsidian Publish)

## Important: Dynamic Loading

Direct WebFetch on page URLs returns only HTML boilerplate. **Must use Obsidian Publish API**.

## API URL Format

```
https://publish-01.obsidian.md/access/91ab140857992a6480c9352ca75acb70/[URL-encoded-path].md
```

URL encoding: spaces→`%20`, `(`→`%28`, `)`→`%29`

## Common Note Locations

| Folder | Path |
|--------|------|
| Literature notes | `30 Areas/32 Literature notes/32.02 Content/` |
| Expressions | `30 Areas/32 Literature notes/32.04 Expressions/` |
| Quotes | `30 Areas/32 Literature notes/32.05 Quotes/` |
| Permanent notes | `30 Areas/33 Permanent notes/33.02 Content/` |
| MoCs | `30 Areas/34 Maps/34.01 MoCs/` |

## Fetching via API

```
WebFetch:
  url: https://publish-01.obsidian.md/access/91ab140857992a6480c9352ca75acb70/30%20Areas/34%20Maps/34.01%20MoCs/Positivity%20(MoC).md
  prompt: List all the note links/concepts mentioned.
```

## Local Repository (Faster)

**Location**: `/home/dsebastien/notesSeb/`

```bash
# Find note by name
find /home/dsebastien/notesSeb/30\ Areas -type f -name "*Note Name*" 2>/dev/null | grep -v ".smart-env"

# Read directly
Read: /home/dsebastien/notesSeb/30 Areas/33 Permanent notes/33.02 Content/Note Name.md
```

## URL Construction for relatedNotes

For concept cards, convert file path to public URL:

```
File: /home/dsebastien/notesSeb/30 Areas/33 Permanent notes/33.02 Content/Note Name.md
URL:  https://notes.dsebastien.net/30+Areas/33+Permanent+notes/33.02+Content/Note+Name
```

Rules: spaces→`+`, remove `.md`, path starts `30+Areas/...`

## Quick Reference

| Task | Method |
|------|--------|
| Fetch online | WebFetch + `publish-01.obsidian.md` API |
| Read local | Read tool + `/home/dsebastien/notesSeb/` |
| Find note | `find` command in local repo |
| Public URL | Spaces→`+`, remove `.md` |

Site ID (fixed): `91ab140857992a6480c9352ca75acb70`
