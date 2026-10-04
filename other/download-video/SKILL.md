---
name: download-video
description: Identify and download individual video URLs from Douyin, TikTok, Bilibili, YouTube, and X/Twitter into verified local media artifacts. Use when a user asks to save a supported social video, when another skill needs a local video from a URL, or when diagnosing whether one of those links is downloadable. Require explicit authorization before reading browser cookies; never treat metadata, a thumbnail, or a partial file as a successful video download.
---

# Download video

Produce one local, playable video and a verified
`awesome-capture.artifact/v2` commit marker. Keep acquisition separate from
transcription and analysis.

## Workflow

1. Extract exactly one `http` or `https` video URL from the request. Ask which URL only when multiple candidates remain.
2. Run the deterministic detector:

   ```bash
   python3 scripts/download_video.py detect "<url>"
   ```

   `detect` returns only the sanitized public URL and its SHA-256 source
   fingerprint. It never echoes signed or unknown query parameters.
3. Run `doctor` once per environment. It checks the tools and the secure POSIX
   runtime. If the runtime is unsupported, `yt-dlp` is stale, or
   `ffmpeg`/`ffprobe` is missing, report the exact remediation before
   downloading.
4. Try anonymous download first. `--output-dir` must be absolute. The script
   restricts yt-dlp to the detected platform extractor, disables the generic
   extractor, and confines downloader output to private staging:

   ```bash
   python3 scripts/download_video.py download "<url>" --output-dir "<absolute-dir>"
   ```

5. Apply only the bounded fallback for that platform:
   - Douyin `FRESH_COOKIES_REQUIRED`: the default `auto` mode may open an isolated headless Chromium context, collect short-lived anonymous `.douyin.com` cookies, retry once, then delete the temporary Cookie file. It never reads the user's browser profile. Report `auth_mode: ephemeral_browser`.
   - TikTok/X recoverable extractor or IP rejection: use `gallery-dl` once when installed. Do not use it for login, private, deleted, geo-restricted, or rate-limited content.
   - Any platform requiring the user's session: use `--cookies <netscape-file>` or `--cookies-from-browser <browser[:profile]>` only after the user explicitly authorizes that named source. Never enumerate browser profiles automatically.
6. Treat success as valid only when the script exits zero and returns an
   artifact whose schema is `awesome-capture.artifact/v2`, type is `video`,
   status is `complete`, `media.has_video` is true, and current media
   bytes/hash/ffprobe facts all match.
7. Return `media_path` and `artifact_path` from the result. Pass
   `artifact_path` explicitly as `transcribe-media --source-artifact`; never
   infer a manifest filename. Do not transcribe unless the user also requested
   it.

If a process was interrupted, recovery is also run automatically for that
source before the next download. It can be invoked explicitly:

```bash
python3 scripts/download_video.py recover \
  --output-dir "<absolute-dir>" \
  --lock-timeout 30
```

Recovery completes transactions whose journal and hashes agree, quarantines
unjournaled private staging, and returns `RECOVERY_CONFLICT` for unknown or
changed state. It never overwrites or deletes an unproven file.

## Reliability rules

- Supported secure runtime: macOS or Linux, Python 3.11 through 3.14, with
  `fcntl`, `dir_fd`, `O_NOFOLLOW`, `O_DIRECTORY`, directory `fsync`, atomic
  no-replace rename, and atomic exchange rename.
  Filesystem-mutating commands fail closed with `UNSUPPORTED_PLATFORM` when a
  required primitive is unavailable.
- Keep `--ignore-config` enabled through the bundled script so machine-global yt-dlp settings cannot change behavior.
- Default to one video. This first version intentionally rejects playlist expansion; add a separate batch adapter later.
- Never bypass DRM, paywalls, private access, or platform authorization.
- Never log, copy, or persist Cookie values in the manifest.
- Reject filesystem roots, the user's home directory, parent traversal,
  symlinked path components, unsafe owner/mode, special files, and managed
  hardlinks.
- Use the persistent per-source lock under the managed root. The default
  `--lock-timeout` is 30 seconds; timeout returns `RESOURCE_BUSY`. Never delete
  the lock file as an unlock mechanism.
- External downloaders may write only beneath a new private staging directory.
  Their child working directory is pinned by an already-open directory FD and
  output arguments remain relative to that directory.
  Require exactly one complete regular media file, positive-duration video
  from ffprobe, and matching bytes/SHA-256 before publication.
- Do not adopt an arbitrary pre-existing media file. Reuse is allowed only for
  a matching v2 artifact whose media is strictly revalidated.
- Do not promise that anonymous downloading works on every network. Anti-bot sites require a current authorized session or a different network.
- The bundled X/Twitter yt-dlp and gallery-dl routes force IPv4. This is a
  transport compatibility choice for observed X media-CDN TLS EOF failures;
  it does not disable certificate checks, add authentication, or affect other
  platforms.
- Keep the Douyin browser fallback isolated and anonymous. If it would require login, stop and obtain explicit user direction.
- Prefer `yt-dlp 2026.07.04` or newer; that release repaired observed Bilibili extraction and includes security fixes absent from the installed 2026.03.17 build.
- Read [platforms.md](references/platforms.md) when handling authentication, anti-bot errors, format selection, or platform-specific limitations.

## Output contract

Success prints exactly one JSON object to stdout; expected failures print one
redacted JSON error to stderr with stdout empty. Success exits 0; the
repository-wide failure codes are: 2 for arguments, schemas, or unsafe
inputs/paths; 3 for unavailable dependencies, models, or platform
capabilities; 4 for locks, conflicts, recovery conflicts, or stale plans; 5
for external-tool, network, or runtime I/O failures; 7 for contract, identity,
or file-evidence integrity failures; and 130 for interruption. A successful
download publishes under:

```text
<output>/.awesome-capture-media/v2/
├── locks/<source-fingerprint>.lock
├── staging/
├── quarantine/
└── downloads/<platform>/<source-fingerprint>/<media-sha256>/
    ├── media.<ext>
    ├── source.info.json
    └── artifact.json
```

Managed directories use mode `0700`; media, metadata, journals, locks, and
artifacts use `0600`. `source.info.json` is sanitized source metadata, not raw
extractor output. `artifact.json` is written last and is the only completion
marker.

The video artifact records the sanitized source fingerprint, absolute media
path, bytes, SHA-256, integer duration, video/audio stream counts, container,
actual auth/fallback, warnings, producer tool/version, and the vendored
contract digest. Producers validate it before publication; consumers must
validate the same canonical contract and recheck authorized file context.

This is a breaking contract change. `awesome-capture.artifact/v1`, absent
versions, unknown versions, and legacy adjacent `<media>.artifact.json` files
are rejected. There is no implicit migration, dual read, or legacy fallback.
