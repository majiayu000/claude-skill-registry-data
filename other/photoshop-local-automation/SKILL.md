---
name: photoshop-local-automation
description: Safely control a user-opened Photoshop on Windows through local automation, including document identity checks, reversible layer edits, save-as or authorized saves, and reopen verification. Use for live Photoshop editing, connection tests, layer creation, drawing, text-item edits, or Photoshop automation troubleshooting. Do not use for file-only raster processing that does not require a live Photoshop document.
---

# Photoshop 本地自动化控制

Use the current user instruction and the live Photoshop document as task-time authority. Treat connection, read, write, save, reopen, and visual acceptance as separate outcomes.

## Entry contract

- Prefer the verified user-open-first route: the user opens Photoshop and the target file, dismisses blocking dialogs, and leaves the target document active.
- Attach only to a visible, responsive Photoshop instance. Do not treat a background automation process or an MCP session read as proof of writable control.
- Before the first mutation, read the active document full path, dimensions, document count, saved state, Photoshop version, and expected target identity.
- Stop before mutation if the active file is not the exact authorized target or if a modal dialog, unknown unsaved document, or ambiguous instance is present.
- Keep one Photoshop instance, one active document, and all save operations serialized.

## Editing

- Use local COM and DoJavaScript when available. Put requested changes in clearly named, independent layers or groups.
- Preserve original layers and pixels. Do not merge, flatten, close, restart, or overwrite unless the current instruction authorizes that exact action.
- Use the smallest reversible test before a new control route touches a user document. Once a route is verified, reuse it rather than retesting connection architecture in the production file.
- If an operation times out, reconcile the active document, layer names, saved state, and output files once before retrying. Never replay a write blindly.

## Saving and acceptance

- Saving is a separate authorization boundary. Prefer a new PSD or PSB path; refuse accidental overwrite unless replacement was explicitly requested.
- For large documents, save as PSB and then close and reopen the saved file. Verify dimensions, layer names and types, group visibility, saved state, and output existence.
- A completed live edit requires direct evidence of the intended layer or pixel result. A completed save additionally requires file readback or reopen evidence.
- Leave Photoshop open unless the user explicitly asks to close it. Never terminate the process while unknown unsaved work may exist.

## Local compatibility

When using Photoshop 2021 on Windows, read [the verified Windows route](references/windows-route.md) before writing COM or ExtendScript control code. It contains the known JSON, PSB-save, hidden-group, and interrupted-run boundaries.
