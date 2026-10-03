---
name: dispatch-next
description: Read the current Round's recommended deployable set, pick the top-priority open package not already in flight, and route it to the correct agent.
invocation: /dispatch-next
---

# /dispatch-next

Read `.astroray_plan/docs/NEXT_STAGE_REPORT.md` §2 (Recommended next
deployable set). Identify the highest-priority open package that does not
already have an open PR or an active worktree.

## Routing rules

0. **Tier check (cost routing).** Before spawning the `package-implementer` agent, decide
   whether the package qualifies for open-model delegation via the `delegate`
   skill (`implement` tier — see `.claude/skills/delegate/SKILL.md`):
   - Qualifies: well-specified small fix or mechanical change with crisp
     acceptance criteria, no novel physics/sampling, no ABI-surface changes,
     full build+pytest+lint gate applies downstream.
   - Does NOT qualify: novel algorithm integration, anything the spec marks
     ambiguous, BSDF/integrator/light-transport math, ABI-touching headers.
   If it qualifies, dispatch through `delegate --tier implement --agent worker`
   in the worktree and have the parent (you) verify evidence + run gates.
   When in doubt, route to `package-implementer` (open-weight) as before.

1. Otherwise spawn the `package-implementer` subagent in a fresh worktree
   (create it with `git worktree add` per the agent's worktree discipline —
   there is no `EnterWorktree` under opencode). Codex is supported again
   (2026-09-05) as a CLI second-opinion reviewer (Terra/Luna via
   `codex exec`), never as an implementer or orchestrator; legacy `Track: E`
   / `Codex-paste-ready` tags in spec frontmatter remain inert and route
   here too.

2. Pass to the spawned agent:
   - The drop-in prompt from NEXT_STAGE_REPORT.md §3 for that package
     (verbatim — those prompts are purpose-written)
   - The package spec path
   - The worktree name (e.g., `pkg55-phase-b`)

3. DRY-RUN mode: if invoked with `--dry-run`, print the routing decision
   (package name, agent, worktree) without spawning the agent.

## Example output (non-dry-run)

```
Dispatching: pkg55 Phase B → package-implementer
Worktree: .claude/worktrees/pkg55-phase-b
Prompt: [NEXT_STAGE_REPORT.md §3.1 verbatim]
```
