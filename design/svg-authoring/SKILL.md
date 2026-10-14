---
model_tier: inherit
name: svg-authoring
description: "Hand-author or edit an SVG — icon, mark, illustration, diagram, animation, raster-to-vector — checked and rendered."
domain: product
personas:
  - design-director
workspaces:
  - engineering
packs:
  - frontend-design
  - ai-image
  - ai-video
  - engineering-base
trust:
  level: professional
install:
  removable: true
scope:
  write: []
  verification_reason: "execution declares no handler, so this skill runs nothing of its own — every write is the calling agent's, under the rules that govern it. No command can prove a scope the skill never executes."
execution:
  type: manual
---

# svg-authoring

> The one owner for SVG an agent writes by hand. Six lanes produce one — a
> missing icon glyph, a geometric mark, an illustration, a diagram, an animated
> asset, a wireframe canvas — and until this skill existed none of them had a
> procedure or a check beyond the agent's own belief that the file looked right.

## When to use

- A glyph the incumbent icon set does not have (`iconography` first — the set wins).
- A simple geometric mark, when `logo-generation` takes the true-vector path.
- An illustration or a diagram authored as SVG rather than generated.
- An animated asset: SMIL, CSS or WAAPI inside an `.svg` or an inline graphic.
- A **surgical edit** to an existing SVG — "change only the hat", "remove the face".
- A **raster converted to a vector** — "turn the logo in this PNG into a real vector".

## When NOT to use

- The icon exists in the set → `iconography`, and stop there.
- A photoreal or illustrative raster → `image-generation`.
- A full brand pipeline → `logo-generation` (which routes back here for the mark).
- Motion design for video → `motion-choreographer`.

## Procedure

1. **Read the delivery mode first — it decides everything after it.** `inline`
   in a host page, a standalone `document` opened directly, `img`, a CSS
   background, or a deck. It decides what can animate, what can execute, and how
   the graphic gets its accessible name. An **undeclared** mode is treated as
   `inline`, the strictest.
2. **Classify the asset** — `icon`, `mark`, `illustration`, `diagram`,
   `animated`. The class picks the fill-ratio threshold and the geometry
   tolerance; there is no global threshold, because a 24-grid icon's designed
   padding reads as an under-filled viewBox against one.
3. **Plan before attributes** — concept, then layout, then attributes.
   Primitives before detail: a mark built from `rect`/`circle`/`polygon` is a
   true vector and is often the right answer, not a lesser one.
4. **Write with the invariants.**
   - ids namespaced to the graphic — a bare `id="title"` names the second
     inline graphic on the page after the first.
   - the accessible name comes from the ARIA corpus, not from here: ground
     `meaningful standalone svg chart graphic accessible name` against
     `accessibility-auditor`'s `aria-patterns.csv` and follow the
     **Meaningful standalone graphic** or **Decorative graphic** row.
   - colour from the project's tokens or `currentColor`, never a loose hex.
   - an explicit `font-family` with a fallback the target actually ships; a
     `<text>` with none resolves to the platform serif.
   - no `<script>`, no `on*`, no `javascript:`, no `foreignObject`, no external
     `href` or `url()`, no internal DTD subset or `<!ENTITY` (a bare public
     DOCTYPE is fine).
5. **Run the static check** — `lint_svg_asset`, with the delivery mode declared:
   ```bash
   npx tsx node_modules/@event4u/agent-config/src/scripts/lint_svg_asset.ts \
     --file path/to/asset.svg --delivery inline
   ```
6. **Run the witness** — the asset profile, which opens the file in a real engine:
   ```bash
   agent-config ui:render path/to/asset.svg --profile asset --class icon
   ```
7. **Look at the render.** Looking stays mandatory for *meaning*; it is never the
   pass for *geometry*. Fix what both the checks and the look found.
8. **Stop** at a clean witness or after three render passes, whichever comes
   first. A stop **at the cap with error findings still open** reports
   `unverified` with the reason `pass-cap-reached` and lists what is open —
   never `verified`, and never done. That reason is yours to report: the render
   manifest never carries it, because one invocation of `ui:render` cannot see
   how many passes you have made.
9. **Report** the renderer and the checks that actually ran — `verified`,
   `static-only` or `unverified` — plus `goal: unassessed`, and name only
   output files read back from disk. Where the renderer is **absent**, run the
   static witness, report `static-only`, and name the missing capability in one
   line; opening the file in a browser is never a step of this procedure or of
   the user's.

## Status — what each word is allowed to mean

| Status | Allowed only when |
|---|---|
| `verified` | a render manifest from the asset profile exists **whose recorded file digest equals the delivered file's digest on disk**. A manifest from an earlier pass does not count. |
| `static-only` | the static check ran and no render did. A parser pass (`xmllint --noout`) is this, never `verified` — a file can parse and still be the wrong picture. |
| `unverified` | no browser resolved, or the pass cap was reached with error findings open (`pass-cap-reached`). Never a pass; never silently upgraded. |

**A second axis, and it is not this table's.** Every status above is about
whether a CHECK ran and what it found. Whether the graphic is *right* is a
different question, and `verified` was being read as an answer to it. So every
report carries `goal:` beside the status, and this skill writes exactly one
value into it:

| Goal | Written by |
|---|---|
| `unassessed` | **always, by this skill and by the renderer.** The default, and the only value either may write. |
| `accepted` / `rejected` | an owner statement, or a pre-registered scenario witness. Never derived from a digest match, a clean witness, or a score. |

## Editing an existing SVG — the baseline replaces the look

Declare the ids the edit is allowed to touch, then let the readout decide:

```bash
npx tsx node_modules/@event4u/agent-config/src/scripts/lint_svg_asset.ts \
  --file after.svg --baseline before.svg --allow hat,hat-band
```

Every element outside the allowed set that changed is reported with the attribute
that changed, after number and whitespace canonicalisation. **No pixel diff
decides this** — anti-aliasing and font metrics would make it a per-machine
verdict.

This applies **between the owner's own passes** too. A part the user already
accepted joins the baseline and may not move by hand. A conversion pass that
re-derives that part from the source instead **re-measures** it and re-checks
the accepted property — a hole that was accepted as a hole stays a hole through
a full re-trace.

## Converting a raster to a vector — its own branch

Drawing it from a look fails, and it fails the same way every time: the outlines
"coincide within a few pixels" by eye and read 0.883 silhouette IoU when
measured. The procedure below reached 0.984 with the same tools.

### Trace to measure, construct to deliver

**The trace is the underlay by default, not the deliverable.** Trace the source
to measure and to align; then construct the deliverable over that underlay from
few points, palette colours and named shapes. Keep a trace AS the deliverable
only when the owner asks for maximum fidelity over editability, and say that is
what they are getting.

The reason is measured, not stylistic. In one session the traced mark scored
0.989 region IoU against the constructed one's 0.935 — and the trace was sent
back fifteen minutes after it was accepted, on criteria no score sees: a crown
cut at the crop edge, hairlines between segments, an off-palette spot, jagged
edges, 49 KB of edit-hostile points, and a face unreadable at 32 px. The
rebuild was 4.5 KB with 14 shapes and about 180 points. **The score is the
alignment check. It is never the acceptance.**

**When the score stops applying.** Once the owner's goal becomes a redesign
rather than a reproduction — different fingers, depth taken from a style
reference — the source-fidelity number measures agreement with something
nobody is still trying to match. Stop reporting it as progress and say why.

1. **Crop the source region with a margin, and make that crop the coordinate
   system.** Write every vector coordinate in the crop's pixel units; fit the
   viewBox to the content at the end, not at the start. **Widen the crop
   whenever source content touches its edge** — a trace takes the crop border
   for a contour, and a comparison against that same crop cannot see the cut.
   One session lost a crown that way: the crop started five pixels below it.
   The engine's `geometry/source-cut-by-frame` reading is the check.
2. **Derive geometry from the pixels, never by eye — then build over it.** One
   traced silhouette that clips everything, then named regions split along an
   edge map; smooth, resample and simplify each contour. The outer edge comes
   from one contour and the holes come from the source. That trace is the
   underlay; the shapes you ship are constructed on top of it.
3. **Fit colour, do not pick it.** Least-squares per region against that region's
   own pixels; swap a linear gradient for a radial one only when the residual
   actually drops.
4. **Classify near-white inside the mark as hole or paint from the source**, and
   check it on a dark background **before** the first report. Near-white paint
   where the source shows a hole is invisible on white and obvious on black.
5. **Keep text, wordmark and slogan out** unless they were asked for.
6. **Score every pass and every candidate change**, and keep a change only when
   the score improves — a tried-and-worse idea is dropped by the number, not by
   taste. Use the two readings the geometry comparison produces: silhouette IoU
   over saturated regions, and mean colour error plus the share of pixels off by
   more than 40/255 — broken down per region, so the worst region is named. The
   score ranks passes against the source; it does not decide acceptance, and it
   stops meaning anything once the goal becomes a redesign.
7. **Stop** at the declared tolerance, at the user's pass budget, or **on a
   plateau** — whichever comes first. A plateau is two consecutive passes each
   improving the score by less than 5 % relative: stop, report the residual's
   cause, and offer the construct-or-redesign option instead of starting
   another pass. An explicit pass budget from the user still wins when it is
   smaller. Measured: twelve further scored passes took mean error 16.78 to
   6.12 and the share off by 40 from 9.1 % to 1.5 %, and the owner said "still
   unclean" twice; the plateau was named only after they brought a reference.
8. **Snapshot every delivered pass** as `<name>.pass-<n>.svg`, and diff the next
   pass against the last accepted snapshot with `lint_svg_asset --baseline`.
   Report which accepted properties carried forward. Restoring "version 4" is
   then a copy, not a reconstruction — one session lost the same accepted
   detail twice between hand edits, and the owner had to supply the file back
   from their own downloads.
9. **Report the per-pass numbers, the cause of the remaining residual, and the
   file size.** Fidelity costs bytes — one accepted conversion went 5.3 KB →
   49.5 KB and nothing measured it. Each number carries the **registration**
   it was taken against as `x,y,w,h` in the source's pixel frame, the
   **scorer** that produced it (`ui:render`, or a named script) and the sample
   resolution. Two scorers disagreed on one file by a factor of four and
   neither number could be told from the other afterwards; a wordmark's frame
   could not be recovered at all, and three plausible ones moved its IoU from
   0.56 to 0.81.

Any tracing tool the host has may do the deriving, and a host with none can
write one. **The measurement is the procedure, not the tool.**

## Deliver, re-open, re-render

The last step reads every delivered file back **from its final path** in a fresh
browser context (`file://`, every other request aborted) and re-renders it from
there — not from the source text the agent wrote. Report path, byte size and
digest. An `img` delivery is additionally loaded through a host `<img>` and must
report a non-zero natural width.

**A file that does not re-open is not delivered.**

## Output format

1. **Delivery mode and asset class** — declared, not assumed.
2. **The file** — path, byte size, digest.
3. **Checks that ran** — the static check's finding count, the witness's
   readings, and the status word from the table above.
4. **For a conversion** — the per-pass score table and the residual's cause,
   each number carrying its **registration** (`x,y,w,h` in the source's pixel
   frame), the scorer that produced it and the sample resolution, so a later
   run can repeat the reading and no second scorer's number is quoted as the
   first's.
5. **Variants** — for a `mark`, the small-size variant when the 16 and 32 px
   captures lose the detail, and a light-on-dark variant when the contrast
   reading is low on a capture's ground. Built, or named as missing. Never
   silent: one wordmark shipped in a dark violet that is unreadable on a dark
   ground, and the dark variant was simply not mentioned.
6. **Outlined lettering** — a word set from an installed font and converted to
   outlines is reported with the font's name and whether its license allows
   outlining into a distributed asset. An unknown license is reported as
   unknown, never as permitted.
7. **Cost** — the reading the manifest carries (`bytes`, `elements`, `paths`,
   `gradients`, `coordinates`), beside the fidelity numbers. No threshold: none
   was measured, and a gate on bytes would have refused a 195 KB trace and a
   59 KB accepted figure alike.
8. **What was looked at** — honestly, or nothing.

## Gotcha

- **A `<path>` is not evidence of a vector.** A raster embedded beside one dummy
  path passes a presence-of-`<path>` check and is not a vector; a mark built
  from `rect`/`circle` fails that check and is one.
- **CSS cannot stop SMIL.** `svg * { animation: none !important }` under an
  emulated `reduce` leaves an `<animate>` running. Route the animation itself.
- **An `<img>`-delivered SVG never sees the OS motion preference.** The host
  needs a `<picture>` with a `media="(prefers-reduced-motion: reduce)"` source
  pointing at a static file.
- **`screenshot({ animations: 'disabled' })` does not freeze SMIL.** Use
  `pauseAnimations()` + `setCurrentTime()`.
- **`transform-origin` without `transform-box` pivots against the view box**, not
  the element — per element, so a correct sibling proves nothing about it.
- **`keySplines` outside [0,1] stops the animation outright** rather than
  clamping it.

## Do NOT

- Do NOT report `verified` on a look, a parser pass, or a render of an earlier
  draft.
- Do NOT say "matches" or "100 %" about a conversion without the two numbers and
  the registration they were measured against.
- Do NOT rename ids or simplify paths as a side effect of a surgical edit.
- Do NOT restate motion, ARIA or render-security mechanism here — point at the
  authority and let it own the rule.
- Do NOT add a rasteriser, a tracing dependency, or an optimiser to the write path.

## See also

> Named rather than linked, and that is a correctness property rather than a
> style one: this skill ships in four packs, so a relative link to an artifact
> that lives in only one of them resolves for a consumer who installed that pack
> and is dead for the other three. The names are stable; the paths are not
> promises this skill can keep.

- `iconography` — the set comes first; this skill is
  for the glyph it lacks.
- `logo-generation` — the brand pipeline that
  routes a geometric mark here.
- `image-provider-routing` — illustrative
  vector art goes to a provider, not here.
- `fe-design` § Motion — the motion authority, in
  `references/design-patterns.md` § *Motion — decision-tree and rationale*. The
  SVG mechanism lines are step **6b, "Which mechanism carries it inside an
  SVG?"** — `transform-box`, `pathLength`, the `keySplines` range, path-morph
  command equality, and delivery mode picking the reduced-motion route. Cited
  here and never restated.
- `frontend-render-security` § *The
  patterns AI ships by default*, row **Untrusted SVG markup into an HTML sink**
  — the sinks an SVG carries into a host origin, and what each delivery mode
  can execute. Its § *Backstop greps* carries the grep that finds them.
- `design-intelligence` — diagram layout; its
  geometric pre-checks are witnessed by the asset profile now.
- `accessibility-auditor` — the ARIA
  corpus that answers what a graphic's accessible name has to be; its
  `data/aria-patterns.csv` carries the **Meaningful standalone graphic** and
  **Decorative graphic** rows this skill grounds against rather than copies.
- `canvas-design`, `wireframe`
  — the two lanes that use SVG as an execution surface.
- `design-fidelity` — a provided artifact is
  the spec; the baseline readout above is its surgical-edit witness.
- `docs/contracts/design-artifact-verification.md` — `frame_seek` and the other
  primitives the witness depends on.
