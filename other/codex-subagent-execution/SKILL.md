---
name: codex-subagent-execution
description: Use when an approved plan has independent tasks ready for delegated execution with fresh subagents and two-stage review.
load_priority: on-demand
---

## TL;DR
Dispatch fresh subagent per task → implementer works → spec reviewer verifies requirements → code quality reviewer verifies quality → fix loops until approved → next task. Use `$sdd` or `$dispatch` to activate.

# Subagent-Driven Execution

## Activation

1. Activate on `$codex-subagent-execution`, `$sdd`, or `$dispatch`.
2. Activate when executing an approved implementation plan with independent tasks.
3. Activate after `codex-plan-writer` generates plan and user approves.
4. Activate when `codex-workflow-autopilot` routes to `implement` phase with independent tasks.
5. Activate on `$review-feedback` or when receiving code review feedback that needs technical evaluation before changes.

**Announce at start:** "I'm using codex-subagent-execution to implement this plan task-by-task."

## The Iron Law

```
FRESH SUBAGENT PER TASK + TWO-STAGE REVIEW = HIGH QUALITY
```

**Why subagents:** You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused. They should never inherit your session's context or history — you construct exactly what they need. This preserves your own context for coordination work.

## When to Use

```
Have implementation plan?
    |- Yes → Tasks mostly independent?
    |   |- Yes → Use codex-subagent-execution ($sdd)
    |   `- No (tightly coupled) → Manual execution
    `- No → Write plan first ($plan)
```

## The Process

```
Read plan → Extract all tasks → Create checklist

For each task:
  1. Dispatch implementer subagent (agents/implementer-prompt.md)
     |- Questions? → Answer, re-dispatch
     `- Implements → tests → commits → self-reviews
  2. Dispatch spec reviewer (agents/spec-reviewer-prompt.md)
     |- Issues? → Implementer fixes → re-review
     `- ✅ Spec compliant
  3. Dispatch code quality reviewer (agents/code-quality-reviewer-prompt.md)
     |- Issues? → Implementer fixes → re-review
     `- ✅ Quality approved
  4. Mark task complete

All tasks done → Final code review → Finish ($finish or $commit)
```

## Model Selection

Use the least powerful model that can handle each role to conserve cost and increase speed.

| Task Type | Model Tier | Signals |
|-----------|-----------|---------|
| Mechanical implementation | Fast/cheap | 1-2 files, clear spec, isolated function |
| Integration work | Standard | Multi-file coordination, pattern matching |
| Architecture & review | Most capable | Design judgment, broad codebase understanding |

## Safe Parallel Dispatch

Parallel implementation subagents are allowed only when all conditions are true:

1. Tasks have disjoint write scopes and no shared migration/config/schema file.
2. Each subagent has explicit file ownership and a clear responsibility boundary.
3. No subagent depends on another subagent's unmerged output.
4. The coordinator reserves final integration, conflict resolution, and verification for the main session.
5. Each branch of work still receives spec compliance review and code quality review before completion.

If write scopes overlap, run tasks sequentially. Parallel speed is not worth merge conflicts or inconsistent architecture.

## Handling Implementer Status

| Status | Action |
|--------|--------|
| **DONE** | Proceed to spec compliance review |
| **DONE_WITH_CONCERNS** | Read concerns → address if correctness/scope issue → proceed if observation |
| **NEEDS_CONTEXT** | Provide missing context → re-dispatch |
| **BLOCKED** | Assess: context → re-dispatch; reasoning → upgrade model; too large → split; plan wrong → escalate to human |

**Never** ignore an escalation or force retry without changes.

## Prompt Templates

Templates in `agents/` directory:

- `agents/implementer-prompt.md` — Dispatch implementer subagent
- `agents/spec-reviewer-prompt.md` — Dispatch spec compliance reviewer
- `agents/code-quality-reviewer-prompt.md` — Dispatch code quality reviewer

## Example Workflow

```
You: I'm using codex-subagent-execution to implement this plan.

[Read plan file once]
[Extract all 5 tasks with full text and context]
[Create task checklist]

Task 1: User authentication endpoint

[Dispatch implementer with full task text + context]
Implementer: "Should I use JWT or session tokens?"
You: "JWT — see existing auth middleware in src/middleware/auth.js"
Implementer: Implemented → 5/5 tests pass → committed

[Dispatch spec reviewer]
Spec reviewer: ✅ Spec compliant — all requirements met

[Dispatch code quality reviewer]
Code reviewer: ✅ Approved — clean implementation

[Mark Task 1 complete]

Task 2: Rate limiting middleware

[Dispatch implementer]
Implementer: Implemented → 8/8 tests pass → committed

[Dispatch spec reviewer]
Spec reviewer: ❌ Missing: per-user rate limits (spec says "per-user")

[Implementer fixes]
[Spec reviewer re-reviews]
Spec reviewer: ✅ Compliant now

[Dispatch code quality reviewer]
Code reviewer: Important: Magic number 100 for rate limit
[Implementer extracts RATE_LIMIT_PER_MINUTE constant]
[Code reviewer re-reviews]
Code reviewer: ✅ Approved

[Mark Task 2 complete]

... (remaining tasks)

[Final code review for entire implementation]
[Run $gate for quality verification]
[Use $commit or $finish]
```

## Red Flags — Never Do

- Start implementation on main/master branch without user consent
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementation subagents in parallel against overlapping files, shared schemas, or shared configuration
- Make subagent read plan file (provide full text instead)
- Skip scene-setting context
- Ignore subagent questions
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues = fix = review again)
- Let implementer self-review replace actual review (both needed)
- **Start code quality review before spec compliance is ✅** (wrong order)
- Move to next task while either review has open issues

## CodexAI Integration

### With Scrum Subagents

When project uses `codex-scrum-subagents`:
- Story delivery ceremony triggers subagent execution
- QA role maps to spec reviewer
- Security role adds security review as 3rd stage when applicable

### With Quality Gate

After all tasks complete:
```bash
# Full verification
python codex-execution-quality-gate/scripts/auto_gate.py --mode full --project-root <repo>

# Deploy readiness
python codex-execution-quality-gate/scripts/auto_gate.py --mode deploy --project-root <repo>
```

### With Git Worktrees

**Recommended:** Set up isolated workspace before starting:
```
$worktree → create isolated branch → $sdd → execute plan → $finish
```

## Related Skills

- **`codex-plan-writer`** — Creates the plan this skill executes
- **`codex-test-driven-development`** — Subagents follow TDD for each task
- **`codex-git-worktrees`** — Set up isolated workspace before execution
- **`codex-execution-quality-gate`** — Verify final implementation via `$gate`
- **`codex-verification-discipline`** — Evidence before claims, always
- **`codex-branch-finisher`** — After all tasks complete, use `$finish` for structured completion
- **`codex-scrum-subagents`** — Team-level coordination overlay

## Reference Files

- `agents/implementer-prompt.md`: implementer subagent dispatch template
- `agents/spec-reviewer-prompt.md`: spec compliance review template
- `agents/code-quality-reviewer-prompt.md`: code quality review template
- `references/code-review-discipline.md`: how to receive and evaluate code review feedback without performative agreement
