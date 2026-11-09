---
name: job-apply
description: Submit a job application through the employer's ATS (Greenhouse, Lever, Ashby, Teamtailor, Workable, Recruitee, Breezy, traffit, SmartRecruiters, LinkedIn Easy Apply) with Playwright, then record it in the Job Hunt funnel. Use when asked to apply to a job, send a CV / resume to a posting, or run the application script for a URL. Needs the dashboard running at http://localhost:4321 and Chrome installed.
---

# job-apply — one application, by script

The browser work is done by [scripts/apply.mjs](../../../scripts/apply.mjs)
(Playwright on the installed Chrome). You never read forms or take
screenshots: you run a command and read one JSON line.

## Facts the forms need

[profile.json](profile.json) is the single source for every field: name,
phone, links, CV path, salary (number per currency and a sentence), notice
period, work authorisation, languages, education, work history. Edit it,
never the script, when a fact changes. [profile.md](profile.md) is the same
in prose, with the reasoning behind each answer. Both are personal and stay
out of git; a fresh checkout starts by copying profile.example.json and
profile.example.md to those names.

## Run it

```
node scripts/apply.mjs <applyUrl> --url <postingUrl> --company "<co>" --title "<title>" \
     --source <indeed|linkedin|himalayas> --cover auto --stack "<comma list from jobs-fetch>" \
     [--location ".."] [--salary ".."] [--pay '<PayRange[] json>'] [--answers <json>] [--office-ok] [--dry-run] [--headed] [--debug]
```

- `--office-ok`: the company is one of the giants in Settings → "My terms"
  (Google, Apple, Netflix, Meta, Microsoft, Amazon, Nvidia, …; `OFFICE_OK` in
  src/profile.ts reads them) and the office is in the city named there (Warsaw). Then LinkedIn's Hybrid/On-site tag does not stop the run.

- `applyUrl` is the ATS page (`applyUrl` from `jobs-fetch`), `--url` is the
  posting as the dashboard knows it — that is the funnel's dedupe key.
- `--cover auto` writes a four-paragraph letter from a template, adding one
  sentence per stack hint (LLM, GraphQL, Electron, Next.js, accessibility).
  Pass a file path or text instead to write your own.
- `--pay` is the posting's published ranges (the dashboard's `pay`, e.g.
  `[{"contract":"b2b","min":5800,"max":8300,"currency":"USD","unit":"month"}]`):
  a salary field asks for the top of the range on its contract and currency
  when that beats profile.json's figure. Without it the profile's figures stand.
- `--dry-run` fills everything, submits nothing, saves a full-page screenshot
  under `~/.job-hunt/shots/` and prints the field→value map. Use it the first
  time a new board shows up.

Result line (stdout, JSON) and exit code:

| `result` | exit | Meaning / what to do |
| --- | --- | --- |
| `applied` | 0 | Submitted and confirmed; `funnel` says `#id inserted`. Done. |
| `dry-run` | 0 | Filled, not sent. Read `filled`, then run again without `--dry-run`. |
| `missing-answers` | 2 | A required field matched no rule. `missing[]` lists label (cut at 200 characters: the `--answers` key), the whole `question`, type and options. Write `{"label substring": "answer"}` into a JSON file and re-run with `--answers`. For dropdowns the answer may be `"a|b|c"` — alternatives in order of preference. Open questions: 3–4 sentences, plain words, facts from the CV only. |
| `submit-failed` | 3 | Submit clicked, no confirmation. `errors[]` has the validation text; `screenshot` shows the page. Fix the rule, re-run. |
| `no-form` / `needs-account` / `captcha` | 4 | Nothing to fill, or the board wants an account or a CAPTCHA. Hand the URL to the user — never create accounts, never solve CAPTCHAs. |
| `board-form` | 4 | A job board's posting whose application only its own form takes: justjoin.it offers without an employer link, every NoFluffJobs posting (both its modes sit behind a CAPTCHA), Himalayas. Answered at once, no browser opened. Hand the posting to the user. |
| `closed` | 4 | The board says the offer is gone. Hide the job; not recorded as an attempt. |
| `not-remote` | 5 | LinkedIn's own tag says hybrid/on-site. Hide the job with that reason — unless it is a giant's Warsaw office: re-run with `--office-ok`. |
| `needs-code` | 6 | The board e-mailed a "confirm you're a human" code (Greenhouse does). Re-run with `--headed`: the window stays open and the **user** types the code. The script never reads the mailbox. |

Rules live in `answerFor()` in the script: label regex → value. When a
`missing-answers` label is one that will recur (a new phrasing of "notice
period", a Polish label), put the answer in the bank instead of an
`--answers` file:

```
node scripts/apply.mjs --remember "<label substring>" "<answer>"
```

It goes into `answers` in profile.json and is used on every later form
(after this run's `--answers`, before the built-in rules). Only facts the user
has confirmed go in the bank; ask when unsure.

Every outcome short of `applied` is recorded as an attempt (the dashboard's
"needs you" list, `node scripts/funnel.mjs attempts`) until the job is applied
to or hidden — no need to keep a list in the chat.

## Boards

| Board | Entry | Notes |
| --- | --- | --- |
| Greenhouse (`job-boards.greenhouse.io`, `.eu.`, or any page with `?gh_jid=` — an embedded board in an iframe) | form on the posting page | react-select dropdowns; "Enter manually" opens the cover-letter box; **e-mails an 8-character security code** on submit → the board runs headed and the user types it (`needs-code` when headless). A `thank you for applying` e-mail from `greenhouse-mail.io` is the proof of receipt; the script's `applied` means the form was replaced by a confirmation |
| Lever | `/apply` | plain form |
| Ashby | `/application` | "Autofill from resume" first, then fields |
| Teamtailor (`careers.<co>.com/jobs/<id>-slug`) | "Apply for this job" | parses the CV, wait ~7 s |
| Workable (`apply.workable.com`) | "Apply now" | multi-step |
| Recruitee (`<co>.recruitee.com/o/<slug>`) | `/c/new` | free-text question takes the cover letter |
| Breezy (`<co>.breezy.hr/p/<id>`) | `/apply` | currency + period selects next to the salary number; Work History / Education are parsed from the CV |
| traffit (`<co>.traffit.com/public/an/<hash>`) | the apply link's href (`/public/form/a/…`), whatever its text — employers rename it («join cerebre»), so it is found by its target | Polish labels: kraj, miasto, obszar technologiczny, rola projektowa, stawka PLN/h |
| SmartRecruiters | "I'm interested" → `oneclick-ui` | one long form |
| LinkedIn (logged-in profile) | the job page | Reads the Remote/Hybrid/On-site chip first (`not-remote` otherwise). **Easy Apply** = native `<dialog>` with `Next` → `Review` → `Submit application`. **"Apply on company website"** (`data-view-name="job-apply-button"`) opens a "Share your profile?" dialog → the script presses Continue, then follows the new tab to the employer's ATS and continues there (often an embedded Ashby/Greenhouse iframe, which the script opens standalone) |
| justjoin.it (`justjoin.it/job-offer/<slug>`) | the offer's `applyUrl` in the page data | the script reads it first and fills the employer's form (traffit, recruitee, Greenhouse…; 65 of 86 offers on 2026-10-24); `null` = justjoin's own form → `board-form` |
| NoFluffJobs, Himalayas | — | `board-form` at once: NFJ gates both its form and its redirect with a CAPTCHA; Himalayas hides the employer's link behind Cloudflare |
| Workday, Cognizant, EPAM, Luxoft, Indeed Apply | — | account required → `needs-account`, list for the user |

LinkedIn login is a one-off: `node scripts/apply.mjs --login` opens a window on
the automation profile (`~/.job-hunt/chrome-profile`); the user logs in and
closes it. Other boards use `~/.job-hunt/chrome-profile-ats`, so a LinkedIn
window never blocks them.

## Batch

```
node scripts/apply-batch.mjs --fetched <fetched.json> [--only 2,10] [--skip 5] [--answers <dir>] [--dry-run] [--out results.json]
```

One line per job: `idx | company — title | result | detail | seconds`. Rows
that need an account, errored in fetch, or are closed are reported as
`skipped`. `--answers <dir>` picks `<dir>/<idx>.json` per job. Re-running with
the same `--out` skips rows already `applied`.

## What "applied" means

`applied` is printed when the submit button was pressed, the form is gone and
the page shows an application-specific confirmation (`thank you for applying`,
`application submitted`…). Generic "thank you" text is not enough — job
descriptions contain it. Boards that confirm by e-mail (Greenhouse, Breezy,
Ashby when configured) can be double-checked in the inbox; a CAPTCHA puzzle
(Recruitee uses one) or a security code means the submission did **not** go
through until the user finishes it.

## Hard limits

No account creation, no passwords, no CAPTCHAs, no verification codes read
from the mailbox, no fields the profile does not answer (they come back as
`missing-answers`). A successful submit is recorded immediately in the
funnel as `applied` via `POST /api/applications`.
