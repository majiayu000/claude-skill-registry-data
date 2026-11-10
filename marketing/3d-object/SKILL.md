---
name: 3d-object
zh_name: "3D 物体"
en_name: "3D Object"
emoji: "🧊"
description: "A product or object in 3D — built from shapes, extruded from a logo, or loaded from your own .glb — lit like a studio shot, turning on a turntable, ready to export as a still, a transparent cut-out or a turntable video."
zh_description: "3D 产品或物体:用基本形体搭建、由 Logo 挤出, 或载入你自己的 .glb 模型;摄影棚光照与转台, 可导出静帧、透明抠图或转台视频"
en_description: "A product or object in 3D — built from shapes, extruded from a logo, or loaded from your own .glb — lit like a studio shot, turning on a turntable, ready to export as a still, a transparent cut-out or a turntable video."
category: 3d
scenario: marketing
tags: ["3d", "three.js", "webgl", "product shot", "turntable", "glb", "gltf", "logo", "3D 模型", "产品图"]
triggers:
  - "3d"
  - "3d object"
  - "3d model"
  - "product shot"
  - "turntable"
  - "glb"
  - "gltf"
  - "3d logo"
  - "hero render"
  - "3D 模型"
  - "产品渲染"
od:
  mode: prototype
  craft:
    requires:
      - color
      - anti-ai-slop
  platform: desktop
  scenario: marketing
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "Make a 3D hero shot of our speaker, a soft cylinder with a glowing ring on top, in our brand colors, turning slowly — then export a transparent PNG and a turntable MP4."
---

# 3D Object

**Intent.** One object, shown well: a product, a logo or a simple form, lit like a studio photo, on a quiet stage, turning slowly. The page is a single self-contained three.js scene. People use it as a hero visual, export a still or a transparent cut-out for slides and pages, or a turntable clip for social.

This is not a 3D editor, a game scene or text-to-3D generation. If the user wants a model of something that doesn't exist yet and can't be built from simple shapes, say so and offer a procedural stand-in.

## 1. Pick the object path

- **Procedural:** build the object from three.js geometry: `LatheGeometry` for anything turned (bottles, speakers, cups, lamps), `ExtrudeGeometry` for flat shapes with depth, boxes and cylinders with bevels (`RoundedBoxGeometry` from the addons) for devices. Combine a few parts in a `Group`. Aim for the silhouette and proportions first; small details (a groove, a light ring, a seam) make it read as a product.
- **Extruded logo:** parse the brand's SVG with `SVGLoader`, turn each filled path into shapes (`SVGLoader.createShapes`), and extrude with a bevel. Flip y (SVG's y points down), center the geometry, and scale it to a fixed size. Strokes aren't extruded; ask for a filled version of the mark if that's all there is.
- **The user's model (`.glb` / `.gltf`):** load it with `GLTFLoader`. Copy the file under `assets/` next to the design (with a shell copy: it's binary) and load `assets/<name>.glb`; if you can't copy it, use its path relative to the design. Set up `DRACOLoader` with the pinned decoder path (below) so Draco-compressed models work. Never assume the model's units, origin or orientation: measure its bounding box, rest it on the ground, center it, and frame the camera from its size (the GLB example's `stage()` does exactly this). If the file is over 50 MB, tell the user it will load slowly and suggest `npx @gltf-transform/cli optimize in.glb out.glb --compress draco` first.

## 2. Build the scene

Use exactly these pinned URLs, through an import map:

```html
<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
} }
</script>
```

Draco decoder path: `https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/libs/draco/gltf/`.

Don't write three.js script tags from memory: `build/three.min.js` no longer exists (removed in r160), nor does `examples/js/…` (removed in r148), so `<script src=".../three.min.js">` 404s, `THREE` is undefined and the page shows nothing. Use the import map above and `import * as THREE from 'three'` in a `<script type="module">`, with addons from `three/addons/…`.

- **Canvas:** one full-bleed `<canvas id="stage" data-od-webgl>` passed to `WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true })`. Size it from the canvas's CSS box on load and on `resize`. On tall, narrow canvases (aspect below 1), frame the object again so it fills the portrait frame as it fills the desktop one: widen the `fov` and move the camera back only as far as the object needs (the `fitView` snippet in the `3d-scene` skill does this from the object's bounding sphere). The check measures how much of each frame the object fills.
- **Color:** `outputColorSpace = SRGBColorSpace`, `toneMapping = ACESFilmicToneMapping`.
- **Materials:** physically based (`MeshStandardMaterial` / `MeshPhysicalMaterial`), with colors read from the design system's tokens (`getComputedStyle(document.documentElement).getPropertyValue('--accent')`) so the object matches the page: the body from `--surface` or `--fg`, one detail from `--accent`. Choose roughness and metalness for the real material (matte plastic 0.6–0.9 rough, brushed metal metalness 1 at 0.25–0.4 rough, glossy paint with `clearcoat`). Keep a user model's own materials unless asked to recolor it.
- **Light:** the `studio` setup by default: studio light from a generated room (`scene.environment = new PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture`, `envMapIntensity` about 0.6), a shadow-casting key `DirectionalLight` `#fff4e6` at intensity 3 from 45° to the side and 40° up (soft shadows: `PCFSoftShadowMap`, `shadow.radius` about 6), a fill `#e6eeff` at 0.9 from the other side and a rim at 2 from behind, exposure 1.0. When the brief sets a scene (daylight, a lamp, a fire, dusk), use that setup from the `3d-scene` skill's light table instead; a light you can see is the key and points at the object. The object is the brightest thing in the frame that isn't a light. When real reflections matter (glass, chrome, glossy paint) or the brief names a setting's light (a sunset, a studio, a forest), find an HDRI with `find_open_design_3d_assets` (`type: "hdri"`, free CC0 files from Poly Haven) and light from it: `new RGBELoader().loadAsync(url)` from `three/addons/loaders/RGBELoader.js`, then `scene.environment = pmrem.fromEquirectangular(tex).texture`. Load it inside `ready`. The same tool finds PBR textures (wood, metal, fabric) and models when shapes alone won't do. List every remote file you use in the head, so a `standalone` export (`embedAssets: true`) or a Claude artifact can carry it inside the page: `<script type="application/od-assets+json">[{ "source": "polyhaven", "id": "studio_small_09", "url": "https://dl.polyhaven.org/…/studio_small_09_1k.hdr", "license": "CC0" }]</script>`.
- **Glass:** don't use `transmission`: it renders unreliably in software WebGL, where checks and exports run, and costs an extra render per frame. Use a thin clear shell instead (`MeshPhysicalMaterial` with `transparent: true`, `opacity` 0.1–0.2, `roughness` about 0.03, `clearcoat: 1`, `envMapIntensity` about 1.6, `depthWrite: false`), and light it from an HDRI so it shows real highlights.
- **Stage:** a large ground plane with `ShadowMaterial` (opacity 0.12–0.2) under the object. When the brief asks for a setting (a hall, a desk, a shelf), build it as an environment: put it in its own group with `userData.odStage = true` (the object itself is never inside that group), and keep it darker, softer and less detailed than the object so it never competes with it. Review views frame the object and leave the stage out. `scene.background` is the `--bg` color, or `null` for a transparent cut-out.
- **Controls:** `OrbitControls` with damping, no pan for single objects, `maxPolarAngle` just under 90° so the camera never goes below the floor, and min/max distance around the framed distance.
- **Budget:** at most about 200k triangles and 2048 px textures, so it stays smooth in software rendering. Lathe and torus segments of 64–160 are plenty.
- **Transparent option:** a `TRANSPARENT` constant at the top. When true: `alpha: true` on the renderer, `scene.background = null`, and a class on `<html>` that makes the page background transparent and hides any caption.
- **Page:** the scene fills the window. A short caption (product name, one line) in the design system's type is fine; keep it in a corner and out of the object's way.

## 3. The ready contract (required)

Exports, the visual check and motion export rely on it:

```js
const start = performance.now();
window.odScene = { rotate: true, rotationSeconds: ROTATION_SECONDS, duration: ROTATION_SECONDS, ready: undefined, scene, camera, renderer, controls };
function pose(now) {
  const turn = window.odScene.rotate ? (((now - start) / 1000) / ROTATION_SECONDS) * Math.PI * 2 : 0;
  product.rotation.y = AUTHORED_ANGLE + turn;
}
window.odScene.ready = (async () => {
  await loadEverything();            // the model, textures, fonts for 3D text
  pose(performance.now());
  renderer.render(scene, camera);    // a direct render, not inside requestAnimationFrame
})();
renderer.setAnimationLoop((now) => { pose(now); controls.update(); renderer.render(scene, camera); });
```

- `ready` resolves only after every asset has loaded and one frame has been drawn **with a direct `render()` call**. Motion export runs the page on a virtual clock where animation frames only advance on its schedule, so a `ready` that waits for an animation frame would never resolve there.
- The turntable angle is computed from time (`performance.now()` or the loop's timestamp), never incremented per frame, so a rotation takes exactly `ROTATION_SECONDS` at any frame rate.
- `rotate = false` returns the object to `AUTHORED_ANGLE`. Still exports set it, so choose the authored angle as the best three-quarter view.
- `scene`, `camera` and `renderer` are required: the check uses them to render the review views (overview, close-up, low angle, wireframe) and to read the renderer's triangle and draw-call counts. Pass `controls` too when there are orbit controls. Set `focus` to the object (its group): the check measures the still's framing and light on it at desktop and mobile. Optional: `subject` (the group to frame in review views, when the stage flag isn't enough), a `[x, y, z]` `focus` instead when only the close-up should aim at a detail, and `views` (`{ low: { position: [x, y, z], target: [x, y, z] } }` to replace a computed view).

## 4. Register and check

1. `register_open_design_artifact` with kind `html` and this skill as the source.
2. `check_open_design_artifact`. Exports and the check switch on software WebGL for pages with `data-od-webgl` or a three.js import, so this works without a GPU. Fix every `webgl` finding: an error means no WebGL context (a script error before the renderer was made, or a canvas without the attribute's renderer); a warning means the canvas is a flat color (the model didn't load: see `broken-asset`; the camera is inside or away from the object; or `ready` resolved before anything was drawn). Fix a `webgl-budget` warning by instancing or merging repeated meshes and lowering segment counts. Fix every `framing` warning (the object too small, cut off, or a flat object edge-on in the still) and `light` warning (the object darker than its surroundings) before the critique.
3. The second image is the **review sheet**: overview, close-up, low angle and wireframe in one picture. The text adds pixel metrics and renderer counts. A clean check only means the page renders; it says nothing about whether the object looks right. That's the critique's job.

## 5. Critique (required before you say it's done)

A design that passes the check can still be plainly wrong: a board with no squares, glass that reads as grey plastic, a model floating above its stand. After the check has no errors, get a critique from someone who didn't build it:

- **Who critiques.** In Claude Code, launch a subagent with the Agent tool. In VS Code, use the `runSubagent` tool when it's available. Otherwise (Codex, or no subagent tool), do a separate critic pass yourself: judge only the review sheet and the brief, not what you meant the code to do.
- **The critic's brief.** Give it the user's brief, the entry path and the scorecard below. It must call `check_open_design_artifact` itself and judge from the images. It returns:
  - a score for each category;
  - any automatic failure;
  - at least three flaws, each naming the view it's visible in, where in the frame, and a concrete fix (e.g. "low view: the board floats above a smaller hexagonal base; make the base wider than the board, or put the board on legs");
  - after finding a flaw, a check for others of the same kind (if one piece floats, look at every piece).
- **Loop.** Fix the flaws, check again, and get a new critique. Stop when the scorecard passes, or after **three** critique rounds. Then tell the user the final scores and any flaws that remain. Don't paste the critique itself unless they ask.

**Scorecard.** Score each category 0 (placeholder), 1 (basic), 2 (finished) or 3 (showcase):

| Category | 1 | 2 | 3 |
|---|---|---|---|
| Form | primitives that only suggest the object | authored silhouette and true proportions, recognizable as a dark shape | memorable silhouette with functional detail where the camera looks |
| Materials | flat colors, one roughness everywhere | each surface reads as its real material (glass, wood, metal, stone) | rich, cohesive materials with wear, trim or texture |
| Light | even light, washed out or murky | intentional key, fill and contact shadow; the form reads | cinematic light that still shows the form clearly |
| Composition | object small, cut off or off-center without reason | object fills the frame well at the authored angle and on mobile | framing that adds drama or story |

Judge **composition** on the desktop and mobile screenshots, which show your own camera. The review views are framed by the check itself, so they always fill the frame.
| Stage | missing, or competes with the object | quiet ground or environment that supports the object | an environment that adds context and depth without stealing focus |
| Fidelity | misses or misreads what the brief asked for | everything the brief names is present and recognizable | details the brief implied but didn't spell out |
| Technical | check errors, or budget warnings ignored | clean check, within budget, loops seamlessly | clean, light and fast to export |

**Automatic failures** (the scorecard fails whatever the scores):

- something the brief names is missing or unrecognizable;
- the object is an unrefined primitive placeholder;
- fog, darkness or glow stands in for missing geometry;
- the object floats above, or passes through, what it rests on (low and wireframe views);
- the object fills less than 40% of the desktop screenshot's height without a reason the brief gives;
- the check reports an error.

**Pass:** every category at least 2, and no automatic failure.

## 6. Export

- **Still:** `export_open_design_artifact` with `format: "png"` (or a preset). Add `selector: "#stage"` to capture only the scene.
- **Transparent cut-out:** set `TRANSPARENT = true` in the file (or make a copy that does), then export with `format: "png"`, `transparent: true`. A warning that no pixel is transparent means the page or scene still paints a background.
- **Turntable:** `format: "mp4"` (or `"gif"` for a small loop, `"webm"`). With `odScene.duration` set to `ROTATION_SECONDS`, the export is exactly one turn and the loop is seamless, with no `duration` to pass. Keep `ROTATION_SECONDS` between 6 and 12; a GIF loops best at 6–8 seconds and 480–720 px wide.
- The scene loads three.js from the CDN, so viewers need a connection, including for `standalone` exports.
