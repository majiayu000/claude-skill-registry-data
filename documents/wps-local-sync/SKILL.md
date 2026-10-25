---
name: wps-local-sync
description: Use local WPS Office on Windows to safely inspect, edit, format, export, and reopen-verify DOCX, XLSX, and PPTX files when the user asks to use WPS, synchronize AI work with the installed desktop app, preserve WPS compatibility, or troubleshoot a WPS-native document workflow. Do not use for ordinary file-only authoring when WPS-native execution or compatibility is irrelevant.
---

# WPS Local Sync

Use WPS itself as the compatibility and execution layer. Keep artifact-specific skills in charge of document, spreadsheet, presentation, or PDF quality; this skill adds the local WPS bridge, native reopen verification, and safe UI fallback.

## Route the task

1. Use background COM through `scripts/invoke_wps_cli.ps1` for operations listed as `verified_background` in the capability matrix. Do not infer support from a command name or zero exit code.
2. Use screenshot/OCR and mouse or keyboard simulation only when the target is already open in WPS, a WPS-only dialog blocks progress, or native visual state cannot be inspected in the background.
3. For complex first-time authoring, create the artifact with the relevant artifact skill, then use this skill to reopen, validate, and export it through WPS.
4. Read [references/local_environment.md](references/local_environment.md) before changing the bridge or diagnosing COM. Read [references/commands.md](references/commands.md) for invocation examples.
5. Read [references/native_capability_matrix.md](references/native_capability_matrix.md) before claiming support for a WPS ribbon command, cloud/AI feature, macro, dialog, or native PDF operation.
6. For multiple files, active WPS work, or concurrency conflicts, read [references/parallel_sessions.md](references/parallel_sessions.md). Do not interpret another WPS task's existence as a global busy condition.

## Protect the user's work

- Preserve the source unless the user explicitly authorizes in-place editing. Create a sibling working copy such as `<stem>_WPS工作副本.<ext>` and keep the original untouched.
- Record the exact target path and its size, modification time, and SHA-256 before mutation. Recheck them after saving.
- Different components (for example Calc + Impress) and distinct target paths may run concurrently through the updated wrapper. It leases only the required components and file paths; the backend uses `DispatchEx` and rejects an already populated or visible returned COM session before hiding, hardening, opening, or quitting it. `-AllowVisibleWps` is retained for argument compatibility, not as a safety bypass.
- The legacy CLI still serializes calls of the same component because its services use active-document state and application-level teardown. Multiple PPTs can instead be operated through explicitly bound Presentation objects under a shared-session owner; follow the tested limits in `parallel_sessions.md`, never launch competing legacy CLI calls against that shared session.
- Do not dismiss Save, Save As, overwrite, compatibility, recovery, or macro prompts blindly. Identify the dialog with a fresh screenshot/OCR first.
- On an error or timeout, reconcile the file state and WPS process state before retrying the same write.

## Run the local bridge

Invoke the wrapper from PowerShell and pass each CLI token as a separate array item:

```powershell
& (Join-Path $env:USERPROFILE '.codex\skills\wps-local-sync\scripts\invoke_wps_cli.ps1') `
  -CommandArgs @('writer', 'info', 'C:\absolute\document.docx', '--json')
```

Run the wrapper in the actual Windows user context and follow the current tool permission profile. A negative COM probe from a restricted process context is not authoritative; do not force an escalation option unsupported by the current environment.

Expect JSON for operational commands. Treat a zero exit code or `success: true` as command evidence only, not final acceptance.

## Use the UI fallback without taking over the desktop

1. Capture a fresh screenshot and verify the WPS app, document name, and active dialog.
2. Perform one bounded mouse or keyboard action.
3. Capture again and verify the effect before the next action.
4. Stop if the target identity, button meaning, focus, or resulting state is ambiguous.
5. Never run an uninterrupted click sequence or reuse stale coordinates after the window changes.

The user permits screenshots, OCR, and simulated input, but not uncontrolled pointer capture. Keep the interaction short and observable.

## Acceptance gate

For a mutation, require all applicable evidence:

- The intended output path exists and the original remains preserved.
- The expected size, modification time, or SHA-256 delta occurred.
- A separate WPS invocation closes and reopens the saved file successfully.
- A read command confirms the requested content or structure after reopen.
- Layout-sensitive work is exported or rendered and visually inspected with the relevant artifact skill.
- The owned session has closed without residual modal UI. Inspect any remaining processes; unrelated concurrent or user-owned WPS processes may legitimately remain and must not be killed.

State format support precisely. A verified DOCX path does not prove XLSX or PPTX automation until those paths have their own real write-and-reopen evidence.

Published COM or JSAPI documentation proves discoverability, not reliable background execution. Put each new operation through an isolated real-file adapter test before using it on a production document.

## Failure handling

- `WPS_RESOURCE_BUSY`: only the named component or path conflicts. Continue authorized work on unrelated resources; serialize the conflicting legacy CLI calls or use the tested explicit-object multi-file route. Do not ask the user to close all WPS windows.
- `WPS_FOREIGN_SESSION`: the actual returned COM session is populated or visible. Leave it untouched, do not retry another ProgID as a bypass, and use an explicitly owned object/session route or a bounded UI route for that target. Other component types remain available.
- `WPS_COM_TIMEOUT`: the wrapper stops its CLI only. It no longer force-kills WPS by a global process difference, which could kill a concurrent job. Inspect the exact target/session and reconcile hashes before retrying or performing ownership-proven cleanup.
- COM ProgID failure: consult `local_environment.md`; do not repeatedly run repair commands or change registration without evidence.
- A command-specific COM incompatibility: reproduce on an isolated fixture, add a focused regression test to the pinned local fork, and rerun the real WPS operation before accepting the patch.
- `WPS_WRITER_MUTATION_UNVERIFIED`: `writer replace`, `writer merge`, and `writer table-insert` are quarantined on this WPS build because real close/reopen tests found non-persistence or ambiguous insertion. Author or edit the DOCX with the document artifact skill, then use WPS for reopen, validation, and export.
- `WPS_IMPRESS_TRANSITION_UNVERIFIED`: `impress transition-set` is quarantined because WPS returned success but restored the default transition after close/reopen. Use a bounded visible WPS action only when the user explicitly needs the native transition.
- `WPS_PDF_UI_REQUIRED`: local WPS PDF mutation launches a visible reader on this build. Use the PDF artifact skill for file-level PDF work, or use one explicitly authorized bounded UI action.
