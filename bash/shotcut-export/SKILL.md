---
name: shotcut-export
description: Create an editable Shotcut .mlt project from canonical editorial state using MLT XML plus Shotcut project, bin, track, audio-mix, effect, transition, subtitle, and portable resource metadata.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Shotcut Export

## Workflow

1. Read `../../references/EDITOR_PROJECT_EXPORT.md`.
2. Use the advanced editor manifest for multitrack editing or optional MLT filters/transitions.
3. Export with:

```bash
python scripts/editor_project_export.py PROJECT --target shotcut --require-sources
```

4. Confirm the output has `main_bin`, named Shotcut timeline playlists, `shotcut:projectAudioChannels`, a main tractor marked `shotcut=1`, background track, audio mixing, and declared media/effects.
5. Keep media resources project-relative.
6. If a specific installed Shotcut version must be certified, open the generated file in that version before claiming import success.

## Done

A structurally valid Shotcut `.mlt` project exists and represents the declared editorial state without reverse-engineered or undocumented private data.
