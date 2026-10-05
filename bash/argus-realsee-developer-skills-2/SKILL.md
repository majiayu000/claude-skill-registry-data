---
name: argus
description: Use this skill to process one to 99 local exact 2:1 equirectangular panorama images with Realsee Argus, producing depth maps, a merged GLB point cloud, camera poses, optional intrinsics, and a validated local output index. Trigger for Argus panorama reconstruction, Argus ZIP input, or explicit Argus start/status/collect lifecycle requests. Do not trigger for panorama editing or stitching, arbitrary-photo 3D generation, existing GLB inspection, or research-only questions.
compatibility: Requires a POSIX shell, Node.js 22+, npm 10+, npm registry access, and network access to app-gateway.realsee.ai or app-gateway.realsee.cn
metadata:
  version: "2.2.0"
  documentation: README.md
---

# argus

Use this Skill to submit 1–99 exact 2:1 equirectangular panoramas to Realsee Argus and collect a validated `output.zip`. The public entrypoint is `scripts/run-argus.mjs`; `<skillDir>` below means the directory containing this file.

Treat the official product, demo, research, and developer sites as background only. Do not infer arbitrary-photo input or other product workflows from them; follow the narrower Skill 2.0 contract in this file.

Argus is a remote upload. Do not upload until the user has selected the input and consented. Never print or log credentials, upload tokens, presigned URLs, or raw provider errors. Keep tokens and signed URLs out of persistent state; store app credentials only with explicit user authorization as described below. Do not open output files unless the user asks.

## 1. Ensure runtime dependencies

Skill installers copy the canonical package but may not install its Node.js dependencies. Before the first Argus command in an installed Skill directory, check all four runtime packages without printing any sensitive data. If any are absent, install the exact lockfile once:

```bash
test -f "<skillDir>/node_modules/@realsee/universal-uploader/package.json" \
  && test -f "<skillDir>/node_modules/@aws-sdk/client-s3/package.json" \
  && test -f "<skillDir>/node_modules/ajv/package.json" \
  && test -f "<skillDir>/node_modules/yauzl/package.json" \
  || (cd "<skillDir>" && npm ci --omit=dev --ignore-scripts --no-audit --no-fund)
```

Do not replace `npm ci` with an unlocked install. If the package cannot be resolved, stop and report the install error; do not begin an upload.

## 2. Resolve credentials

The runtime requires `REALSEE_APP_KEY`, `REALSEE_APP_SECRET`, and `REALSEE_REGION` (`global` or `cn`). The Gateway base is unchanged: global uses `app-gateway.realsee.ai`; CN uses `app-gateway.realsee.cn`. In the CN-only Arkclaw distribution, use `cn` and do not offer the global region.

Resolve values in the existing order:

1. Probe the current shell environment without printing values:

   ```bash
   [ -n "${REALSEE_APP_KEY:-}" ] && [ -n "${REALSEE_APP_SECRET:-}" ] \
     && [ -n "${REALSEE_REGION:-}" ] && echo present || echo missing
   ```

2. If configuration is incomplete and `~/.realsee/credentials` already exists, load it into the shell and probe presence. Never display the file:

   ```bash
   [ -f ~/.realsee/credentials ] && set -a && . ~/.realsee/credentials && set +a; \
     [ -n "$REALSEE_APP_KEY" ] && [ -n "$REALSEE_APP_SECRET" ] && [ -n "$REALSEE_REGION" ] \
     && echo present || echo missing
   ```

3. If values are still missing, ask only for the missing configuration. Have the user configure secrets through their local shell or a secure credential interface without echoing them into chat. Never repeat a supplied value. If the user explicitly chooses persistent storage, use `~/.realsee/credentials` with mode 0600 outside the repository. Never place credential values in a CLI argument or environment prefix recorded by the host.

## 3. Select the input

Two mutually exclusive modes are supported:

- repeat `--image <absolute-path>` for 1–99 local images; or
- pass one `--zip <absolute-path>` containing root-level images.

The CLI performs authoritative validation and deterministic packaging. Inputs must be JPEG, PNG, or WebP, RGB, 8-bit, and exactly `width == 2 * height`. A resolution below 2048×1024 emits a warning. Square 1:1 images are rejected; users who require the old square/single-GLB workflow must pin `v1.0.2`.

ZIP mode is not a validation bypass. The CLI safely extracts, validates, Unicode-normalizes, sorts, and repacks it before upload. Do not manually rename output IDs: consumers trust the algorithm's `name_mapping`.

The Skill ships only `examples/manifest.json`, which lists two first-party example sets and their CDN URLs, byte lengths, and SHA-256 digests. Panorama JPEGs are absent from the current release tree and every generated distribution. If the user wants official examples, ask them to choose a region and an absolute output directory outside `<skillDir>`, then run:

```bash
node <skillDir>/scripts/download-examples.mjs \
  --region cn \
  --output "/absolute/example-output"
```

The downloader publishes the directory only after every file passes its manifest byte-length and SHA-256 checks. Do not create, rename, or replace the requested output path or its parent while the command is running. Use `global` instead of `cn` when appropriate; the CN-only Arkclaw distribution only allows `cn`. Downloading does not consent to a later Argus upload. Before `start`, the user must still select the downloaded files and consent to sending them to Realsee. See the [example panorama guide](references/examples.md) and its [Chinese version](references/examples.zh-CN.md).

## 4. Start once

Before starting, ensure the user has selected the files and consented to sending them to Realsee for remote processing. An explicit request to upload those files is sufficient; file selection alone is not consent. If either is missing, ask one question stating that the selected files will leave the machine. Reuse existing consent for the same input and scope. Do not ask a redundant second confirmation.

Run lifecycle commands in a shell with credentials resolved in step 2. For repeated images:

```bash
node <skillDir>/scripts/run-argus.mjs start \
  --image "/absolute/path/a.jpg" \
  --image "/absolute/path/b.webp" \
  --workspace "/absolute/workspace-root" \
  --yes --json
```

For an existing ZIP:

```bash
node <skillDir>/scripts/run-argus.mjs start \
  --zip "/absolute/path/input.zip" \
  --workspace "/absolute/workspace-root" \
  --yes --json
```

When starting a new shell for `status` or `collect`, resolve credentials there before invoking the command. Capture `workspace_dir` from the JSON response; it is the durable run handle for later commands.

`start` validates and packages locally, uploads one ZIP, submits once, persists `task_code`, and returns. It does not poll in the background. Never automatically rerun `start` after `submission_unknown`: the submit operation is not idempotent and a blind retry may create a duplicate task.

## 5. Query status explicitly

Run one status query:

```bash
node <skillDir>/scripts/run-argus.mjs status \
  --workspace "<workspace_dir>" --json
```

Interpret `task_status` as `queued`, `processing`, `succeeded`, or `failed`. When queued or processing, report the current state and query again later only when appropriate. There is no detached poller and no `--resume` mode.

## 6. Collect a terminal result

When the task succeeds, run:

```bash
node <skillDir>/scripts/run-argus.mjs collect \
  --workspace "<workspace_dir>" --json
```

`collect` retains the original `output.zip`, safely extracts it, validates `output.json` and all referenced artifacts, and writes a local `result.json` index. Repeating `collect` is safe: a completed run is not resubmitted or downloaded twice.

Report these fields separately:

- `task_status`: remote lifecycle state;
- `result_status`: algorithm result (`success`, `partial`, or `error`);
- local `output_zip_path`, output directory, manifest, merged GLB, depth-map, pose, and optional intrinsics paths;
- `missing_ids` and warnings.

For `partial`, the CLI exits 0. Still show a prominent warning and the complete non-empty `missing_ids` list. For `error`, surface the sanitized error and treat the command as failed. Do not present temporary result URLs as durable output.

## References

- [Argus](https://argus.realsee.ai/)
- [Interactive demo](https://h5.realsee.ai/argus)
- [Research](https://argus-paper.realsee.ai/)
- [Realsee Developer Platform](https://developer.realsee.ai/)
- For lifecycle implementation details: [Gateway workflow](references/api-workflow.md)
- When checking request/response fields: [Gateway OpenAPI](references/argus-gateway-openapi.json)
- When interpreting or validating artifacts: [Algorithm I/O contract](references/algorithm-io.md) / [中文](references/algorithm-io.zh-CN.md)
- [Official example panoramas](references/examples.md) / [中文](references/examples.zh-CN.md)
- [`output.json` JSON Schema](references/argus-output.schema.json)
- For older inputs or integrations: [2.0 migration guide](references/migration-v2.md) / [中文](references/migration-v2.zh-CN.md)
- When a command fails: [Troubleshooting](references/troubleshooting.md)
