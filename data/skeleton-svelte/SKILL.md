---
name: skeleton-svelte
description: Use this skill when working with Skeleton UI components in Svelte projects. It provides guidelines for Skeleton's component composition pattern, theme-aware color system, design presets, and layout patterns. Trigger when building UI components, styling elements, creating layouts, or working with Skeleton-specific features in Svelte 5 and SvelteKit 2+ projects.
---

# Skeleton Svelte

## Overview

Skeleton is a design system built on Tailwind CSS that provides framework-specific UI components for Svelte via `@skeletonlabs/skeleton-svelte`. This skill provides workflows and reference documentation for building Svelte applications using Skeleton's component library, color system, and design patterns.

## Core Principles

Apply these fundamental principles when working with Skeleton:

### Component Composition

Use Skeleton's composed pattern with granular child components. Components accept arbitrary props and the `class` attribute for styling:

```svelte
<Card class="preset-filled-surface-100-900">
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Content>
    <p>Content</p>
  </Card.Content>
</Card>
```

### Theme-Aware Colors

**Critical:** Always use color pairings for theme-aware styling. Never hard-code colors with `dark:` prefixes.

✅ Correct:

```svelte
<div class="bg-surface-50-950 text-surface-950-50">
  <p class="text-surface-700-300">Content</p>
</div>
```

❌ Incorrect:

```svelte
<div class="bg-white text-black dark:bg-gray-950 dark:text-white">
  <p class="text-gray-700 dark:text-gray-300">Content</p>
</div>
```

**Color pairing syntax:** `{property}-{color}-{lightShade}-{darkShade}`

Examples:

- `bg-surface-50-950` - Light background in light mode, dark in dark mode
- `text-surface-950-50` - Dark text in light mode, light in dark mode
- `border-surface-300-700` - Adaptive border colors

**Reference:** See `references/colors.md` for comprehensive color system documentation.

### Design Presets

Use built-in presets for consistent styling:

- `preset-filled-{color}-{shade}` - Solid backgrounds with contrast text
- `preset-tonal-{color}` - Soft, tinted backgrounds
- `preset-outlined-{color}-{shade}` - Bordered with transparent background

```svelte
<Button class="preset-filled-primary-500">Primary Action</Button>
<Button class="preset-tonal-secondary">Secondary</Button>
<Button class="preset-outlined-surface-300-700">Cancel</Button>
```

**Reference:** See `references/presets.md` for all preset variants and custom preset creation.

## Workflow: Building UI Components

### Step 1: Identify the Component Type

Determine which Skeleton component best fits the requirement:

- **Avatar** - User profile images with fallback
- **Button** - Interactive actions
- **Card** - Content containers
- **Dialog** - Modal overlays
- **Input/Label** - Form fields
- **Badge** - Status indicators

**Reference:** See `references/components.md` for complete component catalog with examples.

### Step 2: Import and Structure

Import the component and use the composed pattern:

```svelte
<script>
  import { Card, Button } from '@skeletonlabs/skeleton-svelte';
</script>

<Card class="preset-filled-surface-100-900">
  <Card.Header>
    <Card.Title>Component Title</Card.Title>
  </Card.Header>
  <Card.Content>
    <!-- Content here -->
  </Card.Content>
  <Card.Footer>
    <Button class="preset-filled-primary-500">Action</Button>
  </Card.Footer>
</Card>
```

### Step 3: Apply Theme-Aware Styling

Add color pairings and presets using the `class` attribute:

```svelte
<Card class="preset-outlined-surface-300-700">
  <Card.Content>
    <h3 class="font-semibold text-surface-950-50">Heading</h3>
    <p class="text-surface-700-300">Description text</p>
  </Card.Content>
</Card>
```

### Step 4: Add State Management (if needed)

Use Svelte 5 runes for reactive state:

```svelte
<script>
  import { Dialog, Button } from '@skeletonlabs/skeleton-svelte';
  let open = $state(false);
</script>

<Button onclick={() => (open = true)} class="preset-filled-primary-500">Open Dialog</Button>

<Dialog bind:open>
  <Dialog.Content>
    <!-- Dialog content -->
  </Dialog.Content>
</Dialog>
```

## Workflow: Creating Layouts

### Step 1: Choose Layout Pattern

Select an appropriate layout foundation:

- **Single-column** - Blog posts, documentation pages
- **Two-column** - Sidebar + main content
- **Three-column** - Dashboard with dual sidebars
- **Dashboard** - Grid-based card layouts

**Reference:** See `references/layouts.md` for complete layout patterns and examples.

### Step 2: Apply Semantic HTML

Use semantic elements for proper structure:

```svelte
<div class="h-full">
  <header class="sticky top-0 z-10 bg-surface-50-950">
    <nav><!-- Navigation --></nav>
  </header>

  <main class="flex-1 overflow-y-auto">
    <div class="container mx-auto px-4 py-8">
      <!-- Content -->
    </div>
  </main>

  <footer class="bg-surface-100-900">
    <!-- Footer -->
  </footer>
</div>
```

### Step 3: Implement Responsive Behavior

Use Tailwind's responsive prefixes for mobile-first design:

```svelte
<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
  <!-- Responsive grid -->
</div>
```

### Step 4: Add Theme-Aware Styling

Apply color pairings throughout the layout:

```svelte
<header class="border-b border-surface-300-700 bg-surface-50-950">
  <!-- Header content -->
</header>

<main class="bg-surface-100-900">
  <!-- Main content -->
</main>
```

## Common Patterns

### Form with Validation

```svelte
<script>
  import { Button, Input, Label } from '@skeletonlabs/skeleton-svelte';

  let email = $state('');
  let error = $state('');

  function handleSubmit(e) {
    e.preventDefault();
    if (!email.includes('@')) {
      error = 'Invalid email';
      return;
    }
    // Process form
  }
</script>

<form onsubmit={handleSubmit}>
  <div>
    <Label for="email">Email</Label>
    <Input
      id="email"
      type="email"
      bind:value={email}
      class="border-surface-300-700"
      aria-invalid={!!error}
    />
    {#if error}
      <p class="mt-1 text-sm text-error-500">{error}</p>
    {/if}
  </div>
  <Button type="submit" class="mt-4 preset-filled-primary-500">Submit</Button>
</form>
```

### Responsive Card Grid

```svelte
<script>
  import { Card } from '@skeletonlabs/skeleton-svelte';
</script>

<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
  {#each items as item}
    <Card class="preset-filled-surface-100-900">
      <Card.Header>
        <Card.Title>{item.title}</Card.Title>
      </Card.Header>
      <Card.Content>
        <p class="text-surface-700-300">{item.description}</p>
      </Card.Content>
    </Card>
  {/each}
</div>
```

### Status Badge

```svelte
<script>
  import { Badge } from '@skeletonlabs/skeleton-svelte';
</script>

<Badge class="preset-tonal-success">Active</Badge>
<Badge class="preset-tonal-warning">Pending</Badge>
<Badge class="preset-tonal-error">Inactive</Badge>
```

## Project-Specific Configuration

This project uses:

- **Skeleton with Svelte 5** and **SvelteKit 2+**
- **Tailwind CSS 4.x**
- **Mona theme** (configured in `src/app.html`)

The Mona theme provides specific color palettes and design tokens. When creating components, ensure they align with the theme's aesthetic.

## Resources

### Reference Documentation

- `references/colors.md` - Complete color system, pairings, shades, and transparency
- `references/presets.md` - Design presets, variants, and custom preset creation
- `references/layouts.md` - Layout patterns, semantic HTML, responsive design
- `references/components.md` - Comprehensive component catalog with examples

### External Documentation

- Official Documentation: https://www.skeleton.dev
- Component Examples: https://www.skeleton.dev/components
- Theme Generator: https://www.skeleton.dev/themes

## Best Practices

1. **Use color pairings** - Always use dual-tone syntax for theme support
2. **Apply composition pattern** - Leverage child components for flexibility
3. **Semantic HTML** - Use proper HTML elements for accessibility
4. **Mobile-first responsive** - Start with mobile layout, enhance for larger screens
5. **Preset consistency** - Use design presets for uniform styling
6. **State with runes** - Use Svelte 5's `$state`, `$derived`, `$effect` for reactivity
7. **Reference documentation** - Consult references/ files for detailed information

## Important Notes

- Components are built on **Zag.js** for state management
- The design system is **framework agnostic** at its core
- Cannot be used alongside **Flowbite** or **DaisyUI** (conflicting Tailwind modifications)
- Component classes automatically get precedence over internal styles
