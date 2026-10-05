---
name: music-ingestion-publisher
description: >-
  Ingest music into StaticFlow Music DB via ncmdump-rs CLI and sf-cli:
  search/download from Netease Cloud Music or Bilibili, decrypt local NCM
  files, extract metadata/lyrics/cover art, and publish to lancedb-music.
---

# Music Ingestion Publisher

Ingest music files into the StaticFlow Music LanceDB from multiple sources.

## Source Selection Strategy

1. **Netease Cloud Music** (preferred) — best metadata, album info, lyrics, cover art.
2. **Bilibili** (fallback) — when Netease returns "VIP-only" or "no copyright" errors.
   Audio from Bilibili, lyrics still fetched from Netease via `track_id`.
3. **Local files** — for NCM decryption or direct mp3/flac import.

When a Netease download fails with 403/VIP/copyright error, automatically
switch to Bilibili: search `"<song_title> <artist>"`, download audio, but
still use `ncmdump-cli lyric <netease_track_id>` for lyrics.

## Flow Routing

| Task | Flow | File |
|------|------|------|
| Netease online search/download | A | [flows/netease.md](flows/netease.md) |
| Netease bulk album ingestion | D | [flows/netease.md](flows/netease.md) |
| Bilibili single search/download | E | [flows/bilibili.md](flows/bilibili.md) |
| Bilibili batch ingestion | F | [flows/bilibili.md](flows/bilibili.md) |
| Local NCM decrypt + ingest | B | [flows/local.md](flows/local.md) |
| Local mp3/flac direct ingest | C | [flows/local.md](flows/local.md) |
| Verification / cover / vectors / errors | — | [flows/common.md](flows/common.md) |

## Preconditions

1. **ncmdump-cli**: `./tools/ncmdump-rs/target/release/ncmdump-cli` or PATH.
   Build: `cargo build -p ncmdump-cli --release` (from `./tools/ncmdump-rs/`)
2. **sf-cli**:
   - For worker payloads: use `sf_cli_path` from the payload JSON exactly.
   - Manual resolution: build `cargo build -p sf-cli --release`, then use `./target/release/sf-cli`
   - Rebuild whenever the current checkout is newer than the existing binary.
3. **Music DB**: `/mnt/wsl/data4tb/static-flow-data/lancedb-music`
4. **Netease login**: `ncmdump-cli me`
5. **Bilibili login**: `ncmdump-cli bili-me` + `ffmpeg -version`

### Session files
- Netease: `~/.config/ncmdump/session.json` (`MUSIC_U` key)
- Bilibili: `~/.config/ncmdump/bilibili_session.json` (`sessdata` etc.)

### CLI reference
```
# Netease
search <kw>       Search tracks/albums/artists/playlists (--type, --limit)
info <track_id>   Track details
lyric <track_id>  LRC lyrics (original + translation)
download <id>     Download track (--quality, --output)
playlist <id>     Playlist details
login / logout    Netease session management
me                Current Netease user

# Bilibili
bili-search <kw>     Search videos (--limit, --page)
bili-info <bvid>     Video details (title, cover, duration, cid)
bili-download <bvid> Download audio (--format mp3/flac, --output)
bili-login            QR code login (--check to verify)
bili-logout           Clear Bilibili session
bili-me               Current Bilibili user

# NCM
dump <files>     Decrypt NCM → MP3/FLAC (-d, -r, -o, -m)
```

## Hard Rules

- Never delete source audio files.
- Never overwrite existing records unless user confirms.
- **NEVER write to LanceDB directly** — always use `sf-cli write-music` for
  ingestion. The songs table uses Lance blob v2 encoding for `audio_data`.
  Direct writes (Python lancedb, arrow, manual RecordBatch, etc.) WILL corrupt
  the table and require a full rebuild.
- **Binary location**:
  - Worker runs: payload field `sf_cli_path` is the source of truth.
  - Manual runs: rebuild `cargo build -p sf-cli --release`, then use `./target/release/sf-cli`
  - Do not replace that with legacy `./bin/sf-cli` or stale `target/*/sf-cli` snapshots for blob v2 tables.
- **Cover image is MANDATORY** for online tracks. Must be `https://` URL.
  Use `--cover-url` to set it during ingestion (preferred over post-write update).
- **Album metadata is MANDATORY** when available (Netease tracks).
- **Lyrics**: always attempt `ncmdump-cli lyric <netease_track_id>` even
  for Bilibili-sourced songs, as long as a Netease track_id is known.
- All songs must have `searchable_text` populated (auto by sf-cli).
- Verify record after write (see `common.md`).
- Bilibili downloads require ffmpeg in PATH.
- Bilibili cover URLs must use `https://` (not `http://`).
