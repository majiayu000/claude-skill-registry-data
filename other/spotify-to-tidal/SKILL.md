---
name: spotify-to-tidal
description: >
  Migrate all music (liked tracks, playlists, albums, artists, etc) from
  Spotify to Tidal. Supports independent export, import, verification, and
  HTML report generation phases. Use when the user says "migrate spotify to
  tidal", "export spotify library", "import to tidal", "verify tidal import",
  or "spotify to tidal report".
---

# Spotify → Tidal Music Migration

Five-phase migration on the **official TIDAL v2 API** (`openapi.tidal.com/v2`):
(1) export Spotify library, (2) authenticate to Tidal via Authorization-Code +
PKCE (one browser login), (3) pre-import analysis (read-only **exact ISRC**
matching), (4) import to Tidal (batched writes from a resumable match cache),
(5) verify everything landed by reading the account back. Each phase can run
independently.

**Matching is exact by ISRC** (`GET /tracks?filter[isrc]=...`, batched) — no
fuzzy guessing. Matches persist to a resumable cache (`tidal-match-cache.json`),
so an interrupted run resumes instead of restarting. Requests use steady pacing
plus exact `Retry-After` handling on 429.

## Prerequisites

- Python 3.8+
- A Spotify Developer app with Client ID and Client Secret
- A TIDAL Developer app (https://developer.tidal.com) with Client ID/Secret,
  a `http://localhost:3030/callback` redirect URI, and collection + playlists
  read/write scopes
- `requests` library (`pip install requests`)
- `spotify-to-tidal.env` file in your working directory (Spotify **and** Tidal creds)

## Setup

Create a working directory and place your `spotify-to-tidal.env` file there:

```bash
mkdir -p spotify-tidal-working-directory
# Copy spotify-to-tidal.env template from the skill directory
cp .agents/skills/spotify-to-tidal/spotify-to-tidal.env ./spotify-tidal-working-directory/
# Edit it with your real credentials
# nano ./spotify-tidal-working-directory/spotify-to-tidal.env
```

All data files are written to the working directory — not to the skill directory.
Output paths are always controlled by the `DATA_DIR` argument.

## Modes

The skill detects the user's intent and runs one of these modes:

| Mode | Trigger | What It Does |
|---|---|---|
| `spotify-export` | "export spotify", "read my spotify library" | Auth → fetch all → save JSON |
| `spotify-report` | "spotify report", "analyze my spotify" | Read export JSON → generate HTML |
| `spotify-full` | "spotify full", "export and report spotify" | Export + Report |
| `tidal-auth` | "auth tidal", "login to tidal", "connect tidal" | Run tidal_openapi.py auth (PKCE browser login) |
| `tidal-analyze` | "analyze tidal import", "pre-check import" | Read-only exact-ISRC matching → match cache + summary |
| `tidal-import` | "import to tidal", "migrate to tidal" | Read match cache → batch import → save result JSON |
| `tidal-clean` | "clean tidal library", "remove duplicates", "delete albums" | Selectively empty library categories (dry-run available) |
| `tidal-verify` | "verify tidal import", "confirm migration" | Read from Tidal → compare by ID and name → save verification JSON |
| `tidal-report` | "tidal report", "import report" | Read result JSON → generate HTML |
| `tidal-verify-report` | "verification report" | Read verification JSON → generate HTML |
| `tidal-missing-report` | "missing tracks report", "what tracks didn't transfer", "tracks not on tidal" | Read match cache → generate missing-tracks HTML |
| `tidal-full` | "tidal full" | Auth → Analyze → Import → Report |
| `migrate` | "migrate", "move from spotify to tidal" | Spotify-full → Tidal-full → Verify → combined report |

If the user says "migrate my music" without specifying, assume `migrate` mode.

## CRITICAL: Spotify is READ-ONLY — Never Write to Spotify

**This is the most important rule in this skill. The AI MUST NEVER write to Spotify
under any circumstances. No exceptions.**

This skill only **reads** from Spotify (exporting your library). All write operations
— importing tracks, creating playlists, following artists, deleting items — go to **Tidal only**.

The Spotify app credentials used by this skill do not even have write scopes
(only `playlist-read-private`, `playlist-read-collaborative`, `user-follow-read`,
`user-top-read`, `user-read-email`, `user-read-private`). Any attempt to write
to Spotify would be rejected by the API — but the AI should not even try.

**Do NOT:**
- Create, modify, or delete Spotify playlists
- Add or remove tracks from Spotify
- Follow or unfollow Spotify artists
- Modify Spotify library items
- Delete anything from Spotify

**Only DO:**
- Read/export Spotify library data
- Authenticate to Tidal via `tidal_openapi.py auth` (PKCE browser login)
- Write/import to **Tidal** (Phase 5)
- Delete from **Tidal** (clean-library, with explicit confirmation)
- Verify **Tidal** state (Phase 6)

## Human-in-the-Loop Checkpoints

**The AI must follow these rules at all times. If any conflict,
ambiguity, or uncertainty arises at any stage, stop and ask the user. Never guess.**

### Checkpoint A — After Spotify Export (Stats & Approval)

After Phase 1 completes and `spotify-export.json` is saved, the AI MUST:

1. Read the export summary and present it to the user clearly with a **full breakdown**:

   | Category | Count |
   |---|---|
   | Liked tracks | `liked_tracks` count |
   | Playlists | playlist count |
   | Playlist tracks (total) | sum of all `playlists[].tracks` |
   | **Grand total tracks** | **liked + all playlist tracks** |
   | Saved albums | `saved_albums` count |
   | Followed artists | `followed_artists` count |

   Show a few sample track/artist names so the user can verify it looks right.

2. **Ask the user: "Ready to proceed with Tidal import? The import will process all the tracks listed above."**
3. Do NOT start Phase 2 (Tidal auth or import) until the user explicitly approves.

### Checkpoint B — Before Tidal Import (Import Mode Selection)

`import-all.py` is **append-only and idempotent** — items already in Tidal are
left alone (HTTP 409 treated as success), so re-running is safe.

| Option | Description | Safety |
|---|---|---|
| **Append** (default) | Add new items to Tidal. Nothing is deleted. Re-runnable. | Safe ✅ |
| **Replace** | Run `clean-library.py … --confirm` FIRST to empty categories, then import. | Destructive ⚠️ |

**For "Replace" — double confirmation required:**
- Warn the user that the selected categories will be **emptied** on Tidal
- `clean-library.py` itself requires typing `yes delete everything`
- Only run it after the user explicitly asks for a fresh/replace import

The default (and safe) behavior is plain `import-all.py` (append). Only clean
first if the user explicitly requests it.

### Checkpoint C — Fallback Rule

If at any point the AI encounters an error, ambiguity, unexpected result, or anything it is unsure about:
**Stop and ask the user for guidance.** Never make assumptions about the user's data or account.

## Data Directory

All data lives in the **working directory** (the directory containing `spotify-to-tidal.env`):

| File | Purpose |
|---|---|
| `spotify-tokens.json` | Spotify OAuth tokens |
| `spotify-export.json` | Full Spotify library export |
| `tidal-openapi-session.json` | Official-API PKCE session (access/refresh tokens, user_id, country_code) |
| `tidal-match-cache.json` | **Resumable** ISRC/album/artist → Tidal ID match cache |
| `tidal-analysis.json` | Human-readable match summary |
| `tidal-import-result.json` | Import results |
| `tidal-verification-result.json` | Read-back verification vs actual Tidal state |
| `spotify-report.html` | Spotify library HTML report |
| `tidal-report.html` | Import results HTML report |
| `verification-report.html` | Verification health check HTML report |
| `migration-report.html` | Combined migration overview report |
| `tidal-missing-tracks-report.html` | Tracks not found in Tidal's catalog (ISRC + search misses) |

The skill always checks for existing files before starting a phase.
If tokens exist and are valid, they are reused (skip re-auth).
If export JSON exists, the user is asked before re-exporting.

## Phase 1 — Spotify Export

See [spotify/SKILL.md](spotify/SKILL.md) for detailed instructions.

1. Load credentials from `spotify-to-tidal.env`
2. Start `spotify/helpers/auth-server.py` on `127.0.0.1:3030`
3. Open browser for Spotify OAuth authorization
4. Exchange code for tokens, save to `spotify-tokens.json`
5. Run `spotify/helpers/fetch-all.py` to pull all library data
6. Saves `spotify-export.json` to data directory

## Phase 2 — Tidal Authentication (PKCE, one-time)

Authenticate to the official TIDAL API using Authorization Code + PKCE. Opens a
browser login and captures the redirect on `http://localhost:3030/callback`.

```bash
pip install requests   # one-time
python3 tidal/helpers/tidal_openapi.py <DATA_DIR> auth
```

Saves `tidal-openapi-session.json` (access/refresh tokens, user id, country).
Tokens auto-refresh; re-auth only if the refresh token is revoked. Verify a
single lookup with `tidal_openapi.py <DATA_DIR> probe <ISRC>`.

## Phase 3 — Pre-Import Analysis (Recommended)

**Read-only.** Resolves every track by **exact ISRC** via the official
`GET /tracks?filter[isrc]=...` (batched), with a capped text-search fallback for
misses. Albums match by UPC barcode (then fuzzy), artists by name. Writes the
resumable `tidal-match-cache.json` plus a human-readable summary.

```bash
python3 tidal/helpers/analyze-import.py \
    <DATA_DIR>/spotify-export.json \
    <DATA_DIR> \
    <DATA_DIR>/tidal-analysis.json
```

Re-running resumes from the cache (no repeated lookups). Useful flags:
`--batch N`, `--fallback-cap N`, `--no-fallback`, `--limit N` (test slice).
Present the summary to the user before importing.

## Phase 4 — Clean Tidal Library (Optional, destructive)

Standalone cleanup, or to empty categories before a fresh import:

```bash
# Dry run — shows what would be deleted
python3 tidal/helpers/clean-library.py \
    <DATA_DIR> --categories tracks,albums,artists,playlists

# Actually delete (requires --confirm + typed confirmation)
python3 tidal/helpers/clean-library.py \
    <DATA_DIR> --categories tracks,albums,artists,playlists --confirm
```

Categories are independently selectable: `tracks`, `albums`, `artists`,
`playlists`. Removes in batches (50/request) via the official API.

## Phase 5 — Tidal Import

See [tidal/SKILL.md](tidal/SKILL.md) for detailed instructions.

1. Requires `tidal-match-cache.json` from Phase 3 (its source of truth).
2. Run `tidal/helpers/import-all.py`:
   ```bash
   python3 tidal/helpers/import-all.py \
       <DATA_DIR>/spotify-export.json \
       <DATA_DIR> \
       <DATA_DIR>/tidal-import-result.json \
       [--no-liked] [--no-albums] [--no-artists] [--no-playlists] [--no-liked-playlist]
   ```
3. Append-only and idempotent (already-present items return 409 = success).
4. Batched writes (50/req): like tracks, save albums, follow artists, create
   playlists, add playlist tracks **in Spotify order**.
5. After playlists: creates a **"Liked Songs" UNLISTED playlist** containing liked
   tracks in Spotify order — a browsable duplicate of the liked-track favorites.
   Skip with `--no-liked-playlist`.
6. Steady pacing + exact `Retry-After` on 429.
7. Saves `tidal-import-result.json`.

## Phase 6 — Verification (Read-Back)

See [tidal/SKILL.md](tidal/SKILL.md) for detailed instructions.

1. Run `tidal/helpers/verify-import.py`:
   ```bash
   python3 tidal/helpers/verify-import.py \
       <DATA_DIR>/spotify-export.json \
       <DATA_DIR> \
       <DATA_DIR>/tidal-import-result.json \
       <DATA_DIR>/tidal-verification-result.json
   ```
2. Reads actual account state via the official API (favorite tracks, albums,
   artists, playlists + their items).
3. Cross-references expected Tidal IDs (from the match cache) against what is
   actually present; reports liked-track and per-playlist presence health.
4. Saves `tidal-verification-result.json`.

## Reports

Run `reports/generate.py` to build HTML reports. All inputs and outputs are paths inside the working directory (`DATA_DIR`):

```bash
# Spotify library report
python3 reports/generate.py \
  --type export \
  --input <DATA_DIR>/spotify-export.json \
  --output <DATA_DIR>/spotify-report.html

# Tidal import report
python3 reports/generate.py \
  --type import \
  --input <DATA_DIR>/tidal-import-result.json \
  --output <DATA_DIR>/tidal-report.html

# Tidal verification report
python3 reports/generate.py \
  --type verify \
  --input <DATA_DIR>/tidal-verification-result.json \
  --output <DATA_DIR>/verification-report.html

# Combined migration report
python3 reports/generate.py \
  --type migration \
  --spotify <DATA_DIR>/spotify-export.json \
  --tidal <DATA_DIR>/tidal-import-result.json \
  --output <DATA_DIR>/migration-report.html

# Missing tracks report (tracks not found on Tidal)
python3 reports/generate.py \
  --type missing \
  --spotify <DATA_DIR>/spotify-export.json \
  --cache <DATA_DIR>/tidal-match-cache.json \
  --output <DATA_DIR>/tidal-missing-tracks-report.html
```

Reports are self-contained HTML files with embedded CSS — no external dependencies.
Open with any browser.

⚠️ IMPORTANT: Do NOT attempt to open the report in a browser (e.g. via `open`, `xdg-open`, or any similar command).
On Linux systems these commands often fail with missing module errors. Simply print the full path to the
generated HTML file so the user can open it manually.

## Matching Method

| Method | How | Used for |
|---|---|---|
| **ISRC exact** | `GET /tracks?filter[isrc]=...` (batched) | Tracks (primary) — `method: isrc` |
| Text fallback | search by name+artist, fuzzy-confirm (Levenshtein ≥ 0.78) | Tracks Tidal didn't return by ISRC — `method: search` |
| UPC barcode | `GET /albums?filter[barcodeId]=...` | Saved albums (when export has UPC) |
| Album/artist fuzzy | name search, fuzzy-confirm | Albums without UPC; followed artists |

Track matches are stored in `tidal-match-cache.json` keyed by ISRC. Coverage is
typically high-90s% by ISRC; the rest depends on Tidal catalog availability and
the fallback. There is no fuzzy "confidence guessing" for tracks — a track is
matched by exact ISRC or by a high-threshold confirmed search, or it is skipped.

## Architecture

All scripts use the shared `TidalOpenAPI` module (`tidal/helpers/tidal_openapi.py`)
which handles:
- Authorization Code + PKCE auth with auto-refresh (`tidal-openapi-session.json`)
- JSON:API requests (GET/POST/DELETE) with timeouts and retries
- Steady-pace rate limiting (`TIDAL_OPENAPI_MIN_INTERVAL`, default ~8 req/s)
  plus exact `Retry-After` honoring on 429 — no burst-then-backoff
- Cursor pagination for list endpoints
- Matching (`tracks_by_isrc`, `albums_by_barcode`, `search_*`), writes
  (`add_favorites`, `create_playlist`, `add_playlist_items`), reads, and deletes

**API Base:** `openapi.tidal.com/v2` (official developer API)
**Auth:** Authorization Code + PKCE (user's own registered app)
**Credentials:** `TIDAL_CLIENT_ID` / `TIDAL_CLIENT_SECRET` from `spotify-to-tidal.env`