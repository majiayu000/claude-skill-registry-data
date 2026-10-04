---
name: game-production
description:
  "Coordinate an authorized game-production task from its saved GameGen brief through a playable slice, asset reviews
  and integration. Use for multi-stage game work or resuming it."
---

# Coordinate game production

Read [shared context](../../references/shared-context.md) and the ready project preferences through
`scripts/prefs.py read`. Use [repository contracts](../../references/repository.md) for paths, ownership and asset
records. If setup is incomplete, route to game-bootstrap once.

Translate `game.goal` into the player's objective and `game.scope` into this delivery's boundaries. Preserve accepted
art direction and gameplay decisions. A new instruction steers the current task unless it explicitly replaces it.
Inspect current files and evidence before treating inherited work as complete.

## Select only the needed workflows

| Work                                           | Skill                                         |
| ---------------------------------------------- | --------------------------------------------- |
| Visual direction and construction views        | game-concept-art                              |
| 3D sources and exports                         | blender-game-assets                           |
| Pixel, painted, cutout or rendered sprites     | game-sprites                                  |
| Terrain tiles and adjacency rules              | game-tilesets                                 |
| Skeletal, cutout or frame animation            | game-animation                                |
| Gameplay and persistence                       | godot-gameplay                                |
| Levels, camera, lighting and 2.5D presentation | game-world-building                           |
| Interface and cross-device input               | game-ui-input                                 |
| Sound, music and action effects                | game-audio-vfx                                |
| Procedural music and SFX (`local` audio route) | game-audio-procedural, through game-audio-vfx |
| Gameplay and visual verification               | game-qa                                       |
| Measured runtime optimization                  | game-optimization                             |
| Packaged delivery                              | game-export                                   |
| Trailers, gameplay videos and GIFs             | game-trailer                                  |

Load only the selected skill and its relevant references. Provider skills are dependencies for the selected service, not
replacements for the game brief or GameGen preferences.

## Build a representative slice

Choose a small end-to-end experience that proves the core loop: an actor or controllable object, one environment or
screen, one meaningful interaction/challenge, feedback and completion/recovery. Set observable success criteria from the
brief. Use a small asset review scene to validate the art and animation before generating the whole cast or environment
library.

Follow the configured concept and asset review policy. Prepare a concrete image/model/engine capture for user review;
under agent review compare against the approved references and record the selected revision. Resolve silhouette and
camera readability before expensive detail. Keep rejected revisions only when useful for recovery, outside the engine
import tree.

## Parallel work and resumption

Delegate only when authorized by the current task and available tools, within `workflow.parallel_agents` and the host
limit. Use concrete independent assignments with exclusive file ownership. Serialize preferences, shared scenes, asset
manifests, spend reservations and live-editor mutations. Give workers the same preferences revision and an explicit
import/controller contract. Reconcile contract changes before integration.

Each handoff includes readiness, changed files, generated IDs/metadata, verification and blockers. Use the existing
tracker or a compact state file, with one scoped task when sufficient. Do not turn ordinary implementation into a
documentation exercise. Maintain job IDs and reservations across turns so a retry or context reset does not duplicate
expensive work.

Integrate and verify the slice before scaling content. Finish with actual playable behavior and evidence appropriate to
the delivery scope. Make the distinction between working code, visual interpretation, measured performance and
target-platform readiness explicit.
