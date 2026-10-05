---
name: confidence-and-manual-review
description: >
  The dualdb confidence rubric and the triggers that force manual review. Use when
  scoring a finding, when deciding whether a conversion may be applied
  automatically, when writing a MANUAL_REVIEW.md or BEHAVIOUR_RISKS.md entry, or
  when a decision feels borderline. Borderline means manual-review.
---

# Confidence and manual review

## When to use

Scoring a finding; deciding `add-pg-alternate` versus `manual-review`; writing a
review or risk entry; judging whether the engine is being over-confident.

## Decision procedure

1. Classify the finding into one of the three failure classes below.
2. Score it with the rubric under **Scoring**.
3. Apply the escalation triggers - any one of them forces `manual-review`
   whatever the score says.
4. Write the entry: `MANUAL_REVIEW.md` for an unresolved item,
   `BEHAVIOUR_RISKS.md` for every class-3 hit, both if it is both.

## The three failure classes

Keeping these separate is what makes the tool honest.

1. **Compile break** - the code will not build. Loud, cheap to find, easy to
   trust.
2. **Runtime error** - builds, throws at run time. Bad SQL, a missing function, a
   wrong parameter type, an `InvalidCastException` on a reader.
3. **Silent behaviour change** - builds, runs, returns *different data*. The
   dangerous class, and the reason this tool is worth building.

**Class 3 is never auto-converted-and-forgotten.** Every class-3 hit gets a
`BEHAVIOUR_RISKS.md` entry even when the code change itself is confidently
correct.

## Scoring

```
score = base(rule.tier)
      x schema_penalty        (1.0 known / 0.6 inferred / 0.0 unknown-and-required)
      x resolution_penalty    (fully-resolved 1.0 / partially dynamic 0.5 / opaque 0.0)
      x context_penalty       (test coverage present, single call site, etc.)
```

`score < --confidence-threshold` (default 0.85) -> `manual-review`.

**Class-3 hits cap the score at the threshold** regardless of the rest, so they can
never auto-pass silently. A zero in any factor is a zero overall - an opaque
statement or a required-but-absent schema fact is not something the other factors
can compensate for.

The breakdown is stored per change unit, not just the product, so a low score can
be explained rather than merely reported.

## Escalate when

Any one of these forces `manual-review`, whatever the score says:

- an unresolved dynamic fragment (`PG-DYN-004`)
- any rule with `noEquivalent: true` - and its two to three options must be
  carried into the entry (guardrail R9)
- a rule with `requiresSchema: true` and no schema hints supplied - **never
  infer schema**
- a `behaviour-risk` hit the classification cannot resolve from the code alone
  (the two `NOLOCK`s that look identical and are not)
- a `mixed` unit whose data access cannot be cleanly separated from its business
  logic - duplicating logic is forbidden (guardrail R2)
- a provider type in a **public** signature: converting it changes the contract,
  and the callers are outside the unit
- the scope guard rejected the unit under `--strict-scope`

## What decides schema-dependence

`requiresSchema: true` marks a rule whose decision needs facts the source alone
does not carry:

- column nullability - affects `COALESCE` and join semantics, and NULL ordering
- whether a `bit` column is read as `bool` or `int` (partly inferable from code)
- the actual collation of a text column - case-sensitivity behaviour
- whether identifiers were created quoted
- the precision of a `decimal` or `money` column
- the existence of an index referenced by a hint
- the primary key, for `DELETE TOP (n)` rewrites

`--schema-hints <file>` supplies these without the tool ever connecting to a
database. Re-running with hints **upgrades** previous manual-review items into
generated alternates - which is what turns Phase 1 into a repeatable process
rather than a one-shot.

## Writing a good entry

**`MANUAL_REVIEW.md`** - one entry per unresolved item, grouped by cause with the
highest-impact group first. Each carries: what, where (`file:line`), why it could
not be decided, the rule ids, and - for a no-equivalent construct - two to three
options with their trade-offs stated honestly. An option list where one choice is
obviously right is not a real option list; say so and recommend it.

**`BEHAVIOUR_RISKS.md`** - short, ranked, and separate. Every competing tool
reports "conversions made"; reporting *silent behaviour changes* is the
differentiator and the thing a reviewer actually needs.

Write each risk as an **executable test intent** - endpoint or entry point, input,
expected invariant - so Phase 2 can turn it into a dual-run comparison instead of
re-deriving it.

## Worked examples

### 1. Auto - a fully resolved statement with one `auto` rule

`SELECT ISNULL(Discount, 0) FROM dbo.Orders`, in a unit that already uses
`DbConnection`.

```
base(auto) 1.00 x schema 1.00 x resolution 1.00 x context 1.00 = 1.00
```

One hit (`PG-NULL-001`), no class-3 hit, nothing schema-dependent, nothing
unresolved. Above the threshold, so the rule may be applied without human
judgement - inside a generated alternate, or as a `portable-rewrite` if every
condition of the narrow exception holds.

### 2. Capped - a correct conversion that still needs a risk entry

`SELECT Id FROM dbo.[Order] ORDER BY ShippedUtc`, where `ShippedUtc` is nullable.

```
base(auto) 1.00 x schema 0.60 (nullability inferred) x resolution 1.00 x context 1.00
  = 0.60, then capped at 0.85 by the class-3 hit -> 0.60
```

`PG-ORD-001` is a `behaviour-risk`: NULLs sort first on SQL Server and last on
PostgreSQL. Emitting `NULLS FIRST` is mechanically correct and the entry still goes
into `BEHAVIOUR_RISKS.md`, because the *reason* the ordering changes is worth a
reviewer's attention. Below the threshold here because nullability was inferred
rather than known.

### 3. `manual-review` - a zero factor

`SqlHelper.Fill(sql)` where `sql` is a method parameter.

```
base(auto) 1.00 x schema 1.00 x resolution 0.00 (opaque) x context 1.00 = 0.00
```

A zero in any factor is a zero overall. No amount of confidence elsewhere
compensates for not knowing what the statement is. `manual-review`, grouped under
"generic SQL helper", with the call sites listed so the reviewer can see the scale.

Note what the tool does **not** do here: it does not generate a `Fill_PostgreSql`
that forwards the same text to Npgsql. That would compile and fail on the first
T-SQL statement handed to it.

## Traps

- **A high score on a class-3 hit is a bug in the scoring**, not a green light.
- **"It looks obviously fine" is not evidence.** The two `NOLOCK` examples in the
  hub skill differ only in what the caller depends on.
- **A run dominated by `portable-rewrite` means the engine is over-confident.**
  Investigate it as a defect, not as good news.
- **Inferring schema from naming** - assuming `IsActive` is a `bit`, or that
  `Email` is case-insensitive - is exactly the guess this rubric exists to
  prevent.
- **An option list with a hidden default.** If the tool picked one and listed the
  others for form's sake, that is a silent approximation (guardrail R9).

## Do not

- Do not auto-convert anything hand-labelled `manual` in a corpus. That is a
  release blocker.
- Do not let a class-3 hit pass without a risk entry.
- Do not write "review this" as an entry. Say what to check and what would make it
  safe.
- Do not lower the threshold to make a run look better.
