---
name: quality-audit
description: Umbrella quality review — runs quality-coverage + quality-lint + quality-debt + architecture-review, aggregates findings into a single readiness report, flags patterns spanning dimensions. Loads when the operator says "audit the project" / "overall quality check" / "pre-release review" / "how healthy is AICP right now", or as a periodic (monthly/quarterly/pre-release) review.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# quality-audit

The umbrella quality review. Where `quality-coverage` audits one dimension
(tests covering code) and `quality-lint` audits another (code + content
style), this skill runs them BOTH (plus debt inventory + architecture review)
and synthesizes the findings into a single pre-release / periodic readiness
report. The value is in the SYNTHESIS — patterns that span dimensions (e.g.,
"all the coverage gaps are in files with high lint violations AND high debt
markers — these files need full refactor, not point fixes").

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "audit the project", "overall quality check", "how healthy is AICP", "pre-release review", "quality snapshot", "state of the project"
- **Periodic cycle**: scheduled review (monthly, quarterly) — a rolling snapshot lets you track trajectory, not just point-in-time state
- **Pre-release gate**: before shipping a milestone, confirm quality across all dimensions
- **Post-incident retrospective**: after a bug ships, audit surfaces patterns across dimensions (not just the one that caused the bug)
- **New-contributor onboarding**: a fresh audit gives a new contributor the "how healthy is this" overview without them having to synthesize from scratch

Do NOT load when:

- Only ONE quality dimension is the concern (load that specific skill: `quality-coverage` / `quality-lint` / `quality-debt`)
- You want an architecture review (load `architecture-review` — narrower focus)
- You want a status report on work-in-progress (load `pm-status-report` or `pm-assess` — those report on what's being BUILT, not the quality of what's built)

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Run sub-audits in parallel

**Trigger**: skill loaded; operator wants an umbrella audit.

**Process**:

1. Run the coverage sub-audit. This means loading `quality-coverage` and executing at least its Operation 1 (generate coverage report) and Operation 2 (classify gaps). Capture the output file: `wiki/decisions/00_inbox/coverage-audit-<date>.md`.
2. Run the lint sub-audit. Load `quality-lint` and execute at least its Operation 1 (run both linters) and Operation 2 (classify violations). Capture: `wiki/decisions/00_inbox/lint-audit-<date>.md`.
3. Run the debt sub-audit. Load `quality-debt` (currently boilerplate — rewrite pending, but the intent is: inventory all `TODO`, `FIXME`, `XXX`, deferred items from wiki/backlog, known workarounds in code comments). Capture: `wiki/decisions/00_inbox/debt-audit-<date>.md`.
4. Run the architecture sub-audit. Load `architecture-review` on AGENTS.md + CLAUDE.md + aicp/ structure. Capture: `wiki/decisions/00_inbox/architecture-audit-<date>.md`.
5. Confirm all four sub-audits produced a baseline page; if any failed, note in the umbrella report rather than silently omitting.

**Quality bar (Operation 1 done when)**:

- [ ] All four sub-audits ran (or documented failure for any that didn't)
- [ ] All four baseline pages exist in `wiki/decisions/00_inbox/`
- [ ] Per-audit pass/fail captured (so the umbrella report is honest about what succeeded)

### Operation 2: Synthesize cross-dimension patterns

**Trigger**: Operation 1 sub-audits complete.

**Process**:

1. Load each sub-audit page. Read the HIGH-risk / HIGH-priority items from each.
2. Identify **cross-dimension patterns** (the unique value of this skill):
   - **Convergent problems** — a single file appearing as HIGH-risk in 2+ audits. Example: `aicp/core/router.py` has <70% coverage (coverage audit) AND 15 lint violations (lint audit) AND 3 TODO markers (debt audit). That file is a prime refactor candidate.
   - **Dimensional imbalance** — one dimension has many issues, others clean. Example: coverage is good, lint is good, but debt inventory shows 40 TODO markers. Debt is the bottleneck.
   - **Systemic gaps** — a PATTERN of issues across files. Example: every file that imports circuit_breaker has coverage gaps on the OPEN-state path. This isn't a file-level issue — it's a testing-strategy issue.
   - **Clean areas worth protecting** — files that pass all four dimensions. Note them as "healthy — don't break."
3. Rate the overall project health using explicit criteria:
   - **Green**: <5 HIGH-risk items total across all dimensions, no convergent problems
   - **Yellow**: 5-15 HIGH-risk items OR ≥1 convergent problem OR ≥1 systemic gap
   - **Red**: 15+ HIGH-risk items OR 3+ convergent problems OR unaddressed prior-audit findings

**Quality bar (Operation 2 done when)**:

- [ ] Convergent problems identified (files appearing in 2+ sub-audits as HIGH)
- [ ] Dimensional imbalance assessed (is one dimension dominating?)
- [ ] Systemic gaps identified (patterns, not just file-level issues)
- [ ] Healthy areas explicitly noted
- [ ] Overall health rating assigned with explicit criteria

### Operation 3: Author the umbrella report

**Trigger**: Operation 2 synthesis complete.

**Process**:

1. Create `wiki/decisions/00_inbox/quality-audit-<date>.md` (type=reference). Required sections:

   ```markdown
   ## Summary
   Overall health: <Green | Yellow | Red>. One-line rationale.

   ## Sub-audit findings
   Links to the 4 sub-audit pages with their individual ratings.

   ## Convergent problems
   | File | Coverage | Lint | Debt | Architecture | Refactor priority |
   |------|---------|------|------|-------------|-------------------|

   ## Dimensional summary
   | Dimension | Items | Trend vs prior audit | Owner |
   |-----------|-------|---------------------|-------|

   ## Systemic gaps
   Patterns across the codebase that no single sub-audit would catch.

   ## Healthy areas (protect these)
   Files/modules that passed all dimensions cleanly.

   ## Recommended actions
   Prioritized list of follow-ups (not arbitrary — mapped to convergent problems + systemic gaps).
   ```

2. Link the prior quality-audit page (if any) in a `## Trajectory` section. Compare: overall rating trend, per-dimension trend. "Getting better" / "stable" / "regressing" — with evidence.
3. Run `python3 -m tools.lint wiki/decisions/00_inbox/quality-audit-<date>.md`.

**Quality bar (Operation 3 done when)**:

- [ ] Umbrella report has all 6 required sections
- [ ] Convergent problems table populated
- [ ] Trajectory comparison with prior audit (if any)
- [ ] Recommended actions MAP to identified problems (not generic)
- [ ] Report lint passes

### Operation 4: Present + trigger follow-up work

**Trigger**: Operation 3 report authored.

**Process**:

1. Present the report to the operator. Point at the file path; summarize the overall rating + top 3 recommended actions.
2. Operator decides:
   - **Accept + act**: create follow-up tasks in `wiki/backlog/tasks/` for the recommended actions. One task per action, with specific file references from the report.
   - **Accept + defer**: acknowledge findings, don't act yet. Record the deferral in the audit page's Recommended Actions section with a `DEFERRED until <date/milestone>` tag.
   - **Reject + investigate**: operator disagrees with a finding. Re-check the sub-audit that surfaced it; if the finding was methodology-flawed, fix the sub-audit and re-run.
3. If a systemic gap is operator-confirmed, contribute back to second brain as a lesson: `gateway contribute --type lesson --title "..."`. Systemic gaps are exactly the kind of convergent evidence that makes a good lesson (≥3 evidence items from independent sources — the 3+ sub-audits).
4. Schedule the next audit. For AICP scale: monthly default, more frequent if Yellow/Red, less if Green and stable.

**Quality bar (Operation 4 done when)**:

- [ ] Operator received the report (pointed at path, not paraphrased)
- [ ] Follow-up tasks created for accepted recommendations
- [ ] Deferrals documented in the audit page
- [ ] Systemic gap (if any) contributed as lesson
- [ ] Next-audit cadence noted in the report

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Green rating without running all sub-audits (false summary)

The temptation: skip the debt audit because it's "nothing interesting." Rate the project Green based on the three sub-audits that ran. But "we didn't check" is not the same as "we checked and found nothing."

**Detection**: did you run all 4 sub-audits? Or did you skip one because it seemed low-value?

**The rule**: every umbrella audit runs all 4 sub-audits. If a sub-audit's skill is boilerplate (not yet rewritten), document THAT as a known limitation in the umbrella report — don't quietly omit.

### Gotcha 2: Convergent-problem blindness (looking only at per-dimension leaders)

The temptation: the coverage audit highlighted 5 files. The lint audit highlighted 5 different files. You list 10 problem areas without checking if ANY of them overlap. Convergent problems (files on BOTH lists) are different magnitude — they're where refactor is justified. Missing them means recommending 10 small fixes when 1 refactor would handle 3 of them.

**Detection**: did you explicitly cross-reference the sub-audits' HIGH-risk lists for overlap?

**The rule**: Operation 2 step 2 is NOT optional. Cross-reference is the umbrella audit's unique value. A list of issues is cheap; convergence analysis is expensive.

### Gotcha 3: Trajectory without prior baseline (can't see trend)

The temptation: first audit, no prior data, so skip the trajectory section. But the report is the SEED for future trajectory analysis — if this audit has no numbers, the NEXT audit can't compare.

**Detection**: umbrella report has Summary + recommendations but no numeric rundown (total issues per dimension, per-file counts, etc.).

**The rule**: every umbrella audit captures COUNTS per dimension in the report body. The first audit's trajectory section says "baseline established"; every subsequent audit fills in the comparison.

### Gotcha 4: Recommendations not mapped to evidence (generic advice)

The recommendations section says "improve test coverage, reduce lint violations, address tech debt." Those are category-level generics — they're not actionable. Each recommendation should map to specific convergent problems or systemic gaps identified in Operations 2.

**Detection**: could an unrelated project's quality audit contain the same recommendations? If yes, they're too generic.

**The rule**: every recommendation names specific files or patterns. "Refactor aicp/core/router.py — convergent across coverage + lint + debt" is actionable. "Reduce lint violations" is not.

### Gotcha 5: Deferral without tracking (silent "later" again)

Same pattern as `quality-lint` Gotcha 4 and `quality-coverage` Gotcha 5: deferrals without task files are forgotten. At umbrella level the risk is higher because the umbrella's deferrals tend to be larger ("defer this file's refactor" vs specific line-level fixes).

**Detection**: the audit page marks items DEFERRED but no follow-up task file exists.

**The rule**: every deferral has a task file with specific file/line references AND a target date/milestone. Umbrella-level deferrals especially need dates — they're big enough to slip indefinitely without one.

## Reference exemplars

Per Extension Standards, reference exemplars are the second brain's `model-builder` and `wiki-agent` skills. For the OUTPUT artifact:

- **Umbrella audit page shape**: follows the second brain's `Domain Overview` page type (`~/devops-solutions-research-wiki/wiki/spine/standards/domain-overview-page-standards.md`) — state of knowledge across multiple dimensions with coverage + gaps + recommendations.

## Domain context

This skill operates in **backend-ai-platform-python** — see [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml). It's a read-only skill (no code changes directly; it authors wiki pages and files follow-up tasks).

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| quality-coverage | coverage dimension only | Single sub-audit; this skill runs all sub-audits |
| quality-lint | lint dimension only | Single sub-audit; this skill runs all sub-audits |
| quality-debt | debt dimension only | Single sub-audit; this skill runs all sub-audits |
| architecture-review | architecture dimension only | Single sub-audit; this skill runs all sub-audits |
| pm-assess | work-in-progress state | Reports on BUILD status; this skill reports on QUALITY of what's built |
| pm-status-report | progress/velocity/blockers | Business metrics; this skill is technical health |
| full-refactor-cycle | refactor execution | Umbrella audit surfaces refactor candidates; full-refactor-cycle acts on one |
