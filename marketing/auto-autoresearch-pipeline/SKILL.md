---
name: auto-autoresearch-pipeline
description: >-
  Run a long autonomous optimization campaign on a scored artifact (circuit, proof,
  packing) as a role-separated pipeline: one director, parallel area-owning workers,
  an independent paired verifier, a fail-closed integrator, and a compiled-screen
  grinder. Use when many small candidate edits compete for a leaderboard score and
  no single worker can be trusted to measure its own work.
whenToUse: Setting up or auditing a multi-agent benchmark campaign loop, or when candidate measurements from different workers must be compared without contamination
---

# Fliessband (auto-autoresearch-pipeline)

Distilled from haotang1995's "Auto-AutoResearch" harness (two accepted ecdsa.fail
record submissions, 2026-10-29). The pattern took the board in one day; it is
route-agnostic and reusable for any scored artifact.

## Roles — separate them, no exceptions

1. **Director.** Assigns disjoint research areas and owns the idea log. Never edits
   the artifact. Areas are named by *region of the stream* (divide walk, multiply
   walk, history, width), not by technique, so two workers never touch the same rows.
2. **Workers.** One area each. Every candidate ships with: a change note, a **paired
   measurement against its own parent** (same shots, same seeds), and an
   approximate/exact classification. A candidate without all three is not queued.
3. **Independent verifier.** A *separate* worker re-measures every queued candidate
   on fresh shots paired against the current leader — never trust the producing
   worker's numbers. Price conservatively: charge the paired SE and a minimum
   multi-event floor against the claimed delta. Effects smaller than the verifier's
   SE must be re-measured by the worker at 4–16× shot count before they count.
4. **Integrator.** Stacks only qualified leaves, using **predeclared, frozen
   compositions**. Content-keyed matching of edited bodies; fail-closed where an
   edit does not match; **no resampling and no new policy at merge time**; re-verify
   the merged stream before it becomes the leader.
5. **Grinder.** Compile the screening filter *from the final artifact stream* so the
   screen is never hand-written per candidate. The screen is a filter, never the
   judge: only an exact-evaluator pass counts.

## Idea-log discipline

- Log every **start and finish** with an ID per ingredient (their log: E193…E300).
- Failed attempts are first-class entries with the failure mode named
  (UNSAT / timeout / byte-identical / overfit) — timeouts are never recorded as
  impossibility.
- Items with no recorded completion are explicitly unclaimed; the submission note
  says so.
- A positive control that reproduces the parent stream exactly travels with every
  structural claim.

## Submission note contract

State the harness and models, the parent commit, the measured table with seeds and
shot counts, the lambda (failure-rate) position, what is proven vs measured, the
failed-attempt list, and which queued improvements were deliberately excluded.

## Anti-patterns this prevents

- Worker-measures-itself optimism (independent verifier kills it).
- Merge-time rescue edits (frozen compositions kill them).
- Hand-tuned screens drifting from the stream (compiled screens kill that).
- Silent failure debt (the idea log + unclaimed-item rule kill it).
