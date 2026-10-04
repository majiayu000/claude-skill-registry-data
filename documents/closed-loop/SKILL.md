---
name: closed-loop
description: Close the gap between "you corrected me" and "it never happens again." Scan a work session for the corrections you made, the things you approved, and the patterns that held up, then propose specific edits to your skills, playbooks, and docs, high-confidence corrections separated from medium-confidence patterns, with nothing changed until you approve. Trigger on "learn from this session", "what should we update", "turn this into a rule", "close the loop", "improve the playbook", or the end of any session where you corrected or approved the work.
---

# Closed Loop

## What this does
Reads back over a session and turns feedback into durable improvement. It finds where you corrected the work, where you approved it, and where a pattern proved itself more than once, then proposes exact edits to the skills, playbooks, or docs that produced the work. A correction you make twice is a rule you never wrote down. This writes it down, and shows it to you before anything changes.

## What you'll need
You do not need to connect anything to get value today. The session is the input; the skill reads it and proposes updates. Connect the tools below and it can locate the exact file to edit and stage the change for approval.

- Works today with: the session, the corrections and approvals in it, or a transcript you paste. It proposes the updates from that.
- More powerful connected to a repo: it finds the actual skill or doc file the update belongs in and drafts the diff.
- Sharper with a notes or wiki tool: it can point proposed edits at the living playbook, not a copy.
- Sharper with a decision log: it links each accepted change to the decision that justified it.

## How this runs at your connection level
This skill is never reliant on a connector. It reasons over the session in front of it and gets more precise as you connect the targets it might edit. It proposes; it never changes anything on its own.

- **Bring your data**: paste the session or describe the corrections. The skill proposes the full set of updates today. No connection required.
- **Connect your tools**: it locates the real files, drafts the diffs, and stages them, then waits for your yes on each one.
- **Just exploring**: no session yet? Get the confidence rubric and a worked example, so you can see how a correction becomes a proposed edit.

Every run ends with the single highest-value update to make first, and the reason it earned that rank.

## Customize this for yourself
This was built for an operator whose skills and playbooks are living documents. Set these to your setup:

| Set this | What it is | Default / Example |
|---|---|---|
| TARGETS | what can be updated | your skills, playbooks, SOPs, docs |
| CODE_HOME | where skills/docs live | a git repo, a docs folder |
| NOTES_HOME | where playbooks live | a notes/wiki tool |
| HIGH_BAR | what counts as high-confidence | an explicit correction you made |
| MED_BAR | what counts as a pattern | a behavior that repeated, unconfirmed |
| AUTO_APPLY | whether anything applies without asking | off, always off |

The confidence split is the safeguard. Tune what clears each bar. The rule that nothing applies without approval does not move.

## The method

### Session scan
Walk the session for three signals: corrections (you told it to do something differently), approvals (you confirmed something was right), and patterns (the same choice held up more than once). Everything downstream is anchored to a real moment in the session, quoted, not inferred.

### High-confidence corrections
An explicit correction is high-confidence. You said "no, do it this way." That becomes a proposed edit stated plainly, with the before, the after, and the exact spot it changes. These are the sure things, and they are listed first.

### Medium-confidence patterns
A pattern that repeated but was never confirmed is medium-confidence. It is proposed as a question, "you did X twice, should this be the default?", not asserted as a rule. Medium items never get promoted to high on their own.

### Proposed edits, file by file
Each accepted signal maps to one target and one concrete change. It shows what the doc says now and what it would say. If a repo is connected, it drafts the diff. If not, it hands you the exact text to paste.

### The approval gate
Nothing is written. Every proposed edit is presented for a yes or no, one at a time. You can accept the corrections and defer the patterns, or the reverse. The loop closes only on what you approve.

## Quality gates
- Nothing is written, committed, or deleted without your explicit approval, per edit. AUTO_APPLY is off and stays off.
- Every proposed update quotes the moment in the session that justifies it. No update without evidence.
- High-confidence and medium-confidence are never blended. A guess is labelled a guess.
- A pattern is never silently promoted to a rule. It stays a question until you answer it.

## Output (example)
```
CLOSED LOOP · onboarding-automation session · 3 signals found

HIGH CONFIDENCE (explicit corrections)
  1. You corrected: "route by company size, not persona."
     Target: the routing playbook, step 2.
     Now:  "Assign owner by persona match."
     To:   "Assign owner by company size band."
     [ ] Apply   [ ] Skip

MEDIUM CONFIDENCE (patterns, unconfirmed)
  2. You batched the job nightly twice this week without being asked.
     Should "nightly, not real-time" become the default in the SOP?
     [ ] Make it a rule   [ ] Leave as a one-off   [ ] Ask me later

DO THIS FIRST
  Apply #1. It is an explicit correction and it changes live routing.

(nothing above is written until you choose)
```

## Where the inputs come from
The confidence bars are defaults, not laws. HIGH_BAR is "you said it outright"; MED_BAR is "it repeated but you never confirmed." If your work needs a stricter bar before anything touches a playbook, raise it. The separation between sure and suspected is the whole point, and it does not move.

## Example chat
**You:** Before we wrap this session, what should we actually update based on what I corrected?

**Claude:** Found 3 signals in the session.
```
HIGH CONFIDENCE (explicit corrections)
  1. You corrected: "route by company size, not persona."
     Now:  "Assign owner by persona match."
     To:   "Assign owner by company size band."
     [ ] Apply   [ ] Skip

MEDIUM CONFIDENCE (patterns, unconfirmed)
  2. You batched the job nightly twice this week without being asked.
     Should "nightly, not real-time" become the default in the SOP?
```
Nothing here is written yet, that's the whole design. The high-confidence item quotes exactly what you said, so you're approving a change you already made, not a guess about what you meant.

**You:** Apply #1, leave #2 as a one-off for now.

**Claude:** Applied #1 to the routing playbook, step 2. #2 stays a one-off, noted but not promoted. One sharpener: run this at the end of every session instead of just this one, a pattern that repeats a third time without being confirmed is usually the one worth turning into a rule.

## Go further
Reviewing one session by hand catches what you just corrected. Here's how the habit compounds.

- **Run it automatically at session close.** Wire a scheduled Claude task to scan the day's sessions each evening and queue proposed edits for a morning approval pass, so nothing gets lost between sessions.
- **Stage the diffs where you already work.** Connect a git repo so accepted corrections land as real pull requests against your skills and playbooks, not just text you have to paste in yourself.
- **Track what got promoted.** Log every approved edit to a Notion or wiki changelog so the team can see which corrections became permanent rules and when.

A correction made once is feedback. A correction captured every time is a system that stops repeating its own mistakes.

## Make it yours
Fork it. Add a "retire this" pass for rules that stopped earning their place, or a monthly rollup of everything the loop learned. Cut what you do not use. The point is a system that gets better every session instead of repeating the same correction. Built by an operator. Customize it, break it, make it better.
