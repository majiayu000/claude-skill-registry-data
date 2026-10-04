---
name: ecc-hydration-performance
description: Hydration Safety & Font Performance. Use when configuring web typography, preloading font files above the fold, designing fallback overrides to prevent Cumulative Layout Shift, or optimizing Next.js App Router server component hydration issues.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# Hydration Safety & Font Performance

## Purpose
Enforce optimized font loading, CLS metrics matching, fluid typography clamp constraints, and Next.js App Router server-side hydration security guidelines.

## When to Use This Skill
- Declaring custom web fonts with CSS overrides to match local system font fallbacks.
- Setting up preloading strategies for above-the-fold display and body text fonts.
- Implementing responsive font scales using clamp values.
- Resolving React/Next.js dynamic client rendering mismatches (window properties, innerWidth, localStorage).

## Output Format / Delivery
Provide highly optimized, fluid, and hydration-secure CSS rules and React layout components. Render deterministic skeletons or static fallbacks during SSR loading.

## Behavior Rules
1. **Never read window, document, or localStorage values during the initial React render loop** — gate all client-only logic behind an layout effect sync hook.
2. **Never allow above-the-fold font loading to trigger layout shifts** — match the metrics of fallback system fonts concurrently using Fontaine overrides (`size-adjust`, `ascent-override`).
3. **Never apply fluid responsive typography scaling in telemetry panels, grids, or dashboards** — keep spatial layout layouts strictly fixed.
4. **Never preload secondary font weights or italic styles above the fold**.

## Maintenance Notes
This skill is locked for web font performance and Next.js server rendering safety. Update if Next.js hydration error reporting or Fontaine specifications evolve.

---

## Phase 1: Web Font Fallback Overrides (CLS Elimination)

To prevent Cumulative Layout Shift (CLS) during web font loading, match the metrics of local fallback system fonts (e.g. Arial or Times New Roman) to your custom web font. Use standard Fontaine metric-matching overrides:

```css
/* 1. Standard web font declaration with swap display */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom-font.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

/* 2. Overridden fallback matching the custom font's x-height and ascent/descent */
@font-face {
  font-family: 'CustomFont-Fallback';
  src: local('Arial');
  size-adjust: 106%;            /* Scale glyph size to match web font x-height */
  ascent-override: 92%;         /* Match ascender height bounds */
  descent-override: 22%;        /* Match descender depth bounds */
  line-gap-override: 8%;        /* Match line gap spacing */
}

/* 3. Assign stack with matched fallback */
body {
  font-family: 'CustomFont', 'CustomFont-Fallback', sans-serif;
}
```

### Preloading Strategy
* Preload ONLY the primary normal-weight body font used above the fold. 
* Do NOT preload secondary weights or italics.

---

## Phase 2: Fluid Typography Scaling Equations

When implementing responsive typography, follow these mathematical scaling laws:

1. **Fluid Sizing Bounds**: Headings and display text may utilize responsive viewport units bounded by `clamp(min, preferred, max)`:
   * **Rule of 2.5**: The maximum font size MUST be $\leq 2.5 \times$ the minimum size:
     $$\text{max-size} \le 2.5 \times \text{min-size}$$
     Exceeding this ratio breaks browser accessibility zoom, layout reflow, and makes high-resolution viewports unreadably large.
2. **Fixed-Size Exclusions**: App UIs, dashboards, data grids, navigation elements, and all body text MUST use fixed `rem` scales. Fluid viewport-based typography is forbidden in telemetry/dashboard panels to maintain absolute spatial predictability.
3. **Container-Measure Balance**: Ensure that the effective line character measure (`max-width: 65ch`) and responsive font size scale in tandem to prevent text from stretching too wide at high resolutions.

---

## Phase 3: Next.js App Router Hydration-Safety Rules

To avoid rendering mismatches and standard App Router hydration errors, enforce the following pre-flight rules:

* **Hydration Protection Guard**: Never read environment variables, local storage, or window properties (e.g. `window.innerWidth`, `localStorage.getItem`, `new Date()`) directly during the initial React render loop. This causes immediate client/server hydration errors. 
* **Stateful Sync Pattern**: Gate all client-only execution behind a `useEffect` layout sync hook:

```tsx
"use client";
import { useState, useEffect } from "react";

export function ClientOnlyComponent() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div class="w-full h-24 animate-pulse bg-zinc-900 rounded-lg"></div>; // Deterministic skeletal placeholder
  }

  return (
    <div>
      {/* Stateful Client-Only UI Elements */}
    </div>
  );
}
```

* **Provider Isolation**: Global state contexts, themes, or Zustand provider wrappers must be isolated in a dedicated Client Component (`"use client"`). Never wrap layout pages or top-level layout trees in global providers directly.
* **Layout Shift Prevention**: All React `<Suspense>` boundaries must have a `<Skeleton>` fallback with deterministic height and width bounds.
