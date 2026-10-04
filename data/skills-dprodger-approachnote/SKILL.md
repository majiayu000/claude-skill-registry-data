---
name: approach-note-release-validator
description: Validate that a release in the ApproachNote production database is well-formed — check referential integrity, presence of MusicBrainz match, cover imagery, streaming links, track listings, and artist links. Use whenever the user asks to validate, audit, sanity-check, or "look at" a specific ApproachNote release. Triggers on inputs that include an ApproachNote release UUID, a MusicBrainz release ID (MBID), or a song name (in which case run an interactive disambiguation to land on a specific release first). Use this skill even when the user just asks "is this release OK?" / "does this look right?" / "audit release X" with a release-like identifier — don't wait for the word "validate."
---

# ApproachNote Release Validator

Confirm that a single release row in the ApproachNote Postgres database has all expected relationships, references, and metadata populated.

This is a **read-only audit**. No writes, no calls to MusicBrainz or any other external service. The output is a human-readable report of what passed, what warned, and what failed.

---

## When this skill applies

Trigger when the user wants to inspect a specific release. Inputs come in three flavors:

1. **ApproachNote release UUID** — a 36-char UUID that exists in `releases.id`.
2. **MusicBrainz release ID (MBID)** — looks like a 36-char UUID; the user usually labels it as MB or pastes a `musicbrainz.org/release/...` URL.
3. **Song name** (with optional artist / album hints) — requires an interactive disambiguation to pick one release.

If the user gives no identifier at all, ask for one before doing anything.

---

## Setup

Run from `ApproachNote/backend/` so `.env` and `db_utils.py` are on the path. The skill uses **simple (non-pooled) connection mode** — make sure `DB_USE_POOLING` is unset or `false`.

Sanity check before the first query:

```python
import os
os.environ.setdefault("DB_USE_POOLING", "false")
from db_utils import test_connection, execute_query, find_song_by_name
test_connection()
```

If `test_connection()` fails, stop and surface the error to the user — don't try to soldier on with broken credentials.

---

## Resolving the input to a single release

The goal of this stage is one `releases.id` UUID. Confirm with the user before validating, especially in case C.

### Case A — ApproachNote release UUID

Fetch the row directly. Echo back title, artist_credit, year so the user can sanity-check we're looking at the right thing.

```sql
SELECT id, title, artist_credit, release_year, musicbrainz_release_id
FROM releases
WHERE id = %s;
```

If not found, tell the user — likely a typo or a deleted row.

### Case B — MusicBrainz release ID (MBID)

```sql
SELECT id, title, artist_credit, release_year, musicbrainz_release_id
FROM releases
WHERE musicbrainz_release_id = %s;
```

If not found: the release just isn't in ApproachNote yet. Don't try to fetch from MusicBrainz — that's out of scope.

### Case C — Song name (turn-by-turn disambiguation)

Walk the user one step at a time. **Don't dump all candidates at once.** Each step is one question, then wait.

**Step 1: Find the song.**

```python
song = find_song_by_name(user_input)  # handles case + accent normalization
```

If `None`, tell the user. If multiple songs share the title (rare — usually only happens with `alt_titles`), list them with composer + year and ask which.

**Step 2: List candidate artists.**

Show the top 20 distinct `artist_credit` values across all releases that contain a recording of this song, ranked by release count so popular candidates float up:

```sql
SELECT rel.artist_credit, COUNT(DISTINCT rel.id) AS release_count
FROM songs s
JOIN recordings r          ON r.song_id = s.id
JOIN recording_releases rr ON rr.recording_id = r.id
JOIN releases rel          ON rel.id = rr.release_id
WHERE s.id = %s
GROUP BY rel.artist_credit
ORDER BY release_count DESC, rel.artist_credit
LIMIT 20;
```

Present the list and ask which artist. Phrase the question so the user knows they can name an artist that isn't in the top 20 (e.g., "Which artist? Or name one not listed."). Match the user's answer with `ILIKE '%...%'` against `releases.artist_credit` — the match doesn't need to come from the displayed list.

**Step 3: List candidate releases for that song + artist.**

```sql
SELECT rel.id, rel.title, rel.release_year, rel.label
FROM songs s
JOIN recordings r          ON r.song_id = s.id
JOIN recording_releases rr ON rr.recording_id = r.id
JOIN releases rel          ON rel.id = rr.release_id
WHERE s.id = %s AND rel.artist_credit ILIKE %s
ORDER BY rel.release_year NULLS LAST, rel.title;
```

If exactly one — confirm and proceed. If multiple — show title + year + label, ask which. If zero — back up and let the user re-pick the artist.

**Step 4: Resolve to one `releases.id` and validate.**

If the candidate set is ever empty, stop and tell the user where it broke down.

---

## Validation checks

Run all of these against the resolved release and collect findings as `(severity, category, message)`. Severities: `FAIL` (✗), `WARN` (⚠), `PASS` (✓ — usually omitted from output unless the user asked for the full breakdown).

### Core release row

- `title` is non-empty (not just whitespace).
- `artist_credit` is set.
- `musicbrainz_release_id` is set and matches the 36-char UUID shape.
- `musicbrainz_release_group_id` is set.
- `release_year` is set (or `release_date`).
- `format_id` and `status_id` are set.

### Track listing

- `total_tracks` is declared (non-null, > 0).
- Count of `recording_releases` rows for this release equals `total_tracks` (WARN if mismatched, with both numbers).
- No null `track_number` in any junction row.
- No duplicate `(disc_number, track_number)` within the release.
- Track numbers are contiguous from 1 per disc (WARN on gaps, e.g. 1,2,4).
- `total_discs` matches the count of distinct `disc_number` values in the junction.

### Recordings linked to this release

For every recording reachable via `recording_releases`:

- Recording has a `musicbrainz_id` (WARN if missing).
- `song_id` row exists in `songs` (referential integrity).
- Recording has at least one `recording_performers` row (WARN if zero).
- Recording has `recording_year` or `recording_date` (WARN if both null).

Aggregate WARNs across tracks rather than emitting one per track ("3 of 7 tracks have no MB recording ID").

### Imagery

- At least one `release_imagery` row with `type = 'Front'` (FAIL if missing).
- At least one with `type = 'Back'` (WARN if missing — optional but nice).
- If no imagery at all, `cover_art_checked_at` should be set (so we know we tried). FAIL if both: no imagery AND `cover_art_checked_at IS NULL`.

### Streaming

- At least one `release_streaming_links` row, album-level (WARN if none).
- For each `recording_releases`, at least one `recording_release_streaming_links` row (track-level). Aggregate: "N of M tracks missing track-level streaming link."

### Metadata

- At least one `release_events` row (release date with country) — WARN if missing.
- At least one `release_labels` row — WARN if missing (the `releases.label` field can serve as fallback).

> **This is a starter set.** Well-formedness criteria are still being defined and will be tuned as the skill is used. When the user wants to add or change a check, edit this section directly.

---

## Output format

Lead with a one-line identification so the user can confirm we hit the right release:

```
Release: "{title}" — {artist_credit} ({release_year})
  AN ID: {releases.id}
  MB ID: {musicbrainz_release_id or "—"}
```

Then either the all-clear:

> The release appears well-formed.

…optionally followed by a one-line-per-category summary of what was checked, so "well-formed" is concrete.

…or a grouped list of issues, sorted FAILs before WARNs:

```
✗ No Front cover imagery (and cover_art_checked_at is null)
✗ release_labels has zero entries
⚠ 3 of 7 tracks missing track-level Spotify link
⚠ musicbrainz_release_group_id not set
```

Keep the tone factual and scan-friendly — the user will likely either fix issues by hand or queue them for a backfill, so the report should read fast. Don't editorialize ("this is bad!"); just report.

---

## Schema cheat-sheet (release-relevant tables)

Full schema: `ApproachNote/sql/jazz-db-schema.sql`. Most-used columns for this skill:

| Table | Key columns |
|---|---|
| `releases` | id, musicbrainz_release_id, musicbrainz_release_group_id, title, artist_credit, release_date, release_year, country, label, catalog_number, barcode, format_id, packaging_id, status_id, total_tracks, total_discs, cover_art_checked_at |
| `recording_releases` | id, recording_id, release_id, disc_number, track_number, track_position, track_title, track_length_ms — UNIQUE on (recording_id, release_id) |
| `recordings` | id, song_id, title, recording_date, recording_year, musicbrainz_id, default_release_id, duration_ms |
| `release_imagery` | release_id, source (enum: MusicBrainz/Spotify/Wikipedia/Apple/Amazon), type (enum: Front/Back), image_url_small/medium/large |
| `release_streaming_links` | release_id, service (spotify/apple_music/youtube/…), service_id, service_url |
| `recording_release_streaming_links` | recording_release_id, service, service_id, isrc, match_confidence, match_method |
| `release_events` | release_id, country, release_date |
| `release_labels` | release_id, label_name, catalog_number, musicbrainz_label_id |
| `release_performers` | release_id, performer_id, instrument_id, role |
| `songs` | id, title, composer, musicbrainz_id, alt_titles |
| `performers` | id, name, sort_name, musicbrainz_id |
| `recording_performers` | recording_id, performer_id, instrument_id, role |

For anything else, read the relevant section of `ApproachNote/sql/jazz-db-schema.sql` directly.

---

## Helpers worth knowing about in `db_utils.py`

- `execute_query(query, params=None, fetch_one=False, fetch_all=True)` — main read path; returns `dict_row` results.
- `execute_update(...)` — exists, but **don't use it in this skill**. This skill is read-only.
- `find_song_by_name(title)` — case + accent + apostrophe normalized lookup. Use this for Case C step 1, don't roll your own `LOWER(title) =`.
- `find_performer_by_name(name)` — similar, useful if the user gives a performer name.
- `test_connection()` — quick sanity check; returns bool.
