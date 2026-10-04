---
name: check-docs-consistency
description: 'Cross-reference project docs for drift, stale references, and contradictions. Outputs timestamped report. Discovers Markdown wherever it lives in the repo.'
disable-model-invocation: true
tags: [audit, scan, docs, periodic, report]
---

# Check Docs Consistency

Stateless scan. Read docs, cross-reference, write timestamped report. Report-only — resolution is the user's call.

## When to Use

User invokes `/super-bootstrap:check-docs-consistency` when:

- Starting a new feature pipeline (verify source of truth before writing specs)
- Drift pain surfaces ("wait, didn't we decide the opposite?")
- After a batch of merges that touched multiple docs
- Periodically as a health check (weekly or per-milestone)

## Doc Surface

The scan reads `**/*.md` at any depth and keeps the authored project docs. The filter drops generated and vendored Markdown — paths under `node_modules/`, `vendor/`, `.git/`, `dist/`, `build/`, `target/`, `.venv/`, and the scan's own `.review/` reports. The kept set is the doc surface, wherever the project holds it: a `docs/` tree, a root `README` plus scattered `*.md`, `documentation/`, `.github/`, or any mix.

The glob already includes the orchestration files (`CLAUDE.md`, `.claude/agents/*.md`, `.claude/skills/**/SKILL.md`); Step 1 mines those specifically for path references and ownership statements.

Extend the exclusion list per project when a tree carries `*.md` that is generated or vendored output rather than authored project doc (e.g. `.next/`, `coverage/`, `__pycache__/`).

## Procedure

### Step 0: Pre-flight — Block If a Prior Report Is Unprocessed

Glob `.review/docs-consistency-*.md`. (Step 0 reads `.review/` to find prior reports; Step 1's doc-surface scan excludes that same dir — see Doc Surface.)

If a report from a previous date exists, stop and surface the path(s): findings route through the user's triage first (fix / dismiss / track per project convention), and the processed report is deleted or archived before the next scan of the same type. Re-invoke after.

The skill produces no second report while a prior one is pending. Same-day re-runs are exempt (they overwrite today's file; see Step 3). The user may explicitly override the block to force a fresh scan.

### Step 1: Discover and Read All Docs (one pass)

Glob `**/*.md` across the repo, then post-filter to the Doc Surface set — drop paths under the excluded trees, including the scan's own `.review/` reports. Glob takes one positive pattern, so the exclusion is a filter on the result list, not a glob argument. The orchestration files (`CLAUDE.md`, `.claude/agents/*.md`, `.claude/skills/**/SKILL.md`) fall inside this set — Step 1 mines them for path references and ownership statements specifically.

Read each file once. While reading, extract everything into a working set:

**Universal extractions (every project):**

- Cross-references (file paths, `§Section` refs, markdown links to other docs)
- Doc/file path references in orchestration files (CLAUDE.md, agent MDs, skill MDs)
- Ownership/guardrail statements in CLAUDE.md
- Temporal-doc conventions in CLAUDE.md (which dirs are delete-after-merge / temporal — e.g. spec/plan/handoff locations)
- Feature/module names mentioned across multiple docs
- File paths referenced in any doc
- Each prose doc's dimension — state-SSOT (truth-now) vs history-SSOT (dated chronicle) — per the classify predicate in `assets/dimension-predicate.md`. Skip harness MDs (CLAUDE.md, skill/agent/rule files — own no-precedent discipline). Needed for Step 2's P2 dimension-pollution check.
- Catalog rows and their entry files — for each doc (or section) passing the catalog predicate in `assets/catalog-predicate.md`: per row, the **claim set** (what the row asserts about its entry — behavior, arguments, defaults, refusals) and, for the entry file that row resolves to, the **section roster** (`##`/`###` headings plus what each section states). Extract per row against its own file — never a whole-corpus load. Needed for Step 2's P0/P1 catalog-row checks.

**Project-aware extractions (discover from what exists):**

- API endpoint patterns (`GET /...`, `POST /...`) if the project has backend docs
- Database/schema paths if the project has data docs
- Component/module names if the project has frontend/architecture docs
- Field/concept names that appear in multiple docs (potential mismatch surface)
- Screen/route names if the project has UI docs
- Config/env references if the project has deployment docs

The goal: build a map of "what references what" across the doc surface. Don't predetermine the categories — discover them from what the project actually documents.

For each concept named across multiple docs, also note its defining (home) doc — where it is actually specified, not merely mentioned. Required for Step 2's P3 link-gap check.

### Step 2: Cross-Reference

All validations run against the extracted set. Every finding comes from comparing what one doc says against what another doc says — contradictions, orphans, mismatches. The P2 dimension-pollution check is intra-doc: it inspects a single doc's dimension purity rather than comparing a cross-doc pair. Deduplicate: same file+line appears once under the highest-priority match.

**P0 — Would Cause Bugs If Trusted:**

- Cross-reference to nonexistent doc or section (broken link)
- Same concept defined differently in two docs (contradictory definitions)
- API endpoint/route in one doc but missing or different in another
- Schema/field in one doc that contradicts another doc's schema
- Catalog row asserts something its entry file's corresponding section states the negation of (catalog predicate: `assets/catalog-predicate.md`)
- Catalog row omits a whole named contract-class section of its entry file — a constraint its reader would violate unseen (contract-class per `assets/catalog-predicate.md`)

**P1 — Would Waste Dev Cycles:**

- Concept referenced as if it exists but has been removed or renamed in another doc
- Component/module in one catalog but missing from another
- Catalog row omits a whole named descriptive section of its entry file (descriptive per `assets/catalog-predicate.md`)
- Orphan doc (not referenced by any other file, not an index)
- Stale doc/file path in orchestration files (referenced file missing, glob has no matches)
- Removed feature/screen still referenced elsewhere
- Stale temporal artifact — a spec/plan/handoff doc in a delete-after-merge location with no matching active work. The set of delete-after-merge dirs comes from the project's own convention (extracted in Step 1)

**P2 — Slow-Burn Confusion:**

- Field/concept name mismatch for the same thing across docs (e.g., `targetLang` vs `targetLanguage`)
- Ownership contradiction in CLAUDE.md (two docs claiming to own the same concern)
- Internal terminology leaking where user-facing language is expected (or reverse)
- Handoff/WIP folder with no matching feature branch
- Dimension pollution — a prose doc breaks state XOR history per the audit predicate in `assets/dimension-predicate.md`: (a) chronicle crawl-in (timestamps / "was X, now Y" / decision-dated prose accumulating in a persistent state-SSOT doc), (b) stale workspace doc (a vaporizable/status doc gone out-of-date against what it tracks), (c) state leak into history (a decision-timeline doc carrying persistent knowledge that belongs in a state-SSOT home). Harness MDs excluded (Step 1). Surface the doc + polluting lines; the fix (overwrite / move to git / restate as present-tense constraint) is the user's call

**P3 — Cosmetic / Completeness:**

- Doc section referenced in index but empty or stub
- Feature documented in specs but absent from overview module index
- Missing link to a concept's home doc — a link-candidate concept in doc A (per the predicate in `assets/link-predicate.md`: B defines it, A uses it substantively, A is not a catalog/index) carries no link to its SSOT home B. Surface as a suggestion; which link to add is the user's call.

### Step 2.5: Cross-Reference Findings with the Project Tracker (post-analysis only)

Annotate findings against the project tracker per the contract in `assets/tracker-annotation.md` (read it for the post-analysis discipline, overlap→tag table, and delete-on-close git-log verification). Runs only when the project keeps a tracker (e.g. `docs/work/` card set — `{BUG,DEBT,GAP}-###.md` files + `README.md` high-water header); skip otherwise — run AFTER Steps 1–2 classify all findings.

This scan's index targets: file+section references and named concepts (endpoints, field names, component names). Tags land in the report's Cross-Reference Annotations section; the P0–P3 finding tables are untouched.

### Step 3: Write Report

Write the report to:

```
.review/docs-consistency-{YYYY-MM-DD}.md
```

Create `.review/` at the repo root if absent (gitignorable — the report is ephemeral triage state, kept out of the doc surface by the Step 1 exclusion). One file per run date — re-run on same day replaces the previous.

Present summary to user in chat. The persisted file is the source of truth for status tracking.

**Durable hygiene stamp.** Alongside the dated report, overwrite `.review/doc-hygiene.json` with the scan's current-state summary:

```json
{ "last_audited": "{YYYY-MM-DD}", "status": "clean|dirty", "findings": { "p0": 0, "p1": 0, "p2": 0, "p3": 0 } }
```

`status` is `clean` when total findings == 0, else `dirty`; `findings` carries the per-priority counts so a reader sees severity without re-running. This is a **verification stamp** — current-state metadata, not a chronicle: overwrite in place every scan, never append a "was X, now Y" line. Roles: creator = this step; consumer = a config-refresh pass or a human glance; no terminal cleaner — the stamp is self-superseding (each scan overwrites), and orphan risk is moot because `.review/` is gitignored local-ephemeral. Promote to a committed path only if a cross-repo fleet roll-up is built. The Step 0 block-if-pending gate means a blocked run leaves the stamp at its prior value — staleness is then self-evident from `last_audited`.

## Workflow Fan-Out (opt-in)

The inline single-pass above is the default (rung 1). Fan out per the contract in `assets/workflow-fanout.md` — its § Sizing pre-flight + § The escalation ladder own the rung choice (attention-fit informed by cheap proxies, not surface size alone), and the § Fan-out contract covers decomposition, hard report-schema output, merge rule, and reader/judge tier split. Read it before authoring the script.

This skill's binding output is the §Report Format schema below; the judge emits it exactly. The Step 2.5 git-log verification is the tracker-annotation step the judge runs. The Step 3 report + `doc-hygiene.json` stamp are gateway-side writes from the merged result — same in both the inline and fan-out paths.

## Report Format

```markdown
# Doc Consistency Report

**Date:** {today}
**Project:** {project name}
**Docs checked:** {list of docs read}

## P0 — Would Cause Bugs If Trusted

| # | File(s) | Line(s) | Finding |
|---|---------|---------|---------|

## P1 — Would Waste Dev Cycles

| # | File(s) | Line(s) | Finding |
|---|---------|---------|---------|

## P2 — Slow-Burn Confusion

| # | File(s) | Line(s) | Finding |
|---|---------|---------|---------|

## P3 — Cosmetic

| # | File(s) | Line(s) | Finding |
|---|---------|---------|---------|

## Cross-Reference Annotations

**Post-scan layer.** The scan ran blind to the tracker — these annotations only
add context for triage. They do not modify or suppress findings.
{Omit this section when the project keeps no tracker.}

| # | Finding (short) | Tag | Detail |
|---|-----------------|-----|--------|

## Summary

- P0: {count}
- P1: {count}
- P2: {count}
- P3: {count}
- Total: {count}
- New vs already tracked: {n new, n tracked, n potential regressions} {omit without tracker}

## Recommended Actions

{For each P0/P1 finding: what to fix and which doc owns the truth.}
{For borderline items: the question to resolve and who should decide.}
```

## Scope

- Report is a file. Resolution is the user's call.
- Flags inconsistency, not correctness. Decisions are the user's.
- Doc-to-doc cross-reference only. Code is out of scope.
- Stateless between scans for the dated report — each run writes a fresh timestamped file. The one durable carry-over is `.review/doc-hygiene.json` (overwrite-in-place verification stamp).
