---
name: tac-micro-interactions
description: >-
  Catalog of premium micro-interactions and motion choreography for TAC Express. Use when adding hover, focus, press, state-change, scroll, or sequencing animations to any component. Trigger on "add a hover effect", "make this feel responsive", "animate this", "the click feels dead", "polish the interaction", "premium feel", "feels static". Maps every motion to the v6 vocabulary (instant / smooth / expressive) and the Violet Grid easing tokens. Always honors prefers-reduced-motion.
---

# TAC Express — Micro-Interactions Catalog

> Every interaction below is **paste-ready**, uses Violet Grid v6 motion tokens, and respects `prefers-reduced-motion`. The goal is **earned motion**: every animation has a reason — feedback, confirmation, hierarchy, or anticipation.

---

## Motion Vocabulary (v6 — semantic)

| Token | Duration | Easing | Use |
|---|---|---|---|
| `--motion-instant` | 80ms | linear | Mission-control hover, focus, data updates |
| `--motion-smooth` | 180ms | smooth | Modal/sheet open, tab switch, content reveal |
| `--motion-expressive` | 320ms | spring | Hero entrance, KPI count-up, onboarding |

**Rule:** if you can't tell *which one* a motion is, it's the wrong motion. Pick before you write.

---

## 1. Button Press Feedback (Confident Bounce)

```tsx
className="transition-transform duration-base ease-[var(--ease-spring)]
           active:scale-[0.98]
           motion-reduce:transition-none motion-reduce:active:scale-100"
```

**Why premium:** the spring easing makes the press feel like a switch closing, not a fade. The 0.98 scale (not 0.95) is restraint.

---

## 2. Card Hover Lift (Brutalist-Compatible)

```tsx
className="tac-hover-lift"
/* Equivalent to:
   transition: bg + border + transform 80ms linear;
   hover: bg-surface-hover + border-primary + translate(-1px,-1px);
   active: bg-surface-active + translate(0,0);
   motion-reduce: no transform; */
```

**Why premium:** the 1px lift PRESERVES the brutalist offset shadow (it doesn't blur into a soft shadow). You earn the depth without breaking identity.

---

## 3. Focus Polish (2-Layer Signal)

```tsx
className="focus-visible:outline-none focus-visible:tac-focus-premium"
/* Resolves to: 1px primary outline + 8px primary color-mix bloom */
```

Pair every keyboard-focusable element with this. Stop using `ring-[3px] ring-ring/50`.

---

## 4. Status Badge State Change (Zoom + Color)

```tsx
<span className={cn(
  "inline-flex items-center gap-1 px-2 py-0.5 border tac-mono-label",
  "transition-[background-color,border-color] duration-base ease-[var(--ease-smooth)]",
  /* When status changes, animate-in zoom-in 50% over 80ms */
  "data-[changed=true]:animate-in data-[changed=true]:zoom-in-50 data-[changed=true]:duration-fast",
  status === "delivered" && "border-accent-success bg-accent-success/10 text-accent-success",
)}
data-changed={justChanged}>
  {status}
</span>
```

Drive `data-changed` from a `useEffect` that flips it true for one frame after the status prop changes.

---

## 5. Cell Flash on Update (Tabular Data)

```tsx
const [highlighted, setHighlighted] = useState(false)
useEffect(() => {
  setHighlighted(true)
  const t = setTimeout(() => setHighlighted(false), 800)
  return () => clearTimeout(t)
}, [value])

<td className={cn(
  "transition-colors duration-slow ease-[var(--ease-smooth)]",
  highlighted && "bg-primary/15"
)}>
  {value}
</td>
```

Used on real-time AWB scan tables — the row briefly flashes violet so the eye catches the update without the layout shifting. **Cap at 800ms** so flashes don't queue.

---

## 6. Copy-to-Clipboard Confirmation

```tsx
const [copied, setCopied] = useState(false)
const onCopy = async () => {
  await navigator.clipboard.writeText(awb)
  setCopied(true)
  setTimeout(() => setCopied(false), 1500)
}

<button onClick={onCopy}
        className="inline-flex items-center gap-1.5 hover:text-primary transition-colors duration-fast">
  <span className="font-mono tabular-nums">{formatAWB(awb)}</span>
  {copied ? (
    <RiCheckLine className="size-4 text-accent-success animate-in zoom-in-50 fade-in-0 duration-fast" />
  ) : (
    <RiFileCopyLine aria-hidden className="size-4 text-muted-foreground" />
  )}
</button>
```

**Why premium:** the icon swap with zoom-in is instant feedback. No "Copied!" pill bouncing — that's template behavior.

---

## 7. KPI Count-Up (motion/react)

```tsx
import { motion, useSpring, useTransform } from "motion/react"

function KpiCountUp({ value }: { value: number }) {
  const spring = useSpring(0, { stiffness: 50, damping: 20 })
  const display = useTransform(spring, (v) => Math.round(v).toLocaleString())
  useEffect(() => { spring.set(value) }, [value, spring])
  return <motion.span className="t-data tabular-nums">{display}</motion.span>
}
```

**Why premium:** spring physics means it overshoots slightly and settles — feels alive. Use only on initial mount or major state changes, NEVER on every re-render.

---

## 8. Drawer Entrance (Right-Edge, Sharp)

```tsx
/* Already correct via Radix Sheet defaults — verify these properties */
{
  className: "duration-base ease-[var(--ease-smooth)]
              data-[state=open]:animate-in data-[state=open]:slide-in-from-right
              data-[state=closed]:animate-out data-[state=closed]:slide-out-to-right"
}
```

The `--ease-smooth` keeps the slide professional; spring would feel toyish on a 480px wide panel.

---

## 9. Modal Open (Smooth + Backdrop)

```tsx
<DialogContent className="duration-base ease-[var(--ease-smooth)]
                          data-[state=open]:animate-in
                          data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95
                          data-[state=closed]:animate-out
                          data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95">
  {/* zoom-in-95 is restrained — not bouncy, just confident */}
</DialogContent>
```

Backdrop should `fade-in-0 duration-base`.

---

## 10. Scroll-Trigger Reveal (Hero Sections)

```tsx
import { motion } from "motion/react"

<motion.div
  initial={{ opacity: 0, y: 16 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.4 }}
  transition={{ duration: 0.32, ease: [0.34, 1.56, 0.64, 1] }} /* --ease-spring */
>
  <h2 className="t-h1">Mission-grade ops.</h2>
</motion.div>
```

Stagger sibling motion with `transition={{ delay: i * 0.08 }}`. **Cap the stagger** at 6 items — beyond that the sequencing reads as a long delay.

---

## 11. Tab Switch (Border-Track Slide)

```tsx
<TabsList className="relative border-b border-border">
  <TabsTrigger value="overview" className="..."/>
  <TabsTrigger value="manifest" className="..."/>
  <TabsTrigger value="exceptions" className="..."/>
  {/* Active indicator slides via View Transitions API or motion */}
</TabsList>
```

Use Radix's data-state attributes; for the underline indicator, use `motion/react`'s `<motion.div layoutId="tab-indicator" />` so it slides between tabs instead of fading.

---

## 12. Skeleton Pulse (Tokenized)

```tsx
<div className="animate-skeleton-pulse h-4 w-32 bg-muted" />
```

Defined in `globals.css` via `@keyframes skeleton-pulse` + `--duration-pulse: 2s`. **Match the skeleton's shape to the final content** (don't show 5 perfectly-aligned bars when the result is 3 cards).

---

## 13. Marquee (Live Sector Strip)

```tsx
<div className="flex overflow-hidden">
  <div className="animate-marquee-x flex shrink-0 gap-8 [--duration:35s] [--gap:32px] pause-on-hover">
    {sectors.map(/* ... */)}
  </div>
  <div className="animate-marquee-x flex shrink-0 gap-8 [--duration:35s] [--gap:32px]" aria-hidden>
    {sectors.map(/* ... */)}
  </div>
</div>
```

`[--gap:Xpx]` is the only place arbitrary `[]` values are allowed — they parameterize the keyframe.

---

## 14. Number Input — Increment Bounce

```tsx
<button onClick={onIncrement}
        className="size-8 border border-border hover:bg-surface-hover
                   transition-all duration-fast ease-linear
                   active:scale-90 active:duration-base active:ease-[var(--ease-spring)]">
  +
</button>
```

The press scales fast and rebounds slow — feels physical.

---

## 15. Page Transition (View Transitions API)

```tsx
/* In navigation handler: */
if ("startViewTransition" in document) {
  document.startViewTransition(() => router.push(href))
}
```

Combined with `globals.css`:
```css
::view-transition-old(root), ::view-transition-new(root) {
  animation-duration: var(--duration-base);
  animation-timing-function: var(--ease-smooth);
}
```

---

## Honoring `prefers-reduced-motion`

Every animation in this catalog must degrade gracefully. Use these guards:

| Pattern | Guard |
|---|---|
| Tailwind/utility classes | `motion-reduce:animate-none motion-reduce:transition-none` |
| `motion/react` | Library auto-honors `useReducedMotion()`; or wrap with `<MotionConfig reducedMotion="user">` |
| `tac-blink` / `tac-scanline` | `motion-reduce:hidden` (it's decoration, not communication) |
| `animate-skeleton-pulse` | already handled in globals.css |

`globals.css` includes a global override that drops all animations to 0.01ms — this catches anything missed.

---

## What NOT to Do (motion-killers)

| ❌ | ✅ |
|---|---|
| `transition-all duration-300` everywhere | Match motion to intent (instant / smooth / expressive) |
| Bounce easing on a 480px drawer | Smooth easing on slides; spring only on press / KPI |
| Fade-in on data table rows | Cell flash on update — fade-in is wasted on dense lists |
| Toasts that bounce in from below | Toasts that snap in (zoom-in-50, no Y motion) |
| Hovering a card scales it 1.05× | `tac-hover-lift` — preserves brutalist read |
| Auto-advancing carousel | Don't ship one. Let the user drive. |
| Particle / blob backgrounds | LAW 13 — straight lines only |
| `ease-out` on entrance + `ease-in` on exit | Symmetric motion (`ease-smooth`) for elements that toggle |

---

## Pre-Flight (per interaction)

```
[ ] Mapped to instant / smooth / expressive
[ ] Has a reason (feedback / confirmation / hierarchy / anticipation)
[ ] Honors prefers-reduced-motion
[ ] Doesn't shift surrounding layout (use transform, not width/height)
[ ] Doesn't fight the brutalist offset shadow read
[ ] Cross-checked with tac-accessibility (no flashing >3 Hz; aria-live where state announced)
```
