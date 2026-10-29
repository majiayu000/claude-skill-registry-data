---
name: setup
description: Interview the user one question at a time and write the project's rules file, goals file, handoff file and release checklist. Use when starting a new app, adopting The Last Mile in an existing project, or when the user asks to set up or redo their project rules.
---

# Setup

Run a short interview, then write four files from the templates in this skill's
`templates/` folder. The whole thing should take about 10 minutes of the user's time.

## Rules for the interview

- **One question at a time.** Wait for the answer before asking the next.
- **Offer a sensible default in every question** so a short answer is enough.
- **Read before asking.** If the project already has a CLAUDE.md, AGENTS.md, README
  or app.json, read them first and only ask what they do not already answer.
  Confirm what you inferred in one line instead of asking it again.
- **Look at the user's other projects too.** Sibling folders (the project's parent,
  and wherever their other repos live) may hold a rules file that already has a
  **How to talk to me** section or standing decisions marked as applying to every
  repo. Offer to carry those over in one line instead of asking question 4 and the
  push question again. Copy only the personal parts, never another app's settings.
- **Never overwrite** an existing file without showing the user what would change
  and getting a yes. Prefer merging new sections into an existing rules file.
- A screenshot is a perfectly good answer. If the user sends one, use it.

## The questions

Ask these in order. Skip any the project already answers.

1. **What does the app do?** Ask for one sentence.
2. **What is the loop?** The thing a person does, start to finish, that gives them
   what they came for. Example: "add a plant, get a reminder, mark it watered". If
   they cannot say it in one sentence, help them cut it down.
3. **Who is it for?** One specific kind of person and the moment they reach for the app.
4. **How should Claude talk to you?** Offer choices: short and direct; detailed with
   reasoning; plain words with no code names. Ask if there is anything they never want
   to see (some people dislike long dashes, jargon, or recaps).
5. **How do you push code?** Straight to main, or to a branch with a pull request.
   Default: a branch with a pull request, unless they work alone and prefer main.
6. **What command runs your checks?** Default: whatever `package.json` defines as
   `check`, or lint, typecheck and test in that order. Offer to add a `check` script.
   Run the command once before moving on. A first run can install tools or write
   config files (Expo's linter does both); those changes belong to setup, and the
   user should know whether the checks start clean.
7. **What is your first 6 week goal?** Offer the default for their stage:
   - Idea only: "A working version of the loop on my own phone by <date>."
   - Working build: "Live in the App Store (and Google Play) by <date>." For a
     website: "Live at its own domain, with real people signed up, by <date>."
   - Live: "First 100 people using it every week by <date>."
   Then ask for the one number that shows it is working, and 3 to 5 must dos. The set-goals skill's `references/stages.md` has fuller defaults
   for each stage.
8. **Where does it run?** Both stores, iOS only, Android only, or web only (a
   website that never goes to a store). Default: both stores, unless the code is a
   web framework with no app build, then web only. Mention that a new personal
   Google Play account must run a 14 day closed test first, which is why some
   people ship iOS first.
9. **How much before the first launch?** Offer the three levels from the ship skill's
   `references/levels.md`, one line each: Quick ship (the least the stores accept,
   free at launch), Standard (the default: crash reporting, a tested release build, a
   listing written to be found, paid features if any), Full features (analytics,
   subscriptions with a trial, preview video, localized listings). Skip this
   question for a web only project and write `not applicable (web)`.

## What to write

| File | From template | Notes |
| --- | --- | --- |
| `CLAUDE.md` | `templates/rules-file.md` | If the user's agent reads `AGENTS.md` instead, write that and make `CLAUDE.md` point to it |
| `GOALS.md` | `templates/goals.md` | End date is 6 weeks from today |
| `CURRENT_WORK.md` | `templates/current-work.md` | The handoff file session end keeps current |
| `RELEASE_TEST_CHECKLIST.md` | `templates/release-checklist.md` | For a web only project, items are checked on the live site after each deploy |

Fill every placeholder in angle brackets. Date every entry you write, in
`YYYY-MM-DD` form. Remove template sections that do not apply rather than leaving
them empty.

## Finish

Show the user a short summary: the four files written, their goal and end date,
and the skills to use next: connect-tools now, to connect the services the app
uses, session-end every session, see-it-work to see a change
working, reference-hunt before designing a screen, research before a decision,
set-goals when the cycle ends, ship when getting into the stores, and setup again
if anything about the answers changes. Then
offer to commit the files, following the push choice from question 5.
