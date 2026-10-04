---
name: decision-log
description: Stop re-litigating decisions you already made. Keep a decision record where each entry captures the decision, the context that forced it, the options you weighed, why you chose, and when to revisit, one entry at a time, in plain searchable markdown you can grep later. Trigger on "log this decision", "why did we choose X", "write a decision record", "record why we're doing this", "what did we decide about", or any moment a real call gets made and would otherwise be forgotten.
---

# Decision Log

## What this does
Captures a decision the moment it is made, in a form future-you can search and trust. Each entry names the decision, the context that made it necessary, the options on the table, the reason one won, and the condition that should make you revisit it. Six months from now, when someone asks "why is it built this way," the answer is one grep away instead of a debate. It writes one entry at a time and never touches the log without your go-ahead.

## What you'll need
You do not need to connect anything to get value today. Describe the decision and the skill drafts the entry. Connect the tools below and it appends to your real log and keeps the numbering straight.

- Works today with: the decision and the thinking behind it, described or pasted. It produces a clean, structured entry.
- More powerful connected to a repo: it appends entries as numbered markdown files you can grep, diff, and review.
- Sharper with a notes or wiki tool: the log lives where the rest of the project context lives.
- Sharper with a context pack or handoff: decisions logged here feed straight into orientation for the next session.

## How this runs at your connection level
This skill is never reliant on a connector. It drafts the entry from what you tell it and gets more useful as you connect somewhere to keep it. It never writes to the log without approval.

- **Bring your data**: describe the call you made. The skill drafts the full entry today, in standard structure. No connection required.
- **Connect your tools**: it appends the entry to your log, assigns the next number, and keeps the format consistent, once you approve.
- **Just exploring**: no decision to log yet? Get the entry template and a worked example, so the format is ready when the call comes.

Every run ends with the one open question the decision leaves behind, so the next entry has a head start.

## Customize this for yourself
This was built for an operator who makes real calls and hates re-arguing them. Set these to your setup:

| Set this | What it is | Default / Example |
|---|---|---|
| LOG_HOME | where entries live | a git repo, /decisions; a notes tool |
| ENTRY_FORMAT | one file per entry, or one running doc | numbered markdown files |
| ID_SCHEME | how entries are numbered | 0001, 0002, ... (zero-padded) |
| STATUS_SET | the states an entry can hold | proposed, accepted, superseded |
| REVISIT_DEFAULT | default revisit trigger | "revisit if the constraint changes" |
| SUPERSEDE_LINK | how a reversal points back | new entry links the one it replaces |

The five fields are fixed. Where the log lives and how entries are numbered are yours.

## The method

### The five-field entry (fixed)
Every entry carries exactly these, in order.
1. **Decision** what was decided, in one sentence, stated as done.
2. **Context** the situation and constraint that forced a choice.
3. **Options considered** the real alternatives, including the one you rejected and why.
4. **Why** the reason this option won over the others.
5. **Revisit when** the condition that should reopen this, a date, a threshold, an event.

### One entry at a time
Each call gets its own entry. The skill does not batch a week of decisions into one blob. One decision, one greppable record, one number.

### Greppable by design
Plain markdown, consistent headings, a stable ID. So `grep routing` across the log finds every decision that ever touched routing, in seconds, forever.

### Supersede, never erase
When a decision is reversed, you do not delete the old entry. You write a new one that links back and marks the old one superseded. The trail of why-we-changed-our-mind is as valuable as the decisions themselves.

### Revisit triggers
Every entry ends with a condition to revisit, not a vague "someday." "Revisit when volume passes 10k/day" is a trigger. "Revisit later" is not.

## Quality gates
- Nothing is written to the log without your explicit approval. The skill drafts the entry and shows it; you decide if it lands.
- No entry ships without all five fields. An entry with no "options considered" is not a decision record, it is a note.
- A superseded decision is linked, never deleted. History stays intact.
- The revisit condition is concrete, an event or a threshold, not "later."

## Output (example)
```
DECISION 0007 · Route onboarding by company size · status: accepted

DECISION
  New signups are routed to an owner by company-size band, not by persona.

CONTEXT
  Persona routing mis-assigned ~1 in 3 signups. The team lost trust in the
  queue and started hand-sorting, which defeated the automation.

OPTIONS CONSIDERED
  - Persona match (rejected: too noisy, data was sparse on new signups).
  - Company-size band (chosen).
  - Round-robin (rejected: ignores fit entirely).

WHY
  Size band is reliably present on a fresh signup; persona is not. Fewer
  inputs, fewer ways to be wrong.

REVISIT WHEN
  Persona data coverage on new signups passes ~80%, or volume passes 10k/day.

(draft, not saved. approve to append as 0007 in the log)
```

## Where the inputs come from
ID_SCHEME and STATUS_SET are defaults, not laws. Some teams like proposed/accepted/deprecated; some like a plain running doc with dates. The five fields are the standard because each one is a question future-you will ask. Change the packaging. Keep the fields.

## Example chat
Here is the skill running on a real call, start to finish.

**You:** Log this: we just decided to route onboarding by company size instead of persona.

**Claude:** Drafted the five-field entry.
```
DECISION 0007 · Route onboarding by company size · status: accepted
CONTEXT: Persona routing mis-assigned ~1 in 3 signups.
OPTIONS: Persona match (rejected), Company-size band (chosen), Round-robin (rejected)
REVISIT WHEN: Persona data coverage passes ~80%, or volume passes 10k/day.
(draft, not saved. approve to append as 0007)
```
The thing this catches: without a stated revisit-when, this decision sits unexamined forever, or gets re-litigated from scratch in six months with nobody remembering why persona routing got dropped.

**You:** Approved, append it.

**Claude:** Appended as 0007 in the log. It does not supersede anything yet, so no link needed. One sharpener: connect the repo so I can append directly and keep the ID numbering straight instead of you copy-pasting it in.

## Go further
The read is step one. Here is where an operator takes it once the manual version proves out.

- **Append straight to the repo.** Connect a GitHub repo so approved entries write as numbered markdown files automatically, no copy-paste step.
- **Surface stale decisions on their own.** Schedule a Claude task to grep the log monthly for any entry whose revisit condition has likely been met, and flag it in Slack.
- **Hand it to the next session automatically.** Wire the decision log into a context-pack or handoff so a new session opens already knowing what was decided and why.

The log is only useful if it gets read back. Automate the reading, not just the writing.

## Make it yours
Fork it. Add a "consequences" field, a "who was in the room" field, tags for the area of the system it touches. Cut what you never read back. The point is that no real decision is ever silently lost or re-argued from scratch. Built by an operator. Customize it, break it, make it better.
