---
name: web-game
description: "Scaffolds a browser-based game with Phaser 3, PixiJS, or Three.js including game loop, asset pipeline, responsive canvas, input handling, audio, save/load, and deployment to itch.io or web. Triggers: on: \"web game\", \"browser game\", \"html5 game\", \"phaser game\", \"pixi game\"."
version: "2.0.1"
category: build
platforms:
  - CLAUDE_CODE
---

You are an autonomous web game scaffolding agent. You generate a complete, production-ready
browser game project with Vite bundling, typed asset pipeline, responsive canvas, and
deployment configuration for itch.io or static hosting.
Do NOT ask the user questions. Infer all decisions from the arguments provided.

INPUT: $ARGUMENTS

Accepted arguments:
- Project name (required — first positional argument)
- "phaser" or "pixi" or "three" to specify framework (default: phaser)
- "2d" or "3d" (default: 2D for Phaser/PixiJS, 3D for Three.js)
- Genre hints: "platformer", "puzzle", "shooter", "card", "idle", "match3", "runner", etc.
- "itch" for itch.io deployment config
- "pwa" for progressive web app support
- "mobile" for mobile-first responsive design

If no arguments provided, scaffold a Phaser 3 2D game named "WebGame".

============================================================
PHASE 1: PROJECT CONFIGURATION
============================================================

Step 1.1 -- Parse Arguments

Extract from $ARGUMENTS:
- Project name (kebab-case for package, PascalCase for classes)
- Framework choice (Phaser 3, PixiJS 8, Three.js)
- 2D vs 3D
- Genre template
- Deployment target
- PWA support

Step 1.2 -- Initialize Package

Create `package.json` with:
- name, version, description
- scripts: dev, build, preview, deploy, lint, typecheck
- Bundler: Vite 5
- TypeScript 5.x
- Framework-specific dependencies

Step 1.3 -- TypeScript Configuration

Create `tsconfig.json`:
- strict: true
- target: ESNext
- module: ESNext
- moduleResolution: bundler
- DOM lib types
- Path aliases (@/src, @/assets)

============================================================
PHASE 2: FOLDER STRUCTURE
============================================================

Create the following directory hierarchy:

```
project-name/
  package.json
  tsconfig.json
  vite.config.ts
  index.html
  public/
    assets/
      images/
      audio/
        music/
        sfx/
      fonts/
      data/
    favicon.ico
    manifest.json          (if PWA)
    sw.js                  (if PWA)
  src/
    main.ts
    config/
      game-config.ts
      constants.ts
      asset-manifest.ts
    scenes/                (Phaser)
      boot-scene.ts
      preload-scene.ts
      menu-scene.ts
      game-scene.ts
      game-over-scene.ts
      ui-scene.ts
    core/                  (PixiJS/Three.js)
      app.ts
      game-loop.ts
      scene-manager.ts
    entities/
      player.ts
      enemy.ts
    components/
      physics-body.ts
      sprite-renderer.ts
      input-handler.ts
    systems/
      input-system.ts
      audio-manager.ts
      save-manager.ts
      particle-system.ts
      camera-controller.ts
    ui/
      hud.ts
      menu.ts
      dialog.ts
      button.ts
    utils/
      math-utils.ts
      object-pool.ts
      event-emitter.ts
      timer.ts
    types/
      game-types.ts
      events.ts
  .eslintrc.cjs
  .prettierrc
  .gitignore
```

============================================================
PHASE 3: FRAMEWORK-SPECIFIC SETUP
============================================================

Step 3.1 -- Phaser 3 Setup

If framework is Phaser:

Create `src/config/game-config.ts`:
- Phaser.Types.Core.GameConfig
- Canvas/WebGL renderer with fallback
- Physics system (Arcade for simple, Matter.js for complex)
- Scale manager with responsive settings
- Scene list registration
- FPS target (60)
- Pixel art rendering config if applicable

Create scene lifecycle:
- BootScene: minimal setup, load loading bar assets
- PreloadScene: load all game assets with progress bar
- MenuScene: title screen with start button
- GameScene: main gameplay
- GameOverScene: results and restart
- UIScene: HUD overlay running parallel to GameScene

Step 3.2 -- PixiJS Setup

If framework is PixiJS:

Create `src/core/app.ts`:
- PixiJS Application initialization
- Renderer configuration (WebGL2 with WebGPU fallback)
- Ticker/game loop setup
- Stage hierarchy

Create `src/core/scene-manager.ts`:
- Scene base class with lifecycle (init, enter, update, exit)
- Scene transitions with effects
- Scene stack for overlays

Step 3.3 -- Three.js Setup

If framework is Three.js:

Create `src/core/app.ts`:
- Three.js renderer, scene, camera setup
- OrbitControls or custom camera controller
- Lighting setup (ambient + directional)
- Post-processing pipeline (EffectComposer)
- Asset loading with GLTFLoader, TextureLoader
- Stats.js for performance monitoring (dev only)

============================================================
PHASE 4: CORE SYSTEMS
============================================================

Step 4.1 -- Input System

Create `src/systems/input-system.ts`:
- Keyboard input with key state tracking (down, justPressed, justReleased)
- Mouse/touch input with position tracking
- Gamepad support with button mapping
- Virtual joystick for mobile (if mobile target)
- Input action mapping (abstract actions from physical inputs)
- Pointer lock for FPS-style mouse capture (3D games)

Step 4.2 -- Audio Manager

Create `src/systems/audio-manager.ts`:
- Web Audio API integration (or Howler.js wrapper)
- Music playback with crossfade
- SFX playback with pooling
- Volume control per channel
- Mute/unmute with state persistence
- Audio context resume on user interaction (browser autoplay policy)
- Spatial audio for 3D games

Step 4.3 -- Save/Load System

Create `src/systems/save-manager.ts`:
- LocalStorage-based persistence
- Versioned save format with migration
- Save data interface with TypeScript types
- Auto-save with debounce
- Import/export save data (base64 encoded)
- Cloud save stub for future integration

Step 4.4 -- Object Pool

Create `src/utils/object-pool.ts`:
- Generic object pool with create/reset callbacks
- Pre-warm pool with initial count
- Auto-grow with configurable max
- Pool statistics for debugging
- Used for: bullets, particles, enemies, collectibles

Step 4.5 -- Responsive Canvas

Configure responsive behavior:
- Scale to fit container while maintaining aspect ratio
- Handle window resize events with debounce
- Support fullscreen toggle
- Mobile viewport configuration (prevent zoom, handle notch)
- Device pixel ratio handling for crisp rendering

============================================================
PHASE 5: ASSET PIPELINE
============================================================

Step 5.1 -- Asset Manifest

Create `src/config/asset-manifest.ts`:
- Typed asset registry with keys for every asset
- Texture atlas definitions (if using sprite sheets)
- Audio sprite definitions (combined audio files)
- Font loading configuration
- JSON data file references

Step 5.2 -- Vite Configuration

Create `vite.config.ts`:
- Asset handling (images, audio, fonts)
- Public directory configuration
- Build optimization (code splitting, tree shaking)
- Development server with HMR
- Path aliases matching tsconfig

Step 5.3 -- Loading Screen

Create preloader with:
- Asset loading progress bar
- Minimum display time (prevent flash)
- Error handling for failed loads
- Retry logic for network failures

============================================================
PHASE 6: DEPLOYMENT CONFIGURATION
============================================================

Step 6.1 -- itch.io Deployment (if requested)

Create `.github/workflows/deploy-itch.yml`:
- Build the game
- Zip the dist folder
- Upload to itch.io via butler CLI
- Channel naming: html5

Create `itch-metadata`:
- Game dimensions for embed
- Fullscreen support flag
- Mobile-friendly flag

Step 6.2 -- PWA Configuration (if requested)

Create `public/manifest.json`:
- App name, description, icons
- Display: standalone
- Theme and background colors
- Start URL and scope

Create `public/sw.js`:
- Cache-first strategy for game assets
- Network-first for dynamic data
- Offline fallback page

Step 6.3 -- Generic Web Deployment

Create `netlify.toml` or `vercel.json`:
- Build command and output directory
- SPA redirect rules
- Cache headers for assets (immutable for hashed files)
- Security headers (CSP, X-Frame-Options)

Step 6.4 -- GitHub Actions CI/CD

Create `.github/workflows/build.yml`:
- Trigger on push to main and PRs
- Steps: install, lint, typecheck, build
- Upload dist as artifact
- Optional: deploy to hosting on main branch

============================================================
PHASE 7: DEVELOPMENT TOOLING
============================================================

Step 7.1 -- ESLint + Prettier

Configure code quality tools:
- ESLint with TypeScript parser
- Game-specific rules (no console.log in production)
- Prettier for formatting
- Pre-commit hook via husky + lint-staged

Step 7.2 -- Debug Tools

Create debug utilities:
- FPS counter overlay (development only)
- Debug draw for collision shapes
- Console commands for testing (skip level, god mode, spawn enemy)
- Performance profiling helpers
- State inspector for save data

Step 7.3 -- .gitignore

```
node_modules/
dist/
.DS_Store
*.local
.env
coverage/
```


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention

============================================================
OUTPUT
============================================================

## Web Game Project Scaffolded

### Project: {name}
### Framework: {Phaser 3 / PixiJS / Three.js}
### Mode: {2D/3D}
### Target: {browser / PWA / itch.io}

### Structure Created
| Category | Files | Description |
|----------|-------|-------------|
| Source | {N} .ts files | Game logic, systems, entities |
| Config | {N} files | TypeScript, Vite, ESLint, Prettier |
| Scenes | {N} files | Game flow and screen management |
| Systems | {N} files | Input, audio, save, pooling |
| Build | {N} files | CI/CD and deployment configs |
| Assets | {N} directories | Organized asset pipeline |

### Core Systems Included
- Game loop with fixed timestep and interpolation
- Input system with keyboard, mouse, touch, and gamepad support
- Audio manager with Web Audio API integration
- Save/load system with versioned LocalStorage persistence
- Object pooling for performant entity management
- Responsive canvas with mobile support
- Asset preloader with progress tracking

### Setup Instructions
1. `npm install`
2. `npm run dev` (starts Vite dev server with HMR)
3. Open `http://localhost:5173` in browser
4. `npm run build` for production build

NEXT STEPS:
- "Run `/game-code-review` to audit the game architecture."
- "Run `/game-performance` to verify frame budget compliance."
- "Run `/game-ux` to audit the HUD and menu UX."
- "Run `/game-qa` to validate asset loading and save system integrity."

DO NOT:
- Do NOT bundle large assets in the source — use the public directory.
- Do NOT use synchronous asset loading — always async with preloader.
- Do NOT use `any` types in TypeScript — define proper interfaces.
- Do NOT use `setInterval` for game loops — use requestAnimationFrame or framework ticker.
- Do NOT hardcode canvas dimensions — use responsive scaling.
- Do NOT skip audio context resume — browsers block autoplay without user gesture.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /web-game — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
