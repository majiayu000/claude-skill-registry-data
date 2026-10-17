---
name: design-motion-principles
description: Context-aware motion design skill with build and audit modes, applying three distinct philosophies from Emil Kowalski, Jakub Krehel, and Jhey Tompkins
triggers:
  - "audit the motion design in this project"
  - "add animation to this component"
  - "review these animations for quality"
  - "build an animated modal with motion design"
  - "check for AI-generated animation patterns"
  - "create an interactive component with purposeful motion"
  - "analyze motion gaps in the codebase"
  - "add enter and exit animations"
---

# Design Motion Principles

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A motion and interaction design skill with **two modes**: **build** interactive components with purposeful motion, or **audit** existing animations. Applies context-aware guidance from three distinct motion-design philosophies distilled from Emil Kowalski, Jakub Krehel, and Jhey Tompkins.

## Installation

```bash
npx skills add kylezantos/design-motion-principles
```

Compatible with Claude Code, Cursor, Windsurf, and other AI coding assistants.

## Core Concept

The skill applies three motion-design lenses, weighted by project context:

| Lens | Philosophy | Key Question | Best For |
|------|-----------|--------------|----------|
| **Emil Kowalski** | Restraint & speed | "Should this animate at all?" | Productivity tools, high-frequency interactions |
| **Jakub Krehel** | Production polish | "Is this subtle enough?" | Shipped consumer apps, professional refinement |
| **Jhey Tompkins** | Creative experimentation | "What could this become?" | Kids apps, portfolios, playful contexts |

The skill doesn't apply one philosophy everywhere — it weights them based on your project type, creating productive tension between approaches.

## Two Operating Modes

### 1. Create Mode

Build interactive components with motion baked in. The skill:
1. Runs discovery (project context + lens weighting)
2. Generates components (React, Framer Motion, CSS, or HTML)
3. Applies appropriate recipes, accessibility, and performance defaults

**Trigger phrases:**
- "Add animation to this modal"
- "Build an animated toast component"
- "Create a polished dropdown with motion"

### 2. Audit Mode

Review existing motion design. The skill:
1. Does reconnaissance on your project
2. Runs motion-gap analysis (finds UI that should animate but doesn't)
3. Checks against anti-AI-slop checklist
4. Proposes lens weighting
5. Delivers branded HTML report OR terminal markdown report

**Trigger phrases:**
- "Audit the motion design"
- "Review animations in this component"
- "Check for motion quality issues"

**Audit flags:**
```bash
--terminal  # Output inline markdown instead of HTML report
```

Default: HTML report writes to `motion-audits/` and opens in browser.

## Mode Detection

The skill auto-detects mode from your request:

```
User: "Add enter/exit animation to this modal"
→ CREATE mode

User: "Audit the animations in this codebase"
→ AUDIT mode

User: "Review this component's motion"
→ Ambiguous — skill will ask
```

## Context-Aware Weighting

Before any work, the skill maps project type to lens weights:

**Productivity tool / Dashboard:**
```
Primary: Emil Kowalski (fast, minimal)
Secondary: Jakub Krehel (polish)
Selective: Jhey Tompkins (only for delight moments)
```

**Kids educational app:**
```
Primary: Jakub Krehel (production quality)
Secondary: Jhey Tompkins (playful)
Selective: Emil Kowalski (high-frequency interactions only)
```

**Marketing site:**
```
Primary: Jhey Tompkins (creative)
Secondary: Jakub Krehel (polish)
Selective: Emil Kowalski (utility interactions)
```

## Motion Cookbook Reference

The skill uses a single source-of-truth motion recipe library:

### Enter/Exit Patterns

**Fade + Scale (subtle):**
```css
@keyframes enter-subtle {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal {
  animation: enter-subtle 200ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

**Slide + Fade:**
```jsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 8 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -8 }}
  transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
>
  {content}
</motion.div>
```

**Height animation (accordion):**
```jsx
<motion.div
  initial={{ height: 0, opacity: 0 }}
  animate={{ height: 'auto', opacity: 1 }}
  exit={{ height: 0, opacity: 0 }}
  transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
>
  {content}
</motion.div>
```

### Easing Functions

**Emil (fast utility):**
```javascript
const ease = [0.16, 1, 0.3, 1]; // CSS: cubic-bezier(0.16, 1, 0.3, 1)
const duration = 150; // ms
```

**Jakub (subtle polish):**
```javascript
const ease = [0.25, 0.1, 0.25, 1]; // CSS: ease-in-out
const duration = 250;
```

**Jhey (playful bounce):**
```javascript
const spring = {
  type: 'spring',
  damping: 20,
  stiffness: 300
};
```

### Framer Motion Patterns

**Conditional render with AnimatePresence:**
```jsx
import { AnimatePresence, motion } from 'framer-motion';

<AnimatePresence mode="wait">
  {isOpen && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.96 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
    >
      {content}
    </motion.div>
  )}
</AnimatePresence>
```

**List stagger (use sparingly):**
```jsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 8 },
  show: { opacity: 1, y: 0 }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i} variants={item}>
      {i}
    </motion.li>
  ))}
</motion.ul>
```

### CSS Custom Properties for Runtime Animation

```css
@property --progress {
  syntax: '<percentage>';
  inherits: false;
  initial-value: 0%;
}

.progress-bar {
  background: linear-gradient(
    90deg,
    blue var(--progress),
    gray var(--progress)
  );
  transition: --progress 300ms ease-out;
}
```

```javascript
element.style.setProperty('--progress', '75%');
```

### Scroll-Driven Animation

```css
@supports (animation-timeline: scroll()) {
  .parallax {
    animation: parallax linear;
    animation-timeline: scroll();
    animation-range: 0 500px;
  }

  @keyframes parallax {
    to {
      transform: translateY(-100px);
    }
  }
}
```

## Accessibility Requirements

Every animation must include:

**1. Reduced motion support:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Framer Motion:**
```jsx
const reducedMotion = {
  initial: { opacity: 1 },
  animate: { opacity: 1 },
  transition: { duration: 0 }
};

<motion.div
  initial={{ opacity: 0, y: 8 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{
    duration: useReducedMotion() ? 0 : 0.2
  }}
/>
```

**2. Focus management:**
```javascript
// Trap focus in modal during animation
useEffect(() => {
  if (isOpen) {
    const focusableElements = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    focusableElements[0]?.focus();
  }
}, [isOpen]);
```

**3. Meaningful timing:**
- Duration: 150–300ms for utility, 300–500ms for expressive
- Never exceed 500ms for critical path interactions
- Match duration to distance traveled

## Anti-AI-Slop Checklist

The audit mode flags these AI-generated motion patterns:

### 1. Pulsing Indicators
```css
/* ❌ AI slop if used everywhere */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.loading { animation: pulse 2s infinite; }
```

**Heuristic:** Flag if >3 pulsing elements in viewport.

### 2. Hover-Scale-On-Everything
```css
/* ❌ AI slop if on non-pressable elements */
.card:hover {
  transform: scale(1.05);
}
```

**Heuristic:** Flag if >50% of interactive elements have hover scale.

### 3. Stagger-Spam
```jsx
/* ❌ AI slop if stagger > 50ms or >10 items */
transition: { staggerChildren: 0.1 }
```

**Heuristic:** Flag if stagger used on >2 lists per page.

### 4. Blur-Everywhere Entrances
```css
/* ❌ AI slop pattern */
filter: blur(10px);
transition: filter 500ms;
```

**Heuristic:** Flag if blur used on >1 element.

### 5. Bouncy Springs on Utility
```javascript
/* ❌ AI slop for delete buttons, form submissions */
spring: { damping: 10, stiffness: 400 }
```

**Heuristic:** Flag if bounce used on destructive or utility actions.

### 6. Motion-on-Mount for Static Content
```jsx
/* ❌ AI slop: animating static header */
<motion.header initial={{ y: -100 }} animate={{ y: 0 }} />
```

**Heuristic:** Flag if page-level static elements animate.

## Performance Best Practices

**1. Animate only transform and opacity:**
```css
/* ✅ GPU-accelerated */
.fast {
  transition: transform 200ms, opacity 200ms;
}

/* ❌ Causes reflow */
.slow {
  transition: width 200ms, height 200ms;
}
```

**2. Use will-change sparingly:**
```css
.modal[data-state="opening"] {
  will-change: transform, opacity;
}

.modal[data-state="open"] {
  will-change: auto; /* Remove after animation */
}
```

**3. Avoid layout thrashing:**
```javascript
// ❌ Bad: Read then write in loop
items.forEach(item => {
  const height = item.offsetHeight; // Read
  item.style.height = height + 10 + 'px'; // Write
});

// ✅ Good: Batch reads, then batch writes
const heights = items.map(item => item.offsetHeight);
items.forEach((item, i) => {
  item.style.height = heights[i] + 10 + 'px';
});
```

**4. Debounce resize/scroll handlers:**
```javascript
let rafId;
window.addEventListener('scroll', () => {
  if (rafId) return;
  rafId = requestAnimationFrame(() => {
    // Animation logic
    rafId = null;
  });
});
```

## Common Patterns by Framework

### React + Framer Motion

**Modal:**
```jsx
import { motion, AnimatePresence } from 'framer-motion';
import { useEffect } from 'react';

export function Modal({ isOpen, onClose, children }) {
  useEffect(() => {
    if (!isOpen) return;
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="modal-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            className="modal"
            initial={{ opacity: 0, scale: 0.96, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 8 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

**Toast:**
```jsx
import { motion } from 'framer-motion';

export function Toast({ message, onDismiss }) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: -16, scale: 0.96 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.15 } }}
      transition={{ type: 'spring', damping: 25, stiffness: 300 }}
      className="toast"
    >
      <span>{message}</span>
      <button onClick={onDismiss}>×</button>
    </motion.div>
  );
}
```

### Vanilla CSS

**Dropdown:**
```html
<details class="dropdown">
  <summary>Menu</summary>
  <div class="dropdown-content">
    <a href="#">Item 1</a>
    <a href="#">Item 2</a>
  </div>
</details>
```

```css
.dropdown-content {
  overflow: hidden;
  max-height: 0;
  opacity: 0;
  transition: max-height 300ms cubic-bezier(0.16, 1, 0.3, 1),
              opacity 200ms ease-out;
}

.dropdown[open] .dropdown-content {
  max-height: 300px;
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .dropdown-content {
    transition: none;
  }
}
```

## Audit Report Output

### HTML Report (default)

Writes to `motion-audits/report-YYYYMMDD-HHMMSS.html`:

- Auto-looping CSS demos beside each finding
- Severity badges (Critical, Important, Minor)
- Code diffs with syntax highlighting
- Lens-specific recommendations
- One-click fixes where possible

Opens automatically in default browser.

### Terminal Report

Pass `--terminal` flag for inline markdown:

```markdown
## Motion Design Audit

**Project**: Dashboard App
**Date**: 2026-05-28

### Reconnaissance
- **Project type**: Productivity tool (SaaS dashboard)
- **Existing animation**: Framer Motion, 250ms avg duration
- **Motion gaps found**: 7

### Proposed Lens Weighting
- **Primary**: Emil Kowalski (restraint, speed)
- **Secondary**: Jakub Krehel (polish)
- **Selective**: Jhey Tompkins (delight moments only)

### Critical Issues (2)

#### 1. Missing AnimatePresence on modal
**File**: `src/Modal.jsx:15`
**Impact**: Abrupt exit, no exit animation
**Fix**: Wrap conditional in AnimatePresence

#### 2. Hover scale on table rows
**File**: `src/Table.css:45`
**Pattern**: Hover-scale-on-everything (AI slop)
**Fix**: Remove or reduce to scale(1.01)

### Important Issues (3)
...
```

## Troubleshooting

### "Skill doesn't detect mode"

Be explicit:
```
"Run audit mode on this component"
"Use create mode to build an animated modal"
```

### "Lens weighting doesn't match my project"

Override during discovery:
```
"Audit this, but weight Jhey primary for playful style"
```

### "HTML report doesn't open"

Use terminal mode:
```
"Audit with --terminal flag"
```

Or manually open from `motion-audits/`.

### "Motion feels too slow/fast"

Specify during creation:
```
"Build with fast, minimal animations (Emil style)"
"Add polished, 300ms animations (Jakub style)"
```

### "Missing reduced motion support"

The skill auto-includes this. If missing, report:
```
"Add prefers-reduced-motion to this component"
```

## Example Workflows

### Build Animated Notification System

```
User: "Build an animated toast notification system for this dashboard app"

Skill:
1. Detects CREATE mode
2. Runs discovery → Dashboard = Emil primary
3. Generates:
   - Toast component (React + Framer Motion)
   - Fast enter/exit (150ms)
   - Stack management
   - Reduced motion support
   - Auto-dismiss with pause-on-hover
```

### Audit Marketing Site

```
User: "Audit motion design in this marketing site"

Skill:
1. Detects AUDIT mode
2. Reconnaissance → Marketing site = Jhey primary
3. Scans for:
   - Motion gaps (hero CTA, feature cards)
   - AI slop patterns (found 3 blur entrances)
   - Missing accessibility
4. Outputs HTML report with visual demos
```

## Configuration

No configuration file needed. All behavior is context-driven.

**Environment variables:**
```bash
# Optional: Skip browser open for HTML reports
MOTION_AUDIT_NO_BROWSER=1

# Optional: Default to terminal reports
MOTION_AUDIT_TERMINAL=1
```

## References

The skill distills principles from:

- **Emil Kowalski**: [emilkowal.ski](https://emilkowal.ski), [animations.dev](https://animations.dev)
- **Jakub Krehel**: [krehel.com](https://krehel.com)
- **Jhey Tompkins**: [jhey.dev](https://jhey.dev)

This skill is an interpretation, not endorsed by the designers above.

## License

MIT
