---
name: auto-poster
description: "Post or schedule a provided video directly through Zernio. Input is a local video path or public video URL. If no caption is provided, transcribe the video with faster-whisper (tiny.en by default) and generate a caption from that transcript. No Notion lookup or browser download. Triggers: post this video, post /path/to/video.mp4, schedule this video, queue this video, publish reel, post to instagram, post to zernio."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/auto-poster/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# Auto Poster

Take the video the creator gives you and post it through Zernio.

This skill does one job with one optional prep step:

`provided video -> optional faster-whisper caption -> Zernio`

Zernio posting should feel like:

```js
await fetch("https://zernio.com/api/v1/posts", {
  method: "POST",
  headers: { Authorization: `Bearer ${ZERNIO_API_KEY}` },
  body: JSON.stringify({
    content: "Caption goes here",
    platforms: [{ platform: "instagram", accountId: "..." }],
    mediaItems: [{ type: "video", url: "https://example.com/demo.mp4" }],
    publishNow: true
  })
});
```

Zernio's public examples sometimes show the shorthand shape `text`, `platforms`, and `mediaUrls`. The helper script uses the documented OpenAPI shape: `content`, `mediaItems`, and platform targets with account IDs.

## What This Skill Does Not Do

- Does not search Notion.
- Does not download from Frame.io or Google Drive.
- Does not update pipeline status inside the script. The script never touches Notion. After a successful post, the session (not the script) resolves the video's Notion page and flips it to `Posted` + `Post Date` = today, per the project CLAUDE.md status-move rule.
- Does not run the full content production chain.

If the user wants those steps, use the relevant upstream skill first, then come back here with the final video file.

## Inputs

Required:

- Local video path, e.g. `/path/to/final.mp4`
- Or a public direct video URL, e.g. `https://.../video.mp4`

Optional:

- Caption text or caption file.
- If no caption is provided, generate one from a faster-whisper transcript.
- Platforms: default = every account with an ID in `.env`; name platforms (`--platforms instagram,youtube`) to narrow.
- Mode: default `shareNow`.
- Schedule time for `customScheduled`.
- YouTube title. Default is the filename or caption first line.

## Prerequisites

`.env` (in the skill directory) must contain:

The key list below is the template (`.env.example` in the skill folder is a copyable version) — fill in the real values (README.md documents each key). The script defaults to the skill-directory `.env` regardless of cwd; pass `--env-file` only to override. Values in the `.env` win over any `ZERNIO_*` already exported in the shell.

```bash
ZERNIO_API_KEY=
# only the ones you have connected; every key present is a default posting target
ZERNIO_ACCOUNT_INSTAGRAM=
ZERNIO_ACCOUNT_TIKTOK=
ZERNIO_ACCOUNT_YOUTUBE=
ZERNIO_ACCOUNT_LINKEDIN=
ZERNIO_ACCOUNT_FACEBOOK=
ZERNIO_ACCOUNT_THREADS=
```

Aliases also work (same six platforms):

```bash
ZERNIO_ACCOUNT_ID_INSTAGRAM=
ZERNIO_ACCOUNT_ID_TIKTOK=
ZERNIO_ACCOUNT_ID_YOUTUBE=
```

Optional:

```bash
ZERNIO_API_URL=https://zernio.com/api/v1
ZERNIO_PROFILE_ID=
ZERNIO_QUEUE_ID=
ZERNIO_TIMEZONE=America/New_York
```

`ZERNIO_PROFILE_ID` is required only for `addToQueue`. `ZERNIO_TIMEZONE` (an IANA zone, `America/New_York` is just an example) is required only for `customScheduled`; `--timezone` overrides it per call, and `shareNow` ignores it.

System tools used by the helpers: `python3`, `ffmpeg`, `curl`, `uv` (builds the shared faster-whisper venv on first use). Nothing else to install: no compiler toolchain.

To fill (or refresh) the `ZERNIO_ACCOUNT_*` ids, run the one hardened command for it, from the repo root, once `ZERNIO_API_KEY` is in the `.env`:

```bash
python3 .claude/skills/auto-poster/scripts/post_to_zernio.py --list-accounts
```

It calls `GET /accounts` with the key from the skill `.env`, prints one paste-ready `ZERNIO_ACCOUNT_<PLATFORM>=<id>    # platform: display name` line per connected account, never prints the key, and exits 0. Paste the lines you want as default targets into `.claude/skills/auto-poster/.env`. Don't improvise a curl for this.

## Fast Path

Use the helper script. Command paths below are written from the repo root (Bash cwd resets there each turn; on Windows use `python` in place of `python3`):

```bash
python3 .claude/skills/auto-poster/scripts/post_to_zernio.py \
  "/absolute/path/to/video.mp4" \
  --caption-file "$CAPTION_FILE" \
  --mode shareNow
```

Where `$CAPTION_FILE` is a path you created in this session — not a hardcoded shared path. See "Temp files" below. No `--platforms` means every account in `.env`.

For a public video URL:

```bash
python3 .claude/skills/auto-poster/scripts/post_to_zernio.py \
  "https://example.com/video.mp4" \
  --caption "Caption goes here" \
  --platforms instagram,tiktok \
  --mode addToQueue
```

If the creator did not provide a caption, run the transcriber and capture the path it prints to stdout:

```bash
TRANSCRIPT_FILE=$(.claude/skills/auto-poster/scripts/transcribe_for_caption.sh "/absolute/path/to/video.mp4")
```

Then read `$TRANSCRIPT_FILE`, write a caption to a path you control, and pass that to `--caption-file`.

For a scheduled post:

```bash
python3 .claude/skills/auto-poster/scripts/post_to_zernio.py \
  "/absolute/path/to/video.mp4" \
  --caption-file "$CAPTION_FILE" \
  --mode customScheduled \
  --due-at "2026-05-18T12:00:00" \
  --timezone "America/New_York"
```

`--timezone` is any IANA zone (the value above is an example); omit it when `ZERNIO_TIMEZONE` is set in the `.env`. The script refuses to schedule with neither.

For a draft:

```bash
python3 .claude/skills/auto-poster/scripts/post_to_zernio.py \
  "/absolute/path/to/video.mp4" \
  --caption-file "$CAPTION_FILE" \
  --mode draft
```

To see the exact payload with zero network calls (no upload, no verify, no post), add `--dry-run`; the local path stands in for the media URL.

## Transcription (faster-whisper)

`scripts/transcribe_for_caption.sh` uses the one transcription engine every skill in this repo shares: faster-whisper in the persistent venv at `~/.cache/content-os/whisper-venv` (built by `uv` on first use or by `./setup.sh`; `CONTENT_OS_WHISPER_VENV` overrides the location). Model defaults to `tiny.en` (fast, plenty for a caption); override with `AUTO_POSTER_WHISPER_MODEL=base.en` (or `small.en`) for more accuracy at a few seconds more per run.

- The script ffmpeg-extracts 16 kHz mono audio first so whisper processes a few MB instead of hundreds.
- First run on a machine builds the venv (about 200 MB) and downloads the model; every run after that reuses the cache and a 90-second reel transcribes in a few seconds on CPU.
- The venv is sentinel-gated on `.deps-ok`, so an interrupted first build rebuilds cleanly next run.

## Temp files (security)

Do not write transcripts, captions, or downloaded media to predictable shared paths like `/tmp/auto-poster-caption.txt`. Anyone with write access to `/tmp` on the host can pre-seed those files and inject content into a post.

Instead:

- Let `transcribe_for_caption.sh` choose its own output path (it creates the transcript file with `mktemp`, mode 600, owned by you, and prints that path on stdout) and read whatever path it prints.
- When you need to write a caption, use a session-scoped path you create — e.g. the agent's outputs directory or `"$(mktemp -t auto-poster-caption.XXXXXXXX)"`.
- Before reading any file you didn't just create, verify it's owned by the current user (`stat -f %Su "$f"` on macOS, `stat -c '%U' "$f"` on Linux) and was modified after the session started. If either check fails, refuse and ask the user.

## Execution Rules

1. If the user did not provide a video path or URL, ask for the video.
2. If the creator provided a caption, use it.
3. If the creator did not provide a caption, run `transcribe_for_caption.sh`, generate a caption from the transcript, and save it to a session-scoped file you created.
4. If the video is a local file, run `post_to_zernio.py` with that path. The script uploads it through Zernio's presigned media upload flow.
5. If the video is already a public URL, pass it directly as the media URL.
6. Default to every account in `.env` unless the creator names platforms.
7. For YouTube, set `--yt-title` if the creator provides one. Otherwise use the filename or first caption line.
8. Report Zernio post IDs, statuses, platform URLs, and errors. The script marks nothing outside Zernio; the session then flips the video's Notion page to `Posted` + `Post Date` (see "What This Skill Does Not Do").

## Caption Rules

Generate the caption from the transcript, not from a generic template. For Instagram, follow the
shape in `engines/content-os/knowledge/ig-caption-patterns.md` (hook line under ~12 words, 25-60 words,
one ask, 5-6 hashtags from `platforms.md`) and the rules below.

- If the transcript includes a real comment/DM CTA the creator said on camera, put that CTA on line 1 and repeat it at the end.
- If there is no spoken CTA, do not manufacture one. Use the strongest hook/take from the transcript and keep it casual.
- Captions carry no link by default (document, don't manufacture). The one exception: if the creator's spoken CTA names the community (exactly as named in `backbone/offer.md`), mirror that CTA in the caption. Never add a link or offer line the video didn't say.
- Keep it direct, conversational, and short enough for IG/TikTok.
- Use line breaks. Avoid numbered lists unless the video itself is clearly a numbered list.
- Threads only accepts captions under 500 characters (see gotchas below); if the caption runs longer, post a trimmed Threads version in its own call.

## Supported Modes

- `shareNow`: sends `publishNow: true`.
- `addToQueue`: sends `queuedFromProfile`, using `ZERNIO_PROFILE_ID`.
- `customScheduled`: sends `scheduledFor` and `timezone`.
- `draft`: sends `isDraft: true`.

For `customScheduled`, `--due-at` is required, and so is a timezone (`--timezone` or `ZERNIO_TIMEZONE` in the `.env`).

## Platform Metadata

The script sends:

- Caption as top-level `content`.
- Video as `mediaItems: [{ type: "video", url }]`.
- Platforms as `{ platform, accountId }` targets from `.env`.
- YouTube title as top-level `title` when posting to YouTube.

## Notes

- Zernio API base URL is `https://zernio.com/api/v1`.
- Zernio uses bearer auth with `ZERNIO_API_KEY`.
- Local files are uploaded via `POST /v1/media/presign`, then `PUT` to the returned upload URL, then posted with the returned `publicUrl`.
- Zernio also has a shorthand examples style using `text`, platform names, and `mediaUrls`; use the helper unless the creator explicitly asks for the raw shorthand payload.

## Known platform gotchas

Hard-won from real runs. Check these before a post, not after it hangs.

- **Threads captions silently fail over 500 characters.** Zernio reports nothing; the Threads post just never lands. If the caption is longer, post the other platforms in one call and Threads in its own call (`--platforms threads`) with a trimmed under-500-character version.
- **Sources over about 100 MB hang Instagram.** Zernio compresses before TikTok but hands the raw file straight to Instagram's Graph API; a big 4K export sits at `awaiting-finalize` for 20+ minutes with no error. Re-encode to 1080p first, keep the framing (don't reframe horizontal to vertical), then post the re-encode:
  ```bash
  ffmpeg -i in.mp4 -vf "scale=-2:1080" -c:v libx264 -crf 20 -maxrate 12M -bufsize 24M -c:a aac -b:a 160k out-1080p.mp4
  ```
- **A stuck Instagram post leaves a live container open.** Never re-post the same video while an earlier record is still stuck: delete the old post record in Zernio first, or it double-posts once the container finalizes.
- **Zernio account IDs go stale after any OAuth reconnect.** The error reads "accounts do not belong to this user". Refresh with `python3 .claude/skills/auto-poster/scripts/post_to_zernio.py --list-accounts` and update the `ZERNIO_ACCOUNT_*` values in the skill `.env` (`.claude/skills/auto-poster/.env` from the repo root; the script reads only that file).

## Resilience (built into the helper)

The helper is hardened against the failure modes that bit us in real runs. You normally don't need to do anything — just know how it behaves:

- **Media reachability check reads the HTTP status code, not a substring of the header dump.** A `Content-Length` like `102040443` contains "404" and used to false-positive the old check. It now retries a few times (uploads can 404 briefly while they propagate) and is a *soft warning* for media we uploaded ourselves (the `PUT` runs with `curl --fail`, so a rejected upload aborts before the post, and Zernio reads the object server-side) — it only hard-fails for a user-supplied URL.
- **A timed-out create never duplicates.** `POST /posts` can succeed server-side even when the client call times out. The helper uses one stable `x-request-id` per logical post and, on any network/timeout error, *reconciles* against `GET /posts` (matching the exact caption, recent posts only) before deciding anything. If the post already landed it reports `source: recovered-after-timeout`; only if nothing is found does it retry, reusing the same request id. So never re-run the script by hand after a timeout — let it reconcile.
- **Create timeout is 240s** (fan-out to all connected platforms takes a while), vs. the old 120s that gave up too early.
- **`source` in the output** tells you whether the post was `created` or `recovered`.

Flags for edge cases:

- `--wait-seconds N` — `shareNow` only: poll the created post until every platform reaches a terminal state (published/failed), up to N seconds. Good for an accurate final report. Ignored for scheduled/queued/draft posts, which never reach a terminal state.
- `--dry-run`: print the payload and exit with zero network calls (no upload, no verify, no post).
- `--skip-verify` — skip the media reachability check entirely.
- `--max-retries N` — safe create retries (default 1); each is reconcile-guarded so it can't duplicate.
