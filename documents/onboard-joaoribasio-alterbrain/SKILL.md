---
name: onboard
description: Set up Alterbrain for a new user through a friendly, resumable interview (setup, identity, profile, what you are learning or doing, autonomy, then optional voice, career, email, brand and file import); use on first run, when the user says "set me up", "/onboard", "continue setup", or asks to redo one setup step.
model: sonnet
effort: medium
argument-hint: "[status | next | M0-M9 or a name like voice, career, gmail | later]"
---

# Onboard

Get to know the user and set up their Alterbrain, one friendly question at a time.

## When to use

- First run: `state/onboarding.json` is missing or its `status` is `not_started`.
- The session digest says setup is incomplete, **after** the user's own request is handled.
- The user says "/onboard", "set me up", "continue setup", "let's do the voice part", "connect my Gmail".
- `/reconfigure` asks to re-run one module.

It is a ritual, not a gate. Never block another skill because onboarding is unfinished.

## Before you start

0. **Are my safety rules loaded?** The session digest (a block that starts "Alterbrain digest") must be in your context. If it is not, this session started before the folder had its rules, hooks and permissions, so setup would run without its safety checks. Say exactly: "Please close this session and open the folder again, so my safety rules load. Then type /onboard." Then stop. Do not run any module. (`status` only reads, so it may still run.)
1. **The user's request comes first.** If they arrived with a real question or job, do that first. Then offer setup in one line: "When you have about 25 minutes, I can set myself up for you. Say `/onboard`." (Use `estimate_minutes.minimum` from the next step, rounded; the time depends on what the user is learning or doing.)
2. Read where we are: `node system/scripts/onboard-progress.mjs show --json`. It also gives `learner_kind` (what the user is learning or doing; `null` until M2 asks) and `estimate_minutes` (`minimum` and `remaining` for the essentials). The plain `show` lists the minutes per module. Module titles always come from the script. Schema: `references/state.md`.
3. Read what already exists before asking anything:
   - `vault/80_me/USER.md`, `IDENTITY.md`, `SOUL.md`, `fact-sheet.md`;
   - `config/brain.json` (including `learner` and `packs`), `config/autonomy.json`, `config/mcp.selected.json`;
   - `vault/20_areas/programmes/*.md`, `vault/20_areas/courses/*/course.md`, `vault/10_projects/*/project.md` and `vault/20_areas/career/career.md`.
   Never ask what these already answer. Say "I can see you are at …; is that still right?" instead.
4. Get today's date from the system: `node system/scripts/date.mjs --now` (local time). Never guess a date.
5. Clarify does not apply here. This skill *is* the interview.

### How to talk during onboarding

- **One question at a time.** Wait for the answer before the next one.
- **Choices:** use AskUserQuestion with 2–4 options. Put the recommended option first and add "(recommended)".
- **Stories and facts:** ask in free text ("Tell me in two or three lines about…").
- **Infer before asking.** If the user points to a CV, LinkedIn PDF, syllabus or folder, read it first (Read tool handles PDFs). Then ask only to confirm or fill gaps.
- **Confirm, then write.** Before writing a file, show a short summary ("I'll save this: …. OK?"). Write only after a yes.
- **Plain UK English.** Short sentences. Explain any unavoidable term in one line (for example "GitHub: a private online backup of your Alterbrain").
- **Show progress.** At the start of each module say its name, what it is for, and the time ("Step 2 of 5, about 3 minutes").
- **Escape hatch.** Every module accepts "later", "skip" or "stop". Never make the user feel behind.

## Steps

1. **Pick the module.**
   - With an argument (`M5`, `voice`, `gmail`…), run that module.
   - `status`: print `node system/scripts/onboard-progress.mjs show` in plain words and stop.
   - `later`: run the graceful exit (step 5) for the current module.
   - No argument: run `node system/scripts/onboard-progress.mjs next --json` and continue from there. If a module has a `note`, resume from it ("Last time we stopped at course 2. Shall we carry on?").
2. **First time only: welcome.** Three short lines: what Alterbrain is (a second brain and a writing twin that lives in this folder), that nothing is sent without their OK, and that the essentials take about `estimate_minutes.minimum` minutes (the learner question in M2 sharpens it) and can stop any time. Ask: "Ready to start?" (Start now (recommended) / Later).
3. **Run the module.** Mark it started: `node system/scripts/onboard-progress.mjs start <id>`. Then follow its workflow file exactly:

   | id | Module | File | Essential? |
   |---|---|---|---|
   | M0 | Setup (checks, folders, GitHub backup, optional encryption of private notes, Obsidian) | `workflows/M0-setup.md` | yes |
   | M1 | Identity and tone | `workflows/M1-identity.md` | yes |
   | M2 | You and your facts | `workflows/M2-you-and-facts.md` | yes |
   | M3 | Courses and projects (courses with their material, or focus areas and projects) | `workflows/M3-programme.md` | yes |
   | M4 | Autonomy and self-build | `workflows/M4-autonomy.md` | yes |
   | M5 | Your writing voice | `workflows/M5-voice.md` | later |
   | M6 | Career and job search | `workflows/M6-career.md` | later |
   | M7 | Email and tools | `workflows/M7-integrations.md` | later |
   | M8 | Look of your documents | `workflows/M8-brand.md` | later |
   | M9 | Import your existing files | `workflows/M9-import.md` | later |

4. **Close the module.** When its done criteria are met: `node system/scripts/onboard-progress.mjs done <id>`, tick any matching `#ab/onboard` task (`node system/scripts/tasks.mjs done "<task text>"`), and say in one line what was saved and where. Then:
   - essentials not finished: offer the next essential module, with the minutes `show` lists for this kind of learner ("Next: your courses, about 6 minutes with the syllabi only, longer if you bring all your course files. Carry on?" Carry on (recommended) / Later);
   - essentials just finished: go to step 6.
5. **Graceful exit ("later", "stop", or the user changes topic).**
   - Save what was already confirmed. Do not write half-confirmed answers.
   - `node system/scripts/onboard-progress.mjs later <id> --note "<where we stopped, one line>"`.
   - Add one task (no duplicates; check `vault/00_inbox/Tasks.md` first):
     `node system/scripts/tasks.mjs add "Finish setting up Alterbrain: <module title> (~N min). Say /onboard" --tag onboard --priority medium`
   - Say: "Saved. We'll pick up at <module> whenever you like." Then help with whatever they want.
   - **"Skip"** on an optional module (M5–M9): `node system/scripts/onboard-progress.mjs skip <id>`, no task. On an essential module (M0–M4): say in one line what won't work without it, then treat it as "later".
6. **Essentials done (M0–M4).** Celebrate in one line. Then offer the optional modules, one question:
   "Want to do another now, or shall I add them to your task list?" Options: Add them to my tasks (recommended) / Do one now / Not now.
   - Tasks: one per open optional module, tag `onboard`, priority `low`, text from the table below.
   - Then suggest three first things to try (from `/menu`), matched to what they told you and to what they are learning or doing.

   | Module | Task text |
   |---|---|
   | M5 | Teach Alterbrain your writing voice (~15 min). Say /onboard voice |
   | M6 | Set up your job search (~10 min). Say /onboard career |
   | M7 | Connect Gmail and pick extra tools (~8 min). Say /onboard gmail |
   | M8 | Choose fonts and colours for your documents (~5 min). Say /onboard brand |
   | M9 | Import your existing study or work files (~10 min). Say /onboard import |

   Leave out the M9 task for a user who is not studying (`learner_kind` `professional`) unless they mentioned files to import.

7. **Re-running a finished module.** Show what is saved now, in plain words, and ask what to change. Change only that. Do not repeat questions with answers that are still right.

### Model routing inside onboarding

- Interview, summaries, file writing: this skill (sonnet / medium).
- Reading a CV, LinkedIn PDF or syllabus to pull out fields: sonnet / medium in the main thread, or the `helper-triage` agent (haiku / low) for a long list of files.
- Voice profile writing (M5): the `helper-judgement` agent (opus / high; see `workflows/M5-voice.md`). If it cannot run, this skill writes the profile itself and says so in one line.
- Mechanical work (copying templates, stats, config generation): scripts only.

## Outputs

- `state/onboarding.json`: per-module status and timestamps (only via `system/scripts/onboard-progress.mjs`).
- `vault/80_me/IDENTITY.md`, `SOUL.md` (Vibe section), `USER.md`, `fact-sheet.md`, `voice/<lang>/profile.md`, `voice/<lang>/exemplars.md`, `brand/_brand.yml`.
- `config/brain.json` (`learner`, `packs` and the rest), `config/autonomy.json`, `config/mcp.selected.json`, `.mcp.json` (generated by `system/scripts/mcp-gen.mjs`).
- `vault/20_areas/programmes/<Programme name>.md` (once per programme, see "The programme note" in `.claude/skills/course/references/course-setup.md`), `vault/20_areas/courses/<course-slug>/course.md` (with its Material list, same file), `vault/10_projects/<YYYY> <project-slug>/project.md` (working, not studying), `vault/20_areas/career/career.md`.
- Raw copies of files the user shares, via `system/scripts/ingest.mjs` (never written by hand).
- Tasks tagged `#ab/onboard` for later steps. Deadlines found in syllabi and course material still to come are tagged `#ab/course`.

## Safety

- Never ask for a password, API key or token in chat. If a step needs one, tell the user to type it into `.env.local` themselves (see `workflows/M7-integrations.md`).
- Only write facts the user confirmed. Nothing inferred goes into `USER.md` or `fact-sheet.md` without a yes.
- Never change the **Boundaries** section of `SOUL.md` or anything in `system/`.
- Personal documents (CV, LinkedIn export) go through `ingest.mjs`, so they live in the user's private repo with a source record. Say so in one line.
- Course AI policies: copy the exact sentence into `ai_policy_quote`. Look in this order: the course's own syllabus or page, then the programme's rule (copied into the course only after the user confirms it, with the quote starting "Programme rule: "), then ask. Nothing found: `ai_policy: "unknown"` for a programme course (it keeps warning until the user confirms there is no rule), and `none-stated` for an online course from a provider that states none, or when the user confirms that no rule exists. Never guess a policy.
- Never write the `school` block in `config/brain.json`. The programme note replaces it; older installs keep the block and only its display text is read.
- Install software only after the user says yes to that one install (see `workflows/M0-setup.md`), one package at a time, and never retry in a loop. Never sign in or create an account for the user: GitHub sign-in is their click in their browser.
- If a script fails, explain it in one plain line, add a `#ab/onboard` task with the fix, and move on to the next module where possible.
