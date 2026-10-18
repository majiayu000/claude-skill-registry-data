---
name: using-web3d
description: Router for the web3d family — vendored skills for 3D, 2D canvas, motion and scroll on the web (Three.js, React Three Fiber, Babylon.js, PlayCanvas, A-Frame, PixiJS, Motion, anime.js, React Spring, Lottie, Rive, GSAP ScrollTrigger, Locomotive, AOS, Barba, Spline). Use when a page needs a 3D scene, a canvas, animation or scroll-driven effects; it picks the one library skill for the job and the order to combine them. Triggers include "3D", "WebGL", "three.js", "R3F", "animation", "scroll effect", "parallax", "page transition", "Lottie", "Rive", "WebXR".
---

# Using Web3D

**A router, not a rulebook.** Pick the row, load that skill, follow it. Skills live verbatim in `skills/vendor/<name>/`, each with an `UPSTREAM.md`.

## 1. Choose the stack first

**Unsure which library, or combining several** → **`web3d-integration-patterns`** (how Three.js, R3F, GSAP, Motion and React Spring fit together). For the page's overall look, go to **`using-anti-slop`**; `modern-web-design` is a trends-and-patterns reference.

## 2. Pick by task

| You need… | Load |
|---|---|
| **A full 3D scene, vanilla JS** | **`threejs-webgl`**; animation clips, skeletons, morphs → **`threejs-animation`** |
| **A 3D scene in React** | **`react-three-fiber`**; performance and loading rules → **`r3f-best-practices`** |
| **A game-like or physics-heavy 3D app** | **`babylonjs-engine`** · **`playcanvas-engine`** |
| **VR / AR (WebXR)** | **`aframe-webxr`** |
| **Decorative pseudo-3D** — tilt, animated backgrounds, Zdog | **`lightweight-3d-effects`** (reach for this before a full engine) |
| **A 3D scene designed without code** | **`spline-interactive`** |
| **Shrinking a 3D model for the web** — GLB size, draw calls | **`threejs-agents-model-optimizer`** |
| **Fast 2D canvas** — sprites, particles, games | **`pixijs-2d`** |
| **UI animation in React** | **`motion-framer`**; physics feel → **`react-spring-physics`**; ready components (Magic UI, React Bits) → **`animated-component-libraries`** |
| **Timeline animation without a framework** | **`animejs`** |
| **Designer-made animation files** | **`lottie-animations`** (After Effects) · **`rive-interactive`** (state machines) |
| **Scroll-linked animation, pinning, scrub** | **`gsap-scrolltrigger`** |
| **Smooth scrolling** | **`locomotive-scroll`** |
| **Simple fade/slide on scroll** | **`scroll-reveal-libraries`** (AOS) |
| **Page transitions between routes** | **`barba-js`** |

## 3. Rules

- **Lightest tool that does the job.** CSS or `lightweight-3d-effects` before a WebGL engine; AOS before GSAP when a fade is all you need.
- **One animation owner per element.** GSAP and Motion both driving the same transform fight; `web3d-integration-patterns` says how to split them.
- **Done means seen.** Load the page in a real browser (`playwright-cli`): no console errors, the canvas renders non-blank, frame rate holds. Then `design-ship-gate`.
- **Do not edit `skills/vendor/`.** Update by re-copying from upstream and updating `UPSTREAM.md`.
