---
name: quick-lookup-ux
description: Use when changing what kasane tells a user about where they are in a series — Quick lookup, the episode/chapter rail, arc detail, "arcs behind", auto-estimated mappings, progress marks, or any empty, partial, or "no answer" state on a series page.
---

# Quick Lookup UX

Two of the README's three journeys end at one answer: _I finished X, where do I go next?_ Quick Lookup is where that answer is delivered, and it currently renders `—` for every case where the app does not know. Those cases are not all the same, and a dash tells the user nothing about which one they hit.

This skill owns the **behaviour contract**. The component itself is governed by `universal-component`; it exists once, in `src/components/QuickLookup.tsx`, and `MappingSection` renders it on the series screen. Extend that copy — never fork a second one.

## The answer states

`episodeToChapters` and `chapterToEpisodes` both return `[number, number] | null`, and `null` collapses five distinct situations. Distinguish them:

| Situation                           | How to detect                                                    | What to say                                                                                              |
| ----------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Answered**                        | tuple returned                                                   | `chapters 41-80`. Include the season when known, as the manga copy already does.                         |
| **Input beyond the mapped range**   | value exceeds the last arc's end                                 | "The catalog maps through episode N." Not a dash.                                                        |
| **Input inside a gap between arcs** | value falls between two arcs                                     | "Not covered by a mapped arc" — this is filler or a skipped stretch, and saying so is the useful answer. |
| **Chapter is in an unadapted arc**  | arc matched, `episodes` is `undefined`                           | "Not animated yet." This is a _good_ answer for a manga reader and must not look like a failure.         |
| **No mapping exists at all**        | `findMapping` missed and `buildSyntheticMapping` returned `null` | Explain that the series is unmapped, and link to contributing a mapping.                                 |

## Auto-estimated mappings

When `findMapping` misses, `buildSyntheticMapping` distributes episodes evenly across chapters and sets `sourceNotes` to a warning that real arc pacing is rarely uniform. That warning must be **visible wherever the estimate is used**, not only on the series header. An estimated Quick Lookup answer is a guess and has to read like one:

```
≈ chapters 41-80  (estimated — this series has no curated arc mapping)
```

Use `COLOR.notice` for estimated answers, never `COLOR.textPrimary`. A confident-looking wrong answer is worse than no answer, because the user buys the wrong volume.

## Ongoing series

For a manga still publishing, the last arc ends at the last published chapter, not at the end of the story. When a lookup lands in the final arc, say so: "you are current through chapter N". Do not imply the series ends there.

## Consistency rules

- **One vocabulary.** Episodes are cumulative across seasons everywhere in the UI, matching the catalog. Never show a per-season episode number in one place and a cumulative one in another.
- **Ranges render identically** in Quick Lookup, the rail, arc detail, and the progress banner. Route them through one formatter in `src/data/format.ts`.
- **Volume, not just chapter.** An anime viewer's real question is which book to buy. Where MangaDex volume data is loaded, pair the chapter answer with its volume.

## Common mistakes

| Mistake                                        | Consequence                                             |
| ---------------------------------------------- | ------------------------------------------------------- |
| Rendering `—` for every `null`                 | Five different situations look like one failure.        |
| Styling an estimated answer like a curated one | The user buys the wrong volume and trusts the app less. |
| Adding a state to one copy of `QuickLookup`    | The anime and manga copies drift further. Unify first.  |
| Treating "not animated yet" as an error        | For a manga reader that is the answer they wanted.      |
| Formatting a range inline                      | Four call sites drift. Use `src/data/format.ts`.        |
