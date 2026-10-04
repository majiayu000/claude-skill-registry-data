---
name: programmatic-video
description: Create portable frame-deterministic programmatic video compositions and optionally translate them into a Remotion project for complex motion graphics, explainers, maps, kinetic typography, data-driven video, and reusable campaign templates.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Programmatic Video

1. Read `../../references/PROGRAMMATIC_VIDEO.md`.
2. Write `05_post/programmatic/compositions.json` using stable `COMP-###` IDs and project-relative assets.
3. Keep timing in frames or exact seconds derived from declared FPS.
4. Use `scripts/remotion_adapter.py scaffold` only when Remotion is a useful implementation target.
5. Do not bundle Remotion or assume the user is license-eligible.
6. Preserve user edits to generated code on later passes.
7. When rendering is requested, require an installed/configured Remotion runtime and explicit license acknowledgement before invoking it.
8. Register the final render in the media registry and QC it.

Done when the portable composition exists and any requested renderer-specific implementation has been generated or truthfully blocked.
