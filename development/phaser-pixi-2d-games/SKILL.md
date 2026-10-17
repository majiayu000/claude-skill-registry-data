---
name: phaser-pixi-2d-games
category: engine
description: Use when building a 2D web game with Phaser (3.x/4.x) or PixiJS 8 in TypeScript - framework vs renderer, Phaser scenes/game objects/arcade physics/groups as pools/scale manager/loader, scene shutdown cleanup, PixiJS 8 async init, Assets bundles, ticker units and destroy, and keeping rules in plain TS modules.
tech_stack: Web 2D
source: informed by the Phaser 3/4 and PixiJS 8 documentation and migration guides; own wording
---
# Phaser and PixiJS 2D Games

## Overview

Phaser is a game framework: scenes, game objects, input, physics, audio, tweens, a loader and a scale manager. PixiJS is a fast 2D renderer: display objects, textures and a ticker — scenes, physics, input mapping and audio are yours to add. Pick by what the repository already uses; never put both in one game.

**Core principle:** The engine draws and dispatches; rules live in plain TypeScript modules with no engine import, so Vitest can run them (web-game-performance-and-testing).

## Phaser: structure

```ts
// main.ts
new Phaser.Game({
  type: Phaser.AUTO,
  parent: "game",
  backgroundColor: "#101018",
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH, width: 1280, height: 720 },
  physics: { default: "arcade", arcade: { gravity: { x: 0, y: 900 }, debug: false } },
  scene: [BootScene, PreloadScene, GameScene, HudScene],
});
```

```ts
// GameScene.ts — the scene wires engine objects to plain rules
export class GameScene extends Phaser.Scene {
  private player!: Player;
  private bullets!: Phaser.Physics.Arcade.Group;
  private rules!: CombatRules;                       // plain TS, no Phaser import

  constructor() { super("Game"); }

  create(data: { seed: number }): void {
    this.rules = new CombatRules(definitions.combat, mulberry32(data.seed ?? Date.now()));
    this.player = new Player(this, 200, 500);
    this.bullets = this.physics.add.group({ classType: Bullet, maxSize: 64, runChildUpdate: true });
    this.physics.add.overlap(this.bullets, this.enemies, (b, e) => this.onHit(b as Bullet, e as Enemy));
    this.scene.launch("Hud");                        // HUD as a parallel scene listening to events
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => this.cleanup());
  }

  update(_time: number, deltaMs: number): void {
    this.rules.tick(deltaMs / 1000);                  // Phaser's delta is milliseconds
    this.player.applyIntent(this.input.keyboard!, deltaMs / 1000);
  }

  private fire(x: number, y: number): void {
    const b = this.bullets.get(x, y) as Bullet | null;  // reuse from the pool; null when maxSize reached
    b?.launch(600);
  }

  private cleanup(): void {
    this.game.events.off("settings-changed", this.applySettings, this);
  }
}
```

- Scenes: Boot (config) → Preload (loader with a progress bar) → gameplay scenes; HUD/UI in a parallel scene (`scene.launch`) talking through events, not object references.
- Game objects as classes extending `Phaser.GameObjects.Sprite` / `Phaser.Physics.Arcade.Sprite`, added with `scene.add.existing(this)` and `scene.physics.add.existing(this)`.
- Groups are pools: `maxSize`, `get()`, and on release `setActive(false).setVisible(false)` plus disabling the body (`group.killAndHide(obj)`, `body.enable = false`). Never `new` + `destroy` per shot.
- Arcade physics steps on its own fixed rate (`arcade.fps`, default 60); move bodies with velocity/acceleration, not by setting `x`/`y` each frame. Matter physics for real shapes and constraints, at higher cost.
- Listeners registered on `this.game.events`, the registry, or DOM/window must be removed on `SHUTDOWN`; listeners on the scene's own emitter die with it. Restarting a scene that leaked listeners doubles every handler.
- Loader: texture atlases (`this.load.atlas(key, png, json)`), audio with format alternatives (`this.load.audio("hit", ["hit.ogg", "hit.m4a"])`), a pack file for large asset lists.
- Input: map keys to actions once (`this.input.keyboard!.addKeys({ jump: "SPACE", left: "A", right: "D" })`); pointer and touch through the same action layer; gamepads with `input: { gamepad: true }` in the config.
- Phaser 4 keeps the v3 scene and game-object model with a new renderer; follow the repository's major version and its migration notes rather than mixing APIs.

## PixiJS 8: the renderer

```ts
const app = new Application();
await app.init({ resizeTo: window, background: "#101018", antialias: false });   // async in v8
document.getElementById("game")!.appendChild(app.canvas);                         // `canvas`, not `view`

await Assets.init({ manifest: "assets/manifest.json" });
const level = await Assets.loadBundle("level-1");

const world = new Container();
app.stage.addChild(world);
const hero = new Sprite(level.hero);
world.addChild(hero);

app.ticker.add((ticker) => {
  const dt = ticker.deltaMS / 1000;            // seconds; ticker.deltaTime is a frame-scaled factor (~1 at 60 FPS)
  sim.step(dt);
  hero.position.set(sim.hero.x, sim.hero.y);
});
```

- Version 8 changes that break v7 code: async `app.init`, `app.canvas`, the ticker callback receiving the `Ticker`, the chainable `Graphics` API (`new Graphics().rect(0, 0, 10, 10).fill(0xff0000)`), `ParticleContainer` holding lightweight `Particle`s.
- Load through `Assets` with bundles per level; unload a level's bundle when leaving it (`Assets.unloadBundle`).
- `destroy({ children: true })` removes a subtree; pass `texture: true` only for textures nothing else shares.
- Many identical sprites: one atlas texture so the batcher draws them together; `ParticleContainer` for thousands of particles; `cullable = true` on off-screen-heavy scenes.
- Pixi has no physics or input mapping: the simulation (accumulator loop, game-loop-and-time) and the action layer are your modules, and the ticker only renders their state.

## Shared rules

- TypeScript `strict`; no `any`, no `as` casts to silence the compiler — type game object factories and event payloads.
- One source of randomness, seeded (`mulberry32(seed)`), passed into rules; the seed comes from the URL in debug builds so tests and screenshots are reproducible.
- Text: bitmap fonts for frequently changing numbers (score, timers); `Text` objects regenerate a texture on every change.
- Pixel art: `pixelArt: true` (Phaser) or `antialias: false` plus nearest scaling (Pixi), integer zoom, and positions rounded at render time.
- Scale and letterbox to a fixed logical resolution; never size the game from `window.innerWidth` inside rules.

## Common Mistakes

- Treating Phaser's or Pixi's `delta` as seconds.
- Creating and destroying bullets and particles every frame.
- Scene restarts that leak listeners on `game.events`.
- Rules written inside `Scene.update` that Vitest cannot import without a canvas.
- Pixi v7 code (`app.view`, synchronous `new Application({...})`) pasted into a v8 project.

## Red Flags

- `import Phaser` or `import { Sprite } from "pixi.js"` in a file under the rules/logic folder.
- `this.add.text` updated every frame for a score counter.
- A scene with `events.on` on a global emitter and no matching `off`.
