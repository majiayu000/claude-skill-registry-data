---
name: meeting-notes-to-actions
description: Use when the user has meeting notes, a call transcript, or a voice-memo dump and wants decisions, action items, and a follow-up email out of it. Works for client calls, discovery calls, and internal check-ins.
---

# Meeting Notes → Actions

Turn messy notes into three things: a decision log, an owned action list, and a follow-up email the user can send in 30 seconds.

## Step 1 — Load context
Read `.solo/business.md` if present (for tone and to recognize client names). Proceed without it if missing — this skill works standalone.

## Step 2 — Get the notes
Accept a pasted transcript, a file path, or bullet notes. If it's a transcript, identify speakers; if names are missing, use roles (Client, Me).

## Step 3 — Extract, then verify
Extract:
- **Decisions** — things that were agreed. Quote or closely paraphrase; do not upgrade "we could" into "we will".
- **Actions** — each with an owner and a due date if stated. If no date, mark `(no date set)` rather than inventing one.
- **Open questions** — anything raised but unresolved.
- **Risks / flags** — budget hesitation, scope drift, unclear decision-maker, missed deadlines mentioned.

Before writing the email, show the user the decisions and actions and ask one question: "Anything wrong or missing?" Skip this check only if the user said "just do it".

## Step 4 — Write the outputs
Write `meetings/<YYYY-MM-DD>-<client-or-topic-slug>.md`:

```markdown
# <Topic> — <date>
Attendees: ...

## Decisions
- ...

## Actions
| Owner | Action | Due |
|-------|--------|-----|
| Me    | ...    | ... |
| <Client name> | ... | ... |

## Open questions
- ...

## Flags
- ...

## Follow-up email (draft)
Subject: <Topic> — recap and next steps

Hi <name>,

Thanks for the time today. Quick recap so we're aligned:

<2–4 decision bullets>

Next steps:
<action bullets, grouped: yours / theirs, with dates>

<One line on the biggest open question, if any.>

<Sign-off from business.md tone>
```

If the meeting was a discovery call, add a final section `## Proposal inputs` summarizing problem, success criteria, constraints, and budget signals — formatted so `/proposal-writer` can use it directly.

## Tone rules
- Email under 150 words. Recaps that get read are short.
- The client's actions come *after* the user's own — it reads as collaborative, not as assigning homework.
- Neutral wording for flags in the file; flags never appear in the email.

## Do not
- Do not invent dates, owners, or commitments.
- Do not include the "Flags" section in anything sent to the client.
- Do not summarize the whole conversation — only decisions, actions, questions.
