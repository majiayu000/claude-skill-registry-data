---
name: assumptions
description: >
  Generate an evidence-backed Assumptions ledger for a Git diff, feature,
  endpoint, worker, migration, or code path. Use when reviewing a change,
  asking what could break, preparing a release, finding edge cases, assessing
  deployment safety, analyzing retries or concurrency, or designing
  failure-focused tests.
---

# Assumptions

## Purpose

Identify the conditions a change silently depends on in order to work safely
in production.

Produce a structured ledger of:
- hidden assumptions, phrased as conditions that must hold
- repository evidence, with a file and line locator where available
- failure modes
- existing safeguards
- falsification tests
- recommended controls
- status, evidence confidence, and priority

This is not a generic code review. Do not report vague concerns.

## Core standard

Only report an assumption when you can provide all of the following:

1. The assumption stated as a falsifiable condition (what must hold, not
   what the current code does — see "Phrasing assumptions as conditions"
   below).
2. Direct evidence from code, tests, configuration, schema, documentation,
   or the Git diff, with a file path and line range when the tooling
   available can produce one. If a line range is unavailable, cite the
   file path and the symbol (function, route, migration file) instead.
   Never present a claim as repository evidence without a locator.
3. A concrete consequence if the assumption is false.
4. Existing safeguards, or an explicit statement that none were found. A
   "none found" statement must name the scope that was searched (files,
   directories, or symbols) — see "Search boundary for absence claims"
   below. Do not write "none found" without saying where you looked.
5. A practical falsification test or verification step.
6. A status label: Protected, Partially protected, Unprotected, or Unknown
   (see "Status vs. evidence confidence" below).
7. An evidence confidence label: High, Medium, or Low.
8. A priority: P0, P1, P2, or P3.

### Status vs. evidence confidence

These are two different questions and must not be collapsed into one label.

- **Status** answers: *does the repository protect against this condition
  failing?* Values: `Protected` (a safeguard was found and it appears to
  fully address the risk), `Partially protected` (a safeguard exists but
  has a gap), `Unprotected` (no safeguard was found in the searched
  scope), `Unknown` (the reviewed scope doesn't contain enough
  information to tell).
- **Evidence confidence** answers: *how solid is the evidence behind that
  status call?* Values: `High` (direct, unambiguous code/config/test
  evidence), `Medium` (reasonable inference from related code, but not a
  direct observation of the behavior in question), `Low` (thin or
  indirect evidence; flag this rather than rounding up to Medium).

Do not label a status `Protected` or `Unprotected` as "Verified" — that
conflates whether a safeguard exists with whether the underlying
production behavior (e.g. "the gateway never retries") is actually
guaranteed. A status can have High evidence confidence while the broader
real-world claim it implies is still not fully knowable from the repo
alone; say so in "Unknowns and boundaries" rather than overstating the
status label.

### Phrasing assumptions as conditions

Phrase each assumption as the condition that must hold, not as a
description of what the current code appears to do. This keeps the
Assumption column stable even as Status changes across reviews.

| Weaker phrasing (avoid) | Stronger phrasing (use) |
|---|---|
| "Refund processing is idempotent per request." | "Duplicate refund requests are prevented or safely deduplicated." |
| "The migration fully completes before any worker runs." | "New worker code remains safe before, during, and after the schema transition." |
| "The client can always tell whether the refund succeeded." | "A caller can reliably determine the outcome after a response interruption." |

### Search boundary for absence claims

"None found" is only meaningful if it states where the search happened.
Write it as:

```
None found in src/refunds/, db/schema.sql, and tests/refunds/retry.test.ts;
queue configuration was not inspected.
```

not as a bare "None found." An unqualified absence claim reads as
complete when it may only reflect a partial search.

If evidence is insufficient to call a status `Protected` or `Unprotected`,
use `Unknown` and pair it with a concrete verification step rather than
guessing. An `Unknown` status is not a defect — it is a task for someone
with runtime or operational knowledge the repository doesn't contain.

## Investigation procedure

1. Determine scope.
   - If a Git repository and uncommitted changes exist, inspect the current diff.
   - Otherwise use the file, symbol, feature description, or user question.
   - State exactly what was analyzed.
   - **Empty scope:** if no diff exists and no file, symbol, or question was
     given, ask the user what to analyze rather than guessing or scanning
     the entire repository.
   - **Oversized scope:** if the diff or requested scope spans more files
     than can be read carefully (as a guide, more than ~15 changed files),
     do not sample arbitrarily. Instead, identify the highest-risk
     subset (new endpoints, migrations, auth/payment code, concurrency-
     sensitive paths) and state explicitly which files were excluded and
     why, so the user can request a follow-up pass on the rest.
   - **Two-stage output for oversized scope:** before producing the
     ledger, output a short review plan naming the high-risk paths
     selected for this pass and the paths excluded, e.g.:
     ```
     ## Review plan

     High-risk paths selected:
     - New payment endpoint
     - Migration

     Excluded for this pass:
     - UI-only files
     - Generated client files
     ```
     Then produce the ledger for the selected paths only. This makes the
     scoping decision visible before any conclusions are drawn from it.

2. Map the changed behavior.
   - Identify entry points, callers, data reads/writes, side effects, external
     calls, queues, caches, feature flags, authorization checks, and tests.
   - Inspect adjacent code needed to understand the behavior.

3. Identify implied conditions.
   Look for assumptions about (category tag in brackets):
   - input validity and nullability `[input]`
   - data shape and historical records `[input]`
   - uniqueness and ownership `[security]` `[concurrency]`
   - ordering, time, and expiry `[concurrency]`
   - concurrency and atomicity `[concurrency]`
   - retries, duplicate delivery, and idempotency `[concurrency]` `[failure]`
   - partial failure and recovery `[failure]`
   - dependency availability and response behavior `[failure]`
   - migration, rollout, rollback, and version compatibility `[deploy]`
   - configuration and feature flags `[deploy]`
   - scale, pagination, and resource bounds `[failure]`
   - authorization, tenancy, and secrets `[security]`
   - observability and repair `[failure]`

   When a mode flag is given (see Modes), only pursue categories tagged
   for that mode; skip the rest unless evidence for an in-scope category
   surfaces an unavoidable out-of-scope risk (mention it briefly under
   Unknowns rather than opening a full ledger entry for it).

4. Search for evidence.
   - Read relevant tests, migrations, schemas, configuration, and documentation.
   - Search for validation, database constraints, idempotency keys, locks,
     retries, fallbacks, timeouts, metrics, alerts, and recovery paths.
   - Do not assume a safeguard is absent until relevant nearby code has been
     inspected.

5. Rank findings.
   - P0: security breach, irreversible corruption, duplicate financial action,
     or unsafe migration likely to fail rollout.
   - P1: meaningful user impact under plausible production conditions.
   - P2: a real risk that requires verification, documentation, or follow-up.
   - P3: low-impact observation or weak-evidence hypothesis.

6. Produce the ledger.
   - Prioritize high-evidence-confidence, high-impact findings.
   - Include no more than 10 entries by default.
   - If more than 10 valid findings exist, keep all P0 and P1 findings
     first (never drop a P0 to make room for a lower-priority item), then
     fill remaining slots with the highest-priority P2/P3 findings. State
     the count of findings omitted and their priorities so the user knows
     what was cut.
   - Prefer concise evidence over a broad speculative checklist.

7. Offer next steps.
   - Do not change code unless the user asks.
   - If asked to fix findings, address one ledger entry at a time and add a
     regression or falsification test where practical, using the test
     framework, file layout, and naming conventions already present in
     the repository rather than introducing a new one.

## Required output format

```
# Assumptions: <scope>

**Scope:** <files, branch comparison, symbol, or feature analyzed>
**Overall risk:** <Low | Medium | High>
**Release blockers:** <count, or none found>

## Executive summary

<2-5 sentences describing the most important assumptions, evidence quality,
and recommended immediate action.>

## Ledger

| Priority | Assumption | Evidence | If false | Status | Falsification test | Recommended action | Evidence confidence |
|---|---|---|---|---|---|---|---|

Evidence must include a file path and line range when available (or file
path and symbol if a line range can't be produced). Status must be one of
Protected / Partially protected / Unprotected / Unknown, and must state
the search scope when reporting no safeguard was found.

## Existing safeguards

- <Only safeguards actually found in the repository.>

## Required verification before release

- [ ] <Specific verification, test, or operational check.>

## Unknowns and boundaries

- <Important runtime behavior that cannot be confirmed from repository
  evidence.>
```

## Terminology

- **Assumption:** A condition that must hold for the behavior to be safe or
  correct, phrased as the condition itself (see "Phrasing assumptions as
  conditions" above) — not as a description of what the code currently
  appears to do.
- **Status — Protected:** A safeguard was found in the searched scope and
  it appears to fully address the risk.
- **Status — Partially protected:** A safeguard exists but has an
  identifiable gap (e.g. covers one call site but not another).
- **Status — Unprotected:** No safeguard was found within the stated
  search scope.
- **Status — Unknown:** The reviewed scope doesn't contain enough
  information to assign Protected, Partially protected, or Unprotected.
  Pair this with a concrete verification step, not a guess.
- **Evidence confidence — High:** Direct, unambiguous evidence from code,
  tests, schema, or config.
- **Evidence confidence — Medium:** Reasonable inference from related
  code, without directly observing the behavior in question.
- **Evidence confidence — Low:** Thin or indirect evidence. Flag it as Low
  rather than rounding up.
- **Falsification test:** A test or procedure designed to show whether the
  assumption fails.

Status and evidence confidence are independent: a `Protected` status can
carry `Low` evidence confidence if the safeguard was only inferred, not
directly observed. Never substitute one label for the other, and never use
"Verified" as a stand-in for either — it conflates whether a safeguard
exists with whether the broader real-world claim is guaranteed.

## What this skill must not do

- Invent business rules that do not appear in the repository or request.
- Treat every missing validation as a bug.
- Claim production behavior without evidence.
- Generate a generic "possible edge cases" checklist.
- Recommend sweeping refactors before identifying the actual risk.
- Automatically modify production-sensitive code without explicit approval.
- Label a concern "critical" merely because it sounds scary.
- Confuse an unknown external behavior with a verified flaw.

## Modes

| Command | Purpose | Categories in scope |
|---|---|---|
| `/assumptions-scan` | Analyze the current diff or requested scope. | All |
| `/assumptions-scan <file or symbol>` | Analyze one code path, module, endpoint, worker, or function. | All |
| `/assumptions-scan --deploy` | Focus on migrations, rollouts, flags, version overlap, rollback, and compatibility. | `[deploy]` |
| `/assumptions-scan --failure` | Focus on retries, partial failure, dependencies, timeouts, queues, and recovery. | `[failure]` |
| `/assumptions-scan --concurrency` | Focus on races, duplicate delivery, locking, atomicity, and idempotency. | `[concurrency]` |
| `/assumptions-scan --security` | Focus on identity, authorization, tenancy, secrets, trust boundaries, and data exposure. | `[security]` |
| `/assumptions-scan --tests` | Produce falsification tests only. | All (filtering happens on output, not investigation) |
| `/assumptions-scan --compact` | Produce a short PR-ready ledger. | All (filtering happens on output, not investigation) |

Category tags match the ones used in step 3 of the Investigation
procedure. A mode restricts which categories are investigated; it does
not change the Core standard — every reported finding still needs
evidence with a locator, a consequence, a falsification test or
verification step, a status label, an evidence confidence label, and a
priority.

The `/assumptions-scan ...` notation above names the mode, not a
registered slash command — whether it becomes an actual slash command
depends on the host. Treat it as shorthand for "invoke Assumptions in
this mode," e.g. "Use Assumptions in deploy mode for this migration" and
`/assumptions-scan --deploy` refer to the same request.

### `--tests` output format

Skip the full ledger. For each finding that would otherwise appear,
output only:

```
### <Priority> — <Assumption, one line>

**Falsification test:** <concrete steps or test code>
**Proves:** <what a pass/fail result tells you>
```

Order findings P0 first. Omit Evidence, Status, and Recommended action —
those belong in the full ledger, not this mode.

### `--compact` output format

Produce the same investigation and the same Core standard, but render
only:

```
# Assumptions: <scope> (compact)

**Overall risk:** <Low | Medium | High> · **Release blockers:** <count>

| Priority | Assumption | If false | Falsification test |
|---|---|---|---|
```

Limit to the P0 and P1 rows; summarize P2/P3 findings, if any, as a
single trailing line ("N additional lower-priority findings omitted —
run without `--compact` for the full ledger").
