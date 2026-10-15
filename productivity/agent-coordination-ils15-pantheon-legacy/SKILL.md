---
name: agent-coordination
description: "Multi-agent orchestration with model routing, category delegation, and sprint management. Use for coordinating Pantheon agents."
context: fork
globs: []
alwaysApply: false
---

# Agent Coordination

Master guide to orchestrating the multi-agent system. Includes category routing, model selection, and sprint management for rapid, TDD-driven feature development.

---

## Agent Hierarchy

See `AGENTS.md` for the full agent table.

---

## Category Routing

Route tasks to optimized agents based on category instead of specifying agents manually:

| Category | Agent | Use For |
|----------|-------|---------|
| **Deep** | Athena, Hephaestus | Complex planning, AI pipelines |
| **Quick** | Talos, Apollo | Fast fixes, codebase search |
| **Ultrabrain** | Zeus | Multi-agent orchestration, model routing |

---

## Sprint Workflow

```
1. User describes feature
2. @athena creates PLAN with phases and agents
3. User approves PLAN (GATE 1)
4. Zeus dispatches agents to phases (parallel when possible)
5. Each agent: TDD cycle → writes IMPL artifact
6. @themis reviews all phases (GATE 2)
7. User reviews Themis findings
8. If approved → user commits (GATE 3)
9. @mnemosyne updates memory bank
```

---

## Parallel Execution Declaration

```
🔀 PARALLEL EXECUTION — Phase 2
Running simultaneously:
- @hermes   → backend tests   → .tmp/IMPL-phase2-hermes.md
- @aphrodite → frontend       → .tmp/IMPL-phase2-aphrodite.md
- @demeter  → migrations      → .tmp/IMPL-phase2-demeter.md
Themis reviews all three after completion.
```

---

## Artifact Protocol

All phase outputs go to `.pantheon/memory-bank/.tmp/`. See `skill: artifact-management` for the complete protocol (who generates what, templates, lifecycle).

---

## Safety Gates

| Gate | When | Why |
|------|------|-----|
| **GATE 1** | After PLAN | User confirms scope |
| **GATE 2** | After Themis review | User sees changes |
| **GATE 3** | Before git commit | User controls history |

---

## Model Selection

Model routing is handled by Prometheus and the platform configuration. Zeus delegates model selection to the tier system (`fast` / `default` / `coding` / `premium`).

- **Deep tasks** → High-quality models (Claude, GPT-4)
- **Quick tasks** → Fast/cheap models (Haiku, 4o-mini)
- **Visual tasks** → Multimodal models (GPT-4V, Claude Vision)
- **Cost optimization** → Route to cheapest model that meets quality bar

---

## Anti-Patterns

- ❌ Zeus doing implementation work (orchestrates, doesn't code)
- ❌ Skipping TDD cycle (RED → GREEN → REFACTOR)
- ❌ Auto-committing without user approval
- ❌ Parallel phases with dependencies (order matters)
- ❌ Ignoring Themis CRITICAL findings
