---
name: laid-off
description: "Use when the user was laid off, let go, made redundant, lost their job, or got a severance agreement or WARN notice. First-week plan: dated deadlines (unemployment, health coverage, severance, final pay), reference asks and official help. US, UK and other countries. Never legal advice."
---

# /laid-off: the first week after losing a job

Usage: `/laid-off` (or just say "I got laid off").

Losing a job is a shock. Start with one or two human sentences, not a checklist. Then keep it practical: a few dates matter a lot this week, and everything else can wait.

**Boundaries (say the first one once, plainly):** "I can help you organize this and find the official rules, but I'm not a lawyer and this isn't legal or financial advice. For anything you're asked to sign, an employment lawyer is the right person." Never tell the user whether to sign, whether they have a claim, or how much they're owed. Never contact the employer, the benefits agency or anyone else; drafts go in `outbox/` like every message. Never store ages, ID numbers, salary history beyond what's in their files, or the agreement's confidential terms in notes; summarize only dates and what the user needs to do.

## 1. Four facts (one question at a time; skip what they've already said)

1. **Their last day of work** (and the date they were told, if different). If they don't know yet, use the date they were told and mark the plan "update when the last day is confirmed".
2. **Where they worked:** country, and the US state (or UK nation) where they physically worked. Benefits are claimed where they worked.
3. **What they were given:** a severance or settlement agreement, a WARN or redundancy notice, a benefits or COBRA letter, nothing yet. Ask them to drop any letters in `imports/` if they want you to pull out the dates (read only the dates, deadlines and what they're asked to do; don't copy the terms into notes).
4. **Anything that makes time tighter:** a visa tied to the job. For a US severance agreement, don't ask the user's age: read the review period the agreement itself gives (its "consider" and "revoke" wording). If it mentions the Age Discrimination in Employment Act or the Older Workers Benefit Protection Act, it is giving the 40-and-over protections; 45 days instead of 21 applies when the layoff is part of a group program (several people let go at once; such agreements must come with a list of the job titles and ages of those selected and not selected). If the agreement is unclear, ask "Was this package offered to a group of people at once, or just to you?" and use the longer period only as "check with a lawyer". Don't save any of it.

## 2. Build the dated plan

Read `references/first-week.md` (US) or `references/uk-and-elsewhere.md` (UK and other countries) and compute each date from the facts. Use the real calendar (`date`), name the weekday, and say "about" when a date depends on a letter that hasn't arrived. Where a rule depends on the state or the agreement, say "check <official link>" instead of guessing.

Write `jobs/layoff-plan.md` (this exact name, so `/today` finds it):

```
# Layoff plan
last_day: YYYY-MM-DD
where: <country / state>
updated: YYYY-MM-DD

## Dated deadlines
- [ ] YYYY-MM-DD (Thu): File for unemployment with <state agency> (<official link>). Benefits usually count from the week you file, so don't wait for severance or final pay.
- [ ] YYYY-MM-DD: ...

## This week, no fixed date
- [ ] ...

## Done
```

Rules for the plan:
- One line per action, earliest first, each with a date (or "this week"), the action in plain words, and the official link. `/today` shows any unchecked line due within 3 days, and marks it done when the user says so (`[x]`, moved under "Done" with the date).
- Only items that apply: no COBRA lines if they had no employer health plan; no severance lines without an agreement; no visa lines without a visa.
- Don't add tracker rows for these (the tracker is for jobs). The exceptions are real job leads: a former manager offering to help, or being rehired elsewhere in the same company, gets a tracker or contacts row as usual.
- Log one line in `history/activity.md` (`Layoff plan created; first deadline <date>`), no details.

Show the user the dated deadlines (not the whole file) and say which one is first.

## 3. Drafts that are worth doing this week (offer; draft only after a yes)

- **References and recommendations before people scatter.** Colleagues and managers are easiest to reach in the first days. Use `/network` to draft short notes to 2–4 people the user names: a reference ask (save them to `profile/references.md` only after the person agrees) or a LinkedIn recommendation ask (the user sends it inside LinkedIn themselves). Add each person to `contacts/contacts.csv` (`relationship=former-manager` or `former-colleague`).
- **A question about the severance package** (only if there's an agreement and the user wants to ask). One short, polite email in `outbox/` to HR or their manager: ask for time to review, clarify something, or make one specific request (more time, outplacement help, a neutral reference or agreed reference wording, the official departure reason, the end date of health coverage, keeping the laptop). Never invent leverage, never threaten, never suggest legal claims; if the user thinks they were treated unlawfully, that's a conversation for a lawyer first, before anything is sent. Run the usual voice pass.
- **A "still in touch" note** to people they'd like to keep, with personal contact details the user gives you (never take contacts from the employer's systems).

## 4. Update their files (with their OK)

- `profile/master-resume.md`: the end date for the job, and any wins they want recorded while they're fresh (show the exact change first).
- `profile/preferences.md`: a dated line under "Notes from conversations" ("Laid off from <employer>, last day <date>"); if they claim unemployment, offer `/work-search-log` (it records the state, the claim date and any registration deadline, and starts the weekly log). If a visa clock applies, offer to fill the visa lines (`visa_type`, `visa_clock_start` = the first counted unemployment day, not the last day worked, `visa_days_allowed`, `visa_days_used`, `visa_days_used_as_of`; the numbers come from the DSO, the official counter or an immigration lawyer).
- Their former employer may rehire or refer them later: offer to add the company's other teams to the search.

## 5. Then the search

Close with one next step, usually: "Want me to draft those reference notes now?" Then `/today` each session; the plan's dates show there until they're done. If they sound overwhelmed, give just the first deadline and one small task. If they express hopelessness or thoughts of self-harm, respond with care first and point them to local crisis resources (US: call or text 988; UK and Ireland: Samaritans, 116 123; anywhere else: findahelpline.com lists free local helplines by country) before anything job-related.

## Safety lines (never cross)

- Documents to keep are the user's own: pay stubs, benefits and pension statements, the agreement, letters, their own performance reviews if HR gives them out. Never suggest copying the employer's files, code, customer lists or email; that can break their agreement or the law.
- The user signs, files, certifies and sends everything themselves.
- For any question about whether a release is fair, whether to sign, discrimination, unpaid wages or immigration status: refer to an employment lawyer (US: the state bar's lawyer referral service; UK: Acas and a solicitor) or, for immigration, the school's DSO or an immigration lawyer.
