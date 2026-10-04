---
name: sync-brain-source
description: >-
  Onboard a batch of NEW or CHANGED Ramco source files into the Brain — the end-to-end
  playbook that runs WHENEVER a `git pull` of `ramco-erp-brain/` lands new/changed files,
  a new folder/BPC/artefact-class appears, or the user says "sync the brain", "a git pull
  brought new data", "ingest the delta", "new files were added to the source, update the
  brain", or "the source changed — reflect it". This is the DELTA ORCHESTRATOR: it detects
  the change set, documents it, classifies every path, and routes each class through the
  `reindex-brain` skill (§A/§B/§C), then proves no regression with the `eval-brain` skill
  before anything becomes visible. It composes those two skills — it does not replace them.
  Governing rule (inherited): every change is a strictly additive, non-regressing positive
  delta; the current Brain is pre-eminent; nothing is deleted, no prior answer regresses.
---

# Syncing a source delta into the Brain (additive, gated, no regression)

A `git pull` of the immutable raw repo (`ramco-erp-brain/`) periodically lands new files
(a new artefact class, more of an existing source, a whole new BPC) or refreshes existing
ones. This skill turns that raw delta into Brain content **safely and repeatably**. It is
the *orchestration* layer; the *mechanics* live in **`reindex-brain`** (how to add one
thing) and the *proof* lives in **`eval-brain`** (how to grade without regressing).

> Prime directive (from `reindex-brain`): **positive delta, never regress.** Raw is
> read-only; registers are run-id'd and never clobbered; the `accepted` pointer advances
> **only** on a full gate pass; a new BPC adds coverage scope but **never a new wiki
> ontology**.

## The 7-step loop (run in order; each step gates the next)

### 1 · Snapshot the delta (git facts)
- Record `HEAD` before/after, commit list, and `git diff --stat HEAD@{before}..HEAD`
  (added / modified / deleted counts; disk footprint). Deletions in raw are rare and must
  be handled as **provenance-tagged supersedence**, never as a Brain deletion.
- Flag any **new top-level `berp-*` folder** — that is a **new BPC/module tier** (new
  coverage scope + a domain-model note in `CLAUDE.md` and `git_walkthrough.md`), not a new
  page type.

### 2 · Document it (human-readable inventory) — *before touching the Brain*
- Update **`git_walkthrough.md`** (§3 top-level map, §6 `berp-general` table, §7 A/B/C
  cross-ref, §9 gaps) with the new folder-by-folder counts.
- Write a dated **`git_new_addion.md`**-style delta addendum: commit-by-commit attribution,
  per-folder counts grounded in the working tree, and the gap-registry impact.
- *(These two artefacts are the audit trail; produce them even for small deltas.)*

### 3 · Classify every changed path → change shape × artefact class
For each new/changed path decide (a) the **reindex-brain change shape** and (b) whether it
hits an **existing parser glob** or needs a **new class**:

```
More of an existing source (same shape, new dirs) ....... §A GLOB WIDENING (disjoint recount)
A brand-new structured artefact class ................... §A NEW PARSER  (parser_plan_v2 class row)
A binary/prose the LLM must read, not a parser .......... §A HYBRID / LLM-DIRECT (container shim only)
A new relationship the data now supports ................ §B CROSS-CONNECTION (extend an edge generator)
The Brain already has it — chatbot just can't surface it. §C PROMPT / TOOL (cheapest — try first)
```
Dispatch by **magic bytes, not extension**. A new BPC = many §A classes (per-component
loop) + a domain-model note. Never invent an orphan page type.

### 4 · Route each class through `reindex-brain`
Invoke the **reindex-brain** skill per class, honoring its section:
- **§A** — parser mode decision → inherit the output contract (run-id'd JSONL, header
  `counts.in/out/skipped_named`, named residuals, golden-file suite) → **acceptance
  discipline** (golden reproduction → LLM spot-audit ≥5 files → gate pass → *then* the
  `accepted` pointer) → `build_runmaps.py` → re-run generators (idempotent).
  *Glob widening:* prove the new glob is **disjoint**, recount per BPC so
  `old_total + new_disjoint = new_total` with the delta enumerated, tag new sub-classes,
  re-run **only the newly-included dirs**.
- **§B** — extend one of the five edge generators (`gen_cim_cardinality` /
  `gen_sp_callgraph` / `gen_reverse_indexes` + `gen_cross_fk` / `gen_journey_index` /
  `[[wikilinks]]`); resolve by basename; every emitted link must resolve.
- **§C** — append (never contradict) a rule/tool in `brain_chatbot/src/prompt.js` or
  `tools.js`; rebuild the BM25 index.

### 5 · Sequence the work (run-anytime vs gated vs barrier)
- **Run-anytime (P8.0):** glob widenings, named-skip enumeration, prose refresh — they only
  ADD and break nothing. Do these first.
- **Gated (P8.2–P8.9):** classes that consume V1 registers; fan out per gap.
- **Barrier (P9):** after all classes land, re-run dependent overlays (journeys / a2ui /
  migration / rules-semantics), rebuild the BM25 index, then the Regression Gate.

### 6 · Regression Gate (mandatory — use `eval-brain`) before advancing any pointer
- `check_links.py` → 0 dangling `[[links]]`, 0 unreconciled A2UI packs.
- `verify_journeys.py` → 0 schema-invalid, 0 dangling refs.
- Every touched batch's `gates.json` → all pass; count sums reconcile.
- **Re-run the Layer-1 eval via `eval-brain`** vs the last accepted baseline: FULL% and
  answerable% **must not drop**; **no previously-FULL question may regress**; new coverage
  only *adds* FULL answers. Apply eval-brain's grading rules (drop malformed/two-word
  questions; a superset of the gold is CORRECT, not a hallucination). Diff per-question
  verdicts, not just headline %.
- Spot-check 3–5 previously-good questions → unchanged or better, same citations.

### 7 · Record & institutionalize
- `status.json` — open/close `gaps[]` with the **run that changed them**; bump parser /
  generator versions; a closed gap keeps its record (never overwrite).
- `log.md` — append the run history.
- `git_walkthrough.md` / `CLAUDE.md` — apply the domain-model deltas (e.g. an 11th BPC).
- Only on all-green: advance the `accepted` pointer. If any prior answer regressed, **do
  not advance** — the prior baseline is your rollback until the regression is fixed.

## What this skill will NOT do (guardrails)
- Never write into `ramco-erp-brain/` (raw is immutable).
- Never delete a register run, overwrite a good run with an ungated one, or merge two
  sources so a prior row disappears — all forbidden (they regress the Brain).
- Never advance the `accepted` pointer without a green Regression Gate.
- Never simplify or skip the acceptance discipline "to save time" — a bad run must stay
  `.FAILED` and invisible, not be patched into the wiki.

## Related
- **`reindex-brain`** — the per-change mechanics (§A/§B/§C, the 8 non-regression devices).
- **`eval-brain`** — the grading harness the Regression Gate calls.
- **`ramco-journey`** — regenerate journeys for components a delta touched.
- Canonical process docs: `brain_plan/master_plan.md`, `brain_plan/V2/master_plan_v2.md`,
  `brain_plan/parser_plan.md` (+ `V2/parser_plan_v2.md`), `brain_plan/status.json` (gaps).
