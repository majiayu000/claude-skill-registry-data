---
name: cookoff
description: >-
  Runs parallel implementation competition at the design→implementation transition: dispatches 2-5 agents that each create their own plan from the shared design, then tests and the judge pick the winner. Use when design is complete and implementation is about to start — "let's build", "implement this", "looks good let's code", "ready to implement", or after a design doc is committed.
---

# Cookoff

Same design, multiple cooks compete. Each implementation team creates their own plan from the shared design, then implements it. Natural variation emerges from independent planning decisions.

**Part of Test Kitchen Development:**
- `omakase-off` - Chef's choice exploration (different approaches/designs)
- `cookoff` - Same design, multiple cooks compete (each creates own plan + implements)

**Key insight:** Don't share a pre-made implementation plan. Each agent generates their own plan from the design doc, ensuring genuine variation.

## Directory Structure

```
docs/plans/<feature>/
  design.md                    # Input: from brainstorming
  cookoff/
    impl-1/
      plan.md                  # Agent 1's implementation plan
    impl-2/
      plan.md                  # Agent 2's implementation plan
    impl-3/
      plan.md                  # Agent 3's implementation plan
    result.md                  # Cookoff results and winner
```

## When to Use

Trigger when user wants to implement a design:
- "Execute this plan" / "Implement the plan" / "Let's build this"
- After brainstorming completes and design doc exists
- Can also invoke explicitly: "cookoff this"

**Important:** Cookoff works from a **design doc**, not a detailed implementation plan. Each agent creates their own implementation plan.

## Detecting the Design-to-Implementation Transition

**Cookoff triggers at a SITUATION, not a specific skill's output.**

**The situation:** Design is complete, implementation is about to start.

**Signals that design phase just completed:**
- Design doc was written/committed
- User approved a design ("looks good", "yes", "let's do it")
- Discussion shifted from "what to build" to "how to build it"
- Any skill/flow is about to start implementation

**When you detect this transition, ALWAYS offer cookoff:**

```
Before we start implementation, how would you like to proceed?

1. Cookoff (recommended) - N parallel agents, each creates own plan, pick best
   → Complexity: [assess from design]
   → Best for: medium-high complexity features
2. Single implementation - One agent/session implements
3. Direct coding - Start coding without detailed plan
```

**This applies regardless of:**
- Which brainstorming skill was used (superpowers, other, or none)
- Whether a formal design doc exists (could be informal agreement)
- What implementation options another skill might present

**The key insight:** We're not injecting into another skill's menu. We're recognizing a SITUATION (design→implementation) and ensuring cookoff is offered at that moment.

## Phase 1: Implementation Options

**Present choices when user wants to implement:**

```
How would you like to implement this design?

1. Single subagent - One agent plans and implements
2. Cookoff - N parallel agents, each creates own plan, pick best
   → Complexity: [assess from design]
   → Recommendation: N implementations
3. Local - Plan and implement here in this session

Which approach?
```

**Routing:**
- Option 1: Single agent uses writing-plans then executing-plans, cookoff exits
- Option 2: Continue to Phase 2
- Option 3: User implements manually, cookoff exits

## Phase 2: Complexity Assessment

**Read design doc and assess:**
- Feature scope (components, integrations, data models)
- Risk areas (auth, payments, migrations, concurrency)
- Estimated implementation size

**Map to implementation count:**

| Complexity | Scope | Risk signals | Implementations |
|------------|-------|--------------| --------------- |
| Low | Small feature | None | 2 |
| Medium | Medium feature | Some | 3 |
| High | Large feature | Several | 4 |
| Very high | Major system | Critical areas | 5 |

**Setup directories:**
```bash
mkdir -p docs/plans/<feature>/cookoff/impl-{1,2,3}
```

**Announce:**
```
Complexity assessment: medium feature, touches auth
Spawning 3 parallel implementations
Each will create their own implementation plan from the design.
```

## Phase 3: Parallel Execution

**Setup worktrees:**
```
.worktrees/cookoff-impl-1/
.worktrees/cookoff-impl-2/
.worktrees/cookoff-impl-3/

Branches:
<feature>/cookoff/impl-1
<feature>/cookoff/impl-2
<feature>/cookoff/impl-3
```

**CRITICAL: Dispatch ALL agents in a SINGLE message**

Use `parallel-agents` pattern. Send ONE message with multiple Task tool calls:

```
<single message>
  Task(impl-1, run_in_background: true)
  Task(impl-2, run_in_background: true)
  Task(impl-3, run_in_background: true)
</single message>
```

Do NOT send separate messages for each agent.

**Subagent prompt:** See `references/phase3-subagent-prompt.md` for the full template (each agent gets the same instructions with their impl number substituted).

**Monitor progress:**
```
Cookoff status (design: auth-system):
- impl-1: planning... → implementing 5/8 tasks
- impl-2: planning... → implementing 3/8 tasks
- impl-3: planning... → implementing 6/8 tasks
```

## Phase 4: Judging

**Step 1: Gate check**
- All tests pass
- Design adherence - implemented what the design specified

**Step 2: Check for identical implementations**

Before fresh-eyes, diff the implementations:
```bash
diff -r .worktrees/cookoff-impl-1/src .worktrees/cookoff-impl-2/src
```

If implementations are >95% identical, note this - the planning step didn't create enough variation. Still proceed but flag in results.

**Step 3: Fresh-eyes on survivors**
```
Starting fresh-eyes review of impl-1 (N files)...
Checking: security, logic errors, edge cases
Fresh-eyes complete: 1 minor issue
```

### Step 4: Invoke Judge Skill

**CRITICAL: Invoke `test-kitchen:judge` now.**

The judge skill contains the full scoring framework with checklists. Invoking it fresh ensures the scoring format is followed exactly.

```text
Invoke: test-kitchen:judge

Context to provide:
- Implementations to judge: impl-1, impl-2, impl-3 (or however many)
- Worktree locations: .worktrees/cookoff-impl-N/
- Test results from each implementation
- Fresh-eyes findings from Step 3
- Feasibility flags identified
```

The judge skill will:
1. Fill out the complete scoring worksheet for each implementation
2. Build the scorecard with integer scores (1-5, no half points)
3. Check hard gates (Fitness Δ≥2, any score=1)
4. Announce winner with rationale

**Do not summarize or abbreviate the scoring.** The judge skill output should be the full worksheet.

**Cookoff-specific context:** In cookoff, all implementations target the same design, so Fitness should be similar. A Fitness gap (Δ≥2) indicates one implementation deviated from or misunderstood the design - not a different approach choice.

## Phase 5: Completion

**Verification on winner:**
```
Running final verification on winner (impl-2):
- npm test: 22/22 passing ✓
- npm run build: exit 0 ✓
- Design adherence: all requirements met ✓

Verification complete. Winner confirmed.
```

**Winner:** Use `finish-branch`
- Options: merge locally, create PR, keep as-is, discard

**Losers:** Cleanup
```bash
git worktree remove .worktrees/cookoff-impl-1
git worktree remove .worktrees/cookoff-impl-3
git branch -D <feature>/cookoff/impl-1
git branch -D <feature>/cookoff/impl-3
# Keep winner's worktree until merged
```

**Write result.md:** See `references/phase5-result-template.md` for the full template. Save to: `docs/plans/<feature>/cookoff/result.md`

## Skills Orchestrated

| Skill | Phase | Purpose | Fallback |
|-------|-------|---------|---------|
| `superpowers:writing-plans` | 3 | Each subagent creates their own implementation plan | Each agent writes own plan directly |
| `superpowers:executing-plans` | 3 | Each subagent implements their plan | Execute plan tasks sequentially with verification |
| `superpowers:dispatching-parallel-agents` | 3 | Dispatch ALL subagents in SINGLE message | Multiple Task tool calls in one message |
| `superpowers:using-git-worktrees` | 3 | Create worktree per implementation | `git worktree add .worktrees/<name> -b <branch>` |
| `superpowers:test-driven-development` | 3 | Subagents follow RED-GREEN-REFACTOR | RED-GREEN-REFACTOR cycle manually |
| `superpowers:verification-before-completion` | 3, 5 | Before claiming done; before declaring winner | Run command, read output, THEN claim status |
| `superpowers:requesting-code-review` | 3 | Review each impl after completion | Dispatch code-reviewer subagent |
| `fresh-eyes-review:fresh-eyes-review` | 4 | Quality review → judge input | 2-5 min review for security, logic, edge cases |
| `test-kitchen:judge` | 4 | **INVOKE** for scoring framework (loads fresh, ensures format compliance) | Scoring framework with checklists |
| `scenario-testing:scenario-testing` | 4 | Validate if scenarios defined | `.scratch/` E2E scripts, real dependencies |
| `superpowers:finishing-a-development-branch` | 5 | Handle winner, cleanup losers | Verify tests, present options, cleanup |

## Common Mistakes

**Sharing a pre-made implementation plan**
- Problem: All teams copy same code, no variation
- Fix: Each team uses writing-plans to create THEIR OWN plan from design doc

**Dispatching agents in separate messages**
- Problem: Serial dispatch instead of parallel
- Fix: Send ALL Task tools in a SINGLE message

**Not using writing-plans + executing-plans**
- Problem: Subagent implements ad-hoc
- Fix: Each subagent MUST use writing-plans then executing-plans

**Skipping fresh-eyes**
- Problem: Judge has no quality signal, just test counts
- Fix: Fresh-eyes on ALL survivors before comparing

**Not checking for identical implementations**
- Problem: Wasted compute on duplicates
- Fix: Diff implementations before fresh-eyes, flag if >95% similar

**Forgetting cleanup**
- Problem: Orphaned worktrees and branches
- Fix: Always cleanup losers, write result.md

## Example Invocation

```
User: "Let's build this" (after brainstorming produced design.md)

Claude: I'm using cookoff.

How would you like to implement this design?

1. Single subagent - One agent plans and implements
2. Cookoff - 3 parallel agents, each creates own plan, pick best
   → Complexity: medium feature, touches auth
   → Recommendation: 3 implementations
3. Local - Plan and implement here

User: "2"

Claude: Spawning 3 parallel implementations...
Each will create their own implementation plan from the design.

[Phase 3: Create worktrees, dispatch ALL 3 agents in single message]
[Each agent: reads design → writes plan → implements]

Cookoff status:
- impl-1: planning → implementing 6/8 tasks
- impl-2: planning → implementing 4/7 tasks
- impl-3: planning → implementing 5/9 tasks

[All 3 complete]

[Phase 4: Diff check - implementations are different ✓]
[Fresh-eyes on all 3]

| Impl | Plan Approach | Tests | Fresh-Eyes |
|------|---------------|-------|------------|
| impl-1 | Component-first | 24/24 | 1 minor |
| impl-2 | Data-layer-first | 22/22 | 0 issues |
| impl-3 | TDD-strict | 26/26 | 2 minor |

Recommendation: impl-2 (cleanest)
User: "2"

[Phase 5: Verify winner, cleanup losers]

Winner: impl-2 ready to merge
Cleanup: 2 worktrees removed
Plans preserved: docs/plans/<feature>/cookoff/
```
