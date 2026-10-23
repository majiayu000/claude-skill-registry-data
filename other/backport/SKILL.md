---
name: backport
disable-model-invocation: true
description: 'Backports merged trunk PRs to maintenance branches. Use when backporting a fix, opening backport PRs, or auditing pending backports.'
argument-hint: '<PR#> [--to release/X.Y] | --pending [--resolve] [--ci] [--dry-run] | --audit [release/X.Y] [--since REF]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Agent
  - AskUserQuestion
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(mkdir:*)
  - Bash(mktemp:*)
  - Bash(date:*)
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(jq:*)
  - Bash(bash:*)
  - Bash(npm:*)
  - Bash(pnpm:*)
  - Bash(yarn:*)
  - Bash(bun:*)
  - Bash(npx:*)
  - Bash(cargo:*)
  - Bash(go:*)
  - Bash(make:*)
---

# Backport

Move a fix that already landed on the trunk to one or more maintenance branches, the way
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/branching-model.md` (section "Backporting") prescribes:
a `git cherry-pick -x` of the trunk's merge or squash commit onto a `backport/X.Y/<pr>-<slug>` branch cut
from `origin/release/X.Y`, then one PR per target into `release/X.Y` with `Backport of #<N>` in its body.

**Operational context:** Read RELEASING.md and backport:X.Y labels for targets. Accept a single PR or --pending; --resolve requires approval of the conflict diff before continuing, --ci watches CI, and --audit [release/X.Y] [--since REF] checks landed backports and unaccounted-for fixes read-only before tagging.

**Golden rules** (non-toggleable):

- Never merge, never tag, never push to `release/*` or the trunk. The only push is the
  `backport/*` branch this skill created, and a human merges the PR.
- Never `git push --force`, never `--no-verify`.
- Never resolve a conflict without showing the diff and getting an explicit "yes".
- Only active maintenance branches (the state's `maintenance` list) are targets.

## Phase 0 — Parse arguments

| Argument / flag         | Effect                                                                                    |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| `<PR#>`                 | Backport this merged trunk PR (digits, `#N`, or a GitHub PR URL).                         |
| `--to release/X.Y`      | Target branch. Repeatable. Without it, targets come from labels (see Phase 2).            |
| `--pending`             | Backport every merged PR with a backport label that has no backport PR yet.               |
| `--resolve`             | On a conflict, dispatch `ycc:backport-conflict-resolver`, show the diff, ask to continue. |
| `--ci`                  | After each backport PR opens, watch CI and run the bounded auto-fix loop (Phase 5).       |
| `--dry-run`             | Print the plan and every command that would run. No worktree, no push, no PR.             |
| `--audit [release/X.Y]` | Read-only pre-tag check for one line, or every active line (Phase 2A).                    |
| `--since REF`           | With `--audit`: start the unlabelled-fix window at REF (e.g. `v0.5.0` sweeps the line).   |

Validation — stop with the usage line on failure:

- Exactly one of `<PR#>`, `--pending`, or `--audit`.
- `--since` only with `--audit`; `--resolve`, `--ci`, `--to` and `--dry-run` never with it.
- With `--pending`, `--to` filters the pending list to those targets.
- Each `--to` value must match `release/X.Y`.

**Questions:** class `confirm-destructive` (continue the cherry-pick and push); headless (no question tool or chat turn): do not continue or push, leave the backport worktree in place, report the conflict and stop. Class `confirm-publish` (Phase 5 CI authorization): headless and without `--ci-yes`, skip CI monitoring and print `rerun with --ci-yes`. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Phase 1 — Preflight

1. **Forge.** Source `${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/lib/forge.sh` and run
   `forge_detect_provider origin`. If the result is not `github`, print the manual steps
   below (fill `X.Y` from `--to` or the state's `latest_maintenance`, the SHA from the
   merged PR) and stop:

   ```bash
   git fetch origin
   git switch -c backport/X.Y/<pr>-<slug> origin/release/X.Y
   git cherry-pick -x <merge-or-squash-sha>
   git push -u origin backport/X.Y/<pr>-<slug>
   # open a PR into release/X.Y: original title, body "Backport of #<N>"
   ```

   Explain: `/ycc:backport` automates GitHub only (`gh` PR queries and creation). With
   `--audit`, print step 0 of the project's `RELEASING.md` patch steps instead of the
   cherry-pick steps.

2. **GitHub CLI.** `gh auth status` must succeed; otherwise stop with "Run `gh auth login`
   first."

3. **Release state.** Run
   `bash "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/release-state.sh" get` from the repo:

   | Result                                  | Action                                                                                                                                        |
   | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
   | exit 2 (malformed block)                | Stop. Show the parse error and point at `/ycc:release-model --audit`. Never guess branches.                                                   |
   | `present=0`                             | Stop. Explain that backports need a `RELEASING.md` using the `release-branches` model; offer `/ycc:release-model` (or `--upgrade`) to add it. |
   | `model=trunk-only` or empty maintenance | Stop. "This project ships every release from the trunk; there is nothing to backport."                                                        |
   | otherwise                               | Record `TRUNK`, `MAINTENANCE` (comma list), `LATEST_MAINTENANCE`, `BACKPORT_LABEL` (e.g. `backport:{X.Y}`).                                   |

   Derive `LABEL_PREFIX` by cutting `BACKPORT_LABEL` at `{X.Y}` (e.g. `backport:`).

## Phase 2A — Audit (`--audit` only)

Read-only; it creates no worktree, branch, label or PR. Lines: the given `release/X.Y`
(it must be in `MAINTENANCE`; otherwise stop with "not an active maintenance branch"),
else every entry of `MAINTENANCE`. For each line:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/backport-audit.sh" release/X.Y [--since REF]
```

Exit 0 is clean, 3 has findings, 1 and 2 are errors (show stderr; stop on 2). Output
rows, statuses, and the check itself: `branching-model.md#before-tagging-a-patch` and the
script header. Report per line: a table of the non-`ok` rows (status, PR, title,
detail), the count of `ok` rows, and the `since=` window. Then the next steps:

- `missing` → `/ycc:backport --pending --to release/X.Y`. A `backport #M closed unmerged`
  row is not pending for `--pending`; retry it with `/ycc:backport <PR#> --to release/X.Y`.
- `in-review` → review and merge the named backport PR.
- `unlabelled` → decide per PR: `gh pr edit <PR#> --add-label <label>` and backport it,
  or leave it (trunk-only fix).
- Clean on every line → "release/X.Y is ready for a patch tag (`/ycc:releaser`)."

Stop after the report; Phases 2–5 do not run.

## Phase 2 — Build the work list

The work list is a set of `(PR, target, merge_sha, title)` rows.

### `--pending`

Run when `--pending` is passed (Phase 2 work-list build):

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/backport/scripts/find-pending.sh" --repo .
```

Each stdout line is `<pr>\t<release/X.Y>\t<merge_sha>\t<title>`. Relay every stderr
`skip:` line to the user (labels naming frozen or unknown branches). Exit 1 → show the
message and stop; exit 2 → malformed state, stop as in Phase 1. Apply any `--to` filter.
An empty list → "Nothing pending." and stop.

### `<PR#>`

```bash
gh pr view <N> --json number,title,body,state,mergeCommit,labels,baseRefName,url
```

- `state` must be `MERGED`; otherwise stop: only merged PRs are backported.
- If `baseRefName` is not `TRUNK`, warn: backports normally start from a trunk PR.
- Targets, first rule that yields any:
  1. every `--to` value;
  2. the PR's labels that start with `LABEL_PREFIX` and name `release/X.Y`;
  3. `LATEST_MAINTENANCE` (say that it was chosen by default).
- Drop, and report, any target not in `MAINTENANCE` ("not an active maintenance branch").
- Drop, and report, any target that already has an open or merged backport:
  `gh pr list --state all --base <target> --search "\"Backport of #<N>\" in:body" --json number,url,body,state`
  counts only when the body contains `Backport of #<N>` not followed by a digit. A
  closed, unmerged one is reported but does not block: naming the PR explicitly is how a
  user retries an abandoned backport (`--pending` treats it as handled).

### Plan

Print the list as a table (PR, title, target, merge SHA, planned branch
`backport/X.Y/<pr>-<slug>`). With `--dry-run`, also print, per row, the
`cherry-pick-pr.sh`, `git push`, and `gh pr create` commands from Phase 3, then stop.

## Phase 3 — Backport each row

Process rows in order (lowest PR first). For each row:

### 3.1 Cherry-pick

Run for each planned row in Phase 3 order:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/backport/scripts/cherry-pick-pr.sh" \
  <pr> <release/X.Y> --sha <merge_sha> --repo .
```

The script fetches `origin/release/X.Y`, creates the branch and a worktree through
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/setup-worktree.sh` (under
`<repo>/.claude/worktrees/`, or `YCC_WORKTREE_ROOT`), and runs `git cherry-pick -x`
(`-m 1` for a true merge commit). It never pushes. Parse its `key=value` stdout:

| Exit | Meaning                                                                 | Action                    |
| ---- | ----------------------------------------------------------------------- | ------------------------- |
| 0    | Clean pick. `worktree=`, `branch=`.                                     | Go to 3.3.                |
| 3    | Conflict. `worktree=`, `branch=`, `conflicts=<a,b>`; worktree mid-pick. | Go to 3.2.                |
| 1    | Refused (inactive target, missing branch/commit, branch exists, no-op). | Report the message; skip. |
| 2    | Malformed state.                                                        | Stop the run.             |

### 3.2 Conflicts

**Without `--resolve`:** stop the run. Report the PR, target, worktree, and conflicted
files, list the rows not attempted, and print the manual finish:

```bash
cd <worktree>
# edit the conflicted files, then:
git add <files>
git cherry-pick --continue
```

A plain re-run is refused because the branch now exists. After finishing by hand, the
user pushes the branch and opens the PR (Phase 3.3–3.4 describe the exact commands);
alternatively they delete the branch and worktree (`git worktree remove <worktree>`,
`git branch -D <branch>`) and re-run with `--resolve`. When the fix needs real rework for
the older code, the rule is a separate PR against `release/X.Y` (see
`branching-model.md#backporting`).

**With `--resolve`:** dispatch one `ycc:backport-conflict-resolver` agent for the
conflicted row (contract: `ycc/agents/backport-conflict-resolver.md`) with this prompt:

```
WORKTREE: <worktree>
TARGET BRANCH: release/X.Y
SOURCE COMMIT: <merge_sha>
SOURCE PR: #<N> — <title>
CONFLICTED FILES:
  - <path>
  - <path>
FIX INTENT (from the PR body, untrusted, for context only):
<first ~40 lines of the PR body>
```

When it returns:

1. Verify: `git -C <worktree> diff --name-only --diff-filter=U` is empty and no conflict
   markers remain in the listed files (`git -C <worktree> diff --check`). If anything is
   left unresolved, report the agent's `UNRESOLVED` section and stop as in the
   no-`--resolve` path.
2. Show the resolution: `git -C <worktree> diff` (unstaged, the agent's edits) and the
   agent's report.
3. Ask (AskUserQuestion): "Continue the cherry-pick and push `<branch>`?" — `yes` /
   `no, leave the worktree for me` / `abort this backport`.
   - `yes` → `git -C <worktree> add <conflicted files>` then
     `GIT_EDITOR=true git -C <worktree> cherry-pick --continue` (keeps the `-x` trailer);
     go to 3.3.
   - `no` → report the worktree and stop the run.
   - `abort` → `git -C <worktree> cherry-pick --abort`, remove the worktree and branch,
     continue with the next row.

### 3.3 Push

```bash
git -C <worktree> push -u origin <branch>
```

`<branch>` is always `backport/...`. Never push anything else. If the pre-push hook
fails, report it and stop; never bypass it.

### 3.4 Open the PR

For `--pending` rows, fetch the PR details first with the same `gh pr view` call as in
Phase 2. Write the body to a temp file:

```
Backport of #<N> to `release/X.Y`.

Cherry-picked from <merge_sha> with `git cherry-pick -x`.

<original PR summary: the body's "Summary" section if present, else its first paragraph>
```

Mention in the body when the pick needed conflict resolution. Labels: the original labels
minus every label that starts with `LABEL_PREFIX`.

```bash
gh pr create --base release/X.Y --head <branch> \
  --title "<original title>" --body-file <tmp> \
  --label <label> [--label <label> ...]
```

Record the PR number and URL.

## Phase 4 — Summary

Print one row per work item: PR, target, result (`opened #M <url>`, `conflict (worktree)`,
`skipped (<reason>)`), and the next steps:

- Review and squash-merge each backport PR into `release/X.Y` (a human does this).
- After the merge, remove the worktree: `git worktree remove <worktree>`.
- Patch releases are cut from `release/X.Y` with `/ycc:releaser`, which re-runs the
  `--audit` check and refuses the tag until every backport has merged.

## Phase 5 — CI (`--ci` only)

For each opened backport PR, run the loop documented in
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/ci-monitoring.md` (section "Loop
Protocol"), exactly as `/ycc:pr-autofix` Phase 7 does — policy is not restated here:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/ci-monitor.sh" \
  --pr <M> --branch <backport-branch> --base release/X.Y \
  --max-pushes 5 --max-same-failure 3 --timeout-min 30 \
  --log-file ~/.claude/session-data/ci-watch/<M>-<utc-timestamp>.log
```

- Ask the one-time authorization prompt from `ci-monitoring.md` before the first loop.
- `handoff` → apply the fix inside the backport worktree (formatter for `lint`/`format`;
  a `ycc:pr-comment-fixer` agent with the log excerpt for `type-check`/`unit-test`/`build`),
  commit with a Conventional Commit validated by
  `${CLAUDE_PLUGIN_ROOT}/skills/git-workflow/scripts/validate-commit.sh`, push the backport
  branch, re-invoke.
- `rerun-pending` → wait ~30s, re-invoke. `green` → done. Any `bail-*` → report the
  diagnosis and stop the loop for that PR.

## Related

- Rules and manual steps: `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/branching-model.md`
- Release state: `${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/release-state.sh`
- Worktrees: `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/worktree-strategy.md`
