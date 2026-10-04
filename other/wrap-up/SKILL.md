---
name: wrap-up
description: "Saves today's work session as a four-line entry (did, decided, open, next) at the top of the project's log.md, after the student confirms it, so a fresh chat can continue tomorrow with /pick-up. Writes to projects/<client>/log.md or career-vault/log.md, one entry per project touched, never to _new-client. Use when the student says wrap up, done for the day, save my progress, end session, or is about to close the chat."
---

The student typed `/wrap-up`. They are done for the day and about to close this chat. Your job is to save what happened in this session so that tomorrow, in a fresh chat, `/pick-up` can carry on from exactly here.

A new chat remembers nothing from this one. The log is the only thing that carries over, so the four lines you write are all tomorrow's Claude will know.

## Step 1. Work out where the entry goes

The log lives beside the work it describes. Never in one shared file at root.

- Client work goes to `projects/<client>/log.md`. The client is the folder the session worked in: `edubridge`, or their own client folder.
- Career work (Classes 7 and 8, anything in `career-vault/`) goes to `career-vault/log.md`.
- Work on `principles/claude-contract.md` (Class 2) goes to the log of their project, because Class 2 also writes the project contract and that is where they will look for it.
- **Never write to `projects/_new-client/log.md`.** That folder is an empty template.

If the session touched two projects, write one entry into each project's log, each holding only what happened in that project. One client's notes never land in another client's file.

If `log.md` does not exist yet, create it with the header shown in Step 3.

## Step 2. Propose, then let them correct

Do not write straight away. Draft the entry from the session and show it:

```
Before I save, check this:

  Did:     ran /grill-me on the brief, finished brief-v3-interrogated.md
  Decided: bKash is its own flow, because the parent leaves the site
  Open:    the client has not said who handles refunds
  Next:    write scope-email.md

Anything wrong or missing?
```

The **Decided** line matters most. Write the decision and the reason, in their words where you can. If you are not sure something was a decision, ask rather than guess: the decisions are theirs, and a wrong one saved here gets repeated tomorrow as if it were settled.

If nothing was decided, write "nothing decided". Never invent one.

When they answer, apply their corrections. If they say it is fine, save it.

## Step 3. Write the entry

Newest entry at the **top**, directly under the header, so `/pick-up` reads the first entry and stops. Never rewrite or delete older entries.

New file header:

```markdown
# Log

One entry per work session, newest first. `/wrap-up` writes it, `/pick-up` reads it. You never edit this by hand.
```

Entry format, exactly four lines under a dated heading:

```markdown
## 2026-10-02, Class 3

- **Did:** ...
- **Decided:** ... because ...
- **Open:** ...
- **Next:** ...
```

Get today's date from the system, never guess it. Take the class number from the class table in `CLAUDE.md`; if the work was outside any class, leave the class off the heading.

Keep each line to one or two sentences. This is a note to themselves, not a report. Name real files by path.

## Step 4. Close

One line: which file you saved to, and that they can close the chat. Then stop.

```
Saved to projects/edubridge/log.md. Close this chat whenever you like. Tomorrow, open a new one and type /pick-up.
```

Do not summarise the session a second time. Do not suggest more work.
