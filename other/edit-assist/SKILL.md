---
name: edit-assist
description: Perform non-destructive deterministic editorial assistance including silence mapping and jump cuts, optional local transcription, subtitle burn-in, exact clipping, subject-aware reframing, and delivery compression.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Edit Assist

1. Read `../../references/EDIT_ASSIST.md` and the approved edit intent.
2. Preserve the source file and write a new output.
3. Use silence detection as evidence, not automatic permission to delete dramatic pauses.
4. Use reviewed subtitle or transcript text when dialogue accuracy matters.
5. Prefer approved focus metadata for reframing; face estimation is only a fallback aid.
6. Treat delivery presets as project defaults and verify current platform constraints when necessary.
7. Run `scripts/edit_assist.py` for deterministic execution and verify the resulting media.

Done when the requested edit-assist operation produced a new verified output or reported the exact missing runtime.
