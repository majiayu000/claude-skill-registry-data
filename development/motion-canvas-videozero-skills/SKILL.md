---
name: motion-canvas
description: Motion Canvas framework reference covering project setup, core concepts (generators, signals, refs, scene hierarchy, timing, utilities), and 2D components (shapes, paths, text, media, layout, camera, transitions, custom components). Use when building or editing Motion Canvas scenes.
---

# Motion Canvas

## Base Scene Template

```ts
import {makeScene2D} from '@motion-canvas/2d';

export default makeScene2D(function* (view) {

});
```

## Generator Functions & Animation Flow

- `function*` defines a generator function
- `yield` pauses until next frame
- `yield*` delegates to another generator (composition)

```ts
export default makeScene2D(function* (view) {
  const circle = createRef<Circle>();
  view.add(<Circle ref={circle} width={100} height={100} fill={'red'} />);

  yield* circle().position.x(300, 1);
  yield* circle().position.x(-300, 1);
});
```

**Reusable animation pattern:**
```ts
function* flicker(circle: Circle, duration: number): ThreadGenerator {
  const colors = ['#e13238', '#e6a700', '#99C47A'];
  for (const color of colors) {
    circle.fill(color);
    yield* waitFor(duration);
  }
}
yield* flicker(myCircle(), 0.5);
```

## Signals System

```ts
import {createSignal} from '@motion-canvas/core';

const radius = createSignal(3);

radius();            // Get → 3
radius(5);           // Set → 5
yield* radius(4, 2); // Tween to 4 over 2 seconds
```

**Computed signals:**
```ts
const area = createSignal(() => Math.PI * radius() * radius());
```

**Signals in JSX:**
```ts
<Circle width={() => radius() * 2} height={() => radius() * 2} />
yield* radius(200, 1); // Circle updates automatically
```

**Vector signals:**
```ts
const position = Vector2.createSignal(Vector2.up);
yield* position(Vector2.zero, 1);
```

**Reset to default:**
```ts
import {DEFAULT} from '@motion-canvas/core';
signal(DEFAULT);             // Instant reset
yield* signal(DEFAULT, 2);   // Tween to default
```

## References (Refs)

**createRef (single node):**
```ts
const circle = createRef<Circle>();
<Circle ref={circle} width={100} height={100} fill={'red'} />
yield* circle().scale(2, 0.3);
```

**makeRef (arrays):**
```ts
const circles: Circle[] = [];
{range(10).map(index => (
  <Circle ref={makeRef(circles, index)} x={index * 50} width={40} height={40} />
))}
yield* all(...circles.map(c => c.scale(1.5, 0.5)));
```

**createRefMap (keyed):**
```ts
const labels = createRefMap<Txt>();
<Txt ref={labels.a} text="Label A" />
<Txt ref={labels.b} text="Label B" />
yield* labels.a().text('Updated A', 0.3);
```

## Scene Hierarchy

```ts
view.add(<Circle />);               // Add to view
container().add(<Circle />);         // Add to node
container().insert(<Circle />, 0);   // Insert at index
circle().remove();                   // Remove
container().removeChildren();        // Remove all children
circle().reparent(newParent());      // Move to new parent
```

**Z-order:** `moveUp()`, `moveDown()`, `moveToTop()`, `moveToBottom()`, `moveTo(2)`

**Querying:**
```ts
import {is} from '@motion-canvas/2d';
const textNodes = view.findAll(is(Txt));
const firstCircle = view.findFirst(is(Circle));
```

## Save / Restore State

```ts
circle().save(); // synchronous: snapshots the current state
yield* all(circle().position.x(300, 1), circle().scale(2, 1));
yield* circle().restore(1); // Animate back to saved state
```

## Time Events & Waiting

```ts
import {waitFor, waitUntil, useDuration} from '@motion-canvas/core';

yield* waitFor(2);                    // Wait 2 seconds
yield* waitUntil('voice-line-2');     // Wait for named event
const dur = useDuration('segment');   // Get event duration
```

## Utilities

**Random:** `useRandom(42)` → `.nextInt(10, 100)`, `.nextFloat(0, 1)`
**Logging:** `useLogger()` → `.debug()`, `.info()`, `.warn()`, `.error()`; also `debug('msg')`
**Hooks:** `useScene()` → `.getSize()`; `useTime()`
**Range:** `range(5)` → `[0,1,2,3,4]`; `range(2,5)` → `[2,3,4]`
**Threads:**
```ts
// Spawn a background thread (do NOT yield — spawn starts it automatically)
const task = spawn(function* () {
  yield* loop(Infinity, function* () {
    yield* circle().rotation(360, 2);
    circle().rotation(0);
  });
});

// Cancel a running thread
cancel(task);

// Wait for a thread to finish
yield* join(task);
```

```ts
spawn(a()); // run a in the background without waiting for it
yield* waitFor(0.5); // wait 0.5s
yield* b(1); // run b
```


## Shape Components

**Circle:**
```ts
<Circle width={200} height={200} fill={'#e13238'} stroke={'#fff'} lineWidth={4}
  startAngle={0} endAngle={270} closed={false} />
```

**Rect:**
```ts
<Rect width={300} height={200} fill={'#68ABDF'} radius={10} smoothCorners cornerSharpness={0.6} />
```

**Line:**
```ts
<Line points={[[0,0],[100,100],[200,50]]} stroke={'#fff'} lineWidth={4}
  lineDash={[20,10]} lineCap={'round'} lineJoin={'round'} startArrow endArrow arrowSize={12} />
```

**Polygon:**
```ts
<Polygon sides={6} size={200} fill={'#99C47A'} />
```

**Grid:**
```ts
import {Grid} from '@motion-canvas/2d';

<Grid width={'100%'} height={'100%'} stroke={'#333'} lineWidth={1} spacing={80} start={0} end={1} />
```
Animate with `start`/`end` (0-1) for drawing/erasing effects.

**Path** (SVG path data):
```ts
import {Path} from '@motion-canvas/2d';

<Path data={'M 0 -100 L 29 -40 L 95 -31 Z'} stroke={'#e6a700'} lineWidth={3} />
```
Supports morphing: `yield* path().data(newPathData, 1);`

## Filters

```ts
import {blur, brightness, grayscale, sepia, contrast, saturate, hue, invert} from '@motion-canvas/2d';

<Rect filters={[blur(5), brightness(1.5)]} />
yield* rect().filters([blur(0), grayscale(1)], 1); // Animated
```

See [Filters](references/FILTERS.md) for full details.

## Gradients

```ts
import {Gradient} from '@motion-canvas/2d';

const grad = new Gradient({
  type: 'linear',
  from: [-100, 0], to: [100, 0],
  stops: [{offset: 0, color: '#e13238'}, {offset: 1, color: '#68ABDF'}],
});
<Rect fill={grad} />
```

See [Gradients](references/GRADIENTS.md) for radial and conic types.

## Path Components

**Ray:** `<Ray from={[0,0]} to={[300,200]} endArrow />` — animate with `start(1,1)` / `end(0,1)`
**CubicBezier:** `<CubicBezier p0={..} p1={..} p2={..} p3={..} />`
**QuadBezier:** `<QuadBezier p0={..} p1={..} p2={..} />`
**Spline:** `<Spline points={[..]} smoothness={0.4} />` — smooth curves; `smoothness` controls how round the curve is
**Knot:** `<Spline><Knot position={[-200,0]} /><Knot position={[0,0]} startHandle={[-50,0]} /><Knot position={[200,0]} /></Spline>` — explicit control points with optional handles

## Text Rendering

See [Txt](references/TXT.md) for full details.

```ts
<Txt text={'Hello World'} fontSize={64} fill={'#ffffff'} textWrap={true} />
```

## Custom Components

```ts
export class Switch extends Node {
  @initial(false) @signal()
  public declare readonly initialState: SimpleSignal<boolean, this>;

  public constructor(props?: SwitchProps) {
    super({...props});
  }

  public *toggle(duration: number) { /* animation logic */ }
}
```

**Decorators** (import from `@motion-canvas/2d`): `@signal()`, `@initial(value)`, `@colorSignal()`, `@vector2Signal()`

```ts
import {Node, NodeProps, initial, signal} from '@motion-canvas/2d';
```

## Scene Transitions

```ts
import {slideTransition, fadeTransition, Direction, Origin} from '@motion-canvas/core';
yield* slideTransition(Direction.Left);
```

**All transitions** (from `@motion-canvas/core`):
- `slideTransition(Direction.Left, duration?)` — slide in from a direction (or `slideTransition(Origin.TopLeft)` to slide in from a corner)
- `fadeTransition(duration?)` — cross-fade
- `zoomInTransition(area, duration?)` — zoom into a BBox area
- `zoomOutTransition(area, duration?)` — zoom out from a BBox area
- `waitTransition(duration?)` — wait without visual transition

**Directions:** `Direction.Top`, `Bottom`, `Left`, `Right`. For diagonals, pass an `Origin` (`Origin.TopLeft`, `Origin.BottomRight`, …).

Add the new scene's content **before** `yield* slideTransition(...)`; otherwise it pops in after the transition.

**Custom:**
```ts
import {createSignal, useTransition} from '@motion-canvas/core';
const progress = createSignal(0);
// useTransition returns a function that ENDS the transition. It is not a generator.
const endTransition = useTransition(
  ctx => { ctx.globalAlpha = progress(); }, // before the current scene renders
  ctx => { /* before the previous scene renders */ },
);
yield* progress(1, 0.6);
endTransition();
```

## Advanced Patterns

**Conditional:** `if (cond()) yield* a(); else yield* b();`
**Reactive:** `<Circle fill={() => val() > 150 ? 'red' : 'blue'} />`
**State machines:** `while/switch` pattern with enum states

## References

- [Setup](references/SETUP.md) — Project creation, installation, troubleshooting
- [Flow Control](references/FLOW_CONTROL.md) — all, any, chain, delay, sequence, loop
- [Tweening](references/TWEENING.md) — Property tweens, easing, interpolation
- [Springs](references/SPRINGS.md) — Physics-based spring animations
- [Transforms](references/TRANSFORMS.md) — Coordinates, positioning, matrix operations
- [Presentation Mode](references/PRESENTATION_MODE.md) — Slide-based playback
- [Txt](references/TXT.md) — Text rendering, dynamic text, multi-line
- [Layout](references/LAYOUT.md) — Flexbox, cardinal directions, offset
- [LaTeX](references/LATEX.md) — Mathematical equations
- [Media](references/MEDIA.md) — Images, icons, video
- [SVG](references/SVG.md) — Animatable SVG component
- [Icons](references/ICONS.md) — Iconify icon usage and catalog
- [Camera](references/CAMERA.md) — Pan, zoom, follow
- [Filters](references/FILTERS.md) — blur, brightness, contrast, grayscale, sepia, hue, saturate, invert
- [Gradients](references/GRADIENTS.md) — Linear, radial, conic gradient fills
- [Effects](references/EFFECTS.md) — createEffect, createDeferredEffect
- [Rendering](references/RENDERING.md) — Rendering settings and output configuration
- [Sounds](references/SOUNDS.md) — Programmable sound playback (@alpha)
