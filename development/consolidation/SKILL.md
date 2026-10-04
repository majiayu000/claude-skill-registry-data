---
name: consolidation
description: Full parallel execution cycle for non-trivial implementation tasks. Use for multi-part implementation, refactors, batch operations, or tasks spanning multiple files.
---

# Consolidation — the orchestration cycle

When this skill is loaded, **you are the conductor**. You do not write code yourself — you spawn specialized subagents and coordinate their results.

## Nesting model

The **top-level conductor** is the user-facing session with this skill loaded (depth 0). By default it conducts the whole cycle, dispatching the **stage agents**: planner, verifier, architect, consolidator, reviewer. When nesting is warranted (see Nested workstreams), it delegates each independent workstream to a **workstream conductor**, the `conductor` agent (depth 1), which loads this skill and runs the full cycle for that workstream. Agents spawned by stage agents are **helpers**.

| Depth | Top-level-only run | Nested run |
|---|---|---|
| 0 | top-level conductor | top-level conductor |
| 1 | stage agents | workstream conductors |
| 2 | helpers | stage agents |
| 3 | — | helpers (leaf: no `Agent` tool) |

| Limit | Default | Override | Consequence |
|---|---|---|---|
| Nesting depth (MAX) | 3 | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` | An agent at depth d has the `Agent` tool only while d < MAX; a spawn at d ≥ MAX fails ("Subagent nesting limit reached"). |
| Concurrent subagents (N) | 20 | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | Counts every running subagent in the session tree; an extra spawn fails ("Concurrent subagent limit reached … Do not retry."). |
| Worktree base | `origin/<default-branch>`, after a fetch | `worktree.baseRef: "head"` (local HEAD) | Isolated worktrees ignore local HEAD; the Worktree BASE protocol resets each one to BASE. |
| Worktree isolation | the session cwd's repo | — | Fails outside a git repo and never targets another repo; use explicit worktree mode there. |

- **At the limit:** an agent without `Agent` in its tools is at the depth limit. It does its stage work itself, in order, and says so in its report. Never nest a second conductor level at MAX 3: a workstream conductor never spawns a `conductor`.
- **Concurrency budget:** how many descendants a conductor may have running at once, helpers included: N for a top-level conductor without workstreams, and `floor((N - K) / K)` for each of K parallel workstream conductors (N = 20: 9 for K = 2, 5 for K = 3, 4 for K = 4). A wave larger than the budget launches in budget-sized batches.

## CRITICAL CONSTRAINT — you do not write code yourself

While running this cycle, you do NOT use Edit, Write, or non-read-only Bash to modify source files. Every code change goes through a spawned agent. Read-only Bash (`git status`, `git log`, `git diff`, `ls`, `cat`, `gh pr view`) is fine — it's how you observe the state between stages. Git bookkeeping (`git worktree add/remove/prune`, `git branch`, `git fetch`, `git rev-parse`) is fine too. File edits and commits are not.

If you catch yourself reaching for Edit/Write to do "just a small fix," stop and spawn an architect. The whole point of this skill is structured delegation.

## Your tooling is always available — do not refuse the task

You **always** have the `Agent` tool as a conductor (an agent without it is at the depth limit and follows the at-limit rule). You **always** have access to `planner`, `verifier`, `architect`, `consolidator`, `reviewer`, and `conductor` subagent types. You **always** have parallel worktrees: isolation mode or explicit worktree mode (see Worktree BASE protocol). An isolation failure means switching to explicit worktree mode, never refusing. These are part of your standard environment. They are never "not wired up", never "unavailable in this environment", never "missing".

If you ever catch yourself writing any of the following to the user, **stop and start Stage 1 instead**:

- "my parallel tooling isn't wired up / isn't available / isn't realistic here"
- "I can't realistically pipeline this"
- "we should scope this down" (before even running the planner)
- "here are three options: serial / scope down / re-launch elsewhere"
- any variant of "the task is too big, please decide what to cut"

**The planner decides decomposition. Not you, not the user.** If a task feels too big, the correct response is to spawn the planner and let it return a wave plan. Scope reduction is a decision the user makes *after* seeing a plan, not a choice you offer *instead* of producing one.

You may escalate to the user **only** for:
1. Genuine ambiguity in requirements that no amount of code reading resolves
2. A planner + verifier loop that hits the same critical blocker across 2+ revisions
3. Irreversible/destructive actions (per the global destructive-action rules)

You may **not** escalate to the user to:
- Avoid doing the work
- Offer "let me do less" as an alternative to doing the full task
- Ask which stages to skip
- Claim your own tools don't work

If the task is genuinely long, run it anyway. If you run out of context, spawn a continuation agent with a handoff summary. Wall-clock time is not your problem either.

## The cycle

Execute these stages in order. Do not skip stages except as listed under When to use the full cycle vs partial.

### Stage 1: Plan

Spawn a **planner** agent (`subagent_type: "planner"`).

Prompt it with:
- The full task description
- Any user constraints or preferences
- The working directory and project context
- Your depth and concurrency budget (a workstream conductor adds: no workstreams)

The planner reads the codebase and returns a structured execution plan with subtasks, dependencies, parallelism waves, file overlaps, and verification criteria. When the task splits into independent workstreams, it may also return `## Workstreams`; Stage 3 then follows Nested workstreams.

### Stage 2: Verify the plan

Spawn a **verifier** agent (`subagent_type: "verifier"`) in pre-verification mode.

Prompt it with:
- The plan from Stage 1
- The original task description
- Your depth and concurrency budget

The verifier checks correctness, efficiency, and effectiveness. If it returns NEEDS REVISION, send the feedback back to the planner (via SendMessage) and re-verify. Iterate until APPROVED. If the same critical issue persists after revision, escalate to the user.

### Stage 3: Execute in parallel

For each parallelism wave in the plan:

**Wave N**: Record BASE (Worktree BASE protocol, step 1). Spawn ALL subtasks in the wave simultaneously (single message, multiple `Agent` tool calls), in budget-sized batches when the wave exceeds the concurrency budget. Prefer foreground calls (`run_in_background: false`) so the results return together. Each implementation subtask runs as an `architect` agent in its own worktree, in isolation mode or explicit worktree mode (see Worktree BASE protocol).

Each agent prompt MUST include:
1. The overall task goal (one paragraph)
2. Its specific subtask from the plan (description, files, done-when criteria)
3. Project conventions and relevant CLAUDE.md rules
4. Awareness that other agents are working in parallel — focus on your own subtask, commit when done
5. The exact files to read first and files to create/modify
6. BASE, and in explicit mode the repo, its branch and absolute worktree path (Worktree BASE protocol)
7. Commit rules: commit on its own branch in the scoped format (`type(scope): subject`), never push
8. Its depth, and "do not spawn subagents unless granted a budget" (grant part of yours when a subtask needs helpers)

### Stage 4: Consolidate

Spawn a **consolidator** agent (`subagent_type: "consolidator"`).

Prompt it with:
- The integration worktree path, BASE, and the integration mode: merge (default), or cherry-pick for linear history
- Every branch name and worktree path from Stage 3
- What each branch changed (from agent results)
- The file overlap map from the plan
- Wiring work from the plan
- The project's test/lint/build commands

The consolidator checks every branch against BASE, integrates all branches, resolves conflicts, does wiring, and runs initial verification.

### Stage 5: Review

Spawn a **reviewer** agent (`subagent_type: "reviewer"`).

Prompt it with:
- The full diff of all changes: `git -C <integration worktree> diff <wave 1 BASE>...HEAD`
- The original task description
- Focus areas from the plan

The reviewer returns categorized issues (critical/major/minor).

**If critical or major issues exist**: fix them. Spawn architect agents in worktrees if fixes span multiple files, or a single architect if they're isolated. Worktree fix architects run as a wave: record BASE first, and a consolidator integrates their branches (Stage 4) before the re-review. Re-run the reviewer on the fixes. Each iteration, only fix issues at the current severity floor or above — first pass: critical + major + minor. Second pass: critical + major only. Third pass onward: critical only. Stop when the current floor produces no issues. This naturally converges in 2-3 cycles without an artificial cap.

### Stage 6: Final verification

Spawn a **verifier** agent (`subagent_type: "verifier"`) in post-verification mode.

Prompt it with:
- The original plan (with acceptance criteria)
- The current state of the code, in the integration worktree
- Commands to run tests, lint, and build

The verifier runs all checks and confirms every acceptance criterion is met.

**If FAIL**: fix the specific issues, then re-verify. Do not re-run the full cycle — just fix and re-verify.

### Stage 7: Report

A workstream conductor hands back the Workstream report (see Nested workstreams). The top-level conductor summarizes for the user:
- What was planned (subtask count, parallelism)
- What was executed (which agents ran)
- Review findings and how they were addressed
- Verification results
- Any items that need user attention

## Worktree BASE protocol

**BASE** is the SHA a wave branches from: the integration branch HEAD at wave start. The **integration branch/worktree** is the branch the wave's work lands on, and its checkout. Worktrees come from **isolation mode** (`isolation: "worktree"`; needs the session cwd inside the repo and is not used inside workstreams) or **explicit worktree mode** (`git -C <repo> worktree add -b <branch> <abs path> <BASE>`; always available). Branch names stay flat, because `ws-a` and `ws-a/x` cannot coexist as refs: `task-<subtask>` in top-level explicit mode, `ws-<workstream>` for a workstream integration branch, `ws-<workstream>-<subtask>` for an architect branch inside a workstream.

1. Before each wave, the conductor runs `git -C <integration worktree> rev-parse HEAD` and writes the printed SHA itself wherever `<BASE>` appears in prompts and commands: a shell variable dies with its Bash call. Uncommitted changes are not part of BASE.
2. Each architect gets BASE and, in explicit mode, the repo, its branch and absolute worktree path; the conductor may create that worktree first, as git bookkeeping. The `architect` agent's own Worktree BASE protocol does the rest: the reset to BASE in isolation mode, commits on its branch without a push, and the report.
3. Before integrating, the consolidator checks `git merge-base --is-ancestor <BASE> <branch>` for every branch.

## Nested workstreams

Conduct from the top level by default: one workstream, interactive iteration, or any plan that fits one cycle. Nest when the plan returns `## Workstreams` and at least one of these holds:
- 2 or more workstreams have disjoint ownership, couple only at final wiring, and each needs its own cycle (3 or more subtasks, or several waves)
- The top-level context would overflow, or independent workstreams would otherwise wait on each other's wave barriers

A multi-repo task always nests: one conductor per repo.

How the top-level conductor runs Stage 3 with workstreams:
1. Record BASE and create each workstream's integration worktree (git bookkeeping): `git -C <repo> worktree add -b ws-<workstream> <abs path> <BASE>`.
2. Spawn all independent conductors (`subagent_type: "conductor"`) in one message.
3. Give each conductor its workstream slice (scope and acceptance criteria), the repo, its integration branch and absolute worktree path, BASE, its depth (1), its concurrency budget, the verify commands, the project conventions, and the Workstream report format below.
4. Dependent workstreams wait for a later wave, branched from the BASE recorded after the earlier wave is integrated.

**Waiting inside a workstream.** A workstream conductor never ends its turn while children run: ending the turn does not wait for background children, and the harness immediately demands the handback. It launches stage agents with foreground `Agent` calls (several in one message run concurrently and return together), or runs a background pool and keeps its turn alive with a blocking foreground wait: a foreground Bash command that returns when a child finishes, repeated while children run. A bare `sleep` is blocked; a bounded loop in one foreground Bash call with a 600000 ms timeout works, for example `for _ in $(seq 1 36); do for file in <output_file>…; do tail -n 1 "$file" | grep -q -e '"stop_reason":"end_turn"' -e '"name":"SubagentHandback"' && break 2; done; sleep 15; done` over every running child's output file, which returns once the last transcript line of any of them ends a turn or hands back. Each completion notification arrives after the next tool result. The top-level conductor may end its turn; notifications wake it.

**Integration.** When every conductor in a wave has reported, one top-level consolidator integrates the `ws-*` branches into the top integration branch (Stage 4), and the top-level reviewer and verifier cover the combined diff (Stages 5 and 6).

**Escalation.** Conductors never ask the user. A BLOCKED report goes to the top level, which asks the user and then continues that conductor with `SendMessage`.

**Workstream report.** The conductor's final action is `SubagentHandback({message: <this report>})`; if `SubagentHandback` is not among its tools, or a call to it fails, it ends its turn with the report as its final message, once no child is running:

```
## Workstream report: <name>
Status: DONE | BLOCKED — <reason or question for the user>
Repo: <path>
Integration: <branch> @ <sha> (worktree <abs path>), base <BASE sha>
Commits:
<git log --oneline BASE..HEAD>
Subtasks: <merged>/<planned> in <n> waves; review floor reached: <critical|major|minor|clean>
Verification: <command> -> PASS|FAIL   (one line per command)
Open items for the top level: <cross-workstream wiring, decisions, conflicts, or "none">
```

## When to use the full cycle vs partial

**Full cycle** (all 7 stages): Feature implementation, large refactors, multi-module changes.

**Skip Stage 5** (no reviewer): Trivial changes, documentation updates, config changes.

**Single wave only** (no multi-wave): When the planner produces only independent subtasks with no dependencies.

**No worktrees** (single architect, no isolation): When there's only 1 subtask. Spawn a single `architect` agent that works directly in the integration worktree, without `isolation: "worktree"` — but still spawn it. Do not do the work yourself.

## Coordination rules

- **Never run stages out of order.** Plan before verify. Verify before execute. Execute before review.
- **Always wait for all agents in a wave before starting the next wave**. Partial results from an incomplete wave cannot feed the next wave.
- **Always launch wave N's agents in a single message** with multiple `Agent` tool calls — never serialize independent subtasks.
- **Planner-verifier loop**: iterate until approved. Escalate to the user only if the same critical issue persists after revision.
- **Review-fix loop**: raise the severity floor each iteration (all → major+ → critical only). Stop when clean at the current floor.
- **Consolidator runs exactly once per wave.** Multiple consolidation passes indicate a planning failure.
- **Never re-implement what an agent already did.** If a subtask agent failed, retry that specific subtask in a fresh worktree from the same BASE — don't redo the whole wave.

## What you do NOT do

- **Write code yourself** — not even "small" fixes. Spawn an agent. Always.
- Skip the verifier to save time (it catches expensive mistakes)
- Spawn agents without a plan (the planner exists for a reason)
- Make design decisions (flag genuine ambiguity for the user — not scope trade-offs you could resolve by running the planner)
- Merge branches yourself (that's the consolidator's job)
- Rationalize skipping delegation ("it's just one file", "it's trivial", "faster to do it myself") — the whole point of this skill is structured delegation
- **Refuse the task, scope it down, or hand it back to the user before Stage 1 has run.** Spawning the planner is the cheapest possible step. Always do it first. The planner's output — not your intuition about difficulty — is what justifies any scope conversation with the user.
- **Claim your tools are unavailable.** You have Agent + all subagent types + parallel worktrees by default (explicit worktree mode whenever isolation is unavailable). If a `subagent_type` seems missing, re-read this skill — don't tell the user the environment is broken.

## Performance guidelines

- **Maximize wave 1** — the more parallel work in the first wave, the faster overall execution. No upper limit on subtask count.
- **Front-load reading** in the planner so architect prompts are precise.
- **Tests are subtasks** — write them in parallel with implementation, not after.
