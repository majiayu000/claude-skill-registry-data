---
name: creative-suno-archive
description: Archive your own Suno songs into the markdown vault — diff suno.com/me/playlists against what's already downloaded, then pull MP3 + MP4 + WAV per track, capture per-song copyright-evidence screenshots, and write One-Walk-format manifests. Use when the user says "archive my Suno songs", "download my Suno music", "back up <playlist> from Suno", "pull the WAVs for <album>", "check which Suno songs aren't downloaded", or hands a suno.com/playlist/... URL to archive. Drives a logged-in browser via the Playwright MCP + paced download scripts. NOT for composing new songs (use creative-suno-composer).
---

# Suno Archive Skill

Pull the user's own Suno-generated songs into the external vault as a durable,
evidence-backed archive: audio (MP3 + MP4 + lossless WAV) + per-song
copyright-evidence screenshots + manifests, organised per album. Built to be
**gentle on Suno** (throttled) and **resumable** (deterministic, re-runnable).

The reference archive shape is `70_Media/Music/One-Walk-Before-the-Build/`
in the vault. Every album this skill produces matches it.

## Metadata-first or user-downloaded archive route

Use this route when the user asks to update online album/song presentation or
downloads the files themselves. It does not require the legacy Playwright/API
workflow below: use the available supported browser tools and their documented
permissions. Do not extract session tokens or assume legacy endpoints work.

- If requested, save and verify album **and each song** caption/cover before
  downloading video exports. Preserve titles, lyrics, styles, and visibility
  unless changes to them are authorized. Keep the generated original covers.
- Match playlist order and exact song IDs. Two voices with the same title can
  be two intentional selections; never deduplicate by title alone.
- Capture exact lyrics and styles separately. Clipboard output may be empty or
  stale (even the previous lyrics after Copy Styles); validate the section's
  content and fall back to visible page text. Save prompt intent as intent.
- When the user takes over downloading, stop initiating downloads and inspect
  the resulting files. Do not hardcode subscription allowances or model versions.
- Preserve the existing folder layout, including per-version subfolders. Save
  IDs, notes, prompts, captions, covers, format status, and a manifest. Ownership
  screenshots document page evidence; they do not independently establish rights.
- Verify requested files are complete: media streams/codecs and plausible
  duration with available media tools, then source/destination SHA-256 after
  copying. Allow normal encoding padding; do not re-encode merely to match a
  rounded page duration. File presence alone is insufficient.
- Delete download originals only within explicit user authorization, after
  rechecking the archive hashes. Use an exact file allowlist confined to the
  named download directory. Verify duplicate copies by hash. Never clear the
  whole Downloads folder. Existing authorization needs no repeated confirmation.
- Update notes and manifests to the verified state; refresh checksum records
  after subsequent note edits. Do not rerun a stale archive builder that would
  overwrite newer metadata or depend on originals already deleted.


## Prerequisites

1. **Playwright MCP connected** — the `mcp__plugin_playwright_playwright__*`
   tools must be available. It uses a **persistent Chrome profile**
   (`%LOCALAPPDATA%\ms-playwright-mcp\mcp-chrome-*`), so a Suno login persists
   between runs.
2. **Logged into Suno as the owner** — `browser_navigate` to
   `https://suno.com/me/playlists`. If it redirects to the logged-out home, the
   session expired: click "Log in", and **hand off to the user** to complete
   OAuth in the visible window (prefer Phone — Google sometimes blocks
   automated browsers). Do NOT attempt to log in for them.
3. **Scripts present** at `scripts/suno_*.py` in the EmptyOS repo (they read the vault
   path from `emptyos.toml [notes].path`).

### Gotcha: "Browser is already in use"
Leftover `@playwright/mcp` node processes from prior sessions hold the profile
lock. Find + kill ONLY those (`Get-CimInstance Win32_Process -Filter
"Name='node.exe'" | Where CommandLine -like '*@playwright*mcp*'`), then the next
`browser_navigate` respawns a fresh server (the browser tools briefly
disconnect — that's expected). Never `--isolated` (that loses the login).

## The scripts (`scripts/` in the EmptyOS repo)

| Script | Role |
|---|---|
| `suno_vault_index.py` | Scan the vault → master index `70_Media/Music/_suno-index.{md,json}` (every Suno-linked track + local audio + archive status). The diff match-key. Re-run after every pass. |
| `suno_download_album.py --folder --clips [--delay 4]` | Download MP3/MP4 for one album from a clips JSON (paced). Verifies size vs Content-Length. |
| `suno_fetch_wav.py --folder --clips [--timeout 360]` | Poll the CDN for converted WAVs + download (paced). Run AFTER firing `convert_wav` in-browser. |
| `suno_album_manifest.py --folder --clips --playlist --owner --name` | Write `downloaded-audio.md` + `copyright-evidence.md` (One-Walk format, API timestamps). Links any `*.png` in the folder. |
| `suno_batch.py {download,ids,wav,manifest}` | Multi-album batch over a combined JSON. Override the file with env `SUNO_COMBINED=<path>`. Each album may carry an explicit vault-relative `"path"` key (else the built-in folder→path map applies). |
| `suno_place_shots.py --prefix --clips --folder` | Rename numbered `shot-<prefix>-NN.png` (captured to repo root) into `<folder>/NN-<title>-suno-screenshot.png` via the clips JSON — handles `/`,`:` in titles cleanly. Use this for the screenshot pass instead of manual renames. |
| `suno_backfill_manifests.py` | Add manifests to albums that already had audio but none. |

Combined-JSON shape for `suno_batch.py`: `{ "<folder-key>": {"pid","name","path"?,"clips":[...]}, ... }`.
For the screenshot pass: capture each song as `shot-<prefix>-NN.png`, then run `suno_place_shots.py` per album. Curation/mixed playlists (songs that also live in other albums) are fine to archive as faithful per-folder snapshots — duplicates are harmless.

Per-album clips JSON shape (one row per track):
`{"n":1,"id":"<uuid>","title":"...","created":"<ISO>","mp3":"https://cdn1.suno.ai/<id>.mp3","mp4":"<url or empty>"}`

## The Suno API (host matters!)

**Base host is `https://studio-api-prod.suno.com`** — with a DASH, not
`studio-api.prod.suno.com` (the dot variant 404s on download endpoints). All
fetches are done **in-browser** via `browser_evaluate` so the Clerk token never
leaves the page: `const token = await window.Clerk.session.getToken();` then
`fetch(url, {headers:{Authorization:'Bearer '+token}})`. Tokens expire ~60s — re-grab inside each eval.

- **Playlist tracklist:** `GET /api/playlist/<pid>/?page=1` → `{name, playlist_clips:[{clip:{id,title,created_at,audio_url,video_url}}]}` (authoritative order).
- **MP3 / MP4:** public on `https://cdn1.suno.ai/<id>.mp3` / `.mp4` (no auth — Python downloads directly). MP4 is empty for songs with no video.
- **WAV (two-step):**
  1. `POST /api/gen/<id>/convert_wav/` → 204 (kicks off async generation).
  2. Poll `https://cdn1.suno.ai/<id>.wav` until 200/206 (403 = not ready yet). Once ready it's **public** → Python downloads it. (`/api/gen/<id>/wav_file/` returns `{wav_file_url}` but it's the same CDN URL.)

## Workflow

### Phase 0 — scope
1. `python scripts/suno_vault_index.py` (refresh the index).
2. `browser_navigate` → `https://suno.com/me/playlists`; confirm logged in
   (page title shows the user, not "Log in").
3. In-browser, scrape playlist cards (`a[href*="/playlist/"]` → id + the card's
   text for "Name N songs"), or hit `/api/playlist/<pid>/` per playlist.
4. Diff playlist names/song-counts against `_suno-index.json` albums. Bucket:
   **gaps** (on Suno, little/no local audio), **have-audio** (verify only),
   **curation/compilation** (skip unless asked). Report buckets BEFORE downloading.

### Phase 1 — per album (the loop)
For each album to archive:
1. **Clips** — in-browser `GET /api/playlist/<pid>/?page=1`; map to the clips
   shape; write `.cache/suno/<key>-clips.json` (via heredoc, or `browser_evaluate`
   `filename:` save then **un-nest the double-encoded JSON**: `json.loads` twice).
2. **Audio** — `suno_download_album.py --folder "<vault-rel>" --clips <file> --delay 4`.
3. **WAV** — in-browser fire `POST convert_wav` for every id, spaced
   (`await sleep(1200)` between; chunk to ≤32 ids/eval to avoid timeout). Then
   `suno_fetch_wav.py --folder --clips`.
4. **Manifest** — `suno_album_manifest.py --folder --clips --playlist <pid> --owner <handle> --name "<album>"`.
5. **Per-song screenshots** (if requested — see posture below) — for each track:
   `browser_navigate` to `https://suno.com/song/<id>`, then `browser_take_screenshot`
   `filename:"<prefix>-NN-<title>-suno-screenshot.png"`. They land in the repo
   root; move into the album folder stripping the prefix, then re-run the manifest
   (it links every `*.png`). The song page sidebar shows `<handle> / Pro Plan` =
   ownership evidence. Add a `browser_wait_for {time:3}` every ~4 songs.
6. Re-run `suno_vault_index.py` to confirm the album flipped to FULLY ARCHIVED.

### Folder convention (no mass moves)
Download audio INTO the existing album folder next to its notes (preserves
`[[wikilinks]]` + any publish pipeline). YouTube-channel albums live under
`10_Projects/YouTube-Music-Channel/songs/<album>/`; standalone concept albums
under `70_Media/Music/<album>/`. Files are named `NN-<title>.{mp3,mp4,wav}`
(zero-padded track number + Suno title).

## Pacing (avoid bans) — DEFAULT ON

- `--delay 4`+ between tracks; `await sleep(1200..2500)` between API POSTs in evals.
- Run big MP3/MP4 + WAV passes with `run_in_background:true` (large files; avoids
  tool timeouts). For multi-album audio, prefer `suno_batch.py download` / `wav`.
- Never hammer: space playlist fetches (`sleep 2000` in the loop), chunk
  `convert_wav` firing, and don't run page-navigation screenshot bursts at the
  same time as a heavy WAV download.

## Decisions to surface (don't assume)

- **Reorg**: default to **index + standardise in place, no mass relocation**
  (moving files breaks wikilinks + pipelines). Build the master index first.
- **WAV**: lossless but ~30–90 MB/song. Confirm before pulling WAV for large sets.
- **Screenshots**: per-song is thorough but ~2 browser visits/song. The
  `copyright-evidence.md` already carries **authoritative API generation
  timestamps**, so "playlist + Pro-plan shot per album" is a strong, far cheaper
  alternative. Offer both; let the user choose.

## When NOT to use

- Composing/generating new songs → `creative-suno-composer`.
- Third-party songs you don't own (this is an owner-account archive + rights
  evidence tool, not a scraper).
- A song with no `audio_url` (still generating) — skip, revisit later.
