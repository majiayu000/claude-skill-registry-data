---
name: maintenance
description: >-
  Use when the user asks for a project health audit, a maintenance sweep, or a
  multi-category lead-engineer scan followed by interactive issue-by-issue
  resolution. Not for routine lint/test runs, single-file cleanups, or plain
  check-project requests.
---

# Task: Project Maintenance & Health Audit

## Overview

Execute a rigorous multi-category maintenance sweep, then walk the user through each finding interactively. The process has two distinct phases:

- **Scan Phase**: Run all checks silently, collecting findings into an internal list. No fixes during this phase.
- **Resolution Phase**: Present the summary, then iterate through each finding — show details, propose a fix, ask the user for a decision, apply if approved.

## Context

<context>
The "Garbage Collector" / "Building Inspector": keeps the codebase maintainable, documented, and architecturally sound.

Categories checked (full sub-check detail is embedded in the 5 self-contained `maintenance-scan-*` subagents — see the Category index in Step 2):
1.  **Structure**: Files in wrong places.
2.  **Consistency**: Docs vs. Code truth.
3.  **Hygiene**: Dead code, unused imports, weak tests.
4.  **Complexity**: God objects and massive functions.
5.  **Debt**: Accumulated TODOs.
6.  **Language**: Inconsistent terminology.
7.  **Doc Coverage**: Missing explanations in code.
8.  **Instruction Coherence**: Contradictions across project instructions.
9.  **Tooling Relevance**: Skills/agents/rules/hooks that don't match the project.
10. **Documentation Health**: Broken cross-links, stale `[x]` FRs, SRS↔SDS / `index` drift.
11. **Architectural Integrity**: Import cycles, layer leakage, reverse dependencies.
12. **Conceptual Duplication**: Parallel impls of one decision; untyped beside typed; schema clones.
13. **API Contract Review**: Capability-vs-impl, sentinel-vs-missing, dead enums, type-vs-runtime divergence.
14. **Cross-Implementation Symmetry**: Capability / error / reserved-set / warning-latch parity across impls.
15. **Defensive-Programming Smell**: Silent swallows, fallback-on-zero, error-as-decision coupling.
16. **Invariant ↔ Test Pairing**: Documented invariants without tests; stub-only contract tests.
17. **Public-Surface Quality**: Synonym/method dupes; internal-only barrel re-exports; mixed reserved lists.
</context>

## Rules & Constraints

<rules>
1.  **Precision**: Use specific thresholds (e.g., File > 500 lines).
2.  **Constructive**: Every issue must have a proposed fix.
3.  **Holistic**: Scan `documents/`, `.cursor/`, and source code directories.
4.  **Mandatory**: Use a task management tool (e.g., `todo_write`, `todowrite`) to track progress through the phases.
5.  **Language Agnostic**: Adapt checks (imports, syntax, test patterns) to the primary language of the project (TS, JS, Py, Go, etc.).
6.  **No premature fixes**: Do NOT apply any changes during the Scan Phase. Only collect findings.
7.  **User decides**: Every fix requires explicit user approval. Never apply fixes silently.
8.  **Findings are first-hand or verified**: every finding MUST be ground-truthed against the source before the summary. Subagent-supplied findings (`Explore`, `Task`, `Agent`, or a `maintenance-scan-*` bucket worker) are leads, not conclusions, and carry no severity until the parent assigns it. See Step 3 (Verify Findings + Severity gate) and [references/verification-gate.md](references/verification-gate.md).
9.  **Severity calibration**: every finding gets one tier per [references/severity-rubric.md](references/severity-rubric.md). In doubt between two tiers, pick the lower (anti-inflation). Critical share ≤ 35 % of total findings.
</rules>

## Question Format (FR-UNIVERSAL.QA-FORMAT)

Binds on EVERY question you ask — the "how to proceed" prompt in Step 5 and the per-finding **Apply / Skip / Edit** verdict in Step 6 alike:

- **Numbered** — each question is a numbered list item (`1.`, `2.`, …), not a heading, a bold-only line, or a paragraph.
- **Self-contained** — the question is answerable from itself and its options alone. Name what is being decided and what the answer changes, inside the question. "Which of the above?", a bare "Your choice?", and "Which variant do you prefer?" with nothing restated are defects: they send the reader back up the transcript to reconstruct the question.
- **Each option stands on its own** — a reader often jumps straight to the options, so an option's title and the lines under it must be enough to choose without the text above the question or the earlier turns. The title is a short name after the option's letter or number, and the reader answers with that letter or number; the `**Essence:**` line under it says what would be done, to what, and what the reader gets. A short reply option with no analysis of its own (Apply / Skip / Edit) has no Essence line, and its title says it alone. **Inside an option, name things in words, never by a report's ids.** Every line of the option — title, Essence, Pros, Cons, Risks, Best for — is read without the report, and ids slip in most often in Pros, Cons and Risks. Write what the thing is instead of its label: "the checkout errand on the shop site", not `E4`; "the search box ignoring the first keystroke", not `N3`. A label in parentheses after a general phrase — "the two most expensive errands (E4, E3)" — is still a bare label: name each item. A number taken from a report keeps what it measures in the same sentence: a percentage names the whole it is a share of ("page text takes about 40% of the cost", not "a 40% share"), and a sum says whose cost it is. **Any phrase that stands for a group is a pointer**: a count ("the four slow pages", "the same three errands"), a category ("the anomalies", "the issues found"), a rank or superlative ("the costliest runs"), "these", "as above", "the current round" — and so is a partial list, a count followed by a few examples or a "such as". Replace it with every member of the group, named in words, in that option — even when the list is long, even when the report above already lists them; if the whole set does not fit, drop the group from the option. Test: with the report deleted, could the reader name every member from this option alone? A word coined in this session gets a short explanation in the option. An explanation elsewhere in the reply does not count — not in the report above the question, not in another option. Before sending, read each option alone, line by line, and list every label (letters plus digits such as `E4` or `N3`), number, group phrase (a count, a category, a superlative, "the same", "these") and coined term in it; replace each with words or remove it.
- **No catch-all option** — never add an option whose only content is an invitation to answer freely ("Other", "Something else", "Your own variant", "Tell me what you need"). The user can always type a free-form reply instead of a letter or number, and an IDE's question tool (`AskUserQuestion` and the like) already offers a free-text answer of its own, so such an option adds a line and no choice. An option that names a concrete alternative is a real option, even when its title starts with "Other".
- **`agent's choice`** — on a multi-select where the user delegates with `agent's choice` (or its language equivalent), pick the subset yourself, justify the pick in one line, and proceed without re-asking for confirmation.

The findings list stays ABOVE the Step 5 question: it is a report the answer filters, not a set of alternatives, so it is not the question's options. The self-containment rule then carries the weight — the question restates the counts it refers to.

## Instructions

<step_by_step>

### SCAN PHASE

Collect findings into an internal list. Each: category, site, problem, proposed fix, severity (`Critical | High | Medium | Low` per [references/severity-rubric.md](references/severity-rubric.md); ties → lower).

1. **Initialize & Plan**
   - Use a task management tool (e.g., `todo_write`, `todowrite`) to create a plan covering all scan categories below.
   - Identify project's primary language and source directories.
   - **Read-only fan-out (FR-MAINT-SCAN)**: scan the 16 categories via 5 parallel specialized read-only `maintenance-scan-*` subagents (one per bucket — names in the Category index below). Each agent is SELF-CONTAINED: its full check detail is embedded in its body — spawn it with just the project context, no payload. Workers return raw leads, no severity; the Verify gate (Step 3), severity calibration, and Resolution (Steps 4–6) stay parent-only over the union.

2. **Run the 16 Category Checks** (partitioned into 5 thematic buckets W1–W5)
   - The COMPLETE per-category sub-check detail is embedded in the 5 `maintenance-scan-*` agent bodies — the single source. SKILL.md carries only the index below, not the executable detail.
   - **Category index** (Cat → bucket → agent):
     - **W1** (`maintenance-scan-hygiene`) — 1 Structural Integrity · 2 Code Hygiene · 3 Complexity & Hotspots · 4 Technical Debt
     - **W2** (`maintenance-scan-dependencies`) — 10 Architectural Integrity · 11 Conceptual Duplication · 16 Public-Surface Quality
     - **W3** (`maintenance-scan-contracts`) — 12 API Contract Review · 13 Cross-Implementation Symmetry · 14 Defensive-Programming Smell
     - **W4** (`maintenance-scan-docs`) — 5 Consistency (Docs vs Code) · 7 Instruction Coherence · 9 Documentation Health
     - **W5** (`maintenance-scan-coverage`) — 6 Documentation Coverage · 8 Tooling Relevance · 15 Invariant ↔ Test Pairing
   - **Delegate**: spawn each bucket's specialized read-only `maintenance-scan-*` agent (named in the index above) via the IDE's subagent tool (`Task` / `Agent` / background task). The agents are self-contained — pass only the project root and a one-line ask ("scan this project, return leads"); no category payload. Workers return raw leads, no severity.
   - **No inline fallback (loud failure)**: if a bucket's agent is unavailable, fails, or times out — retry it ONCE. If it still fails, do NOT re-scan that bucket yourself; record it as NOT SCANNED and report it prominently: the summary (Step 4) MUST carry a line `Not scanned: W<n> (<category names>) — <reason>` after the closing total. Never silently shrink coverage.
   - Collect every lead into the internal findings list. Consolidate the union before the gate; do NOT assign severity yet — that happens once, parent-side, in Step 3.

3. **Verify Findings + Severity (mandatory gate)**
    - Before presenting the summary, walk the collected findings list and confirm each ONE-BY-ONE against the source — whether the scan was inline or delegated.
    - For each finding, perform ONE targeted verification matched to its shape (numeric metric / symbol behavior / undocumented claim / cross-implementation claim / architectural claim). Full per-shape checklist + rationale: [references/verification-gate.md](references/verification-gate.md).
    - Drop findings the verification falsifies. Refine findings the verification corrects. Note falsified ones inline as `[verified false] <site>: <original claim> — actually <observed>` so the user can see the gate ran and what it caught. `[verified false]` lines do NOT receive a severity tag — they are dropped findings, not graded ones.
    - **Severity check**: for every surviving finding, name the rubric anchor in [references/severity-rubric.md](references/severity-rubric.md) that justifies the chosen tier (e.g. `severity-rubric.md#cat-14-silent-swallow`). If you cannot point at the anchor, drop one tier (anti-inflation tie-breaker) or refine the finding so it matches a row.

### RESOLUTION PHASE

4. **Present Summary**
    - Output the full findings list, grouped by category. Plain-text category labels (not `#` headings). Skip empty categories.
    - **Category labels** — use the 16 English names from the Context block above (`Structural Integrity`, `Code Hygiene`, `Complexity & Hotspots`, `Technical Debt`, `Consistency (Docs vs Code)`, `Documentation Coverage`, `Instruction Coherence`, `Tooling Relevance`, `Documentation Health`, then Cats 10–16 per their Context names). In non-English reports every label MUST be a unique tag for that category — do not collapse two categories to one word and do not omit Documentation Health (FR-DOC-LINT: required dedicated header whenever the Documentation Health check (Cat 9) produced any finding; DOC-to-DOC integrity, distinct from #5 and #6). When in doubt, keep the English label.
    - Each issue line follows the shape: `- [N] [Severity] <file/symbol>: <problem>. (Fix: <proposed fix>)`. **Grammar**: severity is one of the four literal English strings `[Critical]`, `[High]`, `[Medium]`, `[Low]` (stays English regardless of report language), placed IMMEDIATELY after the bracketed number and BEFORE the site path; never in the category header. `[verified false]` drop lines from the gate are emitted WITHOUT a severity tag.
    - **Sort within each category**: Critical → High → Medium → Low, ties stable by issue number. Numbering runs sequentially across all categories.
    - Closing line carries BOTH severity totals and category totals: `Total: N findings — Critical: a, High: b, Medium: c, Low: d (per category: <Cat>: x, <Cat>: y, …)`. If any bucket ended NOT SCANNED (Step 2 loud failure), append on the next line: `Not scanned: W<n> (<category names>) — <reason>`.
    - Brief example (covers Categories 1, 2, 9):
      ```
      Structural Integrity
      - [1] [Medium] src/oldfile.ts: in root, should be in src/utils/. (Fix: move)

      Code Hygiene
      - [2] [Medium] utils.ts: unused export `myFunc`. (Fix: delete)

      Documentation Health
      - [3] [High] FR-AUTH marked [x] in SRS, acceptance test path does not exist. (Fix: create the test file or revert to [ ])

      Total: 3 findings — Critical: 0, High: 1, Medium: 2, Low: 0 (per category: Structural Integrity: 1, Code Hygiene: 1, Documentation Health: 1).
      ```
    - One representative finding per category (all 16), in the same shape, lives in [references/example-findings.md](references/example-findings.md). The full per-category rubric for choosing the tier lives in [references/severity-rubric.md](references/severity-rubric.md).

5. **Ask User How to Proceed**
    - Ask which findings to resolve. **Repeat the counts inside the question itself** — the total and the per-severity breakdown — even though the `Total:` line of the report above already states them. The repetition is deliberate, not redundancy to be optimised away: the question has to be answerable on its own, and a reader who skimmed past the list must not scroll back to learn how many findings there are. Writing the counts once in a `Total:` line and then asking a bare "Which findings should I resolve?" is exactly the defect this rule exists to prevent. Shape it like "Which of the 12 findings should I fix — 2 Critical, 3 High, 5 Medium, 2 Low?". Accepted reply modes:
      - **numbers** (e.g. `1, 3, 4`) — only those findings
      - **category name** (e.g. `Hygiene`) — that category
      - **severity name** (`critical`, `high`, `medium`, `low` — case-insensitive) — that tier
      - **compound severity** (plus-separated, e.g. `critical+high`) — union of listed tiers
      - **`all`** — every finding one by one
      - **`agent's choice`** — pick the most impactful subset yourself with a one-line justification, proceed without re-asking
      - **`done`** — stop, no fixes

6. **Interactive Resolution Loop**
    - For each selected finding (in order):
      1. Show file, problem, proposed fix.
      2. Ask (numbered question per FR-UNIVERSAL.QA-FORMAT): **Apply** | **Skip** | **Edit** (user supplies alternative fix).
      3. After applying, briefly confirm.
    - After all selected findings, show counts: N applied, M skipped, K edited.

</step_by_step>

## Verification

<verification>
[ ] Checked structural integrity (file placement, naming, configs).
[ ] Scanned for dead code and unused imports.
[ ] Checked file/function length limits (500/50 lines).
[ ] Aggregated all TODO/FIXME tags.
[ ] Verified documentation terminology vs code usage.
[ ] Checked for missing code documentation (File/Class/Method).
[ ] Checked instruction coherence across CLAUDE.md, AGENTS.md, and docs (contradictions, ambiguities, redundancy).
[ ] Checked tooling relevance (skills, agents, hooks vs. project stack and domain).
[ ] Checked Documentation Health (FR-DOC-LINT) — findings grouped under the dedicated `Documentation Health` header.
[ ] Checked Cats 10-16 (architectural review): integrity, conceptual duplication, API contract, cross-impl symmetry, defensive smell, invariant↔test, public surface.
[ ] Verified Findings gate ran: each finding was ground-truthed against the source (subagent-supplied findings re-read by the executor) before the summary; falsified findings dropped with a `[verified false]` line.
[ ] Every surviving finding carries one of `[Critical] | [High] | [Medium] | [Low]` per `references/severity-rubric.md`; the anti-inflation tie-breaker was honored (Critical share ≤ 35 %).
[ ] Closing total line reports per-severity counters in addition to per-category counters.
[ ] Presented numbered summary of all findings, grouped by category, sorted within each category Critical → High → Medium → Low.
[ ] Asked the user how to proceed with resolution, accepting numbers, category, severity name, compound severity, `all`, `agent's choice`, or `done`.
[ ] Resolved selected findings interactively (apply/skip/edit per finding).
[ ] Showed final resolution summary (applied/skipped/edited counts).
</verification>
