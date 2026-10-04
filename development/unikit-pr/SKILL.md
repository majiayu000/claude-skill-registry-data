---
name: unikit-pr
description: >-
  Write, open and — when allowed — merge a pull request for the current feature
  branch of a {{engine_name}} project, with or without a plan. Builds a plain-language
  PR text (one feature per line) from the plan's `## Modules` and task `WHY:` lines,
  or — without a plan — from the commits and the code changes themselves; pushes the
  current state (asking where to end when it stands inside a plan module), opens or
  updates the branch's single open PR through the GitHub MCP, and merges with a merge
  commit only when the merge brings nothing from the base branch. Levels: remind (text
  only), create, merge; capped by `git.pull_requests.max_level`. Trigger phrases:
  "pull request", "open a PR", "create PR", "PR description", "merge the PR". For
  commit messages use /unikit-commit; for reviewing a PR's code use /unikit-review.
argument-hint: "[remind | create | merge] [context]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git *)
  - AskUserQuestion
---

# Pull request author

One author of pull requests: this skill. It writes the title and the text, pushes the branch, opens or updates the branch's pull request, and — only when allowed and only when it is safe — merges it. It writes nothing into a plan and commits nothing.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

Skill-specific rules:
- Two languages meet in one run: the pull request — its title and its body — follows `language.artifacts`; everything said to the user is in `language.ui`. The answers of git and of GitHub are data, not a reason to answer in English.
- The question texts and option labels quoted in this skill and its references are templates: say them in `language.ui`. `INFO` / `WARN` / `ERROR` and the `[pr]` tag stay as they are; the words after them are in `language.ui`.

## What the user sees

A pull-request run is short. In this order, and nothing else:

1. A problem, only when one occurs — its `WARN` / `ERROR` line.
2. The plan line: `INFO [pr] plan: <folder> · modules M<a>-M<b>`, or `INFO [pr] no plan — text from the commits and the code`.
3. The title and the body of the pull request, as a block of their own.
4. The question about the remote — never under `remind`.
5. One result line per action: `Pushed <short sha> to origin/<branch>`, `PR #<n> opened: <url>`, `PR #<n> updated — it now also covers <modules>`, `PR #<n> merged: <url>`, `PR #<n> stays open — <reason>`.

A check that passes says nothing. Short SHAs only; a token, a request header or a remote URL carrying credentials never reaches the output.

## Mode

The level is resolved in this order — the first that speaks wins:

1. **An explicit token** — the first word of the argument is `remind`, `create` or `merge`.
2. **The wording of the request**, in any language: "write / describe the PR" → `remind`; "open / create a PR" → `create`; "merge" → `merge`.
3. **The ceiling** — `git.pull_requests.max_level` in `.unikit/config.yaml`. No key → `create`. A value outside `remind | create | merge` → `create`, and `WARN [pr] git.pull_requests.max_level=<v> is not remind, create or merge; took create`.

The ceiling is also a limit: a request above it acts at the ceiling, with one line — `INFO [pr] <requested> is above git.pull_requests.max_level=<ceiling> — acting at <ceiling>`. A call carrying the context `checkpoint: task N.M` and no token acts at the ceiling: that is what a PR checkpoint does.

Two conditions turn any level into `remind`:

- **The GitHub MCP is not available** — its `create_pull_request` tool cannot be called in this session → `WARN [pr] GitHub MCP not available — printing the PR instead; add it with unikit-ai init (GitHub) and set GITHUB_PAT`.
- **`origin` is not on GitHub** — `git remote get-url origin` does not contain `github.com` → `WARN [pr] origin is not a GitHub remote — printing the PR instead`.

## Step 0: Context

1. **The branch** — `git rev-parse --abbrev-ref HEAD`.
2. **The branch's plan** — the folder found by the branch-match rule of `/unikit-implement` Step 0.1 (the three name formats); the flat fast plan is never a PR's plan. No plan is a normal case: the skill works without one.
3. **The boundaries contract** — read `.unikit/system/plan-boundaries.md`. Missing or unreadable → `WARN [pr] plan-boundaries contract missing — module boundaries unknown, the PR is the current state; run unikit-ai update`, and continue.
4. **The base** — at a PR checkpoint, the `→ <base>` of its `PR checkpoint:` line; otherwise the contract's `## Base branch`. The current branch is the base → `WARN [pr] you are on the base branch <base> — nothing to open a PR from`, and stop.
5. **owner/repo** — from the URL of `origin`: `git@github.com:<owner>/<repo>.git` or `https://github.com/<owner>/<repo>(.git)`.
6. `git fetch origin <base>`. A network error → `WARN [pr] fetch failed — using the local origin/<base>`, and continue.
7. **Uncommitted changes** — `git status --porcelain` is not empty → they are not part of the pull request: `WARN [pr] <n> uncommitted file(s) are not part of the PR — commit them with /unikit-commit first`. At `create` and `merge` the Step 4 question then offers `Stop — I will commit first`.

## Step 1: Boundaries

The pull request is the current state — `HEAD` — unless the user chooses otherwise. That holds with any plan and without one.

- **A `boundary <sha>` in the context** (`/unikit-implement` at a PR checkpoint) → that SHA; at the checkpoint it is `HEAD`.
- **An explicit end in the request** ("a PR up to abc123") outranks everything computed here.
- **Inside a module of a plan with PR checkpoints** — the contract's `## Push target` says when `HEAD` is inside a module: not every task is `[x]`, and `HEAD` is not the `## Last completed boundary`. Inside a module the skill asks — it never cuts the PR silently. Before any text is written (Step 2 depends on the range), print `WARN [pr] HEAD is inside module <name> — a PR up to now carries its unfinished part into an open PR of <previous module>, if there is one`, then ask:

  ```
  AskUserQuestion: Where should the pull request end?

  Options:
  1. PR everything up to now (HEAD)
  2. PR up to the end of <name of the last finished module> (<boundary short>)
  3. Cancel
  ```

  An answer already given in the request ("up to the end of the module", "everything there is") counts, and nothing is asked.
- **A closed plan** — the final pull request after `/unikit-verify`. A closed plan is read from its checkboxes — no argument marks the final pull request.

**Resolve the end once.** `git rev-parse --verify <end>^{commit}` gives `<end>` and `git rev-parse --short <end>` gives `<end short>`; every later command pastes them exactly as printed — a hash is never typed from memory or completed by hand (`.unikit/system/plan-boundaries.md` → `## Push target`). When the end is `HEAD`, the push source is the literal `HEAD`.

The start is `git merge-base origin/<base> <end>`. Nothing between them → `INFO [pr] nothing between origin/<base> and <end short> — no PR to make`, and stop.

## Step 2: Text

Read `{{skills_dir}}/{{self_name}}/references/pr-text.md` and follow it. Print the title and the body as a block of their own.

## Step 3: remind

Print the title, the body, the push command `git push origin <end>:refs/heads/<branch>` and the link `https://github.com/<owner>/<repo>/compare/<base>...<branch>?expand=1`. Add one line: merge it with a merge commit, never a squash — a squash brings the merged module back into the next pull request. The remote is not touched.

## Step 4: create

Ask once:

```
AskUserQuestion: Push <end short> to origin/<branch> and open or update the PR?

Options:
1. Push and open/update
2. Only print the text
3. Cancel
```

With uncommitted changes (Step 0.7), `Only print the text` is replaced by `Stop — I will commit first`.

1. **Push** — `git push origin <end>:refs/heads/<branch>`, `<end>` as Step 1 resolved it (`HEAD` when the end is `HEAD`). The command is announced as the push it is, never as a check or a dry run. The remote refuses it (non-fast-forward, a protected branch) → print git's answer and `WARN [pr] push refused — nothing was forced; the branch on the remote has commits this branch does not`, and stop. After the push, `git ls-remote origin refs/heads/<branch>` must print the full `<end>`; a different SHA → `WARN [pr] origin/<branch> is at <short>, not <end short> — check the push`, and stop before any pull request call.
2. **Find the branch's pull request** — `list_pull_requests` with `head: "<owner>:<branch>"` and `state: "open"`.
   - None → `create_pull_request` with `base`, `head: <branch>`, `title`, `body`.
   - One → `update_pull_request` with `title` and `body`, and the line `PR #<n> updated — it now also covers <modules>`: a pull request follows its head branch, so the new module is already in it.
   - More than one → update the newest, and `WARN [pr] <n> open PRs for <branch> — updated #<newest>`.
3. **GitHub refuses a call** (an authorization error) → `WARN [pr] GitHub refused the request (<status>) — check that GITHUB_PAT is set for the agent's environment`. The text is already printed.

## Step 5: merge

Only at the `merge` level, and only after Step 4: read `{{skills_dir}}/{{self_name}}/references/safe-merge.md` and follow it.

## Never

- Never merge the base branch into the feature branch, and never resolve a conflict — both are a developer's decisions.
- Never force-push, never squash, never rebase.
- Never decide where the pull request ends silently — inside a module that is the Step 1 question.
- Never open a second pull request for a branch that has one open.
- Never commit, and never write into a plan: a plan's state is read from its checkboxes.
- Never call the GitHub MCP tools that write into the repository past git — `create_or_update_file`, `delete_file`, `create_branch`.
- Every action on the remote — a push, an opened or updated pull request, a merge — happens only after the user confirmed it.
