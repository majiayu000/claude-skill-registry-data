---
name: plantask
description: Plan a feature or bug fix and break it into well-formed, non-mixing Linear tasks — one parent issue per feature with ordered, dependency-linked sub-issues, each with a detailed plan, acceptance criteria, labels, and a branch name — ready for a coding agent to execute. Use when the user runs /plantask, or asks to plan and create Linear issues/tasks for a feature, bug, or piece of work.
---

# plantask — turn an idea into executor-ready Linear tasks

You are the **planner**. You do NOT write code here. You read the codebase + Linear, decompose
the idea into tasks, get the user's approval, then create the tasks in Linear so an executor
(a coding agent) can pick them up cleanly — without ever mixing one feature's tasks with another's.

Run as `/plantask <idea>` (a feature, a bug, or any piece of work). One run = ONE feature/unit.

## Core model (read this first)

- **Linear Project = an existing real project/initiative. Never create a project per feature.**
- **Feature = one parent issue.** Its tasks = **sub-issues** of that parent.
- Two features on the same project → two parent issues, each with its own sub-issues → they never mix.
- Every task also carries a `feat:<slug>` label and a branch under `feat/<slug>/` for a second and third layer of isolation (filtering + git/PR).

## Pipeline

### 1. Observe (no writes yet)
- **Read the codebase** relevant to the idea (the modules/files it will touch). Plan against reality, not assumptions. If the idea is vague, ask 1-2 clarifying questions before decomposing (don't guess).
- **Read Linear**: `list_teams`, `list_projects`, `list_issue_labels`, `list_issue_statuses` for the target team.
- **Pick the target project**: infer from the repo (git remote / folder name matching a Linear project). If it's ambiguous or nothing matches, **ask the user which team/project** — never guess the destination.
- Derive a short **feature slug** from the idea (kebab-case, e.g. `checkout-revamp`).

### 2. Decompose
- Break the feature into **3-7 tasks** (fewer is better). Each task is one bounded, separately-verifiable unit.
- For EACH task, write the project's task template:
  - **Problem** — what & why (concrete)
  - **Plan** — the steps for that task
  - **Done** — a checkable condition
  - **Verification** — exact commands (build/test/lint, from the project's CLAUDE.md/AGENTS.md)
- Decide **ordering & dependencies**: which task must finish before another (blocks / blocked-by). Number them `[slug N/M]`.
- Flag **independence**: mark which tasks touch disjoint files (parallel-safe) vs which touch shared files (must be sequential). Two parallel-safe tasks must NOT edit the same file.
- Choose **labels** for each task, reusing existing Linear labels where possible:
  - a **type** label (feature / bug / improvement),
  - an **area** label (the module/domain),
  - the **`feat:<slug>`** label (create it if missing — flag this in the plan),
  - the **executor routing label = the repo's name** (e.g. `admagica-agents`), on EVERY task. Cyrus routes an issue to a repo by matching this against that repo's `routingLabels` in `~/.cyrus/config.json` (default = repo name). Without it Cyrus can't tell which repo and stops to ask ("repository selection elicitation") instead of starting. Create the label in Linear if missing.
  - *(optional, only if a routing rule is configured)* a `route:<tool>` label for which executor should run it.
- Choose a **branch name** per task: `feat/<slug>/NN-short-title`.

### 3. Present the plan — STOP for approval
Show the user the complete plan BEFORE writing anything to Linear:
- target team/project, feature slug, parent-issue title;
- the ordered task list with: number, title, one-line goal, Done, labels, deps (what blocks what), independence flag, branch name;
- any new labels you'll create.
**Wait for explicit approval.** State clearly that approving authorizes BOTH creating the issues AND dispatching them to the executor (Cyrus) so coding starts automatically — the user is approving execution, not just issue creation. Creating Linear issues + triggering an autonomous agent are external mutations — do not proceed until the user says go. If they want **plan-only** (create issues but NOT auto-execute), honor that and skip step 5's dispatch. If they adjust scope, revise and re-show.

### 4. Create in Linear (only after approval)
- **Idempotency check first**: if issues with this `feat:<slug>` label already exist, do NOT duplicate — report what exists and ask whether to add/update instead.
- Create the **parent issue** (the feature) in the chosen project: title = feature name, description = overview + the task list + acceptance for the feature as a whole.
- Create each **task as a sub-issue** of that parent (`parentId`), in the same project, with: full task-template description, labels, status `Backlog`/`Todo`.
- Set **dependencies** with the native `blockedBy` / `blocks` params on `save_issue` (confirmed supported) — e.g. the test task `blockedBy: [task1, task2]`. These are real Linear relations, not description text — don't duplicate them as a `Blocked by:` line in the description.
- **Branch / PR linking — each sub-PR closes its OWN sub-issue, never the parent.** The executor's auto-generated branch (`cyrus/adm-NN-...`) already links the PR to *that* sub-issue and moves it to Done on merge (verified — Linear's GitHub integration does this by branch name). So each task's PR should reference its own issue, e.g. `Closes ADM-NN` for that task. **Do NOT put `Closes <parent-id>` in a sub-task PR** — that closes the whole feature parent on the first merge. Let the parent close when all sub-issues are Done (enable Linear's "complete parent when all sub-issues complete"), or have ONLY the final task's PR add `Closes <parent-id>`. Feature isolation comes from `parentId` + the `feat:<slug>` label, not the branch prefix.
- Keep titles prefixed `[slug N/M]` so order is obvious everywhere.

### 4b. Register the repo with the executor (auto — covers /plantask AND manual issues)
The executor (Cyrus) only acts on repos registered in its config, and uses that as the project→repo map — so this registration serves **both** `/plantask`-created issues and ones you create by hand in Linear later.
- Get the remote of the repo you're planning in: `git remote get-url origin`.
- Check if it's already registered: `grep -q "<repo-name>" ~/.cyrus/config.json 2>/dev/null`. If yes, skip (idempotent).
- If not, register + clone it once: `cyrus self-add-repo "<remote-url>" "<linear-workspace>"`. Cyrus clones into `~/.cyrus/repos` (isolated from your working tree) and maps it to the workspace/project.
- Result: a brand-new project's **first** `/plantask` auto-registers its repo; from then on every issue in that Linear project — planned or manual — routes to it with no manual cloning.
- If `cyrus` is not installed/found, note it and continue (don't fail the plan) — the user can register later per `EXECUTOR.md`.

**Give the new repo its `.env` (do this on first registration — most projects need it).** A fresh Cyrus clone has no `.env` (gitignored), so any task that builds/tests/calls a real API will fail without it. Cyrus loads `<worktree>/.env` into the agent's session env automatically (`ClaudeRunner.loadRepositoryEnv`), and copies any file listed in `.worktreeinclude` into each new worktree (`GitService.copyIgnoredFiles`). So, per-repo, isolated, no global collisions:
  - **Ask the user for the project's `.env`** (path, or have them drop it). NEVER read its values into the conversation.
  - Run the **one atomic helper** — it copies the `.env` into the clone, chmods it, adds `.env` to `.worktreeinclude`, AND verifies all three (so it can't be done half-way, the bug that bit us before): `~/loop-config/bin/cyrus-repo-env.sh <repo-name> <path-to-project-.env>`. It prints `OK:` only when worktrees will actually receive the env; treat anything else as a hard stop. Idempotent — safe to re-run. Do NOT hand-do the `cp`/`.worktreeinclude` steps separately.
  - Idempotency: if `~/.cyrus/repos/<repo>/.env` already exists, ask before overwriting (the helper overwrites).
  - If a task needs per-worktree deps (e.g. `npm ci`) or generated files, that goes in a committed `cyrus-setup.sh` at the repo root (runs after worktree creation) — flag it, don't build it blindly.

**Install auto-Done-on-merge (so the dependency chain advances without a manual Done step).** Linear's GitHub integration can't be connected programmatically (needs a browser OAuth + GitHub org admin), and without it a merged PR leaves its issue stuck (not Done), so `blockedBy` dependents never resume. Fix per repo: `~/loop-config/bin/cyrus-repo-linear-done.sh <repo-name>` commits a repo-local GitHub Action (`.github/workflows/linear-done-on-merge.yml`) that moves the linked issue to Done on PR merge — works for any org. One-time user activation (flag it, don't do it silently): add the `LINEAR_API_KEY` repo secret + push/merge the workflow branch. Then merge → issue Done → Cyrus re-checks parked dependents on the Done webhook → the next task can start without a manual re-trigger.

**Apply the SAFETY guard (every newly-registered repo — non-negotiable).** Because the agent now gets the repo's real env (incl. live DB/secrets), it must NEVER be able to delete data or do destructive/irreversible things. Run `~/loop-config/bin/cyrus-repo-guard.sh <repo-name>` once per repo: it sets a strong `appendInstruction` (no migrations against a live DB — offline `prisma migrate diff` only, human applies; no DELETE/DROP/TRUNCATE, no `rm -rf`, no force-push, no deploys/payments/secret edits — stop and ask instead) AND a hard SDK `disallowedTools` denylist for the obvious destructive commands. Idempotent; Cyrus hot-reloads. Behavioral layer + hard backstop = the agent's deliverable stays "a PR a human reviews," never a destructive act.

### 5. Dispatch to the executor + report
- **Pre-dispatch verify gate.** Before delegating, for EACH repo the batch routes to, confirm onboarding is complete: the repo is registered in `~/.cyrus/config.json` with a matching routing label, AND (if it needs env) `cyrus-repo-env.sh` printed `OK` for it. A quick re-check: `grep -qxF .env ~/.cyrus/repos/<repo>/.worktreeinclude && ls ~/.cyrus/repos/<repo>/.env`. If a repo isn't fully onboarded, do NOT dispatch its tasks — finish onboarding first (a half-onboarded repo silently produces env-less worktrees → failed builds/migrations).
- **Auto-dispatch (this is the point of plantask).** Once ALL issues are created and the plan was approved (step 3), assign/delegate the **whole batch** to the executor agent — `save_issue(id, delegate: "Cyrus")` (or assignee = the Cyrus agent) for each task. This is the trigger: Cyrus picks them up and **starts coding automatically**.
  - Do this as the **FINAL step, after every issue exists** — never dispatch mid-creation (that would start task 1 before task 2 is planned, breaking "wait until all planned").
  - Assign **all** of them — at dispatch Cyrus starts only the currently-**unblocked** tasks (`blockedBy` holds the rest). (Respect any concurrency cap configured in Cyrus.)
  - ⚠️ **Blocked tasks do NOT auto-start when their blockers later reach Done** (verified: Cyrus is webhook-driven, not dependency-watching). So after the human merges a blocker's PR, the now-unblocked dependent needs a **re-trigger**: it must carry the routing label, then nudge it (reply the repo URL in its agent-session thread, or re-delegate). Tell the user this in the report so the dependent task isn't silently stranded. *(Open question: whether a task that was cleanly label-routed at creation — never elicited — auto-resumes on unblock is still unverified; confirm on the next clean run, and if it doesn't, this manual re-trigger stands.)*
  - **Plan-only mode:** if the user chose plan-only in step 3, SKIP dispatch — leave issues in Backlog, unassigned.
- **Report** the created parent + sub-issues with links, the order, the parallel-safe set, and confirm they've been dispatched to Cyrus (or left in Backlog if plan-only).
- Progress convention: the executor `save_comment`s on each task as it works. The PR auto-links to that task's own sub-issue via the `cyrus/adm-NN-...` branch and moves it to Done on merge (no magic-word needed for the sub-issue; if you add one, use the task's OWN id, never the parent's — see step 4). The human gate is the PR review/merge.

## Multiple features
Run `/plantask` once per feature. Each run creates its own parent issue + `feat:<slug>`. NEVER place two different features' tasks under one parent or share a slug. Three features on one project = three parents, three slugs, three branch namespaces — zero mixing.

## Guardrails
- **No code.** plantask only plans and creates issues. Execution is a separate step/agent.
- **Approval before any Linear write** (step 3). Idempotent on re-run (step 4).
- **Lean**: compose `writing-plans` / `brainstorming` for the decomposition; use the Linear MCP for writes. Don't build new machinery.
- **Ground in reality**: read the code and the project's CLAUDE.md/AGENTS.md so each task's Verification uses that project's real commands (e.g. some services have no `lint`).

## Linear tools (typical)
`list_teams`, `list_projects`, `list_issue_labels`, `list_issue_statuses`, `create_issue_label`,
`save_issue` (create/update: title, description, teamId, projectId, parentId, labels, state, gitBranchName, links),
`save_comment`. Confirm exact parameter names/relations support at runtime before relying on them.
