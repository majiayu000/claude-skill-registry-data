---
name: anysite-monitor
description: >-
  Build and run recurring monitoring on the Anysite MCP, delivering ONLY new or
  changed items each run by diffing against a persistent "seen ledger". Owns the
  onboarding: interviews the user about the decision the monitor should support,
  then searches the live Anysite catalog for endpoints that serve it, verifies
  each with a real call, and compiles them into a self-contained monitor config.
  No preset source list — sources are discovered per monitor. Use whenever
  someone wants to monitor, track, watch, configure monitoring, or get daily or
  weekly updates on anything Anysite can reach — companies, people, jobs, pricing
  pages, posts, news, reviews, listings, prices — e.g. "monitor X every day", "track changes in",
  "only show me what's new", "alert me when", "set up a recurring check",
  "help me configure monitoring", "настроить мониторинг", "мониторить конкурентов",
  "отслеживать изменения", "только новое", "раз в день".
  Also use it when a saved monitor fires on a schedule. For accounts that live in
  a connected CRM, prefer anysite-crm-signals (it writes signals back to the CRM);
  this skill covers everything outside the CRM and any non-account target.
---

# Anysite Monitor

A one-shot Anysite call answers *"what is the state right now?"*. This skill
answers the harder question — **"what changed since I last looked?"** — by
keeping a **seen ledger** of fingerprints in durable storage, subtracting it from
each fresh fetch, and reporting only what's new or edited.

Two things make a monitor good, and both are decided at setup, not at runtime:

1. **The right sources.** This skill ships **no catalog**. Anysite has 566
   sources and they change; a baked-in list rots and quietly points monitors at
   endpoints that no longer do what their name suggests. Instead, onboarding
   searches the live catalog for the user's actual goal, verifies each candidate
   with `discover` + one probe call, and compiles verified specs into the config.
2. **State that survives.** Each scheduled run is a fresh session with no memory.
   Anysite's request cache does persist for 7 days across sessions (find old
   cache_keys with the free `search_requests`), but it is a cache of fetches, not
   a report state — 7-day retention is shorter than the ledger's rolling window,
   and it can't record what was already *reported*. So the ledger must sit in
   external storage a headless run can reach by token — OR, for daily-or-faster
   monitors with stable-id sources, run **ledgerless** (`ledger_mode:
   "cache_diff"`): diff each fetch against the prior runs' fetches still in that
   7-day cache. Zero storage and no persist step, at the price of no long memory
   and silent loss after a failed delivery — mode selection rules in
   `references/storage-backends.md`.

## Two modes

- **Setup mode** — the user wants to create or change a monitor. Interview,
  discover sources, compile the config, register the schedule, seed the baseline.
- **Run mode** — a scheduled task fired with a config in its prompt. Load ledger,
  execute the config's sources, diff, deliver, persist. If the incoming prompt
  already contains a monitor config, you are in Run mode — skip the interview.

## Core concepts

- **Fingerprint** — a stable id for one item, chosen from the endpoint's real
  `response_fields` (platform id/URN first, normalized URL only as fallback).
- **New / changed / seen** — new = fingerprint absent from the ledger; changed =
  present but its content hash differs (only for hashed sources like pricing
  pages); otherwise suppress.
- **Baseline** — on the first run everything looks new, so seed the ledger
  silently and report one line: "monitoring initialized, tracking N items across
  M sources". Real deltas start at run two. (`initial_snapshot` overrides.)
- **Rolling window** — drop fingerprints unseen for `retention_days` (default 45)
  so the ledger stays bounded.

## Setup workflow

Follow `references/onboarding.md` — it is the playbook, not a summary. The arc:

1. **Decision first.** "What will you do differently when this fires?" Then
   targets as resolvable handles (domain, slug, subreddit, URL), cadence,
   delivery, volume tolerance.
2. **Signals.** Restate the goal as testable signals: what item appears, and what
   makes it worth reporting.
3. **Sources — discovered, never assumed.** Per `references/source-discovery.md`:
   find candidates → `discover(source, category)` for exact params and
   `response_fields` → one small `execute` probe on a real target → record the
   verified spec. Two equally valid ways to find candidates: **MCP-only** (the
   tools self-enumerate — a bogus source/category/endpoint returns
   `available_sources` / `available_categories` / `available_endpoints`, free) or
   **catalog grep** (`docs.anysite.io/llms-full.txt` via shell, adds keyword
   search over descriptions). Use whichever the surface allows; never fetch the
   12 MB `openapi.json`. **Read the params for a time filter** (`posted_after`,
   `date_posted`, `time_filter`…) and use it when present.
4. **Size it out loud.** `targets × signals` calls per run, × cadence × 30 for the
   month. Trim here, before the schedule exists.
5. **Pick the state mode, then check the run surface.** Cadence ≤ 2 days +
   stable-id sources + digest-tolerance → offer `ledger_mode: "cache_diff"`
   (no storage, no persist; state the trade-off out loud). Otherwise ledger,
   backend per `storage-backends.md`. For ledger mode also verify: can the
   scheduled run reach a shell, Python, and this skill's `scripts/`? Test during
   the dry run; if not, record `"diff_mode": "in_session"` so the run doesn't
   discover it at 7 a.m.
6. **Agree, dry-run, register, baseline.** Show the monitor in plain language,
   invite correction, optionally execute one pass to show the real digest, then
   register the task and seed the ledger.

## Scheduling

The schedule must outlive the session. **Do not use `CronCreate`/`CronList`** —
those are session-scoped (and expire in days). Use the host's durable
scheduled-task tools; in Cowork/Claude Code Remote these are `create_trigger`,
`update_trigger`, `list_triggers`, `delete_trigger` (load via ToolSearch if
deferred).

**Verify the tools exist before promising a schedule.** If none is available in
the current surface, do not fake it: finish the config, run the baseline, hand the
user the config plus a one-line instruction for creating the scheduled task
themselves in the UI, and say plainly that the schedule is not registered yet.

The task prompt must be a self-contained Run-mode instruction: "Invoke the
anysite-monitor skill in Run mode with the config below" + the config JSON +
the ledger JSON as a **separate block**. Store the returned id in
`monitor.trigger_id`. Set the task's `notifications` per the chosen delivery.

## Run workflow

**`ledger_mode: "cache_diff"`?** Different loop, no ledger and no persist:
find prior fetches via `search_requests` (match endpoint + target handle, last
7 days), union their id sets via `query_cache`, diff the current fetch against
the union in-session, deliver; the current fetch's cache entry is next run's
history. No prior fetches → baseline (fetch + one-line init). Full recipe in
`references/storage-backends.md`. Everything below is the ledger-mode loop.

1. **Load** config and ledger (backend per `references/storage-backends.md`). No
   ledger → baseline run.
2. **Collect.** For each entry in `config.sources`, `execute` exactly what the
   spec says, capped by `max_items`. No re-discovery, no improvisation: if a
   source errors, note it and continue (fail soft, never abort the digest).
   **Time window:** if the spec has a `time_filter`, convert `last_ok_run` into
   its value per `source-discovery.md` (unix_ts → minus one cadence of overlap;
   enum → smallest bucket covering the gap). **On a baseline run there is no
   `last_ok_run`** — use a deliberate seed window instead: for enum filters the
   smallest bucket that matches the cadence (daily monitor → `day`/`past-24h`),
   for unix_ts `now − 7 days`, and cap by `max_items`. Say the seeded window in
   the init line, because anything older than it will surface as "new" on run 2.
3. **Diff deterministically.** Shape items into
   `{fingerprint, content?, label, url}` and run:
   `python3 scripts/ledger.py diff --ledger <file> --items <file> --today <YYYY-MM-DD> --retention-days <n> [--baseline]`.
   It normalizes URLs, hashes content, buckets new/changed/seen, applies the
   rolling window and returns the updated ledger. Don't hand-roll the diff — the
   whole point is that every run diffs identically.
   **If the surface has no shell or no Python** (or the skill's `scripts/` isn't
   available where the trigger fires — verify this at setup, not at 7 a.m.), fall
   back to diffing in-session, following exactly the rules the script implements:
   normalize URLs (lowercase host, strip `utm_*`/`fbclid`/`gclid`/`ref`, drop
   fragment and trailing slash), compare fingerprints against `ledger.items`,
   treat a differing content hash as *changed*, stamp `s` = today for everything
   seen, drop entries older than `retention_days`. Note in the digest that the
   fallback diff was used — it is the one step where drift can creep in.
4. **Persist, then deliver.** Write the ledger back *before* sending the digest:
   a run that reports deltas and then fails to save them repeats them next time.
   Stamp `last_ok_run` only on a successful write; if it lags `last_run`, say so
   in the digest so repeats are explained. Recovery aid: `search_requests` (free)
   can locate the previous run's fetches and their cache_keys for up to 7 days —
   useful to reconstruct what a failed-persist run had already reported, or to
   skip refetching a source this run already pulled.
5. **Deliver** per the digest format below.

### Digest format

Group by target, then signal. Lead with counts so the reader can triage.

```
📡 <Monitor name> — <date>
<N> new · <C> changed since last run

## <Target A>
### New job postings (2)
- Senior ML Engineer, Berlin — posted <date> — <url>
- Head of Sales, Remote — posted <date> — <url>
### Pricing change (1)
- Pro plan $99 → $79/mo — <url>

_No changes for: <Target B>, <Target C>_
_Source "<name>" returned an error this run — skipped._
```

Nothing new is a valid result: say it in one line. Match the channel — email can
be rich markdown, Telegram/Slack should be tighter. Honour `focus` when set.

## Guardrails

- **Cost.** `discover` and catalog greps are free; `execute` is not. Never
  re-fetch history you've already fingerprinted, use time filters where they
  exist, and keep `max_items` tight.
- **Window overflow.** If a source returns exactly `max_items` new items, the
  window may have overflowed and items were missed — warn in the digest and
  suggest a tighter cadence or a higher cap. Silent loss is worse than noise.
- **Stable fingerprints.** Prefer platform ids over URLs; normalize URLs. An
  unstable fingerprint turns the monitor into a spam machine on run two.
- **Hash meaning, not markup.** For pages, hash the extracted plan names/prices
  or feature list — never raw HTML (nav, banners and tokens change constantly).
- **cache_diff discipline.** Ledgerless mode is only as good as the cache
  window: if the gap since the last fetch approaches 7 days, re-seed quietly
  instead of flooding, and never sell this mode for must-not-miss monitoring.
- **No dead ends on discovery.** If the shell or the docs fetch is unavailable,
  the MCP self-enumeration path (`available_sources` / `available_categories` /
  `available_endpoints`) covers the same ground for free — never abandon a signal
  because one browsing route was blocked.
- **Headless reality.** Only depend on hosted, token-authenticated tools. Anything
  proxied through the user's desktop is unavailable when their laptop is closed.
- **People data.** Monitoring individuals' activity is personal-data processing:
  keep it to what the stated decision needs, and don't quietly widen it.

## Reference files

- `references/onboarding.md` — the Setup-mode interview playbook.
- `references/source-discovery.md` — how to find and verify sources in the live
  catalog, and how to pick fingerprints and time filters from `discover` output.
- `references/config-schema.md` — monitor config (incl. verified `sources[]`
  specs) and ledger schema.
- `references/storage-backends.md` — backend selection and read/write recipes.
- `scripts/ledger.py` — deterministic diff, hashing, URL normalization, rolling
  window.
