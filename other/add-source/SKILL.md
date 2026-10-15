---
name: add-source
description: Add (or repair) one data source in current-events-dashboard — catalog check, recorded fixtures, a pure adapter that emits docs/EVENT_MODEL.md events, fixture tests including error cases, registry entry with polite-polling settings, live smoke, gate, deploy, and a latency measurement. Use whenever a new feed/API/scraper is wired in or an existing one breaks or drifts.
---

# add-source

Adding sources is this project's most repeated task. Every step exists because skipping it bit someone.

0. **Prior art first.** Find the source's row in `docs/SOURCES.md` and its section in `docs/research/` (what was
   measured: URL, validator, cadence, traps). `grep docs/TRAPS.md` and `docs/DECISIONS.md` for its host and name.
   Partisan and third-party sources are allowed as D-009 and D-017 say: labeled by origin, facts only (with a visible
   source credit and link for third-party items); the named third-party sources may be ingested without a terms check
   (D-017 superseded D-009's link-out rule for them).
1. **Catalog row.** The row in `docs/SOURCES.md` must name: `source_id`, URL, features (F-ids), affiliation, license
   or terms, robots status, which cache validator it honours, cadence, rate budget, and known traps. Add or fix the row
   first; it is the source's one home.
2. **Record fixtures** before writing the parser: real responses (status, headers, body) with a `meta.json` sidecar
   (url, fetched_at UTC, User-Agent) under `fixtures/<source_id>/<YYYY-MM-DD>/` (use `node scripts/record_fixture.mjs`). Always include an **error case**
   (e.g. a 200 whose body is an error page) and an **empty / no-new-items case**. During the recess (until Nov 9) use
   the recorded September session days.
3. **Write the adapter as a pure function**: parsed response in, `Event[]` out, no network or platform APIs inside, so
   it runs in a Cloudflare Worker and in Node alike. Parse only what is new (head-only parsing: the Worker free-tier
   CPU limit is tiny, see `docs/ARCHITECTURE.md`). Validate the body's shape and **fail closed**: on unexpected structure, emit a
   `system.source_health` drift event and publish nothing from that payload.
4. **Tests**: each fixture → golden normalized events (schema-validated); the error and empty fixtures produce no
   FEED events (a `system.source_health` signal is allowed: it drives the status page, it is not a feed item); at least one non-default case (tie vote, revision, DST-boundary time…). The test
   must fail if the parser is broken (TESTING.md rule 2).
5. **Register** the adapter with its cadence (business hours vs off-hours, calendar-aware for recess/weekends), the
   validator to send (ETag vs If-Modified-Since), rate budget, User-Agent override if needed, and freshness SLO.
6. **Live smoke** once from the dev machine (and from Cloudflare once the probe Worker exists): status, validator
   behaviour, bytes, parse time. Record the result in the PROGRESS entry; a surprise becomes a `docs/TRAPS.md` entry.
7. **Gate, push** (G-003; a push redeploys the Pages site), **deploy the Worker** only under a Cloudflare deploy grant
   in `docs/OWNER_GRANTS.md` (none exists until the owner gives one; until then ask), then confirm on the deployed system that the source's health shows a successful
   poll (quiet is fine during recess; say why in PROGRESS).
8. **Measure latency** the first time a real event flows: `first_seen_at − occurred_at` (n, date) into the source's
   `docs/SOURCES.md` row. Until then, the row says "latency: unmeasured".
