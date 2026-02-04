---
name: linkedin-search
description: Search your LinkedIn posts/shares by topic, find connections by title or company, and get LinkedIn statistics. Use when analyzing your LinkedIn data, finding specific connections, or reviewing past posts and shares.
allowed-tools: Read, Bash(python:*)
---

# LinkedIn Search

Search your LinkedIn data archive to find posts by topic, connections by role/company, and view statistics.

## Setup

1. Download your LinkedIn data export from LinkedIn Settings → Get a copy of your data
2. Copy the ZIP to the watch folder:
   ```bash
   mkdir -p ~/.linkedin-exports
   cp ~/Downloads/Complete_LinkedInDataExport_*.zip ~/.linkedin-exports/
   ```

That's it! Dependencies install automatically on first use.

## Usage

**Search posts/shares:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-search/linkedin_search.py search-shares --query "AI"
```

**Find connections:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-search/linkedin_search.py find-connections --title "founder" --company "microsoft"
```

**Multi-keyword search:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-search/linkedin_search.py search-connections-keywords --keywords founder gtm
```

**Get statistics:**
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-search/linkedin_search.py stats
```

## How it works

- First query: auto-installs deps, extracts ZIP, loads to SQLite, creates indexes
- Subsequent queries: uses cached database (instant)
- New export: auto-detects and reloads when newer ZIP found in `~/.linkedin-exports/`

## Examples

"Did I write about AI?" → `search-shares --query "AI"`
"Find GTM agency founders" → `search-connections-keywords --keywords founder gtm`
"How many posts?" → `stats`
