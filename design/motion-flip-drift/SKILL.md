---
name: motion-flip-drift
description: Diagnose and fix Motion/Framer Motion FLIP layout drift, especially layoutId indicators, selected tabs, shared elements, pane resize, parent resize, sticky/scroll containers, LayoutGroup/layoutRoot/layoutAnchor/layoutDependency issues. Use this whenever a Motion layout animation drifts, floats away, lags behind, jitters, or animates during resize when it should stay visually attached.
---

# Motion FLIP Drift

Use this when a Motion `layout` / `layoutId` element visually drifts away from the DOM it should track.

Typical symptoms:

- A selected tab indicator floats during pane resize.
- A shared `layoutId` element animates when only its parent resized.
- A child looks one frame behind its container.
- A sticky or scrolled child appears to compensate from the wrong origin.
- A layout animation works while clicking but breaks during continuous resize.

## Core Mental Model

Motion layout animation is FLIP through a projection tree:

1. **First**: snapshot old boxes.
2. **Last**: let React/browser commit the new layout.
3. **Invert**: calculate a transform from measured boxes.
4. **Play**: animate that transform back to identity by shrinking the delta.

Motion does not animate CSS layout properties every frame. It measures before/after layout boxes, computes a transform delta, and renders a `transform` that visually compensates the jump while the browser layout is already at the final position.

Drift happens when the box Motion is compensating is not the same coordinate relationship the user expects to stay fixed.

## Projection Internals That Matter

### Measurement Is Page/Viewport First

The base measurement starts from `getBoundingClientRect()` through `measureViewportBox()`. `ProjectionNode.measure()` then:

1. calls `measurePageBox()`
2. removes ancestor `layoutScroll` offsets
3. removes Motion-known transforms when requested
4. stores both `measuredBox` and corrected `layoutBox`

This means Motion's first-order delta is not "child relative to my component". It is page/viewport geometry with corrections.

Useful source paths:

- `create-projection-node.ts`: `measure()`, `measurePageBox()`, `removeElementScroll()`
- `measure.ts`: `measureViewportBox()` calls `getBoundingClientRect()`

### Layout Delta Is Still Box-To-Box

`notifyLayoutUpdate()` calculates:

```ts
layoutDelta = calcBoxDelta(layout, snapshot.layoutBox);
```

For shared layout it also calculates a `visualDelta`, but the core idea is the same: old measured box vs new measured box. If a parent resizes or moves every frame, the child can appear to animate against a moving target.

### Parent Projection Is Applied Later

During projection, Motion copies the node's `layoutBox` into `layoutCorrected`, applies ancestor projection deltas with `applyTreeDeltas()`, then calculates the projection delta from `layoutCorrected` to the target.

This is why parent/child projection can drift under resize: the parent is not simply subtracted from the child's measurement. Parent deltas are part of a later compensation pass, and continuous resize means the target changes again before the previous visual correction fully settles.

### `layoutRoot` Is A Relative Projection Root

`layoutRoot` does not replace `getBoundingClientRect()` with local coordinates. It changes relative target resolution:

- A node is considered projecting when it has `relativeTarget`, `targetDelta`, or `layoutRoot`, **and** it has measured `layout`.
- Descendants find the closest projecting parent through `getClosestProjectingParent()`.
- If that parent has `layoutRoot`, Motion stores the child's `relativeTarget`, `relativeTargetOrigin`, and `relativeParent`.
- Later, if the relative parent is still a `layoutRoot`, Motion preserves that relative target instead of clearing it.

So the practical rule is:

```tsx
// Meaningful relative projection root
<motion.div layout layoutRoot>
  <motion.div layoutId="indicator" />
</motion.div>;
```

Bare `layoutRoot` is a red flag because React Motion only loads layout features for `layout` or `layoutId`, and `isProjecting()` requires layout data.

### `layoutAnchor` Chooses The Parent Reference Point

Relative projection subtracts an anchor point from the parent box:

```ts
relative.min = child.min - parentAnchorPoint;
```

Default anchor is the parent's top-left. `layoutAnchor={{ x: 0.5, y: 0.5 }}` uses the parent center. This can matter in centered/flex layouts where the visually stable reference is the center, not the left edge.

### `LayoutGroup` Is Identity Scope, Not Coordinate Scope

Shared `layoutId` nodes are stored in a `sharedNodes` map on the projection root. `LayoutGroup` prefixes the resolved `layoutId` string. It does not create a local measurement coordinate system.

Use `LayoutGroup` to avoid accidental shared-element matches:

```tsx
<LayoutGroup id={controlId}>
  <motion.div layoutId="indicator" />
</LayoutGroup>;
```

Do not expect it to fix drift caused by parent resize.

### `layoutDependency` Gates Snapshotting

React's layout feature calls `projection.willUpdate()` when:

- dragging
- `layoutDependency` changed
- `layoutDependency` is `undefined`
- presence changed

Passing `layoutDependency={selectedValue}` narrows layout animation to the state transition that should animate. This is useful when pane resize causes unrelated renders but the indicator should only animate on selected-tab changes.

### Shared Layout Lead/Follow Can Add Surprise

With `layoutId`, members join a shared `NodeStack`. The new lead can inherit a snapshot from the previous lead. That is correct for shared element transitions, but it can be too much machinery for a local selected-state highlight.

If a highlight never needs to morph across unrelated subtrees, question whether `layoutId` is the right abstraction.

## Why Drift Appears During Resize

The common failure shape:

1. A parent pane changes width continuously.
2. A selected indicator is a `layoutId` child.
3. Motion measures the indicator in page/viewport coordinates.
4. The parent changes again before the previous layout transform has visually settled.
5. The label/button is normal DOM layout, while the indicator is partly projection transform.
6. The indicator appears to float, lag, or slide relative to the tab.

The user expected "indicator stays attached to active tab in the tablist's local coordinate system." Motion was doing "animate between measured boxes in the projection tree."

The clean fixes either give Motion the missing relative projection root, or stop asking shared layout projection to solve a purely local geometry problem.

## Case Study: Selected Tab Indicator In A Resizable Pane

Symptom: the tab label stayed in place during pane resize, but the selected indicator drifted.

Bad/incomplete experiment:

```tsx
<motion.div layoutRoot>
  <Tabs />
</motion.div>;
```

Why incomplete: `layoutRoot` alone does not provide layout data and may not activate the layout feature path.

Working Motion fix:

```tsx
<Tabs.List render={<motion.div layout layoutRoot />}>
  {items.map((item) => (
    <Tabs.Tab key={item.value} value={item.value}>
      {item.value === value && (
        <motion.div
          layoutId="indicator"
          layoutDependency={value}
          layoutCrossfade={false}
        />
      )}
    </Tabs.Tab>
  ))}
</Tabs.List>;
```

What this changes:

- `layout layoutRoot` gives descendants a valid projecting relative parent.
- `layoutDependency={value}` keeps the indicator animation tied to selection changes.
- `layoutCrossfade={false}` avoids two highlight pills crossfading when a single local indicator is desired.

Implementation caveat: some headless UI render props clone elements and may leak Motion-only props (`layout`, `layoutRoot`) to the DOM. Verify in React warnings and DevTools. If props leak, use a wrapper component that forwards the ref into a real `motion.*` node, or choose the persistent local-indicator pattern.

## First Checks

Start with these before changing code:

- Identify the moving element with `layout` / `layoutId`.
- Identify the container whose movement should be considered "local".
- Check whether the animation should run for the current cause:
  - selected value changed: usually yes
  - pane/window/container resize: often no
  - scroll changed: maybe, if `layoutScroll` is missing
  - parent switched or re-mounted: maybe, if `layoutId` is intentional
- Inspect whether the `motion.*` element is a real DOM element with a forwarded ref. A custom component without a forwarded ref breaks projection.
- Watch DevTools for React unknown-prop warnings like `layoutRoot` leaking to DOM; a render-prop wrapper may not actually be a Motion projection node.

## Fix Decision Tree

### 1. Missing Relative Projection Root

Use this when a child should stay attached to a local parent while the parent moves or resizes.

Do not write bare `layoutRoot`; it is usually not enough. The parent must participate in layout projection:

```tsx
<motion.div layout layoutRoot>
  {isActive && <motion.div layoutId="indicator" />}
</motion.div>;
```

Why: `layoutRoot` makes the node a projecting relative parent only when it has layout data. In React Motion, the layout feature is enabled by `layout` or `layoutId`, not by `layoutRoot` alone.

For centered/flex layouts, consider anchoring relative projection to the visual center:

```tsx
<motion.div layout layoutRoot layoutAnchor={{ x: 0.5, y: 0.5 }}>
  <motion.div layoutId="indicator" />
</motion.div>;
```

Use `layoutAnchor={false}` only when relative projection is causing worse behavior and you want to opt out.

### 2. Animation Should Only Happen For State Changes

Use `layoutDependency` to prevent unrelated renders/resizes from starting a new layout animation.

```tsx
<motion.div
  layoutId="indicator"
  layoutDependency={selectedValue}
/>;
```

This says: "only snapshot/animate this layout when `selectedValue` changes." It is useful for selected-tab indicators that should animate on tab changes but not during pane resizing.

For shared layout handoffs, `layoutDependency` also affects whether the new lead inherits the previous lead's snapshot. Use it deliberately.

### 3. Shared `layoutId` Collision

`layoutId` matching is global within the projection root. Use `LayoutGroup` as an identity namespace, not as a coordinate root.

```tsx
<LayoutGroup id={controlId}>
  <motion.div layoutId="indicator" />
</LayoutGroup>;
```

If two unrelated components both use `layoutId="indicator"` without namespacing, Motion can connect them through the same shared stack.

### 4. Scroll-Induced Drift

If the apparent movement is caused by a scroll container, mark that container with `layoutScroll`.

```tsx
<motion.div layoutScroll className="overflow-auto">
  <motion.div layout />
</motion.div>;
```

`layoutScroll` corrects scroll offsets. It does not fix ordinary parent resize or layout movement.

### 5. Continuous Resize Is Not A Good Shared-Layout Input

FLIP is good when layout changes once and then animates. Continuous pane resize is different: the target box changes every frame.

If resize is the primary interaction:

- Prefer `layoutDependency` so resize does not start indicator animation.
- Or disable/snap layout animation while resizing.
- Or do not use `layoutId` for the indicator; measure the active item relative to the local container and animate `x` / `width` yourself.

For a simple selected indicator, a persistent local indicator is often cleaner than shared layout:

```tsx
const x = activeRect.left - rootRect.left
const width = activeRect.width

<motion.div animate={{ x, width }} />
```

This is a real local-coordinate system. Motion projection is not.

## Best Practices

- Use `motion/react` imports in modern code.
- Put `borderRadius` / `boxShadow` that need scale correction in `style`, not only CSS classes.
- Prefer `layout="position"` when only position should animate.
- Use `layoutCrossfade={false}` for single highlight pills that should not show two overlapping indicators.
- Keep DOM semantics intact. For Base UI/Radix render props, verify Motion props are consumed by a real Motion component and do not leak to the DOM.
- Verify with resize and interaction together, not just click transitions.

## Debugging Checklist

1. Reproduce with paint flashing or DevTools screenshots.
2. Log old/new `getBoundingClientRect()` for the animated child and intended parent.
3. Add `layoutDependency` around the intended trigger. If drift stops during resize, the wrong event was triggering FLIP.
4. Add `layout layoutRoot` to the intended local parent. If drift stops, the child lacked a relative projection root.
5. Add `LayoutGroup id` if there is any chance of shared `layoutId` collision.
6. Add `layoutScroll` only when scroll offset is part of the symptom.
7. If continuous resize still drifts, switch that affordance to a persistent local indicator instead of shared layout.

## Source Pointers

When source verification is needed, inspect these Motion files:

- `packages/motion-dom/src/projection/node/create-projection-node.ts`
  - `measure()`, `measurePageBox()`, `removeElementScroll()`
  - `getClosestProjectingParent()`, `isProjecting()`
  - `notifyLayoutUpdate()`, relative target handling
  - `sharedNodes`, `registerSharedNode()`, `getStack()`
- `packages/framer-motion/src/motion/features/layout/MeasureLayout.tsx`
  - `layoutDependency` snapshot gating
- `packages/framer-motion/src/components/LayoutGroup/index.tsx`
  - `LayoutGroup` id prefixing
- `packages/motion-dom/src/projection/geometry/delta-calc.ts`
  - `calcRelativePosition()` and `layoutAnchor`

## Red Flags

- "Let's add `layoutRoot`" without `layout`.
- Treating `LayoutGroup` as a coordinate system.
- Expecting `layoutScroll` to fix parent resize.
- Using shared `layoutId` for a purely local indicator without a reason.
- Leaving unknown Motion props on real DOM nodes.
- Judging success only by a click transition, without testing resize/scroll/interrupts.
