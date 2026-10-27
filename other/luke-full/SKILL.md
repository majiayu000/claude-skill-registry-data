---
name: luke-full
description: >
  Full health assessment of the Luke codebase. Orchestrates five read-only
  phases in sequence: platform integrity (/luke-deps platform), architectural
  compliance (/luke-audit), runtime correctness (/luke-bugs), application
  security (/luke-security) and QA adequacy (/luke-test assess), then
  synthesizes them into a categorical health state with an owner per finding.
  Use before a release, after a long vibe coding period, or for a periodic
  full health check. Scoping: /luke-full apps/api | --since <ref> | --full
argument-hint: '[--full|--since <ref>|<path> [--since <ref>]]'
context: fork
agent: general-purpose
background: false
disallowed-tools: Edit, Write, NotebookEdit
---

# Luke Full Audit — Orchestrator

A complete health assessment of the Luke codebase, across five read-only
phases. Do NOT modify any file.

**Orchestrate and synthesize. Never invent a sixth checklist of your own** — if
a check belongs to no phase below, it belongs in the skill that owns that
domain, not here (`.claude/skills/luke-shared/governance-map.md`).

**Read `.claude/skills/luke-shared/audit-protocol.md` first**, and
`.claude/skills/luke-shared/result-contract.md` for the footer this skill emits.

Every phase is read-only. Two are modes chosen precisely because they do not
write: `/luke-deps platform` assesses the platform without upgrading anything,
and `/luke-test assess` reports what evidence is missing without creating it.
**Never invoke `/luke-test write` from here**, and never `/luke-deps apply`.

`/luke-full` is the case where `--full` makes the most sense: before a release
you want the absolute state, not the delta since the last session. Scope is
resolved exactly once, before Phase 0 — see "Scope Resolution" below — never
re-decided independently by each of the four phases that take one. Phase 0 is
the exception regardless of scope: `/luke-deps platform` reads the
repository's own configuration, which has no diff scope.

---

## Scope Resolution — before Phase 0, before anything else

**Invocation arguments:** $ARGUMENTS

Resolve the invocation arguments above per the normative order in
`audit-protocol.md` §1, **before** running any git diff command. This skill
takes no mode, so the whole bound value is the scope selector.

**The selector is carried across the skill boundary unchanged.** Never
translate it into a semantically equivalent one:

| Bound value              | Carried to every phase   |
| ------------------------ | ------------------------ |
| `--full`                 | `--full`                 |
| `--since <ref>`          | `--since <ref>`          |
| `<path>`                 | `<path>`                 |
| `<path> --since <ref>`   | `<path> --since <ref>`   |
| *(empty)*                | *(empty)*                |

`--full` was once rewritten to `.` here, on the reasoning that §1 already
defines an explicit path as recursive and `.` is the repository root. A full
run proved that wrong: the first child bound `.` as an *empty* selector and
silently ran the default diff instead of the monorepo. An equivalent selector
is not the same selector. Carry the canonical token.

On `--full`, do not derive the default diff first "to check", and do not ask
for confirmation — the explicit flag *is* the user's confirmation (§1 point 4).

On an **empty** selector, derive the default diff for your own scope reporting;
if it is empty, say so and stop rather than silently escalating to a full scan
(§1 point 5). Pass the empty selector down unchanged: each child then derives
the identical default from the same repository state. That is the design
working, not a gap — a selector is deterministic, a materialized file list is
not, and §1 defines no form for one.

You may materialize the file set for your own `Scanned:` line. **The
materialized set is never the transport value**, and there is no variable to
forward: each phase below receives the **literal selector string** above.

---

## Execution Plan

Run the five phases **sequentially**, in this order. Set each child skill
call's `args` to the **literal selector string** you resolved above —
`args: "--full"`, `args: "--since abc123"`, `args: "apps/api"`, or `args: ""`
when the invocation was empty. Never pass a
variable name, a placeholder, or the words "carried selector": those are
prose here and would be read by §1 as a path that does not exist, silently
scoping a phase to nothing. Each forked skill declares `background: false`, so
waiting is a property of the runtime and not just an instruction here
(audit-protocol §6.1).

### Phase 0 — Platform & Toolchain

Invoke: `Skill(luke-deps) platform`

Read-only. Takes no diff scope: its input is the repository's own configuration.
Runs first because a platform failure explains application findings that follow
— a version skew reported as four mysterious type errors is one finding, not
four.

### Phase 1 — Architectural Compliance

Invoke `Skill(luke-audit)` with `args` = the carried selector, verbatim.

### Phase 2 — Runtime Correctness

Invoke `Skill(luke-bugs)` with `args` = the carried selector, verbatim.

### Phase 3 — Application Security

Invoke `Skill(luke-security)` with `args` = the carried selector, verbatim.

Findings escalated by Phase 2 are re-derived here, not inherited.

### Phase 4 — QA Adequacy

Invoke `Skill(luke-test)` with `args` = **`assess` followed by the normalized
carried selector, verbatim** — `args: "assess --full"`,
`args: "assess --since abc123"`,
`args: "assess apps/api"`, or `args: "assess"` when the selector is empty.
`/luke-test` is mode-bearing (audit-protocol §1 point 1): it parses the mode
first, then the remainder as the selector. Dropping `assess` would leave the
mode unset — never pass the selector alone.

Read-only. Answers whether the changed surface has evidence behind it. A missing
required tier is a QA GAP, and a QA GAP is a finding — it is what "the tests
passed" cannot tell you.

---

## Final Synthesis Report

After all five phases complete, produce this unified executive summary:

```
═══════════════════════════════════════════════════════════
  LUKE FULL AUDIT REPORT
  Scanned: <path or 'full monorepo'>
  Date: <today>
═══════════════════════════════════════════════════════════

## Health

| Phase                 | Severities (each skill's own scale) | Status |
|-----------------------|-------------------------------------|--------|
| /luke-deps platform   | P0 n · P1 n · P2 n                  | ...    |
| /luke-audit           | HIGH n · MEDIUM n · LOW n           | ...    |
| /luke-bugs            | CRITICAL n · HIGH n · MEDIUM n      | ...    |
| /luke-security        | CRITICAL n · HIGH n · MEDIUM n      | ...    |
| /luke-test assess     | QA GAP n · residual risk X          | ...    |

Severities stay in each skill's own vocabulary — `/luke-audit` has no CRITICAL,
`/luke-security` has no LOW, `/luke-deps` counts P0/P1/P2, `/luke-test` reports
QA GAPs. Do not translate them into a shared scale; the differences are real.

**Overall: <HEALTHY | HEALTHY WITH KNOWN GAPS | ACTION REQUIRED | RELEASE BLOCKED>**

Suppressed by baseline: N

### How the state is decided

Evaluated top to bottom; the first matching rule wins. Only **CONFIRMED**
findings count — a `NEEDS DECISION` is a question for the user, not a defect,
and it never moves the state on its own.

| State                        | When                                                                                                     |
| ---------------------------- | -------------------------------------------------------------------------------------------------------- |
| **RELEASE BLOCKED**          | any confirmed CRITICAL (bugs/security) or P0 (platform), **or** a required gate that ran and failed |
| **ACTION REQUIRED**          | any confirmed HIGH or P1, **or** a QA GAP whose residual risk is HIGH                                    |
| **HEALTHY WITH KNOWN GAPS**  | no confirmed HIGH or above, but **any** confirmed backlog finding (MEDIUM / LOW / P2), QA GAP, baseline suppression or open `NEEDS DECISION` exists |
| **HEALTHY**                  | no confirmed findings at all, and no QA GAP, suppression or open decision                                  |

There is deliberately **no numeric score**. The previous
`100 − (CRITICAL×20 + HIGH×10 + …)` produced a two-digit number out of counts an
LLM produced, which moved when findings were grouped differently rather than
when the code changed. A state that says which rule fired is auditable; `82/100`
is not. Do not reintroduce a score, a percentage or a grade.

`HEALTHY` is deliberately hard to reach: it means nothing confirmed was found
and nothing is knowingly unproven. A confirmed MEDIUM is still a confirmed
finding, so it lands in `HEALTHY WITH KNOWN GAPS` — the state exists to say
"nothing urgent, and here is what we know about". Reporting a backlog as
`HEALTHY` is how a backlog stops being read. No severity arithmetic is involved:
the rule asks whether a confirmed finding exists, not how the scales compare.

**"A required gate that ran and failed"** means exactly that: a gate applicable
to this scope, executed, and red — `pnpm check:drift`, a failing suite, a red
`typecheck:test`. A tier that was *not required* for the scope, or required and
*not executed*, is not a failure. The first is a correct SKIPPED, the second is
a QA GAP, and neither blocks a release by itself. Reporting an unexecuted tier
as a red gate would make every partial run look like an emergency.

A state is not a verdict on the release: it is a statement about evidence. Say
which rule fired and which finding triggered it.

## 🔴 Release blockers
Every CONFIRMED blocker across all five phases — CRITICAL (bugs/security) or P0
(platform) — as: file:line · severity · remediationOwner · one-line fix.
If none: ✅ No blockers.

## 🟠 Action required
Every CONFIRMED HIGH or P1, same shape. A QA GAP with HIGH residual risk belongs
here too, owned by /luke-test.
If none: ✅ Nothing requiring action.

## 🟡 Backlog
Counts of MEDIUM/LOW/P2 by category. No detail — it is in the phase reports.

## ❓ Needs decision
Findings whose status is NEEDS DECISION, with the question each one poses.
These are **not** queued for remediation by anyone: they are yours to answer.
If none: ✅ Nothing awaiting a decision.

## Patterns & Observations
2-3 sentences on recurring themes across all findings.
E.g. "Error propagation is the dominant issue — 4 of 6 HIGH findings
involve errors being swallowed in catch blocks."

## Promotion to rule (consolidated)
Merge the "Promotion to rule" sections from the phases, deduplicating them. If
the same class emerges from two skills, propose it once.
This section is the report's most valuable output: it converts LLM findings
into deterministic checks that make the next report shorter.

## Recommended Next Session Focus
One specific area to address first, based on finding density and severity.
```

---

## Synthesis rules

- **Correlate across phases; deduplicate only on the same root cause.** The same
  `file:line` reaching two phases is a **hint**, not identity — two skills can
  legitimately find different defects on one line. Collapse two reports only
  when they clearly describe the same underlying invariant. Findings with
  different domain owners stay distinct unless there is an unambiguous reason to
  merge them.

  Where a platform or domain-owner finding **explains** downstream symptoms,
  keep the owner's finding canonical and mention the symptoms beside it as
  related observations in the Markdown — a version skew is one finding with
  four visible effects, not five findings.

  **Never rank severities across skills.** The vocabularies have no common
  scale (`luke-audit` has no CRITICAL, `luke-security` no LOW, `luke-deps` uses
  P0–P2), so "keep the higher severity" is not a computable instruction. When
  two reports do merge, the canonical one keeps **its own** severity, and the
  structured finding keeps a single `source` — the contract's `source` is
  singular by design. Name the corroborating phase in the Markdown instead.
- **Every finding carries an owner pair.** `domainOwner` is the skill that owns
  the invariant; `remediationOwner` is who should act — derived from
  `governance-map.md` §3, never from severity. A platform finding is remediated
  by `/luke-deps`, a QA GAP by `/luke-test`, docs drift by `/luke-docs`, and
  application code by `/luke-fix`.
- **Do not invent findings to fill a table cell.** A phase with nothing to say
  reports `✅ No findings`.
- **Emit the structured footer** defined in
  `.claude/skills/luke-shared/result-contract.md`, so `/luke-fix` can route
  without re-reading five reports. The footer records the synthesis; it is not a
  second place health is computed.

## Structured footer

Close the report with the result contract's JSON block. It carries per-finding
`status` and `evidence` alongside the ownership pair, because those are what
keep a `NEEDS DECISION` or a QA GAP from being queued as an executable fix.
