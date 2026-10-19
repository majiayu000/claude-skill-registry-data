---
name: navigation-pathfinding
description: "Use for reusable navigation pathfinding recipes in software and coding-agent work."
---

# Navigation & pathfinding — recipes (generic tier)

On-demand recipes (2). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Use A* over greedy, with total OOB/unexplored handling and a node cap
`generic`

Always use A* for grid navigation, never greedy/best-first, which detours and dead-ends around walls and oscillates forever between two cells each closer on a different axis; A* has no per-tick directional choice so it eliminates oscillation structurally (in alpha_cog cogs-v-clips this cut max stuck-ticks 5875 -> 11 and closed the largest tournament gap, so a sky-high max-stuck stat signals navigation, not strategy, is the bottleneck). Treat out-of-bounds queries as impassable WALL (keeps the search total, avoids scattering bounds checks). Match A*'s unexplored-tile assumption to the policy's: if the policy treats unexplored as passable, A* must too. Use a Manhattan heuristic with a tie-breaking counter for determinism, and cap node expansions to bound per-tick cost (alpha_cog uses 10,000) -- but a cap set below what a real path needs makes A* silently give up even when a path exists (a 30,000 cap failed on a path needing ~92,000 expansions), so confirm reachability with an UNCAPPED BFS and compare expansion count to the cap before blaming the map.
  <sub>sources: claude-code:27984094-3b9e-4e67-92c5-da2a61ceb32a, codex:019e031e-f7d3-7342-a7d9-96993bc91097, claude-code:19ac76fb-7c48-44a1-81dd-eebcbdc9c19c, opencode:ses_1ff24a65cffeJSXwU2v6gcXbHQ (+6)</sub>

#### 2. Give every action a success condition, retry budget, and state-changing exit
`generic` · ⚠ _session-derived, unverified_

Give every action/task a success condition, a bounded retry budget, and a clean failure that hands control back with fresh state. An action with no success signal, no timeout, and no fallback becomes an infinite no-op loop (example: a task pressed a button every other tick for 300+ ticks because its success detection was broken and it never saw completion). A 'complete' flag that does not change the next decision creates a re-entry loop — if a meta-decider re-selects the same state because its inputs are unchanged, ensure completing a state changes observable state or the decider's inputs. A no-op fallback on a transient degraded state traps the agent in dead time if the no-op does nothing to recover — prefer an active escape/recovery action. Make a reflex's cooldown at least as long as the behavior it triggers, or the cooldown expires mid-behavior and the reflex re-fires before finishing.
  <sub>sources: claude-code:3b14ac5a-1d66-4524-94c0-59a48466d223, claude-code:067e7439-cbd1-4b26-9b3f-d054bde3aa40, claude-code:0919285d-1374-4827-b596-6e7107d95526</sub>
