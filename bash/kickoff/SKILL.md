---
name: "Mission Control: Kickoff"
description: "Start a multi-session run from the coordinator session: pick the tasks, create one worktree per task, record the run in the ledger, write the shared guidance and each session's brief, and hand the user one launch line per session"
when_to_use: "When the user wants several Claude Code sessions working the same repository at once and this session is to coordinate them: 'kick off a run', 'coordinate these tasks', 'set up mission control for 10SE.2, 10SE.4 and 11HD.4'. Needs .claude/mission-control.json (mission-control:configure writes one). Never while a run is already active for the repository."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: mission-control
  goblin-spinner: mustering the crew|digging worktrees|writing briefs|numbering assumptions
disable-model-invocation: true
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash(python3:*)", "Bash(git:*)", "Bash(gh:*)", "Bash(ls:*)", "Bash(sh:*)", "Bash(zsh:*)", "AskUserQuestion", "mcp__mission-control__mc_assume", "mcp__mission-control__mc_board"]
arguments: ["tasks"]
argument-hint: "[task ids...] [name <run name>]"
---

# Mission Control: Kickoff

The coordinator's first hour, done before any crew session exists: facts at a named commit, one worktree per task, the run in the ledger, numbered assumptions, a brief per session. The user starts the sessions; the `SessionStart` hook hands each its brief. The protocol the rest of the run follows is `${CLAUDE_PLUGIN_ROOT}/references/protocol.md`; read sections 1 to 3 before step 3.

The CLI is `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/mc.py`. Every write to the ledger goes through it.

---

## Step 0: Parse the arguments

Tokens before `name` are task ids (`10SE.2`), matched against the roadmap when there is one. `name <run name>` names the run; default: the task ids joined with `+`, or the date.

```text
Usage: /mission-control:kickoff [task ids...] [name <run name>]
```

## Step 1: Preconditions

1. `mc.py detect`. Exit 2: stop and say `/mission-control:configure` writes the project config; nothing else happens without it.
2. `mc.py --json status` (the flag goes before the subcommand). A non-null `run`: stop and name it; `/mission-control:end` closes a run.
3. `git fetch origin` in the main checkout, then record the base: `git rev-parse origin/<default branch>` (origin's HEAD), or the branch the user names. Check it is on origin: `git ls-remote --exit-code --heads origin <base>`. A base that is not (a feature branch the PRs will stack on) cannot be a PR target until the user pushes it, and the push publishes its commits, so it is the user's: `mc.py start` puts it on the needs list as item 1 and warns; say so in the hand-over and do not expect a PR before it is done. This sha is quoted in the guidance and every brief; every shared fact is checked at it.
4. `mc.py probe`. Relay what the machine holds (a running server, a migration on the stack from a worktree that is not in this run). It becomes a shared fact.

## Step 2: Choose the tasks

With task ids given, use them. Without, look for a roadmap CLI in order: `$HOME/.claude/marketplace/roadmap/scripts/roadmap.py`, then `$HOME/.claude/plugins/marketplaces/goblin-mode/marketplace/roadmap/scripts/roadmap.py`. Found and `.claude/roadmaps.json` present: `roadmap.py ready --json`, show the candidates as `id · description · unblocks n · milestone` and ask with AskUserQuestion (multi-select) which ones run together. No roadmap: ask for the tasks as free text, one line each.

For each task, read enough of the codebase to answer: which files it will touch, which of those another chosen task also touches, whether it needs a migration, which shared resources it will need. Two tasks on one file, function or table is the thing this run exists to manage: list every overlap.

## Step 3: Conventions and facts

1. Read every file in the config's `conventions` list. Distil the rules this run leans on (where a task runs commands, how PRs land, what regenerates, what never goes on a branch).
2. Read the config's `facts` list: the user's own words for conventions not written in the repository.
3. Anything a brief will need to state that neither source holds (a changelog rule, an env-file layout, a merge order) is **asked** with AskUserQuestion now, never asserted. Offer to add the answer to the config's `facts` so the next run has it; edit the config only on a yes.

## Step 4: Plan, then confirm

Build the table: task, title, branch (project naming: `feat/`, `fix/`, lowercase, hyphens), worktree name (`<task id lowercased without the dot>-<two words>`, under the config's `worktrees.dir`), migration timestamp if needed (the config's `migrations.timestamp_format`, one per task, in the merge order you propose, distinct by at least an hour) and the shared resources each will need.

Ask two things with AskUserQuestion:

1. **The plan**: approve, or change the merge order, a branch name or a task.
2. **PR approval**: `the coordinator reviews each draft PR description and the crew runs pr-create auto (Recommended)` or `the user approves pr-create in each session, as before`. The first removes a visit per session; the merge stays the user's either way.

Nothing below runs before both answers.

## Step 5: Worktrees and claims

For each task, in the main checkout:

1. `git worktree add -b <branch> <main>/<worktrees.dir>/<name> origin/<base>`. A branch that already exists: `git worktree add <path> <branch>` and say so.
2. `zsh "${CLAUDE_PLUGIN_ROOT}"/scripts/worktree-bootstrap.sh <path>` (it is a zsh script; `sh` fails on its array syntax): symlinks the git-ignored `.env*` files and installs every tracked lockfile. Relay its lines; a `failed` line is reported, not retried.
3. With a roadmap: `roadmap.py claim <id> --assignee "<who>"` **inside the worktree** (the claim lives on the branch). Ask who once, for all tasks; never infer a name. Commit with `git commit -m "chore(roadmap): claim <id>" -- .claude/roadmaps.json`.
4. `mc.py crew add --task <id> --branch <branch> --worktree <path> [--migration <timestamp>]`.

Run `mc.py start --name <run name> --pr-approval <answer>` **before** the first `crew add` (crew add needs a run). The run's coordinator is this session, read from `CLAUDE_CODE_SESSION_ID`.

## Step 6: Assumptions, guidance, briefs

1. Set every shared assumption with `mc_assume` (one call each). They are numbered in order and land in the ledger and, from its first turn, in every crew session's system prompt. The ownership rules from the protocol (one author per shared definition, paste the whole body, second to merge rewrites from trunk, thresholds in one place) become assumptions whenever two tasks share code. A shared document is shared by lines, not by rows: two sessions each editing one row of the same table conflict when the rows are adjacent, so the assumption names which side rebases and keeps both.
2. Write `<ledger dir>/guidance.md` from `${CLAUDE_PLUGIN_ROOT}/templates/guidance.md`: crew table, shared facts with where each was read, the assumptions list, the resource rules (the config's notes plus what step 1's probe found), the human gates, the conventions. The ledger dir is in `mc.py status --json` as `ledger_dir`.
3. Write one brief per task at `<ledger dir>/briefs/<task id>.md` from `${CLAUDE_PLUGIN_ROOT}/templates/brief.md`. Criteria are numbered and each names the assumption it leans on. The brief ends with the five questions; it is the whole of what the session is told.
4. Lint both: `~/.claude/library/scripts/slop-scan.py --strict <file>` where that script exists (it is the house style gate); fix every hit.

## Step 7: Hand over

Print one line per session for the user to run in a fresh terminal:

```text
cd <worktree> && claude --name "<task id lowercased> <two words>" "Start: you are crew <task id> in run <run name>. Read your brief at <brief path>, invoke /mission-control:crew and answer its five questions to the coordinator."
```

The trailing prompt is what starts the session's first turn. Without it an interactive session sits idle at an empty prompt: the `SessionStart` hook only adds context, and the board would show the session as `briefing` with nothing happening (this is what the first board-visuals run did). Add `--plugin-dir <plugin root>` to each line when the plugin is being run from a working tree rather than installed.

Then: nothing else is typed into the session. The `SessionStart` hook names the brief and the coordinator; the mod registers the session on the board when it starts inside its worktree; the brief tells it to answer the five questions. Open the board with `/mc` and invoke `/mission-control:coordinate` for the rest of the run.

## Red flags

**Never:** start a run while one is active; state a convention you did not read or hear from the user; create a worktree for a branch checked out elsewhere; infer a roadmap assignee; run a gated command from here (the coordinator has no worktree and no slot); write a brief that asks a session to run a hosted read or write; skip the PR-approval question (it is the user's choice, and it changes what every crew session does at PR time).

<raw-arguments value="$ARGUMENTS" />
