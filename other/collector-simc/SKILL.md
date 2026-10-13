---
name: collector-simc
description: "MythiStone data collection and SimulationCraft: the leaderboard collector and its smoke-tested Docker image, simc builds and chunked BiS runs, talent loadout encoding, keystone.guru route API limits. Use when editing collect*/fetch*/simc* scripts, Dockerfile, entrypoint.sh or the collector/simc image CI."
---

# Collector SimC domain

## Gotchas

Before changing a file listed below, read its gotcha: `ref/<id>.md` in this skill (or `kb_gotcha <id>`).

| id | rule | files |
|---|---|---|
| `collector-smoke-test` | The collector image is pushed only after a runtime smoke test passes, and that test must change together with the collector's runtime contract | `backend_scripts/collectLeaderboardData.py`, `entrypoint.sh`, `Dockerfile`, `backend_scripts/simcBis.py`, `.github/workflows/buildCollectorImage.yml` |
| `keystone-route-api-limits` | The keystone.guru route API gives only npc_id (creature type) + enemyForces per pull, so per-run pack/position/route-consensus analytics are permanently impossible | `backend_scripts/collectLeaderboardData.py`, `backend_scripts/generateDungeonPages.py` |
| `loadout-v2-encoder` | The talent loadout encoder in commonUtils is used only by the local seeder, and only SimulationCraft can prove its output valid | `backend_scripts/commonUtils.py`, `backend_scripts/localDev/*` |
| `pov-video-collection-funnel` | What a raider.io POV video has to pass before it is stored and shown on a streamer or VOD page, and how to find out where a missing one was dropped | `backend_scripts/collectLeaderboardData.py`, `backend_scripts/generateVodsPage.py` |
| `simc-baseline-vs-page-gear` | Why the simcBis baseline gear can legitimately differ from the spec page's displayed equipped items, and why not to "fix" it | `backend_scripts/simcBis.py` |
| `simc-chunked-checkpoint` | A simc BiS run outlives the collector container, so its chunk timeout is tied to the container restart interval and to the single core docker-compose gives simc | `backend_scripts/simcBis.py`, `docker-compose.yml` |
| `simc-resilient-build` | simc builds validate-and-walk-back over commits instead of trusting raw HEAD, and the gate must SIMULATE a real fight (not just init) | `backend_scripts/simcWalkback.sh`, `backend_scripts/validateSimc.sh`, `backend_scripts/buildResilientSimc*.sh`, `.github/workflows/buildSimcImage.yml`, `.github/workflows/buildPages.yml`, `Dockerfile.simc` |
