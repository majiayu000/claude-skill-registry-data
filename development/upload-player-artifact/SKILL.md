---
name: upload-player-artifact
description: 'Use when a Coworld player needs to checkpoint or upload a debug artifact.'
---

# Upload Player Artifact

Help a Coworld player policy maintain one replaceable debug artifact object, separate from logs, for profiling and
post-hoc analysis. The runner hands each player an upload destination; the player uploads itself.

## Select the artifact path by runtime

Check `game.player_runtime`; see the
[runtime guide](https://github.com/Metta-AI/coworld/blob/main/src/coworld/docs/PLAYER_RUNTIMES.md). For `game-hosted`
players, the game writes a non-empty zip to the seat's `artifact_uri` from `COGAME_PLAYER_SEATS_URI` before publishing
results. It receives no player upload URL. Hosted collection skips files above 200 MiB. The environment, upload steps,
and examples below apply to `platform-hosted` container players.

## Contract

The runner injects one environment variable into the player container:

- `COWORLD_PLAYER_ARTIFACT_UPLOAD_URL` — where this player slot uploads its artifact.
  - Hosted: a slot-scoped HTTP `PUT` endpoint (already authorized, no auth header needed).
  - Local: a `file://` path into the mounted workspace.
  - Absent: the player skips uploading. Always treat this as optional.

Rules the player must follow:

- Maintain exactly one object per player slot. Each successful upload replaces its previous contents.
- Maximum size 200 MiB. Larger uploads are rejected.
- Use HTTP `PUT` with header `Content-Type: application/zip`. No auth header (the URL is presigned).
- For `file://` URLs, just write the bytes to that path (create parent dirs).
- Upload before the container is torn down. The player may upload any time, but once the game finishes the container
  stays alive only for a bounded teardown window. An upload that does not finish before teardown is lost. The platform
  never blocks teardown waiting for an upload.
- A missing or failed artifact never fails an otherwise successful episode. Do not crash the player on upload failure
  unless you want the episode to fail.

See `packages/coworld/src/coworld/docs/artifacts/PLAYER_ARTIFACT.md` for the full artifact contract and
`packages/coworld/src/coworld/docs/roles/PLAYER.md` for the player role.

## Building the zip

The artifact is a single `.zip`. The platform stores and serves the bytes as-is and never unzips them, so the player
decides what goes inside. Bundle whatever you want: parquet, sqlite, csv, json, or raw trace files. The `.zip` extension
is a storage convention, not an enforced format.

Two profiling approaches this enables:

- Sampling profiler: dump all per-step state into one file, zip it, upload. Useful early, becomes noise once you know
  what matters.
- Tracing profiler: record only specific named events. Better for optimization once you know what to look for.

Keep the zip well under 200 MiB. If a sampling dump is too large, downsample, compress columns (parquet), or switch to
tracing specific events.

## Steps

1. Read `COWORLD_PLAYER_ARTIFACT_UPLOAD_URL` from the environment. If it is empty or unset, skip the upload entirely and
   return.
2. Collect debug data into one or more in-memory files while the episode runs.
3. Periodically, and after the final game message, build a `.zip` of the latest files in memory.
4. `PUT` the zip bytes to the URL with `Content-Type: application/zip`. For `file://` URLs, write the bytes to the path
   instead. Finish before the container exits.
5. Do not raise on upload failure unless losing the artifact should fail the episode; log and move on, since a missing
   artifact never fails an otherwise successful episode.

## Python example

Players in this repo are Python containers. The `python:3.12-slim` Coworld image already ships `requests`, `pyarrow`,
and `websockets`. This helper covers both `https://` (PUT) and `file://` (local) URLs:

```python
import io
import os
import zipfile
from urllib.parse import unquote, urlparse

import requests


def upload_player_artifact(files: dict[str, bytes]) -> None:
    """Zip `files` (name -> bytes) and upload to the per-slot artifact URL, if set.

    Safe to call unconditionally: a missing env var or failed upload is ignored, since a
    missing artifact never fails the episode.
    """
    url = os.environ.get("COWORLD_PLAYER_ARTIFACT_UPLOAD_URL")
    if not url:
        return  # No URL: artifact upload is disabled for this run.

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    payload = buffer.getvalue()

    parsed = urlparse(url)
    if parsed.scheme == "file":
        path = unquote(parsed.path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(payload)
        return

    # Presigned PUT. No auth header: the URL is already authorized.
    response = requests.put(url, data=payload, headers={"Content-Type": "application/zip"}, timeout=60)
    response.raise_for_status()
```

Call it periodically for checkpointing and after the player receives the `final` message:

```python
async for raw_message in websocket:
    message = json.loads(raw_message)
    if message["type"] == "final":
        upload_player_artifact({
            "trace.parquet": trace_table_bytes,   # tracing profiler output
            "summary.json": summary_json_bytes,
        })
        return
    ...
```

If you prefer no third-party dependency, the runner's own helper `packages/coworld/src/coworld/runner/io.py`
(`upload_data(url, data, content_type="application/zip")`) does the same PUT with retries using only the standard
library.

## Nim example

There is no Nim player in this repo today, so a Nim player would be net-new. If you write one, use `curly` (the
Softmax-standard Nim HTTP client) for the upload and `zippy` for the zip. Handle the timeout and `response.code`
explicitly.

```nim
import std/[os, strutils], curly, zippy

let curl = newCurlPool(1)

proc uploadPlayerArtifact(files: seq[(string, string)]) =
  ## Zip `files` (name, contents) and upload to the per-slot artifact URL, if set.
  let url = getEnv("COWORLD_PLAYER_ARTIFACT_UPLOAD_URL")
  if url.len == 0:
    return                       # No URL: artifact upload is disabled for this run.

  # Build the zip in memory. ZipArchive maps entry name -> contents.
  var archive = ZipArchive()
  for (name, contents) in files:
    archive.contents[name] = ArchiveEntry(contents: contents)
  let payload = archive.writeZipArchive()

  if url.startsWith("file://"):
    let path = url[len("file://") .. ^1]
    createDir(path.parentDir())
    writeFile(path, payload)
    return

  # Presigned PUT. No auth header: the URL is already authorized.
  let response = curl.put(
    url,
    @[("Content-Type", "application/zip")],
    payload,
    60.0'f32
  )
  if response.code < 200 or response.code >= 300:
    # A missing artifact never fails the episode; log instead of crashing.
    echo "artifact upload failed: HTTP ", response.code, " ", response.body
```

## Review checklist

- The player reads `COWORLD_PLAYER_ARTIFACT_UPLOAD_URL` and skips cleanly when it is absent.
- Every upload replaces the slot's one `.zip` object and stays well under 200 MiB.
- The PUT sets `Content-Type: application/zip` and no auth header.
- `file://` URLs are handled for local runs (write bytes, create parent dirs).
- The upload completes before the player exits / the container is torn down.
- Upload failure is logged, not fatal (unless failing the episode is intended).
