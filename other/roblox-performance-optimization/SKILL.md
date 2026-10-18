---
name: roblox-performance-optimization
description: Analyze and optimize Roblox scene and script performance. Use for mobile frame rate, memory, instance count, rendering cost, physics, particles, lighting, asset budgets, streaming, leaks, and using the rbx-scene-analysis workflow.
---

# Roblox Performance Optimization

## Goal

Keep the experience smooth on lower-end phones. Favor measurable fixes over visual guesses.

## Use The Scene Analysis Skill

When available, invoke `rbx-scene-analysis` before deep performance work. Use it to inspect rendering, memory, instance composition, unparented instances, and animation or audio asset usage.

## MCP Workflow

1. Confirm Studio state with `get_studio_state`.
2. Use `search_game_tree` and `inspect_instance` to identify heavy hierarchies.
3. Use `execute_luau` for targeted counts, tag scans, memory snapshots, or property audits.
4. Use `screen_capture` to preserve before/after visuals.
5. Playtest with `start_stop_play` and check `get_console_output`.

## Optimization Targets

- Instance count and deeply nested hierarchies.
- Unanchored parts causing physics cost.
- Excessive constraints, touched events, or per-frame loops.
- Large textures, too many unique materials, and high-poly meshes.
- Particle emitters with high rate/lifetime combinations.
- Dynamic lights, shadows, post-processing, and expensive transparency.
- Scripts that connect events repeatedly or leave stale connections.
- Workspace content that should stream or load later.

## Mobile Budget Habits

- Build the first area to be visually strong but technically cheap.
- Prefer fewer meaningful effects over many constant effects.
- Use Level of Detail thinking for distant props.
- Keep UI lightweight and avoid per-frame layout work.
- Test phones and tablet-like viewport sizes, not only desktop Studio.

## Report Format

Return:

- Biggest performance risks.
- Evidence from scene analysis, instance inspection, console output, or captures.
- Fixes ranked by likely player impact.
- Verification steps and any tradeoffs.

## Next

Confirm the gains on-device with `roblox-mobile-playtest`, and re-run `roblox-playtest-qa` to make sure nothing regressed.

