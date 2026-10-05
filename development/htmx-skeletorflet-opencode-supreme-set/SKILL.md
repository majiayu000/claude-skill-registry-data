---
name: htmx
description: HTMX hypermedia-driven interactions, HX-* attributes, and backend integration patterns. Use when building dynamic web UIs with minimal JavaScript and server-rendered HTML.
---

## htmx

### Core Concepts
- Core attributes: hx-get, hx-post, hx-put, hx-delete, hx-patch for AJAX
- Triggers: hx-trigger (click, change, load, reveal, intersect, every)
- Target swapping: hx-target, hx-swap (innerHTML, outerHTML, beforebegin, afterend)
- Indicators: hx-indicator and hx-request for loading states
- History: hx-push-url and hx-replace-url for URL management

### Common Patterns
- Infinite scroll with hx-trigger="revealed" on last list item
- Form submission with hx-post and hx-target for inline validation
- Lazy loading with hx-trigger="load" for below-fold content
- Polling with hx-trigger="every 5s" for live data updates
- Delete button with hx-delete and hx-confirm for confirmation

### Best Practices
- Return HTML fragments from server, never JSON for HTMX routes
- Use hx-swap-oob for updating multiple parts of page at once
- Combine with Alpine.js for complex client-side interactions
- Set HX-Request header detection on server for partial vs full responses
- Use hx-boost for converting all links/forms to AJAX

### Common Code Patterns
- Search input with hx-get, hx-trigger="keyup delay:300ms", hx-target="#results"
- Todo list with hx-post form, hx-target="#todo-list", hx-swap="beforeend"
- Modal with hx-get loading content and hx-swap="innerHTML" on dialog
