---
name: pick-up
description: "Reads the newest entry of a project's log.md and tells the student where they left off: what they did and decided, what is open, and the next step. Takes an optional project name. With several projects and no name, shows a menu of each project's last entry. Read only. Use when the student says pick up, where did I leave off, read my last log, continue from yesterday, or opens a fresh chat to resume work."
---

The student typed `/pick-up`, maybe followed by a project name. This is a fresh chat and it knows nothing about yesterday. Your job is to read their last log entry and tell them where they left off, so they start working in under a minute.

Read only. This skill writes nothing.

## Step 1. Find the right log

Logs live at `projects/<client>/log.md` and `career-vault/log.md`. Ignore `projects/_new-client/`, which is a template.

Pick the log in this order, and stop at the first one that applies:

1. **They named a project** (`/pick-up acme`). Use that project's log. Match loosely: "acme" finds `projects/acme-fintech/`, "career" or "vault" finds `career-vault/log.md`.
2. **Claude Code is open inside one project folder.** Use that folder's `log.md`.
3. **Only one log exists.** Use it.
4. **Several logs exist.** Read only the first entry of each and show a menu, most recent first:

```
You have three projects with a log:

  1. acme-fintech   yesterday     Next: dashboard empty states
  2. edubridge      3 days ago    Next: write scope-email.md
  3. career-vault   last week     Next: finish 02-portfolio-story.md

Which one?
```

Then wait for their answer.

If no log exists anywhere, say so in one line and point them to `/wrap-up` at the end of today's session. Then offer the normal orientation from `CLAUDE.md`.

## Step 2. Read the newest entry only

Read the first entry under the header. Do not read older entries unless they ask. Do not read the whole project folder yet; the entry names the files that matter.

Then open the file the **Next** line names, if it names one, so you know its current state before you speak. If that file already looks finished, say so: they may have done more after the last wrap-up.

## Step 3. Tell them, in this shape

```
Last time (2 Oct, Class 3) you finished the interrogated brief and
decided bKash is its own flow. Still open: who handles refunds.

Next step: write scope-email.md. Start there, or deal with the
refund question first?
```

Three parts, under 80 words: what they did and decided, what is still open, and the next step as a question. Use their decisions as settled. Do not reopen them unless they ask.

If the entry is older than two weeks, add one line: "This is from <date>, so check it still holds."
