---
name: sk-brief
description: Starts a new short by stating the idea in one sentence, picking the storytelling flow and the visual types, checking image licences before any script exists, scaffolding the video folder, and writing briefs/<id>.md. Use when the user says "new video about X", "write a brief", "which flow fits this topic", "how should this look on screen", "scaffold a video", or "can I use this image". Steps 1, 3 and 4 of sk-pipeline.
---

# sk-brief: idea, flow, visuals, brief

**Announce:** "Using sk-brief for <id>."

Rules: `SOUL.md` three first rules, §1, §2 (`docs/soul/01-voice-and-structure.md`),
§5 (`docs/soul/03-visuals.md`), §13 (`docs/soul/10-files.md`). The § wins over
this file.

## Order (do not swap)

1. **One sentence: what can the viewer repeat after watching?** If you cannot
   write it, the topic is not ready. This sentence is the brief's first line.
2. **Facts first.** Every claim you plan to use needs a `verified` record in
   `docs/facts/facts.json`. Missing ones: run `sk-facts` now, before writing.
3. **Pick the flow.** Read `docs/flows/README.md`, then the candidate flow files,
   especially "When to use" and "Traps". Do not default to the first flow out of
   habit: ask what shape the fact has (a list of reasons, a trace back to a cause,
   a single person, a comparison). Sketch at least two shapes, pick one, and note
   in the brief why the other lost.
4. **Pick the visual types** from `docs/visuals/README.md` (e.g. `text-as-image`,
   `timeline`, `archive-plate`, `news-photo`, `gif`, `b-roll`) and read each
   chosen type's file. Flow is how the story is told; visual is how it gets on
   screen. They are independent axes.
5. **Check the licence of every image and clip now.** Record each in
   `docs/facts/sources.json` with its `licence`. An image you cannot license is a
   claim you cannot show; find another visual or cut the claim before scripting.
6. **Scaffold:**
   ```bash
   bun run new <id> --flow <A..N>
   ```
   Then set `visual` in `src/videos/<id>/narration.json` to the chosen ids.
   `id` follows §13 (lowercase, hyphenated, never reused for a different video).
7. **Write `briefs/<id>.md`** from `briefs/_template.md`.

## What the brief holds

- The one-sentence idea and the angle (what the viewer believes now, and the
  turn that negates it).
- Flow chosen, why, and the shape that was rejected.
- Visual types and, per scene, what is on screen.
- A fact table that points at **ids** (`f-0001`), not copied numbers or URLs. A
  copied number goes stale silently when the ledger is corrected.
- Image list with source ids and licences.
- An empty "Posted" section, filled in after upload (`sk-improve`).

## Verify

- [ ] `flow` in `narration.json` matches the flow named in the brief
- [ ] `visual` is set and every id exists in `docs/visuals/`
- [ ] every fact id in the brief exists in `docs/facts/facts.json`
- [ ] every image has a source record with a licence
- [ ] `bun run facts` exits clean

Next: `sk-narration`.
