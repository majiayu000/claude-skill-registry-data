---
name: new-video
description: Take a video idea from backlog to a shoot-ready script, covering the concept doc, title, hook plan and full script. Use when the user wants to plan, develop or script a new video.
---

# Idea to shoot-ready script

## Steps
1. **Concept doc:** create `video-ideation/ideation_<short_name>.md` following the Doc pattern in `video-ideation/claude.md`.
   - Pull model videos from `outlier-tracking/*/data.json`. Don't re-scan YouTube.
   - Gate: `ideation-doc-sections`.
2. **Titles and hook:** delegate to the `hook-researcher` subagent (mode 2: apply the patterns to this video). Reuse the existing `hook_patterns.md`, and only refresh research if the data is stale.
3. **Script:** delegate to the `script-writer` subagent.
   - Gate: `script-structure` (research citation, hook by 0:10, at most 3.5 words/sec, no woman's dialogue).
4. **Critic:** run `critic` once on the final title + hook + script, apply the MUST FIX items, and allow one more round at most.
5. **Update `video-ideation/video_ideas.md`:** move the idea to Promoted.
6. **Report:** the title, the hook and the script path, plus anything that needs the user (e.g. which footage to use).

## Batch mode
When the user wants several videos planned, run steps 1-3 for all of them, then run the critic once per final script.

## Gotchas (keep this list updated)
- **No dance-request angle** in titles or thumbnails, and no faceless or voiceover-only formats (user feedback).
- **Model videos:** in-person concepts should use `format == "In-Person"` rows only.
