---
name: critic-loop
description: Run an independent critic loop on generated work that is not code or a plan — images, renders, ASCII or canvas art, video stills, frames and shorts, covers, copy. A fresh-context critic scores each round against a rubric written before round 1, starts with a blind read (it says what it sees before it is told what was intended), lists every gap, and the loop stops on a threshold, a stall rule or a round limit. Use when asked to "critic loop", "have a critic score this", "get an independent critic", or before showing generated visuals or copy to the owner as ready. For code, see codex-review; for implementation plans, see plan-review-loop.
user-invocable: true
argument-hint: "<artifact paths | batch dir> [--rubric <file>] [--threshold 8] [--max-rounds 5] [--critics 1|2] [--refs <paths>] [--id <name>]"
metadata:
  version: "1.1.0"
---

# Critic Loop

An independent critic for generated work. The producer makes the work; a critic that has
never seen the producer's reasoning judges it; the producer revises; the loop stops by
rule, not by feel.

**Core principle:** the producer's own check is not a review. An agent that drew a ram
believes it drew a ram, and grades the picture with that belief. Only a critic that has
not been told what the picture is can say whether it shows one.

## When to use, and when not

- Use for anything whose quality is judged by looking or reading: stills, renders,
  contact sheets, video frames, covers, ASCII or canvas art, UI screenshots judged as
  pictures, captions, short copy.
- Code changes: `codex-review`. Implementation plans: `plan-review-loop`. Whether code
  meets its intent: `verify-change`.
- Skip it for a trivial change to work that already passed. Zero rounds is a valid
  outcome; say so.

## Lifecycle

```
rubric → round: packet → blind read → scored verdict → triage → revise → … → stop rule → report
```

Records live in `reviews/critic/<id>/` in the target repo: `rubric.md`, `round-<n>.md` per
round, `summary.md` at the end. They are the only state; there is no hook. If the project
already keeps review evidence somewhere (for example a short's
`docs/research/<date>-<slug>/` with `review-r1-sol.txt`), put the records there instead and
keep the same file roles.

## Phase 1 — Rubric, before round 1

Write `reviews/critic/<id>/rubric.md` **before the critic sees anything**. A rubric
written after looking at the work bends to fit it.

The rubric holds:

1. **The brief:** what the work must show or say, in one or two sentences, and its
   viewing condition (phone at feed size, a 120-column canvas, a 9:16 cover crop). Add
   the owner's standing taste and past verdicts on earlier versions where they exist;
   they are part of the brief, so the critic gets them after the blind read.
2. **Categories**, in one of two forms. Start from the matching rubric in
   [rubrics.md](rubrics.md) and change it to fit the work. Every category names what a
   full score looks like.
   - **Total:** categories with maximum scores totalling 10; the round passes on the total.
   - **Per dimension:** each dimension scored 1–10 on its own; the round passes only when
     every applicable dimension reaches the threshold. Use this when the project scores
     that way (a production-rules file that says "every applicable rating at least 8").
   Name the dimensions the artifact cannot show yet — motion and sound cannot be judged
   from stills. They are recorded as **PENDING**, never scored, until a moving, audible
   test exists.
3. **Blocking conditions:** failures that block a pass at any score — the blind read
   names a different subject; essential text is unreadable at the viewing size; a
   content rule from the project is broken.
4. **Threshold** (default 8), **max rounds** (default 5).
5. **References** (optional): reference examples the owner or the style chose — a style
   guide's sample images, an approved earlier short, the owner's verdicts on past
   versions. They are part of the brief.

If the project has its own rule for a critic (a production-rules file, an ADR), read it
and follow its threshold and gates; it overrides these defaults.

Show the owner the rubric when the work is new or the rubric is new. Do not wait for an
answer to start; record that it was shown.

## Phase 2 — The packet

Each round's critic is a **fresh** agent. Choose the backend from
[../codex-review/reviewer-backends.md](../codex-review/reviewer-backends.md): Codex CLI,
then opencode, then context-blind subagents. A critic of pictures must receive the
pictures:

- Codex CLI: `codex --sandbox read-only exec -i <png> [-i <png> …] --output-last-message "$ROUND_FILE" "<prompt>" < /dev/null`
- opencode: `opencode run --pure --agent inkstone-reviewer -f <png> … "<prompt>" < /dev/null`
- Subagent: give it the image paths and tell it to read them.

A backend that cannot take images is skipped for visual work; log why. Record the critic
as tool **and** model, and say when it is the same model family as the producer.

The packet contains, and only contains:

- the artifact (images, frames, text) at the size it will be seen;
- the rubric, **with the brief held back for the blind read** (Phase 3);
- the references, given with the brief after the blind read;
- from round 2: the previous round's artifact and verdict, and a one-line list of what
  changed. Not the producer's reasons for the changes.

For video, the artifact is frames, not the producer's description of them — see
[Video and shorts](#video-and-shorts).

Never send the producer's conversation, its notes on what it was trying to do, or its
own assessment. Those are the reasoning the critic exists to be free of.

Use [critic-prompt.md](critic-prompt.md) for the prompt.

**Two critics** (`--critics 2`, or when the project asks for it): run two fresh critics
from different model families on the same packet, each blind to the other (for example
a Claude subagent and Codex CLI on a GPT model). The round's total is the **lower** of the
two — per dimension, the lower score in each; a blocking condition from either blocks. Changes both
critics ask for go first; a finding only one raises is still dispositioned.

## Phase 3 — Blind read

The critic first answers, from the artifact alone: **what does this show (or say)?** Name
the subject, the action and the mood, as a stranger would.

Only then does it receive the brief, and compare. A blind read that names a different
subject is blocking, whatever the scores — a lake that reads as two eyes has failed,
however good its ripples are.

For text, the blind read is: what is this saying, and to whom?

## Phase 4 — Scored verdict

The critic scores each category, may use halves, and **lists every gap that keeps each
category from full marks**, each one specific enough to act on ("the horns merge into
the hedge at cells 40–55", not "the ram looks off"). It totals out of 10 and ends with a
verdict: `PASS`, `REVISE` or `RETHINK` (the approach cannot reach the threshold by
adjustment; say what to change).

Rules the prompt gives the critic:

- Be exact and do not soften. A regression scores lower than the round before.
- Stay consistent with the previous verdict, but you are not bound to match or raise its
  score.
- Ignore preferences that do not affect whether the work meets the brief.
- A fixed bug does not by itself earn a higher score. Score the work as it now is.
- Do not score a PENDING dimension, and do not infer it from what is shown.

With two critics, record each critic's scores and reasons separately in the round file,
then the combined result; never only the combined number.

The round's record is `reviews/critic/<id>/round-<n>.md`; check it exists, is non-empty
and names the critic before accepting it.

## Phase 5 — Triage

The producer judges every finding and records one line per finding under
`## Disposition` in the round file:

- **ACCEPTED** — will change it this round.
- **DECLINED** — with the reason (e.g. "deliberate: the brief asks for night; the critic
  wants it brighter").

A critic is confidently wrong sometimes; a producer who accepts every finding did not
read them. A blocking condition cannot be declined — only met or escalated to the owner.

Write each accepted finding as a revision note: where (a timestamp or frame number for
video, cells or coordinates for a still), one change, and the visible result expected.
Fix the largest gaps first; where the project says how many per round (the studio's
"fix the three worst problems and repeat"), fix that many and no more, so the next round
can tell what helped. Re-render the same samples after the fixes, so the critic compares
like with like.

## Phase 6 — Stop rules

After each round, in this order:

1. **Pass:** total ≥ threshold, no blocking condition, every finding dispositioned →
   stop. Notes the critic left that were declined stay in the record.
2. **Stall approaching:** the best total has not risen a full point in 2 rounds, or the
   critic names the same gap twice in a row → no more adjustments. Rethink: a different
   composition, subject treatment or structure, then run the next round on that.
3. **Stalled:** the rethink scores the same or lower → stop and ask the owner whether
   the current best is good enough, with its round file.
4. **Round limit:** max rounds reached → stop and report the best round and its open
   gaps.
5. Otherwise: revise and run the next round.

Keep the best-scoring version; a later round that regressed does not replace it.

## Video and shorts

A critic cannot watch a video through most backends; it gets frames. Extract them from
the file that will be delivered (after any cover, bookend or compression pass), not from
a preview render:

- **Frame zero:** `ffmpeg -i delivery.mp4 -frames:v 1 frame-zero.png`, plus the profile-grid
  crops the platform uses (the studio: centre 1:1 and 3:4). The cover and the frames that
  follow it (the studio: frames 30–50) are scored as their own items.
- **Beat contact sheet:** one frame per beat on the beat grid, labelled with its time.
- **Shot states:** the first, middle and last frame of each shot.
- **Action strips:** consecutive frames around each important action and each cut, so a
  contact error or a jump shows.
- **Crops:** full-resolution crops of faces, hands, feet and object contacts.

Send them at phone size as well as full size. Motion and sound stay PENDING until the
critic is given a moving, audible test it can judge (or the owner judges it); say which.

Where the project defines its own dimensions (hook in the first 2 seconds, phone
readability, motion, variety, brand accuracy, sound sync; for a series, its own
replacements), use them as the per-dimension rubric. See [rubrics.md](rubrics.md).

## Batches

For many artifacts (a set of 64 scenes, a contact sheet of beats):

- One rubric for the set, with a per-item brief. A short's cover, exit and body can be
  items of one batch.
- One critic per item, each fresh. Do not let one critic score a set and drift across it.
- Run a first round over every item, then loop only the items that did not pass.
- `summary.md` holds a table: item, best total, rounds, verdict, open gaps.

## Report

Lead with: the verdict, the rounds run, the best total (or each dimension's best score),
the critic (tool and model, same-family or not), and any PENDING dimensions. Then the open gaps of anything that did not pass, then the paths of
the records and the final images. Never call a piece passed on the producer's own check.

## Rules

- Rubric before round 1. Brief held back until the blind read.
- A fresh critic every round; never the producer's reasoning in the packet.
- The critic sees the work at its real viewing size; video as frames from the delivery
  file.
- PENDING dimensions are never scored from stills.
- Every finding gets a disposition; blocking conditions are met or escalated.
- Stop by the stop rules; a pass is not approval to publish or merge — the owner's gates
  still apply.
- On a tooling failure, report it and say plainly that the round did not run.
