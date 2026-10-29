---
name: clone-check
description: Decide whether a finished build is a clone of one already shipped, the way the final_verdict reviewer decides it. Carries the discrimination the check turns on (reusing a proven component is legitimate, reusing the thing that drives the stump is not, and the prompt shape is a component), the two tracks a finding can land in and why they carry different severity, the tier ladder, and the ways the check itself gives a wrong answer. Use when asked for a clone check, a template check or a duplicate check, when a batch is about to be submitted, and as a pre-flight on a build whose draw is fixed but whose data is not yet cut.
---

# Clone check

> Two builds are not the same task because they share a device. They are the same task when the thing a
> solver has to see is the same thing.

## Part 0. What this is for

The final_verdict reviewer excludes a package that fingerprints against anything delivered, and the client
has said these builds read as templated. The question is whether a reviewer holding both builds learns
nothing new from the second, which is about the driver, not the surface. The check reports at the
severity a reviewer would attach and never repairs; a clone is answered by a redraw, which is the
author's.

**Where it runs.** Every build runs the free half, `guard.py heart` and `guard.py surface`, at stage 3. The
adjudicated check (the `clone-auditor` agent, medium effort) runs only when the author asks, through
`/clone-check`, because it spends tokens. The corpus baseline is `corpus/fingerprints.json` (tracked); the
working cache under `.cache/` is seeded from it and never committed. The author refreshes the baseline on a
checkout holding every pack: `fingerprint.py extract --out .claude/skills/clone-check/corpus/fingerprints.json`. The mechanical screen is `fingerprint.py extract` then
`fingerprint.py screen` (default the last 15 builds), whose **hard tells** (byte-identical files, same-seed
tables surviving a rename, identical column sets, shared multi-word invented names, masked prompt wording)
route straight to adjudication.

## Part 1. The discrimination

- **Reusing a component is legitimate; reusing the driver is not.** A proven device is meant to be spent
  again. The driver, the one insight the solver has to reach, is what a reviewer remembers and a solver
  can be primed against. Familiar moves in a new order with a new decisive move is a new task; new moves
  arriving at the same insight is the old task reskinned. A similarity score ranks these backwards, so the
  check is never a score.
- **The stumping strategy is not a component.** Different drivers can share a strategy (a withheld rule
  under an official decoy; a certified record blessing the wrong method until a forward condition breaks
  it). The client names the first as about 40 percent of what it receives and rejects replicated
  approaches, so a strategy carrying a large share of a batch is a finding even when every pair is clean.
- **The prompt shape is a component** (`guide-to-prompt/references/shapes/`): it supplies the 25 criteria
  and will repeat. Score a shared shape as Track A; escalate only when it hides the same decisive rung.
  It is very visible, so vary it across a batch and check it in pre-flight.
- **Read the position, not the inventory.** A device decisive in one build and at rung 1 in the other is
  demoted, which is reuse. Decisive in both is spent twice, whatever the surface distance.

## Part 2. Two tracks, never merged into one score

**Track A, what a reviewer sees:** prompt wording, file names, schemas, row counts, values, invented names,
dated windows, deliverable species, write-up phrasing. A Track A hit against a delivered task is exclusion
level by itself. The repair is a rename, not optional. Run
`../guide-to-prompt/references/voice-check.py` bare on a batch first: the script measures the surface
(question forms, repeated phrases, length, file count, format mix) and this skill adjudicates. A
monoculture spread thinly is invisible pair by pair and obvious in the counts (eighteen prompts, no two
clones, one skeleton).

**Track B, the mechanism:** gap, pattern, decisive rung, calibration form, decision family. A hit means the
draw failed; the repair is a redraw that usually invalidates the data, so catch it early. Check the
mechanism axes independently, never behind a surface threshold: a fully reskinned surface over a repeated
driver scores near zero on surface and is the worst case.

## Part 3. The tiers, by cost to answer

| Tier | What it is |
|---|---|
| **Exact** | The same artifacts. |
| **Same seed** | Renamed surface over the same generated values (row counts, column sets, numbers survive). Reads as hiding. |
| **Dataset** | The same spine dataset or schema; banned between consecutive builds (`stumping` Part 6). |
| **Template** | The same driver: gap, pattern and decisive rung line up whatever the nouns. The tier the client's note was about, and the only one surviving a full rename. |
| **Shape echo** | Different mechanism, same outline (ask sentence, deliverable species, decision shape, calibration organ). Soft flag. |
| **Idiom** | Author habits across the corpus (a file role, an ask construction, a deliverable pairing). Corpus wide, reported apart from pairs. |
| **Strategy monoculture** | Read each card's `stump_strategy`, `decisive_rule_filed`, `official_decoy`, `validated_decoy` (design notes for older builds). A finding, builds named, when the withheld rule with an official decoy exceeds two in any twelve, the certified-record decoy exceeds three, or any one strategy holds a third of the batch. Corpus wide. |
| **Clean, shares components by design** | A verdict, stated out loud when devices are shared and drivers differ, so the author keeps reusing what works. |

## Part 4. Evidence that is not there

Read the fingerprint cards first (`../fingerprint/cards/`): one vocabulary, a domain-stripped driver
sentence, and `mechanism_source: submission_only` where the mechanism was never recorded. Back-fitted labels
are accurate about the mechanism and approximate about the name, so two builds sharing one share a guess.
Where the mechanism cannot be read, report the pair as checked on Track A only. A driver reconstructed
from a prompt is a fabrication and sends an author to redraw a sound build.

## Part 5. How the check goes wrong

- **Flags legitimate reuse.** Proximity is not a finding; no Template finding without the shared decisive
  move named in one sentence.
- **Misses the reskin.** The mechanism axes need their own route to adjudication.
- **Scores instead of deciding.** A number is triage; the verdict comes from reading both builds.
- **Treats the corpus as flat.** A collision with a delivered build excludes; with a failed or retired
  build it is weaker; with the slot's own earlier architecture it is not a finding.

## Part 6. What a finding carries

The tier, the track, the two builds and both delivery statuses, the shared thing stated as a mechanism in
one sentence (or it is not a finding), and the one axis to redraw. Say when a finding is Track A only:
the repair is a rename, not a rebuild.
