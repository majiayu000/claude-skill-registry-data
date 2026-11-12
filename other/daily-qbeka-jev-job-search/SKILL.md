---
name: daily
description: The daily run, which sends a few applications a day with nobody watching, inside the user's standing policy. Use when the user says /daily, with or without a subcommand (setup, dry, run, schedule, stop), "run it every day", "automate this", "schedule it", or asks about the daily limits or data/policy.json.
argument-hint: "[setup | dry [n] | run | schedule [HH:MM] | pause | stop]"
model: claude-sonnet-5-5
effort: medium
---

# /daily

The user types a short command; you run the tool for them. They should
never have to type `npx`. `docs/DAILY.md` is the reference. The daily run
is off until the user turns it on.

## What the user can type

| They type | You do |
|---|---|
| `/daily` | Run `npx jev schedule status` and read today's `data/runs/daily-<date>.json` if there is one. Say what is set up and how today went. If `data/policy.json` does not exist, go to setup. |
| `/daily setup` | The questions below, then write `data/policy.json` after a yes. |
| `/daily dry` or `/daily dry 3` | `npx jev daily --dry --target <n>` (3 when no number). Read the summary with them. |
| `/daily run` | `npx jev daily`. They typed it, so that is their go for today's run. Read the summary back when it ends. |
| `/daily schedule` or `/daily schedule 08:30` | `npx jev schedule install --at <time>` (09:00 when no time). Say: the Mac must be on and signed in at that time, the tool's Chrome window will open, `/daily pause` removes it again, and `/daily stop` stops a run that is working. |
| `/daily pause` | `npx jev schedule remove`. No further run starts by itself. Say that a run already working carries on. |
| `/daily stop` | `npx jev daily --stop`. The run that is working finishes the application it is on and opens no other. Say that this does not remove the schedule; `/daily pause` does. |

If `npx jev accounts` shows Workday is allowed, a daily run signs in at
employers. Then you do not start `dry` or `run` yourself: show the command
in a `bash` block, which has a Run button, and let them click it.

## Setup: the standing policy

If `data/profile.json` is missing, do `/setup` first. Then ask, one
question at a time:

- How many applications a day? 15 is the default; 25 is the most.
- Where may the jobs be? (Vancouver, the rest of Canada, remote, the
  United States, elsewhere.)
- Internships, new-grad roles, or both?
- Is there a fit score below which you would rather not apply? Show the
  spread in their queue (`npx jev queue`) so the number means something.
- Any employers to leave out?
- A resume written for each job, and a cover letter where a form has a
  box for one? This takes longer per job.
- How much may JEV cost in a day? 50 cents is the default; a normal day
  is a few cents. Say that this limits JEV only: Claude is on their
  subscription, or on their own API key, and is not counted.

Write `data/policy.json` in the shape of `data/policy.example.json`, show
it to them, and save it only after a yes. Then offer `/daily dry`.

## What you never do

- **Never start a real run or install the schedule unless the user typed
  that command** (`/daily run`, `/daily schedule`) in this conversation.
  A general "set it up" is not that.
- **Never write or change `data/policy.json` beyond what the user said.**
- **Never raise a limit in `DAILY` to send more.** If they ask for more
  than 25 a day, say why: no rate is known to be safe, and a board that
  decides one person is a robot stops taking their applications.
- If the permission system declines a command, do not try another way.
  Show the command in a `bash` block for them to run with one click.

## Reading a summary

- "Waiting for you": a human check or a sign-in only they can pass. They
  finish it in the tool's Chrome window, then `/resume`.
- "Clicked and not confirmed": `/resume` settles these too.
- A board left alone until tomorrow asked for a human check. That is the
  tool being careful, not a fault.
