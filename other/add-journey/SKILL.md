---
name: add-journey
description: >-
  Onboard NEW journeys into the journey_v1 corpus (the executor-ready format-v4
  journey brain) so they inherit every accumulated quality lane — JC waves,
  adversarial-verify fixes, Ramco review classes — by running the standing
  idempotent pipeline. Use this skill whenever the user asks to "add a journey",
  "update the brain with journeys", "onboard a new activity/module journey",
  "extend journey_v1", or when new activities/components need journey coverage.
  Canonical runbook: journey_v1/_build/NEW_JOURNEY_PROCESS.md (this skill is its
  executable form). Everything is idempotent over the whole corpus — re-running
  any step is always safe.
---

# Add a journey — the standing onboarding pipeline

All paths relative to `D:/Users/O185005/Documents/ERP/journey_v1` unless noted.
Run python as `python -X utf8` (Windows, UTF-8 JSONs). A journey is NOT part of
the served corpus until step 7 is green and step 8 has run. **Never leave the
result uncommitted** (the 2026-07-08 data-loss incident).

## 1 · Backbone
- Prefer `_build/gen_journey_v1.py` when the P7 pipeline inputs exist; else
  hand-build on the `_build/gen_scminq_backbone.py` pattern — entirely from the
  trace CSV `ramco-erp-brain/berp-general/general/Process_Comp_Act_Task_services/<Comp>.csv`
  (real activity/ILBO/task/service names; init/fetch/get/UI-cascade/help tool spine).
- **EXTJS-pack slot inventory is MANDATORY when the component ships an EXTJS6
  pack** (`berp-*/<bpc>/<Comp>/EXTJS6/<screen>.json` — 560 components do): derive
  the slot set from the pack's input controls, not from SP parameters. The thin
  trace-CSV-only backbone is allowed ONLY when no pack exists, and the omission
  must be disclosed in `provenance.gaps` ("EXTJS pack not consulted/approximated").
  The parity gate (step 7) enforces this.
- Must satisfy `format.json` (v4). Non-obvious requirements that bit before:
  `post_options: []` is required; tool `purpose` and slot `data_type`/rule
  `kind`/`bucket`/basis `kind` must be in the format enums; `on_fill` is an ARRAY;
  `post_conditions.output_variables` entries are objects; every tool needs
  `execution_path`; `thin_slot_view` mirrors slots. Inquiry-class journeys: ALL
  filter slots `obligation: optional` (validator 7.2) — requiredness lives in rules.

## 2 · Depth mining (rules from raw SPs)
- `Workflow{scriptPath: _build/depth_wave.js, args: ["<module>/<file>.json", ...]}`
  (args must be a real JSON array), then bank:
  `python -X utf8 _build/bank.py --output <task.output> --launched <targets> --tag <runid>`.
- Every rule cites raw `SP.sql:line`; dead raises + err=None success-returns excluded.
- Additions are durable in `_build/_additions/` — the recovery source of truth.
- **Payload-leak tripwire (2026-07-10):** agents sometimes serialize part of their
  return INTO the notes string (`<parameter name="new_rules">[...]`) and the
  top-level field arrives empty — bank.py WARNS on the pattern; when it fires run
  `python -X utf8 _build/recover_leaked_payloads.py` (report, then `--apply` +
  merge_depth). Never ignore it: 168 rules + 2 commit fixes were once silently lost.
- Resume protocol on limit stalls: `_build/_WAVE_STATE.json` (see memory
  jc2-depth-wave-resume). ONE workflow per reset window.

## 3 · The standing fixer chain — run after ANY merge/bank, IN ORDER
```
python -X utf8 _build/apply_commit_fix.py --additions <bank.json>  # NEVER skip — the lost-lane incident
python -X utf8 _build/normalize_recovery.py     # enum/tsv/untyped normalization
python -X utf8 _build/fix_template_deps.py      # FC-9 inferred-dep cleanup
python -X utf8 _build/fix_mismsg2.py            # (msg:) vs the P-XLSX error registry
python -X utf8 _build/fix_hygiene.py            # dedup + re-key + MANIFEST REGEN
python -X utf8 _build/fix_invariants.py         # class-vs-content (AFTER manifest)
python -X utf8 _build/prune_dangling_rule_slots.py
```
Trap: if a `commit_fix` proves the journey persists while classed `inquiry-report`,
reclass to `lifecycle` BEFORE `fix_invariants` (else 7.2 strips the commit options
— the 2026-07-08 circularity).

## 4 · Review-class conformance (the accumulated Ramco-review lanes)
`python -X utf8 _build/review_july6_sweeps.py`, then verify the invariants:
- **Commit provenance:** every commit option originates from THIS activity's own
  screens (the Express-PO class — foreign pipelines are `navigation`/linked).
- **Labels = task truth:** option/intent match Model_XML/trace-CSV `task_desc`
  (the PoEdtEntTrn2 Edit-vs-Delete class).
- **No hidden commits:** business-DML save-family tools (FC-3 oracle,
  `vercel_deploy/brain_chatbot/data/sp_writes.json`) are `purpose: commit` with an
  option (the Amend-Return class); fetch-page SPs with del/ret fragments are NOT.
- **Lifecycle:** carried display-only identity slot on the main screen; grounded
  discriminators only (entry filters = `entry_search_filter`); obligations follow
  SCREEN truth for fetched headers; fetch-first elicitation.
- **Create-only leak:** create-worker rules with only create* finish paths on a
  non-create journey get `{path:<real>, enforced:false, reason}` markers.
  Standing detector: `_build/_lint_create_only_leak.json`.

## 5 · Donor parity (only if the journey exists in ERP1)
`python -X utf8 _build/reaudit_vs_erp1.py --assert-zero` (whitelist W1–W8 +
JC-6 verdict-archive routing). New `w3_absent_jc6`/`w4_absent_jc6` counts =
un-adjudicated donor knowledge → run a JC-6-style adjudication batch
(`_build/jc6_wave.js` + `_build/jc6_bank.py` pattern).

## 6 · Enrichment parity
Target the corpus standard (reference shape: `purchase/po_create_direct.json`):
activation gates, obligation_basis, valid_values, on_fill cascades, CW-7
tables_written evidence, CW-8 tax adjudication if the chain touches vat/tcal,
E15 linked_journeys. Most arrive via the depth wave + overlays.

## 7 · Gates — ALL green before serving
```
python -X utf8 _build/verify_v4.py        # 0 SCHEMA / 0 REFERENTIAL / {} executor
python -X utf8 _build/validate_all.py     # only declared G-48 fails allowed
python -X utf8 _build/audit_corpus.py     # D1=0, FAB=0
python -X utf8 _build/reaudit_vs_erp1.py --assert-zero
python -X utf8 _build/check_journey_parity.py <module>/<file>.json   # PARITY GATE
```
The **parity gate** makes "as comprehensive as the corpus" pass/fail: P1
EXTJS-grounded slots (or disclosed), P2 depth-wave ran, P3 every rule grounded,
P4 activation overlay when the register has rows, P5 obligation_basis on
mandatories, P6 a real commit/output surface. A dimension passes by MEETING the
bar or by an honest `provenance.gaps` disclosure — never silently. Calibration:
1,579/1,634 of the existing corpus passes (the 55 fails are the corpus's own
tracked tail, not gate noise).

## 8 · Downstream + durability
1. In `vercel_deploy/brain_chatbot`: `node --max-old-space-size=8192 scripts/build_index.js`
   (default heap OOMs past ~2,300 journeys — the 2026-07-10 FS close; a crashed
   build leaves index.json written but build_manifest.json STALE — check
   `built` freshness) +
   `node scripts/build_grep_index.js`; bump `CACHE_VERSION` in `src/answerCache.js`;
   restart the server (kill `node server.js` workers, relaunch, health-check
   :5173/api/health); `npm run check` (journey-count test self-adjusts from the
   manifest).
2. Refresh the coverage tracker + report:
   `python -X utf8 info_data/journey_status/build_journey_status.py`
   (regenerates `journey_v1/status.json` — the done/pending activity tracker —
   plus the CSV/HTML coverage report; the new journey flips its activity to done).
3. **Commit immediately** (journey_v1 + chatbot data/ + status.json) and push;
   update `_build/_WAVE_STATE.json`. **ALWAYS `git add <paths>` BEFORE a
   pathspec-scoped `git commit -- <paths>`** — pathspec commits include tracked
   modifications but SILENTLY SKIP untracked new files (the 2026-07-10 FS
   incident: 78 new journey files sat uncommitted through two "wave commits").
   Verify with `git status --short -- journey_v1 | wc -l` == 0 after committing.

## 9 · KG + journey-brain delta (once the KG is built)
Follow `kg_plan/KG_PLAN.md` §KG-NJ (NJ-1..NJ-8): corpus stamp → `gen_kg.py` re-run
(node/edge delta; view journeys re-anchor capability rows, `capability_id` stable;
alias map re-resolves) → KG-G-29 backlog row closed + versioned answer-key fixture
flip → formula gates (golden fixtures never regress) → journey-brain/chia serving
refresh → commit + push. KG scope law: the ENTIRE 13-module corpus, never
P2P-scoped. Until the KG exists, steps 1–8 complete on their own.

## Quick reference
```
backbone → depth-mine + bank → fixer chain (3) → review sweeps + invariants (4)
→ donor reaudit (5) → gates (7) → rebuild + restart + COMMIT + PUSH (8) → KG delta (9)
```
