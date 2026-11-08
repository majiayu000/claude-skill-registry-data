---
name: apply-kit
description: "While the user fills in an online application form themselves, print every answer the form will ask for (contact details, work authorization, start date, relocation, salary, self-identification choice, education, each past job, the job's own questions with drafted answers, and which files to upload) as copyable blocks, then mark the job applied when they say they submitted. Use when the user says apply kit, 'I'm filling out the application now', 'what do I put for…' on a form, or asks for their answers to copy."
---

# Apply Kit (chat version)

The chat version of the Claude Apply Kit panel. Read-only, except marking the job applied when the user says they submitted. Never show or store sensitive data (SSN, date of birth, ID, bank or passport numbers, passwords): if a file holds any, leave it out, tell the user to type it into the employer's site themselves, and offer to remove it from the file. Judge by the value, not just the question: a yes/no answer to "Do you have a driver's license?" or a company name containing "Bank" is fine to show; an ID-like number, a full date of birth or an account number is not.

## 1. Pick the job

Read `jobs/tracker.csv` fresh (tolerate a byte-order mark, Windows line endings, quoted commas, and Excel dates like `10/14/2026`, read as AGENTS.md says in "Reading dates someone else wrote"; a date that is still unclear shows as "date unclear" and is never rewritten). If the user named a job, use that row (match the `folder`, or company + role). Otherwise use the `interested` job whose `next_action` starts with `Review package and submit` (if several, the one with the soonest `deadline`, then `next_action_date`). If there is none, list the `interested` jobs and ask which one, one question only. If nothing is `interested`, say so and offer `add-job` or `find-jobs`.

## 2. Gather (read, never guess)

- `profile/master-resume.md` → Contact (name, email, phone, city, LinkedIn, portfolio), Education, Experience. Skip anything inside `<!-- -->` comments (those are templates, not facts).
- `profile/preferences.md` → `name`, `home_base`, the `- Work authorization (<country>):` and `- Needs sponsorship (<country>):` lines for the job's country (match the country in brackets; if there's no line for that country, or it says `Not sure`, it's `[not set]`), Earliest start date, relocation (a relocation line, or the Locations line if it mentions relocating), Willing to travel, Salary floor (for the job's country), and the Voluntary self-identification section.
- The job folder `jobs/<folder>/`: `posting.md` header (`apply_link`, `job_id`, `deadline`, `documents`, `questions`), `application-answers.md` (each question is a heading or bold line with the answer under it), and which of these exist: the resume's sources (`resume.md`, `resume.html`, `resume.rendercv.yaml`, or `cv.html` for an academic or Europass CV), the cover letter's (`cover-letter.md`, `cover-letter.html`) and the PDFs.

Any value that is empty or still says `[ASK]` prints as `[not set]`, with a note that the user can tell you the answer and you'll add it to their profile (ask before changing it). Never fill a gap from memory or inference (AGENTS.md ground rule 1).

## 3. Print the kit

Plain headings, and **each answer in its own fenced code block** so the user can copy it with one click (Codex and most chat apps show a copy button on code blocks). Label above each block. Order:

1. **This job:** company and role, apply link, job ID (if any), deadline, and the contact's name if the tracker has one (for the referral field, only if that person referred them).
2. **Contact details:** full name, email, phone, city and state, LinkedIn, portfolio (optional).
3. **Eligibility and preferences:** work authorization and sponsorship as two separate blocks, earliest start date, willing to relocate, willing to travel, salary expectation. The salary expectation comes from, in order: this job's drafted salary answer in `application-answers.md`, a desired salary the user recorded, the posting's `pay_range`, otherwise `Negotiable` (and offer a market range for this job if the form forces a number). Never invent one. The salary floor is shown only as plain text labelled "Your minimum (don't type this)", never in a copy block.
4. **Voluntary self-identification:** show only what the user confirmed. "Use these on applications" = yes → the recorded answers (any still `[ASK]`: "answer this one yourself"); "decide each time" → say they chose to decide each time and print no answers; decline → tell them to pick "I don't wish to answer" for each; not set → say these are optional, they can answer on the form or ask you to record a choice. Never guess these.
5. **Education:** school, location, degree and major, dates, other listed details.
6. **Work history (for forms that make you retype your resume):** one block per job, newest first: employer, job title, start, end, location, and the description bullets as one copyable block.
7. **This job's application questions:** each question with its drafted answer from `application-answers.md`. Voluntary self-identification questions (race/ethnicity, gender, disability, veteran) found here follow the user's choice in item 4, not the drafted text: "decide each time", decline or not set → no copy block, only the same note as item 4. Any answer with a bracketed blank like `[ASK]`, `[ASK: ...]` or `[Your answer]`, and any certification or attestation question ("I certify the information is true", legal declarations, "I agree to the terms"): no copy block; label it "Only you can answer this". List any question in the posting's `questions` that has no drafted answer as "Not drafted yet". If there is no answers file, say so and offer to draft the answers now (the `apply` skill, step 2).
8. **Files to upload:** `<First>-<Last>-Resume-<Company>.pdf` and, if used, `<First>-<Last>-Cover-Letter-<Company>.pdf` (name hyphenated, from preferences or the master resume). For each say whether the PDF is in the job folder and newer than every source file that exists (resume: `resume.md`, `resume.html` or `cv.html`, `resume.rendercv.yaml`; cover letter: `cover-letter.md`, `cover-letter.html`) (if it's older than any of them, say "This PDF is out of date; make a new one first" and offer it, as in the `apply` skill step 1), or the `.html` (`resume.html`, `cv.html` or `cover-letter.html`) is ready to print, but only once its text has passed its checks (for a resume or CV, `resume-notes.md` beside it has the requirement coverage, written after the checks; a `cover-letter.html` is built only after them); otherwise say it still needs its checks and offer to finish them (ready: open it in a browser → Print → Save as PDF with that name), or it isn't made yet (offer `tailor-resume` / `cover-letter`). A cover letter the posting doesn't ask for: "Not needed". List other `documents` (transcript, portfolio) as "you provide this one".

End with one line: "Tell me when you've submitted it and I'll mark it applied and set your follow-up."

## 4. When the user says they submitted

Only when they say it happened, and with the real date they applied ("yesterday" means yesterday). Re-read `jobs/tracker.csv` right before the change and edit only that row (targeted edit, plain characters with accents kept, the playbook's CSV rules for quoting and formula protection, dates as `YYYY-MM-DD`). If the row is no longer `interested`, change nothing and tell them what it says.

- `status=applied`, `date_applied` = the date they applied
- `next_action=Follow up` (or `Follow up with <contact>` if the row has a contact)
- `next_action_date` = 7 business days after applying (playbook "Follow-up cadence": applied online, 7–10 business days), or 4 business days for an hourly or shift job (`employment:` part-time, temporary or seasonal in `posting.md`, or pay posted per hour)
- `followups=0`

Then add one line to `history/activity.md` (`date '+%Y-%m-%d %H:%M'` for the time; Windows PowerShell: `Get-Date -Format 'yyyy-MM-dd HH:mm'`; e.g. `- 2026-10-06 14:05 · Codex · Acme Corp (Operations Analyst): marked applied on 2026-10-06; follow-up set for 2026-10-15`), re-read the row to confirm, and tell the user in one sentence when the follow-up is. Finish the rest of the `apply` skill's step 6 (a recruiter question in the Outbox, a referral noted in `contacts/contacts.csv`). If the save fails because Excel has the file open, ask them to save and close it, then try again.

## The Claude panel (Claude Code only; Codex: skip)

In Claude Code the same kit is the `/apply-kit` panel: every answer for one job with a Copy button (contact details, work authorization and sponsorship per country, start date, relocation, the job's salary answer, their self-identification choice, education, each job, the job's questions from `application-answers.md`, PDF file names). The salary floor from preferences shows only as "Your minimum — don't type this", with no Copy button. It is read-only except **Mark applied…**: that sets the row to applied today, follow-up in 7 business days, `followups=0`, adds a line to `history/activity.md`, and leaves an `[Apply Kit]` note. Don't re-apply that change; finish the rest of `apply` step 6 (a recruiter question, a referral in contacts). If they applied on another day, fix the dates.
