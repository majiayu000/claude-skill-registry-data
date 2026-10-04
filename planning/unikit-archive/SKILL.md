---
name: unikit-archive
description: >-
  Archive completed plans. Moves finished folder plans from .unikit/code/plans/<folder>/
  to .unikit/code/archive/plans/<folder>/, so plan lookup and the plan lists stop offering
  them; an unfinished plan moves only when the user picks it, and is marked as unfinished.
  Lists every plan with its created and last-change dates; plans can be picked by number
  or by date. Never deletes, renames or commits. Use when user says "archive plans",
  "archive completed", "archive old plans", "clean up plans", or "show archived plans".
  Not for .unikit/code/PLAN.md or FIX_PLAN.md; to check that a plan is really done use
  /unikit-verify, to commit the move use /unikit-commit.
argument-hint: "[list | --all | <plan-folder>]"
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(git *)
  - Bash(mv *)
  - Bash(mkdir *)
  - Bash(date *)
disable-model-invocation: false
---

# Plan Archive

Move finished folder plans out of `.unikit/code/plans/` into `.unikit/code/archive/plans/`. Plan lookup in `/unikit-implement`, `/unikit-verify` and `/unikit-improve`, the plan lists and the "latest plan" choice walk `.unikit/code/plans/*/` and nothing else, so an archived plan simply stops being offered — there is no index to update. Nothing is deleted and nothing is committed.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

Skill-specific rule:
- Everything said to the user — the step lines, the table, the questions and their options, the summary — is in `language.ui`, including a remark made while a command runs. The question texts and option labels quoted in this skill are templates: say them in `language.ui`. Git, file listings and scratch output are data, never a reason to answer in English.

## Scope

**Archived:** a folder plan `.unikit/code/plans/<folder>/` — full or ultra, current or legacy layout, any folder name format (`<name>`, `YYYY-MM-DD_<name>`, `DDD-<name>`) — once Step 2 calls it `completed` and the user has answered any follow-up question; or, `incomplete`, once the user has seen what is left and chosen to archive it unfinished (the unfinished question).

**Never touched:**
- `.unikit/code/PLAN.md` — the fast plan; `/unikit-implement` offers to delete it when it is done.
- `.unikit/code/FIX_PLAN.md` — `/unikit-fix` deletes it.
- researches (`.unikit/code/researches/`, `.unikit/gamedesign/researches/`) — open plans and `GD-IDS.yaml` point at them by path.
- patches (`.unikit/code/patches/`) — `/unikit-evolve` reads them.
- `.unikit/ROADMAP.md`.

**The folder name never changes.** It is how an archived plan is found again: the `Plan: <folder>` trailer that `/unikit-commit` writes names it, and an explicit path `@.unikit/code/archive/plans/<folder>` still works wherever a skill accepts one.

## Step 0: Context

**First, announce the mode** (Step 1 → **Announce the mode first**): the argument alone decides it, and its announcement is the run's first output — before these reads.

1. Read `.unikit/skill-context/unikit-archive/SKILL.md` if it exists — project-level overrides; on conflict the skill-context wins.
2. Read `git.enabled` from `.unikit/config.yaml`. A missing file or key counts as enabled.
3. Get today's date: `date +%Y-%m-%d`.

## Step 1: Mode

| `$ARGUMENTS` | mode |
|---|---|
| empty | **interactive** — classify every plan, ask which completed ones to archive |
| `list` | **list** — show what is already archived, then stop |
| `--all` | **all** — archive every plan that qualifies, after one confirmation |
| anything else | **one plan** — the named folder; a leading `@` and a leading `.unikit/code/plans/` are stripped first |

`list` or `--all` together with a folder name → `ERROR [archive] conflicting arguments: <args>` and stop.

**Announce the mode first.** Classifying thirty plans takes minutes, and a run that says nothing for that long reads as a hang. Right after the language rules are loaded, the run's **very first output** — before Step 0 and before any other sentence, and not a word about the language or the config — is one or two plain sentences in `language.ui`:

- interactive: `I'll check every plan in .unikit/code/plans/ — how far each one got and what is left to hand over — then ask which completed ones to archive. Nothing moves before you answer.`
- `list`: `Showing the plans already archived.`
- `--all`: `I'll check every plan and archive the completed ones after one confirmation.`
- one plan: `I'll check <folder> and archive it if every task is done.`

**Then say what you are doing, as you do it.** Before each step that reads, runs or writes something, one short line in `language.ui` saying what is happening right now — `Found 30 plan folders — checking each one…`, `Reading the dates from git…`, `Looking for MCP findings that never reached the notes…`, `Moving <folder>…`. One line per step, at the moment it starts: not a plan announced in advance, and not a retelling of what went fine. The per-folder `INFO [archive]` lines of Step 2 are the progress of the longest step.

**What the user must see, print as your own message.** Tool output is folded away from the user: a table, a list or an `INFO [archive]` line that only a command printed never reaches the screen. The table, the lists printed before a question and the summary are printed as your own message, in full — never left in a script's output, never cut down to a one-line summary.

## Step 2: Classify a plan folder

Run this for every folder the mode looks at. It reads, it never writes.

1. **Task file.** The folder's legacy task file `TASKS.md` when it has one (a pre-merge plan), otherwise `.unikit/code/plans/<folder>/PLAN.md`. Neither → verdict `not a plan`.
2. **Scope.** The `## Checklist` section of the task file — from that heading to the next `## ` heading. No such heading → the whole file. Lines inside fenced code blocks never count.
3. **Checkbox lines.** A line that starts, after indentation, with `- [` + one character + `] `. `x` or `X` inside the brackets is done. **Any other mark is unfinished** — a space (open), `~` (in progress), `!` (failed). A phase status line such as `**Status:** [ ] Not started` does not start with `- [` and is not a checkbox line.
4. **Verdict.**
   - `completed` — at least one done line and no unfinished line.
   - `incomplete (<done>/<total>)` — at least one unfinished line.
   - `empty` — no checkbox line at all. An empty plan is not archived.
5. **Ultra bundle.** The task file's first line is `<!-- unikit:plan-mode:ultra -->` → every link under its `## Phase Index` heading must resolve to an existing file directly inside the folder. A missing one → verdict `broken bundle (<missing file>)`, not archived.
6. **Follow-ups** — checked for a `completed` plan only. Each is **a question, never a stop**: the plan stays archivable, and the mode asks the user through [the follow-up question](#the-follow-up-question).
   - **MCP findings not transferred.** The task file's `## MCP Findings` table has rows (a row's first cell is `F<n>`), and at least one of them has no back-reference in `.unikit/MCP-RECHECK-NOTES.md` or in a parked `.unikit/MCP-RECHECK-NOTES.archive.*.md` — the installer parks the notes there when the engine server changes. The back-reference of row `F<n>` is the text `<folder>/<task file name>#F<n>`: `/unikit-mcp-trap` writes it into every note it takes from a plan, so it is the exact record of what was moved. No notes file at all → nothing was transferred. A missing back-reference is not always a loss: `/unikit-mcp-trap` lets the user decline a finding, and a declined row leaves no back-reference behind; `/unikit-mcp-audit` removes a note it retires together with its back-reference.
   - **Rule candidates never proposed.** A row of `## Rule Candidates` has the status `open`.

   The verdict names what is left: `completed, <k> MCP findings not transferred`, `completed, <m> open rule candidates`, or both.
7. **Dates** — shown next to the verdict, so the user can tell a finished plan from a forgotten one. Dates are `YYYY-MM-DD`; `—` when nothing below answers.
   - **Created:** the task file's `Created: YYYY-MM-DD` header line; else the `YYYY-MM-DD_` prefix of the folder name; else the date of the commit that added the task file — the last line of `git log --diff-filter=A --format=%as -- <task file>`.
   - **Last change:** run `git status --porcelain -- .unikit/code/plans/` once per run. A folder listed there has changes no commit holds yet → `date -r <task file> +%Y-%m-%d`. Otherwise `git log -1 --format=%as -- .unikit/code/plans/<folder>/`. Without git (`git.enabled: false`, or not a work tree) → `date -r <task file> +%Y-%m-%d`.

Print one line per folder as it is classified: `INFO [archive] <folder>: <verdict>`.

**Commands that handle a follow-up:** untransferred findings → `/unikit-mcp-trap .unikit/code/plans/<folder>/<task file name>`; open rule candidates → `/unikit-verify <folder>` — it proposes them and records each as `added` or `declined`.

## Step 3: Modes

### The follow-up question

Asked once per run, for every plan about to be archived that has a follow-up left. First print, per plan, the findings rows that have no back-reference and the open rule candidates, then:

```
AskUserQuestion: <folder list> still have follow-ups: <k> MCP findings not transferred to .unikit/MCP-RECHECK-NOTES.md, <m> rule candidates never proposed.

Options:
1. Handle them first — leave these plans in place
2. Archive anyway — the rows move with the plan, and /unikit-mcp-trap and /unikit-verify will no longer find them
3. Cancel
```

Name only the kinds that are present.

- "Handle them first" → these plans are not archived — the summary lists them under `Skipped` as `follow-ups left` — and print the command for each (see above). The other chosen plans are archived.
- "Archive anyway" → archive them as usual.
- "Cancel" → archive nothing and stop.

### The unfinished question

Asked once per run, for every chosen plan whose verdict is `incomplete`. First print, per plan, what is left: each unfinished checkbox line — its task id and the start of its text; more than five → the first five and `… and <k> more`. Then:

```
AskUserQuestion: <n> of the chosen plans are unfinished: <folder list>. Archived, they are no longer offered to /unikit-implement and /unikit-verify, and their open tasks go with them.

Options:
1. Archive them unfinished — the manifest says so
2. Only the completed ones — leave these in place
3. Cancel
```

- "Archive them unfinished" → archive them; Step 4 writes the unfinished label.
- "Only the completed ones" → they are listed under `Skipped` as `unfinished — left in place`.
- "Cancel" → archive nothing and stop.

An `empty`, `broken bundle` or `not a plan` folder never reaches this question: it is never archived, and a chosen one is listed under `Skipped` with its verdict.

### list

Glob `.unikit/code/archive/plans/*/`. None → `Archive is empty — no plan has been archived yet.` and stop. Otherwise print each folder with the date from its `Archived:` line (`—` when the line is missing) and `unfinished` when that line says so, then `Total: <n> archived plans`, and stop.

### interactive

1. Classify every folder in `.unikit/code/plans/` and print a table as your own message, one row per folder: # · folder · verdict · created · last change, the oldest last change first — a plan nobody has touched for weeks is what the user is deciding about. `#` numbers the rows for the question below: ask it only once the whole table is on screen — the options name rows by `#`, and without the table the user chooses blind.
2. No folder is `completed` or `incomplete` → `No plan can be archived now.` and stop.
3. Ask which plans. A plan with follow-ups is marked in the table with them, e.g. `(2 MCP findings not transferred, 1 open rule candidate)`.

   ```
   AskUserQuestion: Archive which plans?

   Options:
   1. All <n> completed — only when there are completed plans
   2. Choose by number or date — type it: "3, 5-7", "created on or before 2026-09-14", "not changed since 2026-09-01"
   3. Cancel
   ```

   Option 2 asks the user to type: say its label by that meaning, never as "the listed ones". Its answer arrives as the free-text answer; picked without any text → ask once, as plain text, and end your turn. A date rule is matched against the table's `created` or `last change` column, the given day included; print the folders it selects before anything moves.
4. Chosen `incomplete` plans → [the unfinished question](#the-unfinished-question). Chosen `completed` plans with follow-ups → [the follow-up question](#the-follow-up-question).
5. Archive the chosen folders (Step 4).

### all

Classify every folder in `.unikit/code/plans/`. Print the `completed` ones as your own message, with their created and last-change dates, marked as in interactive mode, and ask:

```
AskUserQuestion: Archive all <n> completed plans?

Options:
1. Yes, archive all <n>
2. Cancel
```

"Yes" and some of them have follow-ups → [the follow-up question](#the-follow-up-question) before anything moves. `--all` takes `completed` plans only: an unfinished plan is archived only by an explicit choice — the interactive mode or its own name.

### one plan

1. Resolve the name inside `.unikit/code/plans/`: an exact folder name; else the one folder ending in `_<name>`, or in `-<name>` after three digits; else the one folder whose name contains `<name>` — a match by this last rule is confirmed before anything moves (`AskUserQuestion: Archive <matched folder>?` — `Yes` / `Cancel`). None → `Plan not found: <name>` — with `(already archived)` added when `.unikit/code/archive/plans/<name>/` exists — and stop. More than one → list them, ask for a more specific name, and stop.
2. Classify it. `incomplete` → [the unfinished question](#the-unfinished-question) for this one plan, its option 2 read as `Leave it in place`. `empty`, `broken bundle` or `not a plan` → print the verdict and stop.
3. Follow-ups → [the follow-up question](#the-follow-up-question); "Handle them first" stops here.
4. Archive it (Step 4).

## Step 4: Archive one plan

1. **Destination** `.unikit/code/archive/plans/<folder>/`. It already exists → one plan: `ERROR [archive] <folder> is already in the archive — rename one of the two folders by hand` and stop; interactive or all: `WARN [archive] skipped <folder>: destination exists` and go on. Never overwrite, never rename.
2. `mkdir -p .unikit/code/archive/plans`
3. **Move.** Use `git mv` only when all three hold: `git.enabled` is not `false`; `git rev-parse --is-inside-work-tree` succeeds; `git ls-files -- .unikit/code/plans/<folder>` prints at least one path. Then run `git mv .unikit/code/plans/<folder> .unikit/code/archive/plans/<folder>`; otherwise `mv .unikit/code/plans/<folder> .unikit/code/archive/plans/<folder>`. Print which one and why: `INFO [archive] <folder>: git mv (tracked)` or `INFO [archive] <folder>: mv (git disabled | not a git work tree | untracked)`.
   "git is installed" is not enough: `git mv` of an untracked or ignored folder fails with `fatal: source directory is empty`. A tracked folder that also holds untracked files moves whole — the untracked files travel along and stay untracked.
   A move that fails anyway → `ERROR [archive] <folder>: <the command's error>`, then stop (one plan) or skip it (interactive, all). Never retry with the other command.
4. **Label.** In the moved task file, insert one line `Archived: <today>` — for a plan archived unfinished, `Archived: <today> — unfinished (<done>/<total>)` — directly below `Updated:`; no `Updated:` → below `Created:`; neither → below the `# ` title line, after a blank line. Change nothing else: `Updated:` stays, the ultra marker stays the first line.
5. Print `INFO [archive] archived: .unikit/code/plans/<folder> → .unikit/code/archive/plans/<folder>`.

After the last plan:

```
Archived <n> plan(s) to .unikit/code/archive/plans/:
  - <folder>
Skipped <k>:
  - <folder> — <reason>
Plans left in .unikit/code/plans/: <m>

Nothing was committed. Commit the move with /unikit-commit.
```

Omit `Skipped` when `<k>` is 0.

## Rules

1. Never archive a plan that is not `completed` on your own: an `incomplete` plan moves only after the user has seen what is left and chosen `Archive them unfinished`, and its label says so; an `empty`, `broken bundle` or `not a plan` folder never moves. Follow-ups — untransferred MCP findings, open rule candidates — never block: they ask, and the user decides.
2. Never delete, overwrite or rename a folder.
3. Never commit or push — `/unikit-commit` does that.
4. Edit nothing but the one `Archived:` line.
5. Other skills do not search the archive, on purpose: an archived plan must stop being offered. Three readers look there explicitly: the `implemented_version` fallback of `/unikit-plan` needs completed plans and skips one labelled `unfinished`; the `/unikit-plan` collision check keeps a new plan from taking an archived plan's name; `/unikit-explore` reads archived plans as history of what was already built — an `unfinished` one as work that was dropped — never as a plan to continue.

## Artifact Ownership

- **Owns:** `.unikit/code/archive/plans/`.
- **Reads:** `.unikit/code/plans/*/`, `.unikit/MCP-RECHECK-NOTES.md` and its parked `.archive.*` copies, `.unikit/config.yaml`.
- **Modifies:** nothing outside the folders it moves.
