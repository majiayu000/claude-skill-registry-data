---
name: roblox-quest-progression-systems
description: Design and implement Roblox quests, achievements, collections, unlocks, prestige, daily/weekly goals, progression pacing, reward claims, and objective tracking. Use for short-term and long-term goals tied to retention.
---

# Roblox Quest Progression Systems

## Goal

Give players clear short-term wins and long-term reasons to return.

## Progression Layers

- Immediate: first reward, first upgrade, first objective complete.
- Session: quest chain, zone unlock, collection progress.
- Multi-day: daily streak, weekly challenge, Day 7 reward.
- Long-term: prestige, mastery, rare collections, leaderboards, social status.

## Quest Design

- Use objectives that reinforce the core loop.
- Show current objective and next reward in the HUD.
- Avoid vague objectives that require menu hunting.
- Reward every cycle, but reserve big unlocks for meaningful milestones.
- Unlock new content near the 2-3 hour mark to fight the Day 3 wall.

## Implementation Rules

- Track canonical quest progress on the server.
- Validate all client-reported actions against server state.
- Separate objective definitions from player progress.
- Make reward claims idempotent.
- Save progress through DataStore-backed profile state.

## MCP Workflow

1. Search for quest/progression scripts and UI.
2. Read definitions, progress mutation, reward, and save scripts.
3. Inspect objective markers and reward UI instances.
4. Patch with `multi_edit` or targeted `execute_luau`.
5. Playtest a full quest loop and check console output.

## Output

Return:

- Progression ladder.
- Objective definitions.
- Reward and claim flow.
- Save requirements.
- Day 1, Day 3, and Day 7 retention impact.

## Next

Tune the reward pacing with `roblox-economy-balancing`, persist progress with `roblox-datastore-persistence`, and verify claims cannot be spoofed with `roblox-security-economy`.

