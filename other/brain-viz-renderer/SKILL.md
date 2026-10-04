---
name: brain-viz-renderer
description: Project-specific R3F patterns for the Brain Visualization 18k-node graph renderer — one InstancedMesh + LineSegments2/GL_LINES edge batches, in-place attribute rewrites, frameloop='demand' discipline, settle-debounced scans, additive-blend brightness budgeting, SpriteText font races, drei OrbitControls event topology, window-hook E2E probes, and the multi-agent git serialization discipline. Use when touching src/components/BrainScene.tsx, GraphCanvas.tsx, CameraRig.tsx, or building any new large-scale (10k+ instance) R3F scene in this repo.
---

# Brain Viz Renderer — hard-won patterns

This is the **project-specific companion** to the generic `r3f-*` skills (`r3f-geometry`, `r3f-interaction`, `r3f-performance`-adjacent lessons, etc.). Everything here was learned the hard way building `src/components/BrainScene.tsx` — an 18,140-node / ~96k-edge live 3D graph that has to hold 100+fps with a real force sim, progressive disclosure, and click/hover picking. Read `team/purav/knowledge.md` §5–6 for the architecture this skill assumes.

The core mistake this skill exists to prevent: **treating an 18k-node graph like a small React Three Fiber scene** — one `<mesh>` per node, geometry rebuilt on every state change, naive per-frame allocation. All of that works at 100 nodes and falls over hard past ~2,000.

## 1. One InstancedMesh for all nodes, per-kind LineSegments2 batches for edges

Don't render nodes as individual `<mesh>` elements. One `THREE.InstancedMesh` (flat `MeshBasicMaterial`, per-instance matrix + `instanceColor`) carries all 18,140 nodes in a single draw call:

```ts
const mesh = new THREE.InstancedMesh(sphereGeom, new THREE.MeshBasicMaterial({ toneMapped: false }), N);
mesh.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(N * 3), 3);
// per-frame: write matrices + colors in place (see §2), then:
mesh.instanceMatrix.needsUpdate = true;
if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
mesh.computeBoundingSphere(); // see the raycast gotcha in §3
```

Edges are **not** individual `<line>` elements either. Group by *kind* (here: `contains · indexed-by · has-layer · references · screen-of · migration-of` + a client-only `bridge` batch) into one `LineSegments2` (fat, real-pixel-width lines from `three/examples/jsm/lines/`) per kind — this gives you free per-kind toggles (visibility flip on one object) and per-kind styling (color/opacity/width) without touching geometry:

```ts
import { LineSegments2 } from 'three/examples/jsm/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/examples/jsm/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/examples/jsm/lines/LineMaterial.js';

const lines = new Map<BatchKind, LineSegments2 | THREE.LineSegments>();
// one LineSegments2 per structural kind:
const seg = new LineSegments2(geometry, new LineMaterial({ color, transparent: true, opacity, linewidth }));
```

**Exception — bulk straight hairlines get native GL_LINES, not fat lines.** `references` (67k+ edges in this graph, always straight, no zoom-adaptive width needed) render as plain `THREE.LineSegments` + `THREE.LineBasicMaterial` instead of `LineSegments2`. `LineSegments2` is instanced screen-space quads under the hood — at tens of thousands of edges that's fill-rate-bound and was the actual cause of a "heavy lag with references ON" bug. Native `LineSegments` is a real hairline draw, effectively free by comparison:

```ts
if (kind === 'references') {
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3)); // pairs, S=1
  const seg = new THREE.LineSegments(geom, new THREE.LineBasicMaterial({ color, transparent: true, opacity }));
}
```

Rule of thumb: reach for `LineSegments2` only when you need real pixel width or per-segment width variation; reach for native `LineSegments`/`LineBasicMaterial` for bulk background structure where a 1px hairline is fine.

## 2. In-place attribute rewrites — never rebuild geometry in a per-frame loop

A live force sim touching 825 component centroids every frame **must not** call `new THREE.BufferGeometry()` or reallocate typed arrays each tick. Every per-frame position update mutates the existing buffer attributes and flips one `needsUpdate` flag:

```ts
// nodes: rewrite the instance matrix in place
const m = new THREE.Matrix4();
for (let i = 0; i < N; i++) {
  m.compose(tmpPos.set(pos[i*3], pos[i*3+1], pos[i*3+2]), tmpQuat, tmpScale.setScalar(scale[i]));
  mesh.setMatrixAt(i, m);
}
mesh.instanceMatrix.needsUpdate = true;

// edges (LineSegments2): instanceStart/instanceEnd are ONE interleaved buffer —
// write with setXYZ, flip needsUpdate on the SHARED underlying attribute once.
const g = seg.geometry as LineSegmentsGeometry;
const startA = g.attributes.instanceStart as THREE.InterleavedBufferAttribute;
const endA = g.attributes.instanceEnd as THREE.InterleavedBufferAttribute;
for (let e = 0; e < E; e++) {
  const a = ab[e*2], b = ab[e*2+1];
  startA.setXYZ(e, pos[a*3], pos[a*3+1], pos[a*3+2]);
  endA.setXYZ(e, pos[b*3], pos[b*3+1], pos[b*3+2]);
}
startA.data.needsUpdate = true; // updating the SHARED interleaved buffer once covers both attrs

// native LineSegments: plain position BufferAttribute, same idea
const posAttr = seg.geometry.attributes.position as THREE.BufferAttribute;
posAttr.setXYZ(e*2, ax, ay, az);
posAttr.setXYZ(e*2+1, bx, by, bz);
posAttr.needsUpdate = true;
```

This same pattern re-arcs the **selection/hover overlay** every sim frame so highlights visually track moving nodes instead of freezing at select-time — store the endpoint *node indices*, not baked positions, and re-derive world positions from the live position array every frame:

```ts
// store WHICH nodes an overlay segment connects, not where they were when you made it:
seg.userData.segPairs = pairsInt32Array; // [a0,b0, a1,b1, ...] node indices
// every frame: re-derive positions from the CURRENT built.pos, write with setXYZ as above.
```

A real regression this caught: removing `mesh.computeBoundingSphere()` from the position-update path (in the name of "avoid per-frame work") silently broke `InstancedMesh.raycast()` — it early-rejects against a stale bounding sphere, so click/hover picking died with zero errors anywhere. `computeBoundingSphere()` belongs in the same "full pass" that runs on settle (not every frame — see §5), never dropped.

## 3. `frameloop='demand'` + invalidate discipline

The whole scene renders through `<Canvas frameloop="demand">`. That means **zero frames draw when nothing is moving** — a huge win for an 18k-node scene with a bloom post-process pass. It also means every single thing that changes visual state must call `invalidate()` explicitly, or the change silently never appears on screen until some unrelated event happens to trigger a frame:

```ts
const invalidate = useThree((s) => s.invalidate);
// after any imperative mutation the render loop wouldn't otherwise know about:
mesh.instanceColor!.needsUpdate = true;
invalidate();
```

Every `useFrame` callback that does per-frame physics/easing/disclosure work must **early-return with zero allocation** when idle (drag not active, sim at rest, no pending tween) — both because `frameloop='demand'` frames are precious and because an always-running per-frame allocator defeats the entire point of `demand` mode. Measured perf gain from adding an idle fast-path to one `useFrame` (the drag-easer): it now returns before any `Vector3`/`Matrix4` allocation on every orbit/zoom frame where nothing is dragging.

## 4. Settle-debounced scans, never per-frame predicates

Anything that decides "should this cluster's links be revealed / should this edge fade / is the camera far enough to switch bands" must **not** run a heavy predicate over thousands of candidates on every single frame. Pattern used throughout this codebase:

1. Throttle the check itself (e.g. every 250ms, and only if the camera moved ≥2 world units since the last check).
2. Compute the *desired* new state (which components should be revealed, which edges should fade).
3. Only if it differs from current state, start a **trailing debounce timer** (~150ms) before actually rebuilding geometry — so a camera that's still moving doesn't thrash rebuilds every check tick, only the final settled position triggers one.
4. Some passes (view-relevance edge fade, background-darkness dimming) are gated to run **only on camera SETTLE**, never mid-tween — computed once when motion stops, not accumulated per frame.

```ts
// throttle + move-gate
if (now - lastCheckRef.current < REVEAL_CHECK_MS) return;
if (camera.position.distanceTo(lastCheckPosRef.current) < REVEAL_MOVE_WU) return;
lastCheckRef.current = now;
// ...compute desired set...
if (setsDiffer(desired, current)) {
  clearTimeout(pendingRef.current.timer);
  pendingRef.current = { pending: desired, timer: setTimeout(rebuildGeometry, REVEAL_DEBOUNCE_MS) };
}
```

The one thing that must stay off this pattern: **hover**. Hover was originally gated behind the same sim/auto-detail conditions as disclosure and it silently drew a tooltip with no links — the fix was making hover **unconditional** (no sim/band gate, capped at 200 edges) because a user hovering expects an immediate response, not a debounced one.

## 5. Per-instance colors for dim/fade — never a global dim pass over all nodes

Don't touch every node's material or run an O(N) dim pass to highlight a selection — recolor only the instances that actually changed:

```ts
// selection change: touch exactly the previous and new selected instance, nothing else
mesh.setColorAt(prevSelIdx, prevColor);
mesh.setColorAt(newSelIdx, SELECTED_COLOR);
mesh.instanceColor!.needsUpdate = true;
```

The same principle extends to background dimming (proximity-based, §6): a node is either "local" (in view / revealed) or "background," and only nodes whose local/background *classification changed since the last settle* get their `instanceColor` entry rewritten — the classification itself is O(N) once per settle (cheap, not per frame), but the color writes are gated to only the deltas.

## 6. Additive-blend brightness budgeting (density-damped ramps)

Additive blending (`THREE.AdditiveBlending`) on edges is what makes overlapping links "glow" under bloom — but it **compounds multiplicatively** with every other brightness knob: per-kind base opacity × a zoom-adaptive width/opacity ramp × a reveal boost × bloom intensity. Tuned in isolation each factor looks fine; stacked at high edge density (e.g. diving toward a hub where 10k+ edges converge, or manual mode with every kind on) they multiply into a blown-out "supernova."

Fix: **damp the ramps by a cheap density proxy** (total currently-visible edge count), not by anything expensive to compute:

```ts
const visibleEdges = countVisible(); // cheap: sum of batch counts already tracked
const densityT = clamp((visibleEdges - DENSE_LOW) / (DENSE_HIGH - DENSE_LOW), 0, 1); // 0=sparse, 1=dense
const zoomBoost = lerp(fullBoostRamp, baseRamp, densityT); // full readability boost only when sparse
```

Sparse close-ups (a handful of edges) keep the full "pop out and read clearly" boost; dense views (tens of thousands of edges) collapse toward the flat base ramp so the compounding stack never blows out. Any time you're tuning a "make it brighter when X" ramp on an additive-blended batch, ask what happens when X and Y and Z all max out simultaneously — that's the real test, not the isolated slider sweep.

## 7. SpriteText font-loading race

`three-spritetext` (`SpriteText`) bakes its label into a `<canvas>` texture **at construction time**, using whatever font is currently available. If your custom webfont (e.g. IBM Plex Sans, loaded via `@font-face`/Google Fonts `<link>`) hasn't finished loading yet when the first batch of `SpriteText` instances is created, the texture is permanently baked with the browser's fallback font — setting `.fontFace` afterward does **not** retroactively fix already-baked sprites; it only affects the *next* bake.

The fix is a two-part gate:
1. **Wait on `document.fonts.ready`** (or the specific `document.fonts.load('<font spec>')` promise) before constructing the first wave of label sprites, so the common case never hits the race.
2. **For any sprite that could plausibly be created before the gate resolves** (e.g. build-up animation labels appearing in the first second), keep a re-bake path: after `document.fonts.ready` fires, force a setter re-assignment on already-constructed `SpriteText` instances (reassigning `.text` or `.fontFace` triggers `three-spritetext`'s internal canvas re-render) rather than assuming the initial bake is final.

```ts
document.fonts.ready.then(() => {
  // re-trigger a canvas re-bake on every already-created label so a fallback-font
  // bake from before the webfont loaded gets corrected — reassignment, not mutation,
  // is what triggers three-spritetext's internal redraw.
  for (const sprite of existingLabelSprites) {
    // eslint-disable-next-line no-self-assign
    sprite.text = sprite.text;
  }
});
```

Watch for this any time labels look correct on a hard refresh (fonts cached) but wrong/system-font on a cold load or in CI/Playwright screenshots (fonts not yet warm) — that asymmetry is the signature of this race.

**Two more SpriteText sharp edges (island-landmarks build, 2026-07-06):**

1. **`padding`/`borderRadius`/`borderWidth` are in WORLD units (textHeight-relative), not pixels.** `_genCanvas` computes `canvasPx = value × fontSize / textHeight`. At world-fixed heights of 8–22 a padding of `2.5` rasterizes ~17px — fine. But construct a sprite with a tiny `textHeight` (e.g. ~0.01 for a `sizeAttenuation:false` screen-space label) and the same `2.5` rasterizes a **~43,000×43,000px canvas → GL_OUT_OF_MEMORY → WebGL context lost** (hit live; the only console evidence was `Texture has been resized from (43928x43516)` warnings before the context died). Always express these as a *ratio of textHeight* (`t.padding = 0.19 * t.textHeight`), never as absolute numbers copied from another sprite with a different height scale.

2. **World-fixed label heights are unreadable at whole-brain distance — use `sizeAttenuation:false` for wayfinding labels.** Measured: a 13wu static label at the default fit (dist ≈ 2.3×maxR ≈ 10,300wu, 900px viewport, fov 50) projects to ~1.2px. Persistent far-view labels (the island landmarks) instead set `material.sizeAttenuation = false` — screen px = `scale.y × (viewportH/2)/tan(fov/2)`, constant at every distance (map-label behavior) — plus `fog=false`, `depthTest=false`, `depthWrite=false` so a label at a cloud centroid is never fogged out or speckled by member spheres.

**E2E footnote — `__viz.diagView('nodes'|'centroids'|'spines'|'off')`** reproduces the layout critique's three diagnostic views live (edges hidden / ~109 island-centroid proxies only / 825 depth-3 spines only / full restore) via visibility+matrix flips, no rebuilds. And when a `__teleportNear` probe reads a stale band on a fresh page, check `__edgeStats().auto` FIRST — a persisted preset (`activePreset` in localStorage) boots the app in manual mode where the band scan is intentionally frozen; that's persistence working, not a band bug.

## 8. drei OrbitControls event topology — preventDefault yes, stopPropagation NEVER

`@react-three/drei`'s `<OrbitControls>` attaches its own native event listeners to **R3F's event root** (a DOM element R3F manages, which is a *parent* of your `<canvas>` in the tree, not the canvas element itself, and definitely not whatever inner wrapper `<div>` you may have added for your own event handling). This has a sharp, non-obvious consequence:

**If your own wheel/pointer handler on the canvas (or a wrapper) calls `stopPropagation()`, you starve OrbitControls' listener on the parent root entirely** — even though your handler is "on the canvas" and OrbitControls is "further up," the event never bubbles that far. This produced a real, user-visible outage: "zoom is dead, is the site stuck" — traced to a wheel handler that called `stopPropagation()` unconditionally to stop page-level scroll/zoom.

The fix, and the rule going forward: **use `preventDefault()` alone.** A non-passive listener's `preventDefault()` cancels the browser's default action (page scroll, ctrl+wheel zoom, trackpad pinch-zoom) *without* stopping the event from bubbling — so your own logic runs, the page doesn't zoom, and OrbitControls (or anything else listening further up the tree) still receives the event normally.

```ts
// CORRECT — blocks page zoom/scroll, does NOT starve OrbitControls up the tree
el.addEventListener('wheel', (ev) => {
  ev.preventDefault();       // yes: kill the browser default action
  // ...your own logic (custom dolly math, nav-detection pulse, etc.)...
}, { passive: false });      // must be non-passive for preventDefault to have any effect

// WRONG — silently breaks any ancestor listener (OrbitControls' root-level handler)
el.addEventListener('wheel', (ev) => {
  ev.preventDefault();
  ev.stopPropagation();      // NEVER do this if OrbitControls (or anything else) is
                              // listening on an ancestor element
}, { passive: false });
```

When debugging "a control stopped working after an unrelated event-handling change," check every `stopPropagation()` call added anywhere in the DOM ancestor chain between the event's origin and wherever the "broken" listener actually lives — with a library like drei that attaches to an R3F-managed root you don't directly render, that ancestor chain is not obvious from reading your own JSX.

**Verifying the fix must assert the actual effect, not just the absence of the symptom.** The first attempt at fixing a broken-zoom regression was verified by checking "no console errors" and "the leak (page scroll) doesn't happen anymore" — both passed, but zoom was *still* dead, because the fix only addressed one half of the bug. The correct verification asserts the **consumer's actual effect**: drive N wheel events, then assert the camera's distance-to-target actually changed by the expected amount. "The bad thing stopped happening" is necessary but not sufficient evidence that "the good thing now happens."

## 9. The window-hook E2E convention

There is no committed Playwright test suite in this repo — verification is interactive, via `mcp__playwright__*` tools driving a live build. To make that verification precise instead of screenshot-eyeballing, every non-trivial internal state gets a **debug hook on `window`**, attached once per graph build/mount:

```ts
useEffect(() => {
  const w = window as unknown as Record<string, unknown>;
  w.__edgeStats = () => ({
    // return PLAIN, JSON-serializable data — a Playwright probe does
    // `page.evaluate(() => window.__edgeStats())` and needs a structured-cloneable result.
    band: bandRef.current, navMode: useGraphStore.getState().navMode,
    visible: countsPerKind(), zoomW: zoomWRef.current, alpha: simAlphaRef.current,
  });
  w.__viz = { set: (...) => {...}, select: (id: string) => {...}, flyToComp: (name: string) => {...} };
  return () => { delete w.__edgeStats; delete w.__viz; };
}, [built]);
```

Rules that keep this convention useful instead of a maintenance trap:
- **Name hooks for what they return, and document the signature in a comment right next to the assignment** — a hook named `__screenPos` that actually takes a component *name* and returns *client pixel* coordinates (not world xyz) caused a real mis-call during verification. The name alone doesn't disambiguate units or argument shape; a nearby comment does.
- Prefer **imperative action hooks** (`__viz.select(id)`, `__viz.flyToComp(name)`) over trying to simulate real pointer events for anything that isn't specifically testing pointer-handling code — synthetic pointer events have real gaps (e.g. `setPointerCapture`/`releasePointerCapture` throw under Playwright's synthetic dispatch and can leave OrbitControls' internal state stuck mid-drag; this is a harness artifact, not a product bug, and re-testing with a real trusted pointer event is the way to confirm that).
- Clean up hooks in the `useEffect` return so a hot-reload or graph rebuild doesn't leave a stale closure attached to `window`.

## 10. Multi-agent serialization discipline

This repo is worked by multiple concurrent agents on the same branch (`feat/layout-v3`). The discipline that keeps that from corrupting work:

- **One writer per file, always.** Before editing a file another agent might be mid-flight on, check `git status`/`git diff` for uncommitted changes there first. If a file is mid-edit by someone else and you don't strictly need to touch it, don't — route your verification around it (see the clean-room pattern below) rather than risking a bad merge of half-finished work.
- **`git pull --rebase origin <branch>` before starting *and* immediately before pushing**, every time, no exceptions — with several agents landing commits, the remote moves under you between when you start and when you're ready to commit.
- **Clean-room verification when you can't safely rebuild the shared dev server:** if a teammate/concurrent agent has an uncommitted, possibly-broken change sitting in the working tree (e.g. a mid-flight `tsc` error), don't run `pnpm build` in the shared checkout — it will pick up their broken file and fail, or worse, succeed and silently serve their half-finished state on the shared `:3000`. Instead: `git archive HEAD | tar -x -C /tmp/cleanroom`, copy in *only* the files you actually changed, hardlink-clone `node_modules` (`cp -al` or equivalent — instant, no real copy), `next build` there, and serve on a scratch port (`:3100`) for your own Playwright verification. The shared `:3000` build and the shared `.next` cache are never touched by your verification run.
- **Retry pushes** (rebase-fetch-retry, e.g. 3 attempts with a short backoff) rather than force-pushing when a push is rejected — a concurrent agent's commit landing between your rebase and your push is the expected case, not an error state.
- **Sweep verification artifacts before committing.** Screenshots and `.playwright-mcp/` directories accumulate fast during interactive verification; move them to `/tmp/` (never commit them) as a matter of routine, not just when you remember.

## See Also

- `r3f-fundamentals` — Canvas/useFrame/useThree basics this scene is built on
- `r3f-geometry` — general instancing patterns (this skill covers the *scaled-up, live-mutated* case)
- `r3f-interaction` — general controls/raycast/event patterns (this skill covers the drei/OrbitControls-specific event-topology gotcha)
- `r3f-postprocessing` — Bloom/EffectComposer basics (this skill covers the antialias-off + additive-brightness-budget specifics)
- `team/purav/knowledge.md` — the full end-to-end architecture this skill's patterns live inside
