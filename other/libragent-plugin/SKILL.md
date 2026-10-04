---
name: libragent-plugin
description: >
  Implement, verify, and deploy a host MediaAssist plugin that converts
  audio/image/video into text when the LLM rejects multimodal input (HTTP 400).
  Use when media-assist placeholders appear, assistPluginStatus reports missing,
  listenContent/seeContent succeed but the next completion fails, or the user
  asks to install an ASR/OCR assist plugin. Triggers: media-assist, MediaAssist,
  multimodal 400, deployAssistPlugin, harness-plugins, libragent-plugin.
---

# LibrAgent MediaAssist Plugin

When the model cannot accept audio/image parts, LibrAgent strips them (or runs
a host plugin) and may show:

`[media-assist] ... load @skill:libragent-plugin ...`

This skill installs a **durable host plugin** under app local storage so later
sessions (including Harbor on this machine) auto-convert media.

## Do / Don't

| Do | Don't |
| -- | ----- |
| Implement `manifest.json` + `run` (stdin JSON → stdout JSON) | `apt`/`pip` whisper mid-task as the only fix |
| Verify with `scripts/verify_plugin.py` | Deploy to `system_skills/` or `user_skills/` |
| Deploy via `media__deployAssistPlugin` on **Host** isolation | Call deploy/status from Docker/Harbor attach sessions (blocked) |
| On Windows, ship `run.cmd` / `run.bat` / `run.exe` (optional `run.py` helper) | Rely on a shebang-only extensionless `run` on Windows |
| In Docker/Harbor: convert with in-container CLI (ffmpeg/OCR) | Assume host plugin ACE works from attach mode |

## Contract (interfaceVersion 1)

Plugin dir after deploy: `{appDataDir}/harness-plugins/media-assist/v1/`

`manifest.json`:

```json
{
  "interfaceVersion": 1,
  "name": "my-media-assist",
  "timeoutMs": 120000,
  "modalities": ["audio", "image", "video"]
}
```

`run` (executable): read one JSON object from stdin:

```json
{
  "interfaceVersion": 1,
  "modality": "audio" | "image" | "video",
  "mimeType": "audio/wav",
  "path": "/abs/path/to/media",
  "maxOutputChars": 8000
}
```

Write one JSON object to stdout:

```json
{ "ok": true, "modality": "audio", "text": "…", "notes": "optional" }
```

On failure: `{ "ok": false, "error": "…", "message": "…" }`.

Templates: `templates/manifest.json`, `templates/run` (Unix), `templates/run.cmd`
(Windows). Stubs echo a clear note until you wire real ASR/OCR/VLM.

## Workflow

1. **Status** — `media__assistPluginStatus`
2. **Scaffold** — copy templates into a workspace folder (e.g. `.libragent/media-assist-build/`)
3. **Implement** — replace stub `run` with local ASR (audio), OCR/VLM (image),
   extract+ASR/OCR (video). Prefer already-installed host tools.
4. **Verify** —  
   `python <skill-base-dir>/scripts/verify_plugin.py <plugin-dir>`
5. **Deploy** — Only under **Host** isolation: `media__deployAssistPlugin` with
   `files` containing at least `manifest.json` and `run` content. **Blocked** in
   Docker/Harbor attach sessions (container breakout prevention). There, convert
   media inside the container with CLI tools (e.g. ffmpeg/whisper/tesseract)
   instead of deploying a host plugin.
6. **Confirm** — `media__assistPluginStatus` → `installed: true` (Host isolation).

## Acceptance

- Verify script exits 0.
- Status shows installed modalities.
- A later multimodal 400 is auto-assisted without re-entering this skill.
