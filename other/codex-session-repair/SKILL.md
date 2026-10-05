---
name: codex-session-repair
description: Diagnose and repair local Codex Desktop/CLI session JSONL files when a thread cannot resume or compact because of context_length_exceeded, invalid image_url, huge compacted records, inline data:image/base64 payloads, or oversized tool/image outputs. Use for Codex thread/context auto-compaction failures and local session bloat recovery.
---

# Codex Session Repair

Use this skill when a Codex thread fails to continue, resume, or auto-compact with errors such as:

- `context_length_exceeded`
- `Error running remote compact task`
- invalid `image_url`
- missing or broken context/compaction behavior after a long image-heavy thread
- huge `compacted`, `function_call_output`, `input_image`, or `data:image` records in `~/.codex/sessions`

## Safety Rules

Codex session JSONL files are user assets. Treat repair as a high-risk local-data operation.

- Start read-only: locate the session and diagnose size/pathology first.
- Never delete session files.
- Always create a backup before generating a repaired candidate.
- Default to candidate-only repair. Apply replacement only after explicit user confirmation.
- Store repair artifacts outside synced/project source folders. The bundled script defaults to a local app-data repair folder.
- Do not paste full session contents into chat or public reports.
- If a thread is currently open in the Desktop app, writes may fail or the UI may need an app restart to reload the repaired file.

## Typical Workflow

1. Locate the target session.
   - Search `$env:USERPROFILE\.codex\session_index.jsonl`, `.codex-global-state.json`, and `sessions\**\*.jsonl` for the thread name or session id.
   - Prefer the exact session JSONL path under `$env:USERPROFILE\.codex\sessions\...`.

2. Diagnose before repairing.
   - Check file size, line count, largest lines, `compacted` lines, `input_image`, `image_url`, `data:image`, and base64 image signatures such as `iVBORw0KGgo`.
   - If the issue is just a remote outage, do not modify local history.
   - If a thread contains large inline image/base64/tool-output records, continue.

3. Generate a candidate.
   - Run `scripts/repair-codex-session.ps1` without `-Apply`.
   - Review the report: parse errors should be `0`, large rows should drop sharply, and `input_image` / `image_url` should be removed from model-visible history.

4. Apply only after confirmation.
   - Run the same script with `-Apply`.
   - The script refuses to overwrite if the source changed after backup.

5. Verify.
   - Validate JSONL parse status and counts.
   - Use a light `codex exec resume --ephemeral` prompt when appropriate:
     `codex exec resume --ephemeral --skip-git-repo-check <SESSION_ID> "本地修复验证。请不要调用工具，只回复 OK。"`
   - Success criteria: resume returns normally; no `context_length_exceeded`; no invalid `image_url`.

## Script Usage

Candidate-only mode:

```powershell
& "$env:USERPROFILE\.codex\skills\codex-session-repair\scripts\repair-codex-session.ps1" `
  -SessionFile "<SESSION_FILE>"
```

Apply mode after user confirmation:

```powershell
& "$env:USERPROFILE\.codex\skills\codex-session-repair\scripts\repair-codex-session.ps1" `
  -SessionFile "<SESSION_FILE>" `
  -Apply
```

The repair replaces historical image objects and inline image/base64 payloads with short text placeholders while preserving normal text history, timing, and event structure.

## What This Fixes

This fixes local session bloat caused by historical image payloads being kept in model-visible history. It can make old threads resume and compact again.

It does not prevent future bloat if the same thread keeps accumulating screenshots, generated images, huge logs, or massive tool outputs. For image-heavy work, prefer a dedicated task thread and keep the repaired advisor/coordination thread mostly text-based.
