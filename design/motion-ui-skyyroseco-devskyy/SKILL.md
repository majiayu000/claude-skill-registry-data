---
name: motion-ui
description: "Production-ready React/Next.js motion system (Framer Motion / Motion for React) covering tokens, AnimatePresence, reduced motion, and SSR safety. Use when adding or reviewing animation in frontend/ — a new motion.* component, an AnimatePresence enter/exit, a scroll-linked transform, or a jank/hydration complaint about an animated dashboard surface. Do NOT use for the WordPress theme's vanilla-CSS/Three.js motion (no React there — use css-cascade-discipline for keyframes and skyyrose-3d-web-os for scene motion), and do NOT use for non-animated component structure (frontend-patterns)."
origin: ECC
---

# Motion System v4.2

Production-ready UI motion system for React / Next.js.

Focused on **performance, accessibility, and usability** — not decoration.

## When to use

**Observable events that trigger this skill:**

* You are about to write or edit a `motion.*` element, `AnimatePresence`, `useScroll`, `useTransform`, `useAnimate`, or `layoutId` inside `frontend/`.
* A dashboard surface under `frontend/app/admin/**` animates and someone reports jank, a hydration warning, or an exit animation that never plays.
* A code review flags an animation as decorative, unstoppable, or missing a reduced-motion path.
* You are choosing an `AnimatePresence` `mode` (the repo has 8 sites with no explicit `mode` — see Verification check 3).

Use this motion system when motion:

* Guides attention (e.g., onboarding, key actions)
* Communicates state (loading, success, error, transitions)
* Preserves spatial continuity (layout changes, navigation)

### Appropriate Scenarios

* Interactive components (buttons, modals, menus)
* State transitions (loading → loaded, open → closed)
* Navigation and layout continuity (shared elements, crossfade)

### Considerations

* **Accessibility**: Always support reduced motion
* **Device adaptation**: Adjust for low-end devices
* **Performance trade-offs**: Prefer responsiveness over visual smoothness

### When NOT to use this skill

* **The WordPress theme** (`wordpress-theme/skyyrose-flagship/`). There is no React there — motion is CSS keyframes plus vanilla Three.js. Use `css-cascade-discipline` for the keyframes and `skyyrose-3d-web-os` / `threejs-animation` for scene motion. Importing this skill's `motion/react` guidance into a PHP template produces code that cannot run.
* **Non-animated component structure** — composition, state, data fetching. That is `frontend-patterns`.
* **The motion is purely decorative**, reduces clarity, or costs frame budget. Then the correct output of this skill is *delete the animation*, not tune it.

---

## Inputs

Everything below must be true **before** you write a line of motion code. Absent input = **stop**, do not
substitute a default — a guessed package name produces imports that resolve to nothing.

| Required | How to confirm | If absent |
|---|---|---|
| The animation package actually installed | `grep -E '"motion"\|"framer-motion"' frontend/package.json` | **STOP.** Neither present → the surface has no motion runtime; installing one is a dependency decision, not a styling decision. Ask before adding. |
| `frontend/node_modules` present | `ls -d frontend/node_modules` | **STOP.** Run `npm install` (npm, never pnpm — `ERR_INVALID_THIS` on Node 22+). Type-check and tests below cannot run without it. |
| The file is a Client Component | first line is `'use client'` | **STOP.** `motion.*` in a Server Component throws at build. Add the directive or move the animated subtree into its own client file. |
| A stated *purpose* for the motion | one sentence: what state does it communicate? | **STOP.** No answer = the motion is decorative. Delete it; see the Final Rule. |

**Observed in this repo `[repo]`:** `frontend/package.json` declares `"framer-motion": "^12.38.0"` and no `motion`
package. Therefore every import in `frontend/` is `from 'framer-motion'` — confirmed at
`frontend/app/admin/elite-studio/design/page.tsx:4`. Writing `from 'motion/react'` here resolves to nothing.

---

## Procedure

1. **Confirm the package.** `grep -E '"motion"|"framer-motion"' frontend/package.json`. Import from the one that exists. Never both — mixing breaks `AnimatePresence` context across the two schedulers.
2. **Confirm `'use client'`** at the top of the target file. Add it if the file is otherwise a Server Component and contains no server-only imports.
3. **State the purpose in one sentence.** Attention / state / continuity. If none apply, stop and remove the animation instead of tuning it.
4. **Animate `transform` and `opacity` only.** If the design needs `width`/`height`/`top`/`left`, restructure (scale, translate, or a layout-parent transition) rather than animating a layout property.
5. **Pull durations and easings from `motionTokens`**, not from ad-hoc numbers, so timing stays consistent across the dashboard.
6. **Set `mode` explicitly on every `AnimatePresence`.** `"wait"` for modals/toasts/page transitions, `"popLayout"` for lists/tabs/dismissible cards, `"sync"` only when overlap is the intent.
7. **Add the reduced-motion path** — `useReducedMotion()` for the JS-driven values *and* the CSS media query for anything animated in a stylesheet. Reduced motion means reduced distance and duration, not a frozen UI.
8. **Give `AnimatePresence` children a stable `key`.** No key = no exit animation, silently.
9. **Match SSR and client initial state** — always set `initial` explicitly, never rely on an implicit origin, or hydration warns and the first frame flashes.
10. **Run the Verification checks below**, all of them, and paste the output into the report.

---

## How It Works

### Core Principle

Motion must:

* Guide attention
* Communicate state
* Preserve spatial continuity

If it does none → remove it.

---

### Installation

```bash
npm install motion
```

---

### Version

* `motion/react` - default for current Motion for React projects (package: `motion`)
* `framer-motion` - legacy import path for projects that still depend on Framer Motion

**Do not mix.** Mixing causes conflicting internal schedulers and broken `AnimatePresence` contexts — components from one package will not coordinate exit animations with components from the other.

To check which version your project uses:

```bash
cat package.json | grep -E '"motion"|"framer-motion"'
```

Always import from one source consistently:

```ts
// Correct (modern)
import { motion, AnimatePresence } from "motion/react"

// Correct (legacy)
import { motion, AnimatePresence } from "framer-motion"

// Never mix both in the same project
```

---

### Motion Tokens

```ts
// motionTokens.ts
export const motionTokens = {
  duration: {
    fast: 0.18,
    normal: 0.35,
    slow: 0.6
  },
  // Use these as the `ease` value inside a `transition` object:
  // transition={{ duration: motionTokens.duration.normal, ease: motionTokens.easing.smooth }}
  easing: {
    smooth: [0.22, 1, 0.36, 1] as [number, number, number, number],
    sharp:  [0.4,  0, 0.2, 1] as [number, number, number, number]
  },
  distance: {
    sm: 8,
    md: 16,
    lg: 24
  }
}
```

Usage example:

```tsx
import { motionTokens } from "@/lib/motionTokens"

<motion.div
  initial={{ opacity: 0, y: motionTokens.distance.md }}
  animate={{ opacity: 1, y: 0 }}
  transition={{
    duration: motionTokens.duration.normal,
    ease: motionTokens.easing.smooth
  }}
/>
```

---

### Performance Rules

**Safe**

* transform
* opacity

**Avoid**

* width / height
* top / left

Rule: responsiveness > smoothness

---

### Device Adaptation

The heuristic combines CPU core count **and** available memory for a more reliable signal. `deviceMemory` is available on Chrome/Android; the fallback covers Safari and Firefox.

```ts
const isLowEnd =
  typeof navigator !== "undefined" && (
    // Low memory (Chrome/Android only; undefined elsewhere → treat as capable)
    (navigator.deviceMemory !== undefined && navigator.deviceMemory <= 2) ||
    // Few cores AND no memory API (covers Safari/Firefox on weak hardware)
    (navigator.deviceMemory === undefined && navigator.hardwareConcurrency <= 4)
  )

const duration = isLowEnd ? 0.2 : 0.4
```

---

### Accessibility

#### JS (useReducedMotion)

```tsx
import { motion, useReducedMotion } from "motion/react"

export function FadeIn() {
  const reduce = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: reduce ? 0 : 24 }}
      animate={{ opacity: 1, y: 0 }}
    />
  )
}
```

#### CSS

```css
@media (prefers-reduced-motion: reduce) {
  .motion-safe-transition {
    transition: opacity 0.2s;
  }

  .motion-reduce-transform {
    transform: none !important;
  }
}
```

#### Tailwind

```html
<div class="motion-safe:animate-fade motion-reduce:opacity-100"></div>
```

---

### Architecture & Patterns

#### Core Patterns

| Scenario | Pattern |
|---|---|
| Hover feedback | `whileHover` |
| Tap / press feedback | `whileTap` |
| Reveal on scroll | `whileInView` |
| Scroll-linked value | `useScroll` + `useTransform` |
| Conditional mount/unmount | `AnimatePresence` |
| Small layout shifts (single element, < ~300px change) | `layout` prop |
| Large layout shifts or full-page reflows | Avoid `layout`; use CSS transitions or page-level routing instead |
| Complex, imperative sequences | `useAnimate` |

> **Why avoid `layout` on large containers?** Framer's layout animation uses `transform` to reconcile positions, but on elements that span the full viewport or trigger deep reflow, the measurement cost causes visible jank and CLS. Prefer CSS Grid/Flexbox transitions or coordinate with `layoutId` on specific child elements only.

#### Layout & Transitions

* Shared element transitions → `layoutId` (must be unique per mounted instance)
* Enter / exit transitions → `AnimatePresence` (see `mode` guidance below)

#### AnimatePresence `mode`

Always specify `mode` explicitly — the default (`"sync"`) runs enter and exit simultaneously, which causes visual overlap in most UI patterns.

| `mode` | When to use |
|---|---|
| `"wait"` | Exit completes before enter starts. Use for **modals, toasts, page transitions**. |
| `"sync"` (default) | Enter and exit overlap. Use only when overlap is intentional (e.g., crossfade carousels). |
| `"popLayout"` | Exiting element is popped out of flow immediately; remaining items animate to fill. Use for **lists, tabs, dismissible cards**. |

```tsx
// Modal — always use "wait"
<AnimatePresence mode="wait">
  {open && <Modal key="modal" />}
</AnimatePresence>

// Dismissible list item — use "popLayout"
<AnimatePresence mode="popLayout">
  {items.map(item => <Card key={item.id} />)}
</AnimatePresence>
```

---

### Advanced Patterns (Concepts)

* Parallax (scroll-linked transforms)
* Scroll storytelling (sticky sections)
* 3D tilt (pointer-based transforms)
* Crossfade (shared `layoutId`)
* Progressive reveal (clip-path)
* Skeleton loading (looped opacity)
* Micro-interactions (hover/tap feedback)
* Spring system (physics-based motion)

---

### Modal Essentials

* Focus trap
* Escape close
* Scroll lock
* ARIA roles
* Use `AnimatePresence mode="wait"` so exit animation completes before the next modal enters

#### Full Example

```tsx
import React, { useEffect, useRef, useState } from "react"
import { motion, AnimatePresence } from "motion/react"

function useFocusTrap(ref: React.RefObject<HTMLDivElement | null>, active: boolean) {
  useEffect(() => {
    if (!active || !ref.current) return
    const el = ref.current
    const focusable = el.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    const first = focusable[0]
    const last  = focusable[focusable.length - 1]

    function handleKey(e: KeyboardEvent) {
      if (e.key !== "Tab") return
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault()
        last?.focus()
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault()
        first?.focus()
      }
    }

    el.addEventListener("keydown", handleKey)
    first?.focus()
    return () => el.removeEventListener("keydown", handleKey)
  }, [active, ref])
}

function useScrollLock(active: boolean) {
  useEffect(() => {
    if (!active) return
    const prev = document.body.style.overflow
    document.body.style.overflow = "hidden"
    return () => { document.body.style.overflow = prev }
  }, [active])
}

function Modal({ open, closeModal }: { open: boolean; closeModal: () => void }) {
  const ref = useRef<HTMLDivElement>(null)

  useFocusTrap(ref, open)
  useScrollLock(open)

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") closeModal()
    }
    if (open) window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [open, closeModal])

  return (
    // mode="wait" ensures exit animation finishes before any new modal enters
    <AnimatePresence mode="wait">
      {open && (
        <motion.div
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 flex items-center justify-center bg-black/40"
        >
          <motion.div
            ref={ref}
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1,    opacity: 1 }}
            exit={{    scale: 0.95, opacity: 0 }}
            transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
            className="bg-white p-6 rounded"
          >
            <h2 id="modal-title">Dialog Title</h2>
            <button onClick={closeModal}>Close</button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export function Example() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button onClick={() => setOpen(true)}>Open</button>
      <Modal open={open} closeModal={() => setOpen(false)} />
    </>
  )
}
```

---

### SSR Safety

* Match initial states between server and client renders
* Avoid implicit animation origins (always set `initial` explicitly)
* Wrap motion components in `"use client"` in Next.js App Router

---

### Debugging

Check:

* Wrong import (mixing `motion/react` and `framer-motion`)
* Missing `"use client"` directive in Next.js App Router
* Missing `key` prop on `AnimatePresence` children
* Hydration mismatch (initial state differs between SSR and client)
* `layout` prop misuse on large containers causing reflow jank
* State-driven animation not triggering (check dependency arrays)

---

### QA

* No CLS
* Keyboard works
* Focus trapped in modals
* ARIA roles correct (`role="dialog"`, `aria-modal="true"`)
* Reduced motion respected (`useReducedMotion` + CSS media query)
* No hydration warnings in Next.js
* Animations stop cleanly on unmount (no memory leaks)
* `AnimatePresence mode` set explicitly on all usage sites

---

### Anti-Patterns

* Animating layout properties (`width`, `height`, `top`, `left`)
* Infinite animations without purpose (always ask: what state does this communicate?)
* Over-staggering lists (keep `staggerChildren` ≤ 0.1s; beyond that it feels slow)
* Ignoring reduced motion preferences
* Using `layout` on large or full-viewport containers
* Omitting `mode` on `AnimatePresence` (default `"sync"` causes visual overlap)
* Using motion purely for decoration

---

### Philosophy

Motion is interaction design.

---

### Final Rule

> If motion does not improve UX → remove it.

---

## Verification

Run all four from `/Users/theceo/DevSkyy/.claude/worktrees/glimmering-crafting-shannon`. Every one can
return "no" — that is the point. Paste the real output; never report a check you did not run.

1. **No package mixing.** The repo is `framer-motion`-only; a stray `motion/react` import resolves to nothing at build time.

```bash
grep -rn "from ['\"]motion/react['\"]" frontend --include='*.tsx' --include='*.ts' \
  --exclude-dir=node_modules | wc -l
```
**PASS:** prints `0`. Any hit is a broken import — fix before proceeding. `[repro]` — observed `0` on 2026-07-28.

2. **Types still compile** (catches wrong `ease` tuple arity, bad `variants` shapes, `mode` typos):

```bash
cd frontend && npx tsc --noEmit
```
**PASS:** exits 0, no diagnostics. `[test]`

3. **Every `AnimatePresence` sets `mode` explicitly.** The default `"sync"` overlaps enter and exit; on a modal that reads as two dialogs on screen at once.

```bash
grep -rn "<AnimatePresence" frontend/app frontend/components --include='*.tsx' | grep -vc "mode="
```
**PASS:** prints `0`.
**Observed 2026-07-28: `8` — this check is RED in the current tree** `[repo]`. 8 sites use bare
`<AnimatePresence>` against 4 with an explicit `mode`. That is a repo-state finding about committed
source; it is **not** a claim about rendered production behavior, which would need `[live]`.

4. **Reduced motion is honoured** wherever motion ships:

```bash
grep -rl "framer-motion" frontend/app frontend/components --include='*.tsx' | wc -l
grep -rl "useReducedMotion\|prefers-reduced-motion" frontend/app frontend/components frontend/lib | wc -l
```
**PASS:** the second count is > 0 and every animated route group is represented.
**Observed 2026-07-28: `32` files import `framer-motion`, `0` reference reduced motion — RED** `[repo]`.
Treat this as the standing baseline: your change must not make it worse, and any file you touch
must gain the reduced-motion path.

**Proving these checks can fail (rule 3).** Check 1 was proven against a scratch tree on 2026-07-28, not
against the working copy: writing a single file containing `import { motion } from 'motion/react';` under
a throwaway `frontend/app/` made the grep print `1`; deleting that file returned it to `0` `[repro]`.
Checks 3 and 4 are *already* returning red, which is itself proof they discriminate. A check never
observed failing is a guess with a citation.

**A gate that dies is not a gate that passed (rule 1).** If `npx tsc --noEmit` is killed, times out, or
aborts on a resolver error, its silence is an *artifact* — re-run it, do not record it as clean.

**A SKIP is not a PASS (rule 2).** There is no `eslint-plugin-jsx-a11y` and no `axe-core` in
`frontend/package.json` `[repo]`, so automated a11y assertion of an animated component is **not
available here**. Say so explicitly and name the closer (a human running the keyboard + screen-reader
pass, or a maintainer installing `@axe-core/playwright`). Silent omission reads as success.

**Attribution before you claim a finding (rule 4).** Checks 3 and 4 have a nonzero baseline, so a red
result after your edit does not mean you caused it. Extract the pristine tree and diff the *lines*, not
the counts:

```bash
mkdir -p /tmp/attr && git archive HEAD frontend/app frontend/components | tar -x -C /tmp/attr
grep -rn "<AnimatePresence" /tmp/attr/frontend/app /tmp/attr/frontend/components | grep -v "mode=" > /tmp/attr/before.txt
grep -rn "<AnimatePresence" frontend/app frontend/components | grep -v "mode=" > /tmp/attr/after.txt
diff /tmp/attr/before.txt /tmp/attr/after.txt
```
**PASS:** `diff` prints nothing, or only lines you intentionally added. `[test]`
**Never `git stash` for this** — the stash stack is shared across worktrees and you can pop another
session's work.

---

## Worked example

**Task (2026-07-28):** confirm the dashboard's motion imports are consistent before adding an
`AnimatePresence` to an admin page.

Read the real import site:

```bash
$ sed -n '1,5p' frontend/app/admin/elite-studio/design/page.tsx
'use client';

import { useState, useRef, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
```

Package check, exactly as the Inputs table requires:

```bash
$ grep -E '"motion"|"framer-motion"' frontend/package.json
    "framer-motion": "^12.38.0",
```

`framer-motion` is the installed runtime and there is no `motion` package — so the correct import in this
repo is `from 'framer-motion'`, and the `motion/react` snippets elsewhere in this document are the
*legacy-path* variant, not what you type here. `[repo]`

Verification check 1 then confirms nothing has drifted:

```bash
$ grep -rn "from ['\"]motion/react['\"]" frontend --include='*.tsx' --exclude-dir=node_modules | wc -l
0
```

Check 3, run in the same session, came back red:

```bash
$ grep -rn "<AnimatePresence" frontend/app frontend/components --include='*.tsx' | grep -vc "mode="
8
```

**Correct report of that result:** "8 `AnimatePresence` sites in the committed tree carry no explicit
`mode` `[repo]`. Whether any of them visibly overlaps in production is unverified — that needs a browser
against the deployed dashboard `[live]`." Reporting it as "8 broken modals in production" would be the
scope jump the evidence rules ban (bug-287).

---

## Failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| Exit animation never plays; element vanishes instantly | `AnimatePresence` child has no stable `key`, or the parent unmounts with it | Give the child a `key`; keep `AnimatePresence` mounted above the conditional |
| Two dialogs visible at once during a swap | `mode` omitted → defaults to `"sync"` | `mode="wait"` (Verification check 3 catches this repo-wide) |
| `Error: ... only works in Client Components` at build | `motion.*` used in a Server Component | Add `'use client'`, or split the animated subtree into a client file |
| Hydration mismatch warning + first-frame flash | `initial` omitted, so SSR and client disagree on frame 0 | Always set `initial` explicitly |
| Import resolves to nothing / `AnimatePresence` context missing | Mixed `motion/react` and `framer-motion` | One package only — Verification check 1 |
| Visible jank on a full-width container | `layout` prop on a viewport-spanning element; reconciliation measurement cost | Drop `layout`; use CSS grid/flex transitions, or `layoutId` on specific children |
| Animation ignores OS reduced-motion setting | No `useReducedMotion()` and no CSS media query | Verification check 4 — currently red repo-wide `[repo]` |
| List reveal feels sluggish | `staggerChildren` > 0.1s | Keep ≤ 0.1s |
| "Zero problems" from a check that was actually killed | Gate died mid-run; output is an artifact, not a result | Re-run by hand — bug-230 (×6), the fail-open pattern |
| A red gate blamed on your change | Pre-existing baseline (8 bare `AnimatePresence`, 0 reduced-motion refs) | Attribute against a pristine tree via `git archive`, diff contents not counts |

---

## Examples

### Button Interaction

```tsx
import { motion } from "motion/react"

export function Button() {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.97 }}
      transition={{ duration: 0.15, ease: [0.4, 0, 0.2, 1] }}
    >
      Click me
    </motion.button>
  )
}
```

---

### Reduced Motion Example

```tsx
import { motion, useReducedMotion } from "motion/react"

export function FadeIn() {
  const reduce = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: reduce ? 0 : 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: reduce ? 0.1 : 0.35, ease: [0.22, 1, 0.36, 1] }}
    />
  )
}
```

---

### Stagger List

```tsx
import { motion } from "motion/react"

const container = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.08 } // keep ≤ 0.1s to avoid sluggishness
  }
}

const item = {
  hidden:  { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0,  transition: { duration: 0.3, ease: [0.22, 1, 0.36, 1] } }
}

export function List() {
  return (
    <motion.ul variants={container} initial="hidden" animate="visible">
      {[1, 2, 3].map(i => (
        <motion.li key={i} variants={item}>Item {i}</motion.li>
      ))}
    </motion.ul>
  )
}
```

---

### Modal with AnimatePresence

```tsx
import { motion, AnimatePresence } from "motion/react"

export function Modal({ open }: { open: boolean }) {
  return (
    <AnimatePresence mode="wait">
      {open && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1    }}
          exit={{    opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
        />
      )}
    </AnimatePresence>
  )
}
```

---

### Scroll Parallax

```tsx
import { useScroll, useTransform, motion } from "motion/react"

export function Parallax() {
  const { scrollYProgress } = useScroll()
  const y = useTransform(scrollYProgress, [0, 1], [0, -80])

  return <motion.div style={{ y }} />
}
```

---

### Skeleton Loading

```tsx
import { motion } from "motion/react"

export function Skeleton() {
  return (
    <motion.div
      className="bg-gray-200 h-6 w-full rounded"
      animate={{ opacity: [0.5, 1, 0.5] }}
      transition={{
        duration: 1.5,       // comfortable pulse — was missing, caused fast flash
        repeat: Infinity,
        ease: "easeInOut"
      }}
    />
  )
}
```

---

### Shared Layout (Crossfade)

```tsx
import { motion } from "motion/react"

// layoutId must be unique per mounted instance.
// If multiple instances can exist simultaneously, append a unique id:
// layoutId={`shared-${item.id}`}
export function Shared() {
  return <motion.div layoutId="shared" />
}
```
