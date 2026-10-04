---
name: imagemagick
description: Use ImageMagick 7 for deterministic still-image and image-sequence conversion, geometry, composition, masking, color, text, drawing, analysis, comparison, animation, metadata, batch work, and production artwork while respecting runtime delegates and security policy.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# ImageMagick

## Workflow

1. Read `../../references/IMAGEMAGICK_TOOLKIT.md`.
2. Inspect source dimensions, format, alpha, colorspace, profiles, and metadata when they affect the requested edit.
3. Query formats, delegates, policy, resources, colorspaces, or fonts if the operation depends on optional runtime state.
4. Use `magick INPUT operations OUTPUT` for ordinary edits so source media is preserved.
5. Use `mogrify` only for explicitly requested in-place batch modification and pass the bridge overwrite guard.
6. Preserve ICC/alpha/bit-depth behavior deliberately rather than relying on filename defaults when fidelity matters.
7. Identify or compare the result after production-critical changes.

## Raw bridge

```bash
python scripts/media_toolkit.py run magick -- ...
```

## Done

The image result exists, requested geometry/format/composition properties were verified, and source media remains intact unless in-place editing was explicitly requested.
