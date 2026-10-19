---
name: env-toolchain
description: "Use for Crewrift-specific env toolchain recipes when optimizing a player."
---

# Environment & toolchain — recipes (crewrift tier)

On-demand recipes (1). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Run Crewrift locally via Nim+nimby; its local config differs from tournament, and teardown must be server-first
`crewrift`

To run Crewrift locally without Docker: install Nim and sync the lockfile (`nimby use 2.2.10; nimby sync -g nimby.lock`), start the server with COGAME_HOST/COGAME_PORT/COGAME_CONFIG_URI pointing at the repo config.json via `nim r src/crewrift.nim`, build the example bot `nim c players/notsus/notsus.nim`, and run at least 8 bots each connecting to ws://localhost:2000/player?slot=$i&token=$token. The local config.json deliberately differs from tournament: maxGames 1 with a kill cooldown of 100 ticks (SHORTER than the manifest default of 500, so local kill-cooldown timing does NOT match tournament when tuning imposter aggression); a fixed deterministic 8-slot roster of 6 crew + 2 imposters with slots 6 and 7 always imposters (pink/orange); and non-secret placeholder dev tokens (do not treat as secrets, but do not reuse the pattern for hosted sessions). Stop the game server BEFORE killing agent clients to dodge an upstream cleanup bug: killing clients with pending whispers first makes Sim.tickWhispers clear pendingWhisperEntry on an already-disconnected player and crash. A standalone bot with its own reconnect loop is more resilient for long runs than a multi-process launcher that propagates a GUI flag to all children and kills all of them when any one exits.
  <sub>sources: bitworld/among_them/players/mod_talks/DESIGN.md, bitworld/among_them/players/mod_talks/LLM_SPRINTS.md, coworlds/coworld-crewrift/README.md, coworlds/coworld-crewrift/config.json (+1)</sub>
