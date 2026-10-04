---
name: responsive-fix
description: Fix responsive/mobile layout issues (320px → desktop) in the MyJKKN app with CSS-only changes — horizontal overflow, clipped/overlapping elements, floating-button (FAB) collisions, unreadable text, and broken breakpoints. MANUAL INVOCATION ONLY - use this skill ONLY when the user explicitly invokes it by name ("/responsive-fix" or "use the responsive-fix skill"). Do NOT auto-trigger this skill just because the conversation mentions responsive design, mobile screens, overflow, 320px, or UI bugs — without an explicit invocation, handle those normally without this skill.
---

# Responsive Fix — MyJKKN

Fix mobile/responsive layout bugs in this Next.js 15 + Tailwind CSS project with
surgical, CSS-only changes. This skill exists because responsive fixes here have
strict scope rules: the app is a shared production project, and the user allows
ONLY visual/layout corrections — nothing else may change.

## Invocation contract (read first)

This skill runs ONLY when the user explicitly invoked it. If you loaded this
skill without the user naming it (e.g. they merely said "the page looks broken
on mobile"), stop and handle the request normally without these instructions.

The user typically provides: a page path (e.g. `/dashboard`), a screenshot,
and/or a description like "320px la adi vangudhu" (broken at 320px). If no page
or component is named, ask which page to fix before touching anything.

## Hard constraints (non-negotiable)

1. **CSS/className changes only.** Never modify texts, labels, workflows,
   business logic, data fetching, handlers, imports of behavior, or other
   modules' code. If a real fix seems to require a logic change, STOP and ask.
2. **Only the named target.** Fix only the page/component the user pointed at.
   If the root cause lives in a shared component (Navbar, BottomNav, a FAB),
   that's allowed — but explicitly tell the user it is shared and affects all
   pages, before or immediately with the fix.
3. **Root cause + math first.** Before editing, state the cause with numbers
   (e.g. "6 items × min-w-[56px] = 336px > 320px viewport → last item clips").
   Never apply a fix you can't explain arithmetically.
4. **Minimal diff.** Prefer editing existing className strings over adding
   wrappers, new components, or new CSS files.

## Definition of "responsive" (acceptance criteria)

A screen passes when ALL of these hold from 320px up to desktop:

- **No horizontal scroll** on the document at any width.
- **No overlapping or cut-off content** — including fixed/floating elements.
- **Nothing overflows its own section/box** — texts and buttons must stay
  inside their containing card/section/container at every width (320px up).
  No label, button, or child element may spill past its parent's border. Cure
  per element: buttons in a row → `flex-wrap` (or stack `flex-col` then
  `sm:flex-row`); long text → `min-w-0` + `truncate`/`break-words`; the button
  that must not shrink → `shrink-0`; genuinely wide content (tables, tab
  strips) → wrap the container in `overflow-x-auto` so the box scrolls, not the
  page.
- **Readable text** — nothing below ~10px; long text truncates with ellipsis
  (`truncate` + `min-w-0`) instead of clipping or forcing overflow.
- **Touch-friendly targets** — interactive elements keep ≥ ~44px effective tap
  area on touch layouts (Tailwind `h-11`/`w-11` ≈ 44px).

Test mentally (or in browser when available) at: **320, 375, 640 (sm), 768
(md), 1024 (lg), desktop**.

## Diagnostic playbook

Work through these known failure classes — they cover nearly every mobile bug
seen in this codebase:

### 1. Horizontal overflow (page scrolls sideways)
Find the widest row of fixed-width items. Common causes and cures:
- Flex row where items can't shrink → add `min-w-0` to the shrinkable item
  (usually the title/text) and `shrink-0` to icons/buttons that must not
  squish; give text `truncate`.
- Fixed min-widths that don't fit: `N items × min-w > 320` → make the min-width
  responsive (`min-w-0 sm:min-w-[56px]`).
- Fixed pixel widths (`w-[400px]`) → `w-full max-w-[400px]`.
- Wide tables/charts → wrap in `overflow-x-auto` (the container scrolls, the
  page does not).

### 2. Fixed/floating element collisions (FABs, banners, bottom nav)
- Position floating elements with **CSS breakpoints, never user-agent
  sniffing**. A `isMobileDevice()` check and a `lg:hidden` nav WILL disagree
  (DevTools emulation, tablets) and cause overlap. Match the exact breakpoint
  of the element being avoided: nav is `lg:hidden` → FAB uses
  `bottom-[Xrem] lg:bottom-4`.
- To align a FAB with others, compute centers: `center = bottom + height/2`,
  then solve for the new `bottom`. State the math.
- Keep each element's existing z-index hierarchy; don't invent new z values.

### 3. Header/toolbar rows too wide
Pattern proven in `components/Navbar/Navbar.tsx`: left cluster gets
`min-w-0 flex-1` + title `truncate`; right cluster gets `shrink-0`; gaps and
paddings shrink at base and restore at `sm:` (`space-x-1 sm:space-x-2`,
`px-3` on compact buttons).

### 4. Grids/cards breaking at small widths
Mobile-first stacking: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`. Never let
a card enforce a min-width larger than ~288px (320 − page padding).

## Workflow

1. **Identify** — restate the reported issue; open the named page/component.
2. **Locate root cause** — grep/read for the offending classes; verify with the
   arithmetic from the playbook above.
3. **Fix minimally** — CSS/className only, mobile-first (`base` styles for
   320px, then `sm: md: lg:` restore larger-screen appearance so desktop is
   pixel-identical to before).
4. **Self-check** — recompute widths at 320px; confirm desktop classes
   (`sm:`/`lg:` values) reproduce the pre-fix layout exactly.
5. **Hand back** — list changed files with line references, the cause, the
   math, and ask the user to re-test; fix further only what they report.

## Verification math examples

- Bottom nav: 6 × `min-w-[56px]` = 336 > 320 → clip. Fix `min-w-0
  sm:min-w-[56px]` → 6 × ~53px = 318 ≤ 320. ✓
- FAB alignment: red center 136+24=160, yellow center 80+24=104 → pair center
  132 → green (44px tall) bottom = 132−22 = 110px = `bottom-[6.875rem]`. ✓
- Header: fixed items 40+85+160+margins ≈ 410 > 320 → title must be the
  flexible item (`min-w-0 flex-1` + `truncate`). ✓
