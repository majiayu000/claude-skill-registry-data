---
name: annotator-input-parity-check
description: |
  Before designing, training, or auditing ANY model that replicates
  human-annotated labels, audit the annotation protocol's INPUT — the exact
  document/evidence the human labelers consulted — and give the model that
  same input. Use when: (1) designing a classifier/LLM extractor whose target
  is a hand-coded label set, (2) a label-replication model shows low recall
  concentrated in a label subset and the diagnosis on offer is "the label's
  information is not in the features", (3) reviewers propose construct splits
  (e.g. "designation vs record-evident"), adjudication sittings, or per-domain
  stop rules to explain residual disagreement with gold, (4) validating an
  extraction pipeline against labels transcribed from a source document.
  Symptom of the underlying failure: elaborate theory accumulates to explain
  why gold is "partially unpredictable" when the model was simply never shown
  the document the annotators read.
author: Claude Code
version: 1.0.0
date: 2026-07-21
---

# Annotator Input Parity Check

## Problem

A model built to replicate human labels is fed a different evidence base than
the one the annotators used. The mismatch masquerades as a modeling or
construct problem: recall collapses on the label subset whose evidence lives
only in the annotators' source, audits produce increasingly sophisticated
theory ("invisible" positives, construct splits, per-domain reliability
gates), and successive model generations inherit the wrong input because each
review critiques the lineage from inside the frozen input assumption.

## Context / Trigger Conditions

- Starting any label-replication build (classifier, LLM scorer, extractor)
  against hand-coded gold.
- A validation report says some share of gold positives have "zero signal" in
  the model's input.
- Proposals appear for: construct splits (what the model CAN see vs what the
  label encodes), human adjudication of "contested" cells, stop rules
  excluding weak domains, or accepting a permanent accuracy ceiling.
- Verified instance (Specialist Directors US, 2026-07-21): three classifier
  generations (bio-BERT AUC 0.5 → structured RoBERTa "unclassifiable" on 3/5
  domains → LLM dossier scorer with E/D construct split + PI adjudication +
  per-domain stop rules) all read director bios + BoardEx records, while the
  RA labels were pure transcriptions of PROXY-STATEMENT disclosures (skills
  matrices + bios, no exogenous data — confirmed in the source paper's
  methodology, 41 Yale J. Reg. 652, 669-72). The "invisible specialist" mass
  (43-79% of some domains) was simply the skills-matrix checkbox content the
  models were never shown. Years of downstream apparatus dissolved once the
  question "what did the labelers actually read?" was asked.

## Solution

1. Before any design work, write down the annotation protocol as the
   annotators executed it: source document(s), what they could see, what they
   could not, whether any exogenous data entered. Get this from the
   codebook/paper methodology section, not from folklore. If the protocol is
   unwritten, ask the PI directly: "did labelers consult anything beyond X?"
2. Compare against the model's planned input. Any evidence the annotators had
   that the model lacks is a hard recall ceiling on exactly the labels that
   evidence determines — no architecture, prompt, or training fixes it.
3. If a mismatch exists, prefer restoring input parity (give the model the
   annotators' document) over modeling around the gap. For transcription-style
   protocols, the task then becomes extraction, not prediction, and validation
   against the hand labels becomes construct-matched (agreement should be
   high; disagreement means extraction bugs, not construct philosophy).
4. Only if input parity is impossible (annotators used private knowledge,
   interviews, paywalled data) is a construct split the honest design — and
   then the model's output must be named as a DIFFERENT variable, never
   graded raw against the full gold.
5. When auditing an EXISTING lineage: ask the parity question first, before
   critiquing rubrics, thresholds, or gold quality. An audit that inherits the
   input assumption can be internally excellent and still miss the dominant
   error term.

## Verification

- The protocol-input inventory exists in writing and the model input is a
  superset of it → recall ceilings from "invisible" labels should disappear;
  residual disagreement decomposes into extraction errors (fixable) rather
  than unknowable-label mass.
- Quick falsification test for a claimed "unpredictable" label subset: pull 5
  such gold positives, open the annotators' source document for each, and
  check whether the label is visible there. If yes, the problem is input,
  not construct.

## Notes

- Distinct from [llm-gold-bound-failure-check], which diagnoses gold that
  fails to SEPARATE classes for a proposed revision; this skill diagnoses
  model INPUT that omits the annotators' evidence. Run this parity check
  first — gold-bound analysis of a parity-broken system wastes effort.
- The mismatch is self-perpetuating across model generations: each successor
  inherits the predecessor's feature pipeline, and each audit optimizes
  within it. Breaking the frame requires asking about the ANNOTATORS, not
  the model.
- Construct splits built on a parity-broken system may still have salvage
  value for a different question (e.g. record-evident-but-undisclosed
  expertise is analytically interesting in its own right) — reframe, don't
  necessarily discard.
