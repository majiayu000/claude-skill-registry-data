---
name: gw-init
description: Apply Galivelop-workflow to the current project by following the workflow repo's apply guide (new or existing project). Use when starting the workflow in a repo (run by hand with /gw-init).
disable-model-invocation: true
license: MIT
compatibility: Claude Code or any Agent Skills agent; git, bash and python3 3.8+; the Galivelop-workflow repo cloned or added to the session
metadata:
  version: "0.4.3"
  source: "Galivelop workshop"
---

# gw-init

If `.claude/gw/gw-init.md` exists in the project, read it first: it holds what is specific to the project.

A thin wrapper: the procedure lives in the workflow repo's guide, `docs/en/apply.md` (Spanish: `docs/es/aplicar.md`).
Follow it step by step. This skill only fixes where to find things and what to confirm.

**Read the workflow with a subagent** (`orchestrate-dealer`, light model): it reads the guide and the project's build
files and returns the step-1 decision table, each candidate value with its source path, and the conflicts with the
project (existing `CLAUDE.md`, hook managers, a red check). The main session decides from that summary and never
reads the workflow's guides or scripts whole.
Reply to the user in the language they use; the project's `language` is decided in step 3.

## 1. Find the workflow repo

`<workflow>` is the clone of `Galivelop-workflow` that holds `scripts/aplicar.py`. Look in this order:

1. A sibling of the project: `../Galivelop-workflow`.
2. A repo already attached to the session (check `ls` of the session's working folders).
3. Otherwise ask the user to clone it next to the project or add it to the session, and wait. Read it, never edit it.

When cloning it, take the latest published tag, not the default branch (which may not be `main` and may be an old
version): `git ls-remote --tags --refs --sort=-v:refname <url>` shows the tags (the first line is the latest), then
`git clone --branch vX.Y.Z <url>`. Whatever the origin (a new clone, a sibling clone that already exists or a repo
added with `add_repo`), compare `git -C <workflow> describe --tags` with the latest tag and, if it is behind, run
`git -C <workflow> fetch --tags` and `git -C <workflow> checkout vX.Y.Z`.

Done when `python3 <workflow>/scripts/aplicar.py --help` runs.

## 2. Check the preconditions

The project is a git repo (`git init` if new), `git status` is clean or the user knows what is unpushed, and the
session was opened with the project as its working folder. If it was not, tell the user to reopen it from the
project: `cd <project> && claude`.

## 3. Decide what needs judgement

Follow section 1 of the guide: `language`, `log`, `install`, `check`, protected branch, `direct` or `pr`, `content`
regexes, and the optional skills `opt-ai` and `scout-updates` (only if the user asks).

- Infer `install` and `check` from `package.json`, `pyproject.toml`, `Cargo.toml`, `pom.xml`, `go.mod` or
  `Makefile`, and run the `check` command once.
- Ask the user whenever a value is a guess. Offer numbered candidates; one question per unknown.

Done when every fact has an answer the user confirmed.

## 4. Apply

1. Dry run first, then the same command without `--dry-run`:

   ```bash
   python3 <workflow>/scripts/aplicar.py <project> --dry-run --init --language <es|en> --log <path> \
     --install "<cmd>" --check-command "<cmd>" --protected-branch <branch> \
     --push-to-protected <direct|pr> --content '<regex>'
   ```

   Repeat `--install`, `--check-command` and `--content` once per value. Add `--with opt-ai` or
   `--with scout-updates` when chosen. Existing projects: read "Existing projects" in the guide first (hook
   managers, existing `CLAUDE.md`, red check, existing log).
2. Auto mode may ask permission to edit `.claude/settings.json`, `.claude/gw/scripts/` and `.githooks/`. Tell the user before running, and
   after a refused call run `git status` and `git diff` before repeating it.
3. Review every `*.gw-nuevo` with the user (guide, step 3). Merge `AGENTS.md` and `CLAUDE.md` blocks by hand; keep
   the `galivelop-workflow` marker line. Delete each `.gw-nuevo` once merged.
   Coming from an earlier or hand-made copy, expect many: merge one at a time, the workflow's version whole and the
   project's own part in `.claude/gw/<skill>.md` (guide, "Migrating from an earlier copy").
   The run also carries the user's personal notes from `~/.claude/gw/notas/` (if any) to `.claude/gw/`; a project
   copy that differs is left as is and reported (`diff <source> <target>`); `--sin-notas-personales` skips them.
4. Fill the `_(…)_` gaps of the log with branch, phase and a concrete next step.

Done when no `*.gw-nuevo` is left and the log has a next-step line.

## 5. Check, commit, push

1. `python3 <project>/.claude/gw/scripts/doctor.py`; fix and rerun until no `FAIL` is left. Explain each `WARN` to
   the user (`docs/en/troubleshooting.md`).
2. Commit with the message `aplicar.py` suggested, replacing its last line with the real `Next:` (`Siguiente:` in
   Spanish projects), then `git push -u origin <branch>`; the new pre-push runs the check on the pushed commit.
3. Report: what was created, what the user must decide next, and that nothing went to the protected branch.
4. Warn the user: a `.claude/settings.json` created mid-session is not loaded until the next session, so the
   `PreToolUse` hook (the PR guard) is not active in this one. Until they open a new session from the project, check
   the review mark by hand before any PR: `bash .claude/gw/scripts/revisado.sh`.

Done when the push went through and `doctor.py` exits 0.
