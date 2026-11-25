---
name: assistant-verification
description: "Analyzes and selects proportionate testing, validation, or evaluation for a change, or assesses whether existing evidence is sufficient across code, skills, plugins, and non-code artifacts. Use on request, and before the first edit of any non-trivial feature, fix, refactor, migration, or skill change, including after plan approval, review feedback, CI failures, or resuming, even when assistant-workflow or assistant-debugging has already loaded. Not for running an existing test command or tests-first requests (assistant-tdd)."
---

# Verification Selection And Evidence Assessment

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.


Choose the smallest credible checks for the requested outcome, or assess whether
supplied evidence supports it. This skill selects and assesses; it does not run,
dispatch, repair, retry, edit, or approve delivery.

## Method

1. Identify the change, acceptance claims, affected boundaries, and plausible
   wrong outcomes. Read relevant existing checks and results before adding work.
2. Separate binding requirements, preferences, and capability limits. Preserve
   exact mandate sources; do not waive a required check or invent a universal
   count, ratio, coverage target, or test quota.
3. Preserve explicit reduced-testing scope/source in the existing scope and
   source-ref fields and an instruction row in `evidence_assessment`, not only preferences; use [selection.md](references/selection.md)
   for that boundary and controlling-check conflicts. Choose checks for distinct material claims. Reuse adequate current evidence;
   add tests only for a real uncovered behavior or failure. Zero new tests still
   needs evidence and meaningful exclusions. Choose scope, technique, and TDD
   independently; meaningful RED is required only when TDD is active.
4. Assess assertions, source/config identity, freshness, results and limits.
   Phrase/schema/file-existence passes prove structure, not behavior/model quality.
   Missing, failed, partial, stale, skipped and unavailable evidence remains gaps.
5. Stop with credible evidence for binding checks/material claims; expand only
   for new gaps, changes, failures, material risks, requests or mandates.

For disputed policy/coverage/cost/TDD use [selection.md](references/selection.md);
for reused/ambiguous/incomplete evidence use [evidence-quality.md](references/evidence-quality.md).
Load only the considered method:
[unit](references/methods/unit.md), [integration](references/methods/integration.md),
[end-to-end](references/methods/end-to-end.md),
[artifact validation](references/methods/artifact-validation.md),
[behavioral evaluation](references/methods/behavioral-evals.md),
[property/mutation](references/methods/property-and-mutation.md), or
[performance/resilience](references/methods/performance-and-resilience.md).

Load `lifecycle` and [lifecycle guidance](references/lifecycle-verification.md) only
for affected lifecycle claims; exclude synchronous/cosmetic-only work.

## Consumed results

Human-only assessments can concisely state checks/evidence, conclusion, gaps
and next action without serialization.
When workflow, skill-creator, a carried decision, or an executable consumer needs
structured results, load `contracts/index.yaml` and the applicable entry,
selection/assessment, current-phase, and completion sets. Missing/invalid selectors
load the full named contract. Preserve canonical `verification_decision`
(CheckSpec/TddChoice) and `evidence_assessment` unchanged; do not create a task-state
file or replacement schema. Human summaries need not dump these full objects.

For command checks, retain exact ID/argv/cwd. Bind result rows only to the selected
IDs and exact `{kind,value,source_ref}` obligations their observed procedure
supports. Preserve explicit required metrics/scopes/thresholds through an enforcing
CheckSpec or report a policy gap and block dependent Build.

Selection without results is planned; a requested assessment without adequate
results is insufficient or blocked. Sufficient closes the named scope and due
checks, with exclusions; it does not establish independent review or delivery
approval. assistant-debugging owns unknown causes, assistant-tdd owns active TDD,
and domain specialists retain their rules.
