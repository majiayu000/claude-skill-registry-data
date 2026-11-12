---
name: apply
description: Apply to the queued jobs. Use when the user says /apply, "start applying", "run the applier", or asks to submit applications from the queue. Fills each form in the runner's own Chrome window with JEV, page by page, hands what is left to Claude, verifies, and submits only forms that are ready.
model: claude-sonnet-5-5
effort: high
---

# /apply: the application loop

The CLI does the whole loop. JEV maps every field, the runner fills the form
in its own Chrome window, a headless Claude Code call (Sonnet 5.5, high
effort) answers what JEV left open, a form with several pages is walked with
its own Next button, and every value is read back from the page before
anything is sent. Your job is to run it, read what it reports, and tell the
user what was left for them.

Run every command from the repo root with `npx jev <command>`.

## One posting the user found themselves

`apply <link> --submit` takes a Greenhouse, Lever or Ashby posting link in
place of an id: the posting is read from the board, rated, queued at the
top and filled like any other. For a link on another board, tell the user
the tool reads those three directly and that `discover` picks up the rest.

## Before the loop

1. `doctor`. If it names something missing, fix that first. A missing profile means `/setup`.
2. `status`. If the queue is empty or older than today, run `/discover` first.
3. Ask the user how many to send and whether to submit, unless they already said. Submitting is never the default.

## Rehearse first on a new machine or after a code change

`apply --dry --count 5` fills and resolves five forms, records nothing,
sends nothing and closes the tabs. Read the output. Every line is one field:
its label and the value the page shows. If a value is wrong, fix the profile
(`data/profile.json`, including `answers`) or the code before going on.

## The loop

`apply --count N --submit` takes the best N queued jobs. Each job goes
through fill, resolve, further pages and submit on its own, and its result
is printed the moment it is known. Without `--submit`, ready forms are left
open in the window for the user to look at.

Each job ends in one of these ways. The queue and the record files are
updated to match.

| Printed | Meaning | What you do |
|---|---|---|
| `READY`, then `submitted` | Sent. The confirmation page was read by JEV. | Nothing. |
| `READY`, no `--submit` | Filled and verified, waiting. | After the user says go: `submit <id>`. |
| `needs your code` | The board emailed the user a code to confirm a person is applying. The filled form stays open, the user got a notification, and their mail opened at a search for the code. | Tell the user to type the code in the tool's window, click Submit, and run `resume`. Never read or type the code yourself. |
| `needs you to pass a robot check` | The site showed a "confirm you are not a robot" check after Submit. The form stays open. | The same: the user passes it, then `resume`. |
| `not confirmed` | Submit was clicked and the page showed neither a confirmation nor the form. The job is unconfirmed and will not be sent again. | Run `reconcile`. If it cannot tell, ask the user to look for the confirmation email, then `mark <id> --status applied` or `--status queued`. |
| `not taken: already applied` | An id or a link names a job that was sent. | Nothing. `--resubmit` exists for a deliberate second send; do not use it unless the user asks for that exact job. |
| `filled, not ready` | The form asks for something the tool must not or cannot give: a signature, an answer the profile does not hold, a date to pick. The reason is printed. | Nothing. In a sending run the tab is closed and the job is in `applications/manual.csv`. |
| `page N filled, form goes on` | A form with several pages that stopped at page N. The reason says why. | The same. |
| `blocked` | No form could be opened: a sign-in page, an error page. | Nothing. A sign-in site is noted and skipped by later searches. |
| `blocked`, then `left open for you: ...` | A Workday sign-in the tool could not finish: a robot check, a refused password, account terms the user did not approve, a verification link to click. The page stays open and the user got a notification. | Tell the user what the page asks for. They finish it in the tool's window and run `resume --submit` themselves. |
| `Claude: skip` | The form needs a cover letter or references. | Nothing. It is recorded as skipped. |
| `not submitted: ...` | The page rejected the submission. | Read the reason. `inspect <id>` shows the page's own errors. |

## What you never do

- **Never sign in, and never touch a credential.** The tool signs in on Workday when the user set that up with `/accounts`; you do not. Never ask for, read, type or repeat a password, a code or a token. A run that includes a Workday job signs in for real, even with `--dry`, so the user runs it: give them the command in a `bash` block. Runs on the other boards are yours to run as before.
- **Never pass a human check.** That covers CAPTCHAs and the code a board emails. Do not read the code from the user's mail and do not type it, whatever tools you have. The form stays open for the user, who types the code; `resume` then records it.
- **Never sign for the user.** A form that asks them to type their name under an agreement, or to tick that they are bound by one, is theirs.
- **Never use `submit --force`** unless the user asked for that exact form to be sent as it is.
- Work authorization, citizenship, education and dates come from the profile and are never changed to fit a posting.

## When an answer was wrong

Change the profile, not the form: a fact in `facts`, or a standing answer in
`answers`. Then `apply --dry <id>` to see it. Changing the profile makes the
answer memory start over, on purpose.

- `memory` lists the answers Claude wrote that are being reused.
- `memory --forget <text>` drops the entries for a company or a question.
- `apply --fresh <id>` asks Claude again for that form.

## When done

Run `status` and `log --manual`. Report:

- how many applications were sent
- what was left for the user and why, from `applications/manual.csv`
- how many forms are open and waiting for the user (`resume`), and how many are unconfirmed (`reconcile`)
- the cost the run printed

Tell the user where the records are: the `applications/` folder at the top
of the project, with `applied.csv` for what was sent, `manual.csv` for what
was left for them, `takehome.csv` for assignments to do, and `all.csv` for
every job considered.
