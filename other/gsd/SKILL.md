---
name: gsd
description: Get Shit Done (GSD) — spec-driven development system. Use this when the user invokes any /gsd-* command or wants to plan, build, verify, or ship features using the GSD workflow. Routes to the appropriate GSD skill in .agent/skills/.
---

# GSD — Get Shit Done (Gateway)

> ⚠️ **MANDATORY FOR EVERY TASK:** Load `.agents/skills/tac-express-onboarding/SKILL.md` first, then `.agents/skills/tac-express-rules/SKILL.md`. The Fourteen Laws are non-negotiable and enforced by ESLint + CI. Any code that violates them will be blocked at commit time.

GSD v1.34.2 is installed at `.agent/skills/`. All 68 GSD skills are available.

## Quick Command Reference

### Core Workflow
| Command | When to use |
|---------|------------|
| `/gsd-map-codebase` | First time — map existing codebase before new project |
| `/gsd-new-project` | Initialize GSD: questions → research → requirements → roadmap |
| `/gsd-discuss-phase [N]` | Lock in implementation preferences before planning |
| `/gsd-plan-phase [N]` | Research + create plans + verify for a phase |
| `/gsd-execute-phase <N>` | Execute all plans in parallel waves |
| `/gsd-verify-work [N]` | Manual UAT with auto-diagnosis |
| `/gsd-ship [N]` | Create PR from verified work |
| `/gsd-next` | Auto-detect and run the next logical step |

### Quick Tasks
| Command | When to use |
|---------|------------|
| `/gsd-quick` | Ad-hoc task with GSD guarantees (atomic commits) |
| `/gsd-fast <text>` | Trivial inline task — no planning overhead |
| `/gsd-debug [desc]` | Systematic debugging with persistent state |

### Navigation
| Command | When to use |
|---------|------------|
| `/gsd-progress` | Where am I? What's next? |
| `/gsd-resume-work` | Restore full context from last session |
| `/gsd-help` | Show ALL commands with descriptions |

## tac-express GSD Config

When `/gsd-new-project` creates `.planning/config.json`, it should include:

```json
{
  "mode": "interactive",
  "granularity": "standard",
  "model_profile": "inherit",
  "planning": {
    "commit_docs": true
  },
  "workflow": {
    "research": true,
    "plan_check": true,
    "verifier": true,
    "ui_phase": true
  },
  "agent_skills": {
    "gsd-executor":         [".agents/skills/tac-express-onboarding", ".agents/skills/tac-express-rules", ".agents/skills/tac-express-stack", ".agents/skills/tac-express-conventions", ".agents/skills/tac-express-ui"],
    "gsd-planner":          [".agents/skills/tac-express-onboarding", ".agents/skills/tac-express-rules", ".agents/skills/tac-express-stack", ".agents/skills/tac-express-conventions"],
    "gsd-phase-researcher": [".agents/skills/tac-express-rules", ".agents/skills/tac-express-stack"],
    "gsd-ui-researcher":    [".agents/skills/tac-express-rules", ".agents/skills/tac-express-ui", ".agents/skills/tac-express-stack"],
    "gsd-verifier":         [".agents/skills/tac-express-rules", ".agents/skills/tac-express-stack"],
    "gsd-plan-checker":     [".agents/skills/tac-express-rules"],
    "gsd-code-reviewer":    [".agents/skills/tac-express-rules", ".agents/skills/tac-express-conventions"],
    "gsd-auth-worker":      [".agents/skills/tac-express-auth", ".agents/skills/tac-express-rules"]
  }
}
```

## Skill Storage

- **GSD system skills** → `.agent/skills/gsd-*/SKILL.md` (68 skills, backward-compatible path)
- **Project skills** → `.agents/skills/tac-express-*/SKILL.md` (new Antigravity default path)
- **GSD agents** → `.agent/agents/gsd-*.md`
- **GSD planning** → `.planning/` (created by `/gsd-new-project`)

## Recommended First Run for tac-express

This is a brownfield Next.js monorepo. Follow this sequence:

```
1. /gsd-map-codebase     ← scan stack, arch, conventions, concerns
2. /gsd-new-project      ← initialize with codebase map context
3. /gsd-discuss-phase 1  ← shape the first phase
4. /gsd-plan-phase 1     ← research + plan
5. /gsd-execute-phase 1  ← build
6. /gsd-verify-work 1    ← UAT
```
