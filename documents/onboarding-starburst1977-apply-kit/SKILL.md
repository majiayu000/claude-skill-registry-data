---
name: onboarding
description: Sets up a job seeker's profile before any CV or cover letter is written. Imports their existing CV and LinkedIn PDF, checks the career timeline for contradictions between sources, captures what they are targeting, sets up their letterhead and renders a first CV as PDF; optionally deepens the profile with role interviews, a numbers audit and a voice sample. Use at the start of every session in this kit when profile/onboarding.md is missing or has an unchecked Quick start step, and whenever the user says "start", "set me up", "onboarding", "import my CV", "update my profile" or "deepen my profile".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(node --version), Bash(npm install), Bash(npm run pdf:*)
---

# Onboarding

Builds the user's profile so that every later CV and letter rests on confirmed facts.
Quick start: about 15 minutes, ends with their first CV as a PDF. Deepen: optional.

## How to run it

1. Open `profile/onboarding.md`. If it is missing, copy it from
   `.claude/skills/onboarding/templates/onboarding.md`.
2. Find the first unchecked step. Tell the user in one line where they are and how long is left.
   On the very first run: "About 15 minutes, 4 short steps, and you'll have your first CV as a
   PDF. Stop whenever you like, I'll pick up where we left off."
3. Run that step with the reference file below. Save to the profile files as you go, never
   only at the end: the user may close the window at any moment.
4. Tick the box, note anything needed to resume under "Notes", go to the next step.
5. After step 4, hand over (end of quick-start.md). Go into Deepen only when the user asks.

| Steps | Instructions |
|---|---|
| 0 to 4, Quick start | [references/quick-start.md](references/quick-start.md) |
| 5 to 7, Deepen; "update my profile" | [references/deepen.md](references/deepen.md) |

Templates for the profile files are in `.claude/skills/onboarding/templates/`. Copy one the
first time its file is needed. Document format: `guide/format.md`.

## Rules

- **Never invent a fact.** Everything in `experience.md` comes from the user's files or their
  answers. If something is missing, ask, or leave it out.
- **Never invent, round or "improve" a number.** Copy numbers exactly as found and tag them
  `[unconfirmed]`. They become `[source: …]` only when the user confirms them. Only sourced
  numbers ever go into a CV or letter.
- **Never settle a conflict between sources yourself.** Two files disagree on a date, a title
  or a count: record both, ask the user.
- **Don't ask what the files already answer.** Confirm instead: "Your CV says …, still right?"
- **Batch small questions** into one numbered message, so the user can answer in a few words.
- **Plain language.** Run every command yourself. Never mention npm, Node or the terminal
  unless something fails, and then say what to do in one sentence.
- **Gaps and personal matters:** ask once, neutrally, and accept "leave it as is".
- **Use the user's language.** If they write German, run the whole onboarding in German.

## Gotchas

- Sources disagree about the same role (dates; "4" in one file, "8" in another). → List every
  conflict in step 2. Never average, never pick the more impressive one.
- Numbers travel from old CVs into new ones with nobody knowing where they came from. → Tag
  `[unconfirmed]` on import; the step 4 check keeps only what the user stands behind.
- Two jobs with overlapping dates can be real (parallel roles, freelancing) or a typo. → Ask.
- A role appears in one source but not another. → Ask whether to include it; don't drop it.
- A fact found in only one file can't be contradicted, so a wrong one slips through: the user
  confirms it from memory. → Mark single-source facts "(one source)" in step 2 and ask for a
  second look. Same for numbers: measured / estimate / not sure, never plain yes or no.
- Word or Pages files don't read reliably. → Ask for PDF.
- LinkedIn PDFs carry page footers, endorsements and "Top skills" lists. → Take roles, dates,
  headline and About; ignore the rest.
- LinkedIn's own PDF export prints only what is expanded on screen, so role bullets end
  mid-sentence and extra roles are missing entirely. Reported by a first buyer, 2026.
  → Tell the user to expand every "see more" and "show all experiences" before saving, and
  in step 2 flag every truncated line back to them instead of importing half a sentence.
- A LinkedIn page printed from the browser is cut off partway and can include the private
  messaging sidebar. → Never use or quote messages. For the missing part, ask for a screenshot.
- A role missing from every file can't be found by comparing files. → Step 2 always ends by
  asking what's missing (freelance work, side businesses, short contracts).
- A shell command that checks for something missing (`ls node_modules` in a fresh kit) exits
  with an error, and the app shows it as a red "Failed" line: alarming as a first impression.
  → Check files with Glob or Read. Only run commands that are expected to succeed.
- Setup ran before the greeting, so the user's first sight was a setup log. → Welcome first.
- `node --version` fails. → The user must install Node themselves (see quick-start.md, step 0).
  Don't try to install it for them.
- `npm install` downloads a browser for PDF rendering and takes a minute or two. → Say so
  before running it, so the silence doesn't worry them.
