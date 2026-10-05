---
name: review-frontend
description: Use when reviewing, debugging, or improving frontend code in this repo (website/ HTML, CSS, JS, service workers, PWA assets) or when asked to "review frontend", "revisa el html/css", "review JS", or "audita el frontend". Reviews for correctness, browser compatibility, accessibility, performance, security (XSS), responsive behavior, and PWA/service-worker correctness, and ends with a "what a user/reviewer would catch" pass.
---

# Frontend Review (HTML / CSS / JavaScript)

You review frontend code like a user, a screen-reader user, a security
reviewer, and a mobile browser all at once. You assume the site will be opened
on a slow phone with a screen reader, and that every input is hostile.

## Steps

1. **Read all files in scope** (HTML, CSS, JS, service worker) as a unit —
   the bug is usually in the interaction between them.
2. **Check the structure mechanically** — for JS, `node --check file.js` for
   syntax; look for unbalanced tags, missing closing braces, undefined
   functions used. Note the repo has no build step: the browser runs these
   files as-is.
3. **Review the dimensions below.**
4. **Scenario pass** — think like a user on a phone, on an old browser, with
   JS disabled, offline, with a screen reader.
5. **Report** in the output format at the bottom.

## Review dimensions

1. **Correctness** — does the JS do what it claims? Right element selected,
   right event wiring, no `null`/`undefined` access, no stale references after
   DOM changes. Watch for code that only works when scripts load in one order.
2. **Security (XSS and injection)** — never insert untrusted text into the DOM
   via `innerHTML`/`outerHTML`/`insertAdjacentHTML` or `document.write`.
   Use `textContent` for data. Escape `URLSearchParams`/`location.hash` values
   before rendering. Check every place user/URL/query data reaches the DOM.
3. **Accessibility** — semantic HTML (`<nav>`, `<main>`, headings in order),
   `alt` text on images, labels tied to inputs, keyboard navigability, focus
   states visible, `aria` used correctly and not overused, contrast meets
   WCAG AA, no content-only-on-hover. A screen reader must be able to use the
   site.
4. **Performance** — render-blocking scripts, image sizes, no layout thrash
   (DOM writes between reads), passive listeners for scroll/touch, no
   unbounded DOM growth, `requestAnimationFrame` for visual work, caching
   headers/service-worker strategies sensible for static content.
5. **Responsive/mobile** — viewport meta present, no fixed pixel widths that
   break on small screens, touch targets large enough, media queries testable,
   horizontal overflow from long content.
6. **Browser compatibility** — features used are supported or guarded
   (`IntersectionObserver`, optional chaining `?.`, `fetch`) with graceful
   fallbacks; old browsers degrade, not crash.
7. **Service worker / PWA correctness** — correct scope, cache versioning
   (bump or the new version never ships), no stale-cache-after-update bug,
   offline fallback sane, no aggressive cache-first for HTML that goes stale,
   `sw-precache.js`/`sw.js` strategy matches the asset list.
8. **Robustness** — JS fails gracefully if an element or API is missing; no
   `try/catch` that swallows real errors; network errors handled (not just
   `.catch(console.error)`).

## Scenario checklist (the superpower)

- **Screen reader** — can a non-sighted user complete the core task?
- **Phone + slow network** — what does it look like at 3G with a 2s
  first-paint?
- **JS disabled** — is content readable and links working?
- **Offline** — does the service worker serve something useful?
- **Hostile input** — paste `<img src=x onerror=alert(1)>` into every input
  and URL param: does it render or execute?
- **Old browser** — does it crash or degrade?

## Output format

- **Verdict** — per-dimension pass/fail.
- **Issues** prioritized:
  - **Critical** — XSS, broken core interaction, service worker serving stale
    content forever, inaccessible core path.
  - **Important** — performance problems, missing fallbacks, a11y gaps,
    unhandled errors.
  - **Style** — consistency, naming, cleanup.
  Each with `file:line`, the problem, and the fix as a code snippet.
- **Scenario results** — how the site behaves in each scenario above.
- When asked to fix, apply edits and re-check the touched files (syntax check,
  re-trace the scenario) before reporting done.
