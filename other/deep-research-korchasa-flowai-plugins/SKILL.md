---
name: deep-research
description: >-
  Multi-directional deep research with sub-agents, scoring, source verification
  and cited synthesis. Use for comprehensive research, deep analysis, or
  evidence-backed answers. Produces an executive summary plus a markdown report.
model: opus
effort: high
---

# Deep Research Skill

Multi-stage research: plan → sequential search (with per-direction review) → escalate if needed → synthesize.

## Overview

**Architecture:**
1. **Planner** (main agent): decomposes topic into non-overlapping research directions, defines search criteria and acceptance criteria per direction
2. **Worker sub-agents** (sequential, one per direction): search → evaluate sources → fetch full content → save to temp file; after each worker completes, main agent reviews output and decides whether to escalate before launching next worker
3. **Synthesizer** (main agent): reads all temp files, merges findings, writes final report

**Key invariants:**
- Every factual claim in the report carries a `[N]` citation
- FACT (from source) vs SYNTHESIS (agent's analysis) are always labeled separately
- Contradictions between sources are reported, not suppressed
- Single-source facts are marked `[unverified — single source]`
- Gaps (what was searched but not found) are listed explicitly
- **Worker sub-agents MUST NOT spawn further sub-agents** — all spawning is done by the main agent only
- **Max directions: 6** — if topic requires more, group related angles into one direction

---

## Phase 0: Search Method Detection

Before planning, detect the available search/fetch method. Try each in order, stop at first that works.

| Priority | Method | Detection |
|---|---|---|
| 1 | Built-in search tool | Check tool list for `websearch` (OpenCode), `WebSearch` (Claude Code), or IDE-native search equivalent — **search must return URLs from a query, not just fetch a known URL** |
| 2 | `playwright-cli` (headless) | Run `playwright-cli --version` via shell; success = available |
| 3 | Playwright MCP | Check tool list for `browser_navigate` + `browser_snapshot` tools |
| 4 | Other MCP search/fetch tools | Check tool list for any MCP tool that accepts a query string and returns results |

**Output of this phase** — printed in chat BEFORE the plan (one line: `Search method: <name> — <detection evidence>`, e.g. `built-in — WebSearch present in the tool list` or `playwright-cli — playwright-cli --version → 1.4x`), and two variables passed to every worker. The detection is an observable step, not a private conclusion: a run that names the method only inside worker prompts has skipped this phase (observed 2026-09-06, `deep-research-plan`).

- `search_method`: short name, e.g. `built-in`, `playwright-cli`, `playwright-mcp`, `mcp_brave`
- `search_instructions`: a brief how-to for that method (see examples below)

**Instruction examples by method:**

```
# built-in
search_method: built-in
search_instructions: >
  Use the built-in search tool (websearch in OpenCode, WebSearch in Claude Code) to run each query
  and get result URLs. Then use the built-in fetch tool (webfetch / WebFetch) to retrieve full
  page content for each accepted URL.
  Run all queries as parallel tool calls in one message where the IDE supports it.

# playwright-cli
search_method: playwright-cli
search_instructions: >
  Use shell to navigate and extract content:
    playwright-cli open
    playwright-cli goto "https://www.google.com/search?q=<encoded_query>"
    playwright-cli snapshot
  Read the snapshot text to extract result URLs, then for each URL:
    playwright-cli goto "<url>"
    playwright-cli snapshot
  Run queries sequentially (one browser session, sequential navigation).

# playwright-mcp
search_method: playwright-mcp
search_instructions: >
  Use browser_navigate(url) to open a page and browser_snapshot() to extract its content.
  For search, navigate to a search engine with the query in the URL:
  browser_navigate("https://www.google.com/search?q=<encoded_query>")
  browser_snapshot()
  Extract result URLs from the snapshot, then for each URL:
  browser_navigate("<url>")
  browser_snapshot()
  Run queries sequentially.

# other MCP (fill in actual tool name)
search_method: mcp_<toolname>
search_instructions: >
  Use mcp_<toolname>_search(query) to search and mcp_<toolname>_fetch(url) to fetch.
  Run all queries as parallel tool calls in one message if the tool supports it.
```

If no method is available: stop, report to user, do not proceed.

---

## Phase 1: Planning

Decompose the research topic into **3–6 non-overlapping directions**.

For each direction, define:
- `direction`: one-sentence description of what to investigate
- `search_queries`: 3–5 query variations (broad + narrow + negation/criticism)
- `acceptance_criteria`: what makes a source acceptable (see `deep-research-worker.md` for authority scores and recency defaults)
- `output_file`: path like `<tmp_dir>/<slug>.md` (where `<tmp_dir>` is created in this phase)

Create a temporary directory using the system temp facility:
```bash
mktemp -d "${TMPDIR:-/tmp}/deep-research-XXXXXX"
```
Save the returned path as `tmp_dir` — pass it to all workers and use in Phase 4–5.

Output the plan as a markdown list before proceeding — the COMPLETE plan: every direction with its full 3–5 query list, its acceptance criteria (source types + recency) and its output file, in the shape of the example below. Printing the plan is a precondition on spawning the first worker: a chat plan that lists only the direction names, with the queries appearing later inside worker prompts, is not the plan (observed 2026-09-06, `deep-research-plan`: three direction names printed, 15 queries visible only to the workers). Do not ask for approval — proceed automatically.

**Example direction definition:**
```
Direction: Current adoption rates and market data
Queries:
  - "deep learning adoption enterprise 2024 statistics"
  - "AI deployment survey 2024 2025"
  - "machine learning production usage report"
Acceptance: data from surveys, analyst reports, or official sources; published 2022+
Output: <tmp_dir>/adoption-rates.md
```

---

## Phase 2: Sequential Search (Sub-agents)

Launch sub-agents **one at a time**. After each completes, the main agent reviews the output and scores it before launching the next.

**Invoke the `deep-research-worker` subagent** for each direction. Pass as task prompt:

```
direction: {direction}
search_queries:
{search_queries}
acceptance_criteria: {acceptance_criteria}
output_file: {output_file}
search_method: {search_method}
search_instructions: |
  {search_instructions}
```

**After each worker completes**, the main agent reads `{output_file}` and evaluates:

| Check | Pass condition |
|---|---|
| Accepted sources | ≥ 2 sources with authority score ≥ 3 |
| Coverage | At least 1 fact per search query angle |
| Confidence floor | ≥ 1 fact with confidence = high or medium |
| No fabrication | All facts have traceable source URL |

- **All checks pass** → launch next direction's worker.
- **Any check fails** → run Phase 3 escalation for this direction first, then continue.

**Workers are NOT launched simultaneously.** Sequential execution allows the main agent to adjust remaining directions based on what earlier workers found.

---

## Phase 3: Escalation (if needed)

Triggered inline during Phase 2 when the main agent's post-worker review fails any check.

**Direction quality score** — computed by main agent after reading each worker's output:

| Metric | Weight | How to score |
|---|---|---|
| Accepted source count | 30% | 0 sources=0, 1=5, 2=8, 3+=10 |
| Avg authority score of accepted sources | 30% | avg of per-source scores (1–5), scaled ×2 |
| Confidence distribution | 20% | high=10, medium=6, low=2 (use best fact's confidence) |
| Coverage of search angles | 20% | (angles with ≥1 fact) / (total angles) × 10 |

**Weighted total:** sum of (metric score × weight). Max = 10.

**Escalation threshold:** direction score < 6.0

**Escalation procedure:**
1. Generate 3 alternative query formulations (different angle: synonym, negation, domain-specific)
2. Spawn a retry worker with the same prompt template but new queries
3. Re-score after retry
4. If score still < 6.0 after one retry: mark direction as `[insufficient data — score: X.X]` in final report; list all queries attempted

---

## Phase 4: Synthesis

Read all `<tmp_dir>/*.md` files.

Produce the final report using `assets/report_template.md`.

**Synthesis rules:**
- Group findings thematically, not by direction
- Merge overlapping facts; note if sources agree or conflict
- Label explicitly:
  - `**[FACT]**` — directly from source with citation `[N]`
  - `**[SYNTHESIS]**` — agent's analysis or inference (no citation)
- Triangulate: facts with 2+ independent sources → `confidence: high`
- Single-source facts → append `[unverified — single source]`
- Contradictions → include both sides with their sources, note the conflict

**Citation format:** `[N]` inline, full entry in Bibliography section.

---

## Phase 5: Output

1. **Save full report** to `research_<topic-slug>_<YYYYMMDD>.md` in the working directory.
2. **Verify report integrity** before any cleanup:
   - File exists and is non-empty
   - Contains `## Findings`, `## Gaps`, `## Bibliography` sections
   - Bibliography entry count matches `[N]` citation count in body
   - No unfilled template placeholders (strings like `[direction name]`, `[url]`)
   - If any check fails: stop, print error, do NOT delete `<tmp_dir>/`
3. **Print executive summary** in chat (3–5 sentences: what was researched, key findings, confidence level, gaps).
4. **Print report path.**
5. **Delete** `<tmp_dir>/` directory — only after step 2 passes.

**Executive summary format:**
```
Research complete: [topic]
Key findings: [2–3 sentences]
Confidence: [high/medium/low] — based on [N] sources across [M] directions
Gaps: [what was not found, if any]
Full report: [file path]
```

---

## Error Handling

| Situation | Action |
|---|---|
| Sub-agent finds 0 accepted sources | Retry with 3 alternative queries; if still 0 → mark gap |
| Sub-agent fails/crashes | Note in report; continue with remaining directions |
| Contradictory sources on key fact | Report both sides; do NOT pick one silently |
| Topic too broad to decompose | Split into sub-topics; cap at 6 directions total; workers MUST NOT spawn sub-workers |

---

## References

- Report structure and worker output format: `assets/report_template.md`
