---
name: inspect-runtime
description: Use when reading state from a running PlayCanvas app, to reach its live Application through the Engine devtools hook without changing app code.
---

# Inspect a running app

From Engine 2.23, every app announces itself to the hook below. Read live state through it, not
`window.app` or debug code.

## Attach

Inject this as an init script, before any page script; a later hook misses existing apps. It chains
an earlier hook, such as a devtools extension's:

```js
{
    const key = Symbol.for('playcanvas.inspector');
    const prev = globalThis[key];
    const apps = (globalThis.__playcanvasApps ??= new Map());

    if (!prev?.playcanvasApps) {
        globalThis[key] = {
            playcanvasApps: apps,
            register(app, info) {
                apps.set(app, info);
                prev?.register?.(app, info);
            },
            unregister(app) {
                apps.delete(app);
                prev?.unregister?.(app);
            }
        };
    }
}
```

- `globalThis.__playcanvasApps` maps each live app to `{ version, revision, protocol }` from
  `app.init()` until `app.destroy()`.
- No entry means the Engine predates 2.23, is a non-debug 2.23.0 build, the hook loaded late, or
  the app set `devtools: false`. The Engine swallows hook errors.

## Read state

- Read after `frameend`, so values reflect a rendered frame.
- Return plain values, not Engine objects.
- Useful reads: `app.root.findByName()` and `findByTag()`, world positions and
  `meshInstance.aabb`, `app.stats.drawCallCount` and `frameTime`, and
  `entity.anim.baseLayer.activeState`.
- Pause with `app.timeScale = 0`; `update` still runs with a zero `dt`. Step one frame by restoring
  the scale, then zeroing it again on the next `frameend`.
- Revert any change made to measure.

## Inspector panel

`@playcanvas/inspector` is a debug panel: `new Inspector(app)` shows the hierarchy, assets, GPU
resources, frame graph, physics, and frame timings; `record: true` records from creation. It must
import the app's own `playcanvas` package, so add it only to development builds. It draws over the
canvas and applies view overrides, so destroy it before `verify-pixels` captures. Stepping through
draws needs the debug build.

With `mcp: true` (0.5.0+), `await inspector.executeTool(name, args)` runs the tools `getTools()`
lists: find entities, get objects by `$id`, record frames, take screenshots, and read logs.
