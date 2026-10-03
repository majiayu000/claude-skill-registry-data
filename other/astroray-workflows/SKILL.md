---
name: astroray-workflows
description: Run Astroray's existing package, verification, lint, rebuilding, visual-check, reporting, and opencode-delegation workflows from Codex without duplicating their canonical instructions.
---

# Astroray workflow bridge

The detailed workflow definitions remain canonical in `.claude/skills/`. Read
the relevant `SKILL.md` in full before acting; do not fork its policy here.

| Goal | Canonical workflow |
| --- | --- |
| Route a package or run the orchestrator | `dispatch-next` or `roadmap-orchestrator` |
| Implement or ship a package | `pkg-ship` |
| Delegate bounded work to opencode | `delegate` |
| Run hygiene, rebuild, or hardware checks | `lint`, `rebuild-pyd`, or `verify` |
| Inspect images or cite an algorithm | `visual-check` or `cite-algorithm` |
| Plan/review or update reports | `architect`, `strategy-review`, `run-report`, `close-round`, or `file-followup` |

Each named workflow resides at `.claude/skills/<name>/SKILL.md`. Use
`astroray-index` first when ownership or an existing script is unclear. The
delegate wrapper resolves opencode models from its tier policy at runtime;
never hard-code a model name in a workflow prompt or hook.
