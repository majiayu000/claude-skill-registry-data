---
name: agent-teams
description: Orchestration playbook for parallel multi-agent work in Claude Code. Use when fanning out genuinely parallel, independent work — N independent modules, multi-lens review, competing-hypothesis debugging, backend+frontend that must agree on a contract. Defaults to background subagents (with worktree isolation only when they write files in parallel and merge later); covers when to reach for Workflows instead. Covers the lead's pipeline (plan → parallel execute → review → merge), per-role models, worktree/merge flow, and the plan-approval gate.
---

# Parallel multi-agent playbook (lead-side)

This skill is the lead/orchestrator's reference for fanning out parallel work.
Only the lead orchestrates and spawns — workers implement and report back.

## 1. Fan out only when work is genuinely parallel

Parallel agents cost significantly more tokens than one session (each is a full
Claude instance). Reach for fan-out only when parts are **independent and run at
the same time**:

- N independent modules/files with no shared edits
- multi-lens review (security / performance / tests) at once
- debugging with competing hypotheses
- backend + frontend that must agree on a contract

For **sequential** work (plan → build → ship), a dependency chain, or same-file
edits, do NOT fan out — run it through the `feature-workflow` skill, whose
delegated execute spawns one `step-executor` per step on the session's own
branch. The value here is the parallel **execution** phase only.

## 2. Pick the mechanism (this is the important decision)

| Mechanism | Use when | Coordination | Cost / overhead |
|-----------|----------|--------------|-----------------|
| **Background subagents** *(DEFAULT)* | independent units; contracts known up front | none — contract pre-specified in each prompt | low; in-process, no setup |
| **Workflows** | large fan-out (10s+), deterministic/repeatable orchestration, cross-checking/voting, resumable runs | script variables | medium; you write/run a script |

Default to **background subagents** (`Agent` tool, no `name`). `team-executor`
sets `background: true` in its frontmatter — the documented way to make a
subagent always run in the background; for ad-hoc spawns say "in the background"
(`run_in_background: true` on the Agent call also works on current builds). They
run **in-process** under the lead (no separate OS process), need
**no shutdown handshake**, and deliver a clean completion notification.
Pre-specify any cross-unit contract in each spawn prompt so they never need to
talk to each other.

Reach for **Workflows** when the fan-out is large or you want deterministic,
repeatable, resumable orchestration with built-in cross-checking. (In this kit
only the lead runs Workflows — the worker roles' `tools` lists deliberately omit
the Workflow and Agent tools, so they can't fan out on their own.)

## 3. Worktree isolation: every concurrent writer gets one

You're in this skill because the fan-out decision already came back "parallel"
— that call is made *before* `agent-teams` loads, per the global CLAUDE.md rule
("Inside a pipeline, delegation is the default … If one subagent can do it, use
one") and `feature-workflow`'s "When to offer (lead only)" bullet — inside a
pipeline, the plan's `Parallel:` line. So within a
fan-out the rule is simple: **writers that run concurrently get `isolation:
worktree` each** — even if the plan says their files are disjoint. Read-only
fan-out (review, research, multi-lens analysis) never gets a worktree,
regardless of count — nothing is written, so isolation is pure overhead.

**You don't decide this per spawn.** `team-executor` carries `isolation:
worktree` in its own frontmatter, so every executor gets a worktree whether or
not the spawning prompt remembers to ask. That's deliberate: the decision was
already made when you picked the parallel path, and a rule that has to be
re-derived at each spawn is a rule that gets skipped.

**If you get here with only one writer, that's not an agent-teams run.** It
means the fan-out decision was wrong or skipped — stop, and hand the work to
`feature-workflow`'s sequential delegated execute, which spawns `step-executor`
on the session's own branch with no worktree and nothing to merge.

**Set `worktree.baseRef` to `"head"` before the first fan-out.** Subagent
worktrees branch from the repository's *remote default branch* unless you
change this — so with the default (`"fresh"`), every executor starts from a
clean `origin/main` that has neither `docs/prompts/<feature>-plan.md` nor any
of the session's in-progress commits, and the merger then drags main↔branch
divergence into each unit. In `settings.json`:
`{"worktree": {"baseRef": "head"}}`.
A worktree is also a fresh checkout, so gitignored files don't come along —
add a `.worktreeinclude` if executors need `.env` or similar to run tests.

**Why "disjoint files" isn't a safe reason to skip worktrees with 2+ writers.**
Disjointness isn't knowable at spawn time: a new unit usually has to register
itself in some hub file (a dispatcher, router, barrel export, `package.json`)
that the plan assigned to nobody. Plan around this:
**if units keep colliding on a hub file, give that file to one unit** instead
of isolating three agents that all want to edit it — prefer fewer, larger
units over more, smaller colliding ones.

**Why review needs a separable diff.** `team-reviewer` reviews "its worktree
diff" and `team-merger` merges each unit in turn after approval; the global
codex gate challenges the merged feature diff once, but the reviewer
still needs a per-unit diff. With 2+ concurrent writers sharing one checkout there is no per-unit
diff to review or merge independently, and a unit that fails review can't be
dropped without untangling it from the others it shares a tree with.

**Clean up after merge — nothing else will.** Once a unit lands, the merger
removes its worktree (`git worktree remove`) and deletes the merged branch
(`git branch -d`) immediately after each successful merge. That is not a
tidiness step: **neither platform cleanup path ever reclaims an executor
worktree.** Claude Code auto-removes a subagent worktree only if the subagent
made no changes, and the periodic `cleanupPeriodDays` sweep skips any worktree
still holding work — changed files, untracked files, or **unpushed commits** —
which describes every executor worktree by construction, since executors commit
locally and never push.
If the merger doesn't remove it, it stays until someone runs `git worktree
remove --force` by hand. For a run that dies before the merger gets there, the
backstop is the lead's end-of-run check that no feature worktrees/branches
remain. The net result: nothing lingers on disk once work
is merged, and there is no pane or process to tear down.

## The pipeline

```
1. PLAN      (LEAD in native plan mode; subagent discovers + validates)
   → the LEAD calls EnterPlanMode, then authors the plan itself, writing
     directly into the plan file — units, file boundaries, shared contracts,
     open decisions, per feature-workflow's Plan shape block
   → codebase discovery goes to explorer subagents (Sonnet, read-only), which
     return summaries; the lead reads no product file itself in plan mode
   → the LEAD spawns team-plan-reviewer (read-only) to validate the plan
     against the code, revises the plan file itself for any blocking finding,
     resolves the open decisions with one AskUserQuestion, then calls
     ExitPlanMode.   ← only gate
   → on approval: copy the plan file to docs/prompts/<feature>-plan.md, commit,
     and mirror the units into the native task list (one task per unit, `owner`
     = the executor that gets it, `addBlockedBy` for any cross-unit ordering;
     REVIEW/MERGE/CODEX tasks blocked by the units) — the list is the work
     queue and the progress view (`Ctrl+T`)
2. EXECUTE   (background subagents: team-executor)   ← parallel
   → lead marks each unit's task in_progress as it spawns its executor and
     completed when the unit's report is ingested (never with red tests);
   → lead spawns one background subagent per independent unit; each gets a
     worktree from team-executor's own `isolation: worktree` frontmatter, not
     from the spawn call; contracts are pre-specified in each prompt
3. REVIEW    (subagent: team-reviewer, opus — read-only, NO worktree)
   → adversarially verifies each unit's diff before it lands
4. MERGE     (subagent: team-merger, sonnet)
   → merges each approved worktree into the base branch; after each successful
     merge removes that worktree + deletes its branch; reports completion
```

Every step delegates to a subagent except the lead's own plan-mode authoring
and gates in step 1; step 2 is the only fan-out (one background subagent per unit).
The lead runs the gates and the codex gate, and ingests summaries — it
does not read large diffs or implement. If the lead starts implementing, stop and
delegate.

**Subagents are headless — they never prompt the user.** A subagent runs to
completion and hands its result back; it has no channel to ask you anything
mid-run. So never delegate an *interactive* gate to one — `ExitPlanMode` and
`AskUserQuestion` are unavailable to a subagent, so a delegated gate either
auto-picks silently or dies. Gates run in the **lead** (the session you're
attached to); only headless work goes to subagents. (This is why step 1 splits:
the lead authors and gates, a subagent validates.)

## Approval gate: PLAN ONLY

The lead must get the **user's** approval on the plan (step 1) before any
fan-out. The gate is Claude's native `ExitPlanMode` in the lead — never a
subagent, which has no channel to the user. Resolve the open taste-decisions with
one AskUserQuestion first, then present the plan and wait. Delegated approval
("approve it yourself") follows the AFK gate's two branches in global CLAUDE.md:
skip plan mode if not yet in it; otherwise get the owner's click or Shift+Tab
before they leave.
After the plan is approved, executors run, review runs, and the merger lands work
and reports completion.
```
5. CODEX     (lead launches `codex-challenge.sh` as one background Bash; `codex-triage` agent triages)
   → ONE `~/.claude/skills/feature-workflow/scripts/codex-challenge.sh <feature-base-sha>..HEAD`
     on the merged feature diff — full output to a file, triaged verdict shown;
     the fix loop, its stop rule and the standalone-finding question are
     feature-workflow stage 5, verbatim.
```

## The approved tail runs unprompted

The approved tail (EXECUTE → REVIEW → MERGE → CODEX) runs unprompted from plan
approval: the lead spawns, ingests summaries, and moves on without returning to
the user except at the real gates — those feature-workflow stage 5 names, and push approval. Roles still return
machine-checkable proof — test exit code + output tail, `git worktree list` /
`git status`, structured per-unit verdicts — because the lead judges completion
from those, not from prose "done".

## Models + effort per role

Per-role `model:` and `effort:` come from the agent definition files and are
honored when the role runs as a subagent. Plan review runs on the session's model and
effort, diff review on Opus; code-writing (Opus when the plan marks a unit), search and mechanical roles run on Sonnet.

| Role | Spawned as | Model | Effort | Rationale |
|------|-----------|-------|--------|-----------|
| Orchestrator (lead) | main session | whatever the owner picked at session start | the session's effort | coordination, authoring, gates |
| `team-plan-reviewer` | subagent | the session's model (`inherit`) | the session's | validates the plan against the code before the gate; read-only |
| `team-executor` | **background subagent** | Sonnet 5.5 (Opus only when the plan marks the unit with a reason) | the saved `claude-sonnet-5-5` level (high) | writes code; a well-specified unit needs no more model |
| `team-reviewer` | subagent | Opus | medium | adversarial bug-hunting on a bounded diff |
| `team-merger` | subagent | Sonnet | medium | mechanical merge/verify |
| `explorer` | subagent | Sonnet | medium | codebase search, read-only, effort pinned by frontmatter (built-in `Explore` floats with the session's effort and runs on Opus under a Fable or Opus master) |

The global spawn-pin rule applies; the table above is this pipeline's role→model
mapping. Override per spawn only when the plan marks a unit Opus with a reason (a design call left to the executor, work spanning several subsystems or that no single test or build can check, or a hard class — concurrency, security, data migration, structural refactor). The
executors carry no `effort:` line: they run at the level saved for their model under `modelSettings`, and the roles that do carry one honor it as background subagents.

## Spawn prompt contract (the lead writes these inline)

Each executor is a background subagent with **no inherited context** — it never
sees this conversation, the plan file's surrounding discussion, or its siblings.
So each spawn prompt must stand alone. Write it yourself as you spawn: it's a
handful of tool calls' worth of text per unit, and routing it through a separate
prompt-writing agent only puts the same words through another context on the way
back to you.

State the unit's **goal and its boundaries**, then stop — don't enumerate
procedure. Step-by-step instructions written for prior models reduce
quality on current ones.

Every prompt carries:
- **Scope + ownership** — what the unit is for, the files it owns, and the files
  it must not touch. Ownership is disjoint across units by construction; a hub
  file belongs to exactly one unit.
- **The full cross-unit contract** it must honor (API shapes, types, names),
  baked in. Background subagents don't talk to each other, so anything it needs
  from a sibling has to be in the text.
- **Acceptance criteria and how to verify them** — the tests or commands that
  prove the unit is done. State them once; no "re-verify" or "double-check"
  rituals.
- **The worktree/branch** it works in. (Retirement is mechanical — each agent's
  `maxTurns` frontmatter cap; spawn prompts carry no budget line, per
  feature-workflow's token-discipline rule.)
- **The model pin** from the table above (`sonnet`, or `opus` only where the
  approved plan marks that unit Opus with a reason) — set via the Agent tool's
  `model:` parameter on the spawn call, not text inside the prompt.

One concern per prompt, sized so the executor finishes in roughly ≤100 tool
calls — a unit bigger than that was planned too large; split it. A fixer prompt
carries exactly one finding set, never several. Nothing in a prompt goes beyond
the approved plan.

## Spawn recipes

Plan (lead in plan mode; explorer discovers, lead authors, reviewer validates), then gate:
> [EnterPlanMode] Spawn explorer subagents to report the files, symbols, and
> patterns <feature> touches, then author the plan directly into the plan file —
> units, file boundaries, shared contracts, open decisions — per feature-workflow's
> Plan shape block. Have team-plan-reviewer validate it, resolve the open decisions
> with the user, and get approval via ExitPlanMode before any execution.

Fan out execution (background subagents that write + merge → worktree), after approval:
> Spawn one team-executor as a background subagent per unit in the approved plan,
> with **no name** (team-executor's `background: true` and `isolation: worktree`
> frontmatter already handle backgrounding and the per-unit worktree).
> Give each a self-contained spawn prompt per the contract above (the cross-unit
> contract is baked in, so they don't message each other). Notify me when each
> completes.

Review + merge (subagents; reviewer is read-only, no worktree):
> Use team-reviewer to adversarially verify each unit's diff, then team-merger to
> merge approved worktrees into the base branch, run tests, and report completion.

Read-only fan-out (no worktree) — e.g. multi-lens review with no executors:
> Spawn 3 background subagents to review this change in parallel — one on
> security, one on performance, one on test coverage — and report findings. No
> worktrees; they only read.

For a large or repeatable fan-out, consider a **Workflow** instead of hand-
spawning subagents: a deterministic script (plan → fan-out → review → merge) that
scales to many units, cross-checks results, and resumes if interrupted.

## Relationship to the feature workflow

This is the parallel-execution variant of the `feature-workflow` skill's pipeline; its stage-5 codex gate rules apply verbatim.
Planning (native plan mode) and shipping are unchanged; fan-out only replaces the execute phase's
sequential per-step subagents with parallel agents when the steps are
independent. A pair from a feature-workflow plan's `Parallel:` line doesn't run
this pipeline: `feature-workflow` stage 4 spawns its two `team-executor`s and one
`team-merger` directly, and the per-step codex round on the merged range stands
in for `team-reviewer`.
