---
name: pixijs-rendering
description: >
  Build a PixiJS v8 render layer: create the async Application, load textures with
  Assets, compose the scene graph with Container and Sprite, drive the ticker loop,
  wire pointer events, and group draws with render groups. Use when building or
  debugging PixiJS v8 — when the user mentions PixiJS, Pixi, Application, app.stage,
  Container, Sprite, Assets.load, app.ticker, or eventMode. Pins the v8 async
  init() API.
---

# PixiJS 8.21 Rendering

Set up and structure a PixiJS **8.21** application: the async `Application`, asset
loading via `Assets`, the `Container`/`Sprite` scene graph, the ticker loop,
pointer events, and render groups. Pins the 8.21 API (async `init`, unified
`Assets`, `eventMode`).

## When to use

- Use when starting a PixiJS v8 project, fixing a blank canvas, structuring the
  display list, loading textures, animating via the ticker, or handling pointer
  input.
- Use when `package.json` depends on `pixi.js` (v8) and code does
  `import { Application } from 'pixi.js'`.

**When *not* to use:** Phaser's scene/loader model → `phaser-core`. 3D scenes →
`threejs-scene-setup`. PixiJS v7-and-earlier code (synchronous `new
Application({...})`, `Loader`, `beginFill`/`endFill`) needs the v8 migration first;
this skill targets v8 only. (`interactive = true` still works in v8 as an alias for
`eventMode = 'static'`, but prefer the explicit `eventMode`.)

## Core workflow

1. **Create and `await` the Application.** In v8, `new Application()` is empty;
   configuration happens in `await app.init({...})`. Append `app.canvas` (not
   `app.view`) to the DOM. Wrap top-level `await` in an async function for bundlers.
2. **Load assets with `Assets`.** `await Assets.load(url)` returns a `Texture`. For
   many assets, register a manifest/bundle and load by name. There is no v7 `Loader`.
3. **Build the scene graph.** Everything descends from `app.stage` (a `Container`).
   Group related objects in `Container`s; child transforms are relative to the
   parent. Draw order = insertion order (later = on top).
4. **Animate with the ticker.** `app.ticker.add((ticker) => {...})`. Scale motion by
   `ticker.deltaTime` (frames, ~1 at 60fps) or `ticker.deltaMS` (milliseconds) so
   speed is frame-rate independent.
5. **Enable events per object** by setting `eventMode = 'static'` (or `'dynamic'`),
   then `obj.on('pointerdown', ...)`. Federated pointer events cover mouse/touch/pen.
6. **Promote big static subtrees to render groups** (`isRenderGroup: true`) so the
   GPU caches their transforms. Profile before and after; confirm pixels on screen.

## Patterns

### 1. Async Application boot (the v8 entry point)

```js
import { Application, Assets, Sprite } from 'pixi.js';

(async () => {
  // v8: construct empty, then await init(). Config does NOT go in the constructor.
  const app = new Application();
  await app.init({
    background: '#1099bb',
    resizeTo: window,        // track the window size
    antialias: true,
    // preference: 'webgpu',  // hint only; default order tries 'webgl' first.
    //                        // Pixi falls back if the backend is unavailable —
    //                        // branch on app.renderer.name, don't assume it took.
  });

  document.body.appendChild(app.canvas); // v8 uses app.canvas, not app.view

  const texture = await Assets.load('https://pixijs.com/assets/bunny.png');
  const bunny = new Sprite(texture);
  bunny.anchor.set(0.5);
  bunny.position.set(app.screen.width / 2, app.screen.height / 2);
  app.stage.addChild(bunny);
})();
```

### 2. Containers for a relative-transform scene graph

```js
import { Container, Sprite } from 'pixi.js';

const world = new Container();
app.stage.addChild(world);

// Children are positioned relative to `world`; move/scale/rotate the whole group
// by transforming the parent.
for (let i = 0; i < 10; i++) {
  const coin = new Sprite(coinTexture);
  coin.x = i * 40;
  world.addChild(coin);
}
world.position.set(100, 100);
world.scale.set(2);            // every coin scales with the container
```

### 3. The ticker loop (frame-rate independent)

```js
let elapsed = 0;
app.ticker.add((ticker) => {
  // deltaTime ≈ 1 at 60fps; deltaMS is milliseconds since last frame.
  elapsed += ticker.deltaMS;
  bunny.rotation += 0.05 * ticker.deltaTime;          // smooth at any frame rate
  bunny.y = app.screen.height / 2 + Math.sin(elapsed / 500) * 50;
});
```

### 4. Pointer events (federated)

```js
bunny.eventMode = 'static';   // 'static' = interactive, doesn't move on its own
bunny.cursor = 'pointer';     // hover cursor; `buttonMode` was removed in v8
bunny.on('pointerdown', (event) => {
  bunny.tint = 0xff0000;
  // event.global is the pointer position in stage space.
});
bunny.on('pointerover', () => bunny.scale.set(1.1));
bunny.on('pointerout',  () => bunny.scale.set(1.0));
```

Dragging needs `globalpointermove`, not `pointermove`. In v8 `pointermove` fires
**only while the pointer is over the object**, so a drag that follows the cursor
past the object's edge stops updating. `globalpointermove` fires on every move:

```js
let dragging = false;
bunny.on('pointerdown', () => { dragging = true; });
bunny.on('pointerup', () => { dragging = false; });
bunny.on('pointerupoutside', () => { dragging = false; }); // release off the object
bunny.on('globalpointermove', (event) => {
  if (dragging) bunny.position.copyFrom(event.global);
});
```

### 5. Loading many assets by name (bundles)

```js
import { Assets } from 'pixi.js';

await Assets.init({
  manifest: {
    bundles: [{
      name: 'level-1',
      assets: [
        { alias: 'hero',  src: 'assets/hero.png' },
        { alias: 'tiles', src: 'assets/tiles.png' },
      ],
    }],
  },
});

const bundle = await Assets.loadBundle('level-1'); // { hero: Texture, tiles: Texture }
const hero = new Sprite(bundle.hero);
```

### 6. Render groups for large static layers

```js
// A big, rarely-changing background subtree: let the GPU cache its transforms.
const background = new Container({ isRenderGroup: true });
app.stage.addChild(background);
// Add hundreds of static tiles to `background`. Moving `background` itself stays
// cheap; constantly re-adding/removing children negates the benefit.
```

## Pitfalls

- **Blank canvas / "app.stage is undefined"** → you didn't `await app.init()`, or you
  configured the constructor. In v8 the constructor is empty; all options go to
  `init()`. `app.renderer`/`app.canvas`/`app.screen` are `undefined` until the
  `init()` promise resolves.
- **`app.view` is undefined** → v8 renamed it to `app.canvas`.
- **Porting v7 code** → `Loader`/`loader.add` → `Assets.load` (the `Loader` class is
  gone); synchronous `new Application({...})` → empty constructor + async `init()`
  (options in the constructor are ignored with a deprecation warning, not an error);
  `beginFill()`/`endFill()` → shape-first `.rect(...).fill(...)`. `interactive = true`
  and `app.view` still work as deprecated aliases.
- **Ticker callback arg is the Ticker, not a delta number** → `app.ticker.add((dt) =>
  { obj.rotation += dt; })` compiles, but `dt` is the whole `Ticker` object, so the
  math yields `NaN` and nothing animates. Read `ticker.deltaTime` off the argument.
- **Top-level await build error (Vite ≤6.0.6)** → wrap boot in `(async () => { ... })()`.
- **Speed varies with frame rate** → multiply movement by `ticker.deltaTime` (~1 at
  60fps) or scale by `ticker.deltaMS`; never assume 60fps. `deltaTime` is a
  dimensionless multiplier, not milliseconds.
- **Clicks do nothing** → the object's `eventMode` is still `'passive'` (the v8
  default: self not interactive, children still are); set it to `'static'` (or
  `'dynamic'` for objects that move under a stationary cursor).
- **Drag stops at the object's edge** → `pointermove` fires only while the pointer is
  over the object in v8; use `globalpointermove` for drag/global tracking.
- **`Texture.from(url)` returns a blank/undefined texture** → in v8 it only reads the
  Assets cache; `await Assets.load(url)` first, then use the returned `Texture`.
- **WebGPU features error out** → `preference` is a hint. If the backend is
  unavailable Pixi falls back (WebGL, then Canvas); branch on `app.renderer.name`
  before using backend-specific code.
- **Textures look blurry on pixel art** → set
  `texture.source.scaleMode = 'nearest'` (or pass it when loading).
- **Memory grows** → `removeChild` does not free GPU memory; call
  `sprite.destroy()` and `Assets.unload(url)` for assets you're done with.
- **Flicker/corruption after tearing down and re-creating an app in the same tab** →
  destroy with `app.destroy({ releaseGlobalResources: true })`; otherwise pooled
  batches/textures from the old app leak into the new one.

## References

- For the texture/asset pipeline (sprite sheets/atlases, `Assets.add`, background
  loading, unloading) and Graphics/Text/`TilingSprite`/`ParticleContainer` plus
  filters, read `references/assets-and-display.md`.

## Related skills

- `phaser-core` — a batteries-included 2D framework (scenes, physics, input).
- `threejs-scene-setup` — 3D in the browser with three.js.
- `prototype-fast` — greybox a playable slice quickly (often cites PixiJS).
