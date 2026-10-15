---
name: motion-layout-animations
description: Motion layout animation internals - layoutId, layoutGroup, FLIP mechanism, NodeStack promote/relegate, scale correction. Use when implementing shared element transitions, debugging layout animations, or understanding why borderRadius must be in style prop.
---

# Motion Layout Animations

Deep technical reference for Motion's layout animation system.

## Core Concepts

### FLIP Principle

Layout animations use FLIP (First, Last, Invert, Play):

1. **First**: Snapshot element's current position/size
2. **Last**: Let browser reflow to new position/size
3. **Invert**: Apply inverse transform to visually restore old position
4. **Play**: Animate transform back to identity (new position)

Motion implements this via the **projection system** - a tree of `ProjectionNode`s that track layout changes and compute compensating transforms.

### Key Components

| Component                | Purpose                                                |
| ------------------------ | ------------------------------------------------------ |
| `ProjectionNode`         | Tracks element layout, computes deltas                 |
| `NodeStack`              | Manages multiple nodes sharing a `layoutId`            |
| `DocumentProjectionNode` | Global root, stores all `sharedNodes`                  |
| `LayoutGroup`            | Adds prefix to `layoutId`, creates isolated namespaces |

---

## layoutId: Shared Element Transitions

### How It Works

When an element with `layoutId` mounts:

```
1. registerSharedNode(layoutId, node)
2. stack.add(node)
3. node.promote()  ← immediately becomes lead
   └── prevLead.updateSnapshot()
   └── node.snapshot = prevLead.snapshot  ← inherits position
   └── prevLead.hide()  (if crossfade=false)
4. node animates FROM prevLead's snapshot TO its own layout
```

**Key insight**: The NEW element animates. The old element is hidden (`visibility: hidden`) and still occupies space.

### Typical Usage

```tsx
// No AnimatePresence needed for basic shared transition
{
  isExpanded
    ? (
      <motion.div layoutId="card" className="expanded">
        <motion.div layoutId="title">Title</motion.div>
        <motion.div layoutId="content">Content</motion.div>
      </motion.div>
    )
    : (
      <motion.div layoutId="card" className="collapsed">
        <motion.div layoutId="title">Title</motion.div>
      </motion.div>
    );
}
```

- `card`, `title`, `content` each get their own `NodeStack`
- When switching, new elements inherit snapshots from old ones
- Old elements hidden via `visibility: hidden` (still occupy layout space)

### Lead/Follow Mechanism

```
NodeStack.members: [A, B, C]  ← C is lead (last registered)
                         ↑
                       lead
```

**Promote** (new element becomes lead):

- `prevLead = lead`
- `lead = newNode`
- `newNode.snapshot = prevLead.snapshot`
- `newNode.resumeFrom = prevLead`

**Relegate** (lead exits, find replacement):

- Iterate backwards from lead's index
- First node with `isPresent !== false` and `isConnected` becomes new lead

See [internals.md](internals.md#nodestack-implementation) for code.

---

## layout: Single Element Transitions

### How It Works

```tsx
<motion.div layout style={{ justifySelf: isRight ? "end" : "start" }}>
  Item
</motion.div>;
```

When CSS causes position/size change:

1. `willUpdate()` → snapshot current layout
2. Browser reflows
3. `didUpdate()` → measure new layout, compute delta
4. Apply inverse transform, animate to identity

### layout Prop Values

| Value                 | Behavior                               |
| --------------------- | -------------------------------------- |
| `true` / `"position"` | Animate position changes               |
| `"size"`              | Animate size changes                   |
| `"preserve-aspect"`   | Maintain aspect ratio during animation |

### Parent Transform Compensation

Child elements with `layout` automatically compensate for parent's transform:

```tsx
<motion.div layoutId="container">
  <motion.div layout>Title</motion.div> {/* Won't stretch with parent */}
</motion.div>;
```

Without `layout`, children would be visually stretched by parent's scale transform.

---

## LayoutGroup: Namespace Isolation

### How It Works

`LayoutGroup` provides a `LayoutGroupContext` with an `id` that prefixes all child `layoutId`s:

```tsx
<LayoutGroup id="sidebar">
  <motion.div layoutId="item" />  {/* actual layoutId: "sidebar-item" */}
</LayoutGroup>

<LayoutGroup id="main">
  <motion.div layoutId="item" />  {/* actual layoutId: "main-item" */}
</LayoutGroup>
```

These two `layoutId="item"` elements **don't share** a `NodeStack` because their prefixed IDs differ.

### Nested Groups

```tsx
<LayoutGroup id="app">
  <LayoutGroup id="panel">
    <motion.div layoutId="card" /> {/* layoutId: "app-panel-card" */}
  </LayoutGroup>
</LayoutGroup>;
```

See [internals.md](internals.md#layoutgroup-prefix) for implementation.

---

## Scale Correction: Why borderRadius Must Be in style

### The Problem

FLIP uses `transform: scale()` to animate size changes. But `borderRadius` in pixels gets visually stretched:

```
Original: 100x100 box, borderRadius: 10px (10%)
Scaled 2x via transform: 200x200 visual, but borderRadius looks like 20px (still 10%)
                         ↑ corners appear stretched
```

### The Solution

Motion's `scaleCorrectors` convert pixel values to percentages relative to target box:

```ts
// packages/motion-dom/src/projection/styles/scale-border-radius.ts
correct: ((latest, node) => {
  const x = pixelsToPercent(latest, node.target.x);
  const y = pixelsToPercent(latest, node.target.y);
  return `${x}% ${y}%`;
});
```

### Why style Prop Required

Motion only tracks values in `latestValues` (from `style` prop or initial read). The `isForcedMotionValue` check forces these properties into the motion value system when `layout`/`layoutId` is present:

```ts
// Simplified from is-forced-motion-value.ts
function isForcedMotionValue(key, props) {
  return scaleCorrectors[key] && (props.layout || props.layoutId !== undefined);
}
```

**Affected properties**: `borderRadius`, `borderTopLeftRadius`, etc., `boxShadow`

If you put `borderRadius` only in CSS class, Motion can't track or correct it during FLIP animation.

See [internals.md](internals.md#scale-correction) for full implementation.

---

## Hidden Elements and Layout Space

When an element becomes `prevLead` (follower):

```ts
// stack.promote()
if (node.options.crossfade === false) prevLead.hide();
```

`hide()` sets `visibility: hidden`:

```ts
// applyProjectionStyles
if (!this.isVisible) {
  targetStyle.visibility = "hidden";
  return;
}
```

**Important**: `visibility: hidden` still occupies layout space. The old element remains in DOM, invisible but affecting layout, until:

- Animation completes and `safeToRemove()` is called (with AnimatePresence)
- Or React unmounts it (without AnimatePresence)

---

## AnimatePresence Integration

Without `AnimatePresence`:

- Old element unmounted immediately by React
- New element animates from old snapshot
- Only new element visible during animation

With `AnimatePresence`:

- Old element kept in DOM via `PresenceChild`
- Both elements visible → crossfade possible
- `relegate()` called when `isPresent` becomes false
- `safeToRemove()` defers actual unmount until animation completes

```tsx
<AnimatePresence>
  {items.map((item) => <motion.div key={item.id} layoutId={item.id} exit={{ opacity: 0 }} />)}
</AnimatePresence>;
```

---

## Common Patterns

### Shared Container Transition

```tsx
function ExpandableCard({ isExpanded }) {
  return (
    <motion.div
      layoutId="card"
      style={{ borderRadius: 12 }} // Must be in style for scale correction
      className={isExpanded ? "expanded" : "collapsed"}
    >
      <motion.h2 layoutId="title" layout>
        Title
      </motion.h2>
      {isExpanded && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          Extra content
        </motion.div>
      )}
    </motion.div>
  );
}
```

### List Reordering

```tsx
function ReorderableList({ items }) {
  return (
    <Reorder.Group values={items} onReorder={setItems}>
      {items.map((item) => (
        <Reorder.Item key={item.id} value={item} layoutId={item.id}>
          {item.label}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  );
}
```

### Isolated Sections

```tsx
<LayoutGroup id="sidebar">
  {sidebarItems.map(item => (
    <motion.div key={item.id} layoutId={item.id} layout />
  ))}
</LayoutGroup>

<LayoutGroup id="content">
  {contentItems.map(item => (
    <motion.div key={item.id} layoutId={item.id} layout />
  ))}
</LayoutGroup>
```

---

## Debugging Tips

1. **Check actual layoutId**: If using `LayoutGroup`, the real ID has prefix. Log `visualElement.projection.options.layoutId`.

2. **Verify NodeStack**: Check `projection.root.sharedNodes.get(layoutId)` to see all members.

3. **borderRadius not animating**: Ensure it's in `style` prop, not just CSS class.

4. **Elements not matching across Portal**: `layoutId` matching is global (via `DocumentProjectionNode`), but verify IDs aren't prefixed differently.

5. **Unexpected layout shifts**: Hidden elements (`visibility: hidden`) still occupy space. Check if old elements are lingering.

---

## Additional Resources

- [internals.md](internals.md) - Detailed code references with line numbers
