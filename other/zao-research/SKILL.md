---
name: zao-research
version: 2.3.0
description: |
  Research skill for the ZAO OS ecosystem. Three-tier workflow (QUICK/STANDARD/DEEP)
  with mandatory community-source coverage. Integrates exa + context7 MCPs,
  Reddit/HN/X searches, staleness detection, parallel-session safety, and action bridges.
  Searches across 30+ bettercallzaal org repos by default. Use when asked to research a
  topic for ZAO OS, COC Concertz, FISHBOWLZ, or ecosystem brands.

  v2.4 (2026-05-24): added bi-directional cowork tracker integration -
  Step 2.6 (pre-write tracker query for in-flight related tasks) +
  Step 9.5 (post-PR fire research-doc tracker task via ~/bin/zao-tracker).
  Tracker = Supabase project etwvzrmlxeobinrlytza, public.tasks table.
  legacy_source prefix = "research-doc:<num>", owner default = Zaal.

  v2.3 (2026-05-20): added Step 4.5 Fetch-Quality Gate + Hard Requirement #11 (Doc 693)
  — every source must be classified FULL/PARTIAL/FAILED and escalated through the real
  fetch ladder (WebFetch → exa web_fetch → Playwright → Wayback) before the doc is
  written. Removed firecrawl references (not installed). Fixes the failure where a
  hard-to-fetch link gets a doc written off metadata or search snippets.

  v2.2 (2026-05-17): added Step 2.5 cross-repo search (Doc 663a) — after local research,
  searches bettercallzaal org repos via mcp__grep__searchGitHub to find implementations,
  patterns, and decisions across 30+ ZAO ecosystem projects (ZAOOS, zaostock, zlank,
  WaveWarZ, COC Concertz, ZOUNZ, etc). Excludes private/archived repos.

  v2.1 (2026-04-29): added Reddit/X scraping fallback chain (Doc 562) — when WebFetch
  blocks reddit.com or x.com, route through `/fetch` skill which calls
  ~/bin/zao-fetch-reddit.sh (curl + Mozilla UA + .json) or ~/bin/zao-fetch-x.sh
  (syndication.twimg.com + nitter + wayback). For multi-source breadth, hand off
  to `last30days-skill`.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - Agent
---

# ZAO OS Research Skill v2

Use this skill when asked to research a topic for any ZAO ecosystem project - ZAO OS, COC Concertz, FISHBOWLZ, BetterCallZaal, or any other brand. The canonical research library lives in one place.

## Research Library Location

**Canonical path:** `/Users/zaalpanthaki/Documents/ZAO OS V1/research/`

This is the single source of truth for all ZAO ecosystem research. All projects read from and write to this library.

## Topic Folders

| Folder | For |
|--------|-----|
| `agents/` | AI agents, OpenClaw, ZOE, frameworks, memory, orchestration |
| `music/` | Player, NFTs, distribution, Arweave, audio, FISHBOWLZ |
| `dev-workflows/` | Skills, Claude Code, testing, autoresearch, git, MCP |
| `infrastructure/` | Next.js, Supabase, streaming, mobile, notifications |
| `governance/` | Respect, ORDAO, Hats, ZOUNZ, fractals, Snapshot |
| `community/` | ZAO guide, onboarding, member profiles, task forces |
| `cross-platform/` | Bluesky, Lens, Nostr, Mastodon, Reddit, X, Twitch |
| `farcaster/` | Protocol, Mini Apps, XMTP, ecosystem, social graph |
| `identity/` | ZIDs, ENS, reputation, knowledge graph |
| `business/` | Revenue, payments, strategy, marketplace |
| `events/` | Bootcamp notes, ship logs, big wins, retros |
| `wavewarz/` | Prediction markets, artist pipeline |
| `security/` | Audits, testing, API verification |

## Three Tiers: Pick Your Depth

| Tier | Time | Sources | Coverage | Use When |
|------|------|---------|----------|----------|
| [QUICK] | 10 min | 1-2 | Official docs only, no web | Sanity check existing knowledge |
| [STANDARD] | 30 min | 5-7 | Docs + 1 Reddit + 1 HN + 1 GitHub + 1 verified URL | Default for most research |
| [DEEP] | 2 hours | 20+ | Full community scan (Reddit threads, HN discussions, X sentiment, blogs, GitHub issues), contradiction checks, staleness audit | Hub topics (10+ dimensions) or critical decision |

**Default:** [STANDARD]. For topics with 10+ dimensions (e.g., strategy, market, architecture), use [DISPATCH] pattern (see Step 4).

## Mandatory Workflow

Follow these steps IN ORDER. Do not skip.

### Step 1: Understand the Request

Parse what the user wants to know. Determine which ZAO ecosystem project (ZAO OS, COC Concertz, FISHBOWLZ, BetterCallZaal). If no tier specified, default to [STANDARD]. Flag if topic looks like a hub (10+ conceptual dimensions) - you may suggest [DISPATCH].

### Step 1.5: Ingest media source (when the input is a podcast / video / audio)

If the research input is a **Spotify episode URL, YouTube URL, Apple Podcasts URL, RSS feed, direct mp3, or a podcast transcript page** (not a topic string), first turn it into a transcript via the shared ingestion engine, then research from that transcript:

```bash
~/bin/zao-ingest.sh "<url>"
# prints the transcript .txt path; also writes <transcript>.meta.json {source,type,title,url}
```

- The transcript becomes a primary source for the doc - cite it `[FULL]` in Sources with the episode title + URL from the `.meta.json` sidecar.
- For Spotify, the engine resolves the DRM episode to its podcast RSS (via the **Podcast Index API** - key in `~/.zao/zao.env`) or a YouTube copy, then transcribes locally. If it can't resolve (Spotify-exclusive original), relay the message and ask for an alternate URL.
- Then continue Step 2 onward as normal, synthesizing the transcript + any web research into the doc. This is how a podcast becomes a research doc. See the `/ingest` skill for the full source matrix.

### Step 2: Search Codebase + Existing Research

Before looking at web research:

```bash
# Check if research already exists (dedup)
grep -ri "<topic_keyword>" "/Users/zaalpanthaki/Documents/ZAO OS V1/research/"*/README.md

# Check codebase for real-world usage
grep -ri "<topic_keyword>" "/Users/zaalpanthaki/Documents/ZAO OS V1/src/"
Glob "**/*<topic_keyword>*" path="/Users/zaalpanthaki/Documents/ZAO OS V1"

# Check config files
read community.config.ts / <project>.config.ts
```

This grounds research in reality. Research docs are aspirational; code is ground truth.

### Step 2.5: Cross-Repo Search (ZAO Ecosystem)

After checking local research + codebase, search across ZAO ecosystem repos (30+ public repositories in bettercallzaal org). Use this step only if topic is cross-repo relevant:

**Cross-repo relevant topics:** Music tech patterns, Snap/Mini App builders, governance bots, Web3 tokenomics, Farcaster integration, automation frameworks, brand consistency.

**Use MCP `mcp__grep__searchGitHub` tool with org scope:**

```bash
mcp__grep__searchGitHub(
  query='<pattern>',
  repo='bettercallzaal/',
  language=['TypeScript', 'TSX', 'JavaScript', 'Python']
)
```

**Rate limits:** 30 requests/min, 60/hour (GitHub API). Budget 2-3 searches per [STANDARD] tier, up to 5 for [DEEP].

**Result handling:**
- **Exact match:** Include repo name + file path. Example: "WaveWarZ player at `wwbase/src/components/SonataPlayer.tsx`."
- **Zero hits:** Document as valuable negative signal. "Pattern not found across 30 ZAO repos; pattern is novel or private."
- **Deduplication:** If pattern appears in 3+ repos, extract as "Standard ZAO pattern" + link representative repo.
- **Hit rate limit:** Stop gracefully. Note "rate-limited after X of Y searches." Resume next day or use fallback: `gh search code "query" --owner=bettercallzaal`.

**Excluded (do NOT search):** Private repos (quad-sandbox, zao-ui, zao-mono, zaoos-workspace, budget2026), archived variants (fractalbotv1old, zaaltimelinev1.1, etc.).

### Step 2.6: Cowork Tracker Pre-Check (NEW v2.4 - 2026-05-24)

Before reserving a doc number, query the ZAO cowork tracker for in-flight tasks on the same topic. Two reasons:

1. **Avoid duplicate work** - if Iman or Zaal has an in-flight task that already covers this research, link to it instead of duplicating.
2. **Surface context** - prior decisions about this topic may have a tracker row with notes / due-date / owner that informs the research.

```bash
~/bin/zao-tracker search "<topic-keyword>" --status todo --limit 5
```

Optional `--source` filter to scope: `--source research-doc` shows prior research-shipped tasks; no filter = all writers (PR test plans, meeting actions, bot adds).

If matches:
- Include the matched tracker rows in the doc's `Also See` section: `- Tracker task <legacy_id> (status, due) - <title>`
- If the match is a research-doc tracker row from a recent shipped doc, the topic may already be covered. Consider [Re-Research Mode](#re-research-mode-updating-an-existing-doc) instead of writing a new doc.

If no matches: continue to Step 3.

This step is non-blocking - if `zao-tracker` is unavailable (env not loaded) or returns no results, proceed normally. The pre-check is best-effort situational awareness, not a gate.

### Step 3: Reserve Doc Number + Branch (Parallel-Session Safe)

Before writing anything. **A claim branch does NOT reserve a number** - on 2026-06-09 two terminals both computed `next=819` off `origin/main` and shipped six colliding pairs (819/824/825/826/827/828), which had to be renumbered after merge. The max-number scan MUST cover in-flight work, not just merged dirs:

```bash
REPO="/Users/zaalpanthaki/Documents/ZAO OS V1"
git -C "$REPO" fetch origin --prune

# 1. Highest MERGED doc number (robust: leading number of NNN-slug dirs, not any digits)
merged=$(find "$REPO/research" -maxdepth 2 -type d -regextype posix-extended -regex '.*/[0-9]+-.*' 2>/dev/null \
  | grep -oE '/[0-9]+-' | grep -oE '[0-9]+' | sort -n | tail -1)

# 2. Highest IN-FLIGHT number on unmerged remote branches (other terminals mid-doc)
inflight_b=$(git -C "$REPO" ls-remote --heads origin 'ws/research-*' 2>/dev/null \
  | grep -oE '[0-9]{3,}' | sort -n | tail -1)

# 3. Highest number sitting in an OPEN PR (claimed, not merged)
# Use the REST endpoint, NOT `gh pr list` — gh pr list/create hit the GraphQL
# bucket (5000 pts/hr, shared with nightly automation + every terminal on the
# bettercallzaal token, and drained fast). REST `gh api .../pulls` uses the
# separate 5000-req/hr core bucket. See research doc 887 rate-limit diagnosis.
inflight_pr=$(gh api 'repos/bettercallzaal/ZAOOS/pulls?state=open&per_page=50' \
  --jq '.[].title' 2>/dev/null | grep -oE 'doc[ #]?[0-9]{3,}' | grep -oE '[0-9]{3,}' | sort -n | tail -1)

# next = max(all three) + 1
next=$(printf '%s\n' "$merged" "$inflight_b" "$inflight_pr" | sort -n | tail -1)
echo "next doc number: $(( next + 1 ))"

git -C "$REPO" checkout -b ws/research-<topic-slug>
mkdir -p "$REPO/research/{topic}/$(( next + 1 ))-{doc-name}"
```

This catches parallel sessions whose docs are branched/PR'd but not yet merged. If you still suspect a race (multiple terminals starting within the same minute), pick `next+2` and leave a gap - a gap is free; a collision costs a renumber. After the renumber incident, see also `feedback_no_synthesis_from_titles` sibling lesson on parallel-session hygiene.

### Step 4: Conduct Research (Tier-Dependent)

#### [QUICK] - 10 minutes, 1-2 sources

1. Check official docs only (context7 if available)
2. 1 GitHub README or official example
3. Zero web search
4. Save + done

#### [STANDARD] - 30 minutes, 5-7 sources

Use **MCP tools in this order:**

1. **context7** — Official library docs (what changed in Next.js? What's new in Supabase RLS?)
2. **exa** — Semantic web search (shows what smart people built, not just Google results)
3. **WebSearch** — Fallback if exa doesn't cover it
4. **Community sources (pick 1 per source type):**
   - **Reddit:** Use WebSearch filtered to reddit.com. Query templates:
     - `"topic" site:reddit.com/r/ClaudeAI` or `site:reddit.com/r/LocalLLaMA` (for tech topics)
     - `"topic" site:reddit.com/r/selfhosted` (infrastructure)
     - `"topic" site:reddit.com/r/Web3` (blockchain)
   - **HackerNews:** Algolia API via WebSearch: `"query" site:news.ycombinator.com dateRange:2025` or search for exact discussion threads
   - **GitHub Discussions:** Check repo official discussions, `gh api repos/OWNER/REPO/discussions`
   - **X/Twitter:** Via exa semantic search, or WebSearch with `site:twitter.com` (Exa covers cross-posts on Substack, Medium, etc.)
5. **Verify URLs:** Check each source URL resolves (no 404s). Use Wayback Machine mentally or note "last checked: [date]".

#### [DEEP] - 2 hours, 20+ sources, full community coverage

1. **All STANDARD sources**
2. **Reddit:** 3-5 threads across relevant subreddits (r/ClaudeAI, r/LocalLLaMA, topical subs). Synthesize comments, flag dissent.
3. **HackerNews:** 3-5 threads, search both recent (last 6 months) and all-time (find historical context). Sort by points; read top 5 comments per thread.
4. **GitHub Discussions:** 2-3 threads from official repos. Synthesize user pain points.
5. **X/Twitter:** Semantic search via exa for sentiment (bullish/bearish on topic). 3-5 threads if relevant.
6. **Blogs + Substack:** exa covers these; fetch 2-3 substantive articles.
7. **Contradiction check:** If sources disagree, flag explicitly. Do NOT synthesize false consensus.
8. **Staleness audit:** Note dates for APIs, pricing, versions. Flag if knowledge is >6 months old.
9. **Verify all URLs:** Wayback Machine check for liveness. Note any dead links.

#### [DISPATCH] - For Hub Topics (10+ Dimensions)

Topics like strategic decisions, market analysis, architectural redesigns often have 10+ independent dimensions (cost, team, timeline, risk, integration points, etc.). Spawn sub-agents:

```
Topic: Architecture Decision for <Feature>
Dimensions: 1) cost, 2) latency, 3) security, 4) team skill, 5) vendor lock-in,
            6) integration with existing stack, 7) testing strategy, 8) monitoring,
            9) vendor roadmap, 10) community adoption

Sub-agents:
  - Agent 1: Cost analysis (pricing tiers, hidden fees, egress costs)
  - Agent 2: Performance (latency benchmarks, throughput under load)
  - Agent 3: Security (audit track record, data residency, compliance)
  - Agent 4: Ecosystem (adoption rate, community size, example implementations)
  - Agent 5: Roadmap (planned features, vendor stability, deprecation risk)

Parent agent: Synthesizes findings into hub README with 5 cross-linked docs.
```

Each sub-agent runs tier=[STANDARD] or [QUICK] research on their dimension. Parent synthesizes into one hub README with "Also see" section linking all sub-docs.

### Re-Research Mode (updating an existing doc)

When the task is to re-research an EXISTING doc (bring a stale or thin doc up to standard) rather than create a new one:

1. **Read the existing doc first.** Note its number, folder, title, and what it already claims.
2. **Reconstruct the `original-query`.** If the doc has no `original-query` field, write one faithfully from the title + Goal + content and suffix it `" (reconstructed)"`. This field is permanent - it lets any future session re-run or extend the research from the same seed. Never drop it.
3. **Re-fetch, do not trust the old text.** Run fresh research (Steps 4 + 4.5) - the old doc's claims may be stale or were written off thin fetches. Climb the fetch ladder for every source.
4. **Preserve the doc number and folder.** Re-research edits the existing `README.md` in place. Never renumber.
5. **Rewrite to the current v2 standard** - full frontmatter (incl `original-query` and a fresh `last-validated`), Key Decisions, Findings, Sources marked FULL/PARTIAL/FAILED, Next Actions.
6. **Note what changed.** If a material fact changed since the last version, say so in Findings ("Updated 2026-05-20: X was Y, now Z").

Large re-research campaigns: dispatch one subagent per batch of ~3-6 docs, each owning whole doc clusters; the parent commits.

### Step 4.5: Fetch-Quality Gate (MANDATORY before writing)

Do NOT write the doc until every source passes this gate. This is the fix for Doc 693 - the failure where a hard-to-fetch link gets a doc written off metadata, search snippets, or a 404.

For each source, classify it:

- **FULL** — the actual content was fetched and read (not the title, not a preview, not a search snippet).
- **PARTIAL** — some content retrieved, some missing (e.g. a tweet's text but not its long-form article body; a Reddit post but not its comment tree).
- **FAILED** — nothing retrieved (404, empty JS shell, tombstone).

**Any PARTIAL or FAILED source MUST be escalated** through the full fetch ladder (WebFetch → exa web_fetch → Playwright / `/browse` → Wayback) before the doc is written. Only after the ladder is genuinely exhausted may a source stay PARTIAL/FAILED — and then it MUST be marked as such in the doc's Sources section (Hard Requirement #11).

Banned: writing the doc from a search snippet because the real page would not load on the first try. The page Zaal sent is the source; a snippet about it is not.

If a high-signal source (long technical post, 500+ upvotes, an actual playbook/spec/wiki) is only PARTIAL after escalation, say so loudly at the top of the doc - do not bury it.

### Step 5: Save with v2 Metadata Frontmatter

**Required structure:**

```markdown
---
topic: [category from Topic Folders, e.g. "infrastructure"]
type: [guide | comparison | decision | audit | market-research | threat-landscape | incident-postmortem]
status: [research-complete | draft | review-pending | superseded]
last-validated: [date, e.g. 2026-04-24]
superseded-by: [doc number if outdated by another doc]
related-docs: [comma-separated doc numbers, e.g. "123, 145, 289"]
original-query: "[the literal research request that spawned this doc, verbatim. For docs re-researched from an older version, a faithful reconstruction - suffix it with ' (reconstructed)'. This field exists so any future session can re-run or extend the research from the same seed.]"
tier: [QUICK | STANDARD | DEEP | DISPATCH]
---

# {Number} — {Title}

> **Goal:** {One-line description}

[... content ...]

## Also See

- [Doc 123](../123-related-topic/)
- [Doc 289](../289-other-angle/)

## Next Actions

| Action | Owner | Type | By When |
|--------|-------|------|---------|
| Update community.config.ts with finding X | @Zaal | PR | After approval |
| Create ZOE task for "monitor vendor deprecation" | @Zaal | Bot task | Next sprint |
| Schedule infrastructure review meeting | @Team | Calendar | 2026-05-01 |

## Sources

- [Source 1 Title](https://...)
- [Source 2 Title](https://...)
```

### Step 6: Detect + Flag Staleness + Hallucinations

Before declaring research complete:

```
Staleness check:
  - APIs, pricing, versions - note "current as of [date]" for each
  - Docs >6 months old? Flag: "Source is X months old; verify with current docs"
  - Contradictions between sources? Flag explicitly: "Source A claims X, Source B claims Y"

Hallucination check:
  - Each URL: Does it resolve? (404? Redirected?) Note "verified: [date]"
  - Citations: Author name + date match the actual page header? Or LLM-invented?
  - Specific claims: Can you trace them back to a direct quote? Or inferred/synthesized?

If any hallucinations suspected, rewrite. Do not publish unverified claims.
```

### Step 7: Add Action Bridge

Every doc ends with "Next Actions" table (see frontmatter template above).

**HARD REQUIREMENT (retrospective 2026-07-03, 5.8:1 research-to-ship ratio):** every Next Actions row MUST have:
- **Exec owner** - a person who will do it (not "team", not blank)
- **A real date** in By When - an absolute date or "wontfix". BANNED values: "When ready", "Next sprint", "Ongoing", "TBD"
- **Shipped-criteria** in the Action text - what observable thing exists when done (PR merged / page live / bot deployed)

A doc whose actions have no owner+date is insight that never ships - do not commit it until the table passes. Link research to:
- **PR:** "Update X config based on finding Y"
- **Todo:** "Investigate Z before next release"
- **ZOE task:** "Set up monitoring for deprecation warning"
- **Calendar:** "Schedule team sync on topic X"
- **Other doc:** "This doc supersedes Doc 234, update links"

Research without action stays archived. Link it forward.

### Step 8: Commit + Push

```bash
git -C "/Users/zaalpanthaki/Documents/ZAO OS V1" add research/{topic}/{number}-{slug}/
git -C "/Users/zaalpanthaki/Documents/ZAO OS V1" commit -m "docs: {topic} research doc {number} (tier:{tier})"
git -C "/Users/zaalpanthaki/Documents/ZAO OS V1" push -u origin ws/research-{topic}
```

### Step 9: Create PR to Main

You (the session) create the PR. Zaal reviews + merges himself.

Use the REST endpoint, NOT `gh pr create`. `gh pr create` hits the GraphQL bucket
(5000 pts/hr, shared across the nightly automation and every terminal on the one
bettercallzaal token — it gets exhausted and blocks PR creation). `gh api .../pulls`
uses the separate, healthy core/REST bucket (5000 req/hr). Proven fix, doc 887.

```bash
BODY=$(cat <<'EOF'
## Summary
[1-3 sentence summary of findings]

## Tier
[QUICK | STANDARD | DEEP | DISPATCH]

## Sources
[Count of unique sources, by type: docs, Reddit, HN, GitHub, blogs, etc.]

## Next Actions
[Link to doc section with action table]
EOF
)
gh api -X POST repos/bettercallzaal/ZAOOS/pulls \
  -f title="doc {number}: {topic} research ({tier} tier)" \
  -f head="ws/research-{topic}" \
  -f base="main" \
  -f body="$BODY" \
  --jq '"PR #\(.number): \(.html_url)"'
```

(Fallback if REST is somehow also limited: open the compare URL
`https://github.com/bettercallzaal/ZAOOS/compare/main...ws/research-{topic}?expand=1`.)

### Step 9.5: Fire research-doc tracker task (NEW v2.4 - 2026-05-24)

After the PR is created, write a tracker row into the ZAO cowork tracker so the research doc shows up in Iman / Zaal's Kanban alongside code tasks:

```bash
~/bin/zao-tracker research <doc-number> "<doc title>"
```

This creates a `todo` task owned by Zaal (default for research kind), due in 3 days, with `legacy_source=research-doc:<num>` and `legacy_id=research-doc-<num>`. Idempotent on legacy_id - re-running the same doc number is a no-op (will fail with a unique constraint; the helper will print the error and exit non-zero, no harm).

Owner override: pass a third arg for non-Zaal review (e.g. `~/bin/zao-tracker research 740 "title" Iman` for an Iman-owned review). Default = Zaal.

Best-effort: if `SUPABASE_SERVICE_KEY` is unset in `~/.zao/zao.env`, the helper exits with a clear error. Skill should NOT abort the run on tracker failure - the doc + PR are already shipped, the tracker task is a nice-to-have for the Kanban surface. Print the error to chat and continue.

Per the standing rule (`feedback_pr_auto_test_task`), the PR itself ALSO gets an `~/bin/zao-tracker pr <prnum> "..."` row separately. The research-doc row and the pr-auto row are different writers with different legacy_source prefixes - both should exist (one tracks "review the research", one tracks "test the PR").

## Hard Requirements (All Must Pass)

| # | Requirement |
|---|---|
| 1 | Recommendations FIRST in Key Decisions table; no preamble |
| 2 | At least 1 file path from relevant project codebase (Step 2 result) |
| 3 | At least 3 specific numbers (versions, prices, dates, counts, benchmarks) |
| 4 | Sources section with 3+ clickable URLs (STANDARD) or 10+ (DEEP) |
| 5 | Comparison table with 3+ options (if decision doc) OR findings table (if guide) |
| 6 | No vague language (see banned phrases below) |
| 7 | [STANDARD]/[DEEP]: At least 1 community source (Reddit, HN, GitHub Discussions, X) |
| 8 | All URLs verified for liveness; note any 404s or paywalled content |
| 9 | Metadata frontmatter with topic/type/status/last-validated/related-docs |
| 10 | Action bridge table ("Next Actions") linking research to concrete todos/PRs/tasks |
| 11 | Sources section marks each source `[FULL]` (content fully read), `[PARTIAL - what is missing]`, or `[FAILED - what was tried]`. No doc ships with an unescalated PARTIAL/FAILED. |
| 12 | Frontmatter carries `original-query` - the verbatim research request, or a faithful reconstruction (suffixed " (reconstructed)") for re-researched docs. Never ship a doc without it. |

### Banned Phrases

| BANNED | USE INSTEAD |
|--------|-------------|
| "consider using" | "USE [X] because [reason]" |
| "it might be worth" | "[X] is worth it because [reason]" |
| "you could explore" | "USE [X]" or "SKIP [X]" |
| "worth investigating" | "INVESTIGATE [X] - [specific question]" |
| "it depends" | State the decision for the specific project context |
| "behind schedule" | State actual date or blockers, e.g. "blocked on Zaal's approval" |

## Context: ZAO Ecosystem Projects

| Project | Stack | Community | Focus |
|---------|-------|-----------|-------|
| ZAO OS | Next.js 16 + Supabase + Neynar | 188 member gated Farcaster music community | Social platform, governance, music, autonomous agents |
| COC Concertz | Next.js 16 + Firebase + Cloudinary | 13+ promoters, virtual concert community | Concert promotion, artist showcasing |
| FISHBOWLZ | Next.js + Privy + Supabase | Audio rooms for music communities | Live audio, discussions [paused Apr 16 for Juke partnership] |
| BetterCallZaal | Static HTML + Farcaster Mini App | Personal brand | Portfolio, consulting, mini app distribution |

## Staleness + Supersession Rules

**Every doc carries `last-validated: <date>`.** This is your SLA. If you ship doc on 2026-04-24, it's valid until 30 days. After 30 days:

- **If still accurate:** Update `last-validated` to today, re-push.
- **If outdated but only slightly:** Add note "Updated 2026-05-24 - [what changed]" and re-validate.
- **If fundamentally wrong or superseded:** Create new doc. Set `superseded-by: <new-doc-number>` in old doc. Update `related-docs` in new doc.

For high-churn topics (pricing, APIs, security), validate every 2-4 weeks.

## Failure Modes + Graceful Degradation

| Failure Mode | Symptom | Recovery |
|---|---|---|
| **Hallucinated URL** (3-13% rate) | Citation resolves to 404 or wrong page | Verify each URL manually. Use Wayback Machine. If dead, note "link rot" and cite next-best source. |
| **Stale Info** (5-18% of content) | API doc is 6 months old; pricing changed | Check `last-validated` date. If >4 weeks old, re-verify. Add timestamp to every external fact: "Current as of 2026-04-24: API v3.2.1 costs $X/month." |
| **JS / bot / paywall wall** | WebFetch returns an empty app shell, "Notion", or thin content | Climb the fetch ladder: exa web_fetch → Playwright MCP → `/browse` skill. Do NOT fall back to WebSearch snippets and write the doc anyway. If a true paywall, note "premium content, not summarized" and use an alternative source. |
| **Rate Limiting** (Reddit, HN Algolia, WebSearch) | Search stops returning results | Stop gracefully. Note "rate-limited" in doc. Suggest manual follow-up. For [DEEP] tier, budget upfront: "max 20 API calls." |
| **Context Collapse** (late-stage hallucination on long research) | Synthesized claims contradict source material | Flag contradictions explicitly: "Source A: X. Source B: Y. Contradiction unresolved; needs manual review." Do not pretend consensus. |
| **Metadata Fabrication** (78.5% of phantom citations) | Title is correct; URL/DOI/author invented | Always extract metadata from page headers, never infer. If page missing metadata, note "metadata unavailable" and use next source. |

## MCP Tool Order (Use in This Sequence)

> firecrawl is NOT installed. Do not reference it. The real tool chain is below (verified 2026-05-20, Doc 693).

**For searching (find the target):**

1. **context7** — Library/framework docs. Zero wait, high signal. Use first for "what's new in X?"
2. **exa web_search** (`mcp__plugin_everything-claude-code_exa__web_search_exa`) — Semantic web search. Use for "what are smart people doing?"
3. **WebSearch** — Fallback if exa search doesn't cover it.
4. **grep.app** — Code search across GitHub. Use for "show me implementations."

**For fetching (read the target) — escalation ladder, climb it until the content is FULL:**

1. **WebFetch** — Plain articles + HTML. First try for any URL.
2. **exa web_fetch** (`mcp__plugin_everything-claude-code_exa__web_fetch_exa`) — JS-rendered pages, clean markdown, batches multiple URLs. This is the firecrawl replacement. Use when WebFetch returns an empty shell or thin content.
3. **Playwright MCP** (`mcp__playwright__*`) or the `/browse` / `/gstack` skills — Full headless browser. Use for Notion wikis, X long-form articles, Spotify, and any login-walled or heavily-JS page that exa cannot render.
4. **Wayback Machine** (`https://web.archive.org/web/<url>`) — For 404s, moved pages, dead links. Always try before giving up on a dead URL.
5. **`~/bin/zao-fetch-reddit.sh`** / **`~/bin/zao-fetch-x.sh`** — Reddit threads / X tweets (see the fallback chain below).

Per-source-type escalation:
- **Notion / JS app shells** → WebFetch returns empty → exa web_fetch → Playwright.
- **X long-form articles** → zao-fetch-x.sh gets the tweet only, NOT the article body → Playwright (logged-out article view).
- **Dead / 404 / moved URLs** → Wayback Machine, then search for the renamed slug.
- **Reddit** → zao-fetch-reddit.sh, then walk the FULL comment tree, not just the top 5.
- **Media (Spotify, YouTube)** → Playwright for the web player, or search the ID for show/episode metadata.

## Reddit / X Scraping Fallback Chain (v2.1, Doc 562 + Doc 564)

When WebFetch returns "unable to fetch from www.reddit.com" or HTTP 402 from `x.com`, do NOT give up. Use this chain:

### Reddit

1. **First try:** `~/bin/zao-fetch-reddit.sh "<url>"` (curl + Mozilla UA + .json suffix). Works for 95%+ of public threads + subreddits.
2. **If 429 rate-limited:** wait 10-15 seconds, retry once.
3. **If still blocked:** invoke the `last30days-skill` skill - it carries full Reddit auth flow plus 10 other sources.
4. **As last resort:** `WebSearch` with `site:reddit.com/r/SUB query`.

### X / Twitter

1. **First try:** `~/bin/zao-fetch-x.sh "<url-or-id>"` — three-tier internal fallback:
   - Tier 1: `cdn.syndication.twimg.com/tweet-result?id=ID&token=4` (works for ~95% of public tweets)
   - Tier 2: `nitter.net/i/status/ID` (HTML scrape; one of few mirrors alive in 2026)
   - Tier 3: `web.archive.org` snapshot
2. **If tombstone (deleted/private):** the script reports it; do NOT retry; surface to user.
3. **For breadth research (multiple X accounts):** invoke the `last30days-skill` which uses a saved browser session token.
4. **As last resort:** `WebSearch` for tweet text fragments to find cached copies.

### Programmatic shortcut

The `/fetch` skill (installed at `~/.claude/skills/fetch/`) auto-routes any URL to the right tool. Prefer it over manual case-handling:

```
# Inside another skill or at the top of /zao-research:
/fetch <url>
```

### When to use `last30days-skill` instead of /fetch

| Use /fetch | Use last30days-skill |
|---|---|
| One specific URL | "What did people say about X in the last 30 days" |
| Reddit thread you know | Subreddit + topic mining |
| One tweet | An account's recent activity + sentiment cluster |
| Single source | Cross-platform synthesis (Reddit + X + YT + HN) |

## Future: Extraction to MCP

When research library is extracted to a shared MCP resource server, agents (ZOE, future ZAO bots) will access docs via:
- `list_resources` - enumerate available docs, filter by topic/type/status
- `read_resource` - fetch a specific doc by number
- Metadata queries - "show me all DEEP-tier docs from 2026-04" or "all docs about Farcaster Protocol"

For now, all access is via this skill using absolute paths.

## Example: How to Invoke

**User says:** "Research what open-source music player libraries would work best for ZAO OS Phase 2. Give me a tier=DEEP analysis of trade-offs."

**v2 Skill flow:**
1. Understand: tier=DEEP, topic=music/player libraries, project=ZAO OS
2. Check codebase: find `/src/providers/AudioPlayer.tsx` + `src/lib/music/`
3. Check existing research: grep for "music player" across research/
4. Reserve doc: [DISPATCH] suggests spawning 5 sub-agents (OSS options, licensing, community, integration, mobile-friendly)
5. Sub-agents each run tier=[STANDARD]: 1) Sonata (MIT), 2) Herocast (AGPL), 3) Nook (MIT), 4) Wavesurfer, 5) Howler.js
6. Parent synthesizes findings into hub README, links all 5 sub-docs
7. Action bridge: "Recommend Sonata for Phase 2.1 -> PR to community.config.ts" + "Setup integration spike -> ZOE task"
8. Commit + PR
9. Zaal reviews, merges

**Result:** Doc 492 (hub) + Docs 492a-492e (sub-docs) with clear recommendations, zero ambiguity.


---

## Lens Mode (merged from /zao-lens, 2026-07-12)

The standalone `/zao-lens` skill is folded into this skill. When the user types
`/zao-lens`, or asks to "look at ZAO OS", "what should ZAO build next", "audit the
lab", "find the non-obvious move", or "what's dead in the repo" - this is LENS MODE,
not standard research. Run the 3-lens breakthrough engine (Builder invents / Skeptic
attacks with ZAO's own boundaries / Synthesizer forges the survivor), grounded in the
real repo - every idea must cite an actual file, research doc, or operating surface.

Full engine (sections 0-N, the ground-in-reality reads, intensity slider, `--drunk`,
`--subsystem <name>`, `--mode build|kill|leverage`, output format) lives in the
sibling file **`lens-mode.md`** in this skill directory. Read it and follow it exactly
when in lens mode. Open every lens run with `ZAO Lens on.`

Lens mode does NOT produce a numbered research doc by default (it is ideation, not
archival research) - only write a doc if the user asks to capture the synthesis.
