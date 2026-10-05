---
name: ha:full
description: Use for large features spanning multiple platforms or autonomous end-to-end implementation. Runs the full plan-implement-review-compound cycle with specialist agents. NOT for executing an existing plan file — use /ha:work for that.
effort: high
argument-hint: <feature description>
---

# Full Home Assistant Feature Development

Execute complete Home Assistant integration development autonomously: research
patterns, plan with specialist agents, implement with verification, Python code
review. Cycles back automatically if review finds issues.

## Usage

```
/ha:full Add a new cloud integration with OAuth config flow
/ha:full Push-based sensor platform driven by a dispatcher coordinator
/ha:full Add service actions with coordinator scheduling --max-cycles 5
```

**Wrong input guard**: if the argument is a path to an existing plan file
(`.claude/plans/*/plan.md`), do NOT re-plan it. Say so and run `/ha:work {path}`
instead — the plan phase already happened.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        /ha:full {feature}                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  │
│  │Discover│→ │  Plan  │→ │  Work  │→ │ Verify │→ │ Review │→ │Compound│→Done│
│  │ Assess │  │[Pn-Tm] │  │Execute │  │  Full  │  │4 Agents│  │Capture │     │
│  │ Decide │  │ Phases │  │ Tasks  │  │  Loop  │  │Parallel│  │ Solve  │     │
│  └───┬────┘  └────────┘  └────────┘  └───┬────┘  └────────┘  └────────┘     │
│       │                            ↑      │    ↑              │         │
│       ├── "just do it" ────────────┤      │    │              │         │
│       ├── "plan it" ──┐            │      ↓    │              │         │
│       │               ↓            │ ┌────────┐│              │         │
│       │     ┌──────────────┐       │ │Fix     ││ ┌─────────┐ │         │
│       │     │   PLANNING   │       │ │Issues  │└─│ Fix     │←┘         │
│       │     └──────────────┘       │ └───┬────┘  │ Review  │           │
│       │                            │     ↓       │ Findings│           │
│       │                       ┌────┴─────────┐   └────┬────┘           │
│       │                       │   VERIFYING   │←──────┘                │
│       └── "research it" ─────┘  (re-verify)                            │
│            (comprehensive plan)                                         │
│                                                                  │
│  On Completion:                                                  │
│  Auto-compound: Capture solved problems → .claude/solutions/     │
│  Auto-suggest: /ha:document → /ha:learn-from-fix                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## State Machine

```
STATES: INITIALIZING → DISCOVERING → PLANNING → WORKING →
        VERIFYING → REVIEWING → COMPLETED → COMPOUNDING | BLOCKED
```

Save state in `.claude/plans/{slug}/progress.md` AND via Claude Code
tasks. Create one task per phase at start, mark `in_progress` on
entry and `completed` on exit:

```
TaskCreate({subject: "Discover & assess complexity", activeForm: "Discovering..."})
TaskCreate({subject: "Plan feature", activeForm: "Planning..."})
TaskCreate({subject: "Implement tasks", activeForm: "Working..."})
TaskCreate({subject: "Verify implementation", activeForm: "Verifying..."})
TaskCreate({subject: "Review with specialists", activeForm: "Reviewing..."})
TaskCreate({subject: "Capture solutions", activeForm: "Compounding..."})
```

Set up `blockedBy` dependencies between phases (sequential).

Run COMPOUNDING phase on COMPLETED to capture solved problems in `.claude/solutions/`.
Suggest `/ha:document` for docs and `/ha:learn-from-fix` for quick pattern capture.

## Cycle Limits

| Setting | Default | Description |
|---------|---------|-------------|
| `--max-cycles` | 10 | Max plan→review cycles |
| `--max-retries` | 3 | Max retries per task |
| `--max-blockers` | 5 | Max blockers before stopping |

Stop with INCOMPLETE status when limits exceeded. List remaining work and recommended action.

## Integration

```text
/ha:full = /ha:plan → /ha:work → /ha:verify → /ha:review → (fix → /ha:verify) → /ha:compound
```

Use Ralph Wiggum Loop for fully autonomous execution:

```bash
/ralph-loop:ralph-loop "/ha:full {feature}" --completion-promise "DONE" --max-iterations 50
```

## Iron Laws

1. **NEVER skip verification** — Every task must pass the dev loop (`ruff format` → `ruff check --fix` → `mypy homeassistant/components/<domain>/` → `python3 -m script.hassfest --domain <domain>`) before moving to the next. Run `pytest tests/components/<domain>/test_<module>.py` per-phase, full component suite (`pytest tests/components/<domain>/ --cov=homeassistant.components.<domain> --cov-report term-missing`) only at final gate
2. **Respect cycle limits** — When `--max-cycles` is exhausted, STOP with INCOMPLETE status. Do not continue indefinitely hoping the next fix works
3. **One state transition at a time** — Follow the state machine strictly. Never jump from PLANNING to REVIEWING — each state produces artifacts the next state needs
4. **Discover before deciding** — Always run DISCOVERING phase to assess complexity. Skipping it for "simple" features leads to underplanned implementations
5. **Agent output is findings, not fixes** — Review agents report issues. Only the WORKING state makes code changes
6. **Skip redundant review agents** — In REVIEWING phase: skip
   verification-runner (work phase already verified), skip iron-law-judge
   if PostToolUse hooks verified all files. For <200 lines changed,
   spawn only python-reviewer + config-flow-reviewer (if `config_flow.py`
   touched) + security-analyzer (if auth/secret handling touched)
7. **ZERO narration in autonomous mode** — This is a HARD rule, not
   a suggestion. NEVER write "Let me now...", "Now I need to...",
   "I'll now...", "Next, I will...", or any preamble before a tool
   call. Just call the tool. Only output text for: decisions that
   need explanation, errors, or phase transitions. If you catch
   yourself narrating, delete the text and just make the tool call.
   (Post-PR validation: 30% of messages still violated this — the
   instruction was too soft. This stronger wording is required.)

## References

- `${CLAUDE_SKILL_DIR}/references/execution-steps.md` — Detailed step-by-step execution
- `${CLAUDE_SKILL_DIR}/references/example-run.md` — Example full cycle run
- `${CLAUDE_SKILL_DIR}/references/safety-recovery.md` — Safety rails, resume, rollback
- `${CLAUDE_SKILL_DIR}/references/cycle-patterns.md` — Advanced cycling strategies
