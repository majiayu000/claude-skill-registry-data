---
name: real-prototype
description: >-
  Implement several variations of a design directly inside the running app, on
  the real page/route, with a live switcher to toggle between them in the browser,
  then recommend one and fold the winner into the real code. Variants are real
  implementations judged against real data, layout, and density (not an isolated
  mockup). Use this skill whenever the user wants to try design options live in the
  app, prototype changes directly on a real page, add a variant switcher, compare
  layouts in-context, asks to "build a few versions of this page", "try variants on
  the real screen", "switch between designs in the app", "implement this with a
  toggle", or says "real-prototype this". For a safe standalone .html copy that
  never touches the app, use the prototype skill instead.
---

# Real Prototype

Implement several variations **directly on the real page in the running app**,
wired to a live switcher so the user flips between them in the browser, judged
against the real header, sidebar, data, and density. Then recommend one and fold it
into the real code.

A standalone mockup is a vacuum: every option looks fine in isolation. This skill is
the opposite of that. The whole value is seeing variants **in context**. If the user
wants a safe standalone `.html` copy that never touches the app, use the
**prototype** skill instead.

## Principles

1. **Real route, real data, throwaway rendering.** Keep the existing data fetching,
   params, and auth on the page; only the *rendered* subtree swaps per variant. The
   wiring is throwaway; mark it clearly as a prototype.
2. **Read-only.** Variants must not fire real mutations — point any write at a stub.
   The question is "what should this look like", not "does the backend work".
3. **No new top-level structure.** Mount variants on the existing route, or inside
   the page that would naturally host the feature. Only create a throwaway route
   when the thing genuinely has no existing home, following the project's routing
   convention and with `prototype` in the path/name.
4. **Never ships to users.** Gate the switcher (and ideally the variant branching)
   out of production builds (`process.env.NODE_ENV !== 'production'` or the project's
   equivalent) so a stray merge can't reach users.

## Process

### 1. State the question and pick N

Default to **3 variants** (2 for a quick A/B, 4-5 when the space is wide open; cap at
5). Write the plan in one line, e.g. "Three variants of the settings page,
switchable via `?variant=` on the existing `/settings` route." Confirm the route and
granularity with the user if they're reachable.

### 2. Build structurally different variants

Draft each variant as its own component (`VariantA`, `VariantB`, ...), using the
project's real component library and styling system so they look native. Variants
must be **structurally different** — different layout, information hierarchy, or
primary affordance, not just different colors. Three tweaked card grids isn't a
prototype, it's wallpaper. If two come out similar, redo one with explicit "don't
reuse that layout" guidance.

### 3. Wire them onto the real route

Render the variant chosen by a `?variant=` URL search param, keeping all existing
data fetching above the switch so every variant sees the same real data:

```tsx
// pseudo-code — adapt to the project's framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A', 'B', 'C']} current={variant} />
  </>
);
```

### 4. Build the live switcher

A small fixed bar, visually distinct from the page (subtle shadow, comfortable
padding, rounded pill) so it's obviously not part of the design being judged. Three
parts: left arrow (previous, wraps), current variant label (key + name, e.g.
`B — Sidebar layout`), right arrow (next, wraps).

**Give it a frosted-glass (blur) background** so it reads as a floating control over
the page rather than a solid block that hides content behind it:

```css
.prototype-switcher {
  background: rgba(20, 20, 20, 0.55);     /* translucent; lighten for light UIs */
  backdrop-filter: blur(12px) saturate(120%);
  -webkit-backdrop-filter: blur(12px) saturate(120%);  /* Safari */
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 9999px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  color: #fff;
}
```

Tune the translucency/text color to the page (a darker pill on light pages, lighter
on dark) so the label stays readable. Keep the bar high-contrast enough to find at a
glance despite the blur. Provide a solid-ish fallback color for browsers without
`backdrop-filter`, so it never renders as an unreadable transparent strip.

**Position it where it stays out of the way:**

- **Default: fixed bottom-centre** (`position: fixed; bottom: 16px; left: 50%;
  transform: translateX(-50%)`), with a high `z-index` so it floats above page
  content. This is unobtrusive on most layouts and easy to reach.
- If the page already has something anchored bottom-centre (a sticky action bar,
  a chat launcher, a cookie banner, a mobile tab bar), move the switcher to a clear
  corner instead — **bottom-right** is the usual safe fallback, then bottom-left or
  top-right. Pick whichever corner the specific page leaves empty.
- Don't let it cover primary content or controls. If the layout is full-height with
  no free edge, make the bar compact and add a small offset, or let it be
  drag-repositionable as a last resort.
- Keep it fully visible at the target viewport(s) — check it doesn't collide with a
  mobile keyboard, safe-area insets, or a narrow-width layout.

- Clicking an arrow updates the URL search param via the framework's router
  (`router.replace` / `navigate`) so the variant is shareable and reload-stable.
- `←` / `→` keys also cycle, but don't intercept them while an `<input>`,
  `<textarea>`, or `[contenteditable]` is focused.
- Gate the whole bar out of production builds.
- Put it in one shared component so it's reusable.

### 5. Hand it over

Give the user the URL and the `?variant=` keys to flip through. Then recommend one:
be a critic, name each variant's real weakness, say why your pick wins in this
context, and explicitly invite the remix — "I want the header from B with the
sidebar from C" is usually the design they actually want.

### 6. Fold the winner in and clean up

Once a variant wins, record which and why (commit message, PR description, or a short
note). Then **delete the losing variants and the switcher**, and fold the winner into
the real page. Rewrite it to production standards as you fold it in: the variant was
built under prototype constraints (read-only, minimal error handling, throwaway
wiring). Don't leave variant components or the switcher rotting in the repo, and for
a throwaway route, promote the winner to a real route and delete the prototype one.

## Anti-patterns

- **Variants that differ only in color or copy.** Real variants disagree about
  structure.
- **Sharing too much between variants.** A shared `<Header>` is fine; a shared
  `<Layout>` defeats the point — each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Keep them read-only; stub any write.
- **Leaving the switcher shippable.** Gate it out of production.
- **Promoting prototype code straight to production.** Rewrite properly when folding
  the winner in.
- **An empty throwaway route when a real page exists.** Mount on the real route so
  variants are judged against real data.
