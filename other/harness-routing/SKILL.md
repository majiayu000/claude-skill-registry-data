---
name: harness-routing
description: Use when choosing workflow/tooling across Pi, Claude Code, Supacode, model roles, delegation, subagents, background agents, or worktrees.
---

# Harness Routing

Route work to the lowest-overhead workflow that preserves the right safety boundary. This skill is a local overlay for shared/upstream skills; do not edit vendored skills just to add harness policy.

## Routing rules

1. **Identify the active harness.** Do not infer Pi from `command -v pi`; use the actual conversation/runtime context.
2. **Choose the surface.** Use Supacode for repo/worktree/tab organization. Use the current agent session for normal single-threaded work. Use Pi tidy subagents or Claude Code native subagents only when delegation clears the threshold.
3. **Choose the model deliberately.** Use Pi's current model and thinking controls; keep concrete model IDs out of shared skills.
4. **Choose delegation only when it pays.** Inline is default. Delegate for broad independent research, fresh-context review, independent hypothesis checks, or approved worktree-scoped execution.
5. **Preserve the active model during delegation.** If the user explicitly chose a provider or model, keep subagents on it unless they ask for a different harness or model. Do not silently route Pi tidy subagents to Claude bridge or another provider.

## Harness modes

- **Pi:** use `@mobrienv/pi-tidy-subagents` (`subagent` / `subagent_control`) for justified foreground/background delegation. Keep children read-only unless the user approved writes, use separate worktrees for parallel writes, and preserve an explicitly selected provider/model.
- **Claude Code:** use native Claude Code subagents/worktrees when appropriate.
- **Other/default:** avoid harness-specific features unless the current runtime explicitly supports them.

## Upstream skill overlay

If a vendored skill says “background agent”, “subagent”, or “parallel agents”, translate that through the current harness:

- Pi → inline by default; tidy subagents only when justified.
- Claude Code → native subagents/worktrees when justified.
- Unknown → sequential inline unless the user explicitly approves another mechanism.

Completion criterion: the next action names the selected harness path, or explicitly says no special routing is needed.
