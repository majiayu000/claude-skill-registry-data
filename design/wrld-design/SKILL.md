---
name: wrld-design
description: WRLD Inc design system for building UI components with Tailwind CSS and ShadCN. Use when creating React components, designing interfaces, generating CSS, or implementing the WRLD brand design system. Includes color tokens, typography, component patterns, and visual guidelines.
---

# WRLD Design System

A comprehensive design system for WRLD Inc, built for Tailwind CSS and ShadCN component libraries. This skill helps you create consistent, branded UI components following WRLD's modern tech-forward aesthetic.

## Quick Start

When building WRLD-branded components:

1. Use the CSS variables defined in this system
2. Follow the OKLCH color palette for perceptual uniformity
3. Apply sharp corners by default (radius: 0), pill-shaped for primary CTAs
4. Use JetBrains Mono for technical/code content
5. Implement both light and dark mode support

## CSS Foundation

Include this CSS at the root of your project:

```css
@layer base {
  :root {
    --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, monospace;

    --background: oklch(1 0 0);
    --foreground: oklch(0.145 0 0);
    --card: oklch(1 0 0);
    --card-foreground: oklch(0.145 0 0);
    --popover: oklch(1 0 0);
    --popover-foreground: oklch(0.145 0 0);
    --primary: oklch(0.67 0.16 58);
    --primary-foreground: oklch(0.99 0.02 95);
    --secondary: oklch(0.967 0.001 286.375);
    --secondary-foreground: oklch(0.21 0.006 285.885);
    --muted: oklch(0.97 0 0);
    --muted-foreground: oklch(0.556 0 0);
    --accent: oklch(0.67 0.16 58);
    --accent-foreground: oklch(0.99 0.02 95);
    --destructive: oklch(0.58 0.22 27);
    --destructive-foreground: oklch(0.99 0.02 95);
    --border: oklch(0.922 0 0);
    --input: oklch(0.922 0 0);
    --ring: oklch(0.708 0 0);

    --chart-1: oklch(0.88 0.15 92);
    --chart-2: oklch(0.77 0.16 70);
    --chart-3: oklch(0.67 0.16 58);
    --chart-4: oklch(0.56 0.15 49);
    --chart-5: oklch(0.47 0.12 46);

    --radius: 0;

    --sidebar: oklch(0.985 0 0);
    --sidebar-foreground: oklch(0.145 0 0);
    --sidebar-primary: oklch(0.67 0.16 58);
    --sidebar-primary-foreground: oklch(0.99 0.02 95);
    --sidebar-accent: oklch(0.67 0.16 58);
    --sidebar-accent-foreground: oklch(0.99 0.02 95);
    --sidebar-border: oklch(0.922 0 0);
    --sidebar-ring: oklch(0.708 0 0);
  }

  .dark {
    --background: oklch(0.145 0 0);
    --foreground: oklch(0.985 0 0);
    --card: oklch(0.205 0 0);
    --card-foreground: oklch(0.985 0 0);
    --popover: oklch(0.205 0 0);
    --popover-foreground: oklch(0.985 0 0);
    --primary: oklch(0.77 0.16 70);
    --primary-foreground: oklch(0.28 0.07 46);
    --secondary: oklch(0.274 0.006 286.033);
    --secondary-foreground: oklch(0.985 0 0);
    --muted: oklch(0.269 0 0);
    --muted-foreground: oklch(0.708 0 0);
    --accent: oklch(0.77 0.16 70);
    --accent-foreground: oklch(0.28 0.07 46);
    --destructive: oklch(0.704 0.191 22.216);
    --destructive-foreground: oklch(0.99 0.02 95);
    --border: oklch(1 0 0 / 10%);
    --input: oklch(1 0 0 / 15%);
    --ring: oklch(0.556 0 0);

    --sidebar: oklch(0.205 0 0);
    --sidebar-foreground: oklch(0.985 0 0);
    --sidebar-primary: oklch(0.77 0.16 70);
    --sidebar-primary-foreground: oklch(0.28 0.07 46);
    --sidebar-accent: oklch(0.77 0.16 70);
    --sidebar-accent-foreground: oklch(0.28 0.07 46);
    --sidebar-border: oklch(1 0 0 / 10%);
    --sidebar-ring: oklch(0.556 0 0);
  }
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

For detailed component patterns, see [components.md](components.md).
For the complete design reference, see [reference.md](reference.md).
