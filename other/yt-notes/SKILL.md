---
name: yt-notes
description: Structured markdown notes from an information-dense YouTube video
model: claude-haiku-4-5
---
Fetch the transcript for $ARGUMENTS using WebFetch. If no captions available, say so and stop.

Organize as markdown with:
- # Title (video title)
- ## Overview — 2-3 sentences on scope
- ## Sections — break the video into logical topic sections using ## headers (roughly matching how the content itself is structured, not fixed intervals). Under each: key points as bullets, with sub-bullets for supporting detail/examples where the source goes deep.
- ## Key Terms / Definitions — if the video introduces specific terminology or concepts
- ## Timestamps — rough time markers for major section transitions, if inferable from the transcript

Preserve technical detail and specific numbers/claims rather than compressing them — this is for reference, not a summary.