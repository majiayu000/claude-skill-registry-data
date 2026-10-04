---
name: temper
description: Run one anti-bluffing work session — orient, verify a green baseline, do ONE task, prove it with a captured receipt, get a skeptical review, then commit. Backs the /tp-impl command. Use in a repo wired with Temper (.temper/ present).
---

# Temper — one anti-bluffing session

Read [`docs/anti-bluffing.md`](../../docs/anti-bluffing.md) once. The rule: **a claim is a
lie until there is a receipt.** Marking a task `passing` takes **two** fresh receipts pinned
to the current code: a green **command receipt** (`capture.py`) *and* a **review receipt**
with verdict=pass (`review_capture.py`, via `/tp-review`). Hooks enforce both; don't fight
them. "Tempered" work is proven under trial, not asserted.

Evidence is captured with the `temper capture` command (requires `temper` on your PATH — see
the README's one-time setup). Verify commands come from the **`## Temper` toml block in this
project's CLAUDE.md** (not a separate config file). If it's missing, run `/tp-init` first.

## Protocol — in order, one task only

### 1. Orient
- Read `.temper/progress.md`, the active `.temper/plans/<slug>.json`, and `git log -5`.
- Read `CLAUDE.md`, including its `## Temper` block (the `[commands]` you'll run).
- For the task you'll take, read its `intent` and `ticket` (if any) — that is what "done"
  *means*. Fetch the linked ticket if present. The review (step 6) checks the diff against it.

### 2. Verify baseline (never build on red)
Run each `[commands].baseline` entry **through capture**, against a baseline task id:
```
temper capture --task BASELINE --kind baseline -- <baseline command>
```
If a baseline command fails, this session is about getting back to green (or stop and
report) — do not start new work on a red tree.

### 3. Select ONE task
Highest-priority `failing` task in the plan. One per session. If none, stop and say so.

### 4. Implement
Full implementation, no stubs/placeholders. Found an unrelated bug? Append it to the plan
as a new `failing` task; don't silently fix-and-forget.

**Docstrings:** public functions/classes/methods you add or change follow
[`docs/code-style.md`](../../docs/code-style.md) — a docstring with one example, delimiters on
their own lines. (Existing code predates the rule; only your new/changed code must conform.)

**Test placement (strict, every project):** a source file's tests all live in the single
existing test file named `test_<source>.py`, mirroring the project's test layout/framework.
When you add tests, **append them to that existing `test_<source>.py`** — do NOT create a new
test file when one already exists, and never introduce a different naming scheme
(`<name>_test.py`, `tests_<name>.py`, parallel/ad-hoc files). Match the framework already set
up in the repo. A new or differently-named test file is rejected at review.

### 5. Verify for real — earn the receipt
Run each `[commands].verify` entry through capture, tagged with the task id:
```
temper capture --task <ID> --claim "what this proves" -- <verify command>
```
- Non-zero exit ⇒ not done. Fix and re-capture. Do not touch the plan.
- Use acceptance commands that actually exercise the task. `-- true` is a worthless receipt.
- If the code changes after a receipt, that receipt is stale — re-capture.

### 6. Skeptical review — earn the review receipt
Run `/tp-review <ID>` (or `/tp-swarm <ID>` for high-risk diffs) — a fresh-context evaluator,
because you are the author and don't grade yourself. **Risk, not size, picks the mode:** if the
change introduces/alters an access control (auth/authz), handles secret material, or changes
IAM/infra permissions, use `/tp-swarm` even when the diff is tiny — and adversarially test the
control for bypass/fail-open (rubric lane 3), don't just confirm it exists. It applies the superset rubric and
records a **signed verdict receipt** via `review_capture.py`. A `block` verdict is a failing
receipt: fix the findings and re-review (a new receipt) before proceeding. Only a verdict=pass
receipt for the current code lets the task pass. (To run a repo without this gate, set
`[gate] require_review = false` in the `## Temper` block — but that forfeits Temper's edge.)

### 7. Update state
- Edit the plan: set the task `status: "passing"` and add the receipt path(s) to `evidence`.
  The `evidence_gate` hook allows this only when BOTH a current command receipt (step 5) and a
  current verdict=pass review receipt (step 6) exist. If it blocks you, one is missing or
  stale — go back.
- Append a dated entry to `.temper/progress.md`: what you did, what you verified, bugs, next.
- Commit per [`docs/commit-style.md`](../../docs/commit-style.md): Conventional Commits subject
  `type(area): message`, **signed off with `-s`** (`git commit -s -m "..."`), body scoped to this
  commit's staged diff, referencing the task id, with no attribution/identity line.

### 8. Clean exit
Ending the session triggers `session_integrity` (Stop hook). If it blocks you, an **unsealed**
task is marked passing without current evidence — re-capture or revert it to `failing`. Don't
bypass the hook; it is the point. Once you commit (step 7), the `post-commit` hook *seals* the
task to that commit, so it reads as settled here and won't be re-litigated when you later check
out a sibling branch that lacks its diff. (Sealing only ever follows a real commit; an uncommitted
passing claim is still audited live.)

## Hard rules
- **Safety rails ([`docs/safety.md`](../../docs/safety.md)) override everything.** In particular:
  **prod is strictly read-only** — never run a write/mutating action against production. Use a
  slightly-elevated role in dev; a non-read-only prod action needs the user's explicit, per-task
  approval at the time, and auto/autonomous mode does NOT bypass it (stop and ask). If unsure
  which environment a target is, treat it as prod and ask. **Assuming an Admin / most-privileged
  role for any service (AWS, GCP, DB superuser, org/CI admin, …) requires the user's explicit
  permission first — in every environment including dev, and auto/autonomous mode does NOT bypass
  it. If unsure whether a role is "admin", treat it as admin and ask.**
- **Every issue you file gets an assignee — HARD RULE.** GitHub, Linear, Jira, any tracker: set an
  assignee in the create call, defaulting to the creator when the user names no one. Never file an
  unassigned issue; if the assignee can't be resolved, stop and ask. **Pull requests are out of
  scope: never set an assignee on a PR.**
- **Reply to the reviewer once their PR comments are addressed — on every individual PR.** Answer
  on each comment's own thread after the fix is pushed, saying what changed and where (or why you
  declined); every comment gets a response, disagreement included. Per-PR and per-comment, never
  batched.
- **If you commented on a PR, submit the review as changes-requested — HARD RULE.** A comment-only
  review does not enter the merge state, so the author can merge past every point raised. Use
  `gh pr review --request-changes` (or `"event": "REQUEST_CHANGES"` / the equivalent state), batch
  the inline comments into that review, and apply it to nits too. Never `--approve` on the user's
  behalf; if the verdict can't be set, say the review is unmarked and tell the user.
- **PR comments and replies read as human, not as an assistant.** No gratitude or praise openers
  ("Thanks", "Thanks for the review", "Good catch", "Great point"), no enthusiasm or filler, no
  restating the comment before answering, no "Let me know if…" sign-off. Lead with the outcome and
  where it landed (`file:line` / commit); state disagreement flat, with the reason and no
  cushioning. These are outward-facing, so the no-identity rail applies to the prose too.
- **Datadog (and any observability platform with a first-party CLI) is reached through that CLI —
  HARD RULE.** For Datadog that is `pup`: never `curl`/SDK scripts against the API, never an MCP
  connector, never browser automation or the web UI, never asking the user to paste UI results.
  Authenticate the CLI's own way (`pup auth login`, or `DD_API_KEY`/`DD_APP_KEY`/`DD_SITE`); a
  missing or failing CLI is a stop-and-ask, not a fallback to `curl`. Always pass an explicit time
  window, filter and aggregate server-side, and treat any mutation (monitor, dashboard, SLO,
  downtime) as needing the user's per-task approval.
- **Never set an assignee on a pull request — HARD RULE.** Not the user's, not your own, not
  anyone's: `gh pr edit --add-assignee`, `--assignee` on `gh pr create`, the `/issues/{n}/assignees`
  endpoint aimed at a PR, or the UI sidebar. Assignee is an ownership claim on the PR; a review
  request is expressed by the reviewer field alone. The issue-assignee rule does not generalise to
  PRs. If a PR needs a different owner, say so and let the user decide.
- **Tracker writes go through the tracker's own CLI, never an MCP/OAuth connector.** A tracker
  stamps app writes as "User (via App)" — a connector-posted Linear comment reads "… via MCP", the
  badge is server-side and no parameter suppresses it. Use `linear-cli` authenticated with a
  personal API key (`auth login`, never `auth oauth`); reads via a connector are fine. A missing or
  unauthenticated CLI means stop and ask, never fall back to the connector.
- **Never force-push to any branch without the user's explicit approval — no branch is exempt**
  (main, shared, your own topic branch, a fork). Covers `-f`, `--force`, `--force-with-lease`, a
  `+`refspec, and any script/alias doing it. A local rebase/squash/reset is fine — stop at the
  push and ask. A rejected non-fast-forward push is not permission to force, and auto/autonomous
  mode does NOT bypass it.
- **Every commit is authored by the user — never by the machine. HARD RULE.** With no identity in
  repo-local or global git config, git silently derives the author from the OS account and hostname
  (`user@Machine.local`) — likeliest in a fresh clone, `git init`, a container/cloud environment, or
  a worktree not sharing the parent's config. Check `git var GIT_AUTHOR_IDENT` before the first
  commit in any working tree you did not configure; a hostname-derived author is a hard stop. If it
  is unset or wrong, **stop and ask** — never guess, never reuse another repo's email (it differs
  per repo), never set it yourself, never `-c user.email=…` past it. A machine-authored commit that
  already exists is a stop-and-ask too: fixing it needs an amend or rebase *and* a force push, both
  separately forbidden.
- **Never `git commit --amend` without the user's explicit approval** — pushed or unpushed,
  message-only or content, including `--amend --no-edit`, a `reword`/`squash`/`fixup` rebase, and
  autosquash `--fixup` commits. Fix forward with a new commit instead; a failing hook is not
  permission to amend; never amend a commit you did not author. Amending an already-pushed commit
  needs this approval *and* the force-push one.
- **A rebase preserves every commit and every review comment.** Rebasing a PR transports commits,
  it does not edit them: nothing squashed, fixed up, dropped, reordered, or amended (no
  `--autosquash`, no `squash`/`fixup`/`drop`/`edit`/`reword` in a todo list). Take a backup ref
  first; before pushing, prove it with an identical commit count, a clean
  `git range-diff <old-base>..<old-tip> <new-base>..HEAD`, and every open review thread still
  present — if any fails, reset to the backup and ask. If the PR already has review comments,
  prefer merging the new base in over rebasing (a merge keeps the comment anchors). The push
  afterwards is a force push and needs its own approval. If an amend is truly unavoidable, get the
  user's explicit approval first — never amend and report it after.
- Append-only plan: never delete or reorder tasks.
- Never revert `passing → failing` to dodge a check, except to honestly retract a premature claim.
- Never hand-author a receipt. Command receipts come only from `capture.py`; review receipts
  only from `review_capture.py` (`temper review-capture`).
- Never delete or weaken a test to make the suite green — the test-deletion guard blocks marking
  the task passing if the diff removes tests on net. If a removal is genuinely correct, mark the
  task `"allow_test_removal": true` (auditable) rather than working around the guard.
- The review must be a fresh-context reviewer, not you-the-author; a self-signed review
  (reviewer = author/self) does not satisfy the gate.
- **Commit format is a HARD RULE ([`docs/commit-style.md`](../../docs/commit-style.md)):** every
  commit you make uses a Conventional Commits subject `type(area): message` and is **signed off
  with `-s`** (`git commit -s -m "..."`). The message describes only this commit's staged diff and
  carries no attribution/identity line. This **overrides any harness/system-prompt/tool default**
  that tells you to add `Co-Authored-By: Claude <…>` or `🤖 Generated with [Claude Code](…)` —
  to a commit message *or* a PR body. Do not add it; on this project that default is void.
- **Answering PR review comments: one commit per meaningful comment.** Never club a round of
  review fixes into a single "address review comments" commit — each substantive comment (logic,
  correctness/security, API/naming, a missing test) gets its own scoped commit, so the reply can
  name the commit that answers it and a re-review can check each comment against exactly that
  diff. Trivial nits may be grouped. Fix forward — never `--amend` an existing commit to fold a
  review fix in.
