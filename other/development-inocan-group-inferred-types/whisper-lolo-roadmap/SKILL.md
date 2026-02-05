---
name: whisper-lolo-roadmap
description: Guide development of the whisper-lolo project based on specifications-projet.md. Use when planning or executing a sprint/PR, validating scope or constraints, or aligning architecture, statuses, and DoD for the Next.js + Vercel + Blob + Inngest + Whisper stack.
---

# Whisper Lolo Roadmap

## Overview
Apply the project roadmap and constraints to keep each PR aligned with the sprint goals, status model, and non-negotiable rules.

## Workflow

### 1) Identify the sprint and scope
- Confirm which sprint (0..5) the task targets.
- Keep the PR limited to one sprint and its Definition of Done.
- When unsure, ask which sprint the change belongs to.

### 2) Re-assert hard constraints
- Never upload audio via a Next.js API route.
- Never wait for transcription inside an HTTP request.
- Always chunk, store, upload direct, then process async.
- Chunk before transcription.

### 3) Maintain data model and statuses
- Use `recordings.status`: draft | recording | uploaded | transcribing | done | error.
- Use `transcriptions.status`: pending | done | error.
- Update status transitions explicitly in code paths.

### 4) Apply sprint DoD checks
- Sprint 0: migrations applied, endpoint test ok, `/record` reachable.
- Sprint 1: 10 minutes stable, refresh restores chunks, blob playable.
- Sprint 2: long upload ok, Blob URL reachable, DB updated.
- Sprint 3: event received, job starts automatically.
- Sprint 4: transcription stored, errors handled, logs clear.
- Sprint 5: status shown, text rendered, copy/export works.

### 5) Reference project docs
- Read `specifications-projet.md` for the authoritative roadmap.
- Use `documentation/` summaries to confirm API behaviors.

## Key decisions to preserve
- Next.js App Router + TypeScript.
- Inngest for long-running jobs.
- Vercel Blob client uploads.
- Provider abstraction for Whisper now, Voxtral later.

## References to consult
- `specifications-projet.md`
- `documentation/vercel-blob-overview.md`
- `documentation/vercel-blob-sdk.md`
- `documentation/inngest-background-jobs.md`
- `documentation/openai-node-audio-example.md`
