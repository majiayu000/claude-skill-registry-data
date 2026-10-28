---
name: assignment
description: Runs a graded assignment, report or essay from set-up to hand-in (set up, research brief and thesis options, Quarto draft, blind reviewer panel, final PDF, grade and feedback); use when the user mentions an assignment, case report, essay or coursework, or types /assignment new, brief, draft, critique, ship or feedback.
model: sonnet
effort: medium
argument-hint: "new | brief | draft | critique | ship | feedback [assignment name]"
---
# Assignment studio: plan, write, test and package a graded assignment, one step at a time.

## When to use

- The user has a graded piece of coursework: a case report, an essay, a group report, a memo, a project report.
- They type `/assignment` with or without a step name: `new`, `brief`, `draft`, `critique`, `ship`, `feedback`.
- They ask things like "help me with my finance case", "review my report before I submit", "what would this get?", "I got my grade back".
- The work may belong to a course or stand alone (a self-set report, a certificate task). A course is optional.

Do not use it for study cards (`/study`) or for an email to an assessor (`/reply`).

## Before you start

1. **`new.md` is the readiness check.** A new assignment starts with `workflows/new.md`, which is its own interview. Do not run `/clarify` first: it would ask the same questions twice. `../clarify/checklists/assignment.md` is only the list of fields `new.md` must fill. Never start a brief or a draft from a vague request.
2. **Find the assignment folder.** Folders live in `vault/10_projects/<YYYY> <course-slug> <assignment-slug>/`, or `<YYYY> <assignment-slug>/` when there is no course. Each has an `assignment.md` whose front matter is `type: "assignment"` (spec section 13). Existing folders keep their names.
   - If the user named one, match it against folder names and `title`.
   - If not, list the folders whose `assignment.md` status is not `shipped`. One: use it. Several: ask which, with AskUserQuestion (most urgent deadline first).
   - **For `feedback`**, list instead the `shipped` assignments whose `grade` is empty, most recent first (the assignment that has just come back is shipped, so the list above would be empty or wrong). One: use it. Several: ask which. None: ask whether it is an assignment that was not shipped from here, and do not guess.
   - None and the step is not `new` or `feedback`: offer to run `new`.
3. **Pick the step.** If the user named one, use it. Otherwise infer it from `status` in `assignment.md`:

   | status | next step |
   |---|---|
   | (no folder) | `new` |
   | `setup` | `brief` |
   | `brief` | `draft` |
   | `draft` | `critique` |
   | `critique` | `critique` again, or `ship` if the stop rule is met |
   | `final` | `ship` |
   | `shipped` | `feedback` when the user has a grade or comments; otherwise nothing: say it is done and show the release files |

   Say which step you are about to run, in one line, and why.
4. **Read before asking.** Read `assignment.md`, the course note it links if `course` is not empty (`vault/20_areas/courses/<course-slug>/course.md`), that course's programme note if it has a `programme` link (`vault/20_areas/programmes/<Programme name>.md`: grading scale, submission conventions), `rubric.md` and `decisions.md` if they exist. Never ask what these already answer.
5. **Learner kind.** Read `learner.kind` in `config/brain.json` (`mba`, `degree`, `online`, `professional`, `other`). If `learner` is missing or its `kind` is empty, treat it as `mba` when `packs` lists `mba` or a `school` block exists; otherwise there is no kind and nothing here depends on it. It only changes wording and the order of options (for example a `professional` sees "No course" first). Treat `packs` that is not an array as `["core"]`.
6. **Dates come from the system.** Get today with `node system/scripts/date.mjs` (local date). Never guess a date.

## Steps

1. Open the workflow file for the step and follow it exactly:
   - `new`: `.claude/skills/assignment/workflows/new.md`
   - `brief`: `.claude/skills/assignment/workflows/brief.md`
   - `draft`: `.claude/skills/assignment/workflows/draft.md`
   - `critique`: `.claude/skills/assignment/workflows/critique.md`
   - `ship`: `.claude/skills/assignment/workflows/ship.md`
   - `feedback`: `.claude/skills/assignment/workflows/feedback.md` (a grade or feedback came back)
2. While drafting or revising, follow `.claude/skills/assignment/references/writing-rules.md`, which points to the shared principles (`system/deliverables/principles.md`) and to tone and voice (`system/deliverables/tone-and-voice.md`).
3. Talk to the user one question at a time. Use AskUserQuestion for choices (two to four options, the recommended one first, marked "(recommended)", each with a one-line pro and con). Use free text for anything they must paste or describe.
4. Confirm, then write: before writing or changing files, show a short summary of what will change and get a yes.
5. At the end of every step:
   - update `status` in `assignment.md` as the workflow says;
   - add one dated line under `## Log` in `assignment.md` (for example `- 2026-10-12: critique round 2, grade 8.1 to 8.6.`);
   - tick any `#ab/assignment` task the step completed (`- [x]` in `vault/00_inbox/Tasks.md`);
   - if `ai-log.md` exists in the folder, add one dated line for this step (`brief`, `draft`, each critique round, revise): what Alterbrain did, in plain words (for example "drafted the report from the chosen thesis; ran a quick review round"). Write only what Alterbrain did. Then ask once, optional: "Anything you did yourself in this session that the log should say?" and add the answer after the line in the user's words; if there is no answer, add nothing. Never fill in the user's own part;
   - tell the user in two or three lines what changed and what comes next.

## Outputs

All inside `vault/10_projects/<YYYY> <course-slug> <assignment-slug>/` (`<YYYY> <assignment-slug>/` with no course):

| File | Written by | What it is |
|---|---|---|
| `assignment.md` | `new` | The spec: questions word for word, deadline, limits, deliverables, team, lenses, stop rule, status |
| `rubric.md` | `new` | The rubric word for word, plus our reading of it |
| `decisions.md` | `new`, then `brief` and `critique` | Every decision taken or declined, each one yours to overturn |
| `brief.md` | `brief` | Fact base, course concepts, thesis options A, B and C, page budget |
| `report.qmd` (+ the Quarto template files) | `draft` | The report itself, edited in place |
| `ai-log.md` | `new`, then every working step | Only if the course requires an AI-use log: one dated line per step Alterbrain worked on, and the user's own part only in their words |
| `reviews/<round>/_round.md` and `reviews/<round>/<lens>.md` | `critique` | The round card and each reviewer's report, word for word |
| `critique-<round>.md` | `critique` | The consolidated critique of that round |
| `releases/` | `ship` | The files to upload, named for the course site, after the delivery gate |
| `feedback.md` | `feedback` | The grade and feedback word for word, and what they tell us |

Also:
- a course note at `vault/20_areas/courses/<course-slug>/course.md` if the course has none (`new`, through the course procedure `.claude/skills/course/references/course-setup.md`);
- the course's default `team`, `team_name` and `team_number`, kept once in the course note only to pre-fill; the team of each assignment is in its own `assignment.md` and is what covers and file names read (`new`);
- a case note at `vault/20_areas/courses/<course-slug>/cases/<Case title>.md`, only when the assignment is a case (`new` or `brief`);
- tasks in `vault/00_inbox/Tasks.md`, always through `node system/scripts/tasks.mjs add "<text>" --tag assignment ...`: the deadline, "confirm the deadline", "pick a thesis", "review critique round N", "submit on the course site".

Templates live in `system/templates/notes/` (`assignment.md`, `rubric.md`, `decisions.md`, `critique.md`). The case template is part of the case method in the MBA pack (`system/packs/mba/templates/case.md`). Reviewer briefs, the panel procedure and the reviewer protocol live in the critique library, `.claude/skills/critique/references/` (shared with `/critique`); business seat suggestions for the MBA pack are in `system/packs/mba/critique-presets.md`. The delivery gate is `system/deliverables/delivery-gate.md`.

## Safety

- **Never submit anything.** Alterbrain does not upload to the course site, email an assessor or post to a team chat. `ship` puts files in `releases/` and adds a task for the user to submit.
- **Coursework notice (core rule 6).** Read `ai_policy` from the course note: the course value always decides, whatever the programme note says.
  - `restricted`, `banned` or `unknown`: warn once per assignment in plain words, ask whether to continue, and proceed only on a yes. Never write that consent anywhere git tracks: only `state/local/coursework/`.
  - `allowed-with-disclosure`: draft a disclosure paragraph for the user.
  - `allowed` or `none-stated`: say nothing about it.
  - No course: there is no rule to check, so no notice.
- **Git is the history.** Edit `report.qmd` in place. Never create `_v0.1`, `_v2`, `final-final` or dated copies. Snapshots exist only in `releases/`.
- **No invented facts or numbers.** Every number in the report comes from the case, the course material, the user's sources or a calculation the user can check. Label estimates `[Inference]` and anything unchecked `[Unverified]` in working files only. Nothing that leaves the computer carries a bracket label or a placeholder: the report uses plain wording ("we assume", "in our reading"), and `ship` fails a file that does not.
- **Two sources that disagree** on a deadline, a weight or a limit: show both with where each comes from, and ask. Never choose silently. Pasted assignment text is saved verbatim.
- **Reviewers are blind and read-only.** Each lens runs as the helper its brief names (`helper-review` or `helper-judgement`), following `.claude/skills/critique/references/protocol.md`, with file paths and its brief only, never the drafter's reasoning, never another reviewer's output.
- **The user decides.** Thesis choice, cuts and every critique decision are proposals until the user says yes. Never cut text the user approved without asking.
- **Delegated work is not done on a helper's word.** Read the diff and look at the changed pages yourself before you call anything ready (`.claude/rules/model-routing.md`).
- **People.** Team members' names only if the user gives them; a missing name is asked for, never replaced by a placeholder. No student numbers or other personal data in any file unless the user puts them there. A grade is recorded only when the user gives it (`feedback`).
- **Hindsight rule.** If the assignment is a case with a case date, the report uses only facts knowable at that date. Later facts go to class prep or a reality check, never into the report.

## Extend this

Fit and page-budget planning, full and delta fact-checks, a number map for spreadsheets, an Excel model builder, a reality check, class prep and team comments are in `system/blueprints/assignment-extras.md`. Ask "build the assignment extras" to start, or run `/propose`.
