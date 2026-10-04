---
name: compliance-drift-guard
description: >-
  Use when governance evidence lives in markdown — a component provenance registry, a deviation
  ledger, a definition-of-done compliance matrix, a coverage manifest — and nothing stops it going
  stale, such as rows citing deleted files, unknown status tokens, roll-up counts that no longer
  match, or code carrying a documented exception that no ledger entry covers.
---

# Compliance drift guard

## Profile keys consumed

- `make.test_unit_client`
- `make.lint_md`
- `architecture.source_root`
- `architecture.modules`

Run the generated guard suite through the target mapped by `make.test_unit_client`; when that key
maps to `null` the repository has no unit lane to host it — skip the run with a recorded
capability-absent note and report which assertions went unverified, rather than invoking a target
that does not exist. The same applies to the docs linter reached through `make.lint_md`.

## Overview

Hand-maintained evidence documents rot the moment code moves. Locking the whole set — registry,
ledger, matrix — into one generated test suite makes drift a build failure instead of a review
opinion. The guard reads the artifacts as text, resolves every claim against disk and against the
runtime exports, and asserts in both directions.

## When to use

- A story or epic produced markdown evidence that later work must not silently invalidate.
- A registry, ledger, manifest, or compliance matrix is maintained by hand.
- Source files carry inline notes about a deliberate exception with no machine link to a record.
- A closed vocabulary (status, kind, verdict, source) is described in prose and enforced nowhere.
- Not for: linting prose or links generally — the docs linter reached through `make.lint_md`
  already covers formatting and relative links.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — no provenance registry or deviation ledger, but the same shape is already used
  by the route-coverage inventory gate (route keys reconciled against a manifest, validated both
  ways) and by the meta-tests under the unit tooling directory that read config and source as text.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — no registry or
  ledger; the nearest equivalents are the file-reading contract tests under the unit contracts
  directory, which the same construction extends.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — a
  component-provenance document, a deviation ledger, and the story artifacts plus a sprint-status
  YAML file are locked by a single provenance-traceability unit test.

## Procedure

The guard is a unit suite: run it through the target mapped by `make.test_unit_client` (skip with the
recorded note above when that key maps to `null`). Parse each artifact once at module scope, then generate cases with `it.each` over the parsed rows so every row
is its own named failure:

```ts
const SOURCE_TOKENS: readonly string[] = ['`ported`', '`adapted`', '`new`'];
const VERDICT_TOKENS: readonly string[] = ['Complete', 'Evidence-elsewhere', 'Gap'];
// Prettier escapes pipes inside table cells, so split on unescaped pipes only.
const cells = (row: string): string[] => row.split(/(?<!\\)\|/).map((c) => c.trim());
```

Cover these classes of assertion:

1. **Coverage, both ways** — every runtime export has exactly one row; every row resolves to a real
   export; rows flagged internal are not exported; every component directory under
   `architecture.modules` has a row or an explicit scope exclusion.
2. **Closed vocabularies** — source, kind, status, and verdict cells hold only listed tokens.
3. **Path resolution** — every file or module path cited in a rationale, alignment note, or row
   resolves on disk.
4. **Evidence minimums** — rationale and alignment fields meet a minimum length (80 characters is
   enough to stop a one-word citation), and each row ends with a closed deviations clause: either an
   explicit "none" with a reason, or a list of ids.
5. **Ledger integrity** — ids unique, each row carrying an owner and a tracking reference, each
   justification meeting the same length minimum, and roll-up counts equal to the parsed row count.
6. **Cross-links** — registry rows cite only ids the ledger defines; ledger rows cite where the
   decision was taken; any ratification register names only defined ids.
7. **Code-level tagging** — scan source under `architecture.source_root` for deviation phrases (a
   criterion number, "deliberate deviation", "documented exception"); each site either carries an id
   or appears in an explicit allowed-site list, and every id found resolves in the ledger.
8. **Matrix compliance** — every story artifact appears in the matrix, every cited artifact exists,
   all verdict cells are closed tokens, and the roll-up per verdict matches the parsed rows.
9. **Link and status invariants** — spec links point only at this repository, and every key in the
   sprint-status file has a matching artifact file.

## Parsing gotchas

- Match code sites by exact phrase, never by line number — line numbers drift on the next edit.
- Rows may cite paths belonging to an upstream repository; exclude those from on-disk resolution
  rather than making them resolve locally.
- Closed tokens appear in two table shapes: a definition table and a roll-up count table. Assert
  both against the parsed rows, or one can drift unnoticed.
- Keep the allowed-site list explicit and small; an open-ended exclusion makes the whole suite pass
  vacuously.

## Common mistakes

- Reading a failure as the guard being too strict — a red guard means evidence is missing or stale.
  Add the row, file the ledger entry, tag the site, or update the matrix.
- Widening a token set, relaxing a citation rule, or deleting a row to get green.
- Asserting only that rows are well-formed, so a deleted export leaves an orphan row nothing
  catches.
- Growing the allowed-site list instead of tagging the site with the record it belongs to.
