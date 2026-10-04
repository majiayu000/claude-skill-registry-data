---
name: follow-up-radar
description: Scan a folder of outreach or CRM markdown files for overdue follow-ups and draft the follow-up messages, oldest first. Report-first and drafts only, it never sends anything. Use when the user says "any follow-ups due", "check my outreach pipeline", "who did I forget to follow up with", or "follow-up status".
---

# Follow-up Radar

Most outreach dies not because the first email failed but because the follow-up never went out. This skill finds the follow-ups you owe and puts the drafts in front of you. It reports first and it never sends anything.

## Step 0: Load the radar config (once)

Look for a `follow-up-radar.config.md` file in the project root. If it does not exist, ask for the values below, then offer to save them.

```
WATCH_FOLDER    Folder containing one markdown file per prospect or contact
STATUS_KEY      Frontmatter key holding the state (default: status)
DUE_KEY         Frontmatter key holding the follow-up date (default: follow_up_due)
DONE_VALUES     Status values that need no follow-up (default: Replied, Closed, Skip)
VOICE_NOTES     Optional tone guidance for drafts
```

The expected file shape is simple frontmatter, for example:

```markdown
---
company: Example Studio
status: Sent
follow_up_due: 2026-05-01
---
```

If the user's files use different keys, map them in the config instead of asking them to change their files.

## Step 1: Scan and report

Read the frontmatter of every markdown file in WATCH_FOLDER. Build the report before drafting anything:

```markdown
# Follow-up Radar: <today>

## Overdue (oldest first)
| Contact | Status | Due | Days overdue | File |
|---|---|---|---|---|

## Due in the next 7 days
| Contact | Status | Due | File |
|---|---|---|---|

## Waiting, not yet due: N
## Done or closed: N
## Files with missing or unparseable dates: <list them, do not guess>
```

Show the report in chat. If nothing is overdue, say so in one line and stop unless asked to continue.

## Step 2: Draft the overdue follow-ups

Only after the user confirms, or if they asked for drafts upfront. For each overdue item, oldest first:

1. Read the full file. If it already contains a prepared follow-up draft, use it as the base and only refresh anything stale (dates, references to "last week").
2. If there is no draft, write one: 80 words max, references the first message in one clause, adds one new angle or piece of value, no guilt-tripping, no "just checking in".
3. Subject line is `Re:` plus the original subject when the original is in the file.
4. Present each draft in chat under the contact's name with the file path.

## Step 3: Update the files (only on confirmation)

When the user says a follow-up was sent, update that file's frontmatter: set the status value they use for a second touch, and either advance DUE_KEY to the next window or clear it if this was the final touch. Never edit files the user did not confirm.

## Rules

- Report before drafting, draft before touching files, and never send anything. A human sends every message from their own inbox.
- Never mark anything as sent on your own.
- Dates you cannot parse go in the report as-is. Do not guess a date.
- No em dashes in any output.

## Output

A radar report in chat (optionally saved to a file on request), follow-up drafts for each overdue contact, and confirmed frontmatter updates.
