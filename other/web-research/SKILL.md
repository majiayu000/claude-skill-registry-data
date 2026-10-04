---
name: web-research
version: 1.0.0
description: '[Research] Use when a workflow step or the user asks for web research. Gathers and triages candidate sources; `--chain=deep-dive` also deep-dives them into an evidence base.'
---

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Run broad web research, classify and deduplicate candidate sources, and produce a tiered source map + gap list for `source-deep-dive`, never a final report.

**Summary:**

- **Purpose:** Breadth-first discovery + triage for `source-deep-dive`; produce a tiered, deduplicated source map, never synthesis.
- **Main steps (all 5, in order):** (1) Define scope — parse topic; generate 5-10 angle-varied queries (overview, current-state, comparison, data, expert, criticism); (2) Execute searches — run `WebSearch` per query (≤10 calls); record title/URL/snippet/source type; (3) Triage — classify each result Tier 1-4; dedupe; (4) Build map — write `tmp/research/_sources-{slug}.md` (Sources + Gaps Identified); (5) Identify gaps — note underexplored angles for `source-deep-dive`.
- Hard-cap fan-out at 10 `WebSearch` calls/invocation; generate 5-10 varied queries, then stop; breadth then triage, not deep-dive.
- Tier every result (.gov/.edu/official > industry reports > established blogs/Wikipedia > forums/social); dedupe URL/syndicated content before counting.
- Deliverable: intermediate source map at `tmp/research/_sources-{slug}.md` (Sources + Gaps Identified), not synthesis; hand off to `source-deep-dive`.
- Mine gaps: missing perspectives, quantitative data, stale recency; guide the next deep dive.
- **Chain mode (caller-passed `--chain=deep-dive`):** after Step 5, read `references/research-chain.md` and run `source-deep-dive` Steps 1-5 inline, leaving `tmp/research/_evidence-{slug}.md`; without the flag stop at Step 5 exactly as above.

**Workflow:**

1. **Define scope** — Parse topic; generate 5-10 varied queries
2. **Execute searches** — Run `WebSearch`; collect results
3. **Source triage** — Classify each source Tier 1-4; dedupe
4. **Build source map** — Write structured source list to working file
5. **Identify gaps** — Note underexplored angles for `source-deep-dive`

**Key Rules:**

- Maximum 10 WebSearch calls per invocation
- Follow source hierarchy: Official docs (Tier 1) > Peer-reviewed (Tier 2) > Industry blogs (Tier 3) > Forums (Tier 4)
- Output intermediate source map, not final report

**MUST ATTENTION** Apply skeptical, sequential thinking; trace every claim and state confidence (>80% to act).

# Web Research

## Knowledge Work Rules (canonical for the research chain)

> **Web Research Protocol** — Factual claims require 2+ independent sources. Rank sources Tier 1 (.gov/.edu/official) > Tier 2 (industry reports) > Tier 3 (credible blogs; cross-validate) > Tier 4 (unverified; NEVER cite as fact). Declare confidence (95/80/60/<60%) for every finding.

1. Follow source hierarchy (official docs > peer-reviewed > industry blogs > forums) for factual claims
2. Cite sources with Tier classification (inline `[N]`)
3. Cross-validate claims with 2+ independent sources
4. Declare confidence: 95/80/60/<60%
5. Use enforced template; include all sections
6. Working files → `tmp/research/` (project-root, disposable); final output → `docs/knowledge/`
7. **Query budget — one rule for the chain:** 5-10 angle-varied `WebSearch` queries, at most 10 calls here; `source-deep-dive` then fetches at most 8 sources. `workflow-research` may lower the depth for a Narrow question (3-5 queries) but never raises a cap. The generic `web-research` protocol guide below (3-5 queries) is the floor for ad-hoc lookups in other skills and never overrides these caps.

These rules are canonical for the research chain; `source-deep-dive` and `knowledge-synthesis` read them from this file.

## Step 1: Define Search Scope

Parse topic; generate 5-10 queries:

- **Definition/overview** — "what is {topic}"
- **Current state** — "{topic} 2026" or "{topic} latest"
- **Comparison** — "{topic} vs alternatives"
- **Data/statistics** — "{topic} market size" or "{topic} statistics"
- **Expert opinion** — "{topic} expert analysis" or "{topic} review"
- **Criticism/risks** — "{topic} challenges" or "{topic} risks"

## Step 2: Execute Searches

For each query:

1. Run `WebSearch`.
2. Record title, URL, snippet, apparent source type.
3. Stop after 10 calls.

## Step 3: Source Triage

For each result, classify Tier:

- **Tier 1:** .gov, .edu, official docs, peer-reviewed
- **Tier 2:** Industry reports, major publications
- **Tier 3:** Established blogs, verified experts, Wikipedia
- **Tier 4:** Forums, personal blogs, social media

Filter duplicate URLs and syndicated content.

## Step 4: Build Source Map

Write to `tmp/research/_sources-{slug}.md`:

```markdown
# Source Map: {Topic}

**Date:** {date}
**Queries executed:** {count}
**Sources found:** {count} (Tier 1: N, Tier 2: N, Tier 3: N, Tier 4: N)

## Sources

| #   | Title | URL | Tier | Relevance | Notes         |
| --- | ----- | --- | ---- | --------- | ------------- |
| 1   | ...   | ... | 1    | High      | Official docs |

## Gaps Identified

- {angle not covered}
- {topic needing deeper research}
```

## Step 5: Identify Gaps

Review source map for:

- Missing perspectives (only positive sources? need criticism)
- Missing data types (no quantitative data? need statistics)
- Recency issues (all sources old? need current data)

Note gaps for `source-deep-dive`.

## Chain Mode (`--chain=deep-dive`)

**[BLOCKING] MUST ATTENTION** when the caller passed `--chain=deep-dive`, read `references/research-chain.md` now and follow it: it runs `source-deep-dive` Steps 1-5 from that skill's own file and writes the evidence base, then returns. Without the flag, skip this section and the run ends at the source map.

---

## Next Steps

**Without `--chain=deep-dive` only** (chain mode follows `references/research-chain.md`). **MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS:** After completion, use `AskUserQuestion`; user chooses:

- **"/source-deep-dive (Recommended)"** — Deep-dive into top sources
- **"/market-analysis"** — If sizing the market (TAM/SAM/SOM), competitors, trends — required before `/business-evaluation`
- **"/business-evaluation"** — If evaluating business viability. **Run `/market-analysis` first** — this skill consumes its sized-market output as evidence and MUST NOT re-derive market sizing.
- **"Skip, continue manually"** — user decides

> **[IMPORTANT MUST ATTENTION]** Use `TaskCreate` to break work into small tasks BEFORE starting.

> **External Memory:** For complex/lengthy research, analysis, scans, or reviews, write intermediate + final results to `tmp/reports/`; prevents context loss and provides deliverable.

> **Evidence Gate:** **MANDATORY IMPORTANT MUST ATTENTION** Every claim, finding, recommendation needs `file:line` proof or traced evidence + confidence (>80% act; <80% verify first).

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `web-research` — Structured web search for evidence gathering; gathering external evidence from the web → .claude/skills/shared/protocols/web-research.md

<!-- PROTOCOL-GUIDES:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Run broad web research, classify and deduplicate candidate sources, and produce a tiered source map + gap list for `source-deep-dive`, never a final report.

**IMPORTANT MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Web Research:** Cross-validate every claim across 2+ credible sources; NEVER cite one source as authoritative.

**IMPORTANT MUST ATTENTION** run ALL 5 main steps in order — (1) define scope + generate 5-10 angle-varied queries → (2) execute `WebSearch` (≤10 calls), record title/URL/snippet/type → (3) triage each result Tier 1-4 + dedupe → (4) build source map at `tmp/research/_sources-{slug}.md` → (5) identify gaps for `source-deep-dive` — why: skipping a step (esp. triage or gaps) yields untiered, gap-blind feedstock that breaks the next stage.
**IMPORTANT MUST ATTENTION** cap WebSearch at 10 calls per invocation; generate 5-10 angle-varied queries (overview, current-state, comparison, data, expert, criticism) then stop at the cap — why: bounded fan-out keeps this breadth-then-triage, not a deep-dive into one angle.
**IMPORTANT MUST ATTENTION** rank every source by tier (Tier 1 .gov/.edu/official > Tier 2 industry reports > Tier 3 established blogs/Wikipedia > Tier 4 forums/social) and dedupe by URL/syndicated content before it counts — why: tier ranking + dedupe keep the feedstock high-signal for source-deep-dive.
**MANDATORY IMPORTANT MUST ATTENTION** NEVER cite a Tier 4 / single source as authoritative — cross-validate every factual claim against 2+ independent sources and declare confidence (95/80/60/<60%) — why: one unverified source = a hallucination-amplifier downstream.
**MANDATORY IMPORTANT MUST ATTENTION** the deliverable is the intermediate source map at `tmp/research/_sources-{slug}.md` (sources table + Gaps Identified), NOT a synthesized report — hand it off to `source-deep-dive`; mine the set for gaps (missing perspectives, missing quantitative data, stale recency) so the next step knows where to dig.
**IMPORTANT MUST ATTENTION** with `--chain=deep-dive`, after Step 5 read `references/research-chain.md` and run `source-deep-dive` Steps 1-5 from its own SKILL.md (never from memory); without the flag stop at the source map — why: the flag is the only contract that lets one step own both halves while each skill still works alone.
**MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting; add a final review todo task to verify work quality; transition one task at a time.
**IMPORTANT MUST ATTENTION** persist intermediate findings/results to a report file in `tmp/reports/` for complex or lengthy work — why: external memory prevents context loss and is itself the deliverable.
**IMPORTANT MUST ATTENTION** a direct `/web-research` call is an explicit skill request: run it with no routing question and NEVER start a workflow from inside this skill; only the post-completion Next Steps question uses `AskUserQuestion`.
**IMPORTANT MUST ATTENTION** every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% verify first) — NEVER speculate without proof.

**Anti-Rationalization:**

| Evasion                                      | Rebuttal                                                                            |
| -------------------------------------------- | ----------------------------------------------------------------------------------- |
| "One strong source is enough"                | NEVER — cross-validate against 2+ independent sources; Tier 4 is never authoritative |
| "I'll just write the report now"             | Out of scope — output the source map + gaps; `source-deep-dive` synthesizes, not this  |
| "Keep searching, more results help"          | Hard-cap is 10 WebSearch calls — breadth then triage, never an unbounded crawl      |
| "Topic is simple, skip tiering/dedupe"       | Tier + dedupe every source — untiered feedstock degrades every downstream step      |
| "Just do it, skip task tracking"             | Skip depth, never skip tracking — `TaskCreate` first, one task in progress          |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.

**IMPORTANT MUST ATTENTION Goal:** triaged, tiered, deduplicated source map + gap list as feedstock for `source-deep-dive` — NOT a final report.
**IMPORTANT MUST ATTENTION** cap WebSearch at 10; cross-validate every claim with 2+ sources; NEVER cite Tier 4 as fact.
**IMPORTANT MUST ATTENTION** `TaskCreate` to break ALL work into small tasks BEFORE starting — this is very important.
