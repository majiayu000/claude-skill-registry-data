---
name: component-variants
description: Creates light and dark mode component variants with consistent color token mapping. Use when building dual-theme components, creating light/dark UI pairs, or implementing theme-aware designs.
---

# Component Variants Pattern

Create matching light and dark variants of UI components using a systematic color token approach.

## Pattern Overview

1. Create paired components: `ComponentLight` and `ComponentDark`
2. Mirror the structure exactly between variants
3. Map colors systematically using the token table below
4. Export a unified component that renders both or accepts a `variant` prop

## Color Token Mapping

### Basic Tokens

| Semantic Use | Light Mode | Dark Mode |
|-------------|------------|-----------|
| Card background | `bg-[#f8f8f8]` | `bg-zinc-800` |
| Card border | `border-zinc-200/80` | `border-zinc-700/80` |
| Content area | `bg-white` | `bg-zinc-900` |
| Primary text | `text-zinc-900` | `text-zinc-100` |
| Secondary text | `text-zinc-600` | `text-zinc-400` |
| Muted text | `text-zinc-500` | `text-zinc-500` |
| Icon color | `text-zinc-400` | `text-zinc-500` |
| Tag background | `bg-zinc-100` | `bg-zinc-800 border border-zinc-700` |
| Tag text | `text-zinc-600` | `text-zinc-400` |
| Accent background | `bg-green-50` | `bg-green-900/50` |
| Accent text | `text-green-700` | `text-green-400` |
| Shadow | `shadow-zinc-200/50` | `shadow-black/30` |
| Hover background | `hover:bg-zinc-100/50` | `hover:bg-zinc-700/30` |

### Gradient & Nested Card Tokens

| Semantic Use | Light Mode | Dark Mode |
|-------------|------------|-----------|
| Outer card gradient | `bg-gradient-to-b from-[#e8e8ea] to-[#dcdce0]` | `bg-gradient-to-b from-zinc-700 to-zinc-800` |
| Outer card border | `border-white/60` | `border-zinc-600/40` |
| Outer card shadow | `shadow-xl shadow-zinc-400/30` | `shadow-xl shadow-black/50` |
| Inner media border | `border-white/40` | `border-zinc-600/30` |

### Badge Tokens

| Semantic Use | Light Mode | Dark Mode |
|-------------|------------|-----------|
| Success badge bg | `bg-[#d4f5d4]` | `bg-emerald-900/40` |
| Success badge text | `text-zinc-700` | `text-emerald-400` |

### Separator Tokens

| Semantic Use | Light Mode | Dark Mode |
|-------------|------------|-----------|
| Dot separator | `text-zinc-300` | `text-zinc-600` |
| Border separator | `border-zinc-300` | `border-zinc-700` |

## Implementation Template

```tsx
// 1. Create the Light variant
function ComponentLight() {
  return (
    <div className="bg-[#f8f8f8] rounded-xl border border-zinc-200/80 shadow-lg shadow-zinc-200/50">
      <div className="bg-white px-4 py-4">
        <span className="text-zinc-900">Primary content</span>
        <span className="text-zinc-500">Secondary content</span>
      </div>
    </div>
  );
}

// 2. Create the Dark variant (mirror structure, swap tokens)
function ComponentDark() {
  return (
    <div className="bg-zinc-800 rounded-xl border border-zinc-700/80 shadow-lg shadow-black/30">
      <div className="bg-zinc-900 px-4 py-4">
        <span className="text-zinc-100">Primary content</span>
        <span className="text-zinc-500">Secondary content</span>
      </div>
    </div>
  );
}

// 3. Export unified component
export function Component({ variant = "light" }: { variant?: "light" | "dark" }) {
  return variant === "dark" ? <ComponentDark /> : <ComponentLight />;
}
```

## Helper Components Pattern

When components have repeated sub-elements, create paired helpers:

```tsx
interface InfoRowProps {
  icon: React.ReactNode;
  label: string;
  value: React.ReactNode;
}

function InfoRowLight({ icon, label, value }: InfoRowProps) {
  return (
    <div className="flex items-center gap-3 py-1">
      <span className="text-zinc-400">{icon}</span>
      <span className="text-zinc-500 text-sm w-32">{label}</span>
      <div className="flex-1">{value}</div>
    </div>
  );
}

function InfoRowDark({ icon, label, value }: InfoRowProps) {
  return (
    <div className="flex items-center gap-3 py-1">
      <span className="text-zinc-500">{icon}</span>
      <span className="text-zinc-500 text-sm w-32">{label}</span>
      <div className="flex-1">{value}</div>
    </div>
  );
}
```

## Checklist

- [ ] Light and dark variants have identical structure
- [ ] All color classes mapped according to token table
- [ ] Text contrast meets accessibility guidelines
- [ ] Shadows appropriate for each theme
- [ ] Hover/focus states defined for both themes
