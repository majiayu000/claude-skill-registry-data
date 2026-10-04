---
name: pb-bug-fix
description: >-
  Turn a GitHub issue into a tested fix on a branch with an open PR: read the
  issue as the contract, find the root cause, write the failing test first,
  fix, prove it, review the diff against the issue, push and open the PR only
  after GO. Merging stays with pb-ship. Use for "fix issue 42", "bug fix from
  this issue", "turn this issue into a PR".
category: engineering-method
kind: playbook
trigger: ["fix issue", "bug fix from issue", "issue to PR"]
inputs: [repo, issue_number]
requires:
  skills: [github, deja-memory, systematic-debugging, test-driven-development, verification-before-completion, git-pr-review, "gh (external)"]
  agents: [reviewer]
  mcps: []
  store: []
go_points: ["git push + gh pr create"]
outputs: ["production_artifacts/pb-bug-fix-<date>.md"]
verify: "new test fails on the base SHA and passes on the branch SHA; gh pr view <branch> --json closingIssuesReferences contains <n>"
difficulty: intermediate
est_time: 30-90 min
---

# GitHub issue to tested fix and PR
What you get: a branch with a failing-then-passing test and the fix, reviewed against the issue, and an open PR that closes it. Merging is a separate run (pb-ship).

## Inputs
- repo — the current directory, or the one the user names; `<owner/repo>` comes from `git -C <repo> remote get-url origin`
- issue_number — the GitHub issue to fix, asked if missing

## Steps
1. github — repo, issue_number → `gh auth status`, then `gh issue view <n> -R <owner/repo> --json title,body,labels,state` as the contract (acceptance points as a list) in the run log (gh missing, unauthenticated, no GitHub remote, or the issue is closed → log it, give the `gh auth login` / remote hint, stop) — contract written
2. deja-memory — error text or symptom from the issue → `deja fix` result in the run log — prior fix found, or "none"
3. systematic-debugging — contract → root cause and a local repro command in the run log — repro fails locally on the base SHA (base SHA logged), or the reason it cannot run locally
4. test-driven-development — root cause → failing test first (run, red, output pasted), then the minimal fix on a new branch `fix/<n>-<slug>` — the new test fails on the base SHA and passes after the fix; no unrelated edits
5. verification-before-completion — repro command and the repo's test, lint and typecheck scripts that exist → fresh passing output pasted in the run log — output pasted, not claimed
6. reviewer (agent) — `git diff <base>...HEAD`; the contract is the issue from step 1, never the run log and never the implementer's claim (input material only) → findings table in the run log — any open `blocking` finding sends the run back to step 4, at most 2 cycles, then stop and escalate
7. git-pr-review — `git log <base>..HEAD` → PR body draft in the run log, ending in `Fixes #<n>` — draft only, nothing posted
8. [GO] git push + gh pr create — `git push -u origin <branch>` then `gh pr create -R <owner/repo> --base <base> --head <branch> --title "<title>" --body-file <draft>` — the WAITING FOR GO line names branch, base, title and issue number. The run stops here until the human types GO. One GO covers the push and the PR creation, one time. (The hook guards the push only; `gh pr create` is not hook-guarded, so this GO is its only guard.)
9. github — `gh pr view <branch> -R <owner/repo> --json url,closingIssuesReferences` → PR URL in the run log — `closingIssuesReferences` contains `<n>`

Run log: `production_artifacts/pb-bug-fix-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- A failed check stops the run: write the failure into the run log and report. No silent retries beyond what a step names.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
