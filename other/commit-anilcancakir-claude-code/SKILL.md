---
name: commit
description: "Split the changes into atomic commits, preflight and push them; also rebase, squash and trace history. Pass --no-push when the user only asked to commit."
when_to_use: "Use when committing, rebasing, squashing, cherry-picking or tracing history; GitHub issues and PRs are ac:github-cli."
argument-hint: "[--skip-preflight] [--no-push]"
allowed-tools: Bash, Read
effort: medium
---

# /ac:commit

Commit the working tree as atomic commits in the repo's own style, then push. Rebase, squash and history tracing live in two references that load only when the request asks for them.

Request: $ARGUMENTS

## Phase 0: Parse arguments and pick the mode

1. `--skip-preflight` in `$ARGUMENTS` sets `SKIP_PREFLIGHT`.
2. `--no-push` in `$ARGUMENTS` sets `NO_PUSH`. Also set `NO_PUSH` when `.ac/state/active-auto.json` exists and its `session_id` is this session's (`${CLAUDE_SESSION_ID}`): that is an `ac:auto` away run, which publishes only from its own close, after its verification gate, and only what the user named. A push from here would land before the gate has judged the work. `NO_PUSH` holds in every mode.
3. Mode, from the request:
   - **COMMIT** (the default): Phases 1 to 5 below.
   - **REBASE** (rebase, squash, autosquash, reorder, split a commit, cherry-pick, update the branch): read `${CLAUDE_SKILL_DIR}/references/rebase.md` and follow it instead of Phases 1 to 5.
   - **HISTORY** (when was X added, who changed this, blame, bisect, history of a file): read `${CLAUDE_SKILL_DIR}/references/history.md` and follow it instead of Phases 1 to 5.
4. Other tokens are a free-form note. When they name files or one unit of work, plan only those.

## Phase 1: Context

The injected lines below are the whole git picture; do not gather it again.

- Branch: !`git branch --show-current`
- Status: !`git status --short`
- Staged stat: !`git diff --staged --stat`
- Unstaged stat: !`git diff --stat`
- Last 30 commits: !`git log -30 --pretty=format:"%h %s"`
- Upstream: !`git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "NO_UPSTREAM"`
- Unpushed commits: !`git log --oneline @{upstream}..HEAD 2>/dev/null || git log --oneline $(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null)..HEAD 2>/dev/null || echo "NO_BASE"`

A clean status means stop with `Nothing to commit. Working tree clean.` and skip every remaining phase.

## Phase 2: Preflight (skip if `SKIP_PREFLIGHT`)

Catch breakage before writing history. `/ac:execute` Phase 4 sets the flag because its Phase 2d checked each wave's touched files and ran the project-wide typecheck, and its Phase 3a ran the build, the full suite and the linter; another pass here would be the same commands on the same tree.

1. Find the typecheck, test and lint commands in `CLAUDE.md` and `CLAUDE.local.md` (sections named `commands`, `scripts` or "Build / Test / Lint"), else the `package.json` `scripts` block. Use the project's own commands, not generic guesses.
2. Run typecheck, then tests, then lint, each through `Bash`.
3. On a failure: stop, print which step failed and the first ~30 lines of its output, stage nothing, commit nothing. The user fixes it and runs `/ac:commit` again.
4. No commands found: print `Preflight: no commands found in CLAUDE.md or package.json; skipping.` and continue.

## Phase 3: Style and plan (blocking output)

**Style.** Classify the 30 subjects from Phase 1:

| Style | Pattern | Example |
|---|---|---|
| `SEMANTIC` | `^(feat\|fix\|chore\|refactor\|docs\|test\|ci\|style\|perf\|build)(\(.+\))?:` | `feat: add login` |
| `PLAIN` | description with no prefix, more than 3 words | `Add login page to the web app` |
| `SENTENCE` | full past-tense sentence | `Implemented the new login flow` |
| `SHORT` | 1 to 3 words | `format` |

Count each subject once, then take the first that holds, in this order: `SEMANTIC` 15 or more of 30, `SENTENCE` 15 or more, `PLAIN` 15 or more, `SHORT` 10 or more, else `PLAIN`. Print one line before planning: `Style: SEMANTIC (22 of 30), e.g. "feat(auth): add token refresh"`.

**Atomic units.** One commit per unit that can be reviewed and reverted alone: a function with its test, a migration with the model change that needs it. File count is a hint, not the rule: a rename across callers is one unit in many files, and two files can be two units. Different directories, component types (model, service, view) or concerns (UI, logic, config, test) usually mean separate units; keep files together only when splitting would leave a commit that does not build or cannot be reverted alone. A commit holding two units is a planning bug; split it. Apply this to every change set, not only the first.

Tests go in the same commit as their implementation (`test_*.py` and `*_test.py` with `*.py`, `*.test.ts` and `*.spec.ts` with `*.ts`, `__tests__/*.ts` with `*.ts`, `tests/*.py` with `src/*.py`).

**Plan.** Print it before any `git commit`:

```
COMMIT PLAN: N files, K commits
1. <message in the detected style>
   - path/a.py
   - path/a_test.py    together because: implementation and its test
2. <message>
   - path/b.py
```

Order by dependency, lowest first: utilities and types, models, services, endpoints, configuration. Check before executing: each commit is one unit, every multi-file commit has its "together because" line, every message matches the style, tests are paired. Replan on any miss.

## Phase 4: Commit

Stay on the current branch, with the git identity exactly as `git config` has it: no `-c user.name`, `-c user.email` or `--author`, and no `Co-Authored-By` or `Signed-off-by` trailer naming the operator.

Per commit, in plan order:

```bash
git add <files>
git diff --staged --stat
git commit -m "<message>"
```

A change that completes a commit not yet pushed (its hash is in the "Unpushed commits" list, and the branch is not `main` or `master`) may be `git commit --fixup=<hash>` instead; after all fixups run one `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash <base>`, where `<base>` is the upstream, or the merge base with `main`/`master` when there is none. A pushed commit is never a fixup target: rewriting published history is REBASE mode and needs its own request.

Then verify with `git status --short` and `git log --oneline <base>..HEAD`.

## Phase 5: Push and report

Skip the push when `NO_PUSH` is set or Phase 1 printed `NO_UPSTREAM`.

1. On `main` or `master`, ask first:
   ```
   AskUserQuestion({
     header: "Push main?",
     question: "Current branch is `<branch>`. Push directly?",
     options: [
       {label: "Push", description: "Push to <upstream>."},
       {label: "Skip push", description: "Leave commits local; user pushes manually."}
     ]
   })
   ```
2. `git push`. Plain `--force` is never used here.
3. A rejected push (non-fast-forward) stops the run: print `git log <upstream>..HEAD` and `git log HEAD..<upstream>` and let the user decide.

Then one report block:

```
## Commit Complete

Branch: <name> [<upstream> | local-only]
Style: <SEMANTIC | PLAIN | SENTENCE | SHORT>
Commits created: <N>
  <hash> <message>
Push: <pushed to <remote>/<branch> | skipped (no upstream) | skipped (--no-push) | skipped (user declined)>
Preflight: <PASS | SKIPPED | NOT CONFIGURED>
```

When `/ac:execute` Phase 4 started this skill, the report block is the handoff signal that the execution pipeline is done. A conflict during an autosquash means the tree changed under it: print `git status`, run `git rebase --abort` and surface it.
