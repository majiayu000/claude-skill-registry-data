---
name: deep-research
description: Multi-source deep research using firecrawl and exa MCPs. Searches the web, synthesizes findings, and delivers cited reports with source attribution. Use when the user wants thorough research on any topic with evidence and citations. Do NOT use for questions about this codebase (read the code), single-fact lookups one search answers, or library/API docs (Context7 first).
origin: ECC
---

# Deep Research

Produce thorough, cited research reports from multiple web sources using firecrawl and exa MCP tools.

## When to use

- User asks to research any topic in depth
- Competitive analysis, technology evaluation, or market sizing
- Due diligence on companies, investors, or technologies
- Any question requiring synthesis from multiple sources
- User says "research", "deep dive", "investigate", or "what's the current state of"

**When NOT to use:**

- Questions about this codebase — read the code (Read/Grep/Glob), never web-search it
- Single-fact lookups a lone search answers — one query, no report scaffolding
- Library/framework/API documentation — Context7 first (`resolve-library-id` → `query-docs`)
- Anything answerable from files the user already provided in the conversation

## Inputs

Required before starting:

1. **A research topic** from the user, plus goal/angle from Step 1 (or an explicit "just research it").
2. **At least one search MCP loaded in this session:**
   - **firecrawl** — `firecrawl_search`, `firecrawl_scrape`, `firecrawl_crawl`
   - **exa** — `web_search_exa`, `web_search_advanced_exa`, `crawling_exa`

   Both together give the best coverage. Configure in `~/.claude.json` or `~/.codex/config.toml`.

**If neither MCP is available: STOP.** Report which tools are missing and how to configure them.
Never fall back to writing a "researched" report from training data — that produces confident
citations for sources never fetched, which is worse than no report (fail-open pattern, bug-230).
Tool availability is a fact of the session's tool listing, not a guess: a tool absent from the
listing is absent.

## Workflow

### Step 1: Understand the Goal

Ask 1-2 quick clarifying questions:
- "What's your goal — learning, making a decision, or writing something?"
- "Any specific angle or depth you want?"

If the user says "just research it" — skip ahead with reasonable defaults.

### Step 2: Plan the Research

Break the topic into 3-5 research sub-questions. Example:
- Topic: "Impact of AI on healthcare"
  - What are the main AI applications in healthcare today?
  - What clinical outcomes have been measured?
  - What are the regulatory challenges?
  - What companies are leading this space?
  - What's the market size and growth trajectory?

### Step 3: Execute Multi-Source Search

For EACH sub-question, search using available MCP tools:

**With firecrawl:**
```
firecrawl_search(query: "<sub-question keywords>", limit: 8)
```

**With exa:**
```
web_search_exa(query: "<sub-question keywords>", numResults: 8)
web_search_advanced_exa(query: "<keywords>", numResults: 5, startPublishedDate: "2025-01-01")
```

**Search strategy:**
- Use 2-3 different keyword variations per sub-question
- Mix general and news-focused queries
- Aim for 15-30 unique sources total
- Prioritize: academic, official, reputable news > blogs > forums

### Step 4: Deep-Read Key Sources

For the most promising URLs, fetch full content:

**With firecrawl:**
```
firecrawl_scrape(url: "<url>")
```

**With exa:**
```
crawling_exa(url: "<url>", tokensNum: 5000)
```

Read 3-5 key sources in full for depth. Do not rely only on search snippets.

### Step 5: Synthesize and Write Report

Structure the report:

```markdown
# [Topic]: Research Report
*Generated: [date] | Sources: [N] | Confidence: [High/Medium/Low]*

## Executive Summary
[3-5 sentence overview of key findings]

## 1. [First Major Theme]
[Findings with inline citations]
- Key point ([Source Name](url))
- Supporting data ([Source Name](url))

## 2. [Second Major Theme]
...

## 3. [Third Major Theme]
...

## Key Takeaways
- [Actionable insight 1]
- [Actionable insight 2]
- [Actionable insight 3]

## Sources
1. [Title](url) — [one-line summary]
2. ...

## Methodology
Searched [N] queries across web and news. Analyzed [M] sources.
Sub-questions investigated: [list]
```

### Step 6: Deliver

- **Short topics**: Post the full report in chat
- **Long reports**: Post the executive summary + key takeaways, save full report to a file

## Parallel Research with Subagents

For broad topics, use Claude Code's Task tool to parallelize:

```
Launch 3 research agents in parallel:
1. Agent 1: Research sub-questions 1-2
2. Agent 2: Research sub-questions 3-4
3. Agent 3: Research sub-question 5 + cross-cutting themes
```

Each agent searches, reads sources, and returns findings. The main session synthesizes into the final report.

## Quality Rules

1. **Every claim needs a source.** No unsourced assertions.
2. **Cross-reference.** If only one source says it, flag it as unverified.
3. **Recency matters.** Prefer sources from the last 12 months.
4. **Acknowledge gaps.** If you couldn't find good info on a sub-question, say so.
5. **No hallucination.** If you don't know, say "insufficient data found."
6. **Separate fact from inference.** Label estimates, projections, and opinions clearly.

## Verification

There is no executable test for whether research *conclusions* are true — that limit is stated
plainly rather than papered over. What CAN fail is the report's citation structure. Run these
against the report file written in Step 6 (substitute its real path for `REPORT`):

```bash
REPORT="<path the report was saved to in Step 6>"
grep -oE 'https?://[^/ )]+' "$REPORT" | sort -u | wc -l   # unique cited hosts
grep -cE '\]\(https?://' "$REPORT"                         # inline markdown-link citations
awk '/^## Sources/,0' "$REPORT" | grep -cE '^[0-9]+\.'     # numbered Sources entries
```

- **PASS (line 1):** ≥ 5 unique hosts. 1–2 hosts is single-source syndrome, not deep research. `[repro]`
- **PASS (line 2):** ≥ 10 inline citations — claims carry their sources in the body, not only in
  the Sources list. `[repro]`
- **PASS (line 3):** ≥ 5 numbered entries under `## Sources`. `[repro]`

Two further checks that can each return "no" but have no grep:

- **Citation provenance:** every URL in the report appeared in a tool result THIS session (a
  search hit or a scrape). A URL with no matching tool result is a hallucinated citation —
  delete the claim it supports, not just the link. `[repro]`
- **Cross-reference floor:** each load-bearing claim traces to ≥ 2 independent sources, or is
  explicitly flagged "single-source, unverified" in the report. Claims labeled as inference
  under Quality Rule 6 are `[inferred]` and never justify a `Confidence: High` header.

## Failure modes

- **Proceeding with no MCP** — neither firecrawl nor exa is loaded and the "report" gets
  synthesized from training data anyway. Fail-open (bug-230): absent input stops the skill,
  never silently degrades it. Symptom: a cited report in a session with zero search tool calls.
- **Hallucinated citations** — a URL in the report that no tool result returned this session.
  The most damaging failure: it looks maximally rigorous while being fabricated. Caught by the
  provenance step in Verification.
- **Snippet-only synthesis** — Step 4 skipped; the report is written from search-result snippets
  alone. Symptoms: no direct quotes, no concrete figures, every section reads like an abstract.
- **Single-source syndrome** — one article's framing repeated as consensus. Quality Rule 2
  requires flagging any claim only one source supports; Verification line 1 catches the extreme
  case.
- **A search that dies is not a search that found nothing** — an MCP error, timeout, or rate
  limit yields zero results as an *artifact*, not a finding. Re-run or switch tools before
  writing "no information found" (same fail-open family as bug-230).
- **Stale answer to a "current state" question** — every cited source predates the last 12
  months. The `startPublishedDate` filter in Step 3 exists for exactly this.

## Examples

```
"Research the current state of nuclear fusion energy"
"Deep dive into Rust vs Go for backend services in 2026"
"Research the best strategies for bootstrapping a SaaS business"
"What's happening with the US housing market right now?"
"Investigate the competitive landscape for AI code editors"
```
