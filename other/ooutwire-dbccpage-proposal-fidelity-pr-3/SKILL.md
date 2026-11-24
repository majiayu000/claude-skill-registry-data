---
name: ooutwire
description: "Append-only register of every admitted skill package with confidence and evidence. An audit trail, not a gate."
status: Registry
archive_prefix: none
operad_source_colours: []
operad_target_colour: "Code"
operad_arity: 0
operad_residual: "unknown"
---

# Ooutwire

`AuthorityEffect: None.`

## Prime Directive

Record every skill package admitted from `/auto-suggest-new-skills` and
`/auto-oe-autop` Stage 6, with the confidence and the evidence that produced it.

## What changed on 2026-09-01

This package was an **inbox**: proposals landed as `PROPOSED / PENDING_ADMISSION`
and waited for a human to promote them. The repository owner amended that rule.
Admission is now automatic, and this package is the **register** — it records
what was admitted rather than deciding what may be.

The gate did not disappear; it moved. It is now on **retention**, not entry:
`/auto-review-skills` archives any package idle for 30 days or more. A package
earns its place by being touched, not by being approved.

Consequences worth stating plainly:

* An `ADMITTED` row means a file exists and was mirrored. It does not mean the
  package was reviewed, tested, or run.
* Confidence is still recorded per entry, so a LOW admission stays legible as
  LOW rather than becoming indistinguishable from a HIGH one.
* Archive is reversible; hard delete still requires human evidence.

## Contents

* `proposed_skills_register.md` — append-only ledger of all admissions.
* `recommended_skills_to_build.md` — ranked queue of work still to do.
* `proposed_skills_register_archive_v1.md` — entries rotated out at 20KB.
