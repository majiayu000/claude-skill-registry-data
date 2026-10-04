---
name: ui
description: User interface design and implementation
license: MIT
metadata:
  audience: developers
  category: design
---

## What I do
- Design visual interfaces for applications
- Create component hierarchies and layouts
- Implement responsive designs
- Apply design systems and patterns
- Handle typography, color, and spacing
- Build interactive UI components

## When to use me
When building user-facing interfaces for web, mobile, or desktop applications.

## Key Concepts

### Layout Techniques
```css
/* Flexbox */
display: flex;
justify-content: space-between;
align-items: center;

/* Grid */
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 1rem;
```

### Component Patterns
- Atomic design (atoms, molecules, organisms)
- Container/presenter pattern
- Higher-order components
- Compound components

### Responsive Design
```css
/* Mobile-first approach */
.container {
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### Design Systems
- Define typography scale
- Establish color palettes
- Create spacing tokens
- Build component library
- Document usage guidelines
