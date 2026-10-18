---
name: roblox-world-level-design
description: Design Roblox worlds, levels, hubs, zones, biomes, obbies, arenas, and exploration spaces. Use for spatial layout, landmarks, player flow, spawn design, objective placement, onboarding paths, traversal, sightlines, social spaces, performance-aware world layout, and guiding players without text.
---

# Roblox World Level Design

## Goal

Build spaces that guide players naturally, support the core loop, and feel good on mobile.

## Spatial Flow

Design for:

- Spawn facing the first objective or landmark.
- First action reachable within 10-30 seconds.
- Clear routes using shape, color, lighting, motion, and landmarks.
- Short loops that bring players back to rewards, upgrades, or social areas.
- New zones that visibly tease future goals.
- Safe space before challenge space.

## Landmarks And Readability

- Give each zone a readable silhouette and color identity.
- Use tall or distinct landmarks to orient players.
- Keep important interactables visually louder than decoration.
- Avoid clutter that hides objectives or enemies.
- Make paths understandable without walls of text.

## Gameplay Placement

Place:

- Objectives where players naturally look and move.
- Rewards immediately after effort.
- Shops and upgrades near loop return points.
- Social spaces where players can show progress.
- Bosses or challenges after preparation cues.
- Hidden secrets off the main path, not on the onboarding path.

## Performance-Aware Layout

- Stream or stage distant content when possible.
- Avoid over-dense prop clusters in the first playable area.
- Keep expensive particles, transparency, physics, and lights intentional.
- Use occlusion, terrain shape, and zone gates to control visual complexity.

## MCP Workflow

1. Inspect the world with `search_game_tree`, `inspect_instance`, and `screen_capture`.
2. Use `character_navigation` during Play mode to test routes and first-action time.
3. Use `execute_luau` for measurements, markers, or layout adjustments.
4. Playtest after layout changes and check `get_console_output`.

## Output

Return:

- Player path.
- Landmarks and guidance cues.
- Objective and reward placement.
- Social space plan.
- Mobile and performance risks.
- Playtest checks.

## Next

Check the layout's cost with `roblox-performance-optimization`, and confirm player flow and first-action clarity with `roblox-game-ux` and `roblox-playtest-qa`.
