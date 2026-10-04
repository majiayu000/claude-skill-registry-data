---
name: anysite-mcp-migration
description: Migrate anysite MCP skills, prompts, and agent instructions from v1 (individual tools like search_linkedin_users, get_linkedin_profile) to v2 (universal meta-tools execute, discover, get_page, query_cache, export_data). Automatically rewrites tool references, adds pagination/filtering/export capabilities, and validates migrated output. Use when users need to update existing skills or prompts for the new anysite MCP v2 API, convert old tool calls to execute() format, or adapt workflows to use new v2 features like server-side filtering and data export.
---

# anysite MCP Migration Assistant

Migrate your anysite MCP skills, prompts, and agent instructions from v1 (individual tools) to v2 (universal meta-tools).

## Overview

Anysite MCP v2 replaces 70+ individual tools with 5 universal meta-tools. This skill helps you:
- **Rewrite tool references** from old format (`search_linkedin_users`, `get_linkedin_profile`) to new `execute()` calls
- **Add new v2 capabilities** like pagination, server-side filtering, aggregation, and file export
- **Validate migrated output** to ensure nothing was missed
- **Preserve workflow logic** while updating only the tool interface layer

## When to Use

- User says "migrate my skill to v2", "update for new anysite API", "convert to execute format"
- User pastes a skill or prompt that contains old-style tool names (`search_*`, `get_*`, `find_*`)
- User asks how to use new anysite MCP features (pagination, cache queries, export)

---

## Migration Workflow

### Step 1: Receive Input

Ask the user for one of:
1. **A skill file path** — read the SKILL.md and any files in `references/`
2. **Pasted prompt text** — the raw text of their prompt or instruction
3. **A description** of what the skill does — you'll help build it from scratch using v2 format

### Step 2: Identify Old Tool References

Scan the input for any of these v1 tool name patterns:

| Pattern | Example |
|---------|---------|
| `search_linkedin_*` | `search_linkedin_users`, `search_linkedin_companies`, `search_linkedin_jobs`, `search_linkedin_posts` |
| `get_linkedin_*` | `get_linkedin_profile`, `get_linkedin_company`, `get_linkedin_user_posts` |
| `find_linkedin_*` | `find_linkedin_email`, `find_linkedin_user_email` |
| `google_linkedin_*` | `google_linkedin_search` |
| `search_twitter_*` / `get_twitter_*` | `search_twitter_users`, `get_twitter_user`, `get_twitter_user_tweets` |
| `search_instagram_*` / `get_instagram_*` | `search_instagram_users`, `get_instagram_user`, `get_instagram_post` |
| `search_youtube_*` / `get_youtube_*` | `search_youtube`, `get_youtube_channel`, `get_youtube_video` |
| `search_reddit_*` / `get_reddit_*` | `search_reddit`, `get_reddit_user`, `get_reddit_posts` |
| `search_yc_*` / `get_yc_*` | `search_yc_companies`, `get_yc_company` |
| `search_sec_*` / `get_sec_*` | `search_sec_filings`, `get_sec_document` |
| `scrape_webpage` | `scrape_webpage` |
| `mcp__anysite__*` | Any tool with the MCP prefix — strip prefix and match above |

Also look for references to **Crunchbase** — this source is disabled in v2 and must be removed.

### Step 3: Apply Tool Mapping

Replace each old tool call using this mapping:

#### LinkedIn

| Old tool | New execute() call |
|----------|-------------------|
| `search_linkedin_users(keywords, location, count, ...)` | `execute("linkedin", "search", "search_users", {"keywords": ..., "location": ..., "count": ...})` |
| `get_linkedin_profile(user)` | `execute("linkedin", "user", "get", {"user": ...})` |
| `get_linkedin_company(company)` | `execute("linkedin", "company", "get", {"company": ...})` |
| `search_linkedin_companies(keywords, count)` | `execute("linkedin", "search", "search_companies", {"keywords": ..., "count": ...})` |
| `search_linkedin_jobs(keywords, location, count)` | `execute("linkedin", "job_search", "search_jobs", {"keywords": ..., "count": ...})` |
| `search_linkedin_posts(keywords, count)` | `execute("linkedin", "post", "search_posts", {"keywords": ..., "count": ...})` |
| `get_linkedin_user_posts(user)` | `execute("linkedin", "post", "get_user_posts", {"user": ...})` |
| `find_linkedin_email(user)` | `execute("linkedin", "email", "find", {"user": ...})` |
| `google_linkedin_search(query, count)` | `execute("linkedin", "google", "search", {"query": ..., "count": ...})` |

#### Twitter/X

| Old tool | New execute() call |
|----------|-------------------|
| `search_twitter_users(query)` | `execute("twitter", "search", "search_users", {"query": ...})` |
| `get_twitter_user(username)` | `execute("twitter", "user", "get", {"username": ...})` |
| `get_twitter_user_tweets(username)` | `execute("twitter", "user_tweets", "get", {"username": ...})` |

#### Instagram

| Old tool | New execute() call |
|----------|-------------------|
| `search_instagram_users(query)` | `execute("instagram", "search", "search_users", {"query": ...})` |
| `get_instagram_user(username)` | `execute("instagram", "user", "get", {"username": ...})` |
| `get_instagram_post(url)` | `execute("instagram", "post", "get", {"url": ...})` |

#### YouTube

| Old tool | New execute() call |
|----------|-------------------|
| `search_youtube(query, count)` | `execute("youtube", "search", "search_videos", {"query": ..., "count": ...})` |
| `get_youtube_channel(channel_id)` | `execute("youtube", "channel", "get", {"channel_id": ...})` |
| `get_youtube_video(video_id)` | `execute("youtube", "video", "get", {"video_id": ...})` |

#### Reddit

| Old tool | New execute() call |
|----------|-------------------|
| `search_reddit(query)` | `execute("reddit", "search", "search", {"query": ...})` |
| `get_reddit_user(username)` | `execute("reddit", "user", "get", {"username": ...})` |
| `get_reddit_posts(subreddit)` | `execute("reddit", "posts", "get", {"subreddit": ...})` |

#### YC / SEC / Web

| Old tool | New execute() call |
|----------|-------------------|
| `search_yc_companies(query)` | `execute("yc", "search", "search", {"query": ...})` |
| `get_yc_company(slug)` | `execute("yc", "company", "get", {"slug": ...})` |
| `search_sec_filings(query)` | `execute("sec", "search", "search", {"query": ...})` |
| `get_sec_document(url)` | `execute("sec", "document", "get", {"url": ...})` |
| `scrape_webpage(url)` | `execute("webparser", "parse", "parse", {"url": ...})` |

### Step 4: Handle Unknown Endpoints

If the input references a tool name **not in the mapping above**:

1. Try to infer the source and category from the tool name (e.g., `get_instagram_user_friendships` → source `"instagram"`, category `"user"` or `"friendship"`)
2. **IMPORTANT: Actually call `discover()` yourself right now** — do NOT leave placeholder `{endpoint}` in the migrated output. Run `discover("{source}", "{category}")` via the MCP tool to get the real endpoint names and parameter schemas.
3. If the first category guess returns "Category not found", try alternative categories (e.g., if `"friendship"` fails, try `"user"` — the endpoint may be nested under a different category)
4. Once you get the real endpoint list from `discover()`, use the exact endpoint name and params in the migrated `execute()` call

**Example — resolving an unknown tool:**
```
Old tool: get_instagram_user_friendships(user, type, count)
→ Not in mapping table
→ You call: discover("instagram", "friendship") → error "Category not found"
→ You call: discover("instagram", "user") → returns endpoints including "user_friendships"
→ Migrated: execute("instagram", "user", "user_friendships", {"user": "...", "count": 100, "type": "followers"})
```

**Rules:**
- NEVER leave `discover()` as a placeholder instruction in the final migrated skill. The migrated output must contain exact `execute()` calls with real endpoint names and params.
- Only include `discover()` in the migrated skill text if the skill's workflow genuinely needs runtime discovery (e.g., the skill works with user-specified sources where the endpoint can't be known at migration time).
- If the mapping above covers the tool, use `execute()` directly — no discover needed.
- Run discover for ALL sources and categories used by the skill to verify that endpoint names and params in the mapping table are still accurate.

### Step 5: Add v2 Capabilities

Review the migrated skill for opportunities to add new v2 features:

#### Pagination
When the workflow processes large result sets or needs "more results":
```
Results from execute() include cache_key. If more data exists, use:
get_page(cache_key="{cache_key}", offset=10, limit=10)
```

#### Server-side Filtering
When the workflow filters results after fetching (e.g., "only show people in SF"):
```
After execute(), filter without consuming context tokens:
query_cache(cache_key="{cache_key}", conditions=[{"field": "location", "op": "contains", "value": "San Francisco"}])
```

#### Aggregation
When the workflow computes statistics or groups data:
```
query_cache(cache_key="{cache_key}", aggregate={"field": "followers", "op": "avg"}, group_by="industry")
```

#### Export to File
When the workflow outputs structured data (CSV, JSON) or the user needs downloadable results:
```
export_data(cache_key="{cache_key}", output_format="csv")
→ returns download URL
```

### Step 6: Update Error Handling

Replace old-style error handling:

**Before:**
```
If search_linkedin_users returns an error, try with different keywords.
```

**After:**
```
If execute() returns an error with "llm_hint", follow the hint.
If execute() returns {"error": "Source not found", "available_sources": [...]}, check source name.
If execute() returns {"error": "Endpoint not found", "available_endpoints": [...]}, call discover() to find correct endpoint names.
```

### Step 7: Remove Disabled Sources

Remove any references to **Crunchbase** — this source is disabled in v2. If the skill relies on Crunchbase data, suggest alternatives:
- Company data → LinkedIn company profiles or Y Combinator
- Funding data → SEC filings or web scraping of funding databases
- Startup research → Y Combinator database

### Step 8: Validate

Run through this checklist on the migrated output:

- [ ] No remaining `search_linkedin_*`, `get_linkedin_*`, `find_linkedin_*` references
- [ ] No remaining `search_twitter_*`, `get_twitter_*` references
- [ ] No remaining `search_instagram_*`, `get_instagram_*` references
- [ ] No remaining `search_youtube_*`, `get_youtube_*` references
- [ ] No remaining `search_reddit_*`, `get_reddit_*` references
- [ ] No remaining `search_yc_*`, `get_yc_*` references
- [ ] No remaining `search_sec_*`, `get_sec_*` references
- [ ] No remaining `scrape_webpage` references
- [ ] No remaining `mcp__anysite__` prefixed tool names (old MCP format)
- [ ] No Crunchbase references
- [ ] `discover()` added only where endpoint/params are genuinely unknown
- [ ] `get_page` / `query_cache` / `export_data` added where beneficial
- [ ] Error handling updated to v2 format
- [ ] Original workflow logic preserved — same steps, same data flow

### Step 9: Output

Present the migrated skill in the same format as the input:
- If the input was a SKILL.md file → output the full migrated SKILL.md
- If the input was a prompt → output the migrated prompt text
- If the input was pasted text → output the migrated version

Always show a **migration summary** after the output:

```
## Migration Summary
- Tool calls replaced: N
- discover() calls added: N
- New v2 features added: [list]
- Crunchbase references removed: N
- Warnings: [any issues found]
```

---

## Examples

### Example 1: Simple Tool Replacement

**Input:**
```
Use search_linkedin_users to find CTOs in Berlin, then get_linkedin_profile for each result.
```

**Output:**
```
Use execute("linkedin", "search", "search_users", {"title": "CTO", "location": "Berlin", "count": 10}) to find CTOs in Berlin, then execute("linkedin", "user", "get", {"user": "{alias}"}) for each result.
```

### Example 2: Multi-Step Workflow

**Input:**
```
1. Use search_linkedin_users to find the person
2. Use get_linkedin_profile to get their full profile
3. Use find_linkedin_email to get their email
4. Use get_twitter_user to check their Twitter
```

**Output:**
```
1. Use execute("linkedin", "search", "search_users", {"first_name": ..., "last_name": ..., "count": 5}) to find the person
2. Use execute("linkedin", "user", "get", {"user": "{alias from step 1}"}) to get their full profile
3. Use execute("linkedin", "email", "find", {"user": "{alias from step 1}"}) to get their email
4. Use execute("twitter", "user", "get", {"username": "..."}) to check their Twitter
```

### Example 3: Adding v2 Features

**Input:**
```
Search for 50 marketing managers and filter by location.
```

**Output:**
```
1. Use execute("linkedin", "search", "search_users", {"title": "Marketing Manager", "count": 50}) to search
2. If more results exist, use get_page(cache_key="{cache_key}", offset=10, limit=10) to load additional pages
3. Use query_cache(cache_key="{cache_key}", conditions=[{"field": "location", "op": "contains", "value": "..."}]) to filter by location server-side
4. Use export_data(cache_key="{cache_key}", output_format="csv") to download the filtered list
```

---

## Quick Reference: v2 Meta-Tools

| Tool | Purpose | When to use |
|------|---------|-------------|
| `discover(source, category)` | Learn available endpoints and params | Before execute() when endpoint name or params are unknown |
| `execute(source, category, endpoint, params)` | Fetch data from any source | Every data retrieval — replaces all v1 tools |
| `get_page(cache_key, offset, limit)` | Load more items from previous execute() | When execute() returned next_offset |
| `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` | Filter/sort/aggregate cached data | When you need to slice results without re-fetching |
| `export_data(cache_key, format)` | Save dataset as downloadable file | When user needs CSV/JSON/JSONL export |
