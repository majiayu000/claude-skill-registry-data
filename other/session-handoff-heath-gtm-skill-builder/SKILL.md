---
name: session-handoff
description: Close a work session without losing what just happened. Write a handoff brief that captures progress, the decisions you made, the unfinished items and their next steps, and the details that would evaporate overnight, then it asks whether to commit or save it, never automatically. Trigger on "wrap up this session", "write a handoff", "close out for the day", "hand this off", "what did we get done", or the end of any working session you might have to resume later.
---

# Session Handoff

## What this does
Writes the brief you wish the last session had left you. It captures what got done, the decisions made and why, what is still open with the actual next step, and the fragile details, the half-finished thought, the thing you were about to try, that never survive to the next session. Then it stops and asks whether to save or commit it. It never writes anything on its own.

## What you'll need
You do not need to connect anything to get value today. The session already happened; the skill reads what you did and drafts the close-out. Connect the tools below and the capture gets more complete and the save becomes one click.

- Works today with: the session itself, what you worked on, what you decided, what you paste in. It drafts the handoff from that.
- More powerful connected to a repo: it reads the diff so "what got done" is grounded in real changes, not memory.
- Sharper with a notes tool: it can append the brief where the next session will look, once you approve.
- Sharper with a task tool: unfinished items become real tasks with next steps, once you approve.

## How this runs at your connection level
This skill is never reliant on a connector. It drafts from the session in front of it and gets more complete as you connect sources. It never claims progress it cannot see, and it never saves without a yes.

- **Bring your data**: tell it what you did or paste the work. It writes the full handoff today. No connection required.
- **Connect your tools**: it reads the diff, drafts the notes entry, and stages the open items as tasks, then waits for your approval to write any of it.
- **Just exploring**: no session to close? Get the handoff template and a worked example, so you know what "good" looks like before you need it.

Every run ends with the commit-or-save question and the one detail most likely to be lost if you walk away now.

## Customize this for yourself
This was built for an operator who resumes work across days and sessions. Set these to your rhythm:

| Set this | What it is | Default / Example |
|---|---|---|
| CODE_HOME | where the build lives | a git repo |
| NOTES_HOME | where handoffs get saved | a notes/wiki tool, a doc |
| TASK_HOME | where open items become tasks | a task tool, a checklist |
| SAVE_MODE | how the brief gets kept | draft only, append to notes, open a task |
| FRAGILE_PROMPT | the "what would be lost" nudge | on by default |
| COMMIT_STYLE | how a code commit is framed | conventional, plain summary |

The save is always yours to trigger. Change where it goes and how it reads. The close-out discipline does not change.

## The method

### Progress capture
State what actually changed this session in plain terms. If a repo is connected, ground it in the diff, files touched, what they now do. No connector? Capture what you report, marked as your account, not verified fact.

### Decision capture
Every decision made this session gets a one-line why. These are the calls the next session must not silently reverse. If a decision log exists, offer to add them there, on approval.

### Unfinished items and next steps
List what is open, and for each, the specific next step, not "keep going." "Finish the parser" is not a next step. "Handle the empty-row case in the parser" is.

### The fragile-details pass
The point of a handoff. Capture what lives only in your head right now: the thing you were mid-thought on, the approach you were about to try, the dead end you already ruled out so nobody re-walks it. This is what a bare task list loses.

### The commit-or-save question
The brief is drafted and shown to you. Then, and only then, it asks: save this to notes, open these as tasks, commit the code, or just hand it back to you. Nothing happens until you choose.

## Quality gates
- Nothing is committed or saved without your explicit approval. The skill drafts and asks; you decide. This is the rule, not a setting.
- No claimed progress the skill cannot support. If it is from your account and not a verified diff, it says so.
- Every unfinished item carries a real next step, not a restatement of the goal.
- The fragile-details section is never skipped, even on a short session. That is the part that would be lost.

## Output (example)
```
SESSION HANDOFF · onboarding automation · end of session

DONE THIS SESSION
  - Added domain-based dedupe (grounded in diff: dedupe.js, router.js).
  - Cut the API calls per run roughly in half by batching.

DECISIONS
  - Batch nightly instead of per-signup. Cost, not speed, was the constraint.

STILL OPEN  ->  NEXT STEP
  - EU routing owner undecided  ->  ask the team lead who owns EU signups.
  - Empty-row case in the parser  ->  handle the blank-domain row, it throws.

WOULD BE LOST IF I WALKED AWAY
  - I was mid-way through testing the batch job against last week's data,
    the 3rd run failed on a timeout, likely the sheet read, not the logic.
  - Ruled out per-persona routing already. Do not revisit; it was too noisy.

SAVE THIS?
  [ ] Append to notes   [ ] Open the 2 open items as tasks
  [ ] Commit the code    [ ] Just hand it back to me
  (nothing is saved until you choose)
```

## Where the inputs come from
The sections are fixed; how the brief is saved is not. SAVE_MODE defaults to draft-only because the safe default is to write nothing. Turn on append or task-creation when you trust the flow, and it still asks every time. The discipline is the same at every level.

## Example chat

**You:** Wrap this session up. We spent the afternoon on the CSV importer.

**Claude:** Here's the handoff.
```
DONE THIS SESSION
  - Added header-mapping so the importer accepts any column order (your account, no diff connected).
  - Fixed the duplicate-row bug on re-upload.

DECISIONS
  - Skip auto-dedupe on email alone. Too many false merges on shared inboxes.

STILL OPEN -> NEXT STEP
  - Large-file timeout -> test a 50k-row file before the next demo.

WOULD BE LOST IF I WALKED AWAY
  - The timeout only shows up past ~30k rows, and it looks like the parser,
    not the upload. Ruled out the upload limit already, do not recheck that.

SAVE THIS?
  [ ] Append to notes   [ ] Open the 1 open item as a task
  [ ] Commit the code    [ ] Just hand it back to me
```
Four sections, but the one that matters is the fragile-details one. That's the thing tomorrow-you would have re-discovered the hard way. One sharpener: connect the repo so "done this session" is grounded in the actual diff instead of your account of it.

## Go further
The handoff is step one. Here is where an operator takes it once the manual version proves out.

- **Ground every handoff in the real diff.** Connect the repo so "done this session" reads from committed changes, not memory, and the brief cannot overstate progress.
- **Turn open items into real work automatically.** Once you approve, push the unfinished items into a task tool with the next step attached, not a restated goal.
- **Close the loop at the start of the next session, too.** Schedule a Claude task to re-surface yesterday's fragile-details section the next time you sit down, so it never gets skipped.

You write the close-out once; the system makes sure it gets read.


## Make it yours
Fork it. Add a "blockers for tomorrow" line, a "who to update" line, a mood check if that helps you resume. Cut what you never use. The point is a close-out that makes tomorrow-you fast, and never surprises you by saving on its own. Built by an operator. Customize it, break it, make it better.
