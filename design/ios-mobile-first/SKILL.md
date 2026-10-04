---
name: ios-mobile-first
description: "iOS-native mobile web UX rules. Use when building any UI component, fixing mobile issues, reviewing responsive code, or touching viewport heights (dvh vs h-screen), safe areas, Dialog vs Drawer, tabs on mobile, touch targets, or input zoom."
---

# iOS Mobile-First Design

> **Official guide:** `~/.arman/rules/nextjs-best-practices/nextjs-guide.md` — See the official guide for core architecture. The old §13 (Mobile-First) was removed; mobile-first patterns in this file will move to a dedicated *Mobile & Responsive UX* guide.

Single source of truth for mobile UX. Desktop stays unchanged; mobile gets iOS-native treatment.

**Reference implementations:** `features/feedback/FeedbackButton.tsx` (tap button), `features/canvas/social/CanvasShareSheet.tsx` (explicit Drawer branch).

---

## Golden Rules

1. **Always `dvh`** — never `vh` or `h-screen`
2. **Always `pb-safe`** — on fixed bottom elements
3. **Fields are ≥16px on touch** — enforced globally by THE iOS ZOOM FLOOR in `app/globals.css`; author mobile-facing fields `text-base` anyway, and never set an inline `fontSize` below 16px on one
4. **Always 44pt touch targets** — and NEVER one element at a time. Put `matrx-touch-targets` on the feature/section/dialog ROOT (`app/globals.css`): it floors every button, tab, menu item and `a[data-tap-target]` inside it — including files written later — under `pointer: coarse` or below `lg` only, so desktop density never moves. A control that must stay SMALL because its size is the control (a bare checkbox, a radio, a 14px switch) is excluded there by design and takes `matrx-tap-area` on its `<label>` instead: an invisible 44×44 ring, painted box unchanged. Opt one control out of the floor with `data-touch-exempt` + a reason at the call site. A Radix dialog PORTALS out of its route's subtree, so its `DialogContent` carries the class itself
5. **Header tokens:** `--shell-header-h` / `--header-height` — never hardcode in calc
6. **Dialogs become bottom sheets on mobile automatically** — a plain `<Dialog>` already does it (see "Dialog = Desktop, Drawer = Mobile"); hand-roll a `Drawer` branch only for a drag handle or a genuinely different mobile layout
7. **Never tabs on mobile** — stack vertically
8. **Never nested scrolling** — single scroll area per view
9. **Always test iOS Safari** — on real device
10. **A data table reflows on a phone** — `<Table wrapperClassName="phone-stack">` (see *Tables on phones*); a fixed-width table with no reflow fails `pnpm check:phone-layout`
11. **Nothing is hover-only on touch** — a control revealed by `opacity-0 group-hover:opacity-100` also carries `pointer-coarse:opacity-100`, so a phone shows it. Dense desktop sizes (`h-5`/`h-7` icon buttons) are fine on desktop; the 44px floor (rule 4) grows them on touch only. The one sanctioned exception is `RouteModeNav` (see `core-route-headers`), whose phone reach is its bottom-sheet rows

---

## Viewport & Layout

### Dynamic Viewport Units

```tsx
// ✅ Adapts to mobile browser chrome
<div className="h-dvh">     <div className="min-h-dvh">     <div className="max-h-dvh">

// ❌ Breaks when browser chrome hides/shows
<div className="h-screen">  <div className="min-h-screen">
```

### Safe Areas

```tsx
// ✅ Respects iPhone home indicator / notch
<div className="fixed bottom-0 pb-safe">
<div className="mb-safe">

// Utilities in globals.css:
// .pb-safe { padding-bottom: env(safe-area-inset-bottom, 1rem); }
// .mb-safe { margin-bottom: env(safe-area-inset-bottom, 1rem); }
```

### Header Height & Page Layout (`(core)` AppShell)

`.shell-main` fills the viewport (negative margin pull-up). **Body wrapper: `h-full overflow-hidden` — do not subtract header height.**

```tsx
// ✅ (core) full-height workspace — chat, tasks, agent build
<>
  <PageHeader>{/* route chrome */}</PageHeader>
  <div className="h-full flex flex-col overflow-hidden">
    <div className="flex-1 overflow-y-auto pb-safe">{/* scroll area */}</div>
  </div>
</>

// ✅ Per-panel clearance when static top UI must sit below the glass header
<div className="h-full overflow-auto pt-[var(--shell-header-h)]">{/* file tabs, titles */}</div>

// ❌ Double-subtracts header inside shell-main → empty band at bottom
<div className="h-[calc(100dvh-var(--header-height))]">
<div className="h-page">

// ❌ Hardcoded
<div className="h-[calc(100vh-40px)]">
```

**When header subtraction IS correct:** `/administration/*` and `(transitional)` (whose layout sets `--header-height` to the shell header and starts content below it) — content below the header, not behind it. Use `.h-page` or `calc(100dvh - var(--header-height))` there only.

Full pattern: `features/shell/components/header/variants/USAGE.md`

---

## Dialog = Desktop, Drawer = Mobile

**The base `DialogContent` (`@/components/ui/dialog`) AUTO-converts to a bottom sheet on mobile** — full width, bottom-anchored, `max-h-[90dvh]`, internally scrollable, `pb-safe`. So a plain `<Dialog>` is already mobile-safe: its confirm/submit control can never be pushed off-screen. This is the systematic guard against mobile "lockout" popups. Opt out with `<DialogContent mobileSheet={false}>` only for a surface that must stay centered on mobile.

**Hand-roll the explicit Drawer branch below only when you need more than the auto-sheet** — a `vaul` drag-to-close handle, or a genuinely different mobile layout (not just a reflow). For a normal dialog, do nothing extra.

**A sheet whose content varies gets ONE fixed height, not an adaptive range.** A `min-h`/`max-h` sheet re-measures on every drill-in, filter keystroke and late load, so the panel grows and shrinks under the user's thumb — read as jumping, not as fitting. Multi-level or tabbed sheets (`BottomSheet` from `@ai-matrx/design-system` → `size="full"`, what `TabbedBottomSheet` uses) pin `h-[92dvh]` and scroll inside it. Adaptive is right only for a single short, static list. (A sub-16px field is the same bug by another route: iOS zooms the page on focus.)

**`DropdownMenuContent` and `PopoverContent` cap to the viewport and scroll** (max-height of `var(--radix-<component>-content-available-height)` plus `overflow-y-auto` — e.g. `--radix-dropdown-menu-content-available-height`), so a long menu can never grow off-screen and lock the user out. Any custom popup panel you build MUST do the same: `max-height` + `overflow-y-auto`, never an unbounded height.

```tsx
import { useIsMobile } from "@/hooks/use-mobile";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Drawer, DrawerContent, DrawerTitle } from "@/components/ui/drawer";

function MyComponent() {
  const isMobile = useIsMobile();
  const [isOpen, setIsOpen] = useState(false);

  if (isMobile) {
    return (
      <Drawer open={isOpen} onOpenChange={setIsOpen}>
        <DrawerContent className="max-h-[85dvh]">
          <DrawerTitle className="sr-only">Title</DrawerTitle>
          <div className="flex-1 overflow-y-auto overscroll-contain pb-safe">
            {/* Content — single scroll area, no nesting */}
          </div>
        </DrawerContent>
      </Drawer>
    );
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="max-w-[95vw] w-full lg:max-w-[1400px] max-h-[90dvh] overflow-hidden flex flex-col">
        <DialogHeader><DialogTitle>Title</DialogTitle></DialogHeader>
        <div className="flex-1 overflow-y-auto">{/* Content */}</div>
      </DialogContent>
    </Dialog>
  );
}
```

| Element | Mobile (Drawer) | Desktop (Dialog) |
|---------|----------------|-----------------|
| Max height | `max-h-[85dvh]` | `max-h-[90dvh]` |
| Max width | Full width | `max-w-[95vw]` / `lg:max-w-[1400px]` |
| Scroll | `overflow-y-auto overscroll-contain` | `overflow-y-auto` |
| Safe area | `pb-safe` | Not needed |
| Layout | Natural flow | `flex flex-col overflow-hidden` |

---

## Tables on phones — THE PHONE-STACK TABLE

A hand-rolled `<Table>` with `TableHead className="w-[120px]"` columns is a 1,200px sideways scroller on a 390px phone: every value an admin needs is off-screen and the row is un-tappable without pinch-zoom (the 2026-09-12 feedback-console report). Do not build a second card list for it, and do not hide it behind `md:`. Opt the SAME markup into the reflow that `app/globals.css` ships (search **THE PHONE-STACK TABLE**):

```tsx
<Table wrapperClassName="phone-stack">
  <TableHeader>…unchanged…</TableHeader>
  <TableBody>
    <TableRow>
      <TableCell data-phone="lead">{row.title}</TableCell>                 {/* headline: first, full width — exactly one */}
      <TableCell data-phone="inline">{statusBadge}</TableCell>             {/* self-naming chip, no label */}
      <TableCell data-label="Owner" data-phone="inline">{row.owner}</TableCell>
      <TableCell data-label="Created" data-phone="inline">{ago}</TableCell> {/* a bare date needs its label */}
      <TableCell data-phone="hidden">{row.id}</TableCell>                  {/* desktop-only detail */}
      <TableCell data-phone="actions">{buttons}</TableCell>                {/* last, right-aligned */}
    </TableRow>
  </TableBody>
</Table>
```

Below 768px the `<thead>` hides, each row becomes a flex-wrapped card, and `data-label` prints a small-caps label above the value. Desktop is untouched. Header-borne sort controls are not reachable on the card list — a table whose ordering matters on a phone puts its sort in a toolbar. `MatrxDataTable` callers use its `mobileCards` prop instead; the two are the same breakpoint.

**Guard:** `pnpm check:phone-layout` (`--strict` in the release gates; `--self-test` proves it can fail) reports every fixed-width table with no reflow (`phone-stack` / `mobileCards` / `useIsMobile` branch), every `h-screen` / `*-[Nvh]` unit, and every ≥3-column grid inside a dialog or sheet with no `sm:` variant (mark a grid that is right N-up — swatches, icons — with a `phone-ok: <reason>` comment on the line above).

**Also in `globals.css`:** the base mobile rule that turned every `<table>` into `display:block` now excludes design-system tables (`data-slot="table"`), which own their scroll wrapper; the block rule made them shrink-to-fit and double-scroll.

---

## MANDATORY: Tabs = Desktop Only

**Never use tabs on mobile.** They cause UX friction, nested scroll trapping, and hidden content.

Stack all sections vertically with visual dividers:

```tsx
import { useIsMobile } from "@/hooks/use-mobile";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

function MyForm() {
  const isMobile = useIsMobile();
  const [activeTab, setActiveTab] = useState("basic");

  if (isMobile) {
    return (
      <div className="space-y-6 p-4">
        {/* Section 1 */}
        <div className="space-y-4">
          <h3 className="text-sm font-medium flex items-center gap-2">
            <div className="h-6 w-1 bg-primary rounded-full" />
            Basic Info
          </h3>
          {/* Fields */}
        </div>

        {/* Section 2 */}
        <div className="space-y-4 pt-4 border-t border-border">
          <h3 className="text-sm font-medium flex items-center gap-2">
            <div className="h-6 w-1 bg-primary rounded-full" />
            Advanced
          </h3>
          {/* Fields */}
        </div>

        {/* Full-width actions */}
        <div className="flex flex-col gap-3 pt-4 border-t border-border pb-safe">
          <Button className="w-full">Save</Button>
          <Button variant="outline" className="w-full">Cancel</Button>
        </div>
      </div>
    );
  }

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab}>
      <TabsList>
        <TabsTrigger value="basic">Basic Info</TabsTrigger>
        <TabsTrigger value="advanced">Advanced</TabsTrigger>
      </TabsList>
      <TabsContent value="basic">{/* Fields */}</TabsContent>
      <TabsContent value="advanced">{/* Fields */}</TabsContent>
    </Tabs>
  );
}
```

**Mobile stacking features:** accent bars (`h-6 w-1 bg-primary`), border separators, single scroll area, full-width buttons, `pb-safe`.

---

## iOS Zoom Prevention

**This is handled globally — you do not have to remember it at every call site.** `app/globals.css` ends with **THE iOS ZOOM FLOOR**: an unlayered `@media (pointer: coarse)` rule that raises every `input` / `textarea` / `select` to `max(16px, 1em)` on touch devices. It is unlayered on purpose — Tailwind utilities live in `@layer utilities`, and only unlayered CSS can out-rank a `text-sm` utility. Desktop density is untouched.

What that means for you:

- A `text-sm` / `text-xs` field is no longer an iOS zoom bug. It is still desktop-density text that a phone user has to squint at, so **author fields as `text-base`** when the surface is used on mobile.
- **Do not "fix" a zoom report by re-disabling pinch-zoom.** See the paragraph below.
- The floor loses only to an inline `style={{ fontSize }}` (deliberate — it keeps code editors that size their own hidden textarea working). If you set an inline font size on a real text field, it must be ≥16px.
- `[contenteditable]` is NOT covered — forcing a size there re-scales a whole rich-text document. A contenteditable **composer** sets `text-base` itself.
- `data-no-zoom-floor` opts a field out. Only for a readonly/display field that can never take text-entry focus, and say why at the call site.

```tsx
// ✅ Authored for mobile — reads well AND never zooms
<Input className="text-base" />
<Textarea className="text-base" />

// ⚠️  Desktop density: the global floor stops the zoom, but this is small on a phone
<Input className="text-sm" />

// ❌ Inline size below the floor — beats the global rule, zooms the page
<Input style={{ fontSize: '13px' }} />
```

**History — why this exists:** the app shipped `userScalable: false, maximumScale: 1` from Nov 2025, which suppresses iOS focus-zoom as a side effect and hid ~450 sub-16px fields. Commit `d7ef647e` (2026-07-01) correctly restored pinch-zoom, and every one of those fields surfaced at once as "the page randomly zooms in". The floor is the fix; the viewport setting is not.

**Prevent input auto-zoom with ≥16px fonts ONLY — never by disabling pinch-zoom.** `app/config/viewport.ts` keeps `userScalable: true` (`maximumScale: 5`) on purpose: pinch-zoom is the user's universal escape hatch when any surface overflows. **Never set `userScalable: false` / `maximumScale: 1`** — it removes the only way out of a mobile lockout.

---

## Responsive Components

### Flex Layouts
```tsx
<div className="flex flex-col sm:flex-row gap-4">
<div className="flex flex-col sm:flex-row items-start sm:items-center">
<div className="flex flex-wrap gap-2">
```

### Conditional Display
```tsx
// Icon-only on mobile, icon+text on desktop
<Button>
  <Icon className="h-4 w-4 sm:mr-2" />
  <span className="hidden sm:inline">Label</span>
</Button>
```

### Touch Targets (44pt minimum)
```tsx
// ✅ Proper touch sizing
<Button variant="ghost" className="h-10 w-10 p-0">
  <Icon className="h-5 w-5" />
</Button>
<Switch className="scale-90 sm:scale-100" />

// ❌ Too small
<Button className="h-6 w-6 p-0">
```

### Responsive Widths
```tsx
<div className="w-full sm:w-48">
<SelectTrigger className="w-full sm:w-48">
```

### Spacing
```tsx
<div className="space-y-4 sm:space-y-6">
<div className="p-4 sm:p-6">
<div className="container mx-auto px-4 sm:px-6 lg:px-8">
```

### Grids
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
<div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-4">
```

### Typography
```tsx
<h1 className="text-[clamp(2rem,1.5rem+2vw,3.5rem)]">
<p className="text-[clamp(1rem,0.95rem+0.25vw,1.125rem)]">
<span className="truncate max-w-[150px] sm:max-w-none">
<p className="line-clamp-2">
```

---

## Nested Scrolling Prevention

```tsx
// ❌ Scroll trapping — user gets stuck in inner area
<div className="overflow-y-auto">
  <div className="overflow-y-auto max-h-[300px]">{/* Trap */}</div>
</div>

// ✅ Single scroll area — content flows naturally
<div className="overflow-y-auto">
  <div className="space-y-4">{/* All content */}</div>
</div>
```

---

## Component Audit Checklist

### Layout
- [ ] `dvh` not `vh`/`screen`; fixed bottom has `pb-safe`; header uses `--header-height`
- [ ] No nested scrolling; proper overflow management

### Dialogs & Modals
- [ ] Plain `<Dialog>` (it becomes a bottom sheet on mobile by itself); `mobileSheet={false}` only with a reason at the call site
- [ ] Hand-rolled Drawer (only when needed): `max-h-[85dvh]`, `overscroll-contain`, `pb-safe`
- [ ] Its `DialogContent` carries `matrx-touch-targets` (it portals out of the route subtree)

### Tabs & Sections
- [ ] Mobile: vertical stack with accent bars; Desktop: tabs OK (max 5)

### Inputs & Forms
- [ ] Mobile-facing inputs/textareas authored `text-base`; no inline `fontSize` below 16px (THE iOS ZOOM FLOOR handles zoom — never add an inline 16px just for it)

### Touch & Interaction
- [ ] Touch targets ≥44px via `matrx-touch-targets` on the section root (never `h-10`, which is 40px); hover-revealed controls also carry `pointer-coarse:opacity-100`
- [ ] Action buttons full-width on mobile

### Responsive
- [ ] `flex-col sm:flex-row`; icon-only buttons on mobile; spacing adjusts

---

## Decision Tree

```
Modal content needed?
├── Plain <Dialog> → centered card on desktop, bottom sheet on mobile, automatically
└── Drag handle or different mobile layout needed → explicit Drawer branch (max-h-[85dvh], pb-safe, overscroll-contain)

Multiple sections?
├── Mobile → Stack vertically (accent bars + border separators)
└── Desktop → Tabs OK

Scrollable content?
├── Mobile → Single scroll area only
└── Desktop → Nested OK but avoid when possible
```

---

## Project Conventions

```tsx
// Design tokens
<div className="bg-textured">    // Main backgrounds
<div className="bg-card">         // Cards

// Layout components
// The frame is AppShell (features/shell/components/AppShell.tsx) — every route group renders it.
import { FloatingSheet } from "@/components/official/FloatingSheet";
import { useIsMobile } from "@/hooks/use-mobile";

// Animations — CSS-first
<div className="transition-all duration-300 [@starting-style]:opacity-0 [@starting-style]:translate-y-4">
// Framer Motion only for gestures/physics
```
