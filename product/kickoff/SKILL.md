---
name: kickoff
description: Turn a loose PRD, notes or an idea into this template's planning spine — FRAME.md (job story, the question the product answers, risks), a riskiest-assumption test, a PRD with stable IDs, week-1 decisions, and shaped milestones — ending in a readiness gate. Use at steps 1–3 of SLIPWAY.md, when the user says "kick off", "start the project", "here's my PRD", or when `pnpm status` says the frame or shape is unfinished.
---

# Kickoff

Steps 1–3 of the slipway path (`SLIPWAY.md`): **Frame → Test the risk → Shape.** Output is files in this repo,
never a chat summary. One question at a time; the user owns every answer.

Before anything: run `pnpm status` and read it. If it reports a later step, say so and stop —
kickoff is not a way to re-plan a running project (that is a new milestone, via
`docs/milestones/TEMPLATE.md`).

Read, in this order and nothing more: the user's input, `docs/product/FRAME.md`,
`docs/PRD.md`, `decisions.md`, `docs/milestones/TEMPLATE.md`,
`docs/milestones/M1-walking-skeleton.md`. Search `process/lessons/` for anything touching
planning (`grep -l -i "plan\|scope\|acceptance\|decision" process/lessons/*.md`) and apply
what is there.

## Rules

- **Ask, one question per message.** Offer 2–4 concrete options with a recommendation when
  you can. Never ask what the input already answers.
- **Nothing invented.** Anything the user has not said and you cannot derive goes into the
  file as `[NEEDS CLARIFICATION: <question>]`, never as a plausible guess.
- **Constraints vs preferences.** When the user states something, ask only if it is unclear
  which one it is (L-39).
- **Stay under a page per artifact.** FRAME is one page; each milestone is one screen.
- Write each file as soon as its phase ends, so the user can read and edit it.

## Phase 1 — Frame (`docs/product/FRAME.md`)

Work through, in order:

1. **The moment.** "When does someone reach for this?" Get a situation, not a persona.
2. **The job story.** Draft "When …, I want to …, so I can …" and have the user correct it.
   The outcome is a change in their life, not a feature.
3. **The question it answers.** One line, in the user's words — e.g. for a dog walkers'
   scheduling app: "Where do I need to be tomorrow, and who hasn't paid?" Test it: every feature in the loose PRD
   either serves this question or is marked for later. Show the user that sort.
4. **Four forces.** Push, pull, anxiety, habit. Push hard on habit: what do they do today,
   precisely? That is the competitor.
5. **Non-users.** Who is this deliberately not for?
6. **Press release and hard questions.** Draft them; the user edits. If the release cannot
   say why this beats the habit, stop and say so — the idea is not ready.
7. **Risks.** List 4–8 assumptions that could kill it, each tagged value / usability /
   feasibility / viability / ethical. Rank by impact × how little evidence exists. Then, for
   each **value** risk, one question per message:
   1. "Do you test this, or does experience already settle it?"
   2. If experience: "Which is it: table stakes, you are the user, or domain expertise?" These
      three, no other. The Result reads `experience: table stakes`, `experience: creator is the
      user` or `experience: domain expertise`.
   3. "What would prove it wrong?" Write the answer verbatim as a `Wrong if:` line in its
      evidence file (`docs/product/evidence/RISK-n-<short>.md`). No answer, or "nothing": the
      risk is not settled; clear the Result and treat it as a test.

   For a test, propose the cheapest one — interviews about past behaviour, a concierge run
   done by hand, a fake door — and ask the user for the **Threshold** before anything runs.
   Leave Result empty. Never propose a rationale or a refutation: both are the user's words.

Write FRAME.md with `status: draft`. When no placeholder or clarification remains, ask the
user to confirm, then set `status: framed`.

## Phase 2 — Test the risk (`docs/product/evidence/`)

You cannot run interviews; the user can. Produce what they need:

- an interview guide: 6–8 questions about specific past behaviour ("tell me about the last
  time you…"), no pitching, no "would you use";
- a results table and the threshold, copied from FRAME, dated today;
- for a concierge test: exactly what the user will do by hand, for how many people, for how
  long;
- nothing for a risk settled by experience: no interview guide, only its `Wrong if:` line. A
  `Wrong if:` that comes true reopens the risk: clear its Result and test it;
- the issue that runs the test, once the user agrees to run it: put its number in FRAME's Tracker
  column and a `Tracked: #n` line (with `Window:`) in the evidence file. `pnpm status` then shows the
  risk as scheduled, and K1 requires the tracker for every untested value risk once the skeleton is
  active.

Tell the user plainly: **no milestone past the walking skeleton can start until each value risk has
a Result, is settled by experience with what would prove it wrong written down, or has a decision
in `decisions.md` to build ahead of it with that decision's id in the risk's Result.** The skeleton may be built in parallel
with the test. When results come back, record them in FRAME's Result column and in
`evidence/`; if the threshold was missed, the options are reframe (back to phase 1) or proceed
anyway with a decision in `decisions.md` that says why.

## Phase 3 — Shape

1. **PRD (`docs/PRD.md`).** Fill it from the input and FRAME: stable IDs everywhere (PRIN-,
   F-, OD-, RISK- reused from FRAME). Features that do not serve the question in FRAME go to
   §4 *Out, explicitly* with where they go. Every open decision gets a working assumption and
   impact-if-wrong; only business-invalidating ones are BLOCKING.

   **When the input is a source document** (a loose PRD, a brief, notes with their own risks),
   fill §3 *Source coverage* before moving on: name it on the `Source:` line (path or link, and
   its version), then walk the source top to bottom and give every risk,
   spike, invariant and blocking decision one row — **kept** (with the new ID), **moved** (with a
   DIV-n saying where and why) or **dropped** (with a DIV-n saying why). A dropped item is fine; a
   missing row is not, because nobody can tell it was dropped on purpose. Never write "handled by
   the features above": name the ID that handles it. With no source document, write
   `Source: none`.
2. **Week-1 decisions (`decisions.md`).** Walk the entries marked *(week 1)*. For each: decide
   with the user, or defer with the event that reopens it. These are the expensive-to-reverse
   choices; do not let one slide into month three. Once D-005–D-008 are decided, rewrite the
   `Stack:` line at the top of `CLAUDE.md` to state the decided stack — agents read it first.
3. **Story map (PRD §10).** Lay the user's journey left to right as 3–6 activities, taken from
   FRAME's job story; put the §5 features under the activity each serves. Draw slice lines
   across: the first is the walking skeleton (the thinnest path across the *whole* journey, not
   one activity done fully), the next answers FRAME's question for a handful of real users, the
   next is what it takes to charge or launch. Rank with the written rule — riskiest open
   assumption first, then dependencies, then value — and record why each feature sits on its
   line. Show the map to the user and let them move features between lines before going on;
   anything below the last line moves to §4 *Out, explicitly*.
4. **Milestones (`docs/milestones/`).** One per slice line. M1 is always the walking skeleton —
   fill its placeholders with this product's thinnest core path. Every Contents item cites the
   F-IDs it builds, or says `(no feature: <reason>)`; every §5 feature is cited by some
   milestone (F1 enforces both once the PRD leaves draft). Each milestone gets an appetite (days or weeks, not a date guess), vertical
   slices, no-gos (move most of the loose PRD here), rabbit holes, a gate that can go red, and
   kill criteria written now, and a one-line `summary:` in its frontmatter. All stay
   `status: shaping`.

   Then **generate** PRD §10's milestones table from the files — one row per milestone, in
   order, `| <id> | <kind> | <summary> |` copied from the frontmatter (a `|` in the summary is
   written `\|`) — rather than writing the
   one-liners a second time. MS1 flags a row that differs from its `summary:`. When a one-liner
   needs to change, change the `summary:` and regenerate.

   Fill the PRD's estimates (§9) the same way: a `Capacity: <n>–<m> h/week` line from the user — the total for
   everyone building, not per person (ask; never guess it) — and one row per milestone with its hours as a range and what they are made of. MS1 warns
   when a milestone's midpoint is more than its appetite holds (appetite days ÷ 7 × the top of
   Capacity). Show the user any warning and let them cut scope, lengthen the appetite or
   re-estimate — do not quietly shrink the estimate to fit.
5. **Readiness gate.** Re-read M1 and M2 as the engineer who must build them. For each slice
   ask: can it be built without inventing a decision nobody recorded? Report:

   ```
   Readiness: PASS | CONCERNS | FAIL
   - <slice>: <decision that would have to be invented> → recorded as an open question in the PRD (OD-n) or a decision in decisions.md
   ```

   Every concern becomes an OD- in the PRD (with a working assumption) or a PD- entry in decisions.md. FAIL
   means a BLOCKING question is open; say who must answer it.

## Hand-off

1. Bump the PRD `Version:` and add a change-log line.
2. **Set up the adversarial review, then stop.** Copy `docs/reviews/TEMPLATE.md` to
   `docs/reviews/<YYYY-MM-DD>-prd-<version>.md` with the two provenance lines already filled in —
   `Reviewed: docs/PRD.md @ <short sha>` and the `Version line:` copied from the PRD — and leave the
   register empty. Commit it with the rest. Then tell the user, in these words:

   > Open a **new** session and run `/review-doc docs/PRD.md`. It fills
   > `docs/reviews/<file>`. This is the document review, not a code review of the PR, which
   > reads a diff and writes nothing here. The build goes red once the PRD leaves draft with no
   > review naming its current version.

   Do not run it yourself: this session wrote the PRD, and a reviewer must not share the author's
   context.
3. Run `pnpm meta` and `pnpm status`; paste both. `status` should now point at step 4 or at
   the risk test.
4. Commit on a branch and open a PR whose `## Verification` shows those two outputs.

Stop there. Starting M1 is the user's call: they set its appetite dates and `status: active`.
