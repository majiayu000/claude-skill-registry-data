---
name: youtube-content
description: Compatibility alias for the canonical `yt-dlp` YouTube skill.
---

# youtube-content (Compatibility Alias)

This skill is retained for backward compatibility only.

Canonical YouTube workflow now lives in:
- `skills/media/yt-dlp/SKILL.md`
- `skills/media/yt-dlp/scripts/fetch_transcript.py`

When this skill is invoked:
1. Follow `yt-dlp` skill instructions as the source of truth.
2. Use the canonical transcript helper in `yt-dlp/scripts/`.
3. Keep all temporary outputs under `data/tmp/yt-dlp`.

Legacy helper path compatibility is preserved:
- `skills/media/youtube-content/scripts/fetch_transcript.py`
  delegates to the canonical helper under `yt-dlp/scripts/`.
