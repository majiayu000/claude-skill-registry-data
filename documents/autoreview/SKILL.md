---
name: autoreview
category: governance
description: |
  Unattended multi-lens review of a plan, launch plan, spec, strategy doc,
  ADR or proposal. The autonomous counterpart to grill-with-docs: instead of
  interviewing the human, the agent asks the grilling questions itself and
  answers each one from evidence (repo docs, code, tickets, meeting notes,
  chat, live systems). Five review types run in a fixed order: drift (is every
  stateful claim still true, and was anything decided after the doc was
  written), grill (walk the decision tree, answer from evidence, keep a
  glossary and ADR candidates), ownership (every workstream and dependency has
  an owner, ticket and date), premortem, and a cross-model adversarial round
  scored on the FINAL text. Only the residue, decisions no reachable evidence
  can settle, goes back to the human, batched once, each with a recommended
  default. Use when the user asks whether a plan is "ready", "fully
  developed", "reviewed", "grilled", "adversarially verified", or says
  "review this autonomously", "grill it yourself", "run all the reviews",
  "autoreview", "/autoreview". NOT for a code diff alone (use code-review or
  cross-review) and NOT when the user wants to be interviewed live (use
  grill-with-docs).
---

# autoreview: every review type, run unattended

`grill-with-docs` asks the human every question. `autoreview` asks the
evidence first and brings the human only what the evidence cannot decide.

## Why this exists

Origin, 2026-09-24. The question was *"is the launch plan fully developed,
grilled with docs, and adversarially verified?"* Assembling the answer by hand
took an hour, and it was **no** on all three counts, each for a reason the
other reviews could not have caught:

- **Adversarially verified, but not the text that shipped.** The plan had
  passed three refutation rounds (4/10, 4/10, 7/10). The four fixes made after
  round 3 were never scored. A score binds to the text it read.
- **Correct on its date, stale a day later.** It was written the day before a
  founder check-in that changed its sign-up policy, its pricing scope and its
  launch checklist. No refutation round could see that: a reviewer shown only
  the document cannot see what was decided after it. Drift is its own review.
- **Never grilled, and it could not have been.** `grill-with-docs` delegates to
  `/grilling` and `/domain-modeling`, neither of which was installed, and it
  needs a person answering in real time.

The first run of this skill on that plan found about 20 stale or wrong claims,
14 later decisions it did not reflect, and 20 launch workstreams with no owner.
It also caught three of its own subagents overstating a fact: a mislabelled
ticket, a 301 reported as a 200, and a production failure attributed to the
wrong region. That is why the spot-check rule below exists.

Each review type is blind to a class the others catch. That is why this runs
five of them instead of the strongest one.

## The five review types

| # | Lens | The question | Catches | Blind to |
|---|---|---|---|---|
| 1 | **Drift** | Is each stateful claim still true, and was anything decided after the doc's date that it does not reflect? | stale statuses, answered questions still listed as open, superseded decisions | whether the plan is any good |
| 2 | **Grill** | For each decision branch: what is the answer, and where is it written? | vague commitments, undefined terms, decisions assumed but never made | facts that changed after the evidence was written |
| 3 | **Ownership** | Does every workstream and dependency have an owner, a ticket and a date? | unowned dependencies, dates with no path to them | whether it is the right work |
| 4 | **Premortem** | Six months on, this failed. Why? | risks the plan never names | risks it names but mis-sizes |
| 5 | **Refutation** | Can a fresh evaluator, ideally different weights, break it? | argument gaps, wrong numbers, unsupported claims | anything outside the text it is shown |

**Order is load-bearing.** Drift before grill, so you do not grill against stale
facts. Refutation last, so it scores the text that ships, and it is shown the
drift findings so it can see past the document's date.

If the artifact is a code diff, lens 5 is `/cross-review` on the diff and lenses
2 to 4 apply only to the design question behind it.

## Procedure

### 0. Frame, before any lens

- Pin the artifact: path, and the commit or content hash of the exact text.
  **Every finding and every score in the run binds to a hash.**
- Name its date, its decision owner(s), its audience, and what "ready" means
  for it: who acts on it, and by when.
- Build the evidence set: the artifact's own citations, the canon it claims to
  follow, and **everything dated after the artifact that touches its subject**
  (meeting notes, tickets, commits, chat, answered asks). For each source, note
  what it can and cannot see.
- **Write the evidence set to one file and hand every lens the same file.**
  Lenses that each gather their own evidence disagree about what is true, and
  the disagreement looks like a finding.

**Run order.** Lens 1 finishes first, and lens 3 rides with it because it
reads the same tables. Fold lens 1's STALE and CONTRADICTED findings into the
evidence file, then run lenses 2 and 4 in parallel against that updated file,
so neither can answer from a claim drift has just invalidated. Lens 5 waits
for every patch.

### 1. Drift

For every claim that carries state (a status, owner, number, date, "open",
"done", "no ticket", "we can", "we cannot"), re-read it from the system of
record and mark it:

- **CURRENT**
- **STALE**: was true, no longer is
- **CONTRADICTED**: the evidence says otherwise, now or at the time
- **UNVERIFIABLE**: name the instrument you would need

Then sweep the post-date evidence for decisions on the artifact's subject. Each
one the artifact does not reflect is a finding **even if no sentence in it is
literally false.** An AI meeting summary is a summary: cite it as "the <date>
summary says", never as words a person said.

### 2. Grill: the autonomous grill-with-docs

Walk the decision tree the way a relentless interviewer would: goal, success
criteria, scope and non-goals, sequence, dependencies, risks, cost, who
decides. One branch at a time; follow each answer to its next question until
the branch bottoms out. Classify every question:

- **ANSWERED**: the evidence settles it. Cite it (`path:line`, ticket id,
  message permalink, query).
- **GAP**: the plan should say it, does not, and the evidence does. Patch the
  plan and cite the evidence.
- **RESIDUE**: only a person can settle it: a value judgment, an authority, an
  external party, money. **Do not answer it.** Record the question, why no
  evidence can settle it, your recommended default, what it gates, and who
  decides.
- **BLOCKED**: the answer is a fact that exists somewhere, but this run cannot
  reach it: a permission denied, an expired login, an outage. It is not
  residue, because nobody has to decide anything. Retry once. Then name the
  instrument and the exact failure, and carry it to the report's blind spots.
  A load-bearing BLOCKED keeps the verdict at NOT READY until it is reached,
  or until an owner accepts the risk in writing. An acceptance already on
  record is ANSWERED, with its citation; one not yet given is RESIDUE.

The test for RESIDUE is not "I am unsure", and not "I could not reach it". It
is "this is a choice, not a fact: no document, system or measurement could
settle it even with full access." A lookup you skipped is not residue, and
neither is one that failed.

**A decision may already have been made.** Before filing any decision as
RESIDUE, search the evidence set for a record that it was taken: a meeting
summary, a ticket, an answered ask, a commit. A decision already taken is
ANSWERED, with the citation, even if nobody wrote it into the artifact. That
case is also a drift finding. The launch plan this skill was built on listed
its date as an open choice; the owners had picked it the day after it was
written.

The "with docs" half runs alongside and produces two side outputs:

- **Glossary**: every term the artifact uses in two senses, or that two sources
  define differently. One line each, with the sense the artifact should use.
- **Decision records**: each decision the grill found already made but written
  nowhere durable, drafted as an ADR candidate. Write it into a repository only
  where that repository's conventions let an agent do so; otherwise hand it back
  as a file.

### 3. Ownership and dependencies

Table every workstream and external dependency: owner (a person, not a team),
ticket, date, and what it blocks. A missing column is a finding. An unowned
dependency inside a dated plan is how the date slips without anyone deciding to
slip it.

### 4. Premortem

Run `/premortem` in autonomous mode: fill its context-gathering step from the
evidence set instead of asking, generate failure reasons, and deep-dive the
strongest in parallel subagents. Keep only the reasons that change the plan: a
mitigation, a gate, a cut, or an early signal with a date to check it.

### 5. Refutation, last

1. **Apply every patch from lenses 1 to 4 first.**
2. Refute the patched text with `/spec-contract` for every document type this
   skill takes: `--profile plan` for a plan or strategy document, `spec` for
   a spec or proposal (`rfd` where the repository keeps RFDs), `adr` for an
   ADR. `spec_check.py <path to the patched text> --profile <profile>` must
   exit 0 on that exact file, then its five-axis
   rubric, pass at ≥11/15 with no axis at 0. Keep `spec-contract`'s two
   escalations, which a total alone hides: **R1 = 0** (a one-way door
   committed silently) stops the document, and **R2 or R4 at 1 or less** means
   the design is unargued. Report that as a structural finding, because
   rewriting prose will not raise it. For code use `/cross-review`.
3. **Name the stratum from model identities, not from the tool.** Record the
   writer's model and the evaluator's model. **Stratum A** requires different
   weights: `codex exec -c sandbox_mode=read-only` qualifies only when Codex
   did not write the document. Otherwise it is **Stratum B**, a fresh context
   on the same weights, recorded as **provisional**.
4. Hand the evaluator the lens 1 findings as well as the document.
5. Act on every objection, or dismiss it with a stated reason.
6. **Re-score. The last scored round must have read the exact text you hand
   back.** A fix made after the last score is unreviewed, however small.
   Record each round in the ledger **before** the next round runs, so the
   reviewer also sees the claimed fixes and can check them against the body.
   Keep the ledger in a **sibling file** (for example `<artifact>.review.md`)
   by default, so the bytes scored and the bytes handed back are the same. If
   the repository's convention puts it in an appendix instead, the only edit
   allowed after the final score is that round's own ledger entry, and the
   report names both hashes: the text scored, and the text with its ledger.

**Round budget.** Take the round *counting* from `/cross-review` (three free
rounds, rounds 4 to 7 earned only by a continuation verdict that names a
located, checkable defect, 8 or more a human's call), but **not its pass
mark**: its 7/10 is for code. A design round passes only on `spec-contract`'s
rule above. To log a design round with `cross-review round record-round`,
decide pass or fail with `spec-contract`'s rule first, then pass `--score` as:

- a **passing** round: the total scaled to ten and rounded down
  (`total × 10 / 15`; 11/15 logs as 7, 12/15 as 8);
- a **failing** round: the same, **capped at 6**. The budget script treats a
  score of 7 or more as passed and closes, so without the cap a round at
  11/15 that fails on R2 or R4 would close the budget on a failure.

Write both halves with their scale — `--score=N/10` and one
`--stratum=L:N/10:PASS|FAIL` per stratum carrying the stratum's own
`spec-contract` verdict. The ledger refuses a raw `/15` score and any bare
integer (BRO-2615), and it refuses a round of 7 or more over a stratum marked
FAIL -- so the cap is enforced for every stratum you record. It cannot see a
stratum you leave out: a failing stratum omitted from `--stratum` is not
detected, which is the writer's assertion, same as `--strata`.

Pass `--defect=yes` when the round located at least one checkable defect in
the text (a contradiction, a wrong number, a gate that cannot be checked as
written), `no` otherwise. Two consecutive `no` rounds stop the budget, which is
right: a score that stays low without a locatable defect is a structural
problem, not a wording one. Keep `R1..R5` and the unscaled total in the
ledger. When the budget
is spent without a pass, stop: do not keep editing. Record the last round's
objections as open, and the verdict follows the output contract.

### 6. Report

Deliver the output contract below. Write the review ledger to the sibling file
from step 5.6, or to an appendix where the repository requires one. **Draft only: never send, post, publish or forward anything.**

## Output contract

1. **Verdict**, decided by the first rule that matches:
   - **NOT READY** if any of these holds:
     - the final text was never scored, or its last round failed;
     - the last round scored R1 = 0, or R2 or R4 at 1 or less;
     - `spec_check` does not exit 0;
     - a STALE or CONTRADICTED claim is unpatched;
     - a load-bearing claim is UNVERIFIABLE or BLOCKED and no owner has
       accepted the risk;
     - a dependency on the critical path has no owner;
     - any finding from any lens has no disposition. Every finding ends as
       patched, residue, BLOCKED, dismissed with a stated reason, or a named
       blind spot.
   - **READY WITH DECISIONS**: none of the above, and only residue remains.
   - **READY**: none of the above, and no residue.

   Add **(provisional)** to READY or READY WITH DECISIONS when the last score
   came from Stratum B only. A missing Stratum A is a blind spot (item 7), not
   residue: nobody has to decide anything about it.
2. **Text reviewed**: path and hash in, hash of the final text out.
3. **Findings per lens**, each with one disposition from the same list the
   verdict rule uses: patched, residue, BLOCKED, dismissed with a reason, or a
   named blind spot.
4. **Scores**: every round, the hash it read, and its stratum.
5. **Residue**, numbered. Each one names the question, why evidence cannot
   settle it, a recommended default, what it gates, and who decides. This is
   the only part the human has to act on.
6. **Glossary and ADR candidates.**
7. **Blind spots**: what this run could not see, and the instrument that would
   have seen it.

## Rules

- Evidence over recall. Every ANSWERED carries a citation.
- Do not ask what you can look up. Do ask what you cannot decide.
- Never answer a residue on its owner's behalf, even when the answer looks
  obvious. Make it the recommended default; the owner decides.
- Two instances of one brief agreeing is one reading, not corroboration.
- **A lens subagent's fact is a claim until you check it.** Before a fact from
  a subagent goes into the artifact, re-run its instrument yourself for every
  load-bearing one. Relaying it is asserting it.
- A score binds to a hash.
- Nothing leaves the workspace.

## Rationalizations to refuse

| Excuse | Reality |
|---|---|
| "It was already adversarially reviewed." | Which text? Anything changed after the last scored round is unreviewed. |
| "Nothing in it is false." | Drift includes what was decided after it was written. A true, stale plan still misleads the people acting on it. |
| "I'm not sure, so it's a question for the user." | Uncertainty is not residue. Look it up; only what no reachable evidence can settle goes back. |
| "The fixes were small." | Small unscored fixes are exactly how a 7/10 document ships text no reviewer read. |
| "The reviewer agreed with me." | Same weights share blind spots. A Stratum B score is provisional. |
| "I'll ask each question as it comes up." | That is grill-with-docs. Batch the residue once, at the end, with defaults. |
| "The owner will obviously pick X." | Then X is your recommended default. It is still their call. |
| "The premortem found nothing new." | Then say which named risks it confirmed and which signal you would watch. "Nothing" is a finding only with its search stated. |

## When not to use

- The user wants to be interviewed live: `/grill-with-docs`.
- A code diff with no design question: `/code-review` or `/cross-review`.
- An idea with no plan yet: help plan first, then review.

## Composition

| Skill | Role here |
|---|---|
| `premortem` | lens 4 |
| `spec-contract` | lens 5 for plans, strategy documents, specs, proposals and ADRs |
| `cross-review` | lens 5 for code, and the round budget everywhere |
| `kg` | building the evidence set where a knowledge graph exists |
| `handback` | delivering the residue when the owner is away |
| `grill-with-docs` | the interactive alternative; run it on the residue if the owner wants to talk it through |
