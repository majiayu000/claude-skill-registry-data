---
name: immersive-interactive-architect
description: >
  Specialized architect for building augmented reality, 3D, and immersive shopping experiences — across ANY output format (React JSX, standalone HTML/CSS/JS, WordPress/WooCommerce PHP, Python backends, or any other language). Use this skill whenever the user mentions: 3D product viewers, virtual try-on, AR fitting rooms, immersive brand showrooms, 3D collection environments, interactive drop pages, Three.js, React Three Fiber, A-Frame, model-viewer, WebXR, GSAP cinematic scroll, Lottie animations, spatial UI, parallax 3D scenes, or any request to make shopping feel like an experience rather than a webpage. Always use this skill even if the request seems simple — immersive experiences require specialized architecture that generic frontend patterns cannot match. This skill extends frontend-design with deep 3D and AR expertise; load frontend-design alongside it for complete visual design guidance.
---

# Immersive Interactive Architect

This skill governs the design and implementation of **AR, 3D, and immersive commerce experiences** — spatial interfaces where products live in three-dimensional space, motion tells the story, and every interaction deepens the emotional connection between brand and customer.

Before coding, always read the `frontend-design` SKILL.md for visual design principles. This skill handles the **spatial architecture layer** on top of it.

---

## Immersive Design Philosophy

Fashion is emotional. Immersive experiences must feel like entering a world, not browsing a store. Every build answers:

1. **The World**: What is the spatial metaphor? (underground vault, rose garden at midnight, elevated rooftop, fractured mirror dimension)
2. **The Journey**: How does the customer move through it? (scroll-driven, click-to-explore, gesture-controlled, camera-tracked)
3. **The Reveal**: When does the product become the hero, and how is it presented?
4. **The Emotion**: What should the visitor *feel* 10 seconds in — awe, mystery, hunger, belonging?
5. **The Exit**: What action do they take? (add to cart, join waitlist, share, save)

**CRITICAL PRINCIPLE**: Never build a 3D experience that is slower, harder, or less emotional than a good 2D page. Immersive = purposeful. Every Three.js mesh, every GSAP timeline, every WebGL shader must earn its render cost.

---

## Technology Stack — Decision Matrix

Select based on the experience type and output target:

| Experience | Primary Tech | Supporting |
|---|---|---|
| 3D Product Viewer (spin/zoom/inspect) | `model-viewer` or Three.js | GSAP for entrance animations |
| Brand Showroom / 3D Environment | Three.js or React Three Fiber | GSAP ScrollTrigger, custom shaders |
| Collection Drop / Launch Page | GSAP + Lottie + CSS 3D | Three.js particle systems (optional) |
| Virtual Try-On / AR Overlay | WebXR + `model-viewer` AR mode | MediaPipe (body/face tracking) |
| Cinematic Scroll Experience | GSAP ScrollTrigger + CSS Transforms | Three.js for accent effects |
| WordPress/WooCommerce Integration | Standalone HTML embed + PHP wrapper | REST API for product data |

### Library CDN References (always use exact versions for stability)

Three.js r169 requires ESM import maps — the legacy UMD `three.min.js` bundle is no longer the recommended path. Use the module build with an importmap:

```html
<!-- Import map — place before any <script type="module"> -->
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/"
  }
}
</script>

<!-- Then in your module script: -->
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader }    from 'three/addons/loaders/GLTFLoader.js';
// CapsuleGeometry, WebGPURenderer — all available in r169
const capsule = new THREE.CapsuleGeometry(0.5, 1, 4, 8);
</script>
```

For WebGPU renderer (r169+):
```html
<script type="importmap">
{
  "imports": {
    "three":        "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.webgpu.js",
    "three/webgpu": "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.webgpu.js",
    "three/tsl":    "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.tsl.js",
    "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/"
  }
}
</script>
```

```
GSAP 3.12:        https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js
GSAP ScrollTrigger: https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js
A-Frame 1.4:      https://aframe.io/releases/1.4.0/aframe.min.js
model-viewer:     https://ajax.googleapis.com/ajax/libs/model-viewer/3.3.0/model-viewer.min.js
Lottie Web:       https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js
```

---

## Output Format Patterns

### React / JSX (Claude.ai Artifacts)
- Use `import * as THREE from 'three'` (r169 — full ESM, all modern geometry available)
- Use `useEffect` + `useRef` for Three.js canvas lifecycle
- `THREE.CapsuleGeometry` is available natively — `new THREE.CapsuleGeometry(radius, length, capSegments, radialSegments)`
- GSAP via CDN script tag injected dynamically, or use CSS animations
- State management: `useState`/`useReducer` for experience phases (loading → explore → selected → cart)

### Standalone HTML/CSS/JS
- Single-file unless complexity demands otherwise
- All CDN libs loaded in `<head>` with `defer`
- Canvas element as full-viewport layer, UI elements as absolute-positioned HTML overlay
- Use CSS custom properties for brand theming
- Mobile-first: touch events alongside mouse events always

### WordPress / WooCommerce
- Deliver as a **self-contained shortcode embed** — PHP wrapper + enqueued scripts
- Use WooCommerce REST API (`/wp-json/wc/v3/products`) for live product data
- Inject product data as `window.SKYYROSE_PRODUCT_DATA = <?php echo json_encode($product_data); ?>`
- NEVER block the WordPress render thread — all 3D init must be `async`/deferred
- Provide both: (a) the shortcode PHP snippet, (b) the full HTML/JS embed file

**For the SkyyRose flagship theme specifically, the CDN/importmap pattern above does NOT apply.** That theme's real loading contract — three.js from jsdelivr via `/+esm` with NO importmap (a late importmap is rejected once the page has run a module script), self-hosted Draco decoder only, `window.THREE` gated behind a `three-ready` event — is documented and load-bearing in `.claude/skills/skyyrose-wp-platform/reference/threejs-immersive.md`. Read that file before writing any three.js code targeting this theme; it overrides this section. The `wp-immersive` agent owns the four `template-immersive-*.php` pages (Black Rose, Love Hurts, Signature, Kids Capsule) — route work there rather than duplicating scene logic here.

### Any Other Language / Stack
- Identify the runtime, then output the canonical pattern for that environment
- Python (Flask/Django): Jinja2 templates + static JS bundles
- Vue/Svelte/Next.js: Component-based with the same Three.js lifecycle patterns
- Always document environment assumptions at the top of the file

---

## Experience Type: 3D Product Viewer

**Goal**: Customer inspects the product from every angle before buying. Eliminates return anxiety. Builds confidence.

**Architecture**:
```
Canvas (Three.js WebGLRenderer)
├── Scene
│   ├── AmbientLight + DirectionalLight (3-point studio setup)
│   ├── ProductMesh (GLTF/OBJ/procedural geometry)
│   ├── EnvironmentMap (HDR or solid gradient)
│   └── ReflectionPlane (optional — adds luxury feel)
├── Camera (PerspectiveCamera, FOV 35-45 for product shots)
├── Controls (OrbitControls or custom drag handler)
└── UI Overlay (HTML)
    ├── Hotspot labels (position projected from 3D to 2D)
    ├── Color/variant switcher
    └── Add to Cart CTA
```

**Lighting Setup for Fashion/Apparel**:
```javascript
// Studio 3-point lighting
const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
keyLight.position.set(5, 8, 5);

const fillLight = new THREE.DirectionalLight(0xB76E79, 0.4); // rose gold fill
fillLight.position.set(-5, 3, 2);

const rimLight = new THREE.DirectionalLight(0xffffff, 0.8);
rimLight.position.set(0, -3, -5); // backlight for fabric edge glow

const ambient = new THREE.AmbientLight(0x111111, 0.6);
```

**Mobile Handling**: Always implement touch-drag controls with `touchstart`/`touchmove` alongside mouse. Pinch-to-zoom via `touchmove` with two-finger distance delta.

---

## Experience Type: Brand Showroom / 3D Environment

**Goal**: Customer enters a spatial world that IS the brand. Products are discovered, not listed.

**Architecture Pattern**:
```
Scene Graph
├── Environment (skybox or procedural background)
│   ├── Fog (THREE.FogExp2 for depth)
│   └── Background particles / atmospheric effects
├── Collection Zones (spatial groupings)
│   ├── Zone: BLACK ROSE → dark marble surfaces, moody spotlights
│   ├── Zone: LOVE HURTS → deep reds, cracked texture, emotional lighting
│   └── Zone: SIGNATURE → clean planes, neutral tones, editorial
├── Product Objects (instanced meshes for performance)
├── Navigation (raycasting on click/tap, camera lerp to target)
└── UI Layer
    ├── Minimap (optional for large environments)
    └── Product detail panel (slides in on selection)
```

**Camera Movement**:
```javascript
// Smooth cinematic camera lerp — NEVER teleport, always glide
function lerpCamera(targetPosition, targetLookAt, duration = 1.2) {
  gsap.to(camera.position, {
    x: targetPosition.x,
    y: targetPosition.y,
    z: targetPosition.z,
    duration,
    ease: "power2.inOut",
    onUpdate: () => camera.lookAt(currentLookAt)
  });
}
```

**Performance Budget**:
- Max 50k triangles total scene for mobile
- Max 150k triangles for desktop
- Use `THREE.InstancedMesh` for repeated objects (particles, floor tiles)
- Texture atlasing: combine small textures into one 2048×2048 atlas
- Disable shadows on mobile: `renderer.shadowMap.enabled = isMobile ? false : true`

---

## Experience Type: Virtual Try-On / AR Overlay

**Goal**: Customer sees the product on themselves or in their environment using the device camera.

**Implementation Tiers** (choose based on scope):

### Tier 1: model-viewer AR Mode (simplest, iOS + Android)
```html
<model-viewer
  src="product.glb"
  ar
  ar-modes="webxr scene-viewer quick-look"
  camera-controls
  auto-rotate
  shadow-intensity="1"
  environment-image="neutral"
  style="width:100%; height:500px;">
  <button slot="ar-button" class="ar-cta">View in Your Space</button>
</model-viewer>
```

### Tier 2: WebXR Hit-Test (full AR placement)
- Requires HTTPS + WebXR-capable browser (Chrome Android, Safari 16+)
- Use `navigator.xr.requestSession('immersive-ar', { requiredFeatures: ['hit-test'] })`
- Render overlay anchored to real-world surface via hit-test matrix
- Always include a graceful fallback to Tier 1 or 3D viewer

### Tier 3: MediaPipe Body Segmentation (garment overlay)
- Advanced: use `@mediapipe/selfie_segmentation` to isolate body
- Overlay product texture on segmented person silhouette
- GPU-accelerated via WebGL — frame rate critical, target 24fps minimum
- Provide detailed instructions: see `references/ar-mediapipe.md`

**AR Trigger UX**: Always show a clear "View in AR" CTA that feature-detects before launching:
```javascript
async function checkARSupport() {
  if (!navigator.xr) return 'unsupported';
  const supported = await navigator.xr.isSessionSupported('immersive-ar');
  return supported ? 'webxr' : 'model-viewer-fallback';
}
```

---

## Experience Type: Cinematic Collection Drop / Launch Page

**Goal**: A product drop feels like a movie premiere. Scroll = timeline. Every frame is intentional.

**GSAP ScrollTrigger Architecture**:
```javascript
// Phase 1: Hero — product emerges from darkness
gsap.timeline({
  scrollTrigger: { trigger: "#hero", start: "top top", end: "+=100%", scrub: 1.5 }
})
.from(".product-hero", { scale: 0.6, opacity: 0, duration: 1 })
.from(".collection-name", { y: 120, opacity: 0, duration: 0.8 }, "-=0.4")
.from(".hero-particles", { opacity: 0, duration: 1.2 }, "-=0.6");

// Phase 2: Collection reveal — products stagger in
gsap.timeline({
  scrollTrigger: { trigger: "#collection", start: "top 80%", toggleActions: "play none none reverse" }
})
.from(".product-card", {
  y: 80, opacity: 0, stagger: 0.15, ease: "power3.out", duration: 0.9
});

// Phase 3: Story section — text reveals word by word
SplitText and staggered character animations
```

**Lottie Integration**:
```javascript
const anim = lottie.loadAnimation({
  container: document.getElementById('lottie-container'),
  renderer: 'svg',
  loop: false,
  autoplay: false,
  path: 'animation.json'
});
// Sync Lottie frame to scroll progress
ScrollTrigger.create({
  trigger: "#lottie-section",
  start: "top center",
  end: "bottom center",
  onUpdate: (self) => {
    anim.goToAndStop(self.progress * anim.totalFrames, true);
  }
});
```

---

## SkyyRose Brand Integration

When building for SkyyRose, always:

**Load**: `skyyrose-market:skyyrose-brand-dna` SKILL.md alongside this skill for full brand context.

**Pre-screened patterns**: `docs/design/visual-pattern-shortlist.md` has 176 animation/visual patterns already cross-checked against this brand system, including a dedicated set tagged "Immersive Worlds scene work." Check there before improvising a pattern from scratch.

**CDN loading**: this is theme-dependent, not a blanket zero-CDN policy — the flagship WordPress theme actually loads three.js from jsdelivr (see the WordPress/WooCommerce section above and `threejs-immersive.md`); only the Draco decoder is self-hosted there. For other output targets, self-host under `SKYYROSE_ASSETS_URI` where the platform supports it. Don't assume either policy — check the target.

**Spatial Brand Palette** (canonical tokens — locked, do not invent alternates):
```css
:root {
  --sr-void: #0A0A0A;          /* scene background / Dark */
  --sr-charcoal: #1C1C1C;      /* surfaces */
  --sr-smoke: #2D2D2D;         /* secondary surfaces */
  --sr-rose-gold: #B76E79;     /* accent lights, UI highlights — global + Kids Capsule */
  --sr-silver: #C0C0C0;        /* BLACK ROSE collection accent */
  --sr-crimson: #DC143C;       /* LOVE HURTS collection energy */
  --sr-gold: #D4AF37;          /* SIGNATURE collection accent */
  --sr-white: #F5F5F0;         /* typography, clean surfaces */
}
```

**Per-Collection 3D Environments**:
| Collection | Environment | Light Color | Fog | Particle Effect |
|---|---|---|---|---|
| BLACK ROSE | Dark marble vault | #B76E79 rose gold key, #C0C0C0 silver rim | Dense black fog | Gold dust particles |
| LOVE HURTS | Fractured red glass space | #DC143C crimson fill, white backlight | Red mist | Ember/ash particles |
| SIGNATURE | Editorial white studio | #D4AF37 gold key, neutral 3-point | None | None |
| KIDS CAPSULE | Playful, launch-mode | #B76E79 rose gold (shared global accent) | None | Physics-based bouncing elements, not ambient particles |

**Product Interaction Sound Design** (optional but impactful):
- Use Web Audio API for subtle UI sounds (no autoplay — always user-triggered)
- Soft chime on product selection, tactile click on variant switch

---

## Performance Standards

Every immersive experience MUST meet these before delivery:

| Metric | Target | Hard Limit |
|---|---|---|
| Initial load (3G) | < 4s to first render | < 8s |
| FPS (mobile) | 30fps stable | Never drop below 20fps |
| FPS (desktop) | 60fps stable | Never drop below 45fps |
| JS bundle (gzipped) | < 400KB | < 800KB |
| Texture memory | < 50MB | < 100MB |
| Lighthouse Performance | > 70 | > 55 |

**Optimization Checklist**:
- [ ] Progressive loading: show 2D placeholder while 3D initializes
- [ ] `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` — cap DPR
- [ ] Frustum culling enabled (default in Three.js, verify not disabled)
- [ ] `geometry.dispose()` + `material.dispose()` on unmount (React) or scene clear
- [ ] Texture compression: use `.basis` or `.ktx2` for production GLTFs
- [ ] Use `requestAnimationFrame` loop only when canvas is visible (IntersectionObserver pause)

---

## Accessibility & Fallback Architecture

Immersive experiences must be inclusive:

```
Experience Tiers:
1. Full 3D/AR       → WebGL + WebXR capable browsers
2. CSS 3D Fallback  → Modern browsers without WebGL (rare but real)
3. Static Fallback  → Accessible, screen-reader-friendly product page
```

Always implement:
- `<noscript>` block with product images and description
- `aria-label` on canvas: `<canvas aria-label="Interactive 3D product viewer. Use arrow keys to rotate.">`
- Keyboard controls for 3D rotation (arrow keys)
- Prefers-reduced-motion media query: disable all animations, show static scene

```javascript
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (prefersReduced) {
  // Skip GSAP timelines, show static scene
  gsap.globalTimeline.pause();
}
```

---

## File Delivery Format

When delivering an immersive experience, always provide:

1. **The primary file** — fully functional, self-contained when possible
2. **Integration notes** — clear comments for WordPress shortcode, npm install, etc.
3. **Asset checklist** — what GLB/GLTF/texture files the developer needs to supply
4. **Demo data** — if no real assets provided, use procedural geometry + placeholder textures so the experience is fully runnable

For WordPress delivery, output two code blocks:
- `experience.html` — the full standalone experience
- `functions.php snippet` — enqueue + shortcode registration

---

## Reference Files

Load these when you need deeper guidance on specific topics:

- `references/three-js-patterns.md` — Three.js boilerplate, geometry patterns, shader snippets
- `references/gsap-scroll-patterns.md` — ScrollTrigger timelines, SplitText, Lottie sync
- `references/ar-mediapipe.md` — MediaPipe body tracking integration guide
- `references/woocommerce-3d-embed.md` — WordPress/WooCommerce integration patterns

---

## Quick-Start Templates

For common requests, scaffold from these mental templates:

**"Build a 3D product viewer"** → Three.js canvas + OrbitControls + studio lighting + HTML overlay CTA

**"Create an immersive collection page"** → GSAP ScrollTrigger multi-phase timeline + Three.js particle background + product cards with 3D entrance animations

**"AR try-on for mobile"** → `model-viewer` with `ar` attribute + WebXR hit-test upgrade path + graceful feature detection

**"Brand showroom / 3D store"** → Three.js environment + raycasting navigation + collection zone spatial layout + camera lerp transitions

**"Drop launch page"** → Cinematic GSAP countdown + particle burst on reveal + product hero with Three.js depth-of-field effect

Always begin with: **What emotion should hit the visitor in the first 3 seconds?** Then build backward from that feeling.
