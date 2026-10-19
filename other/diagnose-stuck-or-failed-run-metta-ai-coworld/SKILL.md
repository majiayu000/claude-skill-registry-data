---
name: diagnose-stuck-or-failed-run
description: Use when classifying a stuck, failed, empty, or zero-scoring evaluation as infrastructure or policy failure.
---

# Diagnose a stuck or failed eval run (infra vs policy)

The reflex when a run looks dead is to blame the policy and revert, or to assume a
crash and resubmit. Both are usually wrong. The vast majority of "dead run" signals
are **infra**, not the policy. This recipe classifies the failure first.

**Golden rule (evidence discipline):** only a TERMINAL, completed round with real
per-player scores is policy evidence. Pending / submitted / claimed / running rounds,
empty logs, and rounds that fail before a player process starts are **non-evidence**.
Never replace a champion or revert a policy from non-terminal or failed-before-startup
rounds alone.

---

## Step 0 — Identify which symptom you have

Match your situation to a branch, then run that branch's checks:

| Symptom | Branch |
| --- | --- |
| Detached/background eval logfile is empty or stuck; "is it dead?" | A — Empty/buffered log |
| A submit printed a JSON decode error or "failed" — about to resubmit | B — uv preamble corrupts JSON |
| Round stuck `pending` / `running` forever; hosted dispatch not picking up | C — Backend / dispatch |
| Empty division leaderboard, or `coworld results` crashed | D — Empty leaderboard trap |
| Round reached terminal `failed`, or completed with zero/garbage scores | E — Failed/zero terminal round |
| A `422` on submit, or fields the server rejects | F — API shape drift |

Don't skip ahead. Each branch ends with a classification (INFRA or POLICY) and a
success check.

---

## Branch A — Empty / buffered detached log ("is my run dead?")

A long-running Python eval launched detached (`nohup`, background, output redirected
to a file) **block-buffers stdout**: the logfile stays empty until the process exits,
even while the run is healthy and working. An empty log is NOT failure evidence.

Before declaring it crashed, check liveness and side-effects (in order, cheapest first):

1. **Process is alive:**
   ```bash
   ps -p <PID>
   ```
   Alive → it is buffering, not dead. Stop here unless other signals contradict.

2. **Side-effect artifacts exist:** the eval writes a run directory as soon as the
   submit succeeds and the poll loop starts. A created run dir = submit succeeded and
   the loop is running. Check the run-dir tree (per-xreq folder with `episode_NN/`
   subfolders + a `summary.json` for the `antfarm_run.py` artifact path).

3. **Live docker container count** (local docker path only):
   ```bash
   docker ps -q | wc -l
   ```
   A non-zero, structured count means games are running. (Session-derived example: 54
   containers = 6 concurrent games × 9 containers each.) (session-derived, unverified)

4. **Query the server for the request's status directly** rather than trusting the log
   — poll the experience-request / round status via the API (see Branch C for the
   status check). The server is the source of truth, not the buffered file.

**The fix (so this never recurs):** force unbuffered stdout in the eval/diagnostic
script — `PYTHONUNBUFFERED=1`, or `python -u`, or
`sys.stdout.reconfigure(line_buffering=True)`. Apply this even to throwaway diagnostic
scripts; the same mistake recurs there. (session-derived, unverified)

**Long-running watches:** run a continuous watch loop via the **Monitor** tool with an
until-loop, NOT a detached Bash shell with a long foreground `sleep` — the detached
shell gets reaped mid-sleep and the watch dies silently. The `monitor.py` tool (the
standalone league rank/round watcher) is the reference pattern for "always-on,
print-only-on-change". (session-derived, unverified)

**Classification:** process alive OR artifacts present OR server says running →
**INFRA (buffering), run is healthy.** Do not resubmit, do not revert. Wait for
terminal status or query the server.

---

## Branch B — A submit "failed" with a JSON decode error (uv preamble)

`uv run` writes an install/sync **preamble to stdout**, which intermittently corrupts
machine-parsed JSON output. A CLI whose JSON you pipe into a parser will throw a JSON
decode error even though **the underlying command SUCCEEDED** — only the parse failed.

Do this:

1. **Do NOT resubmit on a parse error.** The submit may have created the request.
   Resubmitting double-submits. (Session-derived: three consecutive "failed" submits
   had all actually been created.) (session-derived, unverified)

2. **Verify server/queue state before any resubmit** — query the experience-request /
   round list and confirm whether your request already exists (see Branch C status
   check). Only resubmit if the server has no record.

3. **Fix the invocation:** when a CLI's JSON must be parsed, invoke the project's venv
   python directly instead of through `uv run`:
   ```bash
   .venv/bin/python <script> ...
   ```
   This skips the `uv` preamble so stdout is clean JSON.

**Classification:** parse error with a created request on the server → **INFRA (uv
preamble), submit succeeded.** Not a policy or backend failure.

---

## Branch C — Round stuck pending / running / dispatch not picking up

First, decide the **execution backend**. For crewrift experience requests,
`execution_backend="k8s"` is the dependable hosted path. **antfarm is slow-dispatch and
unreliable** — measured ~61% episode failure rate, a ~60s/episode cold-start floor, and
multi-hour outages; a matched probe had k8s complete 4/4 in 239s while antfarm sat
~243s pending then failed all 4 on 502/read-timeout. **If you have a choice, use k8s.**

The A/B eval engine (`eval.py` → `league_eval.run_league_ab` / `run_arm`) already
encodes a formula-derived timeout budget and a wedge detector — let it run rather than
declaring failure early:

- **Total arm budget:** `~ num * maxticks/24 * 3 + 900` seconds. Games run at realtime
  sim pacing (TargetFps 24), so a fixed short timeout falsely fails slow-but-healthy
  episodes. One episode at `maxTicks 10000` ÷ 24 ≈ 7 minutes wall time; episodes
  parallelize fully server-side, so the budget is dominated by the longest single
  episode + warm-up, not `num` × episode-time.
- **Wedged-participant detection:** if ZERO episodes complete within
  `maxticks/24*3 + 600` seconds, a participant is wedged — fail LOUD. `run_arm` does
  this with `stall_grace_seconds` (transient statuses `404/425/429/5xx` are retried;
  zero completions past the grace = declared wedged). Poll cadence ~10s.

Status-probe a stuck round / request directly:

1. **Poll the experience-request to terminal** via `GET`/list on `/v2/experience-requests`
   (the parent) and its child episodes. A status of `submitted`/`claimed`/`running` is
   non-evidence — keep waiting up to the budget above.
2. **If on antfarm and "stuck running":** the episode may have already finished. Hit the
   antfarm episode worker's own `/healthz` and `/results`. `status=finished` + `404`
   results = the game completed but emitted no artifacts (a **game-side gap**, not
   slowness). (session-derived, unverified)
3. **antfarm "pending forever" / registration:** antfarm rejects any roster containing a
   policy version with no antfarm registration row ("Policy version ... is not registered
   with Antfarm"), and top-N/league selection is NOT registration-aware, so it picks
   unregistered policies and fails at dispatch. **k8s has no such requirement** — the
   fastest fix is to re-run the same roster on k8s. (Registration names embed
   `sha256(policy_version_id)[:12]` as a suffix; if you must stay on antfarm, intersect
   the registrar's public `/list` with live league memberships to compute the
   dispatchable set, then pin all seats explicitly.) (session-derived, unverified)
4. **Routing quirk:** prod Observatory dispatches antfarm jobs to antfarm **staging**
   workers; use **prod** (not a local backend) for antfarm requests. A completed run with
   `live_url=None` ran on **k8s**, not antfarm (only antfarm dispatches carry a
   `live_url`) — don't count a k8s success as antfarm proof. (session-derived, unverified)
5. **Disambiguate an outage with controls:** run a known-good simple game on antfarm
   (tells antfarm-wide vs game-specific) and run the same roster on k8s (tells
   antfarm-specific vs systemic).

**Classification:**
- Within budget, status pending/running → **INFRA (still working), wait.**
- Past wedge grace with zero completions → **INFRA (wedged participant / backend), fail
  loud and re-run on k8s.** Not policy.
- antfarm down but k8s completes the same roster → **INFRA (antfarm).** Switch to k8s.

---

## Branch D — Empty leaderboard / `coworld results` crash

An **empty division leaderboard does not mean an empty division.** The leaderboard only
shows SCORED champions, so 0 rows can coexist with a populated division (observed: 0
leaderboard rows alongside `member_count=10`; a champion-eligibility pool of 5 while the
broader competing-membership pool held 136). This is the trap that makes server-side
`top_n` champion auto-fill silently fail to fill a 7-seat field even though plenty of
runnable opponents exist.

Do this:

1. **Do NOT infer "no eligible opponents" from an empty leaderboard.** Check membership
   counts and the live-membership pool **separately** — the `softmax_pull.py` tool
   already surfaces division leaderboards, rounds, and submissions from the endpoints
   that work today (and coerces a null leaderboard to `[]`), so use its
   `fetch_softmax(league_id)` path for the outcome side rather than reading the
   leaderboard alone.
2. **`coworld results <division_id>` (0.1.16) CRASHES on an empty leaderboard:** the API
   returns null and the client validates against `list[LeaderboardEntryPublic]`
   (pydantic "Input should be a valid list"). Divisions with entries work fine.
   **Workaround:** `coworld memberships --mine` to check a qualifying bot's status.
   (Filed as Metta-AI/coworld issue #11.) (session-derived, unverified)
3. This is most common on a freshly-entered division (e.g. Qualifiers right after a
   submission), before any round has scored.

**Classification:** empty leaderboard with a non-empty membership pool → **INFRA /
expected state, not a dead division.** Don't dismiss `top_n` or conclude "no opponents".

---

## Branch E — Failed / zero-score terminal round (the revert trap)

A hosted round that comes back `failed` or with zero/garbage scores is **often a
runtime/infra failure, not a policy regression.** Documented cases where reverting the
policy would have been wrong:

- **Auth crash before any player starts** (e.g. `KeyError: 'authorization'` / missing
  in-cluster auth). No player ran → the round is **zero policy evidence.**
- **Game-image route/version mismatch:** the worker requested one client path while the
  deployed game image served a different one → the round `404`s. Packaging/infra skew,
  not a policy bug.
- **Recorder error** like "results contain N scores for M stored policy versions" →
  points at round recording / runtime state; reproduces even on a fresh upstream
  reference bot, so it is not your policy.
- **Teardown race:** the episode finished and the server was ready to write
  `results.json`, but a player process stayed blocked in websocket teardown and had to
  be force-killed. If the player's process timeout is too short, the player disconnects
  **before** the server records the round → no usable results even though game logic
  completed. (And the runner-side image gate's own timeout must be long enough that a
  `results.json` arriving just after a stingy deadline isn't discarded as a runner
  timeout.)

The classification procedure:

1. **Confirm a player actually started and produced a score** before blaming the policy.
   Inspect the per-episode-request record, the downloaded artifacts
   (`results.json` + game logs + per-agent policy logs — the `antfarm_run.py` harvest
   path pulls all of these into `episode_NN/` folders), and any submission dry-run notes.
2. **No player process started** (auth/route/recorder error before startup) → **INFRA,
   non-evidence.** Do not revert.
3. **Player started but disconnected during teardown / no results despite completed game
   logic** → **INFRA (teardown race).** The fix is operational, not a policy revert:
   wrap the player's run command in a GNU `timeout` with a **generous** duration and
   `--kill-after`, and MAP the timeout exit code to **success** — a player reaped after
   the game is done is normal lifecycle, not a failure. Set the timeout comfortably
   longer than a full episode (tens of seconds disconnected players before results were
   written; minutes fixed it). This is `try/finally`-style lifecycle handling, not
   error-swallowing.
4. **Only if** a TERMINAL round with **real per-player scores** shows the regression,
   reproduced across enough rounds, is it **POLICY evidence.**

**If the live policy genuinely is broken:** fix it operationally — upload a clean
replacement and let the new placement de-champion the old version — rather than adding a
backward-compat shim for an obsolete import path.

**Classification:** failed/zero round with no started player or a teardown race →
**INFRA, non-evidence.** Real per-player scores reproducing a regression → **POLICY.**

---

## Branch F — `422` on submit / API shape drift

Conform to the **deployed** server's OpenAPI, not your local client models — the request
shape drifts. `POST /v2/experience-requests` was reworked on **2026-06-12** to a unified
`roster` body (one entry per seat, `policy_ref`). The old `requester`/`opponents` /
`policy_version_ids` / `top_n` / `target` shape now **422s**.

- The league A/B path (`eval.py` → `league_eval.build_request_body`) is already on the
  post-rework shape: the seat is pinned **inside** the `requester` object
  (`requester.slot`) — the server rejects a top-level `requester_slot` supplied next to a
  `requester`.
- `antfarm_run.py` (`build_request`) still emits the **pre-rework** shape and will 422
  until patched to the unified `roster` body. Re-fetch live members and validate every
  pvid right before launch; the league rolls policy versions mid-session.

**Classification:** a `422` on submit → **INFRA (API shape drift).** Patch the request
body to the deployed schema; not a policy failure.

---

## Success check (you are done when)

You can state, for the specific run, **one** classification with the evidence that backed
it:

- **INFRA** — and you named the cause (buffering / uv preamble / antfarm down / empty
  leaderboard / auth-before-startup / teardown race / API drift) and took the infra
  action (wait, query server, switch to k8s, fix invocation, patch body, raise the player
  `timeout`). You did **not** revert or replace the policy on this evidence.
- **POLICY** — and you have a TERMINAL completed round (or A/B verdict) with **real
  per-player scores** that reproduces the regression across enough rounds to clear the
  verdict bar. Only then is reverting / re-uploading justified.

If you cannot produce a terminal round with real scores, the answer is INFRA-or-unknown,
and the run is **not** policy evidence — do not touch the policy.
