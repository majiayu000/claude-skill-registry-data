---
description: Build an animated SVG diagram (agent graph, build pipeline, RAG flow, etc.) in the Code Origin landing style — purple-on-purple palette, pill messages gliding along edges, paired right-side output panel that reveals progressively, EN+PT dictionary-driven copy. Two patterns are documented — single-scene hub-and-spoke (Hero/Orchestration/AgentDemo) and multi-scene pipeline (RagFlow / "section-4.pdf · 24 pages"). Use when asked to add a new animated section/diagram, replicate the orchestration/agent-demo/RAG style, or refactor an existing diagram into the same primitives.
---

# Animated Diagram

This skill captures the recipes behind every animated diagram in this repo. Two distinct patterns exist:

| Pattern | Examples | Use when |
|---|---|---|
| **A — Single-scene hub-and-spoke** | `Hero.tsx`, `Orchestration.tsx`, `AgentDemo.tsx` | One topology, fixed cast, focal node at centre, ≤8 beats |
| **B — Multi-scene pipeline** | `RagFlow.tsx` (the "chat with PDF" / "section-4.pdf · 24 pages") | Multi-stage flow, cast changes per stage, 5+ scenes, 15+ messages |

If the user asks for "another orchestration-style animation" → Pattern A.
If the user asks for "a RAG flow like the section-4 one", "the chat-with-PDF animation", or "a pipeline animation that shows different stages" → **Pattern B**.

---

## Shared foundation (applies to both patterns)

The two patterns share these rules — non-negotiable for either:

1. **One CSS loop, no JavaScript timing.** All animation is `@keyframes` + `animation: … linear infinite`. No `setInterval`, no React state for animation. JS is only used to mount the SVG and wire dictionary copy.

2. **Every animated element has positive keyframe slot positions** (not negative `animation-delay`). Negative delays cause beats to run *backwards* on first load — the deployer message fires before the planner.

3. **`cqw` (container query width) for destinations.** Wrap the diagram parent in `container-type: inline-size`. Then `1cqw = 1% of stage width`. Positions in `cqw` survive viewport resizes without breaking geometry.

4. **Stage aspect ratio must match SVG viewBox aspect.** Use `aspectRatio: "10/7"` with viewBox `0 0 400 280`. Then `1cqw = 4 viewBox units` uniformly on both axes (so dots placed in SVG coords align perfectly with pills positioned in cqw). Old code used `16/11` — that was off by ~2% and caused subtle misalignment.

5. **Focal node at SVG (200, 140).** HTML pill overlays use `top: 50%; left: 50%` so they start at the stage centre. If the focal node is off-centre, pills start in the wrong place.

6. **`--from-dx / --from-dy / --to-dx / --to-dy` CSS vars per pill** (in cqw %). Set inline:
   ```tsx
   style={{
     ["--from-dx" as never]: src.dx, ["--from-dy" as never]: src.dy,
     ["--to-dx" as never]: dst.dx,   ["--to-dy" as never]: dst.dy,
   } as React.CSSProperties}
   ```
   Keyframes interpolate between them. NEVER hard-code positions in keyframes.

7. **i18n-first.** All copy in `src/app/[lang]/dictionaries/{en,pt}.json`. Component reads `dict.<diagramKey>.*` via `Slice<"diagramKey">`. Never hardcode user-visible strings. Keep agent labels in English (USER, PLANNER, API, REDIS, etc.) — they're glyphs, not prose. Translate message bubbles and output panels only.

8. **`@media (prefers-reduced-motion: reduce)`** — extend the existing rule in `globals.css`, don't add a new one. Animated elements get `animation: none !important; opacity: visible-state-value !important`.

9. **Palette + typography locked to design system.** See "Palette" section at bottom.

---

## Pattern A — Single-scene hub-and-spoke

One topology, fixed cast, N beats × T seconds. Each beat is **(agent, message, optional right-side-effect)**. On the left, one pill glides between two named nodes; on the right, output rows fade in at their beat and persist until loop wrap.

### Layout

```
┌────────────────────────────────────────────────────────────┐
│  ┌──────────────────────┐  ┌──────────────────────────┐    │
│  │  SVG agent graph     │  │  Output canvas:          │    │
│  │  + travelling pills  │  │  reveals progressively   │    │
│  │  + breadcrumb dots   │  │  in lockstep with beats  │    │
│  └──────────────────────┘  └──────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  metrics strip (4 cells)                            │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### Step-by-step

1. **Pick beat count.** 6 beats × 2s = 12s (good for short demos). 8 beats × 2s = 16s (room for plan→build→review→deploy stories). Avoid <1.5s/beat (illegible) or >3s/beat (loses attention).

2. **Author messages with `from` AND `to` fields.** Critical: messages are bidirectional. Old code only had `from` and animated pills always from centre — caused semantics to break for non-hub flows.
   ```json
   { "from": "USER", "to": "AGENT",   "text": "refund didn't process" },
   { "from": "AGENT", "to": "RETRIEVER", "text": "search docs" }
   ```

3. **Build the node map** in the component with `dx/dy` in cqw (from centre):
   ```ts
   const nodes: Record<string, Offset> = {
     USER:      { dx: -35,   dy:    0   },  // SVG (60, 140)
     RETRIEVER: { dx:   0,   dy:  -22.5 },  // SVG (200, 50)
     AGENT:     { dx:   0,   dy:    0   },  // SVG (200, 140) — centre
     "TOOL":    { dx:  35,   dy:    0   },  // SVG (340, 140)
   };
   ```
   Conversion: `dx = (svgX − 200) / 4`, `dy = (svgY − 140) / 4`. Off-by-one in this conversion is the #1 cause of dots/pills not landing on visible nodes.

4. **Generate per-beat keyframes** matching `agBeat1..N` in `globals.css`. Each beat owns a `1/N` slice of the cycle. For 6 beats:
   - Beat 1: 0% → 16.67%
   - Beat 2: 16.67% → 33.33% … etc.

5. **Generate per-(beat × dot-index) breadcrumb keyframes** inline via a `<style>` tag in the component. CSS animations stay perfectly in sync with the pill keyframes (same browser animation clock). **Do NOT use SMIL `<animate>` for the dots** — SMIL drifts against CSS keyframes (this was the cause of "wrong beat's dots showing while a different pill flies"). See `AgentDemo.tsx` → `buildDotKeyframesCSS()` for the reference implementation.

6. **Dot lifecycle (per pill):**
   - `0% → just-before-reveal`: opacity 0 (hidden)
   - `reveal%`: snap to 0.6 (pill passes this point)
   - `arrive%`: hold at 0.6
   - `end%`: fade to 0 (beat boundary)
   - `100%`: hidden, ready to restart
   
   This makes each beat self-contained — no leftover trails into the next beat.

### Reference file

- `src/components/AgentDemo.tsx` — the canonical Pattern A implementation with breadcrumb dots
- CSS in `globals.css`: `.ag-stage`, `.ag-msg`, `.ag-row`, `@keyframes agBeat1..6`

---

## Pattern B — Multi-scene pipeline (RagFlow / "section-4.pdf")

This is what the user means by **"the section-4.pdf · 24 pages animation"**. It's the chat-with-PDF visualisation: user asks "what does section 4 say?", and the right panel builds the answer while the left panel runs through 5 backend pipeline scenes (rate-limit → expand → retrieve → generate → persist).

### Why it's different from Pattern A

| | Pattern A | Pattern B |
|---|---|---|
| Topologies | 1 fixed | N (one per scene) |
| Active cast | Same every beat | Changes per scene |
| Message count | 6–8 | 15–25 |
| Right panel | Reveals tied to beats | Builds a coherent chat UI across all scenes |
| Keyframes by hand? | Yes (≤8 beats × 1 keyframe) | **No.** Generator script required (23 pills × 12 dots = 276 dot keyframes) |
| Scene wrapping | N/A | Yes — `.rag-scene` group crossfades |
| Phase indicator | None | Phase pill cycles (preparing → retrieving → generating → verifying) |

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: title + scene label ("01 · Inbound")  ← cycles 1–5     │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────┐  ┌─────────────────────────────────┐│
│ │  5-scene agent graph    │  │ Chat UI                         ││
│ │  (one <g> per scene,    │  │ - user message bubble           ││
│ │   crossfades)           │  │ - phase pill (cycles)           ││
│ │  + bidirectional pills  │  │ - tool result badge             ││
│ │  + breadcrumb dots      │  │ - streaming answer + cursor     ││
│ │                         │  │ - attribution badges            ││
│ │                         │  │ - claim grounding line          ││
│ │                         │  │ - saliency line                 ││
│ │                         │  │ - action bar (👍 👎 copy …)     ││
│ │                         │  │ - "complete" stamp              ││
│ └─────────────────────────┘  └─────────────────────────────────┘│
├─────────────────────────────────────────────────────────────────┤
│  metrics strip (4 cells)                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Timing model — 32-second master loop

The whole animation is **one 32s loop**. Scene boundaries are fixed % of the loop:

```
Scene 1  Inbound          0%    →  17.2%   (4 pills)
Scene 2  Expand + Embed   17.2% →  34.4%   (4 pills)
Scene 3  Retrieve + Rank  34.4% →  60.2%   (6 pills) ← longest, has rerank step
Scene 4  Generate + Verify 60.2% →  77.4%   (4 pills)
Scene 5  Persist + Audit  77.4% → 100%     (5 pills)
                                  ───────
                                  23 pills total
```

Scenes are **defined by the cumulative pill budget**, not by fixed durations. Allocate more time to scenes that need more pills.

### Pill timing inside a scene

Each scene's pills are evenly spaced within its slot:

```
slotLen = (sceneEnd − sceneStart) / pillsInScene

For pill i in scene s:
  slotStart   = sceneStart + i × slotLen
  flightStart = slotStart + slotLen × 0.12   (pill becomes visible)
  flightEnd   = slotStart + slotLen × 0.78   (pill arrives at destination)
  slotEnd     = slotStart + slotLen          (next pill begins)
```

Pill keyframe (template — actual values generated):
```css
@keyframes ragPillN {
  0%, slotStart%       { opacity: 0; transform: translate(…from…) scale(.85); }
  flightStart%         { opacity: 1; transform: translate(…from…) scale(.95); }
  flightEnd-pad%       { opacity: 1; transform: translate(…to…)   scale(1);  }
  flightEnd+pad%       { opacity: 0; transform: translate(…to…)   scale(.95); }
  slotEnd%, 100%       { opacity: 0; }
}
```

The transform interpolates between `--from-dx/dy` and `--to-dx/dy` (set inline per pill — see Shared rule 6).

### Breadcrumb dots — per-pill, NOT per-scene

Each pill drops `DOTS_PER_EDGE = 12` small circles along its source → destination line. Each dot has its **own keyframe** that:

1. Holds opacity 0 until just before the pill passes its position
2. Snaps to opacity 0.7 at fire time
3. Holds at 0.7 while the pill is still in flight
4. **Fades to 0 by the end of THIS pill's slot** (NOT the end of the parent scene)

Critical: scene 3 has 6 pills. If dots persisted to scene-end, the 6th pill would fly through 5 overlapping trails. The per-pill fade keeps every beat clean.

Dot fire time per index `k ∈ [0, DOTS_PER_EDGE)`:
```
t        = (k + 0.5) / DOTS_PER_EDGE     ← interpolation fraction [0, 1]
fireTime = flightStart + t × (flightEnd − flightStart)
```

Keyframe shape:
```css
@keyframes ragDot_{pillIdx}_{dotIdx} {
  0%, (fireTime − 0.05)%   { opacity: 0; }
  fireTime%, flightEnd%    { opacity: 0.7; }
  slotEnd%, 100%           { opacity: 0; }
}
```

23 pills × 12 dots = **276 keyframes**. **You cannot author these by hand.** Use the generator script (next section).

### The generator script

Located at `/tmp/gen-rag-dots.mjs` (kept in `/tmp/` because it's regenerated on demand, not version-controlled — the resulting CSS is what lives in the repo). To regenerate after changing scene boundaries, pill counts, or `DOTS_PER_EDGE`:

```bash
node /tmp/gen-rag-dots.mjs > /tmp/rag-dots.css

# Then splice the new keyframes into globals.css between the
# selector mappings (around line 1049) and `.rag-row` (~1326):
{
  head -n 1049 src/app/globals.css
  grep "^@keyframes ragDot_" /tmp/rag-dots.css
  tail -n +1326 src/app/globals.css
} > src/app/globals.css.new && mv src/app/globals.css.new src/app/globals.css
```

The selector mappings (`.rag-dot[data-pill="N"][data-dot="K"] { animation: ragDot_N_K 32s linear infinite; }`) are also emitted by the script — replace those too if pill count changes.

A separate companion generator exists for the pill keyframes (`/tmp/gen-rag-keyframes.mjs`). Same idea — regenerate after scene boundary changes.

### Per-scene cast (the `SCENE_COORDS` table)

Each scene defines its own coord map. Reuse the same agent name across scenes if the agent is in both (e.g., `API` appears in all 5 scenes). The `<g className="rag-scene" data-scene={n}>` wrapper handles the cast crossfade — keyframes `ragScene1..5` set group opacity 0/1 within scene bounds.

```ts
const SCENE_COORDS: Record<string, Record<string, { x: number; y: number }>> = {
  inbound: {
    APP:   { x:  70, y: 140 },
    API:   { x: 200, y: 140 },   // focal — always at (200, 140)
    REDIS: { x: 340, y:  70 },
    DB:    { x: 340, y: 210 },
  },
  // ... 4 more scenes
};
```

Rule: **the focal node (API, in this case) stays at (200, 140) across all scenes**. Other participants come and go.

### Chat panel — independent reveals

Unlike Pattern A (where right-side reveals tie to specific beats), Pattern B's chat panel has its **own set of reveal milestones** that fire at specific cycle %:

| Element | Reveals at | Reason |
|---|---|---|
| User message bubble | early scene 1 | The user just sent the query |
| Phase pill ("preparing" → "retrieving" → "generating" → "verifying") | One label per scene, cycles | Mirrors what the backend is doing |
| Tool result badge ("5 chunks found · recall@5 0.92") | End of scene 3 | Retrieval completed |
| Streaming answer + cursor | Scene 4 | LLM is generating |
| Attribution badges ([1] 60% [2] 40%) | Early scene 5 | Persist phase produces these |
| Claim grounding ("3 atomic claims · 100% grounded") | Mid scene 5 | Verification step |
| Saliency line | Late scene 5 | Final audit signal |
| Action bar (👍 👎 copy …) | End of scene 5 | Answer is complete, user can interact |
| "complete" stamp | End of scene 5 | Like the Pattern A deploy stamp |

Each gets its own `data-reveal` attribute and matching `@keyframes ragRow*`. All keyed to the 32s loop.

### Token streaming cursor

The blinking cursor at the end of the streamed answer (`.rag-token-cursor`) has its own short keyframe that pulses opacity 0→1→0 every ~600ms during scene 4 only. Hidden outside scene 4. See `globals.css` for `@keyframes ragTokenCursor`.

### Phase pill — cycling label

A single `<div className="rag-phase-pill">` contains FOUR `<span>` children, each absolutely positioned, each animated to be visible only during its window:

```css
.rag-phase-preparing  { animation: ragPhasePrep 32s linear infinite; }
.rag-phase-retrieving { animation: ragPhaseRetr 32s linear infinite; }
.rag-phase-generating { animation: ragPhaseGen  32s linear infinite; }
.rag-phase-verifying  { animation: ragPhaseVer  32s linear infinite; }
```

Each keyframe shows `opacity: 1` only during its scene's window, otherwise 0. The visible-window mapping:
- preparing → scene 1 + early scene 2
- retrieving → scenes 2 (rest) + 3
- generating → scene 4
- verifying → scene 5

### Scene-label header strip

Mirror of the phase pill but in the card header — shows "● 01 · Inbound" / "● 02 · Expand + Embed" / … rotating once per scene. Uses the same `ragScene1..5` keyframes that drive the SVG `<g>` crossfade — so they're guaranteed in sync.

### Dictionary shape

```json
{
  "ragFlow": {
    "eyebrow": "How a real RAG pipeline runs",
    "title":   { "line1": "Chat with a PDF.", "italic": "Watch the pipeline." },
    "lead":    "Five scenes, real round-trips. …",

    "agents": {
      "app": "APP", "api": "API", "redis": "REDIS", "db": "DB",
      "llm": "LLM", "embedder": "EMBEDDER", "reranker": "RERANKER", "workers": "WORKERS"
    },

    "scenes": [
      {
        "id": "inbound",
        "label": "01 · Inbound",
        "pills": [
          { "from": "APP",   "to": "API",   "text": "POST /messages · section 4?" },
          { "from": "API",   "to": "REDIS", "text": "check rate limit" },
          { "from": "REDIS", "to": "API",   "text": "992 tokens left" },
          { "from": "API",   "to": "DB",    "text": "INSERT user_message" }
        ]
      },
      /* 4 more scenes — see src/app/[lang]/dictionaries/en.json under "ragFlow.scenes" */
    ],

    "chat": {
      "header":    "section-4.pdf · 24 pages",
      "userQuery": "what does section 4 say?",
      "phaseLabels": {
        "preparing":  "preparing",
        "retrieving": "retrieving",
        "generating": "generating",
        "verifying":  "verifying"
      },
      "toolResult":   "5 chunks found · recall@5 0.92",
      "answerLines": [ /* 4 lines of streamed answer */ ],
      "attribution":  { "label": "attribution", "items": [{ "idx": "1", "weight": "60%" }, …] },
      "claims":       "3 atomic claims · 100% grounded",
      "saliency":     "saliency: high · high",
      "actions":      { "thumbsUp": "👍", "thumbsDown": "👎", "copy": "copy", "uncertainty": "uncertainty", "explain": "explain" },
      "stamp":        "complete"
    },

    "metrics": [ /* 4 metric cells */ ]
  }
}
```

The pill `from`/`to` strings MUST match keys in the scene's coord map (case-sensitive). Typos here = pill flies to (200, 140) (the fallback) instead of the named node. Hard to debug visually.

### Step-by-step recipe for a new Pattern B animation

1. **Storyboard the scenes.** Each scene is `(name, participants, message-script)`. Aim for 4-6 scenes. Each scene 4-6 pills.

2. **Allocate cycle %.** Total loop duration in seconds (32s is a good baseline). Each scene gets `% = (its pill count / total pill count)` of the loop. Don't manually pick scene durations — let pill density drive it.

3. **Update the generator script's `SCENE_BOUNDS` and `PILLS_PER_SCENE`** in `/tmp/gen-rag-dots.mjs` (and the matching pill-keyframes generator). Regenerate. Splice into `globals.css`.

4. **Author the dictionary slice** matching the `ragFlow` shape above. Mirror in `pt.json`.

5. **Update `SCENE_COORDS` in the component.** Per-scene coord maps. Focal node at (200, 140) always.

6. **Add scene reveal keyframes** for the right panel (`@keyframes ragRow*`) — one per element that fades in during the loop.

7. **Verify in browser.** Wait a full 32s loop. Check: every pill lands on its named destination; dots fade out before the next pill starts; phase pill matches the current backend stage; chat panel resets cleanly at loop wrap.

### Reference files

- Component: `src/components/RagFlow.tsx`
- CSS: `globals.css` lines ~625–1450 (search for `rag-stage`, `rag-pill`, `rag-dot`, `rag-row`, `rag-phase-pill`, `rag-token-cursor`, `rag-scene-label`, `rag-stamp`, `@keyframes ragScene*`, `@keyframes ragPill*`, `@keyframes ragDot_*`, `@keyframes ragRow*`)
- Dict (canonical): `src/app/[lang]/dictionaries/en.json` → `"ragFlow"` key
- Sequence-diagram source-of-truth: `message-flow.md` at repo root
- Generator scripts: `/tmp/gen-rag-keyframes.mjs` (pills), `/tmp/gen-rag-dots.mjs` (dots)

---

## Palette + typography (Code Origin design system)

Don't deviate without explicit approval:

- Primary purple: `#7C3AED`
- Nubank purple (accent): `#820AD1`
- Background: `#F8F7FF`
- Border: `#E2DFFA`
- Soft purple bg: `#F0EFFE`, `#EDE9FE`
- Text dark: `#0D0B1F`, muted: `#6B6580`
- Mono font (labels, pills, agent names): `var(--font-mono-ibm)` (IBM Plex Mono)
- Display font (titles): `var(--font-chakra)` (Chakra Petch)
- Body: `var(--font-barlow)` (Barlow)
- Gradient combo: `linear-gradient(135deg, #7C3AED, #820AD1)` — for primary CTAs, badges, focal-node strokes, attribution badges
- Edge gradient inside SVG: `#7C3AED → #820AD1 → #7C3AED` with low alpha at the ends

---

## When NOT to use either pattern

- **Static diagrams.** If the diagram doesn't need to animate, just author SVG inline. No keyframe machinery.
- **User-controlled animations** (hover, scroll-driven, click-to-step). The whole point of these patterns is autonomous loops. For interactive demos use React state + Framer Motion or similar.
- **>10 beats in one topology.** Visual rhythm breaks down. Either split into multiple stacked Pattern A scenarios (like `AgentDemo` does), or convert to Pattern B (multi-scene).
- **Real-time / data-bound animations.** These patterns are for marketing demos, not live dashboards.

---

## Templates

- [`templates/component.tsx`](templates/component.tsx) — Pattern A drop-in starter
- [`templates/styles.css`](templates/styles.css) — Pattern A keyframes (6-beat and 8-beat)
- [`templates/dictionary-slice.json`](templates/dictionary-slice.json) — Pattern A i18n shape
- [`templates/multi-scene-pipeline-component-skeleton.tsx`](templates/multi-scene-pipeline-component-skeleton.tsx) — Pattern B starter
- [`templates/multi-scene-pipeline-dictionary-slice.json`](templates/multi-scene-pipeline-dictionary-slice.json) — Pattern B i18n shape
- [`templates/multi-scene-pipeline-keyframe-generator.mjs`](templates/multi-scene-pipeline-keyframe-generator.mjs) — committed copy of the dot-keyframe generator

---

## Working examples in this repo

- [`examples/inventory.md`](examples/inventory.md) — pointers to the live components, with notes on what each one does differently and the bugs they cost to fix.
