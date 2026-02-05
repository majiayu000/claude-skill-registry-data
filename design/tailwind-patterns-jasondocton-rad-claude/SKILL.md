---
name: tailwind-patterns
description: Efficient Tailwind CSS patterns using inheritance and custom config
---

# Tailwind Patterns

**Purpose**: Efficient Tailwind CSS (inheritance, minimal wrappers, custom config)

- Keywords: tailwind, styling, css, className, responsive, tw, tailwindcss

## Quick Reference

| Principle | ✅ DO | ❌ AVOID |
|-----------|-------|----------|
| Inheritance | Set at highest level | Repeat inherited styles |
| Elements | Merge classes | Wrapper divs for styling only |
| Colors | Custom config only | Default Tailwind palette |
| Utilities | Only when changing | Redundant classes |

**Custom colors**: `primary`, `secondary`, `tertiary`, `quaternary`, `accent`, `background`

## Set Styles at Highest Level

```tsx
// ✅ Set once, inherits
export function App() {
  return (
    <body className="text-secondary bg-background font-sans">
      <Header />
      <Main />
    </body>
  )
}

// ❌ Repeating inherited
export function Header() {
  return (
    <header className="text-secondary font-sans"> {/* Already inherited */}
      <h1 className="text-secondary">Title</h1>
    </header>
  )
}
```

## Only Override When Changing

```tsx
// ✅ Only add utilities that CHANGE
export function Card() {
  return (
    <div className="bg-primary text-background p-4">
      <h2 className="text-xl font-bold">Title</h2>
      <p>Body inherits text-background</p>
    </div>
  )
}

// ❌ Re-applying inherited
<div className="bg-primary text-background p-4">
  <h2 className="text-background text-xl">Title</h2> {/* Redundant */}
</div>
```

## Merge Classes, Not Wrappers

```tsx
// ✅ Single element
export function Button({ children }: { children: ReactNode }) {
  return (
    <button className="bg-primary text-background px-4 py-2 rounded">
      {children}
    </button>
  )
}

// ❌ Wrapper div for styling
export function Button({ children }: { children: ReactNode }) {
  return (
    <div className="bg-primary rounded">
      <button className="text-background px-4 py-2">{children}</button>
    </div>
  )
}
```

## Before Adding Class

1. **Already inherited?** Check parents
2. **Can apply to parent?** Reduce duplication
3. **Wrapper necessary?** Or merge into one element?
4. **Color exists in config?** Only use configured colors

## Custom Colors (Default Palette Removed)

```tsx
// ✅ Using custom config
<div className="bg-primary text-background">
  <p className="text-secondary">Text</p>
  <span className="text-accent">Accent</span>
</div>

// ❌ Default Tailwind (not in config)
<div className="bg-blue-500 text-white">
  <p className="text-gray-600">Text</p>
</div>
```

## Why This Matters

1. **Smaller bundles**: Fewer utilities = smaller CSS
2. **Cleaner DOM**: Fewer wrappers = better performance
3. **Single source**: Styles set once, inherited
4. **Easier refactoring**: Change once at root
5. **Consistent design**: Limited palette enforces system

## Responsive

```tsx
<div className="p-4 md:p-6 lg:p-8">
  <h1 className="text-2xl md:text-3xl lg:text-4xl">Title</h1>
</div>
```

## Conditional Styling

```tsx
export function Button({ variant }: { variant: "primary" | "secondary" }) {
  return (
    <button
      className={
        variant === "primary"
          ? "bg-primary text-background"
          : "bg-secondary text-primary"
      }
    >
      Click me
    </button>
  )
}
```
