---
name: llm-gold-bound-failure-check
description: |
  Diagnose whether an LLM classifier's validation-gate failure is GOLD-BOUND
  before spending on prompt revision or model changes. Use when: (1) a scoring
  pipeline over-predicts a label (precision low, recall high) and a prompt
  clarification is proposed to tighten it, (2) a pilot/validation gate fails
  and the fix candidates are prompt edits, (3) inter-rater agreement on the
  weak label was already low (κ < ~0.6). Core check: if gold POSITIVES share
  the exact feature the revision would exclude, no prompt can pass a
  gold-scored gate — recall craters while precision barely moves. Also
  documents the verified surgical-pilot design (single-section diff,
  tune/holdout split, pre-registered gate, perturbation check on untouched
  sections).
author: Claude Code
version: 1.0.0
date: 2026-07-16
---

# LLM Gold-Bound Failure Check

## Problem

When an LLM scoring pipeline over-predicts one label, the reflex fix is a
prompt clarification ("score positive ONLY when..."). But if the gold standard
itself does not separate the texts you want excluded from the texts it labels
positive, the revision removes true and false positives together. The pilot
fails, the spend is wasted, and — worse — an un-gated adoption would have
silently destroyed recall in production.

## Context / Trigger Conditions

- A domain/label shows precision ≪ recall (e.g. P 0.46 / R 0.96) against gold
- A prompt edit is proposed to exclude a specific text type (boilerplate,
  affirmative-program language, non-risk framing)
- The label's gold council/inter-rater agreement was already the weakest
  (κ below ~0.6 is the warning sign that the construct is contested)

## Solution

**Step 0 — the ~$0 check, BEFORE building anything:** read a sample of gold
POSITIVES for the weak label and ask: do they contain the feature the revision
would exclude? Compare them side-by-side with the false positives.

- Gold positives and false positives are the same kind of text → the failure
  is **gold-bound**. Stop. No prompt passes a gold-scored gate. The levers are:
  (a) re-adjudicate the construct with the gold's owners (changes the gold,
  not the scores), or (b) re-interpret the shipped measure honestly (e.g.
  "discussion salience" instead of "risk exposure") in downstream analyses.
- Gold positives clearly differ from the false positives → a prompt revision
  is plausible; proceed to a gated pilot.

**Gated pilot design (verified):**
1. Split gold into tune/holdout halves, stratified on the weak label's
   positives; fixed seed.
2. Draft ONE surgical edit from tune-half errors only — byte-identical
   elsewhere; verify the diff reverses cleanly.
3. Pre-register the gate on the holdout BEFORE scoring: target-label
   thresholds (e.g. precision ≥ X AND recall ≥ Y) plus a perturbation
   tolerance for untouched labels (e.g. within 0.03 F1 / 0.06 κ of a
   same-serving-rev fresh baseline).
4. Score everything fresh under both prompts (same model revision, same day —
   this doubles as the drift control). Never write through the production
   cache layer.
5. Adopt only on a full pass; a REJECT is a valid, cheap outcome.

## Verification

The pilot report shows: the exact prompt diff, tune-vs-holdout metrics for
old and new prompts, per-label deltas on untouched sections, and spend.
A gold-bound diagnosis is confirmed when the revision moves recall sharply
down while precision stays roughly flat.

## Example

Specialist Directors US, 2026-07-16: DEI over-prediction (P 0.46 / R 0.96,
council κ 0.24–0.59). A risk-framing-only DEI clause was piloted ($1.17,
pre-registered holdout gate). Result: recall 0.895→0.263, precision
0.455 (gate ≥0.60) — REJECT. Reading the tune half showed ~¾ of gold DEI
positives were pure affirmative D&I program text, identical in kind to the
false positives; the failure was predictable at Step 0. Bonus finding: the
DEI-section-only edit left all five other domains within 0.025 F1 / 0.05 κ —
single-section prompt edits isolate cleanly, so the perturbation check is a
cheap add, not paranoia. Same pattern one week earlier: a cyber classifier
pilot gate failure traced to E/D gold contamination (misses were
skills-matrix-checkbox-only positives), not model weakness.

## Notes

- Low inter-rater κ on a label is the leading indicator: contested construct
  → gold-bound failures downstream.
- If the pipeline scores all labels in one completion, any post-campaign
  prompt change forces a full re-score — run this check BEFORE the campaign.
- See also: [llm-campaign-drift-gate] for the companion gate on resume
  boundaries and serving-revision drift (same fresh-baseline discipline).
- See also: [annotator-input-parity-check] — run it FIRST. If the model was
  never shown the document the annotators read, apparent gold-bound failures
  (e.g. the 2026-07-16 E/D "contamination" reading above) are actually input
  mismatch: the 2026-07-21 parity audit showed the specialist-director hand
  labels were pure proxy-statement transcriptions, so checkbox-only positives
  were recoverable from the right input all along.
