---
name: coach-prep
description: "Use when the user has (or wants) a meeting with a career coach, their school's career office, an advisor or a mentor, asks how to find one, says 'I'm seeing my career coach', or just had that meeting. Builds a one-page brief to bring (where they stand, what they've tried, what to ask, what to send ahead) and records the advice and next steps afterward."
argument-hint: "[optional: 'after' once the meeting happened]"
---

# /coach-prep: get the most from a meeting with your coach or mentor

Usage: `/coach-prep` before a meeting, `/coach-prep after` once it happened (or just ask in plain English).

A good meeting with a person beats an hour with the assistant on the questions that need judgment, relationships or insider knowledge. This skill makes the user's 20 or 30 minutes count.

Read first: `profile/preferences.md`, `profile/life-design.md` (if it's missing, run `bash .claude/skills/start/scripts/init-data.sh`, or on Windows without bash `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\start\scripts\init-data.ps1`; it only adds missing starter files), `jobs/tracker.csv`, `contacts/contacts.csv`, the last 20 lines of `history/activity.md`, and, if a document will be reviewed, that file.

## Before the meeting

1. **Who and when.** If they haven't got someone yet, suggest who fits their situation: their school's career office (students, and many schools serve alumni for a year or more: tell them to check), a former manager or senior colleague they trust, a professional association's mentoring program, or a paid career coach (say plainly that coaches vary and credentials aren't regulated). Never book for them.
2. **What do they want from it?** One question: "What would make this meeting worth it for you?" If they're not sure, offer three choices that fit their situation (from the files): decide between directions; get feedback on a resume or application; fix a strategy that isn't working (applications without replies, for example); prepare for an interview or offer; or a question only that person or office can answer. If they want help choosing between directions and `profile/life-design.md` has none yet, offer a short `/explore` first so they bring something concrete.
3. **Send ahead, if it helps.** A document for review should be the current, checked version (a tailored resume PDF from a job folder, or, for general feedback, the resume file they're sending out now (a copy of `profile/master-resume.md` is fine too; don't build a new one for this)), sent a day or two before so they can read it.
4. **Write the brief** (one page, plain text, in their voice; show it to them; save it under "Meetings with my coach or mentor" in `profile/life-design.md`, dated with the meeting date):
   - **Where I am** (2-3 lines): their situation, what they're aiming for or exploring, how many applications and conversations so far and how they went (counts from the tracker and contacts; no names of contacts unless the user wants to discuss them).
   - **What I've tried** (2-3 lines): experiments and what they learned (from the notes), and what isn't working, in plain numbers ("12 applications since September, 1 interview").
   - **My questions** (3, most important first): specific and answerable in the time ("Should I take the contract role or keep applying for full-time?", not "what should I do?").
   - **What I'll bring:** the document, the job link, the offer letter (with pay and terms, never ID numbers), as the meeting needs.
   Keep anything private out unless the user wants it in: the brief is theirs to show. Remind them once: "This stays on your computer. Bring it on your phone or print it; nothing goes to anyone unless you show or send it."
5. Offer one practice question if they're nervous ("Want to rehearse how you'll open?").

## After the meeting (`/coach-prep after`)

1. Ask, one at a time: "What did they suggest?" and "What will you do first, and by when?" (and the name of anyone they suggested contacting).
2. Save under that meeting in `profile/life-design.md`: their suggestions, and each next step as `- YYYY-MM-DD · Next step: ...` (when the user says one is done, change it to `Done:`; dropped, `Dropped:`). New people go in `contacts/contacts.csv` only with the user's OK (`relationship=career-educator` for a coach or career-office adviser, `mentor` for a mentor, if the user wants them tracked; for people they suggested, the relationship that fits, usually `alum` or `cold`, with `how_we_met` "suggested by <name>, <date>"). Jobs they pointed to go through `add-job`. Steps with a date: offer to put them where `/today` will show them (a job's `next_action`, a contact's `next_followup`, or a dated `Next step:` line in the notes, which `/today` shows when it's due).
3. If the advice changes their direction or target roles, offer to update preferences (show the lines; their yes) and, if needed, the field pack.
4. Suggest a short thank-you note only if it was someone they'll see again or who gave their time for free (two or three lines, into the Outbox; `truth-checker` and `voice-editor` as usual).
5. Log one line in `history/activity.md`: `- <date time> · <app> · Coach meeting notes saved`.

## Rules

- On their own institution's matters (a school's programs, deadlines, eligibility; an employer's internal process), the person's advice wins over yours. If their advice conflicts with a ground rule (for example, adding something untrue to a resume), say plainly that you can't do that part, and why.
- Never contact the coach or office yourself, never book, and never share the user's files with anyone.
- Don't invent what a school office or program offers: that's a question for the meeting.
