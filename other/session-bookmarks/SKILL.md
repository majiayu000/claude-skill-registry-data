---
name: session-bookmarks
description: "This skill should be used to save URLs or links found this session as Raindrop bookmarks — triggers: 'bookmark URLs from this session', 'save links we found', 'save notable URLs to Raindrop', 'save session URLs', 'raindrop bookmarks from session'. Scans the current conversation for high-signal URLs discovered during research, previews 1-3 bookmark candidates, and creates them in the AI-bookmarked Raindrop collection after user approval. This is URL/link bookmarking to Raindrop — to capture insights, decisions, or lessons into the Basic Memory knowledge graph instead, use session-reflect."
user-invocable: true
allowed-tools:
  - Read
  - mcp__raindrop__find_collections
  - mcp__raindrop__create_collections
  - mcp__raindrop__find_bookmarks
  - mcp__raindrop__create_bookmarks
  - mcp__raindrop__update_bookmarks
---

# Session Bookmarks

Scan the current conversation for high-signal URLs discovered during work,
suggest 1-3 as Raindrop bookmarks, and create them after user approval.

This skill can be invoked directly or is auto-delegated from `/session-reflect`
after its Basic Memory workflow completes.

## Edge Cases

- **No URLs in conversation** — exit silently, no output.
- **All candidate URLs already bookmarked** — exit silently.
- **Raindrop MCP unavailable** — report "Raindrop unavailable — skipping
  bookmark suggestions" and exit. Do not block the calling skill.
- **`create_bookmarks` succeeds but `update_bookmarks` (tags) fails** —
  report partial success: "Bookmark created but tagging failed — add tags
  manually in Raindrop."
- **User declines all** — report "No bookmarks created" and exit.
- **More than 3 candidates pass the filter** — take the top 3 by priority:
  official docs > specs/RFCs > blog posts/tutorials > other.

## Signal Detection

A URL is bookmark-worthy when **ALL** of these criteria are met:

1. **Discovered during the session** — via Tavily search, DeepWiki, web fetch,
   or Claude's own research. NOT a URL the user pasted as the starting point
   of the conversation. URLs found by *following* a user-pasted link ARE
   eligible (the discovery chain matters, not the seed).

2. **Central to a decision or insight** — the URL's content was actively used
   to inform a decision, solve a problem, or confirm an approach. Not just
   mentioned in passing or returned in a search result that was skipped.

3. **Durable, authoritative content** — official documentation, specifications,
   RFCs, well-written blog posts, research papers, detailed tutorials.

4. **NOT any of these** (always skip):
   - Package registry index pages (npmjs.com/package/X, crates.io/crates/X,
     pypi.org/project/X — these are canonical and already discoverable)
   - GitHub repository root pages (github.com/owner/repo without further path)
   - Localhost or development URLs
   - MCP tool-internal or generated URLs

   **GitHub sub-pages ARE eligible**: issues, discussions, release pages,
   specific file paths, wiki pages, PR threads.

Cap at **3 candidates maximum**.

## Workflow

### Step 1: Extract URL candidates

Scan the conversation for URLs that meet the signal detection criteria above.
Focus on URLs that appeared in tool results (Tavily, DeepWiki, web fetch) and
were subsequently discussed or used.

If no candidates are found:
- **Delegated from `/session-reflect`** — exit silently (no output).
- **Standalone invocation** — report "No bookmark-worthy URLs found in this
  session" and exit.

### Step 2: Deduplicate against Raindrop

For each candidate URL, check if it already exists using a two-pass approach:

**Pass 1 — Exact URL match (primary):**

```
mcp__raindrop__find_bookmarks(url_pattern=["*<url-without-protocol>*"])
```

Strip protocol (`https://`, `http://`) and `#fragment`. Keep `www` if present.
Wrap in leading and trailing `*` wildcards.

Example: `https://fastify.dev/docs/Reply/#send` becomes
`url_pattern=["*fastify.dev/docs/Reply/*"]`.

For `github.com` URLs, include owner/repo in the pattern to avoid matching
thousands of GitHub bookmarks: `["*github.com/fastify/fastify*"]`.

If any result returned, the URL is already bookmarked — skip this candidate.

**Pass 2 — Domain search (fallback, only if Pass 1 returned 0):**

```
mcp__raindrop__find_bookmarks(search="<domain-name>")
```

Search by domain name. Scan results for same content at a different URL
(mirrors, CDN republication). A domain match alone is not a duplicate —
only skip if the content is genuinely the same resource.

If the exact URL exists in ANY Raindrop collection (not just AI-bookmarked),
skip it — do not create a duplicate.

**Collection discovery:** Before the first `create_bookmarks` call, discover
the AI-bookmarked collection:

```
mcp__raindrop__find_collections(search="AI-bookmarked")
```

If the collection does not exist, create it lazily:

```
mcp__raindrop__create_collections(collections=[{title: "AI-bookmarked"}])
```

Cache the collection ID for use in Step 4a.

If all candidates are already bookmarked, exit silently.

### Step 3: Preview

Show surviving candidates grouped in a clear format:

````markdown
## Suggested Bookmarks

1. **Fastify Reply Lifecycle** — https://fastify.dev/docs/latest/Reference/Reply/
   Tags: `ai-bookmarked`, `fastify`, `reply-lifecycle`
   _Resolved the double-send issue — documents execution flow after send()_

2. **RFC 9421: HTTP Message Signatures** — https://www.rfc-editor.org/rfc/rfc9421
   Tags: `ai-bookmarked`, `protocol-design`, `foundational-text`
   _Key reference for the webhook HMAC signing design_

Approve all, or specify numbers (e.g. "1").
````

Each candidate shows:
- **Title** — auto-derived from conversation context or the URL itself
- **URL** — the full URL to bookmark
- **Tags** — always `ai-bookmarked` + 2-4 domain tags
- **Rationale** — one line explaining why this URL mattered in the session

**Tag selection — hybrid approach:**

**Step A — Copy-from-similar** (primary signal): Search for bookmarks
similar to the candidate's topic:

```
mcp__raindrop__find_bookmarks(search="<topic keywords from title>", limit=5)
```

Extract tags from the top 3-5 results. Count tag frequency across results.
Skip results with broken links if visible in response metadata —
deprioritize tags from dead bookmarks.

**Step B — Topic-match boost**: If a tag name appears as a word in the
bookmark's title or topic keywords, boost it regardless of frequency.
This prevents specific tags (e.g., `micropub`) from losing to generic
ones (`code`) that are more common across results.

**Step C — Filter blocklist**: Remove any tag listed in the `blocklist`
frontmatter field of the vocabulary file (`~/.claude/references/raindrop-tags.md`,
managed by `/tag-sync` — see "Integration" below). Support exact matches
(case-insensitive) and prefix wildcards (entries ending in `*`). If the
vocabulary file exists but `blocklist` is absent, skip filtering. If the
vocabulary file is missing entirely, apply a minimal fallback: numeric-only
tags (`1`-`9`) and `imported`.

**Step D — Fallback**: If fewer than 3 similar bookmarks found in Step A,
match topics against the vocabulary file's table characterizations. This
covers novel topics with no exemplars in the library.

**Step E — Selection rules**:
- `ai-bookmarked` is mandatory (always first tag)
- Pick 2-3 additional tags (4 more at most, beyond the mandatory tag)
- Each tag must add DISTINCT information — if A implies B, drop B
- Prefer the MOST SPECIFIC tag: `nodejs` not `javascript`
- Two tags from the same cluster is a smell — prefer cross-cluster

**Step F — Examples**:
BAD:  ai-bookmarked, tools, code, javascript (all generic, same cluster)
GOOD: ai-bookmarked, nodejs, testing (specific ecosystem + concern)
BAD:  ai-bookmarked, mac, osx (redundant Apple tags)
GOOD: ai-bookmarked, osx, cli (platform + what kind of content)

Wait for user response before proceeding.

### Step 4: Create approved bookmarks

For each approved bookmark:

**Step 4a — Create the bookmark:**

```
mcp__raindrop__create_bookmarks(create=[{
  link: "<url>",
  title: "<title>",
  collection_id: <ai-bookmarked-id>,
  note: "<rationale from preview>"
}])
```

**CRITICAL:** Use the AI-bookmarked collection ID discovered in Step 2.
NEVER write to any other collection — the user's organically curated
library must not be contaminated with AI-generated additions.

Multiple approved bookmarks can be batched in a single `create_bookmarks`
call (up to 50 per call).

**Step 4b — Add tags:**

```
mcp__raindrop__update_bookmarks(updates=[{
  bookmark_ids: [<returned-id>],
  update: { add_tags: ["ai-bookmarked", "<tag1>", "<tag2>"] }
}])
```

Always include `ai-bookmarked` in the tag list. Batch up to 100 tag updates
per call.

### Step 5: Report

````markdown
## Bookmarks Created

Added N bookmarks to AI-bookmarked:
- Fastify Reply Lifecycle — <raindrop-url>
- RFC 9421: HTTP Message Signatures — <raindrop-url>

Skipped: [anything the user declined]
````

Use Raindrop URLs (not original URLs) in the report — per the Raindrop MCP
server convention, always link to the Raindrop bookmark page.

## Guidelines

- **Preview before writing** — never create bookmarks without user approval.
- **Be selective** — 1-3 high-quality bookmarks beat a dump of every URL seen.
- **Rationale matters** — the `note` field on each bookmark explains *why* it
  was bookmarked, which helps when reviewing AI-bookmarked items later.
- **Tag consistently** — use the vocabulary file when available. Match existing
  tags rather than inventing new ones.
- **Graceful degradation** — if Raindrop is unavailable or the tag vocabulary
  file is missing, the skill should degrade gracefully, not fail loudly.

## Integration

- **From `/session-reflect`** — session-reflect auto-delegates to this skill
  in its Step 6 (Report) after completing Basic Memory work. The delegation
  is seamless — the user sees bookmark suggestions as a natural continuation.
- **Standalone** — can be invoked directly as `/session-bookmarks` at any
  point during a session.
- **Tag vocabulary** — consumes `~/.claude/references/raindrop-tags.md`
  (managed by `/tag-sync`). Falls back to ad-hoc tags if the file is missing.
