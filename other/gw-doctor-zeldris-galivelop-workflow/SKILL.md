---
name: gw-doctor
description: Check that Galivelop-workflow is set up correctly in the current project and explain every failure with its fix. Use when something in the workflow misbehaves or after applying or updating it (run by hand with /gw-doctor).
disable-model-invocation: true
license: MIT
compatibility: Claude Code or any Agent Skills agent; git and python3 3.8+; reads .claude/gw.json
metadata:
  version: "0.4.3"
  source: "Galivelop workshop"
---

# gw-doctor

If `.claude/gw/gw-doctor.md` exists in the project, read it first: it holds what is specific to the project.

The check itself is a script, `doctor.py`: deterministic, no AI, no network. This skill runs it, explains what it
prints and applies fixes the user approves. Reply in the project's `language` (`.claude/gw.json`).

## Steps

1. **Run it from the project root:**

   ```bash
   python3 .claude/gw/scripts/doctor.py
   ```

   Without a copy in the project (not applied yet), run the workflow's script on the project instead:
   `python3 <workflow>/scripts/doctor.py --root <project>`. `--json` gives the list as JSON.
2. **Read every line.** Each is `OK`, `WARN` or `FAIL`, followed by `fix:` with the command that repairs it. Exit
   code 1 means at least one `FAIL`.
3. **Explain each non-OK line** to the user in plain words: what is wrong, what it breaks in the workflow, and the
   fix. `docs/en/troubleshooting.md` (the `doctor.py` table) says what each check means; read it when a line is not
   clear.
4. **Group the fixes** by kind and offer them: commands that only change git settings or file modes
   (`git config core.hooksPath .githooks`, `chmod +x`), commands that rewrite workflow files (`/gw-update`), and
   edits of project files (the log's next step, `check` in `.claude/gw.json`, `AGENTS.md`).
5. **Apply only what the user approves.** After a refused or interrupted call, run `git status` and `git diff`
   before repeating it. Fixes touching `.claude/settings.json` or `.githooks/` may need the user's permission in
   Claude Code's auto mode.
6. **Run `doctor.py` again** and repeat steps 3 to 5 until no `FAIL` is left. A `WARN` the user chooses to keep is
   named in the final report, with the reason.

## Cases that need care

- **`hooks-path` WARN:** another hook manager owns the hooks. Chain the workflow's hooks from it with the line the
  warning gives; never overwrite the manager's files or point `core.hooksPath` back without asking.
- **`check syntax-only` WARN:** a `bash -n`/`sh -n` check command reads only its first file (several files, a glob or
  a substitution). Offer the one-command-per-file or `for` loop the warning gives; edit `check` only if the user agrees.
- **`check command` FAIL:** the tool is missing or the command is wrong. Ask the user which; do not invent one.
- **`session` WARN:** the session was opened outside the repo. The fix is to reopen it from the repo, so tell the
  user; the script cannot do it.
- **`ci access` WARN:** the agent cannot read the CI state of GitHub pushes. Installing `gh` and logging in
  (`gh auth login`) or exporting a token is the user's call (credentials): tell them; never ask for or print the token.
- **`config` FAIL:** run `python3 .claude/gw/scripts/config.py validate` for the exact line; keys are in
  `docs/en/config.md`.

## Report

Reply in 5 lines or fewer: the `FAIL`/`WARN` count before and after, what was fixed, what the user chose to leave,
and the next step.
