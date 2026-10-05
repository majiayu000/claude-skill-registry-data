---
name: reporting
description: >
  How dualdb writes its report - verdict first, grouped by cause, every claim an
  evaluated assertion. Use when rendering report.md, MANUAL_REVIEW.md or
  BEHAVIOUR_RISKS.md, when writing a verdict line, or when deciding whether a claim
  can be made at all. The audience is an engineer who must review and own the
  change.
---

# Reporting

Optimize for **reviewability**, not completeness. The reader is an engineer who
has to own this change, not an auditor counting conversions.

## When to use

Rendering any of the three output documents; writing a verdict line; deciding
whether a claim is supportable.

## Decision procedure

Render from the artifacts, then check each claim before printing it.

1. **The report is rendered *from* the JSON artifacts.** It is never the source of
   truth. Every number traces to `changeset.json`, `plan.json` or a validation
   artifact.
2. **A tick is a verified claim.** The checklist is evaluated, not copied. Items
   the tool cannot evaluate render as `not verified` with the reason - never as a
   tick (guardrail R11).
3. **The report is mandatory even for a partial port** (R12).
4. **Lead with the verdict.** No per-line narration; group by cause and dedupe by
   fingerprint.
5. **Never claim verification against an engine that was never connected to.**
   Phase 1 does not execute against PostgreSQL, so the report says
   *"PostgreSQL: not executed - static validation only"* and enumerates every
   unverified path.

## Structure

```
# DualDB Conversion Report
tool <v> · rulepack <v> · model <id> · repo <sha> · <timestamp>

## Verdict
## What was added        (+ File sweep, Inventory, Seams, SQL changes, Type mapping)
## Configuration
## Manual review (N)     -> MANUAL_REVIEW.md
     ### No PostgreSQL equivalent    <- the R9 flags, first
     ### Reserved-word collisions
## Behaviour risks (N)   -> BEHAVIOUR_RISKS.md
## Rollout prerequisites
## What we deliberately did NOT change
## Limitations
## Checklist             <- evaluated, with pass / fail / n-a / not-verified
```

The headline claim belongs in the verdict, as a number:

> PostgreSQL support **added**. SQL Server code paths: **0 bytes changed across
> 186 units** (verified).
> Build: no new failures (T2 Mono, 3 pre-existing).
> Tests: 412 run, 412 passed, 38 DB-requiring deferred to Phase 2.
> **47 items need manual review before this can ship.**
>
> Setting `Data:Provider = SqlServer` executes the original code exactly as
> before.

## Sections that earn trust

**"What we deliberately did NOT change."** Out-of-scope items observed, with
reasons: the `packages.config` files left alone, the obsolete API warnings, the
pre-existing SQL injection exposure reported rather than fixed. Reviewer trust
depends on this section existing and being specific.

**Every `portable-rewrite` listed individually**, with its justification. Those are
the only places existing behaviour could have been affected, so they get named
rather than counted.

**`BEHAVIOUR_RISKS.md` as a separate, short, ranked document.** Every competing
tool reports conversions made; reporting *silent behaviour changes* is what a
reviewer actually needs. Write each entry as an executable test intent - entry
point, input, expected invariant - so Phase 2 can turn it into a dual-run
comparison rather than re-deriving it.

**Rollout prerequisites.** Phase 0 results, PostgreSQL version, required
extensions, the authentication model, sequence re-sync, `search_path`, pooling, and
every path needing a `40001` retry. This is the section ops reads.

## Worked examples

### 1. A supportable claim

> SQL Server code paths: **0 bytes changed across 186 units** (verified).

Backed by 186 `ImmutabilityAssertion` rows in `changeset.json`, each comparing a
`before_sha256` to an `after_sha256`, checked before and after apply. If one row
failed, the number is not 0 and the sentence changes.

### 2. A claim that must be softened

Wrong:

> Tests: 450 passed.

Right:

> Tests: 412 run, 412 passed, 38 DB-requiring deferred to Phase 2 (listed below).

The 38 were never executed. Folding them into a passed count is the single easiest
way for this tool to lose credibility.

### 3. A checklist item that cannot be ticked

```
- [ ] Existing tests pass on SQL Server, and on PostgreSQL or gap stated.
      not-verified - PostgreSQL was not executed in Phase 1; 38 DB-requiring
      tests deferred, listed in Limitations.
```

Not a tick, not a silent omission, and not a failure either - a stated gap with
its reason. That is what R11 asks for.

## Traps

- **Absolutes instead of deltas.** A build result without a baseline is noise.
- **Counting deferred work as done.** Skipped tests, stubbed procedures and
  manual-review items are not conversions.
- **A checklist copied from the source document** rather than evaluated. Every tick
  must have an assertion behind it.
- **Per-line narration.** A reader who wanted the diff would read the diff. Group
  by cause, dedupe by fingerprint, give occurrence counts.
- **Burying the R9 flags.** The no-equivalent items are the primary client-facing
  content; they go first inside manual review, each with its two to three options.
- **An empty "did NOT change" section** in a real repository. It means nobody
  looked.

## Escalate when

- A number cannot be traced to an artifact - do not print it.
- The immutability check failed for any unit: that is a release blocker and the
  verdict must say so, not average it away.
- The report cannot be rendered at all - `dualdb run` fails, per R12.

## Do not

- Do not hand-edit the report. Fix the artifact or the renderer.
- Do not claim a build tier that was not reached.
- Do not report a conversion count without the manual-review and behaviour-risk
  counts beside it.
- Do not echo a connection-string value, ever (guardrail R5).
