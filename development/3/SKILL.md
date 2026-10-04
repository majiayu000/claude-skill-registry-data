---
name: webgl-renderer-baseline
description: Use this skill whenever initialising or configuring the WebGL renderer, post-processing stack, HDRI environment, shadow maps, tone mapping, context loss handling, tab visibility management, or any code that touches the Three.js renderer setup in the Myelin simulator. This is the authoritative renderer configuration contract. Do not guess renderer settings — load this skill first.
---

This skill defines the complete WebGL 2 renderer configuration for the Myelin simulator. Every renderer initialisation, post-processing addition, and environment setup must follow these specifications exactly. Deviating from these settings produces inconsistent visual output across devices and browser sessions.

---

## Renderer Initialisation

```javascript
import * as THREE from 'three';

function createRenderer(canvas) {
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    powerPreference: 'high-performance',
    alpha: false,
    stencil: false,       // not required for simulator scenes
    depth: true,
    logarithmicDepthBuffer: false  // enable only if z-fighting occurs at large scales
  });

  // Linear workflow — mandatory
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;

  // Shadows
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.autoUpdate = true;

  // Physical lighting model
  renderer.useLegacyLights = false;

  // Device pixel ratio — cap at 2 to limit GPU load on high-DPI displays
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // Initial size
  const { width, height } = canvas.getBoundingClientRect();
  renderer.setSize(width, height, false); // false = do not set canvas style

  return renderer;
}
```

Do not use `WebGLRenderer` without the `powerPreference: 'high-performance'` hint. Do not set `outputColorSpace` to `THREE.LinearSRGBColorSpace` — output must be sRGB.

---

## Shadow Map Configuration by Quality Tier

Shadow map size scales with resolution tier (see `lod-performance-budget` skill for tier definitions).

```javascript
function configureShadows(renderer, qualityTier) {
  const shadowMapSizes = {
    MINIMUM: 1024,
    HD:      2048,
    HD_PLUS: 2048,
    UHD:     4096
  };

  const size = shadowMapSizes[qualityTier] || 1024;

  // Apply to all shadow-casting lights in the scene
  scene.traverse(obj => {
    if (obj.isDirectionalLight || obj.isSpotLight) {
      obj.shadow.mapSize.width  = size;
      obj.shadow.mapSize.height = size;
      obj.shadow.bias = -0.0005;           // tune to avoid shadow acne
      obj.shadow.normalBias = 0.02;        // tune to avoid peter-panning
      obj.shadow.camera.near = 0.1;
      obj.shadow.camera.far  = 50;
    }
  });
}
```

Shadow bias and normalBias must be set on every shadow-casting light. Un-tuned bias produces floating shadow artefacts on the industrial scene surfaces.

---

## HDRI Environment Loading

HDRI must be loaded with a fallback chain. Do not hardcode a single resolution.

```javascript
import { RGBELoader } from 'three/examples/jsm/loaders/RGBELoader.js';
import { PMREMGenerator } from 'three';

async function loadEnvironment(renderer, scene, qualityTier) {
  const pmremGenerator = new PMREMGenerator(renderer);
  pmremGenerator.compileEquirectangularShader();

  const hdriResolutions = {
    UHD:     '/assets/hdri/industrial_workshop_8k.hdr',
    HD_PLUS: '/assets/hdri/industrial_workshop_4k.hdr',
    HD:      '/assets/hdri/industrial_workshop_2k.hdr',
    MINIMUM: '/assets/hdri/industrial_workshop_1k.hdr'
  };

  const hdriPath = hdriResolutions[qualityTier] || hdriResolutions.MINIMUM;

  return new Promise((resolve, reject) => {
    const loader = new RGBELoader();
    loader.load(
      hdriPath,
      (texture) => {
        const envMap = pmremGenerator.fromEquirectangular(texture).texture;
        scene.environment = envMap;
        scene.background  = envMap;
        texture.dispose();
        pmremGenerator.dispose();
        resolve(envMap);
      },
      undefined,
      () => {
        // Fallback to 1k if preferred resolution fails
        if (hdriPath !== hdriResolutions.MINIMUM) {
          loadEnvironment(renderer, scene, 'MINIMUM').then(resolve).catch(reject);
        } else {
          reject(new Error('HDRI_LOAD_FAILED: all resolutions exhausted'));
        }
      }
    );
  });
}
```

Scene environment and background must both be set from the same PMREMGenerator output. Do not set `scene.background` to a flat color in production scenes — use the HDRI or a degraded fallback color only when all HDRI loads fail.

---

## Post-Processing Stack

Use EffectComposer with the following pass order. All passes are optional-by-quality-tier except RenderPass (always required) and OutputPass (always required).

```javascript
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass }     from 'three/examples/jsm/postprocessing/RenderPass.js';
import { SMAAPass }       from 'three/examples/jsm/postprocessing/SMAAPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { OutputPass }     from 'three/examples/jsm/postprocessing/OutputPass.js';

function createPostProcessing(renderer, scene, camera, qualityTier) {
  const composer = new EffectComposer(renderer);

  // 1. Render pass — always on
  composer.addPass(new RenderPass(scene, camera));

  // 2. Anti-aliasing — SMAA on HD+, skip on MINIMUM (too expensive)
  if (qualityTier !== 'MINIMUM') {
    const smaa = new SMAAPass(
      window.innerWidth  * renderer.getPixelRatio(),
      window.innerHeight * renderer.getPixelRatio()
    );
    composer.addPass(smaa);
  }

  // 3. Bloom — subtle arc flash / indicator glow only; threshold high to avoid over-bloom
  if (qualityTier === 'HD_PLUS' || qualityTier === 'UHD') {
    const bloom = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      0.15,   // strength  — kept very low; this is not a stylised game
      0.4,    // radius
      0.95    // threshold — only very bright elements bloom
    );
    composer.addPass(bloom);
  }

  // 4. Output pass — always last; handles final sRGB conversion
  composer.addPass(new OutputPass());

  return composer;
}
```

Do not add depth-of-field or chromatic aberration passes by default. These are available for close-up inspection camera modes only and must be toggled off during step interactions to preserve interaction legibility.

Film grain: apply as a subtle screen-space shader only on UHD tier, strength <= 0.03. It must not affect interaction feedback readability.

---

## Resize and Device Pixel Ratio Handling

The renderer must respond to viewport changes and device pixel ratio changes (e.g. user moves browser to a different monitor).

```javascript
function handleResize(renderer, camera, composer) {
  const width  = window.innerWidth;
  const height = window.innerHeight;
  const dpr    = Math.min(window.devicePixelRatio, 2);

  renderer.setPixelRatio(dpr);
  renderer.setSize(width, height, false);
  composer.setSize(width, height);

  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

window.addEventListener('resize', () => handleResize(renderer, camera, composer));
```

For ResizeObserver on the canvas element (preferred over `window.resize` for embedded contexts):

```javascript
const resizeObserver = new ResizeObserver(entries => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    renderer.setSize(width, height, false);
    composer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }
});
resizeObserver.observe(canvas);
```

---

## Graphics Context Loss Handling

WebGL context loss is recoverable. The renderer must handle it gracefully without requiring a page reload.

```javascript
canvas.addEventListener('webglcontextlost', (event) => {
  event.preventDefault(); // prevent browser default (which discards the context)
  console.warn('WebGL context lost — pausing render loop');
  stopRenderLoop();
  showContextLostOverlay(); // show user-facing message "Restarting display..."
});

canvas.addEventListener('webglcontextrestored', () => {
  console.info('WebGL context restored — reinitialising renderer');
  reinitialiseRenderer(); // reload textures, re-compile shaders, restart loop
  hideContextLostOverlay();
});
```

`reinitialiseRenderer` must re-run the full renderer initialisation sequence including HDRI reload, shadow config, and post-processing stack rebuild. The simulation session state (in JavaScript memory) must be preserved across a context loss/restore cycle — only the GPU resources are lost, not the step progress.

---

## Page Visibility API — Render Pause

When the tab is hidden, rendering must pause to free GPU and CPU resources.

```javascript
let animationFrameId = null;

function startRenderLoop() {
  function loop() {
    animationFrameId = requestAnimationFrame(loop);
    // Update physics
    physicsWorld.step(1 / 60, delta, 3);
    // Update controls
    controls.update();
    // Render
    composer.render();
    // Emit performance metric
    trackFramePerformance();
  }
  animationFrameId = requestAnimationFrame(loop);
}

function stopRenderLoop() {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
}

document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    stopRenderLoop();
  } else {
    startRenderLoop();
  }
});
```

The simulation session timer must also pause when the tab is hidden. Elapsed time for attempt scoring must only count active visibility time.

---

## Adaptive Quality Scaling

When frame pacing degrades, the renderer must drop quality tier to recover frame budget.

```javascript
const FRAME_BUDGET_MS    = 16.67; // 60 fps target
const DEGRADED_THRESHOLD = 22;    // ms — sustained above this triggers downgrade
const RECOVERY_THRESHOLD = 14;    // ms — sustained below this allows upgrade
const SAMPLE_WINDOW      = 60;    // frames to sample before acting

let frameSamples = [];

function trackFramePerformance() {
  const frameTime = performance.now() - lastFrameTime;
  lastFrameTime = performance.now();

  frameSamples.push(frameTime);
  if (frameSamples.length > SAMPLE_WINDOW) frameSamples.shift();

  const avg = frameSamples.reduce((a, b) => a + b, 0) / frameSamples.length;

  if (avg > DEGRADED_THRESHOLD && currentTier !== 'MINIMUM') {
    downgradeQualityTier();
  } else if (avg < RECOVERY_THRESHOLD && currentTier !== detectedCapabilityTier) {
    upgradeQualityTier();
  }
}
```

Quality downgrades must be applied without interrupting the simulation session. Shadow map size changes require a shadow map rebuild — do this between frames, not mid-frame.

---

## WebGPU Detection and Fallback

WebGPU is not required. Use only if detected and only as a progressive enhancement.

```javascript
async function selectRenderer(canvas) {
  if (navigator.gpu) {
    try {
      const adapter = await navigator.gpu.requestAdapter();
      if (adapter) {
        // WebGPU path — use THREE.WebGPURenderer when available
        // Falls through to WebGL 2 if WebGPURenderer is not yet stable
      }
    } catch {
      // WebGPU unavailable — fall through to WebGL 2
    }
  }
  // WebGL 2 baseline — always available
  return createRenderer(canvas);
}
```

The WebGL 2 path is the production baseline. WebGPU is opt-in and must not be required for any assessed interaction.

---

## What Not To Do

- Do not initialise the renderer without `powerPreference: 'high-performance'`
- Do not set `outputColorSpace` to `LinearSRGBColorSpace` — always use `SRGBColorSpace`
- Do not skip shadow bias and normalBias configuration on directional lights
- Do not set `renderer.setPixelRatio(window.devicePixelRatio)` without capping at 2
- Do not add bloom with strength > 0.15 in the standard simulation view
- Do not skip context loss handling — WebGL context loss is a recoverable error
- Do not continue the render loop when the tab is hidden
- Do not count hidden-tab time in simulation attempt elapsed time
- Do not apply depth-of-field during step interactions — it impairs interaction legibility
