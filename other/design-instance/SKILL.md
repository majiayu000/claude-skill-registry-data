---
name: design-instance
description: Map the Scholar method onto a new domain. Interviews the owner through the eight configuring questions (goal, unit, fidelity ladder, status axis, vocabulary, gates, roles, evaluator), starts from the closest existing instance spec, checks the design against the method's non-negotiables, and writes instances/<name>/INSTANCE.md and instance.yaml with a one-chunk pilot plan and a cost estimate. Use whenever someone wants to apply the scholar to a new corpus or problem. Triggers on "new instance", "apply the scholar to", "map this domain", "design a scholar for".
---

# Design an instance

## Step 1: find the closest existing instance
Read `instances/README.md`. Pick the one or two closest specs and read them fully. Say which you picked and why, in one sentence each.

## Step 2: interview through the eight questions
Ask one question at a time. Offer the closest instance's answer as a starting point. Do not accept a vague answer; each question has a test.

| # | Question | The answer passes when |
|---|---|---|
| 1 | **Goal:** what are we trying to establish, for whom, and what is off limits? | It names a holder (so "for" and "against" mean something) and a finished deliverable |
| 2 | **Unit:** what is the smallest thing a conclusion can cite, and how is it located? | A locator exists that a program can resolve back to exact text |
| 3 | **Fidelity ladder:** what counts as read from the source? | At least one confirming grade is not agent output; recollection and agent summaries never confirm |
| 4 | **Status axis:** may a unit be used at all? | There is a resolver (rule or adapter) that decides status per unit, and "unusable but true" is possible |
| 5 | **Vocabulary:** what framework do the experts judge by? | It is transcribed from an authoritative source with a location; issues crosswalk to it |
| 6 | **Gates:** what must the database refuse? | Each gate names a table, field, value and required evidence, and has a reject probe and an accept probe written out |
| 7 | **Roles:** who attacks, judges and audits? | At least one adversarial role and one decision-maker role; the auditor has graded verdicts |
| 8 | **Evaluator:** what fixed test decides whether the system is right or improving? | It has a mechanical part agents cannot edit; a real outcome is named if one exists |

## Step 3: check the non-negotiables
Refuse to finalize until all hold:
- [ ] Coverage is provable (every unit labeled once; validator planned).
- [ ] Important labels carry verbatim quotes checked by a program.
- [ ] Gates live in the datastore and each has both-way probes.
- [ ] Fidelity and status are separate axes.
- [ ] Negative results have a place (ruled_out, refuted, rejected) and are never gated.
- [ ] Outcomes of attempts and attacks live on edges.
- [ ] Bulk ingest writes artifacts only.
- [ ] Lenses are projections; nothing is copied per reader.
- [ ] Human-owned files are listed (gates, ladders, evaluator, privacy).
- [ ] Privacy: deny list outside the repo; allowed providers named; no client data in engine files.
- [ ] Licensing of any borrowed material recorded.

## Step 4: choose modules
List each module from `docs/MODULES.md` as "as-is" or "adapter needed" (and describe the adapter), plus optional modules (staleness for mutable corpora; discovery for hypothesis generation).

## Step 5: write the files
Copy `instances/_template/` to `instances/<name>/`. Fill in `INSTANCE.md` (all 13 sections, synthetic examples only) and `instance.yaml`.

## Step 6: pilot plan and cost
- **Pilot:** one chunk end to end:
  1. intake
  2. labels
  3. validator self-test (planted misquote and missing label must fail)
  4. load
  5. one gate with probes
  6. one lens
  7. one role run
  8. two-labeler agreement sample
- **Cost estimate:** units × tokens per unit. The reference point is about 810 subagent tokens per unit for full expert reading with validation (instance 1: about 7.4M tokens over 9,101 units). Adjust down for status-aware skipping and tiered routing, and state the assumptions.

## Step 7: report
Summarize for the owner:
- the eight answers
- what is unusual about this domain
- the adapters to build
- the pilot steps
- the cost estimate
- the open questions

Record decisions in `docs/DECISIONS.md` if they change the method.
