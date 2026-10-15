---
name: zero-height-side-element
description: Layout pattern for placing a side element (toggle, badge, icon) that visually occupies horizontal space but does not affect the row's vertical height. Use when building list rows, settings rows, or any horizontal layout where a side element should not stretch the container height.
---

# Zero-Height Side Element

A flexbox technique for placing a side element (toggle, badge, icon button) in a row without letting it dictate the row's height. The element still occupies its natural horizontal width and remains vertically centered.

## Problem

In a flex row with `items-center`, the tallest child determines the row height. A large side element (e.g. a 28px toggle in a row with 20px text) stretches the row, breaking consistent spacing set by padding alone.

Using `position: absolute` solves height but removes the element from flow, losing its horizontal space reservation and requiring manual `right` / `padding-right` management.

## Pattern

Wrap the side element in a **zero-height flex container** with centered alignment:

```tsx
<div className="flex items-center justify-between px-4 py-3.5">
  <span className="min-h-[1lh] min-w-0 truncate">{label}</span>
  <div className="flex h-0 shrink-0 items-center">
    <Toggle />
  </div>
</div>;
```

## How It Works

| Class                     | Purpose                                                         |
| ------------------------- | --------------------------------------------------------------- |
| `h-0`                     | Container contributes zero height to the flex cross-axis        |
| `shrink-0`                | Prevents the wrapper from being compressed by flex              |
| `flex items-center`       | Centers the child vertically relative to the wrapper's position |
| `min-h-[1lh]` on the text | Guarantees the row never collapses to zero when text is empty   |

The wrapper sits in normal flow — it occupies horizontal space just like any flex child — but its zero height means the row's cross-size is determined solely by the text element and the container's padding.

## Why Not `absolute`

`position: absolute` removes the element from the document flow in **both axes** — block (vertical) and inline (horizontal). This means:

- The side element no longer reserves horizontal space.
- If the left-side text grows long, it will overlap the absolutely positioned element because flex doesn't know it's there.
- You must manually manage `right` offset and matching `padding-right` on the container to prevent collision.

The zero-height wrapper only opts out of the **block axis** (height). In the inline axis (width) it remains a normal flex child — `shrink-0` ensures it keeps its natural width, and `justify-between` pushes it to the trailing edge. When the left-side text is long, flex's `min-w-0 truncate` on the text element causes it to shrink and ellipsize _before_ it reaches the side element, because the side element legitimately occupies that space in the flow.

```
absolute:      [text overflows underneath]  [toggle floating on top]
zero-height:   [text truncates with ...]    [toggle]
```

## When to Use

- Settings / toggle rows where padding controls row height
- List items with trailing badges or action buttons
- Any row where side content is taller than primary content

## When NOT to Use

- Side element height should legitimately determine row height
- Complex multi-line layouts where absolute positioning is more appropriate
