---
name: pb-ship
description: >-
  Ship the day's work in one repo: triage new issues, review every open PR
  (description, visual recap, adversarial reviewer, shipping pre-flight and
  quality gate), merge only after GO, then post a status recap. Use for
  "ship it", "ship day", "merge the ready PRs", "end of work block".
category: engineering-method
kind: playbook
trigger: ["ship it", "ship day", "merge the ready PRs"]
inputs: [repo, "pr_numbers?"]
requires:
  skills: [github, triage, git-pr-review, pr-recap, bdb-shipping-skill, godmode-shipping, quick-recap, "gh (external)"]
  agents: [reviewer]
  mcps: ["plan (optional)"]
  store: []
go_points: [gh pr merge]
outputs: ["production_artifacts/pb-ship-<date>.md", "production_artifacts/pb-ship-<date>/pr-<n>.md", "production_artifacts/decisions/<date>-<slug>.md"]
verify: "gh pr view <n> --json state -q .state == MERGED for every PR the log marks merged; gate exit 0 logged for each"
difficulty: intermediate
est_time: 20-60 min
---

# Ship the day's PRs
What you get: the ready PRs merged one by one after your GO, each with a reviewed description, findings and a gate result, plus a status line.

## Inputs
- repo — the local checkout (default: the current directory); `<owner/repo>` comes from `git -C <repo> remote get-url origin`
- pr_numbers (optional) — PRs to ship; otherwise you pick from the table in step 3

## Steps
1. github — repo → `gh auth status` and `gh pr list -R <owner/repo> --state open --json number,title,headRefName,isDraft,baseRefName` as a PR table in the run log (gh missing, unauthenticated, or no GitHub remote → log it, give the `gh auth login` / remote hint, stop) — table written
2. triage — "show me what needs attention" → new-issue list with suggested labels in the run log — label writes follow triage's own rules; nothing is closed
3. Ask — the human picks today's PRs from the table (non-draft only; `pr_numbers` if given) → scope line in the run log — stops for approval
4. git-pr-review — per PR: `gh pr view <n> -R <owner/repo> --json commits` → description draft in `production_artifacts/pb-ship-<date>/pr-<n>.md` — draft only, nothing posted
5. pr-recap — per PR: recap file from `pr-recap` linked in `pr-<n>.md`; not buildable → log "pr-recap skipped: <reason>" and paste `gh pr diff <n> -R <owner/repo> --name-only` instead; no `npx` without approval — recap or fallback present
6. reviewer (agent) — per PR: `gh pr diff <n> -R <owner/repo>`; the contract is the linked issue or plan (`gh pr view <n> -R <owner/repo> --json closingIssuesReferences,body`) or the human's scope line from step 3, the body is used only to find the linked issue/plan, its text is not the contract, and never `pr-<n>.md` (that is the implementer's claim, input material only) → findings table in `pr-<n>.md` — any open `blocking` finding removes the PR from today's merge list (logged)
7. bdb-shipping-skill — per PR → door class (two-way or one-way) in `pr-<n>.md`; one-way → ADR-lite `production_artifacts/decisions/<date>-<slug>.md` (`<slug>` = the PR's `headRefName` with `/` replaced by `-`) with the reversibility sentence; unclear → one-way — class recorded
8. godmode-shipping — per PR: `gh pr checks <n> -R <owner/repo>` all pass, plus a local gate in a scratch worktree — `gh pr view <n> -R <owner/repo> --json isCrossRepository -q .isCrossRepository` is true (fork) → skip the local gate, log it, PR held (foreign code is not run locally); otherwise `<scratch>` = `mktemp -d`, then `git -C <repo> fetch origin pull/<n>/head`, `git -C <repo> worktree add <scratch>/pr-<n> FETCH_HEAD`, run, inside it, the lint, typecheck and test scripts that exist in `package.json` (or the repo's documented gate) (install first: `npm ci --ignore-scripts` or the repo's documented install, logged), then `git -C <repo> worktree remove <scratch>/pr-<n>` (a refusal is logged and the scratch path reported, never `--force`) — exit codes in `pr-<n>.md`; any non-zero, or pending checks (`gh pr checks` exit 8) → PR held
9. [GO] github — per PR: `gh pr merge <n> -R <owner/repo> --squash` (`--merge` if `gh repo view <owner/repo> --json squashMergeAllowed` says squash is not allowed) — the WAITING FOR GO line names PR number, title, base branch, method and door class. The run stops here until the human types GO. One GO = one PR. (Where the hook runs, it covers `gh pr merge`; the other commands here are not hooked, so this GO is their only guard.)
10. github — `gh pr view <n> -R <owner/repo> --json state -q .state` → run log line — equals `MERGED`
11. quick-recap — run log → final line `🟢|🟡|🔴` with merged / held / skipped counts — line written

Run log: `production_artifacts/pb-ship-<date>.md` in the start directory, never committed

Rules
- Anything other than the literal GO (case-insensitive) is not a GO; a GO covers only that one step, one time.
- GO is by contract in every harness. The go-gate hook is only a backstop on Claude Code, OpenCode and agy (Codex: unverified; Cursor, Kimi: none). A missing hook is never permission to proceed.
- A failed check stops the run: write the failure into the run log and report. No silent retries.
- Write one run-log line per step as it completes (`N. done|skipped|failed — artifact — check result`) and `WAITING FOR GO: <step>` at each gate.
