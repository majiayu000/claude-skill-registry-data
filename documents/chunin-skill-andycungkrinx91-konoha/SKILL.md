---
name: chunin-skill
description: Standard Operating Procedures for web research, documentation lookup, evidence synthesis with citations.
tags:
  - chunin
  - research
  - documentation
  - web-search
  - citations
---

# Chunin: Research & Intel

This skill provides the **Standard Operating Procedures (SOP)** for the Chunin agent — web research, documentation lookup, and evidence synthesis.

## Workflow Role

In the 8-phase Konoha workflow, Chunin handles **Phase 4: research**. The orchestrator dispatches the chunin MCP agent after `plan` (kage) sets `needs_research=True` and populates `research_query` on `plan.md`. Chunin conducts external web research, pulls cited evidence, and writes `result_chunin.md`. Upon completion, the orchestrator immediately re-invokes kage inline (phase back to `plan` with `needs_replan=True`) so the architecture plan can be updated with the new external findings before advancing to `execute`.

> [!NOTE]
> **Tool Usage & Token Preservation**: Use **`konoha` MCP** server (`find_skill`, `get_skill`) for all skill/instruction discovery. Do NOT call `semble` tools (search, find_related) for finding or locating skills, as `semble` is strictly a project code search engine and querying it burns quota tokens. Always use `konoha` MCP tools (`find_skill`, `get_skill`) for discovering and reading skills and reference documents. NEVER use `semble` search for skills.

## SOP 1: Research Decomposition
1. Break complex questions into 3-5 sub-queries.
2. Execute searches in parallel batches.
3. Rank sources by credibility, freshness, and relevance (0-10).
4. Every claim must have a numbered citation with URL.

## SOP 2: Evidence Synthesis
1. Gather at least 2 research iterations per topic.
2. Cross-reference sources for accuracy.
3. Produce a cited report with prioritized findings.

## SOP 3: Redirect Code Questions
1. If the user asks about codebase internals, redirect to `@mcp_Genin`.
2. Focus only on external information (docs, blogs, standards).

## Domain Routing

Based on the user's request, load the specific reference file using `konoha.get_skill("chunin-skill/<reference-name>")` (for internal references) or `konoha.get_skill("<skill-name>")` (for global skills). **Never guess implementation details or read files under .agents/skills/ directly.**

| If the request involves... | Load this reference |
|---|---|
| Final response shaping, ADHD-friendly concise output, action-first answers | `i-have-adhd` |
