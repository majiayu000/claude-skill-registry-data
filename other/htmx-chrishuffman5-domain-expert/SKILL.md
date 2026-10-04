---
name: htmx
description: "Covers HTMX 2.x: the hypermedia-driven architecture (HATEOAS), HTML-over-the-wire approach, core attributes (hx-get, hx-post, hx-put, hx-patch, hx-delete), hx-trigger with event modifiers (delay, throttle, changed, once, revealed, intersect, polling), hx-target with CSS selectors (closest, find, next, previous), hx-swap strategies (innerHTML, outerHTML, beforeend, delete, none, morph), out-of-band swaps (hx-swap-oob), hx-boost for progressive enhancement, request/response header model, extensions (SSE, WebSocket, Idiomorph, response-targets, preload, loading-states, head-support), scripting companions (Alpine.js, Hyperscript), CSRF token handling, backend integration patterns (Django, Flask, Rails, ASP.NET, Go, FastAPI), and diagnostics. Use for \"HTMX\", \"htmx\", \"hx-get\", \"hx-post\", \"hx-swap\", \"hx-trigger\", \"hx-target\", \"HTML over the wire\", \"HATEOAS\", \"hx-boost\", \"htmx extension\" questions."
license: MIT
---

# HTMX

This skill covers HTMX 2.x, including:

- HATEOAS philosophy: server returns HTML, the DOM is the state, no client-side data model
- Core attributes: `hx-get`, `hx-post`, `hx-put`, `hx-patch`, `hx-delete`
- Trigger system: `hx-trigger` with event modifiers (delay, throttle, changed, once, revealed, intersect, polling)
- Targeting: `hx-target` with CSS selectors, `closest`, `find`, `next`, `previous`
- Swap strategies: `innerHTML`, `outerHTML`, `beforeend`, `afterbegin`, `beforebegin`, `afterend`, `delete`, `none`, morph via Idiomorph
- Out-of-band swaps: `hx-swap-oob` for updating multiple DOM elements from a single response
- Progressive enhancement: `hx-boost` for upgrading links and forms to AJAX
- Request/response header model: `HX-Request`, `HX-Trigger`, `HX-Redirect`, `HX-Reswap`, `HX-Retarget`
- Extensions: SSE, WebSocket, Idiomorph, response-targets, preload, loading-states, head-support
- Scripting companions: Alpine.js for client-side state, Hyperscript for behavior DSL
- Security: CSRF tokens, `selfRequestsOnly` (default true in 2.0), CSP compatibility
- Backend integration: Django, Flask, Rails, ASP.NET, Go, FastAPI, Laravel, Spring, Phoenix
- Diagnostics: `htmx.logAll()`, event listeners, Network tab inspection

HTMX is a hypermedia-driven library: the server controls application state by returning HTML fragments. The browser remains a hypermedia client.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request type:
   - **Swap/targeting issues** -- Load `references/architecture.md`
   - **Backend integration** -- Load `references/patterns/backend-integration.md`
   - **Progressive enhancement** -- Load `references/patterns/progressive-enhancement.md`
   - **Swap strategy selection** -- Load `references/patterns/swap-strategies.md`
   - **Debugging** -- Load `references/diagnostics.md`
   - **Best practices / design** -- Load `references/best-practices.md`

2. **Identify the backend** -- HTMX is backend-agnostic. Ask what server framework is in use (Django, Flask, Rails, ASP.NET, Go, etc.) to provide framework-specific examples.

3. **Load context** -- Read the relevant reference file for deep knowledge.

4. **Analyze** -- Apply hypermedia-driven reasoning. HTMX is not a SPA framework. Avoid recommending JSON APIs, client-side state management, or JavaScript-heavy patterns.

5. **Recommend** -- Provide actionable guidance with HTML + server-side examples. Prefer the simplest attribute combination that solves the problem.

6. **Verify** -- Suggest validation steps (browser DevTools Network tab, `htmx.logAll()`).

## Core Expertise

### Philosophy

HTMX extends HTML's native hypermedia controls. HTML already supports `<a>` (GET) and `<form>` (GET/POST). HTMX generalizes this: any element can issue any HTTP verb, any event can trigger a request, any element can be the target, and the response is always HTML.

No build step. No virtual DOM. No node_modules. A single ~15KB gzipped script.

Locality of behavior: `hx-get="/search"` on an `<input>` tells you everything about what it does. No tracing through JS files or component trees.

### Core Attributes

```html
hx-get="/endpoint"       hx-post="/endpoint"
hx-put="/endpoint"       hx-patch="/endpoint"
hx-delete="/endpoint"
```

### hx-trigger

Controls what event initiates the request. Default: `click` for most elements, `change` for inputs, `submit` for forms.

```html
hx-trigger="click"
hx-trigger="keyup changed delay:300ms"    <!-- debounce, only if changed -->
hx-trigger="click throttle:2s"            <!-- at most once per 2s -->
hx-trigger="click once"                    <!-- fires only first time -->
hx-trigger="load"                          <!-- on page load -->
hx-trigger="revealed"                      <!-- enters viewport -->
hx-trigger="intersect threshold:0.5"       <!-- 50% visible -->
hx-trigger="every 5s"                      <!-- polling -->
hx-trigger="click from:document"           <!-- listen on document -->
```

### hx-target

```html
hx-target="#result"            hx-target="this"
hx-target="closest div"       hx-target="find .child"
hx-target="next .sibling"     hx-target="previous .sibling"
```

### hx-swap

```html
hx-swap="innerHTML"       <!-- replace inner content (default) -->
hx-swap="outerHTML"        <!-- replace entire element -->
hx-swap="beforeend"        <!-- append as last child -->
hx-swap="afterbegin"       <!-- prepend as first child -->
hx-swap="delete"           <!-- delete target, ignore response -->
hx-swap="none"             <!-- no DOM change -->
```

Modifiers: `swap:500ms`, `settle:300ms`, `scroll:top`, `show:top`, `transition:true`.

### Out-of-Band Swaps

One response updates multiple DOM elements:

```html
<!-- Primary content swaps into hx-target -->
<div id="search-results"><p>Result 1</p></div>

<!-- OOB: swaps into matching IDs elsewhere in DOM -->
<span id="result-count" hx-swap-oob="true">2 results</span>
<div id="status-bar" hx-swap-oob="innerHTML">Search complete</div>
```

### hx-boost

Upgrades all `<a>` and `<form>` elements within scope to HTMX AJAX. Pages work without JavaScript; boost is layered on.

```html
<body hx-boost="true">
  <a href="/about">About</a>          <!-- AJAX navigation -->
  <form method="post" action="/save">  <!-- AJAX submit -->
</body>
```

### Request/Response Headers

HTMX sends: `HX-Request`, `HX-Trigger`, `HX-Target`, `HX-Current-URL`.

Server can respond with: `HX-Trigger` (fire events), `HX-Redirect`, `HX-Reswap`, `HX-Retarget`, `HX-Push-Url`, `HX-Refresh`.

HTTP 204 No Content: HTMX performs no swap.

### CSS Lifecycle Classes

- `htmx-request` -- on element while request is in-flight
- `htmx-settling` -- on new content during settle phase
- `htmx-swapping` -- on old content before swap

### Extensions

Extensions are separate scripts activated with `hx-ext`:

- **SSE**: `hx-ext="sse" sse-connect="/stream" sse-swap="message"`
- **WebSocket**: `hx-ext="ws" ws-connect="/ws/chat"`
- **Idiomorph**: `hx-ext="morph"` -- intelligent DOM merging preserving focus and state
- **response-targets**: Map HTTP status codes to different targets
- **preload**: Preload links on mouseenter
- **loading-states**: Automatic loading UI management
- **head-support**: Merge `<head>` content from responses

## Common Pitfalls

**1. Target element does not exist**
If `hx-target` references a nonexistent element, the swap silently fails. Use `htmx.logAll()` to see warnings.

**2. innerHTML vs outerHTML mismatch**
If the response returns a wrapper `<div id="target">` and the strategy is `innerHTML`, the ID appears twice in the DOM.

**3. OOB swap ID mismatch**
`hx-swap-oob` finds targets by ID. No error if no match is found.

**4. HTMX 2.0 selfRequestsOnly blocks cross-origin**
Default `true` in 2.0. Set `htmx.config.selfRequestsOnly = false` for cross-origin APIs.

**5. SSE/WS moved to extensions in 2.0**
`hx-sse` and `hx-ws` no longer built-in. Load the extension script.

**6. DELETE sends URL parameters in 2.0**
In 1.x DELETE used request body. In 2.0 it uses query parameters.

**7. Nested forms are invalid HTML**
Browsers ignore inner forms. HTMX cannot fix this.

**8. CSRF tokens not forwarded**
HTMX sends cookies but not CSRF tokens from meta tags. Set `hx-headers` on `<body>`.

**9. Third-party JS libraries need re-init after swap**
Use `htmx:afterSwap` event to reinitialize date pickers, tooltips, etc.

**10. Response not HTML**
If server returns JSON, HTMX inserts raw text. Verify Content-Type is `text/html`.

## Reference Files

- `references/architecture.md` -- Attributes, swap strategies, OOB, request/response model, extensions
- `references/best-practices.md` -- Progressive enhancement, backend integration, scripting companions, security
- `references/diagnostics.md` -- Request debugging, swap issues, extension conflicts

## Pattern Guides

- `references/patterns/swap-strategies.md` -- innerHTML vs outerHTML vs morph, OOB, infinite scroll
- `references/patterns/backend-integration.md` -- Django, Flask, Rails, ASP.NET, Go, FastAPI patterns
- `references/patterns/progressive-enhancement.md` -- hx-boost, graceful degradation
