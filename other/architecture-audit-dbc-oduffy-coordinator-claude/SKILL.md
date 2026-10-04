---
name: architecture-audit
description: "Rotational arch audit: score systems, audit the top. No code edits."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
argument-hint: "[system-name]"
---

# Architecture Audit — Rotational System Audit

Selects the highest-priority system from the health ledger, dispatches domain reviewers against
it, and **packages findings as spinoff candidates** down a disposition ladder — the audit itself
**never edits code**. Updates the health ledger's `Last targeted audit` clock and the atlas
metadata.

Run when `/workstream-start` surfaces a stale targeted audit (`check-arch-audit-staleness` owns the verdict), or any time PM intuition
wants a targeted review. `$ARGUMENTS` names a system directly, skipping Step 1.

**Announce at start:** _"I'm using /architecture-audit to audit [system name]."_

---

## Step 1: Select Rotation Target

No `state/health-ledger.md` and no `docs/architecture/systems-index.md` → stop: run
`/architecture-survey` first. `$ARGUMENTS` provided → skip to Step 2 with that system. Otherwise
select the highest-priority system in the ledger — selection signals and worked calibration: wiki
(no engine scorer exists yet). Report: _"Rotation target: [system]. Rationale: [why]."_

<!-- engine-gap: field=rotation.target producer=unknown memo=2026-08-27-claude-klabauter-em-doe-unmarked-obligations-and-four-lost-markers.md -->

---

## Step 2: Review Existing Debt

Read `state/debt-backlog/*.yaml` (or `bin/query-records --type debt --status open`) for the target
system; present open items to the PM before/alongside the audit — full pipeline (plan → review →
execute), not inline here.

---

## Step 2.5: Load Atlas Context

`docs/architecture/systems/{target-system}.md` exists → include it in the reviewer dispatch as
background context. Absent → reviewer discovers from scratch.

---

## Step 2.75: Emit Ground-Truth File-Enumeration Artifact

`cartography file_index --target-root <system-dirs>` → write the `index` field to
`state/audits/{run-id}/ground-truth-files.txt`, commit it. Pass the path in every analysis-agent prompt;
the Opus reviewer diffs any "fabricated"/"non-existent" claim against it before issuing a verdict.

**Out of scope: cross-repo targets** — a host↔addon boundary or any target spanning two repos.
Run the audit once per repo and link the two audit records to each other, naming the boundary
in each.

---

## Step 3: Dispatch System Review

Check the target's **live** file count (not the atlas count — systems grow); small systems get a
direct Opus domain-reviewer dispatch, larger ones need Haiku→Sonnet pre-digestion first or the
reviewer overloads. Threshold, dispatch procedure, prompt sources, and multi-reviewer criteria:
wiki.

> **Do not ask whether to dispatch** — invoking this skill IS the request for the dispatch this
> step names; it dissolves no gate this skill's own body names.

<!-- engine-gap: field=dispatch.review_tier producer=unknown memo=2026-08-27-claude-klabauter-em-doe-unmarked-obligations-and-four-lost-markers.md -->

<!--
This audit's Haiku→Sonnet pre-digestion (Step 3, >10-file path) dispatches the SAME Phase-1/1R and
Phase-2 templates the rebuilt /architecture-survey uses, sourced from one shared template file:
`${CLAUDE_PLUGIN_ROOT}/pipelines/deep-architecture-survey/agent-prompts.md` — no separate copy
exists here to go stale. Three things that do NOT apply to this audit are deliberate, not gaps —
do not "fix" them:

- **Engine extraction consumption (`cartography.*` ops replacing agentic Phase-1 inventory)** does
  not apply here: that consume-gate is wired into /architecture-survey's first-run/refresh atlas-
  *construction* pipeline (full-tree extraction), whereas this audit is a narrower re-review of ONE
  system the atlas already describes (Step 2.5 loads the existing atlas page precisely so
  reviewers do NOT rebuild structure from scratch). Wiring the engine's precomputed substrate into this
  audit's pre-digestion is new scope for a future plan, not an omission of this one.

- **Workflow-native dispatch** (single background Workflow owning a multi-phase, multi-system wave
  map) does not apply here either: this audit dispatches exactly ONE system per invocation, a
  single short-lived 3-tier fan-out — not the multi-wave, multi-system problem the Workflow vehicle
  exists to solve. Only if a future change makes this audit batch multiple systems per invocation
  does that become worth revisiting.

- The **H2 anchors** this audit's Sonnet analysis prompt relies on (`## System Narrative` /
  `## Information Flow Diagram` / `## Boundary Catalog` / `## Health Grade` / `## Summary`, under
  "Phase 2: Sonnet System Analysis Prompt (Audit)" in the shared template file above) must
  continue to exist verbatim — renaming any of them silently breaks this audit without touching
  this file, so check here before renaming those headings in the shared template.
-->

---

## Step 3.6: Scaffold the Canonical Audit Record

`coordinator-doc-new --type audit-record --system <target>` writes
`docs/architecture/audit-records/<YYYY-MM-DD>-<target>.md` — the scaffolded skeleton is
authoritative; the reviewer fills it in-place via `mode: auto`. Reviewer prompt must cover:
populate frontmatter (`grade`, `health_status`, `run_id`, `reviewer`), write the `### Diagram
(ASCII)` section, fill every prose section without flattening grade-rationale/ambition-check
content. Detail: wiki.

**Negative-spec (hard):** the three historical audit records (`2026-05-28-coordinator-runtime.md`
et al.) are frozen point-in-time records — they are NOT retrofitted to the canonical schema (plan
D4). The new shape governs only records authored after this step lands.

---

## Step 4: Package Findings as Spinoff Candidates (never edits code)

Disposition is EM judgment down a ladder:

- **Trivial, tradeoff-free, non-structural** → EM dispatches an executor immediately, no PM gate.
  **Hard guardrail:** any finding touching a module boundary, interface, or cross-system surface
  is ineligible regardless of size — always a spinoff candidate instead.
- **Mid-size cluster** → one bundled spinoff candidate, not N singles or one bloated plan.
- **Large/structural** → standalone spinoff candidate, or escalate to `/plan`. Scaffold a DR first
  when it's an architectural decision: `coordinator-doc-new --type decision --title "<title>"
  --out docs/decisions/DR-<NNN>-<slug>.md`.

Spinoff PM-gate applies only to the grouped/standalone path — surface `Candidate spinoff: <slug>
— <topic>. Authorize?` and block. No debt-backlog auto-write (rationale: wiki).

---

## Step 6: Update Health Ledger

Update the system's row (grade, status, audit date, open-issue counts) and the **`Last targeted
audit`** date only — never `Last full audit`. Calculate and update `Next rotation target` if
present. **Stage, do not commit** (`git add state/health-ledger.md`) — the commit lands only after
the Step 6.5 gate PASSes, so the clock never advances against a stale atlas.

<!-- engine-gap: field=rotation.next_target producer=unknown memo=2026-08-27-claude-klabauter-em-doe-unmarked-obligations-and-four-lost-markers.md -->

---

## Step 6.5: Update Atlas Page (Pre-Commit Gate)

No atlas page for the target → skip entirely. Otherwise pick a branch:

- **Branch A (refresh inline):** edit the atlas body for findings, bump both `last_mapped` and
  `last_attested`, set `grade`/`health_status`, stage alongside the ledger.
- **Branch B (assert current):** zero body diff, bump `last_attested` only, stage, and the
  close-out commit message must contain `atlas-current-as-of: <YYYY-MM-DD>`.

Run `verify-arch-audit-atlas-refresh <AUDIT_DATE> <TARGET_SYSTEM> [<COMMIT_MSG_FILE>]` before
`git commit`. `PASS branch=A|B` → commit scoped, explicit-path: `git commit -m "<subject>" --
state/health-ledger.md <atlas-page-path>`. `FAIL` → do not commit; amend per the branch you're on,
re-stage, re-run. Anti-scope and full branch mechanics: wiki.

---

## Step 6.75: Triage Scratch Files

Large-systems path used → `rm -rf tasks/scratch/weekly-architecture-audit/{run-id}/` (Haiku/Sonnet
output is fully consumed by the Opus reviewer).

---

## Step 7: Report

**Precondition:** the canonical audit record at
`docs/architecture/audit-records/<date>-<system>.md` exists with populated frontmatter and a
`### Diagram (ASCII)` section, staged/committed alongside the atlas + ledger close-out, and the
Step 6.5 gate returned `PASS` — on `FAIL`, fix per that step and re-attempt. Chat report ≠ on-disk
record — the FAIL message text: wiki.

```markdown
## Architecture Audit Complete

**System:** [name]
**Reviewer(s):** [name] at High effort [+ second-angle reviewer, or "none — single angle sufficed"]
**Previous grade:** [X] | **New grade:** [Y]
**Findings:** N total — [X → immediate executor, Y → spinoff candidate(s) surfaced to PM, Z → escalated to /plan]
**Spinoff candidates surfaced:** [list, or "none"]
**Next rotation target:** [system]
```

---

## Notes

Failure modes, cost profile, and relationship to `/architecture-survey`, `/review`/`/review-code`,
and `pipelines/weekly-architecture-audit/PIPELINE.md`: wiki.
