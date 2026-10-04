---
name: drift-audit
type: Skill
title: "drift-audit — refresh the canonical-DB conformance numbers, then act"
description: "The re-measure and standing report of the canonical data model's live DB conformance. Use when asked 'where are we at' on DB drift or conformance, to update the drift numbers, when a drift-audit brief is re-issued, or on /drift-audit. NOT the per-table fix recipe (use matrx-frontend's db-canonicalize-table)."
tags: [db, canonical-model, audit, conformance, chips]
timestamp: 2026-08-21T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/drift-audit/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# drift-audit — refresh the numbers, then act

**Invocation: `/drift-audit`.** The deliverable is never just numbers: it is *numbers → diff
→ chips fired → decision list*. Ending at a report with no chips is an incomplete run —
that gap is exactly why this skill exists (Arman, 2026-08-21).

## 0. Ground rules

- **Live project ONLY: `brsgrqvjdzwihsvnfqkf`** (`db.matrxserver.com`). Never access the
  retired project `txzxabzwovsujtloxrus`, including for reads or historical comparison;
  use archived evidence for historical comparisons instead.
- **Verify against live state, never against a brief.** Audit briefs go stale and get
  re-issued: the 8-finding "Canonical Architecture Drift Audit" brief is from 2026-08-15 and
  was fully adjudicated the same day.
  If a finding doesn't reproduce live, say so — that is a result, not a failure.
- Canon = [db-rules FEATURE.md](/systems/architecture/database/FEATURE.md); operating doctrine =
  [database-changeover-doctrine](/policies/database-changeover-doctrine.md) (measurement
  traps §4: certified-vs-all universes, `is_component` vs `rls_variant`, cached certify,
  counts are not work lists).
- The sentinels below measure the whole database on purpose. When one of them surfaces a specific
  table, say which kind of table it is before reporting it —
  [canonical-first triage](/policies/canonical-first-triage.md): deprecated is never mentioned, and a
  problem on a certified or foundation table outranks the same problem on an uncertified one.

## 1. Measure (read-only, via Supabase MCP)

Run these against live; record each number with its query framing so the next run diffs
apples to apples:

| # | Sentinel | Query sketch |
|---|---|---|
| 1 | Certification | `count(*) filter (where certified)` / total from `audit.summary` (run `select audit.refresh()` first if stale) |
| 2 | Component `created_by` policies | policies on `rls_variant='component'` active tokens whose qual/with_check mention `created_by` — **must be 0** |
| 3 | Nullable org (registered) | active `entity_types` rows whose table's `organization_id` is nullable (~34 known; diff the SET, not the count) |
| 4 | Event triggers | `count(*) from pg_event_trigger` (expect 5 platform + Supabase built-ins; **any restore silently drops them**) |
| 5 | pg_cron | `count(*) from cron.job` (restore also drops these) |
| 6 | ddl_guard_log | total, unacknowledged, and unacknowledged `hand_rolled_entity` rows + new `object_ref`s since last run |
| 7 | Versioned-without-capture | active `is_versioned` + `version_store='history'` tokens with no trigger whose **`tgfoid`** resolves to `platform._version_capture` (never match by trigger name) |
| 8 | Grant holes | tables with `authenticated` policies but no SELECT grant — check `role_table_grants` **∪ `role_column_grants`** (column-grant designs are deliberate: files/secrets/docproc) |
| 9 | RLS-off / zero-policy | `pg_class.relrowsecurity` false, or RLS on with 0 policies but live SIUD grants (the D184 class) |
| 10 | Reachability | `count(distinct refreshed_at)` (1 = recent full rebuild; several = incremental upkeep visible); run `platform.reachability_drift()` if it exists |

## 2. Diff against the last recorded state

Sources, in order: the standing report artifact (update it in place — ask Arman for the link
or use the artifact list; 2026-08-21 baseline:
`https://claude.ai/code/artifact/15a5737b-075a-4307-81a0-2e26c2e3cbc0`), the archived
08-15 adjudication, `matrx-frontend/FOUND_DEFECTS.md` (D146/D182/D184/D232 family), and the
session-memory note `project_drift_audit_adjudication`. For every worsened number, find the
cause (new tables? a lost trigger? a restore?) before reporting it. **Republish the same
artifact** — never a new URL (if it was deleted, publish fresh and repoint this line + the
memory note in the same session).

## 3. Act — this is the point

Split every open item three ways:

1. **Chip it** (default): anything a focused session can finish end-to-end — a guard, a
   gate, a bounded sweep, a ≤3-table fix. Fire `spawn_task` chips immediately. Every chip
   prompt must be self-contained: live project id + never-touch-retired rule, the canon and
   doctrine pointers, the exact end state, the non-breaking constraints, the full-change
   contract (doctrine §8a: DB + ORM + types + consumers + commit/push), and the
   retreat-cycle rule (§3a: finish forward).
2. **Split it**: too big for one session → chip the first bounded piece with a self-contained brief; never chip "do the whole backlog".
3. **Arman's list**: openness calls, machinery ratifications, schedule approvals, anything
   db-rules marks Arman-only. Direct question + your recommendation each
   (his standing format — never a doc pointer). Do NOT chip these.

## 4. Report

One message: headline numbers with deltas, what improved, what worsened and why, chips
fired (titles), decisions awaiting Arman. Update the artifact, update the
`project_drift_audit_adjudication` memory, log the run in common-docs if any doc changed.

## Known standing items (groom this list each run — remove what's done)

As of 2026-08-21 evening: the first enforcement wave is DONE and verified live (birth-gate
ERROR + provisioner marker, ddl_guard_log ack contract + readers + full triage → D232,
blocking ratchets + strict org-backstop gate, column-grant guard, component-created_by
blocking check, canon residue trio fixed, 10/11 pg_cron jobs restored,
`reachability_drift()` built, four rules in both CLAUDE.mds). All six Arman rulings are
DECIDED — NO NULL ORG ever (platform-wide, enforced at every layer) · no machinery
exemptions, fix classification instead (per-variant column contract) · batch.* is
user-visible (canonical model) · reachability check daily + self-heal. Second-wave chips in
flight: seo backstop pair + ack, last 9 versioned-without-capture, D232 residue,
component created_by neutralization, NULL-org annihilation + screamers, batch access, drift
schedule. **DONE 2026-08-21: variant-contract reclassification** — `iam.verify_canonical` v4
(db-rules §6d-3) makes the base contract per-variant, so "machinery exemption" is retired as a
concept for base columns; FAILs 799→445, certified 242→281, 42 tables fixed / 0 regressed, and
the `seo`+`runtime` families are FAIL-free. **Read §6d-3 before reading any base-column finding.** Next run: verify those landed, then groom
this list down.
