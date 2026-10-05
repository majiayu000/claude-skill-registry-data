---
name: codex-improvement-loop
description: Use when a broad codebase improvement, UI/UX revamp, release hardening pass, multi-PR cleanup, or "boil the ocean" request needs decomposition, worker/reviewer coordination, PR sequencing, and visible loop state.
---

# Codex Improvement Loop

Use this skill when a request is too broad for one clean diff or when multiple agent workers/reviewers would reduce risk. This is not an automation framework. It is an operating pattern for keeping large agentic coding work understandable, reviewable, and honest.

## Plain-English Contract

Before starting, tell the user what this does in non-technical terms:

- It turns one big messy project into smaller reviewable chunks.
- One orchestrator keeps the plan and decides what runs next.
- Worker threads make changes.
- Reviewer threads inspect changes and call out problems.
- The loop repeats until each chunk is approved, tested, or blocked.
- It does not make the model smarter by itself. It improves coordination and reduces missed issues.

Do not interrupt or redirect an already-running agent thread unless the user explicitly asks. If a related run is already underway, use this skill only to create a checkpoint overlay: snapshot current state, identify missing gates, and suggest the next safe step.

## When To Use

Use for:

- full-product UI/UX revamps
- multi-platform parity work across web, mobile, and desktop
- release hardening with tests, screenshots, and deploy checks
- architecture cleanup that should be split into multiple PRs
- auth, billing, security, migration, analytics, or data-model work with high blast radius
- any task where "do everything" would produce an unreadable diff

Do not use for:

- one-file fixes
- short writing/admin work
- simple debugging with one likely root cause
- any task where orchestration overhead is bigger than the work

## Operating Rules

- Preserve dirty work. Check `git status` before edits and never revert unrelated changes.
- If the worktree is dirty, classify changes before editing:
  - unrelated files: leave them alone
  - same files needed for this node: inspect them first and work with them
  - unclear ownership or risky overlap: pause and ask the user before editing
- Do not use `git stash`, `git checkout --`, or `git reset` as a default dirty-work cleanup path.
- Prefer one integration branch for the initiative, then focused worker branches or worktrees.
- Prefer sequential PRs unless parallel work clearly touches separate modules and contracts.
- Allow parallel workers only when their nodes have no unmet dependencies and their likely file paths do not share a close module boundary, data contract, migration, generated artifact, or test fixture.
- Keep every worker scoped. If a worker finds extra work, it reports a proposed new node instead of expanding its diff.
- Keep reviewers read-only. Reviewers should not implement fixes.
- Do not merge to the final target branch unless the user explicitly asked for that.
- Run real verification before claiming readiness: tests, screenshots, app smoke checks, deploy status, PR status, or an explicit statement of what could not be verified.
- If a required domain skill is missing on a high-risk path, state the missing skill, name the fallback, assign risk level, and pause unless the fallback is clearly equivalent.

## Workflow

1. Define the initiative.
   - Name the goal in one sentence.
   - State the target repo, target branch, constraints, and non-goals.
   - Ask for confirmation only if merge/deploy/send/release actions are unclear or risky.

2. Snapshot reality.
   - Read repo instructions, current context, and relevant skills.
   - Run `git status --short`.
   - Identify current branch, dirty files, active PRs, active threads, and known blockers.
   - If a related run is already active, do not restart it. Build a checkpoint plan around its current state.
   - Choose exactly one loop state owner. Default owner is the orchestrator thread. Workers and reviewers report status back; they do not edit the state file unless explicitly assigned.

3. Build a small PR graph.
   - Split work into focused nodes with `id`, `title`, `scope`, `depends_on`, `branch`, `status`, `acceptance`, and `tests`.
   - Mark each node as `sequential`, `parallel`, or `stacked`.
   - Default parallelism cap: 2 active workers.
   - Keep UI/UX nodes aligned by user workflow, not by random component folders.

4. Start or guide workers.
   - Use thread/worktree tools when the user wants separate agent threads.
   - Otherwise, use same-session subtasks and keep the state table visible.
   - Every worker gets only its local work packet: goal, files, constraints, acceptance, tests, and immediate predecessor context.
   - Every worker must run a git preflight before edits if it will publish a branch.

5. Review each node.
   - Use reviewer threads or review stance after each meaningful diff.
   - Findings must lead, ordered by severity, with file/line references.
   - Missing tests and truth gaps count as real review findings.

6. Loop on fixes.
   - Send only unresolved blocking comments and current CI/test failures back to the owning worker.
   - Require fixes on the same branch/diff unless the graph changes.
   - If the same blocker repeats three times, mark it blocked and ask the user instead of forcing progress.

7. Merge or close.
   - Merge only when authorization is explicit and current. Restate the exact branch/PR/base before merging.
   - If local-only was requested, do not push or merge remotely.
   - End with changed/merged nodes, verification performed, remaining risks, and the next human decision.

## State

For short runs, keep state in the thread. For long runs, create or update a loop state file in one of these places:

- repo-local: `docs/workplans/<initiative-slug>.md`
- workspace-local: `work/<initiative-slug>-loop-state.md`
- durable team docs, only when appropriate: `docs/active-agent-loops/<initiative-slug>.md`

Only the orchestrator owns the state file by default. Parallel workers and reviewers should return structured updates to the orchestrator instead of editing the file directly.

Use the compact template in `references/loop-state-template.md`.

## Worker Packet

Use the template in `references/worker-packet.md` when creating a worker or subtask. Trim it aggressively so the worker gets enough context without inheriting the whole initiative.

## Reviewer Packet

Use the template in `references/reviewer-packet.md` when creating a reviewer or doing a formal review pass.

