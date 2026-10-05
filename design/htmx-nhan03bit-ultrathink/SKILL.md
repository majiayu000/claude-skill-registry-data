---
name: htmx
description: HTMX hypermedia-driven development with hx-get, hx-post, hx-swap, hx-trigger, out-of-band swaps, boosting, extensions, and minimal JS patterns
layer: domain
category: frontend
triggers:
  - "htmx"
  - "hx-get"
  - "hx-post"
  - "hx-swap"
  - "hypermedia"
  - "htmx pattern"
  - "html over the wire"
  - "minimal javascript"
inputs:
  - Interaction pattern (form, search, infinite scroll, modal)
  - Server framework (Express, FastAPI, Go, Rails)
  - Progressive enhancement requirements
outputs:
  - HTMX attribute markup
  - Server endpoint returning HTML partials
  - Extension configurations
linksTo:
  - nodejs
  - fastapi
  - django
  - forms
linkedFrom:
  - api-designer
  - ui-ux-pro
preferredNextSkills:
  - forms
  - css-architecture
fallbackSkills:
  - react
  - vue
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# HTMX Hypermedia Skill

## Purpose

Build dynamic web interfaces by returning HTML from the server instead of JSON. HTMX extends HTML with attributes for AJAX requests, CSS transitions, and WebSocket/SSE connections -- no build step, no virtual DOM, no client-side routing.

## Core Philosophy

```
Server returns HTML partials, not JSON.
The browser is the template engine.
Hypermedia is the engine of application state (HATEOAS).
```

## Installation

```html
<!-- CDN (recommended for simplicity) -->
<script src="https://unpkg.com/htmx.org@2.0.4"></script>

<!-- Or npm for bundled projects -->
<!-- npm i htmx.org -->
```

## Core Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `hx-get` | GET request | `hx-get="/api/users"` |
| `hx-post` | POST request | `hx-post="/api/users"` |
| `hx-put` | PUT request | `hx-put="/api/users/1"` |
| `hx-delete` | DELETE request | `hx-delete="/api/users/1"` |
| `hx-swap` | How to swap content | `hx-swap="innerHTML"` |
| `hx-target` | Where to place response | `hx-target="#results"` |
| `hx-trigger` | What triggers the request | `hx-trigger="click"` |
| `hx-indicator` | Loading indicator | `hx-indicator="#spinner"` |
| `hx-push-url` | Update browser URL | `hx-push-url="true"` |
| `hx-select` | Pick fragment from response | `hx-select="#content"` |
| `hx-vals` | Include extra values | `hx-vals='{"key":"val"}'` |

## Key Patterns

### 1. Click-to-Load Content

```html
<button hx-get="/api/users"
        hx-target="#user-list"
        hx-swap="innerHTML"
        hx-indicator="#spinner">
  Load Users
</button>
<span id="spinner" class="htmx-indicator">Loading...</span>
<div id="user-list"></div>
```

Server returns an HTML fragment:
```html
<!-- GET /api/users response -->
<ul>
  <li>Alice <button hx-delete="/api/users/1" hx-target="closest li" hx-swap="outerHTML">Delete</button></li>
  <li>Bob <button hx-delete="/api/users/2" hx-target="closest li" hx-swap="outerHTML">Delete</button></li>
</ul>
```

### 2. Live Search with Debounce

```html
<input type="search" name="q"
       hx-get="/api/search"
       hx-target="#results"
       hx-trigger="input changed delay:300ms"
       hx-indicator="#search-spinner"
       placeholder="Search..." />
<div id="results"></div>
```

```python
# FastAPI server endpoint
@app.get("/api/search")
async def search(q: str = ""):
    results = await db.search(q)
    rows = "".join(f"<li>{r.title}</li>" for r in results)
    return HTMLResponse(f"<ul>{rows}</ul>" if rows else "<p>No results found.</p>")
```

### 3. Inline Editing

```html
<!-- Display mode -->
<div id="name-display" hx-get="/api/users/1/edit" hx-trigger="dblclick" hx-swap="outerHTML">
  <span>Alice Johnson</span>
</div>

<!-- Edit mode (returned by GET /api/users/1/edit) -->
<form id="name-display" hx-put="/api/users/1" hx-swap="outerHTML">
  <input name="name" value="Alice Johnson" autofocus />
  <button type="submit">Save</button>
  <button hx-get="/api/users/1/display" hx-swap="outerHTML" hx-target="#name-display">Cancel</button>
</form>
```

### 4. Infinite Scroll

```html
<div id="feed">
  <!-- Initial items -->
  <div class="item">Post 1</div>
  <div class="item">Post 2</div>

  <!-- Sentinel element triggers load when visible -->
  <div hx-get="/api/feed?page=2"
       hx-trigger="revealed"
       hx-swap="outerHTML"
       hx-indicator="#load-more-spinner">
    <span id="load-more-spinner" class="htmx-indicator">Loading more...</span>
  </div>
</div>
```

Server response replaces the sentinel with new items and a new sentinel:
```html
<div class="item">Post 3</div>
<div class="item">Post 4</div>
<div hx-get="/api/feed?page=3" hx-trigger="revealed" hx-swap="outerHTML">
  <span class="htmx-indicator">Loading more...</span>
</div>
```

### 5. Out-of-Band (OOB) Swaps

Update multiple parts of the page from a single response:

```html
<!-- Main response swaps into hx-target as usual -->
<div id="notification-count" hx-swap-oob="innerHTML">3</div>
<div id="main-content">
  <p>Item created successfully!</p>
</div>
```

### 6. Boosted Navigation (SPA-like Feel)

```html
<!-- Boost all links in nav to use AJAX instead of full page load -->
<nav hx-boost="true">
  <a href="/dashboard">Dashboard</a>
  <a href="/settings">Settings</a>
  <a href="/profile">Profile</a>
</nav>
```

## Swap Modes Reference

| Mode | Behavior |
|------|----------|
| `innerHTML` | Replace inner content (default) |
| `outerHTML` | Replace entire target element |
| `beforebegin` | Insert before the target |
| `afterbegin` | Insert inside target, before first child |
| `beforeend` | Insert inside target, after last child |
| `afterend` | Insert after the target |
| `delete` | Delete the target element |
| `none` | No swap (fire-and-forget) |

## Best Practices

1. **Return HTML partials**, not full pages -- only the fragment that changed
2. **Use `hx-indicator`** on every user-triggered request for perceived performance
3. **Add `delay:300ms`** on search inputs to avoid excessive requests
4. **Use `hx-push-url`** for navigable pages so browser back/forward works
5. **Prefer `outerHTML` swap** for replaceable components -- avoids wrapper div pollution
6. **Use OOB swaps** to update counters, notifications, and other page regions from any response
7. **Progressively enhance** -- forms should work without JS, then HTMX enhances them

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Returning full HTML pages | Entire page re-rendered in target | Return only the partial fragment |
| Missing CSRF token | POST/PUT/DELETE rejected | Include token via `hx-headers` or meta tag |
| No loading indicators | UI feels broken during slow requests | Always use `hx-indicator` |
| Forgetting `hx-swap-oob` IDs must exist | OOB swap silently fails | Ensure target element exists in the DOM |
| Not setting `hx-push-url` | Users cannot bookmark or share URLs | Add on navigation-like requests |
