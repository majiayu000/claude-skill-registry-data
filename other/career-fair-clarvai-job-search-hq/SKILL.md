---
name: career-fair
description: "Prepare the user for a career fair, recruiting event, or networking event (target list, 30-second pitch per company, questions, what to bring) and handle follow-ups afterward. Use when the user mentions a career fair, info session, industry meetup, conference, campus showcase, or networking event."
argument-hint: "[event name]"
---

# /career-fair

Usage: `/career-fair <event name/date> or 'after' for follow-ups` (or just ask in plain English).

## Before (`$ARGUMENTS` = the event)
1. Ask for the employer or attendee list and the date/time (the user pastes it from the event page; if the user is a student or new grad, Handshake usually shows it for campus fairs).
2. Rank employers into **Must visit (5)**, **Good (5)**, **If time** using `profile/preferences.md`, `knowledge/field/target-employers.md`, and open roles (quick check of each careers page).
3. Write `interviews/<date>-<event>-plan.md`:
   - Route: must-visits first (lines grow later).
   - A **30-second pitch** the user says out loud: name, who they are in one line (from preferences and the master resume: for students, school, major and graduation year; otherwise current or most recent role and years of experience), one proof point from `profile/master-resume.md` picked for that employer, what role they want, one question. Make 2–3 variants for the user's main target role types.
   - Per must-visit company: one specific thing they do, one smart question, the open role link.
   - Checklist: printed copies of their best general resume (about 15 for a large fair; offer to tailor an event version), padfolio and pen, dress as the event says, phone charged with LinkedIn QR code ready, water.
   - At each booth: get the recruiter's name and ask "What's the best way to follow up with you?"; after walking away, jot two lines (name, what they discussed) for the follow-ups.
   - **Virtual fairs (e.g. Handshake):** short one-on-one slots (often 10 minutes) and group sessions fill up; book must-visits when sign-up opens, after completing the profile (employers can limit who sees slots).
   - **Conferences and meetups:** pick 3–5 people from the attendee list or app (speakers, target employers) and draft a short note to send beforehand (`/network`); a question after a talk is an easy opener.
   - If crowds drain the user: aim for 2–3 real conversations, arrive early, take breaks.
4. Offer a 5-minute practice: you play a busy recruiter at a booth (Interview Room, style `behavioral`, each question with `seconds: 30`; start with "So, tell me about yourself").

## After (`$ARGUMENTS` = after)
0. Work out which event this is: the one the user names, or the one already established in this conversation. Never pick by file date (a plan for a future event may be newer). If it's unclear, list the `interviews/*-plan.md` events dated on or before today (most recent first) and ask which one. Read that plan and use its event name and date everywhere below (`how_we_met`, message text).
1. Go through the people one at a time, asking one question per message: name and company, their title, what they talked about, and any instruction ("apply online and mention me"). Skip what the user already said.
2. Add each new person to `contacts/contacts.csv` (`relationship=met-at-event`, `how_we_met` = the event and date, `status=talked`, `touches=0`, `job` if they pointed to a posting); for someone already there, update `last_contact` and notes but never lower their status. Run `add-job` for any posting they pointed the user to. Log the changes in `history/activity.md`.
3. Draft follow-ups into `outbox/` within 24 hours: ≤ 100 words, reference the conversation specifically, mention the role, thank them. LinkedIn connection note (≤ 200 characters) if no email. Run `truth-checker`, then `voice-editor`, on them. Once the user sends a note, set that person's `last_contact` to the date sent. These people already talked with the user (`talked`), so the note adds no `touches` and no `next_followup`; a job they've applied to owns its own follow-up date. If the user wants a reminder to reach out again (say, after applying), set `next_followup` only for pure networking and only when they ask.
