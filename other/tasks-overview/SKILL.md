---
name: tasks-overview
description: >-
  Show the current state of the project's tasks, hiding archived ones, by
  writing a project-local status script for however the project stores its
  tasks. Use when the user asks which tasks are open or in progress, or how far
  the work has got.
---

# Tasks Overview

## Overview

Every project keeps its tasks somewhere, and the storage differs from project
to project: one Markdown file per task with a status key in the frontmatter,
headings in a single roadmap file, a YAML or JSON list, an issue tracker
reached through its CLI. flowai proposes one layout (the `tasks` role from
AGENTS.md, by default a date-nested `<tasks dir>/<YYYY>/<MM>/<slug>.md` tree
with `status: to do | in progress | done | superseded`) and many projects use
their own. Reading every task by hand on every request is slow and
inconsistent, so this skill writes a script for the project's storage once,
keeps that script in the project, and runs it from then on.

This skill ships no script. The storage is known only inside the project, so
the script is written there, for that storage, against the output contract
below. The contract keeps the report the same in every project; the
completeness check replaces the tests a shared template would have had.

## Output Contract

The project script is `scripts/tasks-overview.py`. It MUST:

- run with Python 3 and its standard library only (`subprocess` is allowed
  when the tasks live in a tracker reachable through a CLI);
- print the non-archived tasks grouped by status: `in progress` first, `to do`
  second, then the remaining statuses in alphabetical order, each group under
  a `<status>:` header line, using the project's own status names (map the
  project's equivalents of "in progress" and "to do" to the first two places);
- print one line per task: its location (file path, `file#heading`, issue
  number), the progress `[done/total]` when the task has checklist steps, the
  title, and the date when the storage has one;
- end with the footer `N open, M archived (hidden; use --all)`;
- show the archived groups too when called with `--all`, and then drop the
  `(hidden; use --all)` part of the footer;
- print `no tasks under <location>` and exit 0 when there are none;
- exit 2 with a message on stderr naming the path or command when the storage
  is missing, a task cannot be read, or the argument is unknown — never skip a
  task silently;
- never write to the task storage.

## Rules & Constraints

<rules>
1. **An existing script wins.** If the project already has
   `scripts/tasks-overview.py`, run it and report. Do not re-derive the storage
   and do not rewrite the file — the user owns it once it is in the project;
   if its output looks wrong, say so and leave the fix to the user.
2. **The project's convention beats the framework default.** AGENTS.md (or
   CLAUDE.md) is the source for the task storage. When it carries a
   project-specific section that overrides or contradicts the framework's
   default task rules, the project-specific one is the truth. The framework
   layout is only assumed when AGENTS.md carries no project-specific override
   of it.
3. **Never modify the task storage.** This skill reads tasks; it does not fix
   frontmatter, flip statuses, move files or edit issues. The only file it
   writes is the script.
4. **Write for the storage the project has.** Write the script yourself, to
   the Output Contract, for the storage AGENTS.md describes — not for the
   framework layout, and not by forcing a different storage into the
   one-file-per-task shape. Keep it short and readable: the user will edit it.
5. **Show the derivation, with quotes.** Before writing the script, state how
   the tasks are stored — where they live, what one task is, where its status
   and its steps come from, which statuses count as archived — and QUOTE the
   AGENTS.md sentence each answer comes from (the words themselves, in
   quotation marks or a code span — not a paraphrase), so a wrong guess is
   caught before it becomes a script. An answer with no quoted source is a
   guess and must be named as one.
6. **No guessed location.** If neither AGENTS.md nor the tree says where the
   tasks live, ask the user in one line and STOP. Do not scan the whole
   repository for anything that looks like a task.
7. **Check completeness on the first run.** A freshly written script is
   untested. After its first run, count the tasks a second, independent way
   and compare with the script's total — see step 5.
8. **Fail loudly.** If `python3` is missing, or the script exits with 2,
   report the message and STOP — do not fall back to reading the tasks by
   hand.
</rules>

## Instructions

<step_by_step>

1. **Reuse gate.** Check for `scripts/tasks-overview.py` in the project root.
   - Present → run it exactly as in step 4, skip steps 2, 3 and 5. If the user
     asked for archived tasks too, pass `--all`.
   - Absent → continue.

2. **Derive the storage from AGENTS.md.** Read `AGENTS.md` (or `CLAUDE.md`
   when that is the file the project has). Find the rules about tasks: the
   `tasks` role in the documentation hierarchy, a "Tasks" section, or any
   sentence naming where tasks live. Apply Rule 2. Establish:
   - **location** — the directory, file or tracker that holds the tasks;
   - **unit** — what one task is (a file, a heading, a list entry, an issue);
   - **status** — where a task's status comes from (a frontmatter key, the
     section the task sits under, a field, a label) and its possible values;
   - **archived** — which statuses, directories or sections mean finished or
     retired (`done`, `superseded`, `closed`, `archived`, `dropped`, …);
   - **steps** — what measures progress (`- [ ]` / `- [x]` items under a
     given heading, sub-tasks), or none;
   - **title and date** — where they come from, if the storage has them.
   If AGENTS.md carries no project-specific task rules, use the flowai default
   (the directory the `tasks` role names, every `*.md` under it, frontmatter `status`, archived `done` and
   `superseded`, steps under `## Definition of Done`, title from the first
   `# ` heading, frontmatter `date`) — but only after confirming that
   directory exists. If the location cannot be established, apply Rule 6.
   Look at one or two real tasks to confirm the shape before writing code.

3. **Show the derivation and write the script.** Show one line per answer from
   step 2 with its quoted source (Rule 5), for example:
   `status — the enclosing "## " section: "A task's status is the ## section it sits under"`.
   Then write `scripts/tasks-overview.py` (create `scripts/` if needed) to the
   Output Contract (Rule 4).

4. **Run it.**

   ```bash
   python3 scripts/tasks-overview.py
   ```

   Add `--all` when the user wants archived tasks too. Exit 2 → apply Rule 8.

5. **Completeness check (new script only).** Count the tasks without the
   script — `find <dir> -name '*.md' | wc -l` minus the ignored files, `grep -c`
   over the task headings, the tracker CLI's own count — and compare that
   number with the script's total (open plus archived from the footer). Say in
   chat what you counted, how, and whether the numbers agree.
   - Agree → go to step 6.
   - Disagree → find which tasks the script missed or invented, fix the script
     you just wrote, and run steps 4–5 once more. If they still disagree,
     report both numbers and the tasks in question, and STOP without
     presenting the list as complete.
   - No independent count exists (a tracker with no count command) → say so
     plainly instead of claiming completeness.

6. **Report.** Paste the script's output VERBATIM in a fenced code block in
   your reply — the user sees your message, not the tool result, and a
   retelling of the list is not the list. Comments or a short reading of it may
   follow the block, never replace it. When the script was just created, add
   one sentence saying that `scripts/tasks-overview.py` now lives in their
   project and is theirs to edit — the next request will run it directly.

</step_by_step>
