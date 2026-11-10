---
name: 3d-scene
zh_name: "3D 场景"
en_name: "3D Scene"
emoji: "🏛️"
description: "A small 3D world: several objects in a setting (a diorama, a room, a courtyard, a tabletop, a little landscape), planned first, lit by a real sky, textured with free CC0 assets, as stills or a camera flythrough video."
zh_description: "小型 3D 场景:多个物体组成的环境(微缩景观、房间、庭院、桌面、小型地形),先规划后搭建,真实天空光照与免费 CC0 素材,可导出静帧或镜头漫游视频"
en_description: "A small 3D world: several objects in a setting (a diorama, a room, a courtyard, a tabletop, a little landscape), planned first, lit by a real sky, textured with free CC0 assets, as stills or a camera flythrough video."
category: 3d
scenario: marketing
tags: ["3d", "three.js", "webgl", "scene", "diorama", "environment", "flythrough", "hdri", "poly haven", "3D 场景", "微缩景观"]
triggers:
  - "3d scene"
  - "diorama"
  - "3d room"
  - "3d environment"
  - "flythrough"
  - "3d world"
  - "3d courtyard"
  - "3D 场景"
  - "微缩景观"
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
  example_prompt: "A small stone courtyard at dusk: cobblestones, rough stone walls on three sides, a brass lantern on a post, two potted plants, a warm sky. Then give me a still and a 10-second flythrough video."
---

# 3D Scene

**Intent.** A small world shown well: several objects that belong together in one setting (a diorama, a corner of a room, a courtyard, a tabletop, a small landscape), lit by a real sky, framed by a camera that knows where to look, and optionally moving through it. The page is one self-contained three.js scene. People use it as a hero visual, a still, or a short flythrough clip.

Use `3d-object` instead for a single product or logo on a stage. This isn't a game: no player, physics or input beyond orbiting.

## 1. Plan before you build

Write the **scene spec** first, as a block in the page, and build everything from it:

```html
<script type="application/od-scene+json" id="scene-spec">
{
  "explicit": ["stone courtyard", "dusk", "brass lantern", "two potted plants", "10 s flythrough"],
  "inferred": ["8 × 6 m floor", "walls 2.4 m high on three sides", "lantern on a 1.6 m post, left of center"],
  "units": "m",
  "seed": 7,
  "layout": [
    { "name": "floor", "position": [0, 0, 0], "size": [8, 0.1, 6] },
    { "name": "lantern", "position": [-1.2, 1.6, 0.5], "size": [0.12, 0.29, 0.1] }
  ],
  "focal": "lantern",
  "views": {
    "hero": { "position": [5.5, 2.4, 6.5], "target": [-0.6, 1.2, 0.3], "fov": 40 },
    "heroPortrait": { "position": [4.2, 2.0, 5.6], "target": [-0.8, 1.3, 0.4], "fov": 52 }
  },
  "path": [
    { "t": 0, "position": [6.5, 2.8, 7.5], "target": [0, 1, 0] },
    { "t": 10, "position": [2.5, 1.6, 3.5], "target": [-1, 1.2, 0] }
  ],
  "duration": 10,
  "assets": [{ "source": "polyhaven", "id": "Lantern_01", "url": "https://dl.polyhaven.org/…/Lantern_01_1k.gltf", "license": "CC0" }]
}
</script>
```

- `explicit` holds only what the user said. Everything you decided goes in `inferred`, so the user can see and change your assumptions.
- Sizes are real meters. Use the asset tool's sizes for models. A model made at real size and shrunk (a 1:87 kart) records `"scale": "1:87"` on its asset.
- `focal` names the `layout` item (or a group of items) the scene is about. There is one focal point; everything else supports it.
- Before building anything non-trivial, show the user the layout and views as a short table. For anything that must be spatially exact (a real place, a floor plan, a recreated photo), draw a top-down SVG with meter dimensions and get it confirmed first.
- The page reads the block (`JSON.parse(document.getElementById('scene-spec').textContent)`) to place objects and drive the camera, so the spec and the render can't disagree.

## 2. Blockout, then finished

For a scene with more than about five objects, build a **blockout** first: boxes and simple forms at the final positions and sizes, with the final camera and light. Set `window.odScene.tier = "blockout"`, check it, and get one critique on layout, scale and framing only. Then build the finished scene (`tier: "finished"`, the default). Never show a blockout to the user as the result.

## 3. Build the scene

Use exactly these pinned URLs, through an import map:

```html
<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
} }
</script>
```

Don't write three.js `<script src>` tags from memory: `three.min.js` is gone since r160 and `examples/js` since r148.

- **Canvas and renderer:** one full-bleed `<canvas id="stage" data-od-webgl>`; `WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true })`, `outputColorSpace = SRGBColorSpace`, `toneMapping = ACESFilmicToneMapping`, pixel ratio capped at 2, sized from the canvas's CSS box on load and resize.
- **Assets:** call `find_open_design_3d_assets` for what procedural code can't make convincingly: a sky, stone, wood, plaster, a lantern, a chair, a plant. It returns free CC0 files from Poly Haven with direct URLs. Use 1k files; 2k only for the hero object. If it can't reach Poly Haven, build procedurally and say so.
  - **Sky (HDRI):** `new RGBELoader().loadAsync(url)`, then `scene.environment = pmrem.fromEquirectangular(tex).texture`, and `scene.background = tex` (with `tex.mapping = EquirectangularReflectionMapping`) when the sky should show. The lights go with it as in section 4.
  - **Textures:** load diffuse with `colorSpace = SRGBColorSpace`; normal, roughness and ARM stay linear. Set `wrapS`/`wrapT` to `RepeatWrapping` and `repeat` to the surface size in meters divided by about 2 (most Poly Haven textures cover about 2 m). An ARM map is AO in red, roughness in green, metalness in blue: use it as `aoMap`, `roughnessMap` and `metalnessMap` together.
  - **Models:** a Poly Haven `.gltf` refers to its `.bin` and textures by relative paths that don't exist on the CDN. Pass the tool's `includes` map through a loading manager:

    ```js
    function polyHavenLoader(includes) {
      const manager = new THREE.LoadingManager();
      manager.setURLModifier((url) => {
        for (const [rel, abs] of Object.entries(includes)) if (url === rel || url.endsWith('/' + rel)) return abs;
        return url;
      });
      return new GLTFLoader(manager);
    }
    const gltf = await polyHavenLoader(lanternIncludes).loadAsync(lanternUrl);
    ```

    Measure each model's bounding box, scale it to its `layout` size, rest it on what it stands on, and turn on `castShadow`/`receiveShadow` for its meshes. Clone a loaded scene (`gltf.scene.clone()`) to place it again: clones share geometry.
  - **Offline:** to work without a connection, download each file into `assets/` with your terminal, keeping the `.gltf`'s relative layout (`assets/<id>/<id>_1k.gltf`, `assets/<id>/textures/…`). Then load the local paths with no URL map.
  - **Record every asset** in the scene spec's `assets` (source, id, URL, license). Poly Haven assets are CC0, so no credit is required on the design.
- **Stage:** mark the sky, ground and backdrop meshes `userData.odStage = true` when they're large or far, so the review views frame the scene, not the horizon. The objects the scene is about are never stage, and never children of a stage group: add a brazier to the scene, not to the hall group, or the review hides it as a wall in the way.
- **Composition:** one clear focal point (the `focal` item), with near, middle and far layers for depth. Light leads the eye to it (section 4) and the camera frames it (section 5). Leave breathing room; don't fill every gap with props.

## 4. Light

Pick one setup for the brief and start from its numbers (three r160, ACES tone mapping). **Brightness `E`** is what a light delivers at the focal subject. A `DirectionalLight`'s intensity is `E`. A `PointLight` or `SpotLight` (decay 2) needs intensity `E × d²`, where `d` is its distance to the focal subject in scene units, so the same numbers work at any scale (a 20× chess hall or a 1:1 desk).

| Setup | When | Key | Fill and rim | Environment, exposure |
|---|---|---|---|---|
| `studio` | products, a tabletop on a sweep | `DirectionalLight` `#fff4e6`, `E` 3, 45° to the side, 40° up, the one shadow caster | fill `#e6eeff` `E` 0.9 from the other side, low; rim `E` 2 from behind, above | `RoomEnvironment`, `envMapIntensity` 0.6; exposure 1.0 |
| `daylight` | outdoors by day | `DirectionalLight` `#fff1dc`, `E` 3.5, from the HDRI's sun direction, shadow camera tight on the scene | none; the sky fills | day HDRI, `envMapIntensity` 1.0, shown as background; exposure 1.0 |
| `interior-lamp` | a desk or room lit by a lamp | `SpotLight` `#ffcf99` (2700 K) **at the lamp head, aimed at the focal subject**, `E` 3, angle 0.6, penumbra 0.6, the one shadow caster; an emissive bulb mesh | window fill: `DirectionalLight` `#cfdcff` `E` 0.6 from the window side, no shadow; `HemisphereLight` `#e8e2d8`/`#3a3028` at 0.5 | interior HDRI or `RoomEnvironment`, `envMapIntensity` 0.3; exposure 0.9; walls darker than the desk |
| `fire-lit` | a hall or camp lit by fire | `PointLight` `#ff8a3c` **at the flame**, `E` 4 at the focal subject, the one shadow caster (1024 map, bias −0.002); flicker ±15% from time, not per frame | cool fill: `HemisphereLight` `#2a3550`/`#120c08` at 0.15; a warm rim `PointLight` `E` 1 behind the subject, no shadow | `envMapIntensity` 0.15; exposure 1.1; flames as additive sprites with a soft gradient texture, never cones |
| `dusk` | outdoors at sunset or blue hour | `DirectionalLight` `#ffb070`, `E` 2, low (10–15° up) and raking across the focal subject | practicals (lanterns, windows): `PointLight` `#ffb45a`, `E` 1.5 at what they light, no shadow | dusk HDRI, `envMapIntensity` 0.6, shown as background; exposure 1.0 |

Rules for every setup:
- **A light you can see is the key.** A lamp, fire or window in the scene is where the main light comes from, and it is aimed at the focal subject (`spot.target`, or a fire placed so the subject is the nearest thing it lights). Don't add an unrelated sun to a lamp-lit room.
- **The focal subject is the brightest thing that isn't a light.** If a wall, the floor or a backdrop is brighter, darken it (lower albedo, move it out of the key's cone) rather than raising everything.
- **A fixture doesn't shadow its own light.** A light placed inside a lamp shade, lantern or brazier bowl is blocked by that fixture when the fixture casts shadows: turn `castShadow` off on the fixture's meshes, and put the light just outside the shade's opening.
- **Ambient stays low, but not black:** hemisphere or ambient light between about 0.15 and 0.3 × the key's `E`. More flattens the form; less turns the room around the subject into a black void, which fails the stage.
- **Everything resting on something has a contact shadow:** from the shadow map (shadow camera tight around the focal area), or a blob shadow from the cookbook under small props.
- The check measures the focal subject's brightness against the lit scene around it in the hero still (background and sky left out), and warns (`light`) when it's darker. Aim for 1.5× or more: just passing doesn't make it read as lit.

## 5. Camera: framing, views and path

- `views.hero` is the still. Put the camera at its position, aim at its target, and set its `fov`.
- **Frame portrait separately.** When the canvas is taller than wide, use `views.heroPortrait` (closer, a wider `fov`, re-aimed), or fit the camera to the subject:

  ```js
  // Keep the view's direction; move along it until the focal subject's bounding sphere
  // spans `share` of the frame's smaller dimension.
  function fitView(view, focal, share = 0.45) {
    const sphere = new THREE.Box3().setFromObject(focal).getBoundingSphere(new THREE.Sphere());
    const dir = new THREE.Vector3(...view.position).sub(new THREE.Vector3(...view.target)).normalize();
    const half = Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2) * Math.min(1, camera.aspect);
    camera.position.copy(sphere.center).addScaledVector(dir, sphere.radius / (half * share));
    camera.lookAt(new THREE.Vector3(...view.target).lerp(sphere.center, 0.5));
  }
  function heroView() { return camera.aspect < 1 && spec.views.heroPortrait ? spec.views.heroPortrait : spec.views.hero; }
  ```

- **Show flat things at three-quarters.** A sign, gantry, screen, painting or doorway faces the camera 30–55° off its face, never edge-on and rarely dead-on.
- **Fill the frame with the subject:** the focal subject should span roughly a third to two-thirds of the still's width or height, at both aspects (the `fitView` share of 0.4–0.6). Crop the scene, not the subject.
- The check measures the hero still at desktop and mobile with your camera: how much of the frame the focal subject fills, whether it's cut off, and whether a flat focal object is edge-on. Fix every `framing` warning before asking for a critique.
- When the scene moves, pose the camera from **time** along `path`, never per frame, so video export is frame-exact:

  ```js
  const ease = (x) => x * x * (3 - 2 * x);
  function poseCamera(seconds) {
    const p = spec.path;
    if (!window.odScene.rotate || !p?.length) return setView(heroView());
    const t = Math.min(seconds % spec.duration, p[p.length - 1].t);
    let i = 0;
    while (i < p.length - 2 && t > p[i + 1].t) i++;
    const a = p[i], b = p[i + 1] ?? a, k = b.t > a.t ? ease((t - a.t) / (b.t - a.t)) : 0;
    camera.position.lerpVectors(new THREE.Vector3(...a.position), new THREE.Vector3(...b.position), k);
    camera.lookAt(new THREE.Vector3(...a.target).lerp(new THREE.Vector3(...b.target), k));
  }
  ```

- Keep moves slow and simple: one dolly or arc of 8–12 seconds, the camera never passing through geometry, the focal point in frame the whole time.

## 6. The ready contract (required)

```js
const start = performance.now();
window.odScene = { rotate: true, tier: 'finished', duration: spec.duration, ready: undefined, scene, camera, renderer, controls, focus: undefined };
window.odScene.ready = (async () => {
  await loadEverything();               // HDRI, textures, models
  window.odScene.focus = objects[spec.focal]; // the Object3D named by `focal`
  poseCamera(0);
  renderer.render(scene, camera);       // a direct render, not inside requestAnimationFrame
})();
renderer.setAnimationLoop((now) => { poseCamera((now - start) / 1000); renderer.render(scene, camera); });
```

- `ready` resolves after every asset has loaded and one frame is drawn with a direct `render()`. Motion export runs on a virtual clock, so a `ready` that waits for an animation frame never resolves there.
- `rotate = false` (set by still exports) holds the camera at `views.hero`.
- `duration` is the path length in seconds. Video exports use it when no duration is given; leave it out for a still-only scene.
- `scene`, `camera` and `renderer` let the check render its review views; add `controls` when there are orbit controls.
- `focus` is the Object3D named by `focal`. The check measures the hero still's framing and light on it, and aims the close-up review view at it.
- Optional: `subject` (the group to frame in review views), `views` (named `{ position, target }` overrides for the review).

## 7. Budgets (software rendering)

Checks and exports render WebGL in software, so keep the whole scene within about **300,000 triangles, 400 draw calls and 64 textures** (`webgl-budget` warns above that):

- Instance anything repeated more than ten times (`InstancedMesh`): stones, plants, posts, tiles.
- Use 1k textures and share materials across meshes that play the same part.
- Use at most one shadow-casting light, with a 2048 shadow map and a tight shadow camera around the scene.
- Use at most two post-processing passes.
- Check a model's polycount (the asset tool lists it) before using or cloning it. Poly Haven counts polygons, so a model can render up to twice that many triangles. A 70k-polygon plant is about 140k triangles; two of them blow the budget.

## 8. Cookbook

Adapted from majidmanzarpour/threejs-game-skills (MIT) and checked against three r160. In r160, set `envMapIntensity` per material; `scene.environmentIntensity` arrived later.

- **Glass.** Real glass (`transmission: 1`) renders unreliably in software WebGL and costs an extra scene render per frame, so fake it:

  ```js
  new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.03, transparent: true, opacity: 0.14,
    clearcoat: 1, clearcoatRoughness: 0.03, envMapIntensity: 1.6, depthWrite: false })
  ```

  With an HDRI it picks up real highlights. Add the rim below for a visible edge.
- **Fresnel rim** (a glass edge, a glow around a hero object):

  ```js
  mat.onBeforeCompile = (shader) => {
    shader.uniforms.uRim = { value: new THREE.Color(0xffffff) };
    shader.fragmentShader = 'uniform vec3 uRim;\n' + shader.fragmentShader.replace('#include <emissivemap_fragment>',
      '#include <emissivemap_fragment>\n float fres = pow(1.0 - saturate(dot(normalize(vNormal), normalize(vViewPosition))), 3.0);\n totalEmissiveRadiance += uRim * fres * 0.6;');
  };
  mat.customProgramCacheKey = () => 'od-rim';
  ```

- **Gradient sky dome** (a stylized sky without an HDRI): a `SphereGeometry(500, 32, 16)` with a `BackSide` `ShaderMaterial` that mixes a horizon and a top color by `normalize(position).y`, plus a sun disc from `pow(dot(dir, sunDir), 800.0)`. Mark it `userData.odStage = true` and `frustumCulled = false`. A raw `ShaderMaterial` skips tone mapping, so author its colors a little brighter.
- **Contact shadow** (small props that don't need the shadow map): a flat plane under the object with a radial-gradient `CanvasTexture`, `transparent: true`, `depthWrite: false`, a few millimeters above the ground.
- **Post chain** (only when the scene has authored glowing parts): `EffectComposer` → `RenderPass` → `UnrealBloomPass(size, 0.4, 0.3, 0.85)` → `OutputPass`, last, from `three/addons/postprocessing/…`. Render with `composer.render()`. Bloom only sells glow that's already there; if a shape only reads because it glows, the geometry is missing.
- **Materials by role:** stone and plaster at roughness 0.8–0.95; varnished wood 0.4–0.6 with a little clearcoat; brushed metal at metalness 1 and roughness 0.3–0.45; brass metalness 1, roughness 0.25, warm color. Separate surfaces by roughness and value, not hue alone.

## 9. Register, check, critique, export

1. `register_open_design_artifact` with kind `html` and this skill as the source.
2. `check_open_design_artifact`. Fix every error, every `broken-asset` (a wrong asset URL or a missing URL map), `webgl` warnings, `webgl-budget` warnings, and every `framing` and `light` warning (sections 4 and 5). The second image is the review sheet (overview, close-up, low angle, wireframe).
3. **Critique (required).** A clean check only means the page renders. Get a critique of the review sheet and the desktop and mobile screenshots against the brief from someone who didn't build it: a subagent with the Agent tool in Claude Code, `runSubagent` in VS Code, otherwise a separate critic pass that judges only the images and the brief. The critic scores each category 0–3:
   - form: true proportions, recognizable shapes;
   - materials: each surface reads as its real material;
   - light: intentional key, fill and contact shadow, with the light leading to the focal point;
   - composition: a clear focal point and depth, judged on the desktop and mobile shots;
   - stage: a sky and ground that support the scene;
   - fidelity: everything in `explicit` is present and recognizable;
   - technical: a clean check and within budget.

   **Automatic failures:**
   - something in `explicit` is missing or unrecognizable;
   - placeholder primitives in a finished scene;
   - fog, darkness or glow standing in for missing geometry;
   - objects floating or passing through each other (see the low and wireframe views);
   - an empty or unbalanced frame;
   - a check error.

   The critic lists at least three flaws, each with the view, where, and a fix. Fix them, check again and get a new critique until every category is at least 2 with no automatic failure, for at most three rounds. Then tell the user the scores and anything left.
4. **Export:**
   - **Still:** `export_open_design_artifact` with `format: "png"`; it shows `views.hero`.
   - **Flythrough:** `format: "mp4"` (or `"webm"`, or `"gif"` for a short loop). With `odScene.duration` set, no `duration` is needed.
   - Viewers need a connection for three.js and CDN assets, including for `standalone` exports, unless you made offline copies. `export_open_design_artifact` with `format: "standalone"` and `embedAssets: true` embeds every asset in the spec's `assets` (and each file a glTF includes) in the file; publishing as a Claude artifact does it automatically. Keep `assets` complete, with each asset's own URL (a texture's folder URL is fine), or that file stays remote.
