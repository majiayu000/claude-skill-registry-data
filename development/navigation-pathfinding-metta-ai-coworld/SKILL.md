---
name: navigation-pathfinding
description: "Use for Crewrift-specific navigation pathfinding recipes when optimizing a player."
---

# Navigation & pathfinding — recipes (crewrift tier)

On-demand recipes (2). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Keep interaction gates on true geometry and surface missing anchors at startup
`crewrift` · ⚠ _session-derived, unverified_

After changing navigation TARGETS to baked anchors, leave the completion/trigger condition unchanged on the true game geometry (task-rect containment, vent center within VentRange) so the game still accepts the action. Keep a runtime fallback build path for tests/custom maps: default runtime loads the prebaked asset, but unit tests and experiments lazily build a small synthetic graph from a supplied walkability sprite, guarded so a caller supplying a custom map does not silently inherit the default prebaked graph. If any task/vent/button has no reachable anchor, log it at build time (frame 1): a missing anchor that fails silently mid-episode looks like the agent freezing, whereas a startup warning is diagnosable.
  <sub>sources: claude-code:962c8ab4-4ea3-4aaa-9f6d-20ea3cfce003, codex:019eaee5-b54e-79f2-bf0f-ac59a6a1eae2</sub>

#### 2. Plan role-specific navigation up front: ghosts skip A*, vents are imposter-only by construction
`crewrift`

Plan role-specific nav special cases up front rather than bolting them on -- a single uniform nav layer that ignores role misbehaves. Ghosts fly directly toward goals and are NOT constrained by the walk mask, so route them straight to goal (no A*). Imposters need belief-state-gated vent usage (vent only when no witnesses present); make vent-teleport traversal imposter-only BY CONSTRUCTION by adding the directed teleport edges between same-group vent anchors to the SHARED nav graph but only letting an imposter 'escape' intent traverse them, so crewmate routes are never affected by their presence.
  <sub>sources: bitworld/among_them/players/how_to_make_a_bot.md, bitworld/among_them/players/SMART_BOT_GUIDE.md, personal_labs/crewrift_lab/crewrift/crewborg/design.md, opencode:ses_204495c66ffe7u8C8SOiEX1zdH</sub>
