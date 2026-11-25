---
name: sk-promo
description: Makes an ad, TVC, product launch film or feature teaser as a promo, either vertical 9:16 or landscape 16:9, using video.json format and mode. Use when the user says "make an ad", "TVC", "commercial", "product video", "launch film", "promo", "teaser", "quảng cáo", "làm video giới thiệu sản phẩm", "video ngang", "16:9", "landscape", or asks for a video that sells or announces something rather than explains a fact. Not for narrated knowledge shorts (use sk-pipeline).
---

# sk-promo: an ad or TVC, vertical or landscape

**Announce:** "Using sk-promo for <id>."

A promo sells or announces; a short explains a fact. A promo **starts from the pain of the people who use the product** and reveals the product as the answer; a feature tour is not a promo. They share the engine and
differ in rules. Rules: `docs/promo/README.md` (read it first). SOUL's story rules
do not apply; its hard rules do (licences, encode spec, never auto-publish).

## Voice or no voice

- **No voice** (music and sfx, like a TVC): `bun run new <id> --voice none`. The clock
  is `promo.json` (seconds or beats). No narration, TTS, facts file or flow. See
  "A promo with no voice" in `docs/promo/README.md`.
- **Voice-over**: `bun run new <id> --flow <X> --mode promo`, then the normal
  narration path (`sk-narration`).

Read "What is not built yet" in `docs/promo/README.md` and tell the user which of
those their film needs **before** starting (no beat measurement, no strip review,
no page capture yet).

## Steps

| # | Step | How | Evidence |
|---|---|---|---|
| 0 | **Objective and placement.** Copy `briefs/_template-promo.md` to `briefs/<id>.md`. Fill objective, the one measure, CTA (exact words), mandatories, placement (feed ad or launch film) and the deliverables matrix (master, cutdowns, formats, captions) | `docs/promo/README.md` rules 11, 12, 15 | those sections filled and confirmed by the owner |
| 1 | **Pain point first.** Write, in the target user's own words: who they are, the moment they feel the pain, what it costs them. The owner confirms it before anything else is designed. Then the format (portrait or landscape) from where it is watched | `docs/promo/README.md` rules 0 and 1 | pain point written in the brief and confirmed |
| 1a | **Concept routes:** 2-3 routes, each one sentence + key frame + how it shows the pain. The owner picks one; rejected routes and why stay in the brief | `docs/promo/README.md` rule 13 | the chosen route and the rejected ones written |
| 1b | **Treatment, confirmed before any build:** scene by scene in plain words, what the viewer should understand at the end of each (`docs/promo/aesthetics.md` C1-C8): one idea per scene, plain words before product words, a before and after, labels on every number | `docs/promo/aesthetics.md` Clarity | the owner confirmed the treatment |
| 2 | Brief: one sentence, shot list, every asset and its licence. A licence that is not checked makes the film internal-only, and the brief says so at the top | `sk-brief` (skip the flow's "turn" rule) | `briefs/<id>.md` |
| 3 | Scaffold | no voice: `bun run new <id> --voice none --format <portrait\|landscape>`; voice-over: `bun run new <id> --flow <X> --format <..> --mode promo` | `src/videos/<id>/video.json` (+ `promo.json`) |
| 4 | No voice: write `promo.json` (scenes in seconds or beats, music, `bpm` measured, not guessed). Voice-over: write the words | no voice: `docs/promo/README.md`; voice-over: `sk-narration`, and `sk-facts` only for checkable claims (prices, numbers, "first", "only") | `bun run lint <id>` 0 errors |
| 5 | Shot list approved before scene code; every shot has a `size`, and a `card` from `docs/shots/` where one fits | `bun run storyboard <id> --init` (no voice: one shot per promo.json scene, split by `beat`; voice-over: one per line), `docs/storyboard.md`, review in `bun run preview` (Storyboard and Timeline tabs) | every shot `approved` |
| 5a | **Animatic gate:** full-length timed rough cut (one plain card per scene: its big type and a box or still), real music on the grid, scratch voice if voiced. Render it, the owner watches at full speed, and someone new takes the "before" comprehension test (C8). No scene code until it passes | `docs/promo/README.md` rule 14 | animatic rendered; the owner's OK and the stranger's answer written in the brief |
| 6 | Scenes | `sk-scene`; real product components: `docs/promo/real-ui.md`; size and safe area from `useFormat()` / `safeFor()` in `src/shared/format.ts`, never the `W` and `H` in `theme.ts` | `bun run check` clean |
| 7 | Stills with the safe overlay | `bun run still <id> --frame=<n> --safe` | stills opened and looked at |
| 8 | Render, normalize, encode | `sk-render` (size is checked against the video's own format) | ffprobe passes |
| 8a | **Comprehension test:** show the cut to someone who has not seen it; ask what it is for and what changes if you use it; write their answer in the brief (C8) | `docs/promo/aesthetics.md` | their answer names the pain, the product and the benefit |
| 8b | **Review pass:** every rule in `docs/promo/aesthetics.md` answered `✓` or `✗ (shot/frame)`, from a contact strip, ideally by a reviewer who did not make the film; each deliberate break written in the brief | `docs/promo/aesthetics.md` | the pass is written down |
| 8c | **Cutdowns and formats** from the deliverables matrix: each re-edited (pain, product, CTA in its own length), its own composition, checked like the master | `docs/promo/README.md` rule 15 | every row of the matrix has a file that passes ffprobe |
| 9 | Hand-off | `sk-handoff` (a 16:9 cover is not cropped; the 1:1.29 grid crop is for portrait) | every file in the deliverables matrix is in `out/<id>/` |

## Traps

- Components that still import `W`/`H` from `theme.ts` (map, nature, marks, figures,
  chart, FootageStage, PipShot) are portrait only. In a landscape video, check each
  on a still, or make it format-aware with `useFormat()` first.
- The template's `scenes.tsx` uses portrait safe-zone constants. For landscape use
  `safeFor("landscape")`.
- Voiced promo: `bun run lint` still applies the short rules to narration; read its
  warnings as advice, not gates. Voiceless promo: lint checks only the clock and files.
- `bun run render` renders only the `Video` composition; render a cutdown with `bunx remotion
  render` (see "What is not built yet").
- A feed ad that opens on the pain still needs the product name or mark visible by 5 s (rule 12).
- `ingest`/`cut` normalise footage to 1080×1920; landscape footage is not
  supported yet.
- Never auto-publish.
