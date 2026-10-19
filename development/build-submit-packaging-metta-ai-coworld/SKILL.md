---
name: build-submit-packaging
description: "Use for Crewrift-specific build submit packaging recipes when optimizing a player."
---

# Build, package & submit — recipes (crewrift tier)

On-demand recipes (3). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Crewrift configs and the nav bake pipeline ordering; use the full scoring config, verify games via the replay
`crewrift`

For a crewrift quality signal use the full Among Them config (8 players, 2 imposters, 8 tasks/player, 1200 kill-cooldown ticks, 600 vote-timer ticks, 10000 max ticks, ~120 role-reveal, ~360 game-over, mirrored from bitworld_among_them_8p_2imposters); smoke/certification configs that zero tasks and tick budgets are unusable for quality. Crewrift's certification (smoke) variant uses tasksPerPlayer 1, startWaitTicks 0, roleRevealTicks 0, gameOverTicks 1, maxTicks 300, voteTimerTicks 120, HUD arrows/bubbles off; use it for fast deterministic real-replay capture (pass --save-replay/--save-scores, synthesize episode metadata yourself — the game does not write it; a time-limit draw replay exercises the no-winner render branch). Among Them's canonical tournament variant runs 8 players with exactly 2 imposters and 8 tasks/player at 24 FPS (6000 ticks = 250s). The nav bake has STRICT prerequisite ordering that silently breaks if reordered: walk_mask.bin (derived from upstream assets) must exist before waypoint editing; the nav graph JSON the editor produces must exist before the path-baker computes per-edge costs and the packed nav_paths.bin; gate the re-bake on reporting zero failed/unreachable edges. League episodes can return empty game_stats/policy_results even though games ran, so confirm a real game by decompressing the replay (zlib-compressed as replay.json.z; zippy is a dependency) and checking it is a valid ~41 KB CREWRIFT replay.
  <sub>sources: claude-code:10f74020-e0e6-4515-8d0c-f071d41766ad, claude-code:25488cd9-61d5-4231-bd87-e2744b6db043, claude-code:48add98e-a83d-4348-97bf-0079c48c42d6, claude-code:63658f66-83c7-482e-a805-d58527e10975 (+6)</sub>

#### 2. Pin CREWRIFT_REF centrally and keep it matched to the live league; record the engine version per submission
`crewrift`

Pin the crewrift game version centrally in crewrift_lab/tools/versions.env (CREWRIFT_REF), passed as a --build-arg to every Nim player build, and keep it matched to the game version running in the league you target: a player compiled against a different game version can skew from live behavior (the same version-skew that breaks expand_replay). CREWRIFT_REF cannot be auto-resolved (the platform exposes no commit and master runs ahead of :latest), so bump it deliberately when build_expand_replay starts hash-failing on fresh replays (the redeploy signal). Record the engine version a submission was built against, since smoke-config and protocol details (tick counts, frame format) are version-specific; building against a cached older among_them image is acceptable when the newer cannot be pulled (e.g. v0.1.20 used because v0.1.24 returned a ghcr.io 403).
  <sub>sources: personal_labs/crewrift_lab/docs/designs/building_players.md, coworlds/coworld-crewrift/README.md</sub>

#### 3. The crewborg publish path: amd64 build, upload-policy, submit, live-resolved league id
`crewrift` · ⚠ _session-derived, unverified_ · tool: `coworld`

The crewborg publish/submit path is: Docker build as linux/amd64, then `coworld upload-policy`, then `coworld submit`. Resolve the Crewrift league id LIVE (e.g. 'Crewrift Daily', or the current 'game-of-week') rather than trusting stale/memory-noted ids, and upload a new version under the EXISTING policy name (e.g. v4 over active v3). New submissions land in the Qualifiers division with status qualifying. Run the player's pytest suite and `ruff check` before uploading; the Dockerfile's `FROM --platform=linux/amd64` triggers an expected lint warning that is not a build failure.
  <sub>sources: codex:019e8fc7-ebad-7b00-bc95-df1727641ce0, codex:019eaea8-4f78-7072-b4b0-539df963b7df</sub>
