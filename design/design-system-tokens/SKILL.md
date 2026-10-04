---
name: design-system-tokens
description: Use this skill whenever writing any UI component, page layout, CSS, style declaration, or frontend code in the Myelin platform. This defines the tokenized design variables, component library rules, theme mapping, routing conventions, accessibility baseline, and the fixes required for known prototype inconsistencies. Do not hardcode colors, spacing, or typography values. Load this skill before writing any HTML, CSS, or frontend JavaScript.
---

This skill is the design system and frontend contract for the Myelin platform. Every UI surface — learner app, lecturer console, admin panel, simulation shell, and demo path — must be built from these tokens and component rules. Consistency across sessions depends on Codex always reading this file first.

---

## Design Language

Myelin is a professional, high-stakes training platform for engineering trades. The visual direction is:
- Industrial precision: clean geometry, high contrast, purposeful density
- Dark-first: the primary experience is a dark theme; light theme is a supported alternative
- Trust-signalling: evidence of rigour — clear status indicators, precise labels, structured layouts
- No decorative noise: every visual element serves a function

The simulation environment demands a UI that recedes and lets the 3D scene lead. The learner app and admin console are structured and data-dense without being cluttered.

---

## Color Tokens

Define as CSS custom properties on `:root`. All component code must use these tokens — never hardcoded hex values.

```css
:root {
  /* Brand */
  --color-brand-primary: #1A6B4A;       /* Myelin green — primary actions */
  --color-brand-primary-hover: #145839;
  --color-brand-accent: #2ECFA0;        /* Bright teal — highlights, progress */

  /* Backgrounds */
  --color-bg-base: #0F1117;             /* Page background (dark theme) */
  --color-bg-surface: #171B24;          /* Card, panel surface */
  --color-bg-elevated: #1E2330;         /* Elevated surface, modal, dropdown */
  --color-bg-overlay: rgba(0,0,0,0.6);  /* Modal backdrop */

  /* Text */
  --color-text-primary: #F0F2F5;
  --color-text-secondary: #A8B0C0;
  --color-text-muted: #5C6478;
  --color-text-inverse: #0F1117;        /* Text on light surfaces */
  --color-text-link: #2ECFA0;
  --color-text-link-hover: #5BDCB8;

  /* Borders */
  --color-border-default: rgba(255,255,255,0.08);
  --color-border-strong: rgba(255,255,255,0.16);
  --color-border-focus: #2ECFA0;

  /* Status */
  --color-status-success: #1D9E75;
  --color-status-success-bg: rgba(29,158,117,0.12);
  --color-status-warning: #D4903A;
  --color-status-warning-bg: rgba(212,144,58,0.12);
  --color-status-danger: #D85A4A;
  --color-status-danger-bg: rgba(216,90,74,0.12);
  --color-status-info: #3A8FD8;
  --color-status-info-bg: rgba(58,143,216,0.12);

  /* Simulation-specific */
  --color-sim-step-locked: #2A2E3A;
  --color-sim-step-unlocked: #1E2A3A;
  --color-sim-step-active: #163A2A;
  --color-sim-step-passed: #0F2A1E;
  --color-sim-step-failed: #2A1618;
  --color-sim-hud-bg: rgba(15,17,23,0.85);
  --color-sim-hud-border: rgba(46,207,160,0.2);

  /* Spacing scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* Radii */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-pill: 9999px;

  /* Elevation (box shadows) */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.5);
  --shadow-focus: 0 0 0 2px var(--color-border-focus);

  /* Motion */
  --duration-fast: 100ms;
  --duration-base: 200ms;
  --duration-slow: 300ms;
  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
  --easing-enter: cubic-bezier(0, 0, 0.2, 1);
  --easing-exit: cubic-bezier(0.4, 0, 1, 1);
}
```

### Light theme overrides

```css
[data-theme="light"] {
  --color-bg-base: #F5F6F8;
  --color-bg-surface: #FFFFFF;
  --color-bg-elevated: #F0F2F5;
  --color-text-primary: #0F1117;
  --color-text-secondary: #4A5568;
  --color-text-muted: #9AA3B2;
  --color-text-inverse: #F0F2F5;
  --color-border-default: rgba(0,0,0,0.08);
  --color-border-strong: rgba(0,0,0,0.16);
  --color-sim-hud-bg: rgba(255,255,255,0.92);
}
```

Apply theme by setting `data-theme` on `<html>`. Default is dark. User preference is persisted in their profile settings. Theme key for local fallback storage: `myelin-theme` (not `theme` — fix the prototype inconsistency).

---

## Typography Tokens

```css
:root {
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-xs:   11px;
  --text-sm:   13px;
  --text-base: 15px;
  --text-md:   17px;
  --text-lg:   20px;
  --text-xl:   24px;
  --text-2xl:  30px;
  --text-3xl:  36px;

  --weight-regular: 400;
  --weight-medium:  500;
  --weight-semibold: 600;

  --leading-tight:  1.25;
  --leading-base:   1.5;
  --leading-loose:  1.75;
}
```

Typography scale usage:
- Page titles: `--text-2xl`, `--weight-semibold`
- Section headings: `--text-lg`, `--weight-medium`
- Body text: `--text-base`, `--weight-regular`, `--leading-base`
- Labels and metadata: `--text-sm`, `--weight-regular`, `--color-text-secondary`
- Monospace (code, IDs, step labels): `--font-mono`, `--text-sm`
- Simulation HUD text: `--text-sm`, `--weight-medium`, `--font-mono` for values

---

## Component Library Rules

### Buttons

Three variants. Use the correct variant for the context — do not invent new button styles.

```css
/* Primary — main action per view */
.btn-primary {
  background: var(--color-brand-primary);
  color: #ffffff;
  border: none;
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-5);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background var(--duration-base) var(--easing-default);
}
.btn-primary:hover { background: var(--color-brand-primary-hover); }
.btn-primary:focus-visible { outline: none; box-shadow: var(--shadow-focus); }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }

/* Secondary — supporting action */
.btn-secondary {
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-5);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: border-color var(--duration-base) var(--easing-default),
              background var(--duration-base) var(--easing-default);
}
.btn-secondary:hover { background: var(--color-bg-elevated); border-color: var(--color-border-focus); }
.btn-secondary:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

/* Destructive — irreversible actions only */
.btn-danger {
  background: var(--color-status-danger);
  color: #ffffff;
  border: none;
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-5);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  cursor: pointer;
}
.btn-danger:hover { opacity: 0.85; }
.btn-danger:focus-visible { outline: none; box-shadow: 0 0 0 2px var(--color-status-danger); }
```

### Cards

```css
.card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
}
.card-elevated {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-md);
}
```

### Form Inputs

```css
.input {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-base);
  padding: var(--space-2) var(--space-3);
  width: 100%;
  transition: border-color var(--duration-fast);
}
.input:focus {
  outline: none;
  border-color: var(--color-border-focus);
  box-shadow: var(--shadow-focus);
}
.input::placeholder { color: var(--color-text-muted); }
```

### Status Badges

```css
.badge { display: inline-flex; align-items: center; gap: var(--space-1); border-radius: var(--radius-pill); padding: 2px var(--space-2); font-size: var(--text-xs); font-weight: var(--weight-medium); }
.badge-success { background: var(--color-status-success-bg); color: var(--color-status-success); }
.badge-warning { background: var(--color-status-warning-bg); color: var(--color-status-warning); }
.badge-danger  { background: var(--color-status-danger-bg);  color: var(--color-status-danger);  }
.badge-info    { background: var(--color-status-info-bg);    color: var(--color-status-info);    }
.badge-muted   { background: var(--color-bg-elevated); color: var(--color-text-muted); border: 1px solid var(--color-border-default); }
```

### Progress Indicators

```css
.progress-track {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-pill);
  height: 6px;
  overflow: hidden;
}
.progress-fill {
  background: var(--color-brand-accent);
  height: 100%;
  border-radius: var(--radius-pill);
  transition: width var(--duration-slow) var(--easing-default);
}
```

---

## Simulation HUD Rules

The HUD overlays the 3D scene. It must not occlude the simulation objects or interaction targets.

```css
.sim-hud {
  position: fixed;
  background: var(--color-sim-hud-bg);
  border: 1px solid var(--color-sim-hud-border);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: var(--space-4) var(--space-5);
  pointer-events: none; /* HUD must not block scene interaction */
}
.sim-hud-interactive {
  pointer-events: auto; /* Only for HUD elements that need clicks */
}
```

HUD placement: step progress indicator top-left, assist mode toggle top-right, camera reset button bottom-right. All HUD controls must have visible focus states for keyboard accessibility.

Step indicator states map to:
- LOCKED: `--color-sim-step-locked`
- UNLOCKED: `--color-sim-step-unlocked`
- IN_PROGRESS: `--color-sim-step-active` + pulsing border animation
- PASSED: `--color-sim-step-passed` + static checkmark
- FAILED: `--color-sim-step-failed` + static X indicator

---

## Application Shell and Routing

Replace all inline `onclick` navigation with a URL-addressable routing system. Route structure:

```
/                         → Public landing
/about                    → About page
/login                    → Authentication
/register                 → Registration
/demo                     → Prospect demo entry point

/app/dashboard            → Learner dashboard
/app/pathway              → Learning pathway view
/app/modules/:moduleId    → Module view
/app/simulator            → Simulation shell (current step loaded from session state)
/app/submissions/new      → e-Portfolio new submission (post-simulation route — NOT /assignments)
/app/submissions/:id      → Submission detail
/app/peer-reviews         → Peer review queue
/app/logbook              → Workplace logbook
/app/results              → Statement of results
/app/profile              → Profile and settings
/app/coach                → AI learning coach (standalone)

/staff/cohorts            → Lecturer cohort dashboard
/staff/submissions        → Submission review queue
/staff/reports            → Institution reporting

/admin/users              → User management
/admin/programmes         → Programme configuration
/admin/policy             → Institution policy
/admin/audit              → Audit log viewer
/admin/exports            → Report exports
```

All routes under `/app`, `/staff`, and `/admin` are role-gated. Unauthenticated access redirects to `/login` with the intended route as a `?redirect=` parameter.

---

## Known Prototype Inconsistencies — Fix Required

These must be resolved in the rebuild. Do not replicate them.

1. **Broken post-simulator route**: The prototype routes to a non-existent `assignments` view after simulation completion. Correct target: `/app/submissions/new` (see `simulation-state-machine` skill, SESSION_COMPLETE handler).

2. **Theme storage key inconsistency**: Some prototype pages use `myelin-theme` and others use `theme` as the localStorage key. Canonical key in the rebuild: `myelin-theme`. All pages must read from and write to this single key.

3. **Standalone module pages**: Prototype has standalone `module-1.html` etc. that diverge from the unified app state model. In the rebuild, all module views are rendered within the `/app/modules/:moduleId` route using the unified shell — no standalone module pages.

4. **Inline onclick handlers**: Prototype uses `onclick="..."` attributes throughout. Replace with event delegation and routing dispatch in all rebuilt components.

---

## Accessibility Baseline

All UI must meet WCAG 2.2 AA. Minimum requirements for every component:

- All interactive elements have visible focus states using `--shadow-focus` or equivalent
- Color contrast ratio for normal text: 4.5:1 minimum against background
- Color contrast ratio for large text (18px+ or 14px+ bold): 3:1 minimum
- All images and icons have descriptive `alt` text or `aria-label`
- Form inputs have associated `<label>` elements (not just placeholders)
- All core simulation interactions have keyboard alternatives
- Reduced-motion preference is respected: wrap all non-essential animations in `@media (prefers-reduced-motion: no-preference)`
- HUD controls in the simulator have keyboard shortcuts documented in accessible help text
- Focus order follows logical document order

---

## Responsive Behaviour

- Desktop-first: full simulator and management surfaces target 1280px+ viewport
- Tablet (768px – 1279px): learning and review workflows fully supported; simulation supported with capability check
- Mobile (< 768px): lightweight learner tasks, notifications, and logbook entry supported; simulator deferred to capability-gated flow

Use CSS custom breakpoints via media queries — do not use a grid framework in the simulator shell (performance-critical). Responsive layout in the learner and admin shells may use CSS Grid or Flexbox directly with these token-derived breakpoints:

```css
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;
```

---

## What Not To Do

- Do not hardcode any color, spacing, radius, or timing value — always use tokens
- Do not use the `theme` localStorage key — use `myelin-theme`
- Do not route post-simulation completion to `assignments` — use `/app/submissions/new`
- Do not create standalone module HTML pages outside the unified shell route
- Do not use inline `onclick` handlers — use routing dispatch and event listeners
- Do not omit focus states on any interactive element
- Do not wrap animations outside `@media (prefers-reduced-motion: no-preference)`
- Do not build HUD elements with `pointer-events: auto` unless they require clicks — the scene must remain interactive underneath the HUD
