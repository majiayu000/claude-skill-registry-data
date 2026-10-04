---
name: css
description: CSS styling for web pages including selectors, flexbox, grid, and animations
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: web-development
---
## What I do
- Style web pages with CSS
- Use flexbox and grid layouts
- Create responsive designs
- Implement animations and transitions
- Use CSS custom properties (variables)
- Handle pseudo-classes and pseudo-elements
- Optimize CSS for performance

## When to use me
When styling web pages or building UI components.

## Selectors
```css
/* Basic */
p { color: blue; }
.class { font-size: 16px; }
#id { margin: 0; }

/* Combinators */
div p { }     /* descendant */
div > p { }   /* child */
p + p { }     /* adjacent sibling */
p ~ p { }     /* general sibling */

/* Pseudo-classes */
:hover :focus :active :visited
:first-child :last-child :nth-child(2n)
:not(.active) :checked :disabled

/* Pseudo-elements */
::before ::after ::first-letter ::first-line ::selection
```

## Flexbox
```css
.container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.item {
  flex: 1 1 auto;
  order: 1;
  align-self: center;
}
```

## Grid
```css
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto;
  gap: 1rem;
}

.item {
  grid-column: 1 / 3;
  grid-row: 1 / 2;
}
```

## Variables
```css
:root {
  --primary: #007bff;
  --spacing: 1rem;
}

.button {
  background: var(--primary);
  padding: var(--spacing);
}
```

## Animations
```css
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

.element {
  animation: slideIn 0.3s ease-in-out;
  transition: all 0.2s ease;
}
```
