---
name: nextjs-ui-ux-and-animations
description: >
  Opinionated UI/UX and high-performance animation system for
  Next.js App Router projects: layout, spacing, typography, and
  smooth, GPU-friendly motion patterns.
---

# Next.js UI/UX and Animations Skill

## When to use this Skill

Is Skill ko tab use karo jab:

- Next.js 16+ App Router frontend design kar rahe ho (landing pages,
  dashboards, marketing sites, SaaS UI, etc.).
- Tum chahte ho ke Claude **hamesha ek hi visual language** follow kare:
  spacing, typography, color, layout.
- Tumko **smooth but fast** animations chahiye jo FPS kill na karein:
  CSS/Framer Motion patterns jo sirf GPU-friendly properties animate
  karein. [web:204][web:205][web:211][web:214]

Ye Skill generic hai, kisi ek repo tak limited nahi, lekin Next.js App
Router + React ecosystem assume karta hai.

---

## Tech + design assumptions

- Frontend: Next.js 16+ App Router.
- Styling: Tailwind CSS ya CSS Modules/vanilla-extract style utility
  approach (Skill framework-agnostic but utility-first friendly).
- Animation libs:
  - Native CSS transitions/animations (preferred for simple hovers,
    reveals). [web:204][web:205][web:208]
  - Framer Motion for complex/conditional motion (page transitions,
    layout animations). [web:209][web:212][web:218][web:221]
- Design system:
  - 4- or 8-point spacing system (spacing values multiples of 4). [web:210][web:213]
  - Limited, consistent typographic scale (3–6 sizes, clear hierarchy). [web:216][web:219][web:222]

Koi specific color palette enforce nahi hota; ye Skill sirf **structure
aur motion** ke rules define karta hai.

---

## Layout & spacing principles

- **Sectioning the page**

  - Har major screen ko clear sections me todho:
    - Hero / header section.
    - Content sections (features, stats, lists).
    - Call-to-action (CTA) bands.
    - Footer.
  - Har section ka vertical spacing consistent ho (e.g. `py-16`, `py-20`
    level, not random values per section). [web:210][web:213]

- **Spacing system**

  - Spacing 4- ya 8-point grid follow kare:
    - Allowed values: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64... px equivalents. [web:210][web:213]
  - Components ke andar padding/margin inhi values ke multiples me ho,
    random `13px`, `27px` jaisi values avoid karo.

- **Grids & alignment**

  - Desktop par 12-column mental grid follow karo (even agar Tailwind
    se implement ho):
    - Content max-width constrained (e.g. `max-w-5xl` / `max-w-6xl`) and
      horizontally centered.
  - Text blocks ko readable width tak limit karo (around 60–80 chars
    per line for body text). [web:216][web:222]

---

## Typography & color hierarchy

- **Type scale**

  - Fixed typographic scale use karo:
    - Heading levels: e.g. `h1`, `h2`, `h3` with decreasing sizes.
    - Body text: 1–2 sizes (base + small).
  - Har level ke liye consistent:
    - `font-size`, `line-height`, `font-weight`. [web:216][web:219][web:222]

- **Hierarchy**

  - Har section me:
    - 1 primary heading (visual focal point).
    - Optional subtitle/eyebrow text for context.
    - Body copy for detail.
  - Over-decoration avoid karo (too many fonts, colors, sizes).

- **Color & contrast**

  - Primary + accent color limited rakho (1–2 main accent colors).
  - Text/background contrast sufficient ho, WCAG-friendly (dark text on
    light bg ya vice versa). [web:216][web:219]

---

## Component patterns (cards, lists, CTAs)

- **Cards**

  - Card pattern:
    - Padding follows spacing grid (e.g. `p-4`, `p-6`).
    - Border-radius consistent across app.
    - Shadow ya border ek hi scale ka use karo across cards.
  - Hover state:
    - Slight elevation ya scale via `transform` + `box-shadow` change
      (avoid layout reflow). [web:204][web:205][web:211]

- **Lists & rows**

  - Repeated items (tasks, features) me:
    - Consistent gap (`gap-4`, `gap-6`).
    - Consistent alignment of titles, metadata, actions.

- **Buttons & CTAs**

  - Primary button style:
    - High-contrast background + white/near-white text.
    - Clear hover/focus states.
  - Secondary / ghost buttons consistent alternate style use karein.

Claude ko new UI banate waqt ye base patterns ko reuse karna chahiye,
na ke har page pe completely naya button/card style invent karna.

---

## Motion design system — core rules

Aim: **smooth, 60fps‑ish** animations jo CPU/GPU pe light hon. [web:204][web:205][web:211][web:214]

- **What to animate**

  - Animate **only GPU-friendly properties** by default:
    - `transform` (translate, scale, rotate).
    - `opacity`. [web:204][web:205][web:211][web:223]
  - Avoid animating:
    - `top`, `left`, `width`, `height`, `margin`, `padding`,
      `box-shadow` in heavy/continuous animations (ye layout / paint
      thrash kar sakte hain). [web:204][web:205][web:211][web:217]

- **Duration & easing**

  - Use limited duration tokens:
    - `fast` ~ 120–180ms (small hovers/feedback).
    - `normal` ~ 200–260ms (transitions, modal open).
    - `slow` ~ 320–400ms (page transitions, major UI change). [web:206][web:208]
  - Easing:
    - Default: `ease-out` / cubic functions for entry.
    - Use `ease-in` for exit animations.
    - For micro interactions, consider standard easing curves library
      (Framer Motion defaults ya custom bezier). [web:206][web:209]

- **Levels of motion**

  - Micro interactions:
    - Button hover: slight scale/translate, color shift.
    - Icon hover: small rotate/bounce, opacity change.
  - Content reveal:
    - Section fade/slide-in on scroll (threshold-based, once per view).
  - Page transitions:
    - Route change par fade/slide of whole page or key sections.

---

## Performance & accessibility guardrails

- **Performance**

  - Prefer CSS transitions for simple one-off animations; JavaScript
    driven / Framer Motion sirf jab logic/control chahiye. [web:204][web:205][web:211]
  - Long-running or scroll‑linked animations minimal rakho; avoid heavy
    parallax har section me. [web:205][web:211][web:214]
  - Use `will-change: transform` ya Framer Motion ki internal
    optimizations only jahan zaroorat ho (excessive use se bhi perf
    down ho sakta hai). [web:204][web:211]

- **Reduced motion**

  - Respect user preferences:
    - CSS: `@media (prefers-reduced-motion: reduce)` ke andar animations
      ko disable/simplify karo. [web:205][web:214]
    - Framer Motion: `useReducedMotion` hook se motion intensity kam
      karo ya turn off karo. [web:209][web:221]
  - Large page transitions / auto-scrolling effects reduced motion
    users ke liye skip karo.

- **Focus & usability**

  - Animations kabhi focus/keyboard navigation ko break na karein
    (focus rings visible, tabbable elements stable).
  - Loading states:
    - Use skeletons / subtle shimmer animations instead of janky
      layout shifts.

---

## Framer Motion patterns (Next.js)

Jab Framer Motion use ho:

- **Variants & layout**

  - Shared `variants` objects define karo (e.g. `fadeInUp`, `scaleOnHover`)
    jo multiple components reuse karein.
  - Layout transitions sirf jahan actual layout change ho; avoid
    overusing `layout` prop everywhere.

- **Page transitions**

  - App Router layout me:
    - `PageTransition` wrapper component use karo jo:
      - Initial: `opacity: 0, y: 8`
      - Animate: `opacity: 1, y: 0`
      - Exit:    `opacity: 0, y: -4`
    - Duration ~ 0.2–0.3s, easing `easeOut`. [web:209][web:212][web:218][web:221]

- **Scroll-reveal**

  - Intersection Observer ya `whileInView` (Framer) ka use karo:
    - Trigger once per section, threshold ~ 0.15–0.3.
    - `initial` off-screen + low opacity, `whileInView` on-screen. [web:209][web:212]

Claude ko nayi animations likhte waqt yahi patterns reuse karne chahiye
instead of har jaga naya custom Framer code likhne ke.

---

## Things to avoid

- Over-animating: har element pe heavy motion, har hover par big scale
  ya bounce; app cheap lagti hai aur performance girta hai. [web:205][web:211]
- Animating layout-affecting properties (width/height/margins) in
  continuous loops; is se reflow + repaint issues aate hain. [web:204][web:205][web:217]
- Using multiple disjoint spacing/typography scales in the same app.
- Scroll-jacking (custom scroll behavior jo default scroll ko override kare)
  unless spec explicitly demand kare.

---

## References inside a repo

Jab ye Skill use ho:

- Design guidelines / tokens ideally:
  - `frontend/styles/design-tokens.(ts|json)` – spacing, durations,
    easing, radii, etc.
  - `frontend/components/ui/` – base components (Button, Card, Section,
    PageTransition, etc.) jo in rules ko enforce karein.
- Framer Motion wrappers:
  - `frontend/components/motion/` – reusable motion primitives based on
    is Skill ke patterns.

Agar ye files missing hon, Claude ko propose karna chahiye ke pehle
yeh base components/tokens create karein, phir nayi screens unka reuse
kar ke banayein — is tarah tumhara UI/UX + animations ek **signature
style** ban jayega jo har nayi app me recognizable rehega.
