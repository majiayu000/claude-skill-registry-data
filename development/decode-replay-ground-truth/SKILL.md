---
name: decode-replay-ground-truth
description: Use when decoding a Crewrift replay for authoritative deaths, survival, movement, roles, tasks, or rewards.
---

# Decode replay ground truth (replay_mine oracle)

The authoritative answer to "what actually happened in this episode" comes from
**re-simulating the recorded replay**, not from telemetry. `replay_mine.nim` loads the
recorded `.bitreplay(.z)` / `.z` replay, decompresses it (zippy), rebuilds the game
config, and replays the recorded inputs tick-by-tick through a real `initSimServer`.
Because roles and deaths are **input + seed driven**, the reconstruction reproduces them
exactly — that is why it is an oracle and not an estimate.

Do NOT infer death / survival / movement from:
- live telemetry (player artifacts, notsus traces),
- the **crewborg `trace.db`** matched observer (its `game_over.alive_by_color` is
  UNRELIABLE — the trace ends mid-meeting and mismatched authoritative kills in 36–53 of
  60 episodes), or
- server **`results.json`** (a matched observer; fine for `scores`/`win`/`kills` per
  seat, but the per-slot diedTick/dist oracle lives only here).

The tool in this package is `universal/tools/replay_mine.nim` (see its `.note.md`). It is
the canonical copy of the `_crewrift-0136` branch oracle. It imports `./replays` and
`./sim` relatively, so **it must be built inside a live crewrift repo checkout**, not in
this package.

---

## Step 1 — get the replay URL for the episode

Replays are public S3 objects, zlib/zippy-compressed.

- **Known job_id** (from a memory note or a prior run): the URL pattern is
  ```
  https://softmax-public.s3.amazonaws.com/replays/{job_id}.z
  ```
- **From an experience-request**: `GET {server}/v2/experience-requests/{xid}` →
  each `episodes[]` entry carries `id` (`ereq_…`), `job_id`, `participants[]`, and a
  ready-to-use `replay_url` (the public S3 URL). Use `replay_url` directly.

Important: **only experience-request episodes return a downloadable `replay_url`.**
League-round (non-experience-request) replays are NOT available via API
(`/v2/episode-requests` 404s) — those are watchable only in the softmax.com Observatory
web UI. So always confirm cruxes via experience-request episodes, which DO return a
replay you can decode here.

Download it:
```bash
curl -fSL "https://softmax-public.s3.amazonaws.com/replays/{job_id}.z" -o /tmp/ep.z
# or, from an xreq detail:
curl -fSL "<replay_url from episodes[].replay_url>" -o /tmp/ep.z
```

Tip: the artifact-harvesting launcher `universal/tools/antfarm_run.py` saves
replay + results + logs per episode into `episode_NN/` folders, so if you already ran it
the `.z` is on disk. (NOTE: that launcher is SUPERSEDED — it emits the pre-rework xreq
body and 422s until patched to the unified `roster` shape per the
`crewrift-xreq-roster-api-change` memory note. If you only need the replay URL, hit
`GET /v2/experience-requests/{xid}` directly instead.)

---

## Step 2 — build replay_mine inside the live crewrift repo

`replay_mine.nim` imports `./replays` and `./sim`, so build it where those sibling
modules and the `data/` dir live — the crewrift repo's `src/crewrift/`.

```bash
# Copy this package's canonical copy into the live repo's src dir, then build:
cp /Users/daveey/packages/crewrift-player-optimization/universal/tools/replay_mine.nim \
   <CREWRIFT_REPO>/src/crewrift/replay_mine.nim
cd <CREWRIFT_REPO>
nim c -d:release src/crewrift/replay_mine.nim
```

`<CREWRIFT_REPO>` is the live crewrift checkout. (session-derived, unverified) In recent
sessions that checkout was the `_crewrift-0136` branch dir,
e.g. `~/code/crewrift/_crewrift-0136`; confirm the actual path before building. If the
repo already has its own `src/crewrift/replay_mine.nim`, build that one — it's the same
oracle.

---

## Step 3 — run it against the replay

Run with **cwd = the crewrift repo** so it finds `data/`.

```bash
cd <CREWRIFT_REPO>
./src/crewrift/replay_mine /tmp/ep.z /tmp/ep.csv 2>/dev/null
```

- **Arg 1** = the replay file (`.bitreplay`, `.bitreplay.z`, or the `.z` from S3).
- **Arg 2** (optional) = output CSV path. **Always pass it when scripting** — with an out
  path it writes a CLEAN CSV to that file, kept separate from the sim's stdout noise.
  With NO second arg it writes the CSV to **stderr** (and stdout still carries sim noise),
  so a no-arg run is for eyeballing, not parsing.
- `2>/dev/null` drops the sim's stderr noise. The tool also prints a full
  kill / vote / meeting log to **stdout** during the replay — keep stdout if you want that
  event log; redirect or ignore it if you only want the CSV.

---

## Output CSV schema

One row per slot, exactly `config.minPlayers` rows (the seated players):

```
slot,role,reward,tasks,alive,diedTick,dist
```

| column     | meaning |
|------------|---------|
| `slot`     | 0-based player index — matches the seat order you passed images / roster entries to run-episode. |
| `role`     | `crew` / `imposter`, seed-deterministic. |
| `reward`   | final per-player score (the leaderboard input). |
| `tasks`    | tasks rewarded. (May diverge harmlessly from the live run — see gotchas.) |
| `alive`    | survived to end (`true`/`false`). |
| `diedTick` | **`-1` = survived**, otherwise the integer tick of death. |
| `dist`     | total Manhattan distance traveled (accumulated per tick from position deltas) — a movement / activity / positioning proxy. |

`diedTick` + `dist` are exactly what the `crewrift-perception-presence-not-recall` and
`crewrift-leaderboard-gap-diagnosis` notes mean by "replay-decoded": presence-at-kill,
isolation, and victim-link diagnoses all ground out in these columns.

To find YOUR tested policy's row: the slot is the seat you placed it in. To cross-check
against `results.json` (`GET {server}/observatory/jobs/{job_id}/artifacts/results`, whose
length-8 arrays are slot-indexed, slot i = seat i), match your
`policy_version_id` against `participants[].position` / `participants[].policy_version_id`
from the xreq detail to recover the seat index.

---

## Gotchas

- **Build location is load-bearing.** `replay_mine.nim` uses relative imports
  (`./replays`, `./sim`) and the sim needs `data/`. Build it inside the crewrift repo's
  `src/crewrift/` and run with cwd = that repo. Building it standalone in this package
  fails to resolve imports.
- **diedTick `-1` means SURVIVED**, not "died at tick -1". Filter `diedTick >= 0` for
  actual deaths.
- **`tasks` / `reward` may diverge harmlessly** from the live run (the tool's own header
  flags this). `role`, `alive`, and `diedTick` are seed/input-exact and are what you trust
  for who-died / who-survived. Use `reward` for relative scoring, not as a byte-exact match
  to the live leaderboard.
- **No second arg → CSV on stderr.** If you forget the out-path and parse stdout, you'll
  parse sim noise. Always pass `out.csv` when scripting.
- **Wrong S3 path 403/404s.** The bucket is `softmax-public`, prefix `replays/`, suffix
  `.z`. League-round replays simply don't exist at that route — use an experience-request
  episode's `replay_url`.
- **Slots vs. colors.** This CSV is slot-indexed (seat order). The crewborg trace
  resolves color↔role but is a different (and for who-died, unreliable) observer — don't
  cross slots and colors without the `role_resolved` mapping.
- **A sibling `replay_ambush.nim` / `replay_pos.nim` exists** for other extractions
  (kill-log, per-tick x/y/alive/role for all 8 slots at any sample rate). This
  `replay_mine` emits the compact `diedTick/dist/role/reward` CSV — pick the tool that
  emits the column you need rather than assuming one binary has everything. The position
  variant is built the same way (import `./sim`, `./replays`; dump per-tick tracks).

---

## Success check

You have the oracle output when:
1. `/tmp/ep.csv` exists and its header is exactly `slot,role,reward,tasks,alive,diedTick,dist`.
2. It has `config.minPlayers` data rows (typically the seated count, e.g. 8).
3. `role` values are `crew`/`imposter` and the imposter count is plausible (not all-crew).
4. `diedTick` is `-1` for survivors and a positive tick for the dead, and the count of
   `diedTick >= 0` rows matches the kill/vote log the tool printed to stdout.

If `role` is empty, all rows show `diedTick = -1` on a known-lethal game, or the run
errored on a missing `data/` path, you built/ran outside the crewrift repo — redo Step 2
with cwd = the live repo. If the download 403/404s, you used a league-round job_id or the
wrong S3 prefix — re-fetch `replay_url` from an experience-request episode.
