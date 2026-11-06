---
name: vawe-critique
description: "Review and fix a video made from an HTML page. Look at a rendered page film and say what is wrong, as a fresh session that did not write it: the phone, strip and loop views, bin/vawe critique, page-check, the default-reject judge that names shot, frame and fix, the top five, and re-rendering only the affected seconds. Load after any draft render, before any fix."
effort: high
license: Apache-2.0
---

# vawe-critique: how to look

When you talk to the person, use plain words: describe what the viewer sees, not the harness terms (map: harness/lib/plain-words.mjs).
Run this skill inside a vawe checkout: `AGENTS.md`, `taste/` and `bin/vawe` live there. With no checkout, get one: `git clone https://github.com/vawe-hq/vawe.git && cd vawe && npm install && bin/vawe-dev doctor`.

The author never grades its own film. Run this in a session that has not seen the authoring, or
let `bin/vawe critique <page> --fresh` start one (a headless critic with the prompt below; it writes
`out/<film>.critique-<n>.md`). Default verdict is REJECT; the film passes only when you
cannot find a reason to reject it. Grade what is on screen, not what the film meant.

## The views, in this order

```bash
bin/vawe critique films/<name>/page.html [--ref quality/refs/<ref>/source.mp4]
```

It writes the sheet, the strip, the phone view and the loop pair, and runs the page checks. Then
look, and write one line per finding under each view:

1. **Sheet**: every frame. Is the focal point obvious in under a second? Is anything cramped,
   overlapping or unreadable? Producing a sheet is not looking at one: one line per frame.
2. **Strip**: both sides of every cut. Does the cut land on its beat? Does the eye know where to go
   after it? Does any exit run slower than its entrance?
3. **Phone**: the 9:16 render, or 16:9 at one third size. Can you read every string? Is the accent
   still one colour?
4. **Loop or end**: t=0 beside t=duration. A loop is pixel-identical; an end holds long enough to
   read.
5. **Checks**: `quality/gates/page-check.mjs` findings (readable hold, hook length, em dash, message
   and spectacle meta, aspect layout) and `bin/vawe check anim-traps <page>`.

With a reference: frame-locked. Pull the same five timestamps from both. For each pair write light,
type scale, and the curve of the one thing that moves: same or not. Anything the draft added without
a KEEP/CHANGE line is a rejection (`vawe-reference`).

## The look verbs

`vawe see <mp4 | page | ref-id> [--vs <ref>]` reads a film completely: shots, motion, light, type, sound, every image
with its numbers; `--vs` adds deltas and advice that names the page literal. Its parts: `vawe refs frames` (reference
stills), `vawe frame --world all` (your page), `vawe frame --cuts` and `--moment s` (motion through every cut or one
moment, a reference or your draft; `--onion` and `--velocity` for one move), `vawe see <ref.mp4> --spec` (a reference
measured into SPEC.md), `vawe frame --at s,s,s` (a labelled sheet of seconds; `--vs <mp4>` puts the reference beside
your frames), `vawe frame --board` (one HTML board: frame cards, moves, eases, handoffs, sound, rhythm), `vawe frame
--at s` (one full-size PNG of a page or mp4 at a second). A site route, url or static html page: `vawe new --from-url <route> --w 1440,390 [--full]`, never a puppeteer script;
the site's links: `vawe-dev check links`. A field of many small moving parts (rain, dust, sparks): `vawe see` prints one
"Particle field" line with count, direction and speed.

## The judge

Score the film axes of `guides/judge.md` (hook, motion, scenes, type, colour, sound, pace,
expensive), 1 to 10. A score under 8 needs a fix. Two
runs, A and B, before a beat closes; one judge is an opinion: `bin/vawe-dev judge <page> --struct --runs A,B`. A
PASS is never self-recorded.

Name the idea in each beat and each cut: read the brief's `## Ideas` table (`guides/IDEATE.md`) and look at the frames. Does the frame show the chosen idea (the shared element, the object), or only the plan text? An idea planned in the ledger and absent in the frames is a finding, with the second and the fix. Also name an Ideas row whose four ideas are one idea reworded.

Name every default you recognise; each is a rejection: a particle burst, a bouncy spring, a glow, a
logo slam, a gradient on chrome, a centred title on a gradient, everything fading in, corner labels,
a crossfade where a cut belongs, fake UI, dead time that no `authoring` waiver declares.
Name the rule id of each (`no-tells`, `overshoot`, `entrance-origin`, `crossfade-limit`, `show-real-thing`,
`live-hold`); every id is in `taste/README.md`.

## The report shape

Every finding is shot + frame + fix:

```
REJECT: 7 findings, top five first.
1. [3.2s, frame 96] the stat lands on the same frame as the label; stagger the label 60 ms later.
   fix: films/x/page.html:88, delay 3200 -> 3260
2. [8.0s] exit of the card (420 ms) is slower than its entrance (300 ms). fix: line 131, 420 -> 220
...
```

End with exactly one of:

- `REJECT: <n> findings, the top five first.`
- `PASS: I looked for a reason to reject it and found none. <one sentence on what is best>`

A finding with no file and line is a complaint, not a critique. The critic proposes; the author
decides.

## After the critique (the author)

- Fix the top five (the top three for a short film). Re-render only the seconds they name:
  `bin/vawe dev films/<name>/page.html --from <s> --to <s>`.
- Then a fresh critique again. Stop when it passes, or when two rounds in a row fix nothing the
  critic scores higher. Hand back with the last critique attached.
- Findings are fixed, not moved: the next critic gets the previous report and checks.

## The critic prompt, and the panel

Hand a fresh agent this and nothing else about the authoring: "You are the critic. You have not seen how this film was made. Film: <page>, rendered at <mp4>. Reference: <ref or none>. Brief: <brief.md>. Default verdict is REJECT; do not fill in what the film meant. Look at the four views in order, one line per finding; frame-locked against the reference at five shared timestamps if there is one; score the film axes of guides/judge.md; name every default you recognise; end with the REJECT or PASS line." Ask the author five things first, each with a default: the mp4 (the last draft), the brief (`brief.md`), the reference (none), the previous critique (none; the critic checks findings were fixed, not moved), the judges (two, A and B).

A fresh critic matters because the thread that wrote the page has anchored on its own easing, crop and headline. Its value is independent evidence: judge by what artifact it sees that the author did not (a render, a strip, a reference), not by a fresh pair of eyes. For a panel, hand each critic one artifact and demand a fixed verdict shape:

| critic | input | verdict per item |
|---|---|---|
| beat | the phone sheet and strip of `bin/vawe critique` | `{beat, reads, flaw, fix}` |
| bg-motion | a strip of 4 or more frames, reference and render at matched times (a still says nothing about speed) | `{axis, ours, reference, delta, fix}` |
| reveal | a dense strip of the entrance and exit windows | `{beat, enter, exit, paired, flaw, fix}` |
| fidelity (recreations) | `bin/vawe frame --vs` frames | `{beat, score 0-10, gaps}` (gaps, not agreement) |
| seam | the seam frames and the loop seam | `{seam, flash, evidence, fix}` |

Launch the panel in one message so the critics run at once. Critics report, the main thread fixes. A critic is evidence, not a ruling: if you look and the flaw is not there, it is wrong. A panel suits a full authoring pass, a recreation and any render you ship; a colour swap is not worth it. The fan-out cost and the brief lines for any subagent: `guides/SUBAGENTS.md`. Judge dimensions: `guides/judge.md`.

<!-- doc-refs-allow: films/x/page.html · an example path in a sample judge line -->
