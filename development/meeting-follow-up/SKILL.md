---
name: meeting-follow-up
description: "Turns one or more meetings into a verified follow-up plan and review-ready email drafts. Reads your notes or transcripts, plus the calendar invite and email threads if you have connectors, then works out who attended (names and emails checked against sources, never guessed), what was promised both ways (owed by us vs owed by them), who gets each follow-up (To and CC, one owner per action), what to send and when. Checks for replies and booked calls before suggesting a nudge. Drafts only; never sends, schedules or writes to a CRM. Use when someone says \"follow up on this call\", \"who do I email after the meeting\", \"what did we promise\", \"draft the follow-ups\", \"map the attendees\", \"recap and next steps\" or pastes meeting notes and asks what to do next."
---

# Meeting Follow-up

Follow-ups fail quietly: a wrong address, a promised document that never goes out, a nudge to someone who already replied. This skill turns a meeting into a short, checked plan plus drafts. You read them and press send.

## What it does

1. A verified attendee list, with the source of every name and email.
2. Every promise, split into **owed by us** and **owed by them**.
3. Actions with one owner, one thread, To, CC and a send window, checked against what happened since.
4. Drafts for review, plus a list of anything it could not verify.

## What you need

| Source | Gives you | If missing |
|---|---|---|
| Notes or transcript (pasted, a file, or a recorder such as Fathom, Otter or Fireflies) | What was said and promised | Required. Rough notes work; say so and confidence drops. |
| Calendar invite (Google Calendar or Outlook connector, or pasted) | Title, time, organizer, invitee emails | Ask the user for attendee emails, or mark them unverified |
| Email threads (Gmail or Outlook connector, or pasted) | Exact addresses, latest replies, what was already sent | Ask: "Has anyone replied or sent anything since the call?" |
| Your settings | Cooldown between nudges (default 3 business days), your sign-off, who is on your side | Use the defaults and say so |

Works in Claude.ai (paste notes, or use connectors if enabled) and Claude Code (connectors, or exported `.txt`, `.vtt`, `.eml` or `.ics` files in a folder). Everything is read-only.

## Steps

### 1. Fix the scope
Confirm which meeting(s), the date and the timezone. For "today's calls", list what you found and confirm. Ignore travel blocks, focus time and room resources.

### 2. Build the attendee list
For each person: name, email, company, role, attended or only invited, and source.

- An email is **verified** only if it appears in an invite, an email header or a signature, or the user typed it.
- A name is verified only if a source ties it to that email. Do not expand initials or build a name from an address.
- Never guess an address from a pattern (first.last@company). Write `UNVERIFIED: ask user` instead.
- An invite shows who was asked, not who came. "No response" on an RSVP is not proof of absence. Use the transcript or the user's word for attendance.

### 3. Extract promises
Read the full notes, not a summary of them. For each commitment record: who promised, what exactly, to whom, any date mentioned, and a short quote or timestamp. Sort into:

- **Owed by us:** materials, answers, intros, proposals we said we would send.
- **Owed by them:** data, decisions, intros, documents they said they would send.
- **Decisions made:** things agreed that need no action, so nobody asks again.

If something is vague ("we'll circle back"), list it as **unclear** with the quote. Do not turn it into a promise.

### 4. Check the current state
Before recommending any email, look at what happened after the meeting:

- Has anyone on either side already replied, sent the material, or answered the question?
- Is a next call already booked? If so, scheduling is done, but promised materials may still be owed.
- Did they ask to pause or pick a later date? Their timing wins. Mark the action **HOLD** with the date.
- When did our side last write? If it was inside the cooldown, a nudge waits until it ends. Count anyone on your side, not just the user.
- Is there an unsent draft already? Mention it; do not draft a second one.

Without email access, write "not checked" and ask the user, rather than assuming nothing happened.

### 5. Turn promises into actions
- **Count actions, not people.** Two people on one shared thread about one topic is one action.
- **One owner per action** on our side, named.
- **To** is the person who must do or decide the thing. **CC** is the sponsor or coordinator who needs visibility. Do not CC a busy coordinator on every email.
- If you do not know who on their side owns something, send one narrow question to the closest verified attendee ("Who is best to send the Q3 file?"). Do not label that person as the owner.
- Keep **materials owed by us** separate from **nudges**. Owed materials go out now, cooldown or not. A nudge about their open items respects the cooldown and any hold.
- Do not re-ask for something they already sent, or re-offer something we already delivered.
- Give each action a status: **SEND NOW**, **SEND ON (date)**, **HOLD (reason)**, **NO ACTION (reason)** or **NEEDS INFO (what)**.

### 6. Draft the emails
One draft per action, not per person. Each draft:

- Reply in the existing thread if there is one, and say which.
- Opens with the useful thing (the file, the answer, the decision), not "just following up".
- Recaps only what the source supports. No invented numbers, dates, names or agreements.
- Ends with one clear ask and a date if one was agreed.
- Marks every placeholder clearly: `[ATTACH: pricing sheet]`, `[CONFIRM: start date]`.

If the user has a Gmail or Outlook connector and asks for native drafts, you may create unsent drafts. Never send, schedule, invite, share files or update a CRM, even if the tools allow it.

### 7. Quick check before you hand it over
- Every email in To or CC is verified, or the draft is marked HOLD.
- Every claim in a draft traces to a line in the plan's source facts.
- No action is duplicated across drafts.
- Nothing contradicts a later reply.

## Output

Fill `templates/FOLLOW-UP-PLAN.md`. Order:

1. **Bottom line:** one or two sentences, the number of actions and what goes first.
2. **Source facts:** meeting details, attendees, promises, decisions, each with its source. Facts only.
3. **Recommendations:** the action table. Clearly labelled as recommendations.
4. **Drafts:** one per action, ready to review.
5. **Gaps:** unverified identities, unclear promises, sources not checked.
6. **The line:** "Nothing was sent, scheduled or changed. Drafts are for your review." (Or, if native drafts were created: "Unsent drafts created in your mailbox: (list). Nothing was sent.")

See `examples/worked-example.md` for a short filled-in run.

## Rules

- Source facts and recommendations never share a line. "Dana owns the budget" needs a source; otherwise write "Recommended owner: Dana".
- Never invent a fact, an email address, a date, a price or a commitment. Missing means missing.
- Later sources beat earlier ones. A reply that says "we went another way" overrides the enthusiasm in the call.
- Respect the cooldown the user sets, measured from the last message anyone on our side sent.
- If the user names someone to skip, skip them for the whole run.
- Keep private details (phone numbers, access codes, side remarks) out of drafts.

## Honest limits

- It only knows what you give it. Without email access it cannot tell whether someone already replied, so it asks you.
- Transcripts mishear names and numbers. Check any figure before it goes in an email.
- "Attended" from an invite is a guess; the transcript or you are the real source.
- It does not know your relationships or politics. It recommends To and CC; you decide.
- Long multi-meeting runs can miss a promise. Skim the list before sending.
