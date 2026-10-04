---
name: scbe-webtoon-book-conversion
description: Convert The Six Tongues Protocol and related manuscript sections into webtoon/manhwa storyboard packets, episode roadmaps, panel expansion plans, and image-generation-ready prompt lanes. Use when extending the series storyboard, adapting book chapters into vertical scroll episodes, or keeping art generation tied to canon instead of drifting into generic fantasy panels.
---

# SCBE Webtoon Book Conversion

Use this skill when the task is to adapt the book into a webtoon/manhwa production lane.

This skill owns:
- episode ordering for the full series
- chapter-to-webtoon panel expansion
- section-by-section storyboard packets
- visual canon preservation for Marcus, Polly, the Six Tongues, and Aethermoor spaces
- prompt-lane preparation for image generation, strip assembly, recap video, and voice sync

## Core Rule

Do not invent a new structure if the repo already has one.

The canonical adaptation stack is:
1. `artifacts/webtoon/production_bible.md`
2. `artifacts/webtoon/SERIES_STORYBOARD_ROADMAP.md`
3. `artifacts/webtoon/series_storyboard_manifest.json`
4. the relevant act key-beat script
5. the actual manuscript chapter/interlude source

## Read Order

When this skill triggers:

1. Read `references/source-map.md`.
2. Read `references/episode-pacing.md`.
3. Read `references/output-schema.md`.
4. Read only the manuscript section and act script you need for the current episode.

Do not bulk-load the entire novel unless the task is a full-series audit.

## Workflow

1. Lock the episode.
- Identify the exact chapter, interlude, or epilogue section.
- Resolve its `episode_id` from `artifacts/webtoon/series_storyboard_manifest.json`.

2. Pull the actual source.
- Prefer `content/book/reader-edition/` for episode adaptation.
- Use `content/book/source/` when you need chapter-title alignment or drafting context.

3. Pull the existing visual skeleton.
- Use the appropriate act script in `artifacts/webtoon/act*_panel_scripts.md`.
- Treat those as key beats, not final full episode density.

4. Expand to a webtoon episode.
- Add breathing panels, domestic beats, object close-ups, transitions, and exterior shots.
- Preserve the chapter's emotional order.
- Keep lore attached to visible action.

5. Emit a production-ready packet.
- human-readable storyboard packet
- panel list with beat purpose
- prompt-ready visual notes
- text overlay notes if requested

6. Keep canon stable.
- Marcus is grounded before spectacle.
- Polly's form and timing must match chapter canon.
- Sacred Tongue colors never drift.
- Earth scenes stay materially human before Aethermoor takes over.

## Project-Specific Rules

For `The Six Tongues Protocol`:
- Chapter 1 starts with a cover splash, then blackout, then Marcus asleep, then wake/routine, then desk, then rupture.
- Every episode should usually land in the `10+` panel zone even if the key-beat script is shorter.
- The existing `159` key beats are a skeleton; the adaptation lane expands them into full webtoon rhythm.

## Output Standard

A good output from this skill should leave behind:
- a stable episode ID
- the source manuscript path
- the act script path
- target panel range
- a list of actual panel beats in reading order
- short, usable visual directions instead of vague hype

## References

- `references/source-map.md`
- `references/episode-pacing.md`
- `references/output-schema.md`
