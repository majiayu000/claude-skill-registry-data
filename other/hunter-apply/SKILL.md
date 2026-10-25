---
name: hunter-apply
description: >-
  The Application Assistant. Fills the user's job applications from their
  own saved answers and leaves every one as a draft for them to review and
  submit: maps each form question to hunter/profile.json (name, links, work
  authorization, sponsorship, start date, relocation and more), flags what
  only the user can answer (salary, voluntary self-identification, anything
  not in the profile), runs a per-application checklist (tailored resume,
  cover letter, research, warm intro), fills the form in the user's browser
  with Claude in Chrome and stops before Submit. Use when the user says
  "apply to this job", "fill out the application", "fill the Greenhouse
  form", "prep my application", "what's left before I apply", or "save it as
  a draft".
argument-hint: "[role id]"
---

# hunter-apply

Most of an application is the same twenty questions. This skill answers
those from the user's own saved answers, asks about the rest, fills the form
in their browser, and stops with the Submit button untouched. The user reads
it, fixes anything, and submits it themselves.

What the user typed after `/hunter-apply`: `$ARGUMENTS`

Tool in this folder (standard library Python; it never submits anything):

```bash
python3 "${CLAUDE_SKILL_DIR}/answers.py" --help
```

## What it reads and writes

- `hunter/profile.json`: the user's facts and reusable answers. The shape
  every hunter skill reads is `profile.example.json` in this folder (the
  reel's fictional Jordan Reyes). Anything left `null` is asked, never
  guessed.
- `hunter/applications/<role-id>.json`: the answer plan for one form.
- `hunter/pipeline.json`: the role gets `"application": {"status": "draft",
  ...}`, next step "Review the application draft and submit it yourself";
  after the user submits, stage `applied` and the date.
- Reads `hunter/resumes/<role-id>.md`, `hunter/covers/<role-id>.md` and
  `hunter/companies/<company>.md` for the checklist.

## The rules

- **Only the user's truth.** Every filled answer comes from the profile or a
  document the user approved. Nothing is invented: no experience, title,
  degree, date, number, referral or reason.
- **Some answers are the user's alone.** Voluntary self-identification
  (gender, race or ethnicity, veteran, disability) is answered only with the
  user's own saved choice, or left for them. Salary history is the user's
  call (several US states and cities bar employers from asking): never
  estimate it. A salary expectation comes from the user, informed by
  `/hunter-salary`.
- **No accounts, no passwords, no CAPTCHAs.** If a site needs a sign-in
  (Workday often does), the user signs in. Claude never creates an account,
  types a password or solves a CAPTCHA.
- **Stop before Submit.** Never click Submit, Apply or Send on a form.

## Steps

1. Checklist first:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/answers.py" checklist --role <role-id>
   ```

   Tailored resume (`/hunter-resume`), cover letter if the form takes one
   (`/hunter-cover`), research brief (`/hunter-research`), work
   authorization in the profile, and ideally a warm intro (`/hunter-connector`).
2. With the user present, open the application in their browser with Claude
   in Chrome and read the form. Write its questions, as labelled, to a JSON
   list (with `options` for selects and `required` where marked).
3. Map them:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/answers.py" fill --questions form.json --role <role-id> --out hunter/applications/<role-id>.json
   python3 "${CLAUDE_SKILL_DIR}/answers.py" answer --question "Will you now or in the future require sponsorship?"
   ```

   `fill` rows go in as they are. `ASK` rows: ask the user, and offer to save
   the answer to `hunter/profile.json` for next time. `USER` rows: the user
   answers them. `ROLE` rows: the approved cover letter or a short answer
   written for this role from the research brief.
4. Fill the form field by field at a human pace. Attach the tailored resume
   the user picks. Review every page with the user.
5. Stop before Submit. If the site offers "save for later" and the user is
   signed in, use it only with their yes. Record the draft:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/answers.py" draft --role <role-id> --form-url <url> --answers hunter/applications/<role-id>.json
   ```

6. The user reviews and clicks Submit. When they say they did:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/answers.py" submitted --role <role-id> --confirm "I submitted it"
   ```

   The role moves to `applied`, with a follow-up date a week out for
   `/hunter-followup`.

## Example: the reel

Jordan Reyes (fictional) applies for the Software Engineer role at Google
after his coffee chat with Maya C. is booked. The checklist shows the
tailored resume, the cover letter and the Google brief are done. On the
form, `fill` answers 9 questions from his profile (name, email, LinkedIn,
"authorized to work in the United States": Yes, "require sponsorship": No,
relocation: Yes, never worked at Google: No), asks him for his phone number,
his salary expectation and a non-compete question it cannot know, leaves
gender, veteran status and current salary to him, and marks "Why Google?"
for the cover letter. Claude fills the form in his browser and stops. The
pipeline shows "Draft · not sent" until Jordan reads it and clicks Submit
himself.

## What it never does

- Never submits an application, clicks Submit or Apply, or sends a form.
- Never invents an answer, a referral, a salary history or a demographic answer.
- Never creates an account, types a password or solves a CAPTCHA.
- Never applies in bulk or on a schedule: one application at a time, with
  the user there.

## Consent

- Nothing is sent or submitted without the user's explicit yes for that exact
  message or application. Claude fills the form and leaves it for the user to
  submit from their own browser and their own account.
- No bulk or automated applying, no scraping behind logins, no tricks around
  a site's limits or CAPTCHAs.
- The user's personal data goes only into the form they chose to fill, and
  voluntary questions stay theirs to answer.
- Outreach that comes with an application follows the connector's stop rules:
  stop at the first no, at most 2 follow-ups, nothing after 21 days of
  silence, and a stop request is honoured forever.
