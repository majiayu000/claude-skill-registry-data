---
name: jev
description: Delegate a repeated decision to Jev, TypeSafe AI's System One model, instead of deciding every item yourself or spending a Claude agent on it. Use when the same yes/no (or choice, or score) judgment is made over many items with the answers known up front, such as triage ("does this bug break play?"), routing, gating, labelling, or spotting duplicates. Not for code, reviews, or anything that needs a written reason.
---

# /jev: delegating decisions to Jev

Jev does not write text. It takes a **state** (a JSON object) and a typed question, and returns a
calibrated probability that code can branch on: a smart `if` for conditions code cannot compute.
It answers in well under a second, for a fraction of a cent (vendor figures).

## Does the job fit? All five must hold

1. **Repeated.** The same question is asked of many items: dozens now, or every session.
2. **Closed.** The answers are known up front (yes/no), and the action for each is known.
3. **It fits in a state.** An item is a small JSON object, such as an issue's title, body and labels.
4. **Cheap to be wrong at the ends.** A wrong answer at a confident end costs less than you
   deciding every item, and a person can still overturn it.
5. **Cleared to leave.** The content may be sent to a third-party API. Ask the user before
   sending anything from a private repository for the first time.

Not Jev's:
- code (OpenCode);
- reviews and anything that needs a reason (Claude);
- anything a script can compute (file lists, the fix-lane test);
- a one-off decision.

## The procedure

1. **Define.** Add the decision to `harness.json` under `jev.decisions`:
   `{"type": "noul", "instructionsFile": "docs/jev/<name>.md"}`. The instructions say:
   - what the state is;
   - what yes means, and what no means;
   - the confusing cases, and which side they fall on.

   `docs/jev/breaks-play.md` is an example.
2. **Label.** Collect at least 60 items with the right answer, as JSONL lines of
   `{"id", "state", "label": true|false}`.
   - The best labels are decisions people already made: issue labels, triage outcomes, merged or
     closed.
   - Labels you make yourself measure Jev against you, not against the truth. Use them only if
     the user agrees, and say so in the record.
3. **Trial.** Run `node tools/harness/jev.mjs trial --decision <name> --in labels.jsonl`. It picks
   each end's cutoff on half the labels and reports it on the other half.
   - Adopt the cutoffs only if the held-out precision holds and there are no warnings.
   - Record them in `harness.json`: `autoYesAt`, `autoNoBelow`, and a `trial` object with the
     date, the model, the held-out counts, precision and coverage.
   - Commit with the numbers in the message.
   - An end without a cutoff stays yours.
4. **Route.** Build `items.jsonl` (for issues:
   `gh issue list ... --json number,title,body,labels --jq '.[] | {id: .number, state: {title, body, labels: [.labels[].name]}}'`),
   then run `node tools/harness/jev.mjs route --decision <name> --in items.jsonl --out routed.jsonl`.
   - Act on the `yes` and `no` rows, and say on each item that Jev decided it and with what `p`.
   - Decide the `middle` rows yourself.
5. **Keep it honest.**
   - A person's decision always outranks Jev's.
   - When the user overturns a Jev answer, add the item to the labels.
   - Re-run the trial when the model pin or the instructions change. The cache is keyed on both,
     so a rerun asks again.

## Exits

- **0**: done.
- **1**: refused (an untrialled decision), or stopped by a provider failure. The answers so far
  were written and cached; decide the rest yourself, or rerun later.
- **3**: Jev is off (no key, or no `jev` section). Decide every item yourself, as before.

`ask` returns raw answers for any question type. `trial` and `route` handle `noul` only, until the
response formats of Choice and Score are confirmed.
