---
name: dropdown-menu
description: Creates dropdown menus with proper click-outside detection and z-index stacking for list contexts. Use when building action menus, context menus, or any dropdown that appears in cards/list items.
---

# Dropdown Menu Pattern

Build dropdown menus that work correctly in list/card contexts, handling z-index stacking and click-outside dismissal properly.

## Why This Pattern?

Dropdown menus in list items have three common bugs:

1. **Clipped by parent's `overflow-hidden`** - dropdown gets cut off
2. **Covered by sibling cards** - z-index doesn't help across stacking contexts
3. **Double-toggle on trigger click** - menu closes then reopens immediately

This pattern solves all three.

## Core Implementation

```tsx
"use client";

import { useState, useRef, useEffect } from "react";
import { MoreVertical, Pause, X } from "lucide-react";

// The dropdown menu component
function DropdownMenu({
  dark = false,
  onClose,
}: {
  dark?: boolean;
  onClose: () => void;
}) {
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        onClose();
      }
    }
    // IMPORTANT: Use "click" not "mousedown" to allow stopPropagation on trigger
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, [onClose]);

  return (
    <div
      ref={menuRef}
      className={`absolute right-0 top-full mt-1 z-20 rounded-lg shadow-lg border overflow-hidden ${
        dark ? "bg-zinc-800 border-zinc-700" : "bg-white border-zinc-200"
      }`}
    >
      <button
        className={`flex items-center gap-2 w-full px-3 py-2 text-xs font-medium transition-colors ${
          dark
            ? "text-zinc-300 hover:bg-zinc-700"
            : "text-zinc-700 hover:bg-zinc-50"
        }`}
        onClick={(e) => {
          e.stopPropagation();
          onClose();
        }}
      >
        <Pause className="w-3.5 h-3.5" strokeWidth={1.5} />
        Pause
      </button>
      <button
        className={`flex items-center gap-2 w-full px-3 py-2 text-xs font-medium transition-colors ${
          dark ? "text-red-400 hover:bg-zinc-700" : "text-red-600 hover:bg-red-50"
        }`}
        onClick={(e) => {
          e.stopPropagation();
          onClose();
        }}
      >
        <X className="w-3.5 h-3.5" strokeWidth={1.5} />
        Cancel
      </button>
    </div>
  );
}
```

## Key Elements

### 1. Click-Outside Detection (Use `click`, NOT `mousedown`)

```tsx
// CORRECT - allows stopPropagation on trigger button
document.addEventListener("click", handleClickOutside);

// WRONG - fires before button's onClick, causing double-toggle
document.addEventListener("mousedown", handleClickOutside);
```

**Why?** With `mousedown`, the sequence is:
1. mousedown fires → click-outside closes menu
2. click fires on button → toggle reopens menu

With `click`, `stopPropagation()` on the button prevents the document listener from firing.

### 2. Parent Card Z-Index Elevation

When menu is open, elevate the entire parent card above siblings:

```tsx
<div
  className={`rounded-xl border cursor-pointer relative ${
    menuOpen ? "z-30" : "z-0"
  }`}
>
  {/* card content with dropdown inside */}
</div>
```

**Why?** Each card creates its own stacking context. The dropdown's `z-20` only applies within its card. Sibling cards rendered later in the DOM naturally stack on top.

### 3. Avoid `overflow-hidden` on Dropdown Containers

```tsx
// BAD - clips dropdown regardless of z-index
<div className="rounded-xl overflow-hidden">
  <DropdownMenu />
</div>

// GOOD - only use overflow-hidden where needed (e.g., expandable sections)
<div className="rounded-xl">
  <div className="relative">
    <DropdownMenu />
  </div>
  <div className="overflow-hidden">
    {/* expandable content only */}
  </div>
</div>
```

### 4. Trigger Button with stopPropagation

```tsx
<div className="relative">
  <button
    onClick={(e) => {
      e.stopPropagation(); // Prevents parent card click AND click-outside
      onMenuToggle?.();
    }}
    className="p-1.5 -m-1.5 rounded-lg hover:bg-zinc-100 transition-colors cursor-pointer"
  >
    <MoreVertical className="w-5 h-5 text-zinc-400" strokeWidth={1.5} />
  </button>
  {menuOpen && onMenuClose && <DropdownMenu onClose={onMenuClose} />}
</div>
```

Note the `-m-1.5` negative margin - this increases the clickable area without affecting layout.

## Full Card Example with Dropdown

```tsx
interface CardProps {
  title: string;
  menuOpen?: boolean;
  onMenuToggle?: () => void;
  onMenuClose?: () => void;
}

function Card({ title, menuOpen = false, onMenuToggle, onMenuClose }: CardProps) {
  return (
    <div
      className={`rounded-xl border border-zinc-200 p-4 cursor-pointer relative ${
        menuOpen ? "z-30" : "z-0"
      }`}
      onClick={() => console.log("card clicked")}
    >
      <div className="flex items-center justify-between">
        <span className="font-medium">{title}</span>
        <div className="relative">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onMenuToggle?.();
            }}
            className="p-1.5 -m-1.5 rounded-lg hover:bg-zinc-100 transition-colors"
          >
            <MoreVertical className="w-5 h-5 text-zinc-400" strokeWidth={1.5} />
          </button>
          {menuOpen && onMenuClose && <DropdownMenu onClose={onMenuClose} />}
        </div>
      </div>
    </div>
  );
}

// Parent component managing which menu is open
function CardList() {
  const [openMenu, setOpenMenu] = useState<number | null>(null);
  const items = ["Item 1", "Item 2", "Item 3"];

  return (
    <div className="flex flex-col gap-3">
      {items.map((item, index) => (
        <Card
          key={index}
          title={item}
          menuOpen={openMenu === index}
          onMenuToggle={() => setOpenMenu(openMenu === index ? null : index)}
          onMenuClose={() => setOpenMenu(null)}
        />
      ))}
    </div>
  );
}
```

## Menu Positioning Options

```tsx
// Below, right-aligned (default)
className="absolute right-0 top-full mt-1"

// Below, left-aligned
className="absolute left-0 top-full mt-1"

// Above, right-aligned
className="absolute right-0 bottom-full mb-1"

// Above, left-aligned
className="absolute left-0 bottom-full mb-1"
```

## Related: Tooltips in Stacked Items

When showing tooltips on items that have varying z-indexes (like stacked cards), the tooltip will be trapped in its parent's stacking context. The solution is to render the tooltip **outside** the item loop as a sibling element, calculating its position based on which item is hovered.

See the **stacked-cards** skill for the full pattern.

```tsx
// WRONG - Tooltip trapped in parent's z-index
{items.map((item, i) => (
  <div style={{ zIndex: items.length - i }}>
    <Card />
    {hovered === i && <Tooltip />}  {/* Trapped! */}
  </div>
))}

// CORRECT - Tooltip outside the loop
{items.map((item, i) => (
  <div style={{ zIndex: items.length - i }}>
    <Card />
  </div>
))}
{hovered !== null && (
  <Tooltip style={{ /* calculated position */ }} />
)}
```

## Checklist

- [ ] Click-outside uses `click` event (not `mousedown`)
- [ ] Parent card has conditional `z-30` when menu is open
- [ ] No `overflow-hidden` on containers that hold the dropdown
- [ ] Trigger button has `stopPropagation()` in onClick
- [ ] Menu items have `stopPropagation()` in onClick
- [ ] Trigger wrapper has `relative` positioning
- [ ] Dropdown has `absolute` positioning with `top-full` or `bottom-full`
- [ ] For stacked items, tooltip rendered outside the loop (see stacked-cards skill)
