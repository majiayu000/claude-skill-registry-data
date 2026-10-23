---
name: database
description: >-
  Read data from Lyrion's SQLite databases — library stats, stored lyrics,
  album covers, recent plays. Use this whenever a task queries `library.db` or
  `persist.db`, adds or changes a statistic, or touches `services/database.py`.
  Covers the read-only connection model (RO open + `ATTACH persist.db`), the
  key tables, the `play_counts` view over the Alternative Play Count plugin,
  the single-flight stats cache, and why the app must never write to these DBs.
  Reach for it before writing any SQL against the Lyrion databases.
---

# Reading Lyrion's SQLite databases

All DB access lives in `services/database.py`. These databases belong to **Lyrion**, not to this app — the app opens them **read-only** and never writes. (Web lyrics can't be persisted here for exactly this reason; they go to a cache or into file tags — see the `lyrics` skill.)

## The connection model

Use the `get_db_conn()` context manager for every query — don't open sqlite inline in a route or elsewhere:

```python
with get_db_conn() as conn:
    row = conn.execute("SELECT lyrics FROM tracks WHERE id = ?", (track_id,)).fetchone()
```

It opens `library.db` in read-only URI mode (`file:...?mode=ro`), **`ATTACH`es** `persist.db` (also RO) as the `persist` schema, sets `row_factory = sqlite3.Row` (access columns by name), applies read-tuning pragmas (mmap/cache/temp), wraps the work in `BEGIN DEFERRED` … `COMMIT`, and defines the `play_counts` TEMP view (see below). Two databases, one connection:

- **`library.db`** (default schema) — the music library: `tracks`, `albums`, `contributor_track`, `genres`.
- **`persist.db`** (referenced as `persist.<table>`) — persistent per-track state: `persist.tracks_persistent` (ratings, `lastplayed`, …), and the Alternative Play Count table `alternativeplaycount` when the plugin is installed.

The DB paths come from config (`DB_PATH`, `DB_PERSIST_PATH`). They are derived from `LYRION_DATA_DIR`, the directory holding Lyrion's own `prefs/` and `cache/` — `{dir}/cache/library.db` and `{dir}/prefs/persist.db` — which `DB_DIR` and `DB_PERSIST_DIR` override one at a time when either was relocated. Tests set the two overrides directly (see the `testing` skill), so they never depend on that layout.

## Key tables and columns

- `tracks` — one row per track. `id` (the Lyrion track id used everywhere, e.g. lyrics lookup), `url`, `urlmd5` (join key to the play counts), `album` (→ `albums.id`), `audio` (filter `audio = 1` for real tracks), `lyrics`, `year`, `coverid`.
- `albums` — `id`, `artwork` (the **coverid** of the album's artwork track, the same id `/cover/<coverid>.jpg` serves).
- `contributor_track` — track↔artist links with a `role`: **role 5 = ALBUMARTIST**, **role 1 = ARTIST** (track artist). "Album artists" filter `role = 5`; the `track_artists_*` stats filter `role IN (1, 5)` — the union, shown in the UI as "All artists".
- `persist.tracks_persistent` — `rating`, `playcount`, `lastplayed` (unix seconds; **bumped on skips too**). Lyrion's own counters, and the fallback source of `play_counts`.

## Play counts: `play_counts`, not the plugin table

Real listening data comes from the [Alternative Play Count](https://github.com/AF-1/lms-alternativeplaycount) plugin's `alternativeplaycount` table, which keeps **plays separate from skips**:

- `playcount` / `lastplayed` — genuine plays. "Played" means `playcount > 0`.
- `skipcount` / `lastskipped` — skips.

The plugin is **recommended, not required**, so no query names that table. `get_db_conn` defines a TEMP view **`play_counts`** (`urlmd5`, `playcount`, `skipcount`, `lastplayed`) over whichever source `_use_apc` picks — it looks for the table in **both** schemas, since the plugin keeps it in `persist.db` so a library rescan cannot drop it, and the view's unqualified name then resolves to whichever holds it — the plugin's table, else `persist.tracks_persistent` with `skipcount` forced to 0 — and every query joins the view, aliased `apc`. `PLAY_COUNTS_SOURCE=lyrion` forces the fallback even when the plugin is installed, for a library whose history predates it. A TEMP view is writable on a read-only connection: it lives in the connection's temp schema, never in Lyrion's files. Use the view for anything about what was played; add a column to both definitions rather than referencing a source table directly.

### The play history and the velocity

The plugin also keeps a play-by-play history, on by default, in a file of its own: `apc_external.db`, beside `persist.db` (`APC_HISTORY_PATH`). Its `play_history` table has one row per genuine play (`urlmd5`, `played` in unix seconds, `client_id`, `rating`, `remote`), streams included. `_history_velocity` opens it read-only on a connection of its own (an `ATTACH` cannot happen inside `get_db_conn`'s transaction) and counts the plays in the velocity windows (`velocity_30d`, `velocity_1year`), plus the plays per local day over the last `CALENDAR_DAYS` (365) for the listening calendar: `listening_calendar` is `{today, start, days: {"YYYY-MM-DD": plays}}` — `today` from the server's clock, `start` the history's first day, days without plays left out — and `None` whenever the velocity falls back. Without that file, or with `PLAY_COUNTS_SOURCE=lyrion`, the velocity counts library tracks whose last genuine play falls in the window, through `play_counts` — a number of tracks, not of plays. Either way the windows start at local midnight, through the `TZ` environment. A history only starts when the plugin started recording it (its March 2026 release), so a window reaching further back cannot be counted: `_add_plays_before_history` then adds, for the stretch before the history's first play, the library tracks whose last genuine play falls in it — each was played at least once — and sets `velocity_30d_partial` / `velocity_1year_partial`. The figure is a floor in the same unit, never an estimate: replays before the history count once, and a track replayed since counts only in the history. Both flags stay false without the history, whose fallback counts tracks.

On the fallback two things degrade, and the code says so where it matters: skips do not exist at all, and `lastplayed` is bumped on a skip too, so `get_recent_album_covers` can surface an album that was only skipped past. `_compute_stats` reports which source it used as **`apc_available`** — the plugin's table *and* not overridden — and the template drops the "Skips" row when it is false.

## The stats cache (single-flight)

`get_stats()` returns library statistics cached for `STATS_TTL` (60s) behind `_stats_lock`. The lock makes the recompute **single-flight**: when the cache expires, simultaneous clients wait for one computation instead of each firing their own set of full-library aggregations. It returns a **copy** so callers can't mutate the cached dict. Keep both properties if you touch it — the stats are four full-library scans and the page polls them from every open client.

`_compute_stats()` runs **four queries** on the library (plus one on the play history, above) (albums+songs, album artists, track artists, misc) using CTEs to scan `tracks JOIN play_counts` once each, then derives percentages via the local `pct()` helper. Every count coalesces to 0 (`row[...] or 0`) so an empty library yields zeros, not `None`.

## Adding or changing a statistic

1. Add the aggregation to the right query in `_compute_stats` (reuse the `track_play` CTE pattern; scan once, don't add a query per number).
2. Add the key to the `stats` dict (coalesce to `0`); add a `_pct` via `pct()` if it's a proportion.
3. Surface it: the `/stats.json` route returns the whole dict, and the template renders named fields — a new stat shown on the page needs an `i18n.py` label (both `fr` and `en`) and a mention in `docs/endpoints.md` or `docs/configuration.md` if it's part of the documented surface (see the `i18n` and `add-route` skills).
4. Test it: build a small temp SQLite DB with the tables/rows you need and assert the computed number, with and without `alternativeplaycount` if the number depends on play counts (see `tests/test_get_recent_album_covers.py`, `tests/test_without_alternativeplaycount.py`, `tests/test_stats_cache.py`). Don't hit a real Lyrion DB. See the `testing` skill.

## Rules

- **Read-only, always.** No `INSERT`/`UPDATE`/`DELETE`; the app must never write to Lyrion's databases. The one `CREATE` is the `play_counts` TEMP view, which lands in the connection's temp schema.
- Always go through `get_db_conn()`; parameterize queries (`?` placeholders), never string-format user input into SQL.
- Filter real tracks with `audio = 1`; join play data via `urlmd5`.
- Join `play_counts` (never `alternativeplaycount` directly) when you mean "actually played".
