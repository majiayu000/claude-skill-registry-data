---
name: health
category: healthcare
version: 0.12.0
primitive_candidate: P22  # not promoted; candidate per bstack-engine rule-of-three
description: Personal health knowledge graph — local-first ingest of Garmin (Apple Health, Whoop, Oura, CGM in v2+) traces into SQLite, projected to Obsidian daily-note frontmatter, synthesized into validated longevity-proxy metrics (HRV-CV, CTL/ATL/TSB, VO2max arc). Hex architecture so new sources drop in as adapters. NOT a coaching surface in v1.
author: broomva
license: MIT
tags: [health, garmin, apple-health, whoop, oura, hrv, training-load, vo2max, longevity, local-first, knowledge-graph]
compounding:
  - bookkeeping       # P6 — high-signal health insights promote into research/entities/concept/health-*.md via Nous gate ≥ 5/9
  - persist           # P12 — `persist iterate health-sync.md` for daily cron loop
  - telos             # GOALS.md / MISSION.md / MODELS.md cross-links (Attia/Galpin longevity frames)
trigger_keywords:
  - health, my health, sync garmin, garmin sync, garmin connect
  - training readiness, hrv trend, hrv-cv, recovery, sleep last night
  - vo2max, body battery, training load, ctl, atl, tsb, race readiness
  - my fitness, workout history, longevity, peter attia metric, andy galpin metric, stacy sims
  - daily health note, health dashboard, healthos
---

# Health — Personal Health Knowledge Graph

The Health skill turns your wearables into a **queryable, local-first knowledge graph** with validated longevity-proxy synthesis on top. It is a substrate, not a coach. The agent reads from it; the user reads the projections; humans interpret. v1 ships the Garmin adapter and the hex architecture that lets Apple Health, Whoop, Oura, and CGM drop in as single-file adapters with zero application-core changes.

This is the *substrate-shaped* answer to the questions "how did I sleep last night?", "am I overreached?", "what's my VO2max arc this year?" — answered against a trace store you own, not a vendor cloud.

---

## Setup (first run — installs all dependencies)

This skill is a Python package with a `health` CLI. **`npx skills add` copies
this manifest but does NOT install the CLI** — so, before the first `health`
command, ensure it's installed. This is the single step that pulls **all**
dependencies:

```bash
command -v health >/dev/null 2>&1 || bash "<this skill's dir>/install.sh"
```

`install.sh` (bundled alongside this `SKILL.md`) detects `uv` / `python3 ≥ 3.12`,
creates an **isolated venv**, installs `broomva-health` **with every dependency**
(pydantic, typer, rich, garth, …) plus the `[garmin]` extra, and symlinks
`health` onto your PATH. It is **idempotent** — safe to re-run; upgrades in
place; never touches global Python.

> **Agent:** if `command -v health` fails, run `bash <skill-dir>/install.sh`
> (resolve `<skill-dir>` to the directory containing this `SKILL.md`) **before**
> the first `health` command, then proceed. Re-run it after updating the skill.

---

## Agents (the reasoning layer)

This skill ships authored agents in [`agents/`](agents/) — prompts as versioned
data, released with the skill. `install.sh` links them into `~/.claude/agents/`,
so one install yields **CLI + skill + agent**.

| Agent | Invoke for | Tools |
|---|---|---|
| [`health-analyst`](agents/health-analyst.md) | "how did I sleep", "how's my recovery", "am I overreached", "what's my HRV trend", "summarize my last month" | `Bash`, `Read`, `Grep` |

**Invocation paths:** auto-delegation (the host agent routes on the spec's
`description`) · explicit (`Agent(subagent_type: "health-analyst", …)` or "use
the health-analyst agent") · parallel fan-out (one per metric domain) ·
scheduled (cron / `/loop`) for digests.

**The split that makes this work:** the skill is the *retrieval substrate*
(raw → structured → series → synthesis); the agent is the *reasoning layer*. An
agent reaches data **only** through the `health` CLI — never Garmin, never the
SQLite store — so ingest is never duplicated and every answer traces to a
command. It also keeps large reads (a `raw` dump over months) inside the
subagent's own context instead of the main thread.

> New agents are a one-file PR: add `agents/<name>.md`, and
> `tests/unit/test_agent_specs.py` pins the contract.

---

## When to invoke

Invoke this skill on any trigger in the frontmatter `trigger_keywords` list. The router is:

| User intent | Workflow | Command |
|---|---|---|
| "Where do I stand?" / health snapshot | [Status](Workflows/Status.md) | `health status` |
| "Pull my latest" / fresh data | [Sync](Workflows/Sync.md) | `health sync --source garmin` |
| "Backfill the last N months" / cold start | [Backfill](Workflows/Backfill.md) | `health backfill --source garmin --months 10` |
| "Today's daily note" | [DailyNote](Workflows/DailyNote.md) | `health daily-note` |
| "Am I overreached?" / training-load read | [TrainingLoad](Workflows/TrainingLoad.md) | `health synthesis` (CTL/ATL/TSB field) |
| "Recovery review" / 7-day rollup | [RecoveryReview](Workflows/RecoveryReview.md) | `health synthesis` (hrv_cv_30d + recovery_score) |
| "VO2max arc" / longevity check | [VO2maxArc](Workflows/VO2maxArc.md) | `health synthesis` (vo2max_arc field) |
| "Coach me / what should I do" | [Coaching](Workflows/Coaching.md) | **NOT IMPLEMENTED in v1** |

Default discipline: any health-domain conversation opens with `health status` (a P15 Snapshot reflex). The agent **never** answers a health question from training-data priors when the live trace store could answer it.

---

## Architecture

Five-layer hex, dependency arrow points inward:

```
cli/         ─→  application/  ─→  ports/  ←─  adapters/
                                                 ├─ sources/      (Garmin v1; Apple, Whoop, Oura, CGM ≥ v2)
                                                 ├─ repositories/ (SQLite default; SQLCipher v1.1)
                                                 ├─ projections/  (Obsidian daily-note; healthOS feed)
                                                 ├─ token_stores/ (filesystem default; Keychain optional)
                                                 ├─ rate_limiters/ (token-bucket)
                                                 └─ mfa/          (prompt / env / Keychain)
domain/      pure Pydantic v2 — sample shapes, metric registry, results, errors
synthesis/   derived views — HRV-CV, CTL/ATL/TSB, VO2max arc (stdlib-only)
migrations/  numbered SQL files + idempotent runner
config/      paths + settings (TOML + env, env wins)
```

- **domain** has zero I/O. It defines `QuantitySample`, `CategorySample`, `CorrelationSample`, `Workout`, `Device`, the `MetricCode` registry with canonical units, the `Source` enum, all `Result` types, and the `HealthError` hierarchy.
- **ports** are `Protocol`-typed seams: `TraceSource`, `TraceRepository`, `ProjectionTarget`, `RateLimiter`, `TokenStore`, `MFAProvider`, `Clock`.
- **application** holds the four v1 use cases: `SyncSourceUseCase`, `BackfillSourceUseCase`, `HealthStatusUseCase`, `RenderDailyNoteUseCase`. Each is a frozen dataclass with constructor-injected ports.
- **adapters** are the only place concrete dependencies live.
- **cli** wires concrete adapters into use cases at startup. The CLI is the *only* impure entry point.

This separation is what lets a new source (e.g. Whoop) drop in as a single file in `adapters/sources/` without touching anything else. The application layer never imports an adapter.

Deep-dive: [References/architecture.md](References/architecture.md).

---

## Workflows

| Name | Command | When | Output |
|---|---|---|---|
| **Status** | `health status` | P15 Snapshot reflex; entry to any health convo | `list[SourceStatus]` (token validity, last sync, rate budget) |
| **Sync** | `health sync --source garmin` | Foreground / cron; pulls since last sample ts | `SyncResult` (samples_ingested, workouts_ingested, duration_s) |
| **Backfill** | `health backfill --source garmin --months N` (or `--days N` / `--from YYYY-MM-DD`) | Cold start, after gap | `BackfillResult` |
| **DailyNote** | `health daily-note [--date YYYY-MM-DD]` | After successful sync | Path to `~/broomva-vault/07-Health/YYYY-MM-DD.md` |
| **Raw** | `health raw [--from D --to D] [--endpoint NAME]` | Agent needs a field the structured layer doesn't map | verbatim JSON per `(date, endpoint)` — lossless, uncapped |
| **Series** | `health series --metric M [--from D --to D] [--bucket B --agg A]` | Trend over time / processed view of one metric | structured time-series, raw or bucket-aggregated |
| **Synthesis** | `health synthesis [--on YYYY-MM-DD]` | Derived metrics over full history | `SynthesisSnapshot` (hrv_cv_30d, ctl, atl, tsb, vo2max_arc, recovery_score) |
| **TrainingLoad** | `health synthesis` → `ctl`/`atl`/`tsb` | When asking about freshness/fatigue | CTL, ATL, TSB — 42d/7d EWMA of Garmin per-activity training load |
| **RecoveryReview** | `health synthesis` → `hrv_cv_30d`/`recovery_score` | Weekly review; after illness | HRV-CV + recovery composite |
| **VO2maxArc** | `health synthesis` → `vo2max_arc` | Quarterly check; longevity tracking | `{quarter_key: mean_vo2max}` |
| **Coaching** | *(not implemented in v1)* | — | — |

Each workflow doc starts with a one-line **When invoked** rule and ends with example output. See `Workflows/*.md`.

---

## CLI surface

```bash
# Authentication
health auth login [--source garmin] [--profile NAME]   # one-time MFA login
health auth status [--source garmin]                    # token validity per source
health auth logout [--source garmin]                    # delete token bundle

# Sync & backfill
health sync [--source garmin] [--since ISO_DATETIME]   # incremental pull (today's snapshot)
health backfill --source garmin --months N             # last N calendar months
health backfill --source garmin --days N                # last N days
health backfill --source garmin --from YYYY-MM-DD [--to YYYY-MM-DD]  # explicit range
#   Activities fetched once for the window; daily wellness day-by-day, ~1s/day
#   pacing (a 10-month pull ≈ 20 min). Idempotent → safe to re-run / resume.
#   For a complete multi-year cold start, prefer Garmin's GDPR export tarball.

# Reflexive
health status                                           # snapshot across all sources
health doctor                                           # verify install + paths + perms

# Projection & query
health daily-note [--date YYYY-MM-DD]                  # emit Obsidian daily-note frontmatter
health context [--focus s1,s2,...] [--window-days N] [--activities N] [--no-health] [--no-weight]
#   sections: profile, stats, health, training, weight, activities, synthesis (latest-in-window snapshot)
health series --metric M [--from D] [--to D] [--bucket day|week|month|quarter|year] [--agg mean|sum|min|max|first|last|count]
#   STRUCTURED time-series for any metric (the layer between context's snapshot and raw's JSON).
#   No --bucket → every sample, uncapped. With --bucket → query-time aggregation (processed/enriched),
#   e.g. `series --metric steps --bucket month --agg sum`, `series --metric resting_heart_rate --bucket week`.
health synthesis [--on YYYY-MM-DD]                     # derived metrics traversing full history
#   → hrv_cv_30d, ctl, atl, tsb, vo2max_arc, recovery_score
#   ctl/atl/tsb = 42d/7d EWMA of Garmin per-activity training load (activityTrainingLoad); TSB=CTL−ATL.
#   Per-metric `health <sleep|hrv|rhr|...>` and `training <status|vo2max|...>` queries are v1 stubs.
health raw [--from D] [--to D] [--endpoint NAME] [--source garmin]   # verbatim upstream responses
#   The LOSSLESS layer: every field the source returned, nothing curated. Garmin's daily summary
#   is ~94 fields (we type ~5); sleep carries sleepLevels (stages) + hrvData; stress carries the
#   intraday array. Completeness over truncation — uncapped within range. Captured on every
#   sync + backfill. endpoints: daily_summary, sleep, hrv, stress, spo2, respiration,
#   body_battery, vo2max, training_readiness, weight, hydration.

# Output formatters (applies to every subcommand)
health <cmd> --format {json,jsonl,csv,tsv,human}       # default: json
```

**Exit codes:** `0` success · `1` error · `2` auth-required (re-run `health auth login`) — matches `eddmann/garmin-connect-cli` convention so wrapping scripts can branch on `$?`.

**Output formatters:** every CLI subcommand routes user-visible output through `cli/formatters.py::format_value`. Direct `print(json.dumps(...))` calls inside subcommands are an explicit anti-pattern.

---

## Garmin backends (config: `[garmin] backend`)

Garmin has four interchangeable backends behind the one `TraceSource` port — the payoff of the hex architecture. Select via `~/.config/broomva-health/config.toml`:

```toml
[garmin]
backend = "native"        # default — in-house garth client, rides your token
```

| Backend | How auth works | Tradeoff |
|---|---|---|
| **`native`** (default) | **In-house.** We call Garmin's `connectapi` endpoints ourselves through `garth` (pinned MIT), riding an existing token. Bootstrap once with `health auth import` (copies the token `garmin-connect auth login` minted — **no password through this skill, no fresh login**). `garth` auto-refreshes the OAuth2 bearer; we own aggregation + mapping + lifecycle. | Captures the **richest** set (steps, sleep, **HRV**, **VO2max**, body-battery, **training readiness**, floors). Needs a one-time token import; when the ~1yr OAuth1 token expires, re-mint via `cli`/`library` then re-import. |
| **`cli`** | **Delegated** to [`eddmann/garmin-connect-cli`](https://github.com/eddmann/garmin-connect-cli). One-time `garmin-connect auth login`; the CLI owns the token lifecycle. | Needs the `garmin-connect` binary on PATH (`uv tool install garmin-connect-cli`). Syncs via `context` (no HRV/VO2max). |
| **`library`** | Direct `garminconnect` import (diauth); `health auth login` collects the password via `getpass`. | Automatable, but **fresh** SSO login is Cloudflare-walled (429 → CAPTCHA → account-lock). Install `pip install '.[garmin]'`. |
| **`browser`** | (planned) Interceptor real-Chrome capture; you log in once in your browser. | CAPTCHA-proof but needs an interactive session; not yet wired. |

**The skill never handles your Garmin password on the default (`native`) backend.** `health auth login` detects the delegated backend and skips the password prompt; auth is the token import.

First-time setup (default `native` backend):

```bash
# Mint a token once (interactive — credentials go straight to Garmin):
uv tool install garmin-connect-cli && garmin-connect auth login
# Bring it in-house + pull data:
health auth import                   # copies that token into our store
health sync                          # in-house garth pull → trace DB
```

Already have an `oauth1_token.json` + `oauth2_token.json` elsewhere? `health auth import --from <dir>`.

---

## Composition with bstack primitives

The skill is designed to *compound* with the existing bstack primitives, not replace any of them.

| Primitive | How Health composes |
|---|---|
| **Bookkeeping (P6)** | High-signal health observations (e.g. "CTL crossed 60 for the first time"; "HRV-CV jumped > 0.15 — illness onset?") get promoted into `research/entities/concept/health-*.md` via the Nous gate (≥ 5/9). The Health skill does NOT compete with the entity graph — it feeds it. |
| **Persist (P12)** | Daily sync loop runs as `persist iterate skills/Health/PROMPT.md`. Each iteration spawns a fresh agent context; state lives in the trace DB + a tiny `state.jsonl`. Backpressure is from the sync `SyncResult` + the rate-limiter, not model self-grading. |
| **Snapshot (P15)** | `health status` is the P15 reflex for the health domain. Every health-domain agent response opens with it. |
| **Audience (P18)** | Daily-note projections are *agent-and-human-readable* (markdown rendered by Obsidian) — Category B per the format-discernment rule. Plans/specs about the skill itself are HTML under `docs/plans/`, `docs/specs/`. |
| **Cross-Review (P20)** | Validation-evidence calls are MED/LOW confidence by default and require a second-model pass before being baked into agent prose. Vendor "recovery scores" never escape the trace layer un-flagged. |
| **Telos** | Cross-links to `USER/TELOS/GOALS.md` (longevity/fitness goals), `MISSION.md` (the underlying *why*), `MODELS.md` (Attia/Galpin/Sims mental models). The Health skill can emit a `health context --format json` blob suitable for direct Telos GOALS-progress queries. |

The skill is **not** a primitive — it is a substrate that several primitives compose against.

---

## Privacy invariants

The Health skill is the most privacy-sensitive workspace component. The invariants are hard:

1. **SQLite by default; SQLCipher upgrade path documented** — v1 ships unencrypted SQLite at `~/broomva-health/traces/<source>.db`. v1.1 will add the `[encrypted]` extra (`pysqlcipher3`) and a one-shot migration to SQLCipher with the encryption key stored in macOS Keychain. See [References/privacy-architecture.md](References/privacy-architecture.md).
2. **Tokens at `0o600`; directory at `0o700`** — `~/.config/broomva-health/tokens/` directory is mode `0o700` (only owner can read), token files are mode `0o600`. The filesystem token store enforces this at write time.
3. **Never log PII** — no log statement may contain email, password, MFA code, raw token bytes, sample values, or device serials. The agent never echoes these to the conversation log either. PII redaction is enforced at the formatter layer.
4. **Local-first; no telemetry; no third-party calls beyond the source's own API** — the Health skill makes network calls only to the source vendors (Garmin Connect, in v1). No analytics, no crash reporters, no "phone home".
5. **Reconciliation is a projection, not a column** — samples carry `source` + `device`; which-source-wins for a given metric/window is computed at projection time, not stored as a flag in the trace. This preserves provenance permanently.
6. **Apple HealthKit's local-only model is the reference** — Apple keeps every HKSample on-device unless the user explicitly shares with an app. We aspire to the same posture for everything we ingest.

Failure to uphold these invariants is a P20 blocker — Cross-Review must reject any PR that touches `adapters/repositories/` or `adapters/token_stores/` without re-verifying them.

---

## What this skill explicitly is NOT

- **Not a coaching surface in v1.** It does not tell you to take a rest day, hit zone 2, or sleep more. Coaching is the v2 vision (see [Workflows/Coaching.md](Workflows/Coaching.md)) and requires Telos + calendar + context integration that is intentionally out-of-scope here.
- **Not Apple Health in v1.** The Apple Health adapter is *designed-for* (the `APPLE_HEALTH` Source enum member exists; the port shape is HealthKit-compatible) but unimplemented. Adding it is a P5 fan-out task per [References/extension-guide.md](References/extension-guide.md).
- **Not a Garmin Health API client.** Garmin Health is enterprise-only and not viable for a single-user knowledge graph. The default `native` backend is in-house — it calls Garmin's `connectapi` through `garth`, riding an existing token (no fresh login, no external binary); `cli` delegates to `eddmann/garmin-connect-cli`, `library` uses `garminconnect` directly — see [References/garmin-api-landscape-2026.md](References/garmin-api-landscape-2026.md) and the **Garmin backends** section above.
- **Not a replacement for `apps/healthOS/`.** `healthOS` is the platform; this skill produces the substrate that `healthOS` can read from. The `[ProjectionTarget]` port exists precisely so `healthOS` can subscribe without coupling.
- **Not a Strava / Wahoo / Polar middle-tier.** Strava has no sleep/HRV/body-battery; Wahoo has no API; Polar's API is gated. These are not viable substrates for a health KG.
- **Not a vendor "recovery score" passthrough.** Body Battery, Training Readiness, Whoop Recovery are stored as opaque metric codes (`BODY_BATTERY`, `TRAINING_READINESS`) for completeness but synthesis recomputes its own composites. Reasoning: Altini and others have documented that vendor recovery scores are unvalidated "made up scores" — see [References/validation-evidence.md](References/validation-evidence.md).

---

## Self-evolution hooks

The Health skill is a **P22 primitive candidate** — *not promoted*. Per the L3 stability budget in CLAUDE.md, promotion requires the rule-of-three: three concrete failures the skill prevents, with citations, logged in `research/entities/pattern/bstack-engine.md`. Current count: **0**. Track here:

- Failure 1: *unrecorded* — the daily "did I sync Garmin?" ritual that produced no persistent answer.
- Failure 2: *unrecorded* — repeated re-asking of "what's my VO2max trend?" because no skill owned the question.
- Failure 3: *unrecorded* — agent answering health questions from training-data priors when the live trace store could answer.

When each failure is logged with citation (session ID + date + concrete artifact), the skill graduates from `primitive_candidate` to a numbered primitive. Until then it remains a skill — useful, composable, but not in the table at CLAUDE.md §Bstack Core Automation Primitives.

The L3 cadence is deliberate: skills compose; primitives stabilize. Don't promote until the substrate has earned its row.

---

## Related skills / references

**Workspace skills:**
- `/bookkeeping` (P6) — promote high-signal health observations into the entity graph
- `/persist` (P12) — `persist iterate health-sync.md` for daily sync loop
- `/cross-review` (P20) — mandatory gate before merging health substrate changes
- `/telos` — health metrics feed Telos GOALS/MISSION/MODELS

**Per-workflow docs:**
- [Workflows/Sync.md](Workflows/Sync.md)
- [Workflows/Backfill.md](Workflows/Backfill.md)
- [Workflows/Status.md](Workflows/Status.md)
- [Workflows/DailyNote.md](Workflows/DailyNote.md)
- [Workflows/TrainingLoad.md](Workflows/TrainingLoad.md)
- [Workflows/RecoveryReview.md](Workflows/RecoveryReview.md)
- [Workflows/VO2maxArc.md](Workflows/VO2maxArc.md)
- [Workflows/Coaching.md](Workflows/Coaching.md) (NOT IMPLEMENTED in v1)

**References:**
- [References/architecture.md](References/architecture.md) — hex architecture deep-dive
- [References/garmin-api-landscape-2026.md](References/garmin-api-landscape-2026.md) — why we built from scratch
- [References/healthkit-data-model.md](References/healthkit-data-model.md) — sample-type rationale
- [References/extension-guide.md](References/extension-guide.md) — how to add a source
- [References/rate-limit-discipline.md](References/rate-limit-discipline.md) — what's safe; what bans accounts
- [References/privacy-architecture.md](References/privacy-architecture.md) — local-first model + SQLCipher path
- [References/validation-evidence.md](References/validation-evidence.md) — what synthesis metrics are HIGH-confidence

**External:**
- [Linear BRO-1235](https://linear.app/broomva/issue/BRO-1235)
- Design plan (HTML, human-readable): `docs/plans/2026-05-22-health-skill.html`
- Trace schema spec (HTML, human-readable): `docs/specs/2026-05-22-health-trace-schema.html`
