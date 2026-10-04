---
name: registry-hygiene
description: Use when the traceability registries (SN/SR/LLR/TC and the off-spine PB/PART/ASSET/REPO/CMP) need checking or fixing — run trace.py/check.py with the right flags for the current gate, read the orphan/integrity/schema findings, and correct them.
stacks: [python, node, powershell, go, rust, any]
domains: [any]
phases: [dev, gate]
tags: [traceability, trace, registries, orphans, schema]
scope: kit
---

# Registry hygiene (any repo built from this kit)

Keep the `SN → SR → LLR → TC` spine (and the off-spine `PB`/`PART`/`ASSET`/`REPO`/`CMP`
registries) clean: zero orphans, no duplicate/malformed ids, valid schema. Run
the right check for where you are, then read and fix the findings.

## Which command, when

```
# Always-valid floor (pre-commit + check.py at G1): duplicate/malformed ids
# and CSV structure (every registry data row parses to the header's column count).
python scripts/trace.py --strict-integrity

# Full orphan check (aim for orphans=0 before any gate).
python scripts/trace.py --strict

# G2+: also reject leftover template example rows (ids ending -000).
python scripts/trace.py --strict --no-placeholders

# G3: required fields non-empty + closed Verification/Tier vocabularies + Verified.
python scripts/trace.py --strict --no-placeholders --strict-schema --require-verified
```

`scripts/check.py` (or `scripts/check.{sh,ps1}`) runs the gate-appropriate set
automatically from the active gate in `docs/gate` — prefer it for a full gate run;
call `trace.py` directly to iterate on a specific finding.

## Reading findings

- **orphan** — a row not joined end-to-end. Common causes: an SR with no LLR/TC
  yet (fine early; a real orphan at G2+), a `Refs`/`SN-Refs`/`SR-Refs` id that
  points at nothing, a TC that verifies no real id. Fix the back-link, don't
  delete the evidence.
- **integrity** (duplicate/malformed id, or a CSV structure break) — two rows
  share an id, an id doesn't match the `PREFIX-###` shape, or a data row parses
  to more/fewer columns than its header (almost always an unquoted comma in a
  `Permutations` set or free-text cell — quote the cell). Renumber the
  duplicate; fix the malformed id; quote the offending cell. The structure sweep
  covers every `*.csv` under `docs/requirements/` and `docs/test/`, including
  registries `trace.py` never joins (interfaces, project-added ones).
- **schema** (`--strict-schema`) — a required field is empty, or a
  `Verification`/`Tier` value is outside the closed vocabulary
  (`Test|Demonstration|Inspection|Analysis|Manual|Attest|Critique`;
  `Smoke|Full|Release`).
  Fill the field or correct the value.
- **placeholder** (`--no-placeholders`) — a template `-000` example row survived;
  delete it once real rows exist.
- **AC advisory** (`WARNING (advisory)`, warn-only — never fails a run) — an
  `AcceptanceCriteria` uses a comparative term (identical / indistinguishable /
  equivalent / "same as" / matches) without naming its predicate. Pin it: say
  identical *in what*, judged *how* — or accept the wording knowingly at the G1
  consistency review (process.md §4).
- **LLR status-coherence advisory** (`WARNING (advisory)`, warn-only — never
  fails a run) — an LLR reads below `Verified` while every TC that cites it is
  `Verified`, so the evidence to lift it already exists. Fix: edit the LLR's
  `Status` cell to `Verified` (registries are hand-owned — no generator writes
  them back). It never gates: LLR status is non-gating under the derived-gate
  model (the SR's `Verified` drives G2→G3), so a lagging LLR is a readout drift,
  not a coverage hole.

## Verify the fix

Re-run the same command; it must print `orphans=0` (and exit 0). `trace.py`
regenerates `docs/test/report.md` — the readable matrix — so review that too.
Off-spine registries (PB/PART/ASSET/REPO/CMP; legacy MOD read too) are
**integrity-checked only** plus their declared joins (PB Refs, REPO DelegatedSRs,
CMP PartOf/SupersededBy + the primitives' Component tags); a valid
inert `-000` placeholder there never blocks a gate.
