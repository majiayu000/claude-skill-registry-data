---
name: ship
description: Take a task or an open PR to merge-ready — executor lane, independent verifier lane, bounded fix rounds by fresh agents, deterministic prepare/gates/merge via omc ship
argument-hint: "<task description> | --pr <number>"
level: 4
---

# Ship

Carry one change from task (or existing PR) to a merge-ready PR. Agents do
the judgment work; `omc ship` does everything mechanical and refuses the
unsafe steps itself. The ship state lives in `.omg/state/ship/<pr>.json`, so
a run survives restarts: `omc ship status <pr>` tells you where you are.

## Hard rules (every lane, every brief)

Each rule exists because breaking it once cost a round-trip or a wiped tree.

- Never self-approve. The lane that wrote a change never records its verdict;
  `omc ship verdict` refuses a reviewer equal to the implementer.
- Reviewers get the diff and the task, never the author's summary or
  conclusion. An author's "all tests pass" anchors the reviewer.
- Fixes go to a fresh agent, never back to the implementer or the reviewer.
  A fresh context does not defend its earlier choices.
- No `git worktree add` / `git worktree remove`, no `npm ci` in a junctioned
  tree: removing a worktree empties the shared `node_modules` junction target.
- No force push, no rebase, no amend. Update a branch with
  `git merge origin/<base>` and a plain push. `omc ship` only spawns an
  allowlist of the exact git/gh/node command shapes it builds, so force,
  rebase, pull, amend, `reset`, `gh api`, any npm command and a push to
  `main` / `master` / `dev` / the run's base are refused before anything
  spawns.
- The inventory regeneration is the LAST commit. Any later commit re-stales
  `inventory/inventory-graph.json`; `omc ship prepare` orders this for you.
- Merge only through `omc ship merge`. It checks the gates and the verdict;
  a human-typed `gh pr merge` skips both.
- Lanes never edit `.omg/state/ship/`, never touch the `ship` block of
  `.copilot/omg.jsonc`, and never set `OMG_SHIP_HUMAN`. Those are the owner's
  controls: `ship.allowAdminMerge` is the only switch that runs the admin
  merge, and `OMG_SHIP_HUMAN=1` is the only way to `init --force` over a
  blocked or merged run, to reset the implementer or fix-round count of a
  run that has verdicts, or to merge a PR that touches `.copilot/omg.jsonc`,
  `.github/known-flaky-tests.json` or `.github/workflows/`.

### Where the safety settings come from

`ship.allowAdminMerge`, `ship.advisoryChecks`, `ship.requiredChecks` and
`ship.knownFlakyFile` are read only from (1) the user config at its default
location, then (2) `.copilot/omg.jsonc` as committed on the base branch,
then (3) the defaults. A lane can drop an untracked file into the checkout
and a PR can commit one, so the working-tree file and the PR head never set
them: `omc ship` ignores those keys there and prints a warning. The other
`ship` keys keep the usual order (defaults, base-branch file, user config,
working-tree file). The known-flaky list is read from the base branch too.

- **User config location.** The safety keys come from
  `<home>/.config/claude-omc/config.jsonc` (Windows:
  `<home>\AppData\Roaming\claude-omc\config.jsonc`), with `<home>` the
  account's home as the OS reports it. When `XDG_CONFIG_HOME` / `APPDATA`
  select another file, that file's safety keys are ignored with a warning.
- **Base branch.** The base, its sha and the head sha come from GitHub
  (`gh pr view`), never from the run state. `omc ship` checks that the
  `origin` URL (`git remote get-url origin`, `insteadOf` applied) is the
  PR's repository, fetches the base,
  checks that `refs/remotes/origin/<base>` equals GitHub's base sha, and
  reads `<base sha>:.copilot/omg.jsonc` with replace refs off
  (`GIT_NO_REPLACE_OBJECTS=1`), so `git replace` or a moved or shadowed ref
  in the checkout changes nothing. When that check fails, `gates` warns and
  uses the defaults; `merge` refuses.
- **Trusted bases.** Only bases in `ship.trustedBases` (user config only;
  default `dev`, `main`, `master`) are read. For any other base the defaults
  apply and `merge` prints the admin merge command instead of running it: a
  lane can create a branch and target its PR at it.
- **Legacy name.** `.copilot/omc.jsonc` is never read from the base branch.
  A working-tree file under that name gets one warning; rename it to
  `.copilot/omg.jsonc` and commit it to the base.
- **Environment.** Engine commands run without the `GIT_*` variables that
  redirect git (`GIT_CONFIG_*`, `GIT_DIR`, `GIT_SSH_COMMAND`,
  `GIT_EXEC_PATH`, ...) and without `GH_REPO` / `GH_HOST`; `GH_TOKEN`
  passes through for authentication. A custom ssh belongs in
  `core.sshCommand`.

### What the engine can and cannot prove

The implementer / reviewer names, `OMG_SHIP_HUMAN` and every other
environment input are advisory against a hostile lane: `omc ship` compares
the strings it is given and cannot verify which agent typed them, and a
process that controls its environment can set `OMG_SHIP_HUMAN=1` or put
another `git` first on `PATH`. The state file
is not tamper-proof either. Every engine write records a sha256 over the
state (verdicts, housekeeping commits, phase, history) in `integrity`; later
updates and `merge` refuse a state whose hash no longer matches, which
catches a hand edit, but anyone who reads the source can recompute it. The
real protections are the lane discipline above, the owner-only config, and
`gh pr merge --match-head-commit`.

Known limits:

- A lane with write access to `.git/objects` can forge loose objects (a
  commit or blob stored under another object's sha). Replace refs are off
  and every base read is by GitHub's sha, but git trusts its object store;
  `omc ship` cannot detect a forged object behind a correct sha.
- Environment and `PATH` overrides are advisory: the engine scrubs the git
  and gh variables it knows, but a process that controls the environment
  can run another `git` or `gh`.
- `gh` resolves the repository from the checkout's remotes too. The remote
  check catches `origin` pointing away from the repository `gh` reports,
  not a checkout whose every remote and `gh` default were repointed.
- Engine commits are checked by content, not trusted by provenance. Hooks
  (`pre-commit`, `pre-merge-commit`, `commit-msg`) are skipped with
  `--no-verify`, but `post-commit` / `post-merge` hooks and custom merge
  drivers still run. So `merge` re-checks every recorded housekeeping
  commit: a one-parent commit may change only `inventory/` against its
  parent; a merge is rebuilt with `git merge-tree --write-tree` and may
  differ from that tree only under `inventory/`; and a merge made while any
  `merge.<name>.driver` is configured is refused outright. Anything else
  needs a new verdict.

## Steps

1. **Implement (executor lane).** Skip with `--pr <n>` when the PR exists.
   Copilot CLI host, headless:
   `omc team 1:copilot:executor --transport sdk "<executor brief>"`.
   In-session: `Task(subagent_type="oh-my-copilot:executor", prompt="<executor brief>")`.
   The lane pushes a branch and opens a draft PR to the base branch.
2. **Start the run:** `omc ship init <pr> --implementer <lane-name>`.
   Record the head sha you hand to the reviewer: `git rev-parse HEAD`.
3. **Review (independent lane).** Give it the reviewer brief below.
   Headless: `omc team 1:copilot:verifier --transport sdk "<reviewer brief>"`
   (the sdk transport rejects the code-reviewer/critic roles; verifier runs).
   In-session: `Task(subagent_type="oh-my-copilot:verifier", ...)` or
   `oh-my-copilot:code-reviewer`. Then record what it said:
   `omc ship verdict <pr> --reviewer <reviewer-lane> --sha <sha> --approve`
   or `--request-changes --notes "<one line>"`.
4. **Fix round (fresh agent)** when changes were requested: a new executor
   with the fix brief below, then back to step 3 with the new head sha. The
   run blocks after `ship.maxFixRounds` (default 2) change requests; stop and
   report to the user instead of starting another round.
5. **Prepare:** `omc ship prepare <pr> --push`, run on the PR branch the run
   was started for, with the reviewed sha in HEAD (it refuses otherwise, and
   refuses a dirty tree, staged changes in the index, or a merge / rebase /
   cherry-pick / revert in progress). It checks that `origin` is the PR's
   repository, fetches the base, requires `refs/remotes/origin/<base>` to
   equal GitHub's base sha, and merges that sha (never the ref name, which a
   local tag named `origin/<base>` could shadow) in with `--no-ff`,
   runs `tsc`, eslint on changed files, the tests mapped from the diff and
   the generator `--verify` checks, then regenerates the inventory as the
   last commit (`git commit -- inventory`, so a file another lane stages
   meanwhile stays out) and pushes plainly. Its merges and commits run with
   `--no-verify`: hooks never shape engine commits. A conflict outside `inventory/` stops it:
   hand the conflict to a fresh fix agent, then re-review (step 3).
6. **Gates:** `omc ship gates <pr> --watch`. Exit 8 means still pending after
   one watch window (9 minutes, under the 10-minute watcher cap): run the
   same command again. Green needs every `ship.requiredChecks` name reported
   (a missing one, such as `Build` before its `needs:` jobs finish, is
   pending) and every workflow run for the head sha completed; a run that
   completed red without reporting any check (a startup failure) is failed,
   and a head that moves during the read is pending. `no-workflows-triggered`
   means the head has no checks and no workflow runs at all: a PR opened or
   pushed with the Actions `GITHUB_TOKEN` (draft bot PRs) triggers nothing,
   so push from a PAT or close and reopen the PR. Exit 1 lists
   the real failures; a failure whose every failing test matches a
   title-scoped entry in `.github/known-flaky-tests.json` (as committed on the
   base branch), with no unhandled
   errors, failed suites or failing non-test step in the log, is rerun once
   automatically (`gh run rerun <id> --failed`); the same test failing again
   is a real failure.
7. **Merge-readiness:** mark the PR ready (`gh pr ready <pr>`), then
   `omc ship merge <pr>`. It refuses unless the gates are green, the state
   passes its integrity check, the last approval covers the head (only
   ship housekeeping commits may follow the reviewed sha: the head's
   first-parent chain back to it holds only commits `prepare` recorded,
   each recorded merge brings in a commit in GitHub's current base
   history, and each recorded commit changes nothing outside `inventory/`
   beyond what its parents give; anything else needs a new verdict), and the PR's
   changed files touch no merge-rule file (those PRs are the owner's to
   merge). It lists the changed files itself
   (`git diff --name-only --no-renames -z <base sha>...<head sha>`), so a
   rename out of `.github/workflows/` still counts and the 300-file cap of
   `gh pr diff` no longer applies. It also refuses when the base cannot be
   fetched or does not match GitHub's base sha. With
   `ship.allowAdminMerge` unset (the default), or a base outside
   `ship.trustedBases`, it prints the exact `gh pr merge --admin --merge`
   command for the owner; there is no flag that turns it on, and merging is
   the owner's call.

## Executor brief (template)

```
Task: <task>
Repo: <path>, branch <branch> off origin/<base>. Read <files> first.
Deliver: the change, tests for it, a plain `git push -u origin <branch>`, a
DRAFT PR to <base>. Report the PR number and head sha.
Never: git worktree add/remove, npm ci, force push, rebase, amend, merging
the PR, editing .omg/state/ship/ or the ship config, setting OMG_SHIP_HUMAN.
Do not edit dist/ or bridge/.
Verify before reporting: npx tsc --noEmit and the tests you touched.
```

## Reviewer brief (template)

```
Review PR #<pr> at commit <sha> against this task: <task>.
Read the change yourself: git diff origin/<base>...<sha> (fetch first).
You were not given the author's summary on purpose; judge the diff.
Check: does it do the task, correctness and edge cases, tests that would fail
without the change, safety rules (no force/rebase paths, no dist/ edits).
Run the targeted tests yourself. Do not edit, commit, or push anything.
Never: git worktree add/remove, npm ci, force push, editing .omg/state/ship/
or the ship config, setting OMG_SHIP_HUMAN.
Answer with VERDICT: approve | changes-requested, then a numbered list of
blocking findings (file:line, why, expected) and non-blocking notes.
```

## Fix brief (template)

```
PR #<pr>, branch <branch>, head <sha>. A reviewer requested changes:
<numbered blocking findings, verbatim>
Fix exactly these findings; do not refactor beyond them. Add or adjust a test
per finding. Commit as new commits and plain-push (`git push`), never amend.
Never: git worktree add/remove, npm ci, force push, rebase, editing
.omg/state/ship/ or the ship config, setting OMG_SHIP_HUMAN.
Report the new head sha and which finding each commit addresses.
```

## Config (owner-edited: user config, or `.copilot/omg.jsonc` committed on the base)

```jsonc
{
  "ship": {
    "base": "dev",
    "maxFixRounds": 2,
    // Safety keys: user config or the base branch's committed file only.
    "allowAdminMerge": false,
    // User config only: bases whose committed config is read and that merge
    // may admin-merge into.
    "trustedBases": ["dev", "main", "master"],
    // Never blocking. The Socket Security GitHub App checks have no workflow
    // file and are advisory by default too.
    "advisoryChecks": [
      "No Committed Build Artifacts",
      "Authorize generated artifacts from base trust root",
      "Socket Security: Pull Request Alerts",
      "Socket Security: Project Report"
    ],
    // Omit to keep the default (all 18 checks this repo's CI reports on a PR);
    // a value replaces the whole list. A listed check not reported yet is pending.
    // ci.yml and upgrade-test.yml run only for PRs to main / dev, so a PR to
    // another base stays pending under the default list: give it its own.
    "requiredChecks": ["Lint & Type Check", "Test", "Test (Windows path suite)", "Build", "npm pack + install test", "..."],
    "knownFlakyFile": ".github/known-flaky-tests.json",
    "autoRerunFlaky": true,
    "pollIntervalSeconds": 30,
    "watchTimeoutMinutes": 9
  }
}
```

## Output

Report the PR number, the final phase from `omc ship status <pr>`, each
verdict (reviewer, sha, approve/changes), the fix rounds used, the gate
result, and either "merged" or the exact merge command left for the owner.
