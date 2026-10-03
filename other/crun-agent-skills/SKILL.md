---
name: crun-agent-skills
description: Run Crun image, video, audio, music, and media-tool workflows through the bundled standalone runtime. Use whenever the user wants to generate, edit, or transform an image, video, voice, speech, or music clip — even if they never say "Crun" or name a model — as well as for model routing, model-schema inspection, credit estimation, local-media upload, asynchronous task execution, downloading generated media, or inline local previews.
---

# Crun Media Agent Skills

Use this skill as the entry point for Crun media work. Resolve all commands from this directory:

- `runtime/crun_cli.py` handles model discovery, credit checks, task creation, status, polling, local-file upload, and
  generated-media downloads. Upload with `crun_cli.py upload <local-file>`.
- `catalog/models.json` is the local routing catalog.
- `skills/` contains the core pipeline skills, and `skills/scenarios/` the scenario skills, listed below; read the
  relevant child `SKILL.md` before performing that part of the workflow.

## Select the workflow

**Core pipeline skills** — the shared infrastructure every request flows through (route → estimate → create/monitor):

| Need                                        | Read and use                           |
|---------------------------------------------|----------------------------------------|
| Choose a model from a broad request         | `skills/crun-model-router/SKILL.md`    |
| Check balance or affordability              | `skills/crun-account-credits/SKILL.md` |
| Create, monitor, resume, or retrieve a task | `skills/crun-task-runner/SKILL.md`     |

**Scenario skills** (`skills/scenarios/`) — matched by user intent; each one composes the core pipeline internally:

| Need                                                                | Read and use                                            |
|---------------------------------------------------------------------|---------------------------------------------------------|
| Generate static image or animated GIF memes                         | `skills/scenarios/crun-meme-generator/SKILL.md`         |
| Generate multi-panel educational comics & storyboards               | `skills/scenarios/crun-educational-comic/SKILL.md`      |
| Enhance an uploaded image or video                                  | `skills/scenarios/crun-media-enhancer/SKILL.md`         |
| Enhance character action, pose & camera motion (T2I, I2I, T2V, I2V) | `skills/scenarios/crun-action-camera-enhancer/SKILL.md` |
| Generate character reference sheets                                 | `skills/scenarios/crun-character-reference/SKILL.md`    |
| Replicate, restyle, or remake photos (portrait, pose, style)        | `skills/scenarios/crun-photo-replication/SKILL.md`      |
| Discover and apply Kling, Vidu, or ByteDance effect templates       | `skills/scenarios/crun-effect-template/SKILL.md`        |
| Generate promotional images or videos directly from website/product URL | `skills/scenarios/crun-url-promo-generator/SKILL.md`  |

For a broad end-to-end request — the common case where the user describes the media they want but does not know Crun
model names or payloads — follow the "Orchestrate safely" steps below, reading each child skill as that step needs it.
Treat `crun-task-runner` as the single authority for task creation, authorization gates, timeout recovery, failure
handling, and result delivery. Read it before creating any task.

## Pass JSON portably

Prefer a UTF-8 JSON file on Windows and whenever shell quoting is uncertain:

```text
python <skill-root>/runtime/crun_cli.py task estimate --model <model> --input-file <input.json>
python <skill-root>/runtime/crun_cli.py models route --intent-file <intent.json>
```

Use `-` instead of a path to read that JSON object from stdin. Use `--input-json` or `--intent-json` only when the
current shell can preserve the JSON string exactly. Each JSON source must contain one object.

Upload a new local input image, video, or audio file before constructing model input:

```text
python <skill-root>/runtime/crun_cli.py upload <local-file>
```

Use the returned `file_url`. Never send Base64, data URIs, or local paths as Crun media inputs. For derivative work,
reuse the resource URL returned by the earlier Crun task instead of downloading and uploading it again.

## Orchestrate safely

1. Identify the output modality and operation. Collect only indispensable inputs, and require source media for edits,
   references, lip-sync, face-swap, watermark-removal, voice-cloning, and similar transformations.
2. Upload only new local source media (`crun_cli.py upload`); reuse an existing Crun resource URL directly.
3. Route only when the user did not specify an exact model (`crun-model-router`), then inspect the selected model's live
   schema and construct only supported input fields.
4. Estimate the exact model input before every new task (`crun-account-credits`). For a routed model, report the model,
   estimated credits, and relevant settings, then obtain explicit confirmation. Skip only this extra confirmation when
   the user explicitly named the model — never treat the original generation request as the confirmation.
5. Create once with `task create`, capture the returned `task_id`, and continue only with `task wait` or `task status`
   using that ID.
6. Follow `crun-task-runner` for all failures, timeouts, retries, and result delivery.

Use balanced quality and speed when the user has no preference. Ask about native audio only when it changes the viable
models, and do not ask the user to choose a provider unless the alternatives have materially different tradeoffs.

Always estimate affordability before creating any task, including tasks for a user-specified model. Require
`affordable: true` from `task estimate` before `task create`. The reason is that `CreateTask` charges credits and is
never retried, so an unaffordable or malformed submission wastes a real charge that cannot be undone.

Keep `task run` and `media run` only for compatibility or deliberate one-shot use. They create a task directly, so
estimate affordability yourself beforehand and confirm a routed model first — they do not gate on either. Do not use
them as the default agent workflow.

## Handle sensitive media

Before transforming a real person's face or voice, or removing a watermark, require confirmation that the user owns or
is authorized to transform the source. Preserve any disclosure or labeling request. Refuse impersonation, fraud,
non-consensual sexual content, and unauthorized removal of an ownership mark.

Keep API keys out of task payloads, output, and committed files. Let the runtime resolve `CRUN_API_KEY` in this order:
the `~/.crun/.env` file first, then the `CRUN_API_KEY` environment variable. When no key is configured, the runtime
returns `configuration_options` — an ordered list with a permanent setup command for each method split by platform
(`macos_linux`, `windows_cmd`, `windows_powershell`). Recommend the first option: the CLI's own
`python "<absolute path to runtime>/crun_cli.py" config set-api-key <your_api_key>` command (already fully resolved in
the
payload), which validates the key and persists it into `~/.crun/.env` so it works across sessions on every platform.
