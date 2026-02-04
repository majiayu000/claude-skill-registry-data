---
name: whisper-lolo-audio-ingest
description: Build or modify the browser-side recording and upload pipeline for whisper-lolo. Use when implementing MediaRecorder + IndexedDB chunking, assembling audio blobs, or configuring Vercel Blob client uploads with progress and callbacks.
---

# Whisper Lolo Audio Ingest

## Overview
Implement long-form browser recording with chunked storage in IndexedDB and direct uploads to Vercel Blob, without serverless upload limits.

## Recording workflow
1) Initialize MediaRecorder with a supported mime type.
2) Start with `MediaRecorder.start(timeslice)` to emit chunks.
3) On `dataavailable`, persist each chunk to IndexedDB.
4) On stop, rehydrate chunks and assemble a final Blob.
5) Clear stored chunks after a successful upload.

## Storage guidance
- Do not keep full audio in RAM; always store chunks in IndexedDB.
- Use idb-keyval for simple storage of Blob chunks.
- Guard against empty chunks; some browsers emit zero-size data.

## Upload workflow (client uploads)
1) Use `upload()` from `@vercel/blob/client`.
2) Generate tokens via a server route using `handleUpload`.
3) Persist `blob_url` and update status to `uploaded` after completion.
4) Use `onUploadProgress` for UX feedback on large files.

## Non-negotiable constraints
- Never upload audio via a Next.js API route.
- Do not wait for transcription inside HTTP requests.
- Chunk before transcription; upload only after assembly.

## Common pitfalls
- Check `MediaRecorder.isTypeSupported()` before selecting mime type.
- Resume/pause should not break chunk order in IndexedDB.
- Ensure `onUploadCompleted` works locally only with a tunnel or
  `VERCEL_BLOB_CALLBACK_URL`.

## References to consult
- `documentation/mediarecorder-mdn.md`
- `documentation/web-dictaphone-mdn.md`
- `documentation/idb-keyval.md`
- `documentation/mediarecorder-examples-mozdevs.md`
- `documentation/vercel-blob-client-uploads.md`
- `documentation/vercel-blob-sdk.md`
- `documentation/vercel-blob-examples.md`
