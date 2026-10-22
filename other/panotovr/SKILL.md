---
name: panotovr
description: Create a Realsee VR space from local equirectangular panoramas using PanoToVR. Use for image-directory or manifest submission, resuming a known VR task, and retrieving its VR URL. For depth maps, point clouds, or camera poses use Argus instead.
---

# PanoToVR

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

PanoToVR uploads panoramas, creates a remote VR task, polls it, and writes `result.json` with `status`, `task_code`, `project_id`, `vr_url`, and `workspace_dir`. This is independent of Argus and local Blender modeling.

## Before execution

- Obtain consent for remote upload and VR task creation. Reuse explicit authorization for the same files and scope. Selecting files alone is not consent.
- Resolve `<skillDir>` as the directory containing this file, regardless of the caller's working directory.
- Require Node.js 22+ and npm 10+. Install locked dependencies with `npm ci --prefix <skillDir> --omit=dev --ignore-scripts --no-audit --no-fund`.
- Configure `REALSEE_APP_KEY`, `REALSEE_APP_SECRET`, and `REALSEE_REGION=global|cn` locally. The runtime reads the process environment or `.env` in the current working directory; it also accepts `CLAUDE_PLUGIN_OPTION_REALSEE_*`. It does not load Argus's credential file. Never request secrets in chat or print them.
- Confirm the account region; the runtime defaults to `global` when omitted. For missing access, use [my.realsee.ai](https://my.realsee.ai/) for global or [my.realsee.cn](https://my.realsee.cn/) for CN. Request the panorama-to-VR API capability through developer@realsee.com with account region, UserID, and IdentityID. Do not send an email without authorization.
- Keep workspaces outside the installed skill and repository. State includes upload receipts and may contain temporary download URLs; treat it as private. The runtime clears proxy environment variables for its own process.

## Execute

Image directory (auto-generated manifest):

```sh
node <skillDir>/scripts/run-panorama-to-vr.mjs --images-dir <imagesDir> --workspace <workspaceRoot> --json
```

Existing manifest (read [input modes](references/input-modes.md) and use [the synthetic template](assets/manifest.example.json)):

```sh
node <skillDir>/scripts/run-panorama-to-vr.mjs --manifest <manifestPath> --images-dir <imagesDir> --workspace <workspaceRoot> --json
```

Resume a known task without packaging, upload, or submission:

```sh
node <skillDir>/scripts/run-panorama-to-vr.mjs --workspace <workspaceRoot> --task-code <taskCode> --json
```

`--workspace` is the parent root, including on resume; the emitted `workspace_dir` is the task subdirectory. Optional `--project-name`, `--poll-interval-ms`, and `--poll-max-attempts` configure new runs/polling. Defaults are 30 seconds and 60 attempts; environment alternatives are `REALSEE_POLL_INTERVAL_MS` and `REALSEE_POLL_MAX_ATTEMPTS`.

## Interpret and recover

Read `result.json` in the emitted workspace and report the task identity, status, workspace, and VR URL when present. A remote error may be returned as `status: error` even with exit code zero; inspect the JSON rather than relying only on exit code. Polling timeout does not prove remote failure. Resume a known task after interruption; if submission may have succeeded without returning a task code, stop and reconcile before submitting again. Do not claim a usable VR link when it is null.

The runtime normalizes JPEG/PNG/WebP to JPEG and checks manifest structure and file matches; it does not enforce Argus's 1–99/RGB8/exact-2:1 validation contract. Confirm equirectangular inputs rather than claiming those checks ran.

Load references only as needed: [API workflow](references/api-workflow.md), [host installation](references/host-differences.md), [troubleshooting](references/troubleshooting.md).
