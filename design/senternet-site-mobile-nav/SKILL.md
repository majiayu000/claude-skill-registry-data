---
name: senternet-site-mobile-nav
description: Collapse the desktop header nav into a hamburger menu on mobile, with support for nested section anchors.
---

# Mobile Navigation

Turn the site's horizontal header nav into a hamburger-driven panel below the `md` breakpoint, with body scroll locked while open and auto-close on navigation. Optionally support a top-level link that exposes its page's sections as a dropdown on desktop and an inline expanded list on mobile.

## The problem this solves

Desktop horizontal navs overflow or wrap awkwardly on phones. We want one `Layout.tsx` that:

- Renders a normal horizontal nav at `md+`
- Renders a hamburger button below `md` that toggles a full-width panel under the sticky header
- Locks body scroll while the panel is open so iOS doesn't scroll the page behind it
- Closes automatically when the user navigates (pathname OR hash change)
- Stays accessible: `aria-label`, `aria-expanded`, `aria-controls`, and `role="menu"` on dropdowns

## Patterns

### Pattern 1: Tailwind breakpoint split

The desktop nav uses `hidden md:flex` and the hamburger button uses `md:hidden`. They live as siblings inside the header bar so only one is ever visible.

```tsx
<header className="sticky top-0 z-20 border-b border-[var(--color-border)] bg-white/90 backdrop-blur-md">
  <div className="max-w-5xl mx-auto px-6 h-20 flex items-center justify-between">
    <Link to="/" className="flex items-center gap-2.5">
      <img src={logo} alt="Site name" className="h-14 w-auto" />
    </Link>

    {/* Desktop nav */}
    <nav className="hidden md:flex items-center gap-6">
      {/* links here */}
    </nav>

    {/* Mobile hamburger */}
    <button className="md:hidden ..." />
  </div>
</header>
```

Use the site's CSS variables (`var(--color-brand)`, `var(--color-text)`, `var(--color-text-muted)`, `var(--color-border)`, `var(--color-bg)`) so colors track the design system, not hard-coded hex values.

### Pattern 2: State and auto-close on navigation

`useState` for the open/closed flag, and a `useEffect` that watches BOTH `pathname` and `hash` from `react-router-dom`'s `useLocation`. Watching only `pathname` leaves the menu open when the user taps a hash-anchor link, because the same route is still mounted.

```tsx
import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'

const { pathname, hash } = useLocation()
const [mobileOpen, setMobileOpen] = useState(false)

useEffect(() => {
  setMobileOpen(false)
}, [pathname, hash])
```

### Pattern 3: Body scroll lock

Lock the document body while the menu is open and restore the previous value on cleanup. This is what prevents the page from scrolling behind the open panel on iOS.

```tsx
useEffect(() => {
  if (!mobileOpen) return
  const prev = document.body.style.overflow
  document.body.style.overflow = 'hidden'
  return () => {
    document.body.style.overflow = prev
  }
}, [mobileOpen])
```

### Pattern 4: Hamburger button (icon swap)

A single button that swaps between three lines and an X based on state. Inline SVG keeps it dependency-free and themable via `currentColor`.

```tsx
<button
  type="button"
  aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
  aria-expanded={mobileOpen}
  aria-controls="mobile-menu"
  onClick={() => setMobileOpen((v) => !v)}
  className="md:hidden inline-flex items-center justify-center w-10 h-10 rounded-lg text-[var(--color-text)] hover:bg-[var(--color-bg)] transition-colors"
>
  <svg aria-hidden="true" className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    {mobileOpen ? (
      <>
        <line x1="6" y1="6" x2="18" y2="18" />
        <line x1="6" y1="18" x2="18" y2="6" />
      </>
    ) : (
      <>
        <line x1="4" y1="7" x2="20" y2="7" />
        <line x1="4" y1="12" x2="20" y2="12" />
        <line x1="4" y1="17" x2="20" y2="17" />
      </>
    )}
  </svg>
</button>
```

### Pattern 5: Mobile panel

The panel sits inside the sticky `<header>` (so the page can scroll independently below it) and is hidden at `md+`. Cap its height to the viewport so long nav lists don't overflow off-screen.

```tsx
{mobileOpen && (
  <div
    id="mobile-menu"
    className="md:hidden border-t border-[var(--color-border)] bg-white max-h-[calc(100vh-5rem)] overflow-y-auto"
  >
    <nav className="px-6 py-4 flex flex-col">
      {/* links here with py-3 text-base font-medium */}
      <a className="mt-3 text-center px-4 py-3 bg-[var(--color-brand)] hover:bg-[var(--color-brand-hover)] text-white rounded-lg font-semibold shadow-[var(--shadow-soft)]">
        {/* primary CTA */}
      </a>
    </nav>
  </div>
)}
```

The `calc(100vh-5rem)` matches the `h-20` (5rem) header. If the header height changes, update both.

### Pattern 6: Nested section sub-menu (optional)

When one top-level link has page sections worth jumping to (e.g., a long About page), drive both desktop dropdown and mobile inline list from one array constant.

```tsx
const aboutSections = [
  { hash: 'fragmentation', label: 'The fragmentation problem' },
  { hash: 'solution', label: 'What we do' },
  // ...
]
```

**Desktop:** hover-triggered dropdown using `group` + `group-hover` with a chevron that rotates on hover.

```tsx
<div className="relative group">
  <Link to="/about" className="inline-flex items-center gap-1 py-2 ...">
    About
    <svg
      aria-hidden="true"
      className="w-3 h-3 transition-transform group-hover:rotate-180"
      viewBox="0 0 12 12" fill="none" stroke="currentColor"
      strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"
    >
      <path d="M3 4.5L6 7.5L9 4.5" />
    </svg>
  </Link>
  <div
    className="absolute left-1/2 -translate-x-1/2 top-full pt-2 w-64 invisible opacity-0 translate-y-1 group-hover:visible group-hover:opacity-100 group-hover:translate-y-0 focus-within:visible focus-within:opacity-100 focus-within:translate-y-0 transition-all duration-150 z-20"
    role="menu"
  >
    <div className="rounded-xl border border-[var(--color-border)] bg-white shadow-[var(--shadow-card)] py-2">
      {aboutSections.map((s) => (
        <Link key={s.hash} to={`/about#${s.hash}`} role="menuitem" className="block px-4 py-2 text-sm text-[var(--color-text-muted)] hover:text-[var(--color-brand)] hover:bg-[var(--color-bg)] transition-colors">
          {s.label}
        </Link>
      ))}
    </div>
  </div>
</div>
```

The `pt-2` gap (instead of `mt-2`) keeps the dropdown's hover area continuous with the trigger so the menu doesn't snap shut between the link and the panel.

**Mobile:** the sub-list is collapsed by default and toggled with a right-side chevron button. The parent row splits into two zones — the `<Link>` on the left (still navigates to the parent route) and a separate `<button>` on the right that only toggles expansion. This keeps tap targets unambiguous on touch devices.

Track expansion with an accordion state (only one submenu open at a time), and reset it when the mobile menu closes or the route/hash changes:

```tsx
const [expandedSubmenu, setExpandedSubmenu] = useState<'about' | 'features' | null>(null)

useEffect(() => {
  setMobileOpen(false)
  setExpandedSubmenu(null)
}, [pathname, hash])

useEffect(() => {
  if (!mobileOpen) setExpandedSubmenu(null)
}, [mobileOpen])

const toggleSubmenu = (key: 'about' | 'features') =>
  setExpandedSubmenu((cur) => (cur === key ? null : key))
```

Then in the mobile panel:

```tsx
<div className="flex items-center justify-between">
  <Link
    to="/about"
    className={`flex-1 py-3 text-base font-medium ${
      pathname === '/about' ? 'text-[var(--color-brand)]' : 'text-[var(--color-text)]'
    }`}
  >
    About
  </Link>
  <button
    type="button"
    aria-label={expandedSubmenu === 'about' ? 'Collapse About submenu' : 'Expand About submenu'}
    aria-expanded={expandedSubmenu === 'about'}
    onClick={() => toggleSubmenu('about')}
    className="p-2 -mr-2 text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors"
  >
    <svg
      aria-hidden="true"
      className={`w-4 h-4 transition-transform ${expandedSubmenu === 'about' ? 'rotate-180' : ''}`}
      viewBox="0 0 12 12" fill="none" stroke="currentColor"
      strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round"
    >
      <path d="M3 4.5L6 7.5L9 4.5" />
    </svg>
  </button>
</div>
{expandedSubmenu === 'about' && (
  <div className="pl-4 border-l-2 border-[var(--color-border)] ml-1 mb-2">
    {aboutSections.map((s) => (
      <Link key={s.hash} to={`/about#${s.hash}`} className="block py-2 text-sm text-[var(--color-text-muted)] hover:text-[var(--color-brand)] transition-colors">
        {s.label}
      </Link>
    ))}
  </div>
)}
```

The `-mr-2` offsets the button's internal padding so its visual edge aligns with the rest of the menu. The `flex-1` on the `<Link>` makes the entire left zone tappable for navigation, leaving the chevron's hit area dedicated to the toggle.

### Pattern 7: Hash anchor scrolling

The hash-anchor sub-menu items rely on a `ScrollToTop` that scrolls to the hash target when present. Update the standard `ScrollToTop` in `src/App.tsx`:

```tsx
function ScrollToTop() {
  const { pathname, hash } = useLocation()
  useEffect(() => {
    if (hash) {
      const el = document.getElementById(hash.slice(1))
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' })
        return
      }
    }
    window.scrollTo(0, 0)
  }, [pathname, hash])
  return null
}
```

Add `scroll-mt-32` (or another value matching the sticky header height) to every target section so the heading isn't hidden behind the sticky header after scroll-into-view:

```tsx
<section id="fragmentation" className="scroll-mt-32">...</section>
```

## Checklist

- [ ] Desktop nav uses `hidden md:flex`; hamburger uses `md:hidden`
- [ ] Header has `z-20` so the panel sits above the page; mobile panel uses `id="mobile-menu"`
- [ ] Hamburger button has `aria-label`, `aria-expanded`, `aria-controls="mobile-menu"`
- [ ] Open/close state is `useState`, auto-closes on `[pathname, hash]` change
- [ ] Body scroll is locked with `document.body.style.overflow = 'hidden'` and restored on cleanup
- [ ] Mobile panel is capped at `max-h-[calc(100vh-5rem)]` and `overflow-y-auto`
- [ ] All colors reference CSS variables (`var(--color-brand)`, `var(--color-text-muted)`, etc.)
- [ ] If a top-level link has a nested sub-menu: both desktop dropdown and mobile collapsible list are driven from one array
- [ ] Mobile sub-lists default to collapsed and expand via a right-side chevron button (separate from the parent `<Link>`); `aria-expanded` on the toggle button matches state; only one submenu open at a time; resets to collapsed on menu close and on route/hash change
- [ ] If using hash anchors: `ScrollToTop` watches `hash` and target sections have `scroll-mt-*` matching the sticky header

## Testing

Chrome DevTools device toolbar at iPhone width (e.g., iPhone 14):

1. Tap the hamburger. Confirm the icon swaps to an X and the panel slides under the header.
2. Try to scroll the page underneath the open panel. The body should NOT scroll.
3. Tap any nav link. The menu should close and the route should change.
4. Tap a parent with a sub-menu (e.g., About). The link area should navigate to `/about`. Re-open the menu and tap the chevron next to "About" — the sub-list should expand, the chevron should rotate, and tapping it again (or expanding the other sub-menu) should collapse it.
5. With the About sub-list expanded, tap any sub-section anchor. The page should scroll to that section with the heading visible (not clipped under the sticky header), and the menu (plus expansion state) should reset.
6. Resize past the `md` breakpoint. The hamburger should disappear and the horizontal nav should return.
7. Lighthouse mobile accessibility audit should still pass (hamburger and chevron buttons each have an accessible name, expanded state, and target tap area ≥ 44×44 px).

## Framework: Next.js track

The markup, breakpoints, scroll-lock, and nested-anchor behavior are unchanged. Two adjustments:

- The nav is stateful, so it must be a `'use client'` component — but keep it a *leaf*. Extract just the toggle and panel into `components/MobileNav.tsx` with the directive, and leave `app/layout.tsx` and the surrounding header as server components. Marking the layout `'use client'` to get a hamburger working ships the entire site to the browser.
- Use `<Link>` from `next/link` for nav links, and close the menu on route change by keying an effect on `usePathname()` — client-side navigation does not unmount the nav, so without this the panel stays open over the new page.

See `/senternet-site-framework` for the full convention map.
