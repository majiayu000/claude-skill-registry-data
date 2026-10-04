---
name: torque:migrate
description: "Evaluate whether to upgrade from Torque (GSD + Superpowers) to Meridian, and guide the migration if ready. Use when projects outgrow the routing model."
---

# Migrate to Meridian

Evaluate whether the current project would benefit from upgrading to [Meridian](https://github.com/mattjaikaran/meridian) and provide a migration path.

## What is Meridian?

Meridian is the standalone successor to Torque. Instead of routing between GSD and Superpowers, Meridian IS the system — a SQLite-backed state machine with 39 commands, deterministic resume, quality gates, and remote agent dispatch.

## When to Migrate

### Signals you've outgrown Torque

Run through this checklist. If 3+ are true, Meridian is the right move.

- [ ] **Session continuity is painful** — you lose context between sessions and `/gsd:resume-work` isn't enough
- [ ] **Multi-milestone project** — you've completed 1+ milestones and are starting another
- [ ] **Team coordination** — multiple people or AI agents need to work on the project
- [ ] **You want deterministic resume** — same state should produce the exact same prompt every time
- [ ] **You need board sync** — Linear, Jira, or similar needs to stay in sync with phases
- [ ] **Remote execution** — you want to dispatch plans to other machines or agents
- [ ] **Execution learnings** — you want the system to learn from failures and improve over time
- [ ] **You're fighting the routing** — GSD and SP conflict resolution is becoming overhead

### Stay with Torque if

- Project is simple (< 3 milestones expected)
- You like GSD and Superpowers separately and just need them coordinated
- You don't need persistent state beyond `.planning/` files
- Lightweight is a feature, not a limitation

## Migration Path

### Step 1: Install Meridian

```bash
git clone https://github.com/mattjaikaran/meridian.git ~/.claude/skills/meridian
```

### Step 2: Initialize in your project

```bash
# In your project directory
# Meridian will detect existing .planning/ and offer to import
```

Then run `/meridian:init` — it creates `.meridian/state.db` and imports existing state.

### Step 3: Map your workflow

| Torque (GSD + SP) | Meridian equivalent |
|-------------------|-------------------|
| `/gsd:new-project` | `/meridian:init` |
| `/gsd:discuss-phase` | `/meridian:discuss` |
| `/gsd:spec-phase` | `/meridian:discuss` (spec built-in) |
| `/gsd:plan-phase` | `/meridian:plan` |
| `/gsd:execute-phase` | `/meridian:execute` |
| `/gsd:verify-work` | `/meridian:verify-phase` |
| `/gsd:validate-phase` | `/meridian:verify-phase` (Nyquist built-in) |
| `/gsd:resume-work` | `/meridian:resume` (deterministic) |
| `/gsd:quick` | `/meridian:quick` |
| `/gsd:fast` | `/meridian:fast` |
| `/gsd:ship` | `/meridian:ship` |
| `/gsd:pr-branch` | `/meridian:pr-branch` |
| `/gsd:autonomous` | `/meridian:autonomous` |
| `/gsd:insert-phase` | `/meridian:insert-phase` |
| `/gsd:remove-phase` | `/meridian:remove-phase` |
| `/gsd:undo` | `/meridian:revert` |
| `requesting-code-review` | `/meridian:review` (two-stage) |
| `receiving-code-review` | `/meridian:review` (handles both sides) |
| `systematic-debugging` | `/meridian:debug` (with KB) |
| `/gsd:note` | `/meridian:note` |
| `/gsd:plant-seed` | `/meridian:seed` |
| `/gsd:session-report` | `/meridian:report` |
| `/torque:status` | `/meridian:status` or `/meridian:dashboard` |
| `/torque:next` | `/meridian:next` |

### Step 4: What you gain

- **Deterministic resume**: SQLite-backed, not file-based. Same state = same prompt.
- **Quality gates**: Regression gate, stub detection, coverage tracking — enforced, not suggested.
- **Two-stage review**: Spec compliance first, then code quality. Built-in, not bolted on.
- **Execution learnings**: System learns from failures and injects rules into future plans.
- **Debug knowledge base**: Resolved bugs persist and inform future debugging.
- **Board sync**: Connect Linear/Jira with a pluggable provider.
- **Remote dispatch**: Send plans to other agents for autonomous execution.
- **39 commands**: Everything Torque routes to, Meridian provides natively.

### Step 5: Clean up

After migrating, you can optionally remove Torque:
```bash
rm -rf ~/.claude/skills/torque
```

The `.planning/` directory is still valid — Meridian uses `.meridian/` alongside it.

## Output format

After evaluating the checklist:

```
## Migration Assessment

**Score**: 5/8 signals detected — Meridian recommended

### Signals detected
✓ Multi-milestone project (2 milestones completed)
✓ Session continuity issues (3 HANDOFF.md files found)
✓ Complex routing (both .planning/ and docs/plans/ present)
✗ No board sync needed
✗ No remote execution needed

### Recommendation
→ Install Meridian and run `/meridian:init` in this project.
   Your existing .planning/ state will be imported automatically.
```

## Rules

- Never modify any files. This is assessment-only unless the user explicitly asks to migrate.
- Be honest — if Torque is sufficient, say so.
- Always show the command mapping table so the user knows what changes.
