---
description: "Deterministic explainer-video agent for the multi-channel content factory. Turns a finished post into a silent 30-45s motion-graphics MP4 — animated text, counting numbers, growing bars — rendered through a headless browser. Text is exact and re-renders are byte-identical. No model or network call at render time. Invoked inline by channel pipelines at the visual step, or standalone. Use for data-dense posts: numbers, mechanisms, formulas, before/after."
trigger: /video-gen-agent
---

# /video-gen-agent

Turns a finished post into a short explainer video. Animated text and charts on the factory's dark palette, silent, sized for a muted autoplay feed.

**Project-side home:** `./agents/video-gen/`
**Renderer:** `./agents/video-gen/renderer/`
**Reference spec:** `./agents/video-gen/specs/example-token-usage-spike.json`

---

## Interface contract

```
[VIDEO BRIEF]
Channel: <linkedin | x | instagram | blog>
Source post: <path to final-post.md>   ← preferred; the agent reads and scenes it
Dimensions: <1080x1350 | 1080x1080 | 1080x1920>   ← omit for 1080x1350
Target length: <seconds>   ← omit for ~35-40s
Handle: <e.g. @teachmebro>
Domain: <e.g. AI ENGINEERING>
Output path: <post-folder>/explainer.mp4   ← omit to write into ./image-gen-output/
Must carry: <any stat or line that has to appear>
```

When `Source post` is absent, the caller must supply the content inline. Never invent
a statistic that is not in the post or the brief.

---

## Step 1 — Read and scene the post

Read the post. Find its **spine**: the one mechanism or claim the whole thing exists to
land. Everything else is setup or payoff.

Then break it into **5-8 scenes**, one beat each. A working shape:

1. **Hook** — the surprising fact, stated flat, no argument yet (`title`)
2. **The gap** — the misconception vs the reality (`stats`)
3. **Mechanism** — why it happens (`bars`)
4. **The worked example** — the post's most concrete number, shown (`bars`)
5. **The general rule** — the formula or principle it implies (`formula`)
6. **The fix** — 2-3 actions (`list`)
7. **Close** — the question or challenge (`title`)

Budget 4.5-7s per scene. Under 4s is unreadable; over 8s stalls.

**Rules for scene text:**
- One idea per scene. If a scene needs two sentences of setup, it is two scenes.
- Cut every word that is not load-bearing. The post can afford prose; a 5s scene cannot.
- Never put a paragraph on screen. Longest `sub` is about 18 words.
- The numbers must be traceable to the post. No rounding that changes the claim.
- No emojis. No company or internal tool names.
- Avoid " — " in on-screen copy; use a full stop or a line break.

---

## Step 2 — Write the spec

Write `spec.json` next to the output (or into the post folder). Follow the format in
`agents/video-gen/AGENT.md` — layouts, fields, and the colour spans are documented there.
Read the reference spec before writing your first one.

Design notes that matter:

- **`bars` carries most arguments.** Pick what bar height *means* and say it in the
  `title` or `punch`. To hold a quantity constant while a total grows, keep `h × slab`
  equal across bars; the slab then stays the same physical height while the bars climb.
- **`stats` values count up.** Use it for a contrast, not a single number.
- **`formula` assembles term by term.** Colour the terms that grow.
- Give the closing scene the post's actual CTA, verbatim where it fits.

---

## Step 3 — Contact sheet FIRST

```bash
node agents/video-gen/renderer/render.mjs <spec.json> /tmp/contact.png --contact
```

About 5 seconds, one settled frame per scene, tiled. **Read the image.** Check:

- Any text clipped, overflowing, or wrapping badly (long titles wrap to a dangling word)
- Bars that are too short to read, or a slab too small to see
- A scene that is visually identical to its neighbour
- Numbers that disagree with the post

Fix the spec and re-run. Iterate here, not on the full render. Use
`--still <seconds>` to inspect one exact moment.

---

## Step 4 — Full render

Only once the contact sheet is clean:

```bash
node agents/video-gen/renderer/render.mjs <spec.json> <post-folder>/explainer.mp4
```

Roughly 1,200 frames for a 40s video. If the render fails, the error is almost always a
missing Chromium — see the setup note in `AGENT.md`.

---

## Step 5 — Surface block

```
[VIDEO GENERATED]
Agent: video-gen (deterministic)
Scenes: <n> · <duration>s · <W>×<H> @ <fps>fps
Spine: <the one thing the video lands, in a sentence>
Spec: <path to spec.json>
MP4: <output path> (<size> MB)
Contact sheet: <path>
Carries: <the stats and lines that appear on screen>
```

---

## Edge cases

- **Post has no numbers.** `bars`, `stats` and `formula` all fall flat. Build it from
  `title` and `list` only, leaning on typography and pacing, and consider a `bg`
  backdrop image per scene to carry the mood the data would have carried.
- **Post is very long.** Do not try to cover it. Pick the spine and cut to it. A video
  that lands one idea beats one that summarises nine.
- **Requested length would need more than 8 scenes.** Push back in the surface block
  and produce the tighter cut.
- **A layout does not exist for the shape you need.** Add one to `scene.html` per the
  instructions in `AGENT.md` rather than forcing the content into a bad fit.
- **`magick` missing** (contact sheet only): fall back to `--still` at a few timestamps.

---

## Shared rules

- Never invent statistics, quotes, or claims not in the source post or brief
- No emojis unless explicitly asked
- No company names or internal tool names unless the brief includes them
- Strip private details
- The spec is committed alongside the MP4 so the video can be re-rendered or corrected
