---
name: css-inspector
description: Deep CSS analysis tool for understanding specificity, cascade order, inheritance chains, and computed styles. Visualizes CSS complexity and suggests simplifications. Use when debugging specificity issues or understanding CSS behavior.
allowed-tools: Read, Grep, Glob
---

# CSS Inspector Skill

This skill helps you understand how CSS rules interact through the cascade, specificity, and inheritance. I'll analyze your CSS to reveal computed styles, explain why certain rules apply, and suggest simplifications.

## What I Can Analyze

### Specificity Calculations
- Calculate selector specificity
- Compare competing rules
- Identify specificity issues
- Suggest lower-specificity alternatives

### Cascade Analysis
- Show rule application order
- Identify overridden rules
- Explain cascade layers
- Track source order impact

### Inheritance Tracking
- Show inherited properties
- Identify inheritance chains
- Explain computed values
- Detect inheritance issues

### Selector Complexity
- Measure selector depth
- Identify overly specific selectors
- Find redundant selectors
- Suggest simplifications

## Specificity Explained

### Specificity Formula: (a, b, c, d)

- **a**: Inline styles (1,0,0,0)
- **b**: ID selectors (#id)
- **c**: Class selectors (.class), attribute selectors ([attr]), pseudo-classes (:hover)
- **d**: Element selectors (div), pseudo-elements (::before)

### Examples

```css
/* (0,0,0,1) */
div { }

/* (0,0,1,0) */
.button { }

/* (0,0,1,1) */
div.button { }

/* (0,0,2,0) */
.button.primary { }

/* (0,0,2,1) */
nav.button.primary { }

/* (0,1,0,0) */
#header { }

/* (0,1,1,1) */
#header .button { }

/* (0,0,3,0) */
.nav .item .link { }

/* (1,0,0,0) */
<div style="color: red"> /* Inline style */
```

### Specificity Comparison

```css
/* Which rule wins? */

/* (0,0,1,0) - .button */
.button {
  color: blue;
}

/* (0,0,2,0) - .nav .button - WINS */
.nav .button {
  color: red;
}

/* (0,1,0,0) - #header - WINS */
#header {
  color: green;
}

/* !important overrides specificity */
.button {
  color: yellow !important; /* WINS over everything except inline !important */
}
```

## Cascade Order

### Rule Resolution Order (Highest to Lowest)

1. **Inline styles with !important**
   ```html
   <div style="color: red !important">
   ```

2. **Stylesheet rules with !important**
   ```css
   .text { color: blue !important; }
   ```

3. **Inline styles**
   ```html
   <div style="color: green">
   ```

4. **Stylesheet rules** (by specificity)
   ```css
   #id .class element { }
   ```

5. **Browser defaults**

### Same Specificity? Last One Wins

```css
/* Same specificity (0,0,1,0) */
.button {
  color: blue;
}

.button {
  color: red;  /* WINS - appears later */
}
```

### Source Order

```html
<head>
  <style>
    .button { color: blue; }
  </style>
  <link rel="stylesheet" href="styles.css"> <!-- .button { color: red; } -->
  <style>
    .button { color: green; } /* WINS - last in source order */
  </style>
</head>
```

## Cascade Layers

### Layer Priority (Low to High)

```css
/* Define layer order */
@layer reset, base, theme, utilities;

@layer reset {
  * { margin: 0; }
}

@layer base {
  button { padding: 0.5rem; }
}

@layer theme {
  button { padding: 1rem; } /* WINS over base */
}

@layer utilities {
  .p-2 { padding: 0.5rem !important; } /* WINS over everything */
}

/* Unlayered styles have highest priority (except !important) */
button { padding: 2rem; } /* WINS over all layers */
```

## Inheritance

### Properties That Inherit

```css
/* Text properties inherit */
color            /* ✓ Inherits */
font-family      /* ✓ Inherits */
font-size        /* ✓ Inherits */
font-weight      /* ✓ Inherits */
line-height      /* ✓ Inherits */
text-align       /* ✓ Inherits */
text-transform   /* ✓ Inherits */
letter-spacing   /* ✓ Inherits */
word-spacing     /* ✓ Inherits */

/* Most other properties don't inherit */
display          /* ✗ Doesn't inherit */
margin           /* ✗ Doesn't inherit */
padding          /* ✗ Doesn't inherit */
border           /* ✗ Doesn't inherit */
background       /* ✗ Doesn't inherit */
width            /* ✗ Doesn't inherit */
height           /* ✗ Doesn't inherit */
```

### Force Inheritance

```css
/* Force a property to inherit */
.child {
  border: inherit;        /* Inherit from parent */
  color: inherit;         /* Explicitly inherit */
  all: inherit;           /* Inherit all properties */
}

/* Use currentColor for color inheritance */
.icon {
  fill: currentColor;     /* Uses inherited color */
  stroke: currentColor;
}
```

### Inheritance Chain Example

```css
body {
  color: #333;
  font-size: 16px;
}

main {
  /* Inherits color: #333 */
  /* Inherits font-size: 16px */
}

.card {
  font-size: 14px;         /* Overrides inherited 16px */
  /* Still inherits color: #333 */
}

.card-title {
  font-weight: bold;
  /* Inherits font-size: 14px from .card */
  /* Inherits color: #333 from body */
}
```

## Analyzing Specificity Conflicts

### Example Problem

```css
/* Why isn't my button blue? */

.button {
  background: blue;  /* Not working! */
}

/* Other rules in stylesheet: */
nav .menu .button {
  background: red;   /* This wins: (0,0,3,0) > (0,0,1,0) */
}
```

### Solution Analysis

```
Current selector: .button
Specificity: (0,0,1,0)

Conflicting selector: nav .menu .button
Specificity: (0,0,3,0)

Problem: Conflicting selector has higher specificity

Solutions:
1. Increase specificity: nav .menu .button--primary (0,0,4,0)
2. Reduce other selector: .button (refactor nav .menu .button)
3. Use :where(): :where(nav .menu) .button (0,0,1,0)
4. Last resort: !important
```

## Computed Style Analysis

### What Gets Computed?

```css
.element {
  /* Declared values */
  font-size: 1.5em;
  color: inherit;
  width: auto;

  /* Computed values (depends on context): */
  /* font-size: 24px (if parent is 16px) */
  /* color: #333 (if parent color is #333) */
  /* width: 800px (if content requires 800px) */
}
```

### Relative Units Resolution

```css
html {
  font-size: 16px;
}

.parent {
  font-size: 1.5rem;    /* Computed: 24px */
}

.child {
  font-size: 2em;       /* Computed: 48px (2 × parent's 24px) */
  padding: 1em;         /* Computed: 48px (1 × element's 48px) */
  margin: 1rem;         /* Computed: 16px (1 × root's 16px) */
}
```

## Selector Complexity Analysis

### Overly Complex Selectors

```css
/* ❌ Too complex (specificity: 0,1,3,3) */
#sidebar nav.primary ul.menu li.item a.link {
  color: blue;
}

/* Problems:
 * - Very high specificity (0,1,3,3)
 * - Hard to override
 * - Fragile (breaks if HTML structure changes)
 * - Slower selector matching
 */

/* ✓ Simplified (specificity: 0,0,1,0) */
.nav-link {
  color: blue;
}

/* Benefits:
 * - Low specificity
 * - Easy to override
 * - Structural independence
 * - Faster matching
 */
```

### Redundant Selectors

```css
/* ❌ Redundant tag selector */
div.container { }      /* Tag adds nothing useful */
span.text { }

/* ✓ Class alone is sufficient */
.container { }
.text { }

/* ❌ Redundant nesting */
.card .card-header .card-title { }

/* ✓ Flat BEM structure */
.card__title { }
```

## Inspector Tools

### Browser DevTools

**Chrome/Edge DevTools:**
```
1. Inspect element
2. Styles tab shows:
   - Applied rules (from highest to lowest specificity)
   - Crossed-out rules (overridden)
   - Computed values
   - Specificity on hover

3. Computed tab shows:
   - Final computed values
   - Which rule each property came from
```

**Firefox DevTools:**
```
- Shows specificity values inline
- Rule source (file and line number)
- Excellent Grid/Flexbox inspectors
- Override tracking
```

### Specificity Calculator

```
Input: #header .nav .item a:hover

Breakdown:
- IDs: 1 (#header)
- Classes: 3 (.nav, .item, :hover)
- Elements: 1 (a)

Specificity: (0,1,3,1) or "0,1,3,1"
Decimal: 0131 (for comparison)
```

## Common Specificity Issues

### Issue 1: !important Wars

```css
/* ❌ !important cascade */
.button {
  color: blue !important;
}

.button-primary {
  color: red !important;   /* Must use !important to override */
}

/* ✓ Fix: Remove !important, use specificity */
.button {
  color: blue;
}

.button--primary {
  color: red;  /* Overrides with higher specificity */
}
```

### Issue 2: ID Over-specificity

```css
/* ❌ ID selector too specific */
#header .button {
  background: blue;
}

/* Very hard to override */
.button--primary {
  background: red;  /* Doesn't work! */
}

/* ✓ Fix: Use classes */
.header .button {
  background: blue;
}

.button--primary {
  background: red;  /* Works! */
}
```

### Issue 3: Deep Nesting

```css
/* ❌ Deep nesting */
.container .row .col .card .header .title {
  font-size: 1.5rem;
}

/* ✓ Fix: Use flat BEM */
.card__title {
  font-size: 1.5rem;
}
```

## Debugging Workflow

### Step 1: Identify Applied Rules

```css
/* In DevTools, see which rules apply */
.element {
  color: blue;  /* ✓ Applied */
}

.element {
  color: red;   /* ✗ Overridden (crossed out) */
}
```

### Step 2: Check Specificity

```
Hover over selector in DevTools to see specificity:

.button              → (0,0,1,0)
nav .button          → (0,0,1,1)
#header .button      → (0,1,1,0) ← Highest, wins
```

### Step 3: Trace Inheritance

```css
/* Check Computed tab */
body {
  color: #333;  /* Inherited by all descendants */
}

.card {
  /* color: #333 (inherited from body) */
}

.card-title {
  color: #000;  /* Overrides inherited color */
}
```

### Step 4: Identify Solution

```
Solutions ordered by preference:

1. Increase specificity of target rule
2. Decrease specificity of conflicting rule
3. Use :where() for zero specificity
4. Adjust source order
5. Use !important (last resort)
```

## Specificity Best Practices

### ✓ Good Practices
- Keep specificity low and consistent
- Use single classes when possible
- Avoid IDs for styling
- Use BEM or similar methodology
- Use :where() for low-specificity utilities
- Document intentional high specificity

### ❌ Bad Practices
- Using !important to fix specificity
- Chaining multiple classes (.btn.btn-primary.btn-large)
- Deep nesting (.a .b .c .d .e)
- Mixing IDs and classes
- Inconsistent specificity levels

## Example Analysis

**You provide:**
```css
.container .card .title {
  font-size: 1.5rem;
  color: blue;
}

#featured .title {
  color: red;
}

.title.large {
  font-size: 2rem;
}
```

**I'll analyze:**
```
Specificity Analysis:

1. .container .card .title
   Specificity: (0,0,3,0)
   Properties: font-size, color

2. #featured .title
   Specificity: (0,1,1,0) ← HIGHEST
   Properties: color
   Overrides: .container .card .title color

3. .title.large
   Specificity: (0,0,2,0)
   Properties: font-size
   Doesn't override: .container .card .title font-size (lower specificity)

Final computed styles for <h2 class="title large"> inside .container .card:
- font-size: 1.5rem (from .container .card .title)
- color: blue (from .container .card .title)

Final computed styles for <h2 class="title large"> inside #featured:
- font-size: 1.5rem (from .container .card .title OR inherited)
- color: red (from #featured .title)

Recommendations:
1. Remove ID selector #featured, use .featured class
2. Flatten .container .card .title to .card__title
3. Use .title--large instead of .title.large for clarity
```

## Just Ask!

Request CSS analysis:
- "Calculate specificity for #nav .menu .item"
- "Why isn't this CSS rule applying?"
- "Explain the cascade for this element"
- "Analyze these conflicting rules"
- "Show me the computed styles"

I'll explain how CSS rules interact!
