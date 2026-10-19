---
name: generate-a-crux
description: Use when finding and statistically confirming a reproducible Crewrift crux before changing the policy.
---

# Generate a crux

A **crux game** is a config (map + role assignment + field) where a specific rival
policy reproducibly beats your policy at a **fixed role and seat**. A crux is the only
honest justification for a behavior change: it isolates a single, reproducible deficit
you can diff on replays. A leaderboard gap is NOT a crux — most "losses" in the
standings are role-assignment / field / seed variance that vanish when you reconstruct
and re-run. Confirm before believing.

## Two crux sources (different reproducibility)

1. **A real LEAGUE round** you scored badly in (or a rival topped). The API does NOT
   expose the round's original seed. You can only rebuild the round's FIELD from its
   participants' *current live* pvids and pin a FRESH seed. You are reproducing the
   matchup, not the exact game.
2. **Your OWN past experience-request episode.** The exact config — INCLUDING the seed
   — is known and re-runnable. This is a **swap tournament**: re-run that exact config
   once per candidate rival swapped into YOUR seat, all arms in parallel, and
   Wilson-compare each rival arm against your original score.

Source 2 is strictly stronger (deterministic config). Prefer it when you have an own
low-scoring episode.

## Constants and identifiers (inline — do not look them up)

- Crewrift league id: `league_605ff338-0a2e-4e62-aeda-559df9a9198f`
- Manifest default seed: `679961`. `sim.nim` calls `initRand(config.seed)`, so a pinned
  `seed` makes map + task assignment + role assignment deterministic. This is THE crux
  reproducibility lever.
- A standard arm = 8 seats: 1 forced-role tested seat + 7 league opponents.
- Wilson z = 1.96 (95% CI). `harness_core.wilson(k, n)` returns `(p, ci_low, ci_high)`.
- Target sample: **n=30 per arm** for a single-config probe; pool across related configs
  to clear Wilson at small per-config n (see Pooling below).

## Tools this recipe drives

All shipped in `../../tools/` (the package `universal/tools/` dir; in the live repo
they live in `_harness/`, run as `uv run python _harness/<tool>.py`).

- **`eval.py`** — the league-faithful A/B CLI. One forced-role seat for the tested
  policy, 7 top league players fill the rest. Prints win-rate + Wilson CIs. Use this
  for the league-round source and as the canonical verdict path.
- **`league_eval.py`** — the engine `eval.py` calls (`run_league_ab`); both arms run
  concurrently server-side. Use its functions directly when you script a swap
  tournament (one arm per swapped rival).
- **`league_roster.py`** — `live_members(client, league_id=...)` returns all live
  members ranked by best recent round score (rows: `player_id`, `player_name`, `label`,
  `policy_version_id`, `score`); `fetch_top_players(...)` returns the top-N opponent
  pvids excluding yourself. This is how you reconstruct a field and pick candidate
  rivals to swap in.
- **`harness_core.py`** — `wilson(k, n)`, `forced_imposter_slots(seed, ...)`,
  `slot_role_config(...)` for the seed-deterministic forced-role layout.
- **`metrics.py`** — offline per-episode diagnosis (`uv run python _harness/metrics.py
  <run_dir> [--candidate <substr>] [--json]`): win-rate, vote accuracy, where score is
  lost. Use AFTER a crux is confirmed to diff WHY the rival wins.
- **`antfarm_run.py`** — artifact harvester (downloads results.json + replays per
  episode) when you need raw logs for deep diagnosis. NOTE: this copy emits the
  pre-2026-06-12 request shape and will **422** until patched to the unified `roster`
  body — `eval.py`/`league_eval.py` are already patched, prefer them.

## Recipe

### Step 0 — pick the source and the seat to fix

Decide role (`crew` or `imposter`) and that you are fixing it. The requester's role is
chosen by *picking a seat of that role* in the seed-deterministic layout, not by
editing the layout. `eval.py` does this for you via `requester_slot_for_role(role,
seed)`.

### Step 1A — LEAGUE-ROUND source: reconstruct the field, pin a fresh seed

You cannot recover the round's seed. Rebuild the matchup:

1. Get live members and identify the round's top scorer / the rival you lost to. Resolve
   them to a **current live** `policy_version_id` — stale pvids from old round results
   are rejected as not-runnable, and bare player names with >1 live version are rejected
   as ambiguous:
   ```python
   import league_roster
   from coworld.api_client import CoworldApiClient
   client = CoworldApiClient.from_login()
   members = league_roster.live_members(
       client, league_id="league_605ff338-0a2e-4e62-aeda-559df9a9198f")
   # find the rival row, take members[i]["policy_version_id"]
   ```
2. Run the A/B with YOUR policy as `--baseline`, the rival as `--candidate`, your fixed
   role, a pinned fresh seed, and the league top-7 filling the field:
   ```bash
   uv run python _harness/eval.py \
     --baseline <your-policy-label> \
     --candidate <rival-policy-label-or-pvid> \
     --role crew --num 30 --top-n 7 \
     --game-config seed=679961   # pin a FRESH seed; vary it across a small set, see Step 3
   ```
   `--candidate`/`--baseline` must be owned, uploaded policy labels; pass the rival as a
   live pvid via `--opponent <pvid>` seating if it is not one of your owned policies.

### Step 1B — OWN-EPISODE source: build a swap tournament (session-derived, unverified)

You have an own past experience-request episode (a config + seed your arm scored low
in). Turn it into a multi-comparator crux:

1. Recover the exact `game_config_overrides` from that episode's request record,
   **including its `seed`** and any forced-slots config. This config is re-runnable
   verbatim.
2. For each candidate rival (the round's top players, from `live_members`), construct ONE
   arm that re-runs that exact config with the rival's pvid swapped into YOUR seat, every
   other seat unchanged. Run all rival arms (plus a re-run of your original) **in
   parallel** — each is a separate single-roster-entry request. `league_eval.run_arm` /
   `run_league_ab` is the concurrent submit/poll engine; the recon-sweep controller in
   the source sessions ran ~20 arms in flight (`tmp/crux/recon/sweep.py`,
   session-derived, not a shipped universal tool).
3. Wilson-compare each rival arm's win/score against your original arm.

### Step 2 — pin determinism correctly

- Pin `seed` via `--game-config seed=<int>` (arbitrary keys pass through; verified keys
  include `seed`, `tasksPerPlayer`). To force imposter SEATS explicitly on top of the
  seed, set `imposterCount: 2`, `autoImposterCount: false`, and a `slots` array of
  per-seat `{"role": "crew"|"imposter"}` (the `_harness` `forced_slots_config`).
- **Deterministic-bot caveat:** if a pinned seed makes every episode literally identical
  (1 distinct outcome across all 30), that collapses to **n=1** statistically. Detect
  this (all 30 results equal) and SPREAD the trial over a small set of distinct crux
  seeds instead of re-running one. The source sweep caught two deterministic
  seed-artifacts this way — one tier5c-favorable seed hid a real optimizer crux until
  reseeded. **Always reseed any arm with ≤1 distinct outcome.**

### Step 3 — optional: isolate the button mechanic (imposter cruxes)

If a strong IMPOSTER rival is the suspected crux, run its arm twice with identical
seed/field/seat: once default, once with `--game-config buttonCalls=0` (this is the
ONLY accepted key — `numberOfButtonCalls`/`maxButtonCalls`/`buttonCallsPerGame` all
HTTP-400). If the edge survives `buttonCalls=0`, it's learnable behavior (an actionable
crux). If it vanishes, the edge is the one-per-game button mechanic — feeds the
"press build" lane, not a behavior fix.

### Step 4 — read the verdict and confirm with Wilson

`eval.py` prints, per arm: `wins/n`, win-rate `p`, and the 95% Wilson CI. A confirmed
crux requires the **rival's Wilson CI to separate strictly ABOVE yours (non-overlapping
intervals)** at your fixed role/seat.

- **Non-overlapping, rival above you ⇒ CONFIRMED CRUX.** File it (see Success check)
  with a who-does-better table so the implementer knows which rival to study and on
  which replays.
- **Overlapping or you ahead ⇒ NOT a crux at this n.** Either pool more (Step 5) or
  record "hard map / variance, not a crux" and stop spending cycles on that config.

### Step 5 — pooling (how small real deficits clear Wilson)

A single config at n=30 often overlaps. Pool a **same-direction** deficit across related
configs (same rival, several reconstructed rounds / several crux seeds) and run Wilson on
the pooled k/n. The confirmed optimizer crux was pooled 167/540 (you, 0.31 [0.27,0.35])
vs 228/540 (rival, 0.42 [0.38,0.46]) — non-overlapping only after pooling; single rounds
inside that pool overlapped. Do NOT pool opposite-direction results (that's just
averaging away signal). If pooling at large n stays overlapping, it is variance — drop
it (the source sweep ran some rivals to n=630 and they stayed inconclusive; those are
NOT cruxes).

## Gotchas

- **Reconstruct before believing a standings gap.** Most top-of-leaderboard "losses" do
  NOT reproduce. In the source sweep, ONLY one rival (crewborg-optimizer) reproducibly
  beat the baseline at crew-slot-0; truecrew, crewborg-aaln, jernau, sussyboi/RowDaBoat
  all tied or lost on reconstruction. The #1-by-floor leader topped ZERO of 26 rounds —
  its rank was mean-floor consistency, not head-to-head skill. A high leaderboard rank is
  not evidence of a crux.
- **Seat-verification in swap tournaments (session-derived, unverified):** a comparator
  that ALSO appears in your standard field-of-7 shares its pvid across two seats and
  can't be seat-verified by unique pvid. In that case opponents land in LIST ORDER —
  verify the swapped seat by `episodes[].participants[].position`, not by matching pvid.
- **Re-validate every pvid right before launch.** The league rolls policy versions
  mid-session; a pvid valid an hour ago may be stale. Re-fetch `live_members` /
  `client.list_memberships(active_only=True).entries` immediately before each submit.
- **Empty Competition division:** server-side `{"player": {"top_n": 7}}` auto-fill draws
  ONLY from the Competition-division champion pool, which is empty today (all play is in
  Qualifiers), so it returns too few opponents and 400s. Use the explicit `policy_ref`
  roster path (not champion-restricted) ranked by `league_roster` recent-round scores
  instead. `{"player": {"random": true}}` draws WITH replacement (can dup, including your
  own champion into an opponent seat) — fallback only.
- **Watch long runs with the Monitor tool, NOT a backgrounded Bash sleep.** A detached
  shell with a long foreground `sleep` gets reaped and the poller dies silently
  (0-byte logfile, arms finish server-side, no verdict). Poll with Monitor + an
  until-loop.
- **`antfarm_run.py` 422s** on the current server (pre-rework request shape). Use
  `eval.py`/`league_eval.py` for arms; only reach for `antfarm_run.py` after it is
  patched to the unified `roster` body, and only when you need the raw replay/log
  download for diagnosis.

## Success check

You have generated a crux when:

1. The rival's Wilson CI separates **strictly above** yours at the fixed role/seat
   (single config or pooled), AND
2. Any arm with ≤1 distinct outcome was reseeded (no n=1 seed-artifact), AND
3. The deficit is BROAD/reproducible, not one favorable seed.

Then record it for implementation: the rival, your fixed role/seat, the
config(s)/seed(s), the pooled k/n and CIs, the per-episode replay ids, and a one-line
who-does-better summary. (In the source workflow these were filed as Asana "Crux Games"
tasks; file wherever your team tracks crux work.) If no rival's CI separates above you
after pooling, record "not a crux — variance/hard map" and stop — that is also a
successful outcome (it saves implementation cycles).
