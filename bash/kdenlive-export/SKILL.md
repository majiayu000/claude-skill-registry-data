---
name: kdenlive-export
description: Create a current Generation 5 Kdenlive .kdenlive project from canonical editorial state using Kdenlive document version 1.1, main_bin, sequence and track tractors, MLT playlists, source producers, optional effects/transitions, and portable media references.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Kdenlive Export

## Workflow

1. Read `../../references/EDITOR_PROJECT_EXPORT.md`.
2. Use the canonical advanced editor manifest when multitrack layering or MLT effects/transitions are required.
3. Export with:

```bash
python scripts/editor_project_export.py PROJECT --target kdenlive --require-sources
```

4. Confirm the output contains a Generation 5 `main_bin`, document version `1.1`, sequence tractor with `kdenlive:uuid`, Kdenlive track tractors/playlists, and final project tractor wrapper.
5. Keep media resources project-relative.
6. If a specific installed Kdenlive version must be certified, open the generated project in that version before claiming import success.

## Done

A structurally valid `.kdenlive` project exists at the requested location and represents the declared editorial tracks/cuts/effects without fabricated editor-private state.
