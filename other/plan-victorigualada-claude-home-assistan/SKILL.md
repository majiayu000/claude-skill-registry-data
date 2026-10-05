---
name: ha:plan
description: "Plan features spanning multiple domains: config flow (setup, migration, breaking changes), auth (OAuth, reauth), real-time (push coordinators, dispatcher), webhooks, service actions. Use when designing interconnected systems or converting review findings into tasks."
effort: high
argument-hint: <feature description OR path to review/plan file>
---

# Plan Home Assistant Feature

Plan a feature by spawning Home Assistant specialist agents, then output
structured plan with checkboxes.

## What Makes /ha:plan Different from /plan

1. Spawns Home Assistant specialist agents for research
2. Plans with `[coordinator]`, `[lit]`, `[service]` task routing
3. Checks for Iron Law compliance in the plan
4. Includes `mypy/ruff/hassfest/pytest` verification
5. Understands integration module boundaries

## Usage

```
/ha:plan Add energy sensors with a reset service action
/ha:plan .claude/plans/notifications/reviews/notifications-review.md
/ha:plan Implement notifications --depth deep
/ha:plan .claude/plans/auth/plan.md --existing
```

## Arguments

- `$ARGUMENTS` = Feature description, review file, or existing plan
- `--depth quick|standard|deep` = Planning depth (auto-detected)
- `--existing` = Enhance an existing plan with deeper research

## Workflow

1. **Gather context** — File path (skip to agents), brainstorm
   interview.md (skip clarification), clear description, or vague
2. **Clarify if vague** — Ask questions ONE at a time (skip if
   brainstorm interview.md exists with Status: COMPLETE)
3. **Detect depth** — Auto-detect quick/standard/deep
4. **Runtime context** (dev instance) — Gather live entity states,
   registered services, and log warnings before spawning agents
   (direct path only — the research orchestrator gathers its own)
5. **Spawn research** — Selective, based on need. **0–2 agents**:
   spawn directly in parallel. **3+ agents** (broad multi-platform
   feature): spawn ONE `planning-orchestrator` to run and compress
   the fan-out, then read only its digest and
   `summaries/consolidated.md`. Create a Claude Code task per spawn:
   `TaskCreate({subject: "{Agent} research", activeForm: "Researching..."})`,
   mark `in_progress` on spawn, `completed` when done
6. **Wait for ALL agents** — Do NOT proceed until all return
   "completed". NEVER write plan while any agent is still running
7. **Breadboard** (Lit) — System map for multi-page features
8. **Completeness check** — MANDATORY when planning from review
9. **Split decision** — One plan or multiple, concrete options
10. **Generate plan** — Checkboxes, phased tasks, code patterns.
    Also create `plans/{slug}/scratchpad.md` for decisions and dead-ends
11. **Self-check** (deep only) — Three questions in Risks section
12. **Present and ask** — STOP, show summary, let user decide

**When planning from review**: Every finding must appear in the
plan — either as a task OR explicitly deferred by the user.

See `${CLAUDE_SKILL_DIR}/references/planning-workflow.md` for detailed step-by-step.

### --existing Mode (Deepening)

Enhances an existing plan instead of creating a new one:

1. Load plan, search `.claude/solutions/` for known risks
2. Spawn SPECIALIST agents (not Explore) for thin sections.
   Each agent writes to `.claude/plans/{slug}/research/` and
   returns only a 500-word summary. Same agent selection rules
3. Wait for ALL agents (mark tasks `completed` as each finishes)
4. Add implementation detail, resolve spikes, add verification
5. Present diff summary — **NEVER delete existing tasks**

## Iron Laws

1. **NEVER auto-start /ha:work** — Always present plan and ask
2. **Research before assuming** — Web-search unfamiliar tech
3. **Spawn agents selectively** — Only relevant, not all
4. **NEVER write plan while agents still running**
5. **NEVER skip input findings** — Every finding MUST have a task
6. **Do NOT spawn pypi-library-researcher for existing deps**
7. **Skip research when planning from review/investigation** — When
   input is a review file or `/ha:investigate` output, the findings
   ARE the research. Do NOT spawn agents to re-discover what the
   review already found. Convert findings directly to plan tasks.
   (Confirmed: 56-session analysis showed same findings discovered
   3-4x across review→investigate→plan phases, wasting ~96K tokens)
8. **Every phase with `[lit]` tasks starts with the Impeccable gate
   task** — first task of the phase: verify the `impeccable` skill is
   installed and invoke it before UI implementation; if missing, ask
   the user to install it. This is a plan task, not prose — see the
   plan template.

## Integration with Workflow

```text
/ha:plan {feature}  <-- YOU ARE HERE
       |
   /ha:plan --existing (optional enhancement)
       |
   ASK USER -> /ha:work .claude/plans/{feature}/plan.md
       |
/ha:review → /ha:compound
```

## Notes

- Plans saved to `.claude/plans/{slug}/plan.md`
- Research reports in `.claude/plans/{slug}/research/` can be deleted after

## CRITICAL: After Writing the Plan

**STOP. Do NOT proceed to implementation.**

After writing `.claude/plans/{slug}/plan.md`:

1. Summarize: task count, phases, key decisions
2. Use `AskUserQuestion` with options:
   - "Start in fresh session" (recommended for 5+ tasks)
   - "Get a briefing" (`/ha:brief` — interactive walkthrough)
   - "Start here"
   - "Review or adjust the plan"
3. Wait for user response. Never auto-start work.

**When user selects "Start in fresh session"**, print:

```
1. Run `/new` to start a fresh session
2. Then run one of:
   /ha:work .claude/plans/{slug}/plan.md
   /ha:full .claude/plans/{slug}/plan.md  (includes review + compound)
```

This is Iron Law #1. Violating it wastes user context.

## References (DO NOT read — for human reference only)

- `${CLAUDE_SKILL_DIR}/references/planning-workflow.md` — Detailed step-by-step
- `${CLAUDE_SKILL_DIR}/references/plan-template.md`
- `${CLAUDE_SKILL_DIR}/references/complexity-detail.md`
- `${CLAUDE_SKILL_DIR}/references/example-plan.md`
- `${CLAUDE_SKILL_DIR}/references/agent-selection.md`
- `${CLAUDE_SKILL_DIR}/references/breadboarding.md`
