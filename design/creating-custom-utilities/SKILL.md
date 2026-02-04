---
name: creating-custom-utilities
description: Create custom utilities with @utility directive supporting static utilities, functional utilities with values, theme-based utilities, and multi-value utilities. Use when extending Tailwind with custom CSS properties or patterns.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Creating Custom Utilities

## Purpose

The `@utility` directive creates custom utility classes with full variant support (hover, focus, responsive, etc.). This is the proper way to extend Tailwind v4 with custom utilities.

## Static Utilities

Define utilities with fixed values:

```css
@utility content-auto {
  content-visibility: auto;
}

@utility content-hidden {
  content-visibility: hidden;
}

@utility text-balance {
  text-wrap: balance;
}

@utility text-pretty {
  text-wrap: pretty;
}

@utility bg-glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
```

**Usage:**

```html
<div class="content-auto hover:content-hidden"></div>
<p class="text-balance lg:text-pretty"></p>
<div class="bg-glass"></div>
```

Static utilities work with all variants automatically.

## Functional Utilities with Integer Values

Create utilities that accept numeric values:

```css
@utility mt-* {
  margin-top: calc(0.25rem * --value(integer));
}

@utility truncate-* {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: --value(integer);
  overflow: hidden;
}

@utility text-stroke-* {
  -webkit-text-stroke-width: --value(integer) px;
}
```

**Usage:**

```html
<div class="mt-5"></div>
<p class="truncate-3"></p>
<h1 class="text-stroke-2"></h1>
```

The `--value(integer)` function extracts the numeric value from the class name.

## Theme-Based Utilities

Reference theme variables using `--value(--namespace- *)`:

```css
@theme {
  --tab-size-2: 2;
  --tab-size-4: 4;
  --tab-size-8: 8;
  --tab-size-github: 8;
}

@utility tab-* {
  tab-size: --value(--tab-size- *);
}
```

**Usage:**

```html
<pre class="tab-2"><code>...</code></pre>
<pre class="tab-github"><code>...</code></pre>
```

**Another example:**

```css
@theme {
  --aspect-square: 1 / 1;
  --aspect-video: 16 / 9;
  --aspect-portrait: 3 / 4;
}

@utility aspect-* {
  aspect-ratio: --value(--aspect- *);
}
```

**Usage:**

```html
<img class="aspect-square" />
<video class="aspect-video" />
<div class="aspect-portrait"></div>
```

## Multi-Value Utilities

Create utilities that accept multiple value types:

```css
@utility text-stroke-* {
  -webkit-text-stroke-width: --value(integer) px;
  -webkit-text-stroke-color: --value(--color- *);
}
```

**Usage:**

```html
<h1 class="text-stroke-2-blue-500">Stroked text</h1>
<h1 class="text-stroke-1-primary">Stroked with theme color</h1>
```

**Another example:**

```css
@theme {
  --blur-sm: 4px;
  --blur-md: 8px;
  --blur-lg: 16px;
}

@utility backdrop-blur-* {
  backdrop-filter: blur(--value(--blur- *));
  backdrop-filter: blur(--value(integer) px);
}
```

**Usage:**

```html
<div class="backdrop-blur-sm"></div>
<div class="backdrop-blur-12"></div>
```

## Arbitrary Values Support

Support both theme values and arbitrary values:

```css
@utility tab-* {
  tab-size: --value(integer);
  tab-size: --value([integer]);
}
```

**Usage:**

```html
<pre class="tab-4">Theme value</pre>
<pre class="tab-[12]">Arbitrary value</pre>
```

The `--value([integer])` function enables arbitrary value syntax with square brackets.

## Complex Utility Examples

### Gradient Text

```css
@utility text-gradient-* {
  background: linear-gradient(to right, --value(--color- *), --value(--color- *, 2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

**Usage:**

```html
<h1 class="text-gradient-blue-500-purple-600">Gradient text</h1>
```

### Grid Template Columns

```css
@utility grid-cols-* {
  grid-template-columns: repeat(--value(integer), minmax(0, 1fr));
}
```

**Usage:**

```html
<div class="grid grid-cols-3"></div>
<div class="grid grid-cols-5"></div>
```

### Custom Line Clamp

```css
@utility line-clamp-* {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: --value(integer);
  overflow: hidden;
}

@utility line-clamp-none {
  display: block;
  -webkit-box-orient: horizontal;
  -webkit-line-clamp: none;
  overflow: visible;
}
```

**Usage:**

```html
<p class="line-clamp-2 lg:line-clamp-3 xl:line-clamp-none"></p>
```

### Custom Spacing Scale

```css
@theme {
  --spacing-base: 0.25rem;
}

@utility gap-* {
  gap: calc(var(--spacing-base) * --value(integer));
}

@utility space-x-* > * + * {
  margin-left: calc(var(--spacing-base) * --value(integer));
}
```

**Usage:**

```html
<div class="flex gap-6"></div>
<div class="flex space-x-4"></div>
```

### Glassmorphism Utilities

```css
@utility glass-* {
  background: rgba(255, 255, 255, --value(integer) / 100);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@utility glass-dark-* {
  background: rgba(0, 0, 0, --value(integer) / 100);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

**Usage:**

```html
<div class="glass-10"></div>
<div class="glass-dark-20"></div>
```

## Utilities with Pseudo-Elements

```css
@utility before-content-* {
  &::before {
    content: --value([string]);
    display: block;
  }
}

@utility after-content-* {
  &::after {
    content: --value([string]);
    display: block;
  }
}
```

**Usage:**

```html
<div class="before:content-['★']">Star before</div>
<div class="after:content-['→']">Arrow after</div>
```

## Complete Custom Utilities Library

```css
@import 'tailwindcss';

@utility content-auto {
  content-visibility: auto;
}

@utility content-hidden {
  content-visibility: hidden;
}

@utility text-balance {
  text-wrap: balance;
}

@utility text-pretty {
  text-wrap: pretty;
}

@utility truncate-* {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: --value(integer);
  overflow: hidden;
}

@utility bg-glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

@utility text-stroke-* {
  -webkit-text-stroke-width: --value(integer) px;
  -webkit-text-stroke-color: --value(--color- *);
}

@theme {
  --aspect-square: 1 / 1;
  --aspect-video: 16 / 9;
  --aspect-portrait: 3 / 4;
  --aspect-ultrawide: 21 / 9;
}

@utility aspect-* {
  aspect-ratio: --value(--aspect- *);
  aspect-ratio: --value([number]);
}

@theme {
  --tab-size-2: 2;
  --tab-size-4: 4;
  --tab-size-8: 8;
}

@utility tab-* {
  tab-size: --value(--tab-size- *);
  tab-size: --value(integer);
  tab-size: --value([integer]);
}
```

## Why Use @utility Instead of @layer utilities

**Don't do this:**

```css
@layer utilities {
  .my-button {
    padding: 1rem;
  }
}
```

Won't work with variants like `hover:my-button`.

**Do this:**

```css
@utility my-button {
  padding: 1rem;
}
```

Works with all variants: `hover:my-button`, `focus:my-button`, `lg:my-button`.

## Best Practices

1. **Use @utility for variant support** - Always use `@utility` instead of `@layer utilities`
2. **Support arbitrary values** - Include `--value([type])` for flexibility
3. **Use theme variables** - Reference theme with `--value(--namespace- *)`
4. **Name utilities semantically** - Use clear, descriptive names
5. **Group related utilities** - Keep similar utilities together

## Common Use Cases

- Custom CSS properties not in Tailwind
- Browser-specific prefixed properties
- Complex multi-property patterns
- Domain-specific utilities (e.g., print styles)
- Experimental CSS features

## See Also

- RESEARCH.md section: "Advanced Patterns" → "Custom Utilities with @utility"
