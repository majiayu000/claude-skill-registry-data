---
name: ai-film-production-ledger
description: Record append-only AI-film prompt, asset, model, output, review, selection, and retry lineage for multi-shot production without making creative or generation decisions.
---

# AI Film Production Ledger

Authority: `record_only`.

Use this Skill when a multi-shot project needs a reproducible record of the
final generation candidate, submitted prompt, exact asset versions, model
surface/settings, output evidence, review, selection, and retry ancestry.

## Ownership

- DIRcreative remains the project, story, shot, continuity, asset, approval,
  and final-state owner.
- This Skill records lineage only. It is never a story owner, director,
  generation adapter, approval authority, or delivery authority.
- Runtime state remains the canonical project truth. Ledger entries reference
  its IDs and hashes rather than creating a second project state.

## Deterministic contract

Validate with:

- `docs/film-preproduction/schemas/ai-film-production-ledger.schema.json`
- first snapshot: `python3 scripts/ai_film_production_ledger.py validate <ledger> --initial-ledger [--artifact-root <root>]`
- append: `python3 scripts/ai_film_production_ledger.py validate <ledger> --previous <snapshot> [--artifact-root <root>]`

The generation-candidate envelope is immutable; output and review collections
may only append. A retry binds its parent, one primary delta, preserved
successes, exact prompt hash, real asset bytes/version hashes, model
surface/settings, expected visible proof, and optional verified cost. State
changes are separate append-only events. `--initial-ledger` accepts only one
genesis attempt plus one `planned` event; subsequent snapshots require
`--previous` and preserve `ledger_id` plus `genesis_sha256`.

The baseline flag is mandatory: omitting `--previous` cannot silently reset the
append-only boundary. Verified generation, review, selection, and delivery also
require project-relative receipt-manifest files and output bytes whose hashes
resolve beneath `--artifact-root`. Verified receipts are signed and their
authority keys must already be pinned in DIRcreative's host-owned review trust
registry; the generic CLI cannot introduce a key. Media-provider, human-review,
and delivery authority scopes are separate and cannot sign for one another.

## State boundaries

Keep `planned`, `attached`, `executed`, `observed_unverified`,
`generated_verified`, `selected`, and `delivered` distinct.

- Early drafts are not attempts; record only the final candidate actually queued
  for generation, or a clearly `planned` candidate when execution is not
  authorized.
- `generated_verified` and `delivered` require external verified evidence.
- `selected` requires independent or human review evidence.
- `verified` cost/credits require a signed billing-provider receipt bound to the
  exact attempt and amount/currency; otherwise cost remains `unverified`.
- A failed/rejected parent is preserved; never overwrite it with a retry.
- Output paths stay project-relative, output hashes cannot be reused across
  attempts, `output_id` is ledger-global, and credentials, authorization
  headers, bearer values, cookies, and session material never enter the ledger.

The optional timeline field is a reservation for a later editorial system; this
Skill does not perform editing, grading, mixing, mastering, or delivery.
