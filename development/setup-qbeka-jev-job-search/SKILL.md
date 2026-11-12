---
name: setup
description: First-run setup, start to finish. Use when the user says /setup, "set this up", "get me started", "help me use this", hands you this repository for the first time, or when data/profile.json does not exist. Installs what is missing, builds the profile from the resume and a short interview, has the user add their own JEV key (TypeSafe or OpenRouter), finds jobs, rehearses, and stops for a "go" before anything is sent.
model: claude-sonnet-5-5
effort: high
---

# /setup: from a fresh clone to the first applications

The user should need to do four things: give you their resume, answer your
questions, paste one key into a file, and say "go". You do everything else.

Run every command from the repo root. After each step run
`npx jev doctor --json`. It lists what is in place and names the
next thing to do, so you never have to guess where you are. If the user
stops halfway and comes back, start from what `doctor` says.

## 1. Install

1. If `node_modules` is missing, run `npm install`.
2. Run `npx jev doctor`. Fix what it names, in order:
   - Node.js older than 22, Google Chrome missing, or Claude Code missing:
     tell the user what to install and wait. You cannot install these.
     (You are running inside Claude Code, so it is present; a user who
     prefers a Claude API key can add `ANTHROPIC_API_KEY` to `.env` and the
     commands use the API instead.)
   - Everything else is covered by the steps below.

## 2. The resume, and anything else in documents/

Look in `documents/` first. Besides `resume.pdf`, a user may have put past
material there for you to read: old resumes, a LinkedIn profile export as
PDF, transcripts, past applications, a portfolio page saved as PDF. Read
every PDF and text file there (the Read tool opens PDFs). Each is a source
for the profile in step 3: a bullet, a date, a project, a skill that the
current resume leaves out. Nothing personal in `documents/` is ever
committed; the folder is git-ignored apart from its README. Re-running
`/setup` after more files land there is safe: it adds, it does not
overwrite what the user confirmed.


1. Ask for the resume as a PDF. The user can drag the file into the chat or
   give its path.
2. Copy it to `documents/resume.pdf`.
3. Read the PDF. It is your first source for the profile.

## 3. The profile

Build `data/profile.json` in the shape of `data/profile.example.json`.
The schema is `src/profile/schema.ts`.

1. Fill in everything the resume states: name, contact details, links,
   education, each job and project with its bullets, skills.
2. Ask the user what the resume does not state. The full list is in
   [questions.md](questions.md). Follow it top to bottom, and skip a
   question only when the resume or the user has already answered it.
   Ask in small groups, at most four questions at a time. Use
   AskUserQuestion when a question has a fixed set of answers.
3. Write `summary` (three or four sentences: who they are, what they want,
   where, when) and `facts` (one line per claim, every number exact, copied
   from the resume or said by the user).
4. Write `answers`, the standing answers, from part G of the questions.
5. Show the user a short summary of the profile and correct what they flag.
6. Run `doctor` again. A schema error names the field to fix.

Rules for this step:

- Never invent or round a fact. If you are not sure, ask.
- Never guess a demographic answer. Every one of them can be declined.
- `resume.path` is the absolute path of `documents/resume.pdf`.
- These files are git-ignored. Never commit them and never paste their
  contents into a file that is tracked.

## 4. Their voice and their drafts

1. Copy `data/voice.md` to `data/voice.local.md`.
2. Write `data/bank.json` in the shape of `data/bank.example.json`: one
   starting draft per common question, from the user's own facts. Keep the
   text in braces where an answer depends on the company.
3. Draft one sample answer to "Why do you want to work here?" for a made-up
   company and ask whether it sounds like them. Adjust
   `data/voice.local.md` and the drafts until it does. One or two rounds is
   enough.

## 5. The key

JEV is the only part of this tool the user is billed for. Tell them the
numbers before they pay: about 6 cents each time the tool finds jobs, and
about 1 cent for every 10 applications. Five dollars of credit lasts for
months.

1. Ask them to create a key and add a few dollars of credit, at either
   https://console.typesafe.ai/keys (TypeSafe, who make JEV) or
   https://openrouter.ai/keys (OpenRouter, who resell it). The model and
   the price are the same.
2. Run `cp .env.example .env`, then `open -e .env` so the file opens in a
   text editor.
3. Ask them to paste a TypeSafe key after `TYPESAFE_API_KEY=`, or an
   OpenRouter key after `OPENROUTER_API_KEY=`, save, and tell you when it
   is done.
4. Run `npx jev doctor --online`. It makes one tiny JEV call and
   one tiny Claude call to prove both work.

Never ask the user to paste the key into the chat, and never print it. If
they paste it into the chat anyway, tell them to delete that key where they
made it (console.typesafe.ai/keys or openrouter.ai/keys) and create a new one, because a key in a chat is exposed.

## 6. Find jobs

Run `npx jev discover`. It takes about a minute. Show the top 15
as a short table: score, company, role, location, date posted. Say how many
jobs are queued and name the main reasons jobs were skipped
(`npx jev status`).

If the user wants other locations or kinds of roles than the ranking
prefers, the settings are in `src/config.ts` (`LOCATION_MULTIPLIER`,
`FIT_WEIGHTS`, `DISCOVER`).

## 7. Rehearse

1. Run `npx jev apply --dry --count 3`. A Chrome window opens,
   three forms are filled, nothing is sent, and the tabs close.
2. Show the user every answer, grouped by form. Point out anything the tool
   held and why.
3. For each answer the user corrects, change the profile: a fact, or a
   standing answer in `answers`. Then rehearse again. Do not move on until
   the user says the answers are right.

Tell the user one thing before the first rehearsal: some job boards save a
form as it is typed, so a rehearsal there leaves an unsent draft on that
board. It is not an application and the employer is not told.

## 8. One application, ready for them to read

Setup ends with a real application filled and waiting, not with a list of
commands. Run `npx jev apply --count 1` on the best job in the queue that
is on Greenhouse, Lever or Ashby. Without `--submit` the form is filled,
checked and left open in the tool's Chrome window.

Tell them to look at that window. Read the answers back to them, name
anything the tool held, and ask: "Send this one?" Only when they say yes,
run `npx jev submit <id>`. Then show the row in `npx jev log`.

That is the whole loop. Say so in one sentence, then stop asking
questions.

## 9. What is next, in three lines

Do not list commands. Say only:

- `/apply` sends more: they say how many.
- `/report` is the dashboard: what was sent, what needs them, and the
  switch for a daily run.
- `/status` says where things stand at any time.

Mention these once, and only when they apply. Do not set any of them up
during setup:

- If many of the jobs they would want are on Workday (`npx jev status`
  lists "workday" among the skip reasons), say that Workday employers each
  want an account and `/accounts` handles that when they are ready.
- If they asked for it to run by itself, `/daily`.

Two things the tool will not do, so they are not surprised: it does not
pass a "prove you are human" check, and it does not sign in anywhere
unless they set that up. A form that needs them stays open in the tool's
window; `/resume` picks it up.
