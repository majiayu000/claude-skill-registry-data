---
name: pull-request
description: '[Git] Use when asked to create, open, finish, update or mark ready a pull request. Runs in the main session with user test and review choices, including explicit skip: branch, commit, open PR, CI to green.'
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
## Quick Summary

**Goal:** Drive current work to a pull request **ready to merge** — not draft, whole-branch review and local tests run or explicitly skipped by the user, every CI check green — with test and review choices before publishing.

**Summary:**

- **Purpose:** one invocation creates a new PR, finishes the current PR, or flips a draft to ready. Invocation IS explicit authority for add/commit/push/PR operations on the selected branch — nothing more.
- **Main session, user choices:** run inline, but STOP for the test and review questions in the [User Choice Contract](#user-choice-contract). Include explicit Skip options; never answer for the user. A PR request or `skillAutoTrigger: false` does not settle these choices.
- **Review decision before commit:** review the whole branch or obtain an explicit user-approved skip for that scope and exact commit candidate. Every later candidate change invalidates earlier evidence and skip decisions.
- **Main steps:** (1) target → (2) fresh branch at the latest target → (3) stage + guard + test choice → (4) whole-branch review choice → (5) verify final evidence → (6) `commit` skill → (7) push + create/ready PR → (8) CI loop until green → (9) mergeable check + report.

**Workflow:**

1. **Target** — base named in request → open PR's base → `pullRequest.targetBranch` (`docs/project-config.json`) → `main`.
2. **Branch** — a PR branch starts at the latest target. Already merged into target → `git switch --no-track -c <type>/<slug> origin/<target>`, no rebase. Otherwise on target or detached HEAD → new branch from HEAD. Behind the latest target and not yet pushed → stash, `git rebase origin/<target>`, pop; conflicts → `$git-conflict-resolve`. Already pushed → never rebased.
3. **Stage + guard** — `git add -A` minus secrets; `doc-stamp-guard.cjs --staged` unstages stamp-only churn.
4. **Review choice** — ask for a whole-branch fix-loop review or explicit Skip; run the chosen review and record its receipt, or bind the user-approved skip to the exact candidate.
5. **Final evidence** — verify the test and review decisions still cover the final candidate; ask again for choices invalidated by later edits.
6. **Commit** — via `commit` skill, reusing the same-candidate user decisions and review/skip receipt.
7. **Push + PR** — `git push -u origin <branch>`; create PR (not draft) or update it + `gh pr ready`.
8. **CI loop** — wait; failure → evidence → root cause → fix → review → commit → push → wait again, until all green.
9. **Mergeable** — not draft, no conflicts, `mergeStateStatus` clean (or blocked only by human review); report.

**Key Rules:**

- MUST ATTENTION run inline in the main session; NEVER hand the whole task to a sub-agent — why: `workflow-review-changes` owns its convergence loop only in the main session.
- MUST ATTENTION ask the user about tests and review, with Skip options, before executing either gate or publishing. Wait for their answers; broad autonomy wording and auto-trigger preferences never choose an answer.
- MUST ATTENTION commit only a candidate covered by a review receipt or an explicit user-approved skip receipt. NEVER self-approve a skip; report skipped review truthfully.
- MUST ATTENTION review the WHOLE branch: scope is always `<base-ref>...HEAD` ∪ uncommitted (the total diff that will merge into the target), never the latest commit or the current changes alone — why: a defect introduced in an earlier commit of the branch ships in the PR exactly like one in the last commit.
- NEVER merge the PR, enable auto-merge, push to the target branch, force-push, rebase/amend a pushed commit, or run a destructive git command — rebase only commits no remote ref contains (Step 2's never-pushed test); resolve drift on a pushed branch with `git merge --no-commit` + `$git-conflict-resolve`, then review and commit through the `commit` skill.
- A user-approved Skip waives only the selected local test or review gate for the named candidate. NEVER weaken/delete tests or checks, bypass required CI, or describe skipped work as passed.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Pull Request Skill

## Authority

Invocation IS the user's explicit request for every Git/GitHub operation below, scoped to the current repository and the PR branch it selects or creates: `add`, `commit`, `push` of that branch, branch creation and `switch`, `stash push | pop`, `rebase` of that branch's own unpushed commits (Step 2), `gh pr create | edit | ready`. NEVER authorizes merging the PR, enabling auto-merge, pushing to the target branch, force-pushing, rewriting pushed history, or `reset --hard` / `clean -f` / `checkout -- <path>` / `restore <path>` / `stash drop`. Record a git-operation lease for `["add","commit","push"]` per `commit` skill Step 0; revoke it in a `finally` path.

## Execution — main session, explicit test and review choices

- Run every step in the main session. `$workflow-review-changes --fix-loop`, `commit` and `fix` run inline via the skill invocation; their own reviewer sub-agents still fan out per their skills. — why: `workflow-review-changes` MUST run inline in the main session, never as a sub-agent, because it owns its convergence loop there; this session owns the whole task end to end.
- Ask both test and review questions through the [User Choice Contract](#user-choice-contract), even when evidence already exists or local tests are not applicable. Reuse an actual user answer for the unchanged candidate when calling `commit`; do not ask twice for the same choice.
- Finish with one report: PR URL, state, target + branch, review rounds, local test result, CI result, deferred/blocked items.

## Procedure

Write `tmp/reports/pull-request-<date>-<branch>.md` from the first step; append after each step — why: a cut-off run still leaves evidence.

### Step 1 — Resolve target branch

1. Run `git remote` + `gh auth status`. No `gh` → use GitHub MCP tools if present. Neither → branch, commit and push still work, but opening a PR or watching CI does not → stop there, report a Blocker.
2. Find an open PR for the current branch: `gh pr list --head <current-branch> --state open --json number,baseRefName,isDraft,url`.
3. Target = first that applies:
   1. Base branch the user named in the request. Open PR has a different base → retarget: `gh pr edit <n> --base <target>`.
   2. Open PR's `baseRefName` — covers finishing an existing PR.
   3. `pullRequest.targetBranch` in `docs/project-config.json`.
   4. `main`.
4. Run `git fetch --prune origin`. Base ref `R` = `origin/<target>`, falling back to local `<target>` when no remote branch exists. Neither exists → config or request wrong → Blocker. — why: pruning drops the `origin/<branch>` ref of a branch deleted after its merge, which Step 2 reads as "not pushed".

### Step 2 — Choose branch

<!-- REVIEWED FIXES — DO NOT REVERT. Each was reproduced in a throwaway git repo during the "branch PRs fresh" PR review; a framework re-sync had silently re-applied the old text three times.
1. `git switch -c --no-track <name> R` FAILS with "only one reference expected": `-c` consumes the next word as the branch name. Write `git switch --no-track -c <name> R`.
2. Every "merged" test must exclude HEAD == R: a zero-commit branch cut from an up-to-date R satisfies both `--is-ancestor` and the `merge-tree` tree comparison, and would be replaced, dropping the user's branch name.
3. "No `origin/<branch>` ref" does NOT mean never pushed (a branch cut a moment ago, a detached HEAD on a pushed commit, and a branch deleted after its merge all lack one). Test the commits themselves against the remote refs.
4. `--is-ancestor` cannot see squash or rebase merges (they get new SHAs); with no `gh` (Azure DevOps Server remotes) use the `merge-tree` tree comparison.
5. `git rebase --continue` reopens the commit-message editor after a conflict; `git -c core.editor=true …` avoids it in every shell (`GIT_EDITOR=true` is POSIX-only). -->

A PR branch starts at the latest `<target>` (`R` from Step 1.4). Name for a new branch: `<type>/<slug>` — `<type>` = conventional-commit type of the work (`feat`, `fix`, …); `<slug>` = kebab-case, ≤40 chars, from the change's intent; name exists locally or on `origin` → append `-2`, `-3`, ….

1. **Merged already?** Never when `git rev-parse HEAD` equals `git rev-parse R`: that is a branch just cut from `R` (or the target itself, level with `R`), not a merged one → it falls to item 2 and stays — why: `--is-ancestor` is also true for a branch just created at `R`, and replacing it would drop the user's branch name. Otherwise yes when any of these holds:
   - `HEAD` is an ancestor of `R`: `git merge-base --is-ancestor HEAD R` succeeds (also true on a local `<target>` behind `R`, and on a named branch whose commits `R` already contains).
   - Squash or rebase merge, git-only: `git merge-tree --write-tree R HEAD` prints a tree equal to `git rev-parse R^{tree}` (git ≥ 2.38; skip this test when unsupported or when it reports conflicts) — the content is already in `R` under other SHAs, which `--is-ancestor` cannot see.
   - `gh pr list --head <branch> --base <target> --state merged --json number,headRefOid` returns a PR whose `headRefOid` equals HEAD.
   - **Yes** → `git status --short` first: a clean tree means nothing to PR — report and stop, creating no branch. Otherwise `git switch --no-track -c <name> R` (flag order matters: `-c` takes the next word as the branch name). No rebase — nothing on this branch is left to carry over.
   - **Merged PR head is a proper ancestor of HEAD** (work added after the merge; needs `gh` for `headRefOid`) → `git switch -c <name>` from HEAD, then rebase with `--onto R <headRefOid>` only when the replayed commits pass the never-pushed test of item 2; otherwise stay.
2. **Not merged** → on target or HEAD detached: `git switch -c <name>` from HEAD (pending work and local commits ahead of `R` come along; report that local `<target>` still holds them; NEVER reset it). Then judge the branch against `R`:
   - **Up to date** (`git merge-base --is-ancestor R HEAD`) → stay.
   - **Behind `R`, never pushed** → rebase onto `R`. Never pushed = no commit to replay is reachable from a remote ref: `git rev-list --count HEAD ^B --not --remotes` equals `git rev-list --count B..HEAD`, with `B` = `R` (or `headRefOid` on the `--onto` path). — why: a lookup of `origin/<branch>` by name misses a branch cut a moment ago from a pushed commit, and a detached HEAD.
   - **Behind `R`, any commit to replay pushed** → stay, no rebase — it would rewrite pushed commits and need a force-push. Step 7.1 merges `origin/<branch>` and Step 9 merges `R` when GitHub reports the branch behind or conflicting.
3. **Nothing to PR** — decided before any `git switch -c`, and only for a branch that is not merged (item 1 handles a merged one, whose old commits would otherwise count as "ahead"): no commits ahead of `R` + no pending changes → report and stop.

**Moving with pending work.** `git switch` refuses when a local change collides with the destination, and `git rebase` refuses a dirty tree → `git stash push --include-untracked -m "pull-request <branch>"`, switch or rebase, `git stash pop`. A `pop` conflict → `$git-conflict-resolve` (stash-apply); the entry stays in the stash list, so name its ref in the report. NEVER `git stash drop`.

**Rebase.** `git rebase R` (or `--onto` above) on the unpushed branch only. A conflict → `$git-conflict-resolve`, `git add` the resolved paths, `git -c core.editor=true rebase --continue` (keeps the original message without opening an editor in a non-interactive run; works in every shell). A conflict whose intent is unclear → `git rebase --abort`, restore the stash, **Blocker**. Step 4 reviews the rebased branch as a whole, resolved hunks called out — why: replayed commits are new commits made outside the `commit` skill, and only the whole-branch review vouches for them.

### Step 3 — Stage and guard pending changes

1. `git status`, then `git add -A` — the user asked for all staged + unstaged work to be committed. Leave out secret-like files (`.env*`, keys, credential files) via `git restore --staged -- <path>`; list them in the report.
2. `node .claude/hooks/lib/doc-stamp-guard.cjs --staged`. Exit `3` → `git restore --staged -- <paths>` for the stamp-only files; leave them in the working tree. NEVER revert the working tree.
3. **Review candidate target.** Nothing left unstaged → review uses the default `worktree` target (working tree = index). Anything left unstaged → pass `--target=staged` to the fix-loop snapshot; each round `git add`s the paths it fixed before the next snapshot. — why: the receipt binds the exact candidate tree; reviewed content MUST equal committed content.

### Step 3.5 — Ask about local tests

STOP and ask: **Run local tests before publishing, confirm already verified, or skip?** Offer:

1. **Run local tests (Recommended)** — execute the configured delta-scoped commands using the project phase rules and managed runners.
2. **Already verified** — show any existing evidence; the user confirms it covers this candidate. Do not choose this answer yourself.
3. **Skip local tests** — explicit user decision; record `Local tests: skipped by user`.

For documentation-only changes, explain that no local test lane is required and offer **Confirm no tests required** alongside Run and Skip. Wait for the user's answer. Missing commands or a blocked environment are reported as unavailable, never passed; obtain an explicit skip or stop. Test failures require root-cause fixes, then refresh the candidate and invalidate affected evidence. A skip never disables required CI or Ready gates imposed by the project.

### Step 4 — Ask about review of the whole branch

**Review scope invariant.** A pull-request review covers the TOTAL net change of the branch against the target: `git diff <base-ref>...HEAD` (three-dot, from the merge-base, every branch commit) ∪ uncommitted changes. NEVER only the latest commit (`HEAD~1..HEAD`, `git show`), never only the current working-tree changes, and never just the fix made since the last round — a later CI fix or merge is reviewed as part of the whole branch diff. Reviewing an existing PR (no local edits) uses the same scope from the PR's base (`baseRefName`) after `git fetch origin`. Record the scope proof in the report: base ref, merge-base SHA, `git rev-list --count <base-ref>..HEAD` and the changed-file count of `git diff --stat <base-ref>...HEAD`.

STOP and ask: **Review the whole branch before publishing, use an existing review, or skip?** Offer all three `--fix-loop` review choices from `commit` Step 3.6, recommending one using its size/risk selection rule (whole-branch signals), plus **Use existing review** when its evidence covers this full scope, and **Skip review** last. Wait for the user's selection; a PR request is not an answer. A commit-only receipt does not prove the whole branch was reviewed.

For a review selection, run the selected `changes-review`, `why-review` or `workflow-review-changes` fix-loop inline via the skill invocation over the whole scope. For the full workflow, run `$workflow-review-changes --fix-loop` inline via the skill invocation, scope `<base-ref>...HEAD ∪ current uncommitted changes` — the three-dot base is the fixed merge-base, so the review covers every branch commit + pending work, a Step 2 rebase included. Follow that workflow's `references/fix-loop.md` as written: each round re-runs the whole default workflow over the recomputed scope (parallel reviewers, validated fixes at the owning layer, `$docs-manager --mode=update`); converges on a zero-fix round; keeps round cap + severity floor; mints the `workflow-review-changes` receipt.

- **User chooses Skip:** record the whole-branch scope proof and `Review: skipped by user`; this is not a successful review. If a commit is needed, follow `commit` Step 3.6 `snapshot` + `issue --kind=skip` using the exact prepared commit descriptor. Never mint a review receipt for skipped work. With no pending commit, record the explicit branch-scope skip in the PR report; no commit receipt is needed.
- A partial review or self-approved skip NEVER satisfies this gate. An existing full review or skip decision is reused only after the user confirms it for this run and candidate.
- **Integration-merge scope** (uncommitted merge from Step 7.1 or Step 9): review the PR's net change — `git diff <base-ref>` over the working tree, after `git fetch origin <target>` — with conflict-resolved hunks called out. Incoming target-branch commits are NOT review targets: they were reviewed on the target branch. The receipt still binds the whole merge candidate. — why: during an uncommitted merge `HEAD` is the pre-merge commit, so the default `...HEAD ∪ uncommitted` scope would pull every incoming target commit into the review.
- Fix-loop escalates (cap spent with blockers open, blockers not shrinking, blockers increasing, ambiguous intent) → **Blocker**. No commit proceeds without a qualifying receipt or explicit user-approved skip. A failed review is not a skip; ask for any new skip decision instead of inventing one. Then hand back per the Blocker rule in the [User Choice Contract](#user-choice-contract), listing the open findings.

### Step 5 — Verify final evidence and decisions

Check that Step 3.5 test evidence/decision and Step 4 review evidence/decision still cover the final branch scope and exact commit candidate. A review fix, CI fix, merge or other edit invalidates affected evidence and candidate-bound skip decisions: ask again for the affected test/review choice, then run it or record an explicit new skip. Within an authorized review/test fix-loop, its required nested checks remain authorized. Never silently expand a completed choice to a later candidate.

### Step 6 — Commit via `commit` skill

Invoke `commit` over the staged candidate. Every mandatory message part applies: `Estimate:` first body line, purpose → what → how body, Reviewers block, attribution footer. Pass the recorded user test/review answers and the matching review or user-approved skip receipt. These actual same-candidate answers satisfy its interactive gates without a duplicate question; this skill never answers them for the user. A missing answer requires the question; a changed candidate returns to the affected choice. NEVER commit with `--no-verify`; NEVER run a raw `git commit` outside the skill.

### Step 7 — Push and open PR

1. `git push -u origin <branch>`. Rejected because the remote branch moved → `git pull --no-rebase --no-commit origin <branch>` so the merge result stays uncommitted, resolve conflicts via `$git-conflict-resolve`, review it (Step 4, integration-merge scope), commit via Step 6, push again. NEVER force-push — why: a merge commit created outside the `commit` skill skips the receipt-bound review.
2. **No open PR** → `gh pr create --base <target> --head <branch> --title "<conventional title>" --body-file <file>`. No `--draft`.
3. **Open PR** → `gh pr edit <n> --body-file <file>`; draft → `gh pr ready <n>`.
4. **PR body** — what the branch does (purpose → what → how); review evidence (rounds, report path, deferred LOW findings) or `Review: skipped by user`; local test evidence or `Local tests: skipped by user`; per-area Reviewers block; `Fix-Origin:` field when `commit.fixOriginTrailer` is `true`; same attribution footer as the `commit` skill.

### Step 8 — CI loop: wait, fix, repeat until green

1. **Wait:** `gh pr checks <n> --watch --interval 30`. Wait would outlast the host tool timeout → run it in the background or re-run it. NEVER sleep in the foreground past the timeout. Then read the final state: `gh pr checks <n> --json name,state,bucket,link,workflow`.
2. **No checks yet:** checks register late after a push → keep polling up to ~5 minutes. Still none + `gh pr view <n> --json statusCheckRollup` empty → the repository runs no CI on this PR; record `CI: none configured`, go to Step 9.
3. **All `pass` / `skipping`** → Step 9.
4. **Any `fail` / `cancel`** → per failed check:
   1. Read the evidence. GitHub Actions → `gh run view <run-id> --log-failed` (run id in the check `link`). Other providers → the check's link or description.
   2. Test the environment hypothesis before blaming code. Log names an infrastructure cause (runner lost, registry/network timeout, quota) → **one** rerun: `gh run rerun <run-id> --failed`. Second infrastructure failure → Blocker. NEVER rerun to fish for green.
   3. Otherwise `$fix --target=ci`: trace the root cause backward from the failing log, fix at the owning layer — a stale test included, only once adjudicated TEST-WRONG. NEVER skip, delete, or weaken a check or test to get green.
   4. Return to Step 3.5 for the changed candidate. Re-run Step 4 over the WHOLE branch diff again (`<base-ref>...HEAD ∪ uncommitted`, the fix included — never the fix alone; earlier reports are history only), then Step 5, Step 6, push.
5. Loop to step 1. No attempt cap while each attempt removes a failure or changes its cause. **Blocker** when the same failure signature survives 3 attempts addressing different causes, or the fix needs something outside the repository (secret, permission, runner/service setup, product decision).

### Step 9 — Ready to merge

Read `gh pr view <n> --json isDraft,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup`.

| State                                                                                               | Action                                                                                                                                                     |
| --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `isDraft: true`                                                                                     | Run `gh pr ready <n>`.                                                                                                                                     |
| `mergeable: CONFLICTING`, or `mergeStateStatus: DIRTY` / `BEHIND` (base requires up-to-date branches) | Run `git merge --no-ff --no-commit origin/<target>` (no rebase). Resolve conflicts with `$git-conflict-resolve`, review the uncommitted result (Step 4, integration-merge scope), commit via Step 6, push, then repeat Step 8. |
| `mergeStateStatus: BLOCKED` with no human-review cause | Run `gh pr checks <n> --required`. Required check pending or not yet reported → back to Step 8 and wait; still missing after the Step 8.2 grace period → Blocker naming the check. Other branch rule → Blocker naming it. |
| `mergeStateStatus: UNSTABLE` | A non-required check is failing → Step 8.4 (every check must pass). |
| `mergeable: UNKNOWN`                                                                                | GitHub is still computing it. Read the state again after a short wait.                                                                                     |
| `reviewDecision: REVIEW_REQUIRED` / `CHANGES_REQUESTED`                                             | Only a human can clear this. Report it as outstanding, not as a failure of this run.                                                                       |

**Done** = not draft · `mergeable: MERGEABLE` · `mergeStateStatus` `CLEAN` or `HAS_HOOKS` — or `BLOCKED` solely by a `reviewDecision` of `REVIEW_REQUIRED` / `CHANGES_REQUESTED` — · every check `pass`/`skipping` (or `CI: none configured`) · full-scope review receipt or explicit user-approved review skip · local tests green, user-confirmed not applicable, or explicitly skipped. Report skips prominently; they do not mean passed. NEVER merge — stop at ready.

## User Choice Contract

Both `commit` and `pull-request` ask the user about tests and review, including explicit Skip options, independently of `portability.skillAutoTrigger`, workflow routing mode or a general request to finish autonomously. Do not auto-answer, infer consent from silence, select a default without an answer, or treat evidence alone as the user's choice. A prior explicit answer for this exact candidate in the current run may be reused when calling `commit`.

- **Tests:** Run, user-confirmed Already verified, or user-approved Skip; documentation-only candidates also offer Confirm no tests required.
- **Review:** all three fix-loop reviews from `commit` Step 3.6, existing full-scope review when available, or user-approved Skip. Recommend one review; never recommend Skip.
- **Receipt:** an exact commit-candidate review/skip receipt remains mandatory when committing changed content. Only the user can authorize minting a skip receipt.
- **Later changes:** refresh scope and ask again for every invalidated choice. Preserve answers, evidence, scope and pending questions across compaction/resume and in delegated briefs.
- **Other questions:** honor the called skill's own gates; this contract does not waive them.
- **CI:** a local test/review skip does not waive required checks, human approval or project Ready rules.

A **Blocker** ends the run. Pending user choices pause only dependent steps. If blocked, list evidence and options; keep/create a draft PR only when pushed commits and project authority permit it. Otherwise report with pending work uncommitted. Never fabricate a receipt or push unreviewed content without an explicit user-approved skip.

## Related

- `commit` — the only commit path; its Push & PR section routes pull-request requests here.
- `workflow-review-changes` — the `--fix-loop` review run over the whole branch.
- `fix` — `--target=ci` diagnoses and fixes CI failures.
- `git-conflict-resolve` — resolves merge conflicts with the target branch.

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — one per procedure step, plus a final review task.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `environment-fault-hypothesis` — Weigh the environment as a competing cause, with a named discriminator; judging a bug report, failing test, error or unexpected output → .claude/skills/shared/protocols/environment-fault-hypothesis.md
- `root-cause-debugging` — Systematic root-cause debugging, never guess-and-check; debugging a failure → .claude/skills/shared/protocols/root-cause-debugging.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:environment-fault-hypothesis:reminder -->

**MUST ATTENTION** environment-fault gate: a bug, failed test, error, or odd output is NOT proof of a code defect. Sweep environment preconditions (versions, deps/install state, config & env vars, services, ports/network/clock, permissions, leftover state) and resource/transience suspects (RAM, CPU, disk, handles, network, timeouts) as a competing hypothesis, cite the discriminator you ran, and fix an environment cause in the environment — never by editing code or weakening a test. "Flaky" is a symptom, not a verdict.

<!-- /SYNC:environment-fault-hypothesis:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Drive current work to a pull request **ready to merge** — not draft, whole-branch review and local tests run or explicitly skipped by the user, every CI check green — with test and review choices before publishing.

- **MUST ATTENTION — MAIN STEPS IN ORDER:** (1) target: request → open PR base → `pullRequest.targetBranch` → `main` · (2) branch: merged → new branch at latest target; unpushed + behind → rebase (stash, `$git-conflict-resolve`); pushed → never rebased · (3) stage + guard · (3.5) test choice · (4) whole-branch review choice · (5) verify final evidence · (6) `commit` skill · (7) push + create/ready PR · (8) CI loop until green · (9) mergeable check + report.
- **MUST ATTENTION — ASK TESTS AND REVIEW:** run inline, STOP for both user choices including Skip, and wait. Auto-trigger restrictions never suppress these questions or block the selected review and its required dependencies.
- **MUST ATTENTION — REVIEW BEFORE COMMIT:** the receipt binds the exact candidate. Every later edit, CI fix included, refreshes the user choices and requires a matching review or explicitly approved skip before commit. NEVER self-approve a skip.
- **MUST ATTENTION — REVIEW THE TOTAL BRANCH DIFF:** every review round in a PR run covers `<base-ref>...HEAD ∪ uncommitted` (all branch commits against the merge-base), never only the latest commit or the working tree.
- **MUST ATTENTION — CI FIXES:** root cause first, environment hypothesis included; one rerun only for a named infrastructure cause. NEVER weaken, skip or delete a test or check.
- **NEVER** merge, enable auto-merge, push to the target branch, force-push, rewrite pushed history, or run a destructive git command — stop at ready to merge.
- **Blocker** = listed blockers + report (+ draft PR only when pushed commits and PR tooling exist); user test/review questions also pause the run. NEVER commit unreviewed work without an explicit user-approved skip.
- **MUST ATTENTION** create one task per procedure step plus a final review task before starting.

**Anti-Rationalization:**

| Evasion                                                | Rebuttal                                                                                                                          |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| "Hand the whole task to a sub-agent"                   | The procedure runs in the main session. `workflow-review-changes` must run inline there, and a sub-agent cannot own its loop.     |
| "The user will want to confirm the branch name"        | Derive the branch name and report it; test and review choices still require the user's answers.                                                     |
| "Rebase the pushed branch too, then force-push"        | Rebase rewrites pushed history and needs a force-push, which is never authorized. Merge `origin/<branch>` (Step 7.1) or `R` (Step 9) in instead.       |
| "Only the new changes need review"                     | The first review covers `<target>...HEAD` ∪ uncommitted: the whole branch. CI-fix rounds re-review the whole branch too — the fix is part of it.       |
| "CI is red because of a flaky test, rerun until green" | One rerun, and only for a named infrastructure cause. Anything else is investigated and fixed at its root.                        |
| "Mark the failing test skipped so the PR goes green"   | That forces green. Adjudicate the test, then fix the source or the stale test.                                                    |
| "Checks passed, merge it"                              | The target is ready to merge, not merged. Never merge.                                                                            |
| "Commit first, review later"                           | The commit gate needs a review receipt or user-approved skip for the exact candidate. Ask first; commit only that candidate. |
