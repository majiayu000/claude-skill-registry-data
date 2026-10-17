---
name: perfscan
description: "Performance scanner: finds React/Next.js perf issues - key props, effect deps, layout shift, bundle size, client components, render patterns."
trigger: /perfscan
vibe: true
---

# /perfscan

## What this is for

Your app feels slow. Perfscan finds the 7 most common React/Next.js performance issues in 1 minute - prioritized by impact. No profiler needed. Each finding includes impact, diagnosis, and concrete steps to fix.

## Usage

- `/perfscan` - interactive wizard (HIGH first)
- `/perfscan high` - only HIGH impact checks (keyprops + effect + layoutshift)
- `/perfscan quick` - all 7 checks
- `/perfscan keyprops` - single check
- `/perfscan -help` - show full usage and stop

## DIALOG PROTOCOL - STRICT

Follow DIALOG.md. Findings are IMPACT-prioritized: always show HIGH first, then MEDIUM, then LOW.

### Rules

1. Every prompt MUST show numbered options + `[0] Exit`
2. Show impact badge before each finding: `[HOCH]` / `[MITTEL]` / `[NIEDRIG]`
3. Every finding MUST include: **Impact** → **Diagnosis** → **Explanation** (1 sentence) → **Implementation** (1-3 steps)
4. Base options per finding: `[F] Fix` `[S] Skip` `[N] Next` `[0] Exit`
5. Check-specific extras: `[K] Add key=` `[D] Add deps` `[W] Add width/height` `[R] Remove 'use client'`
6. Before any fix: show diff + ask confirmation `[y/n]`

## PROTECTION RULE

Read-only by default. No writes without explicit user consent per operation.

## Checks

### HIGH Impact

### 1. keyprops - Missing key Props

**Script:** `check-keyprops.ps1 -ProjectDir <path>`

`.map()` calls that render JSX without `key=`. Causes full list re-render on every state change.

### 2. useeffect - Broken Effect Dependencies

**Script:** `check-useeffect.ps1 -ProjectDir <path>`

`useEffect` without dependency array (runs every render) or with inline object literals in deps array (breaks referential equality).

### 3. layoutshift - Cumulative Layout Shift

**Script:** `check-layoutshift.ps1 -ProjectDir <path>`

`<img>` without `width`/`height`, `<Image>` without `width`/`height`/`fill`, `<Image fill>` without `sizes`.

### MEDIUM Impact

### 4. images - Unoptimized Images

**Script:** `check-images.ps1 -ProjectDir <path>`

`<img>` used even with `next/image` imported. Large files in `public/` (>200KB).

### 5. client - Unnecessary Client Components

**Script:** `check-client.ps1 -ProjectDir <path>`

`'use client'` directive on components that use no browser APIs, hooks, or event handlers. Can be Server Components.

### 6. bundle - Bundle Size Warnings

**Script:** `check-bundle.ps1 -ProjectDir <path>`

Files with >150 lines, >30 imports, or multiple components without lazy loading.

### LOW Impact

### 7. render - Render Optimization

**Script:** `check-render.ps1 -ProjectDir <path>`

Inline arrow functions as props, inline `style={{}}` objects, `.map()` with inline JSX.

## Confidence Levels

Assign per finding: **proven** (script evidence), **likely** (strong signal, needs review), **suspected** (weak signal).
