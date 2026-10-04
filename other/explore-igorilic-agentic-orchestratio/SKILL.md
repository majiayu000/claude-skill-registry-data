---
name: explore
description: >
  Exploratory mode — spike, prototype, brainstorm. Throwaway code
  under spikes/. Use when the goal is to learn or generate options,
  NOT to ship. Pairs with the explorer agent.
  Triggers on: explore, spike, prototype, experiment, sketch, try out.
disable-model-invocation: true
---

## /explore <topic>

Exploratory track — first-class alternative to the production pipeline.
Use when you want to learn, prototype, or compare approaches without
the spec/todo/test ceremony.

```
/explore <topic>
  ↓
explorer (Sonnet)
  ↓
spikes/<topic>/  ← throwaway code (gitignored)
  ↓
spikes/<topic>/FINDINGS.md  ← what was learned + recommendation
  ↓
hand back to user (re-enter via /plan to promote findings)
```

### Usage

#### Claude Code (interactive)
```
Use the explorer agent to spike <topic>
```

#### Copilot CLI
```bash
copilot --agent=explorer --prompt "Spike <topic>"
```

### What goes under `spikes/`
- `spikes/<topic>/` — prototype code, scratch files, anything throwaway
- `spikes/<topic>/FINDINGS.md` — what was learned, recommendation
- Path is gitignored by default (add `spikes/` to `.gitignore`)

### Rules
- Spike-only commits bypass the TDD gate (banner shown)
- Touching files outside `spikes/` re-engages the gate
- Findings DO NOT auto-promote to production — re-enter via `/plan`

### When NOT to use
- You already know the design — go straight to `/plan`
- You're fixing a bug — use the production pipeline (or troubleshooter)
- The work needs to ship today — spikes are not shippable
