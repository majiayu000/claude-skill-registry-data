---
name: meeting-notes
version: 1.0.0
description: Turn a raw transcript or scribble into decisions, action items with owners and dates, and open questions - so nothing agreed in the room evaporates afterwards.
triggers:
  - meeting notes
  - clean up these notes
  - structure this transcript
  - action items from this meeting
  - what did we decide
capabilities: []
inputs:
  - name: transcript
    required: true
    description: Raw transcript, chat log, or rough notes from the meeting.
  - name: attendees
    required: false
    description: Names/roles present, to help attribute owners correctly.
---

# Meeting Notes

## When to use
Use this when you have a raw transcript, chat log, or rough scribble from a meeting and need the three things that matter afterwards: what was decided, who does what by when, and what is still open.

**Not for:** verbatim minutes required for legal or governance records (those must capture everything, not a distillation); real-time note-taking during the meeting; or a transcript so fragmentary that no decision or owner can be identified - flag that rather than inventing structure. Do not use it to editorialize on who performed well.

## Method
1. **Read the whole transcript once** before writing anything, so you know how debates resolved before you summarize them.
2. **Extract decisions.** *Decision point:* record something as a decision only if someone actually agreed to it in the text; proposals that got no agreement go under Open Questions, not Decisions.
3. **Extract action items:** task, owner, date. *Decision point:* if no one was assigned, write "owner: UNASSIGNED" loudly rather than guessing a name; if no date, "by: not set".
4. **Attribute carefully.** Never put words in a named person's mouth; when the speaker is unclear, write "someone raised".
5. **Keep disagreement visible.** If someone objected and was overruled, note it in one line - that context matters a month later.
6. **Write a two-line summary at the top** for people who were not there. If `attendees` was provided, sanity-check every owner against that list.

## Example
**Input (raw):** "ok so pricing... Sam thinks $29 is too low, Ana wants to test both. fine we'll A/B it. Sam will set up the test this week. also the churn dashboard is still broken, nobody knows why, Jo will look maybe"

**Output:**
**Summary:** Agreed to A/B test $29 vs current pricing rather than settle the debate now. Churn dashboard breakage remains undiagnosed.

**Decisions**
1. Run an A/B price test instead of picking a price now (Ana proposed, Sam agreed; Sam had argued $29 is too low).

**Action items**
- [ ] Set up the pricing A/B test - owner: Sam, by: this week
- [ ] Investigate broken churn dashboard - owner: Jo (tentative), by: not set

**Open questions**
- What is actually breaking the churn dashboard?

## Pitfalls
- **Promoting proposals to decisions.** Recording something as decided when the room only discussed it.
- **Owner-less actions.** Listing a task with no owner, so nobody picks it up - mark UNASSIGNED instead of leaving it blank or guessing.
- **Play-by-play.** Reproducing the discussion turn by turn instead of one line per thread; the deliverable is decisions and actions.
- **Erasing dissent.** Dropping the objection that got overruled removes the context needed if the decision is revisited.

## Output format
```
**Summary:** <two lines for someone who missed it>

**Decisions**
1. <decision> (<who proposed / who agreed>)

**Action items**
- [ ] <task> - owner: <name | UNASSIGNED>, by: <date | not set>

**Open questions**
- <unresolved item or ungreed proposal>
```
