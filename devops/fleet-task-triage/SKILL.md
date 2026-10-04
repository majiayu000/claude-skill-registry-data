---
name: fleet-task-triage
description: How PM triages inbox tasks — set ALL fields, assign agents, identify dependencies. The foundation for correct dispatch.
---

# Task Triage — PM's Core Skill

Triage is the PM's highest-frequency operation. Every unassigned inbox task passes through you. The quality of triage determines the quality of everything downstream: dispatch, model selection, contributions, effort, and stage progression.

## Why Triage Matters to 5 Systems

1. **Orchestrator** reads task fields to decide dispatch order (task_scoring.py)
2. **Router** reads story_points + complexity to select model + effort (model_selection.py)
3. **Contributions** reads task_type + agent_name to determine required inputs (synergy-matrix.yaml)
4. **Context** reads task_stage + delivery_phase to inject stage instructions (methodology.yaml)
5. **Budget** reads effort level to assess cost impact (budget_monitor.py)

A task with missing fields = broken dispatch. A task with wrong type = wrong contributions. A task with wrong agent = wrong tools.

## The 12 Fields You MUST Set

Every task needs ALL of these before it leaves inbox:

| Field | What to Set | Why It Matters |
|-------|------------|----------------|
| title | Clear, specific action | Agent reads title first |
| description | Full context, acceptance criteria | Agent needs this to plan |
| task_type | epic/story/task/subtask/spike/concern | Controls contribution matrix + review gates |
| agent_name | The agent best suited | Determines role-specific tools + skills |
| story_points | 1/2/3/5/8 (Fibonacci) | Model selection: SP >= 5 = opus, SP <= 2 = sonnet |
| complexity | low/medium/high | Model selection: high + SP >= 5 = opus + high effort |
| task_stage | conversation/analysis/investigation/reasoning/work | Determines methodology protocol + blocked tools |
| task_readiness | 0-100 | Maps to stage boundaries (0-20 = conversation, 80-99 = reasoning) |
| delivery_phase | poc/mvp/staging/production | Phase standards + test rigor + infrastructure needs |
| requirement_verbatim | PO's exact words, unmodified | Anti-corruption anchor — agents reference this |
| priority | low/medium/high/urgent | Dispatch order within scoring |
| plan_id / sprint | Sprint assignment | Sprint velocity tracking |

## Triage Decision Tree

```
New inbox task arrives
  |
  +-- Is the requirement clear?
  |     NO  --> task_stage = conversation, task_readiness = 10
  |             Agent will clarify with PO first
  |     YES --> Continue
  |
  +-- Does it need research?
  |     YES --> task_stage = analysis, task_readiness = 30
  |     NO  --> Continue
  |
  +-- Is the approach obvious?
  |     NO  --> task_stage = investigation, task_readiness = 50
  |     YES --> Continue
  |
  +-- Is it a simple fix or subtask?
  |     YES --> task_stage = work, task_readiness = 99
  |             (skip reasoning for trivial work)
  |     NO  --> task_stage = reasoning, task_readiness = 80
  |             Agent will plan before implementing
  |
  +-- Who should do it? (agent_name)
  |     Code work      --> software-engineer
  |     Design needed  --> architect (first), then transfer to engineer
  |     Security scope --> devsecops-expert
  |     Infra/CI/CD    --> devops
  |     Test design    --> qa-engineer
  |     Documentation  --> technical-writer
  |     UX assessment  --> ux-designer
  |     Process audit  --> accountability-generator
  |
  +-- What type? (task_type)
  |     Large scope, multiple agents --> epic
  |     Feature with contributions   --> story
  |     Single-agent, moderate       --> task
  |     Child of epic/story          --> subtask
  |     Research only                --> spike
  |     Issue to investigate         --> concern
  |
  +-- Set story_points based on scope
  |     Trivial (1 file, < 1h)     --> 1
  |     Small (2-3 files, < 4h)    --> 2
  |     Medium (module, < 1 day)   --> 3
  |     Large (cross-module, days) --> 5
  |     XL (architectural, week+)  --> 8
```

## Common Triage Mistakes

1. **Missing requirement_verbatim** — agent has nothing to anchor to. Always copy PO's exact words.
2. **task_type = "task" for everything** — this skips the contribution matrix. Stories and epics NEED contributions.
3. **task_stage = "work" for unclear tasks** — agent will implement without understanding. Start at conversation.
4. **No story_points** — model selection falls back to defaults. Set it explicitly.
5. **Wrong agent** — engineer assigned to a design task. Architect should go first.

## After Triage: What You Trigger

When you set fields and move a task from unassigned to assigned in inbox:
- Orchestrator scores it for dispatch (task_scoring.py reads all fields)
- If epic/story: brain may create contribution subtasks from synergy matrix
- Agent sees it on next heartbeat with FULL context (all fields populated)
- The stage protocol text is injected based on task_stage you set

Your triage quality = their dispatch quality.
