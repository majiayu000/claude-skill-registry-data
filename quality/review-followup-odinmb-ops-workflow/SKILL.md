---
name: review-followup
description: Process follow-up files from autonomous runs (ops:batch-execute, ops:get-to-work). Walks through each item, presents options, takes action, and cleans up.
argument-hint: "[optional path to follow-up file]"
---

# Review Follow-Up

Process follow-up `.md` files left by autonomous commands (`/ops:batch-execute`, `/ops:get-to-work`).

## 1. Find the follow-up file

If `$ARGUMENTS` contains a file path, use that. Otherwise, search for follow-up files:

1. Check `.plans/` and `plans/` for files matching `*follow*up*` or `*followup*`.
2. If multiple found, list them and ask the user which to review.
3. If none found, tell the user and stop.

Read the file. Also read the branch's git log (`git log main..HEAD --oneline`) to understand what was done.

## 2. Frame what's open

Triage first (see Rules), then open with two or three sentences: what the run produced, and what kinds of decisions are still waiting on the user. If whoever invoked this skill has already said what the run produced — the `/ops:get-to-work` handoff does — don't say it again; open with what's still open. No item count, no section-by-section inventory, no commit count — the branch and its log are yours to keep track of.

## 3. Walk through each section

**Decidable before asked.** Never ask "what do you want to do about X?" without first making X decidable — at the level the user decides at. Read the plan file, the artifact, the state file, run `git show` on the commit, whatever it takes so *you* understand the concrete reality. Then say it in plain terms: what the project has now, what's wrong or thin about it, what each option would change, and what it costs. Don't paste what you read. Quote a document only when the text itself is the thing being decided — copy the user will send, an answer to a form, a spec — or when they ask.

Process sections in this order (skip empty ones):

### Implementation Issues
These block quality. Present each issue with options:
- **Fix now** — address the issue immediately
- **Create backlog item** — add to `.plans/` or `backlog/` for later
- **Dismiss** — not worth fixing

### Controversial Decisions
The agent made a judgment call. For each, say what it chose and why in terms of what the deliverable now claims or does — not the edits it made — then offer:
- **Keep as-is** — the agent's choice is fine
- **Revert** — undo this specific change (identify the commit)
- **Modify** — adjust the approach (ask what they want)

### User Input Needed
Questions the agent couldn't resolve. Read the plan file, the artifact, or the reference material first, then ask about intent — what the deliverable has to achieve, who it's for, what's acceptable — with concrete options where possible. Never hand the agent's question back in the agent's terms. After getting the answer, act on it: revise the artifact, the plan, or the state file it changes.

### Files to Delete
For each entry: what the file held, why nothing needs it now, and what's lost if that judgment is wrong. Group entries that share the same reasoning into one ask; paths go at the end of an entry, never at the front of it. Offer:
- **Delete all** — remove everything listed
- **Pick individually** — go through one by one
- **Skip** — leave them for now

### Skipped Items
Opportunities the agent chose not to act on. For each:
- **Plan it** — create a plan file for future work
- **Add to backlog** — lighter-weight tracking
- **Dismiss** — not worth pursuing

### Borderline Insights
Findings the agent wasn't sure were worth persisting. State each as a one-sentence rule or fact and say whether it applies project-wide or to one topic only, then offer:
- **Keep it** — scoped to that one topic
- **Keep it, project-wide** — most sessions need it
- **Dismiss** — not worth keeping

Pick the destination file yourself: project-wide rules go in `CLAUDE.md`, topic-specific ones in the matching `references/` or `state/` file, cross-project knowledge in `MEMORY.md`. Never ask which file — filing is your call.

### Suggested Follow-Up Work
Potential new work items. For each:
- **Create plan** — write a plan file
- **Add to backlog** — add as a backlog item
- **Dismiss** — not worth pursuing

## 4. Clean up

After all items are resolved:

1. Delete the follow-up file.
2. Close with what is now settled and what changed as a result — plus, in one line, the calls you took off the user's plate during triage. Not a tally of kept, reverted, planned, and dismissed.
3. If the session queued new work, say what the work is; a path belongs at the end of that sentence, if at all.

## Rules

- **Decidable before asked, always.** The follow-up file's one-liner is a pointer, not a decision brief — read the actual source before presenting anything. Then present what you learned as outcome and consequence, not as the material you read.
- **Triage first.** Before walking the sections, take out everything that's yours to decide. An item reaches the user only if their answer changes content, scope, priority, or a real-world commitment. Filing choices, INDEX cascades, naming, and mechanical cleanups: decide them, do them, and say in one line at the end that you did.
- Use **AskUserQuestion** with concrete options — don't ask open-ended questions when you can present choices.
- Batch related items when possible (e.g., "these 3 skipped items are all further research on the same funder — plan all, dismiss all, or pick individually?").
- When reverting, use `git revert` on the specific commit rather than manual edits, unless the commit contains mixed changes.
- When creating plan files, follow the project's existing plan format (check `.plans/` or `plans/` for examples).
- Keep momentum — the goal is to process the entire file in one session.
