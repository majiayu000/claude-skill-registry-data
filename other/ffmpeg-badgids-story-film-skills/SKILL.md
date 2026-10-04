---
name: ffmpeg
description: Use the installed FFmpeg and FFprobe capability surface for deterministic video, audio, subtitle, stream, codec, container, filter-graph, metadata, capture, analysis, QC, and delivery operations without hardcoding build-specific features.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# FFmpeg

## Workflow

1. Read `../../references/FFMPEG_TOOLKIT.md`.
2. Probe the actual source streams with FFprobe when stream structure matters.
3. Query the local FFmpeg build for any optional codec, filter, protocol, device, or hardware feature before using it.
4. Choose stream copy when no decode/re-encode is required; otherwise choose explicit codecs and filters appropriate to the delivery requirement.
5. For complex work, construct a reproducible filter graph or portable tool manifest.
6. Never use `-y` through the bridge unless overwriting was explicitly intended.
7. Validate the output with FFprobe and the applicable media/delivery QC.

## Raw bridge

```bash
python scripts/media_toolkit.py run ffmpeg -- ...
python scripts/media_toolkit.py run ffprobe -- ...
```

## Done

The actual output exists, stream/container properties were checked when relevant, and the exact operation can be reproduced from saved arguments or a tool manifest.
