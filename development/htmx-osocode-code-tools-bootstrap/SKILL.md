---
allowed-tools: Read, Write, Edit
description: 'Build server-driven web applications with HTMX.

  Use when implementing dynamic UIs with server-rendered HTML, streaming responses,
  or adding interactivity without heavy JS frameworks.

  Includes guidance on accessibility, performance pitfalls, and when HTMX is NOT the
  right choice.'
name: htmx
---

# HTMX Development

Build server-driven web applications using HTMX. This guide covers best practices, accessibility requirements, and honest guidance on when HTMX is—and isn't—the right choice.

## When to Use HTMX

HTMX excels when your application is primarily server-rendered and you want to add interactivity without adopting a full JavaScript framework.

### Good Fit ✓

| Use Case | Why HTMX Works |
|----------|----------------|
| Server-rendered apps (Django, FastAPI, Rails, Go) | Natural extension of existing templates |
| Content-heavy websites | SEO-friendly, fast initial load |
| CRUD applications | Simple request/response patterns |
| Streaming LLM/chatbot responses | SSE extension handles streaming well |
| Progressive enhancement of forms | Graceful degradation possible |
| Admin dashboards | Server handles complexity |
| Incremental modernization | Add to existing apps without rewrite |

### Poor Fit ✗

| Use Case | Why HTMX Struggles |
|----------|-------------------|
| Offline-first applications | Requires server for every interaction |
| Real-time collaborative editing | Needs complex client-side state sync |
| High-frequency interactions | Drawing tools, games—latency kills UX |
| Complex client-side state | No built-in state management |
| Apps needing separate mobile API | You'll duplicate endpoint logic |
| Instant feedback requirements | Network round-trip adds delay |

**Be honest with yourself:** If you need Redux/Zustand-style state management, you probably need React/Vue/Svelte instead.

## Core Attributes

### Request Methods

```html
<!-- GET request -->
<button hx-get="/api/data" hx-target="#results">Load</button>

<!-- POST with form data -->
<form hx-post="/api/submit" hx-target="#response">
  <input name="email" type="email" required>
  <button type="submit">Submit</button>
</form>

<!-- Other methods -->
<button hx-put="/api/item/1">Update</button>
<button hx-patch="/api/item/1">Partial Update</button>
<button hx-delete="/api/item/1" hx-confirm="Delete this item?">Delete</button>
```

### Targeting and Swapping

```html
<!-- Target another element -->
<button hx-get="/content" hx-target="#container">Load</button>
<div id="container"></div>

<!-- Swap strategies -->
<div hx-get="/data" hx-swap="innerHTML">Replace contents (default)</div>
<div hx-get="/data" hx-swap="outerHTML">Replace entire element</div>
<div hx-get="/data" hx-swap="beforeend">Append inside</div>
<div hx-get="/data" hx-swap="afterend">Insert after</div>

<!-- Swap modifiers -->
<div hx-get="/data" hx-swap="innerHTML swap:300ms settle:100ms">
  <!-- Delays for animations -->
</div>
```

### Triggers

```html
<!-- Default triggers: click (buttons), change (inputs), submit (forms) -->
<button hx-get="/data">Click triggered</button>

<!-- Custom triggers -->
<input hx-get="/search" hx-trigger="keyup changed delay:500ms" hx-target="#results">

<!-- Trigger modifiers -->
<div hx-get="/data" hx-trigger="click once">Fire once only</div>
<div hx-get="/data" hx-trigger="every 5s">Poll every 5 seconds</div>
<div hx-get="/data" hx-trigger="intersect">When scrolled into view</div>
<div hx-get="/data" hx-trigger="load">On page load</div>

<!-- Listen to other elements -->
<div hx-get="/data" hx-trigger="click from:#other-button">
  Triggered by #other-button
</div>
```

## Accessibility Requirements

HTMX does NOT automatically handle accessibility. You must implement these patterns.

### Focus Management

When content updates, manage focus explicitly:

```html
<!-- Server response should include autofocus or JS to manage focus -->
<div id="results" aria-live="polite">
  <!-- Updated content here -->
</div>
```

```python
# FastAPI example - return focus management in response
@app.get("/search")
async def search(q: str):
    results = await do_search(q)
    return f"""
    <div id="results" aria-live="polite">
        <p class="sr-only">{len(results)} results found</p>
        {render_results(results)}
    </div>
    """
```

### ARIA Live Regions

Announce dynamic content changes to screen readers:

```html
<!-- For important updates -->
<div id="notifications" aria-live="assertive" aria-atomic="true"></div>

<!-- For less critical updates -->
<div id="results" aria-live="polite"></div>

<!-- Indicate loading state -->
<div id="content" aria-busy="true">
  Loading...
</div>
```

### Loading States

```html
<!-- Indicate busy state during requests -->
<button hx-get="/data"
        hx-target="#results"
        hx-indicator="#spinner"
        aria-describedby="loading-status">
  Load Data
</button>

<span id="spinner" class="htmx-indicator" aria-hidden="true">
  <span class="sr-only" id="loading-status">Loading...</span>
  <!-- spinner icon -->
</span>
```

### Use Proper Interactive Elements

```html
<!-- BAD - div is not keyboard accessible -->
<div hx-get="/action" hx-trigger="click">Click me</div>

<!-- GOOD - button is focusable and announces as interactive -->
<button hx-get="/action">Click me</button>

<!-- If you must use a div, add proper attributes -->
<div hx-get="/action"
     hx-trigger="click, keydown[key=='Enter']"
     tabindex="0"
     role="button"
     aria-label="Perform action">
  Click me
</div>
```

### Screen Reader Announcements

```html
<!-- Visually hidden but announced -->
<style>
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }
</style>

<!-- In your response -->
<div id="results">
  <p class="sr-only">Search complete. 5 results found.</p>
  <!-- visible results -->
</div>
```

## Streaming with SSE (LLM/Chatbot Pattern)

HTMX's SSE extension is well-suited for streaming LLM responses.

### Setup

```html
<head>
  <script src="https://unpkg.com/htmx.org@2"></script>
  <script src="https://unpkg.com/htmx-ext-sse@2"></script>
</head>
```

### Client-Side Pattern

```html
<div id="chat-container">
  <div id="messages"></div>

  <form hx-post="/chat"
        hx-target="#messages"
        hx-swap="beforeend"
        hx-on::after-request="this.reset()">
    <input name="message" placeholder="Type a message..." autocomplete="off">
    <button type="submit">Send</button>
  </form>
</div>

<!-- SSE streaming response container -->
<div hx-ext="sse"
     sse-connect="/chat/stream"
     sse-swap="message"
     hx-target="#current-response"
     hx-swap="beforeend">
</div>

<div id="current-response"></div>
```

### Server-Side Pattern (FastAPI)

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI()

@app.post("/chat")
async def start_chat(message: str):
    # Return placeholder that will receive streamed content
    return f"""
    <div class="message user">{message}</div>
    <div class="message assistant" id="response-{uuid4()}">
      <div hx-ext="sse"
           sse-connect="/chat/stream?msg={quote(message)}"
           sse-swap="message"
           hx-swap="beforeend">
      </div>
    </div>
    """

@app.get("/chat/stream")
async def stream_response(msg: str):
    async def generate():
        # Stream from your LLM
        async for chunk in llm.stream(msg):
            # SSE format: data field with HTML content
            yield {
                "event": "message",
                "data": f"<span>{escape(chunk)}</span>"
            }
        # Signal completion
        yield {
            "event": "message",
            "data": '<span hx-swap-oob="true" id="status">Complete</span>'
        }

    return EventSourceResponse(generate())
```

### SSE Reconnection

HTMX SSE extension handles reconnection automatically with exponential backoff:

```html
<!-- Configure reconnection -->
<div hx-ext="sse"
     sse-connect="/events"
     sse-reconnect="5">  <!-- Retry up to 5 times -->
</div>
```

## Performance Pitfalls

### The "Pop-In" Problem

Over-fragmenting a page causes jarring visual updates:

```html
<!-- BAD - Too many separate requests -->
<div hx-get="/header" hx-trigger="load"></div>
<div hx-get="/sidebar" hx-trigger="load"></div>
<div hx-get="/content" hx-trigger="load"></div>
<div hx-get="/footer" hx-trigger="load"></div>
<!-- User sees parts "pop in" sequentially -->

<!-- GOOD - Single request, or initial server render -->
<div hx-get="/page-content" hx-trigger="load">
  <!-- Or better: render on initial page load -->
</div>
```

### Request Flooding

```html
<!-- BAD - Fires on every keystroke -->
<input hx-get="/search" hx-trigger="keyup">

<!-- GOOD - Debounce with delay -->
<input hx-get="/search" hx-trigger="keyup changed delay:300ms">

<!-- GOOD - Throttle for continuous events -->
<div hx-get="/position" hx-trigger="mousemove throttle:100ms">
```

### Request Cancellation Gotcha

By default, HTMX cancels in-flight requests when a new request is triggered on the same element:

```html
<!-- This can lose user input if they type quickly -->
<input hx-get="/search" hx-trigger="keyup delay:200ms">

<!-- Use hx-sync to control behavior -->
<input hx-get="/search"
       hx-trigger="keyup delay:200ms"
       hx-sync="this:replace">  <!-- Replace previous request -->
```

### Disable Elements During Requests

Prevent double-submission:

```html
<button hx-post="/submit" hx-disabled-elt="this">
  Submit
</button>

<!-- Disable multiple elements -->
<form hx-post="/submit" hx-disabled-elt="find button, find input">
  <input name="data">
  <button>Submit</button>
</form>
```

## Security

### Always Escape User Content

Server-side template escaping is critical:

```python
# FastAPI/Jinja2 - auto-escaping is ON by default
# But be careful with |safe filter

# BAD
return f"<div>{user_input}</div>"  # XSS vulnerability

# GOOD - use template with auto-escaping
return templates.TemplateResponse("result.html", {"content": user_input})
```

### CSRF Protection

Include CSRF tokens in all mutating requests:

```html
<!-- Add to <body> or <html> to include in all requests -->
<body hx-headers='{"X-CSRF-Token": "{{ csrf_token }}"}'>
```

```python
# FastAPI - verify token on server
@app.post("/submit")
async def submit(request: Request):
    token = request.headers.get("X-CSRF-Token")
    if not verify_csrf(token):
        raise HTTPException(403, "Invalid CSRF token")
```

### Restrict Request Origins

```javascript
// Only allow requests to same origin (default)
htmx.config.selfRequestsOnly = true;

// Disable inline script execution if serving untrusted content
htmx.config.allowScriptTags = false;
htmx.config.allowEval = false;
```

### Sensitive Pages

Exclude from browser history cache:

```html
<div hx-history="false">
  <!-- Sensitive content not cached in localStorage -->
</div>
```

## Progressive Enhancement

HTMX can degrade gracefully, but it requires intentional design:

```html
<!-- Form works with or without JavaScript -->
<form action="/search" method="GET"
      hx-get="/search"
      hx-target="#results"
      hx-push-url="true">
  <input name="q" placeholder="Search...">
  <button type="submit">Search</button>
</form>

<div id="results">
  <!-- Initial content or server-rendered results -->
</div>
```

```python
# Server detects HTMX requests and responds appropriately
@app.get("/search")
async def search(request: Request, q: str):
    results = await do_search(q)

    # HTMX request - return partial
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            "partials/results.html",
            {"results": results}
        )

    # Regular request - return full page
    return templates.TemplateResponse(
        "search.html",
        {"results": results, "query": q}
    )
```

## Common Patterns

### Infinite Scroll

```html
<div id="items">
  {% for item in items %}
    <div class="item">{{ item.name }}</div>
  {% endfor %}

  <div hx-get="/items?page={{ next_page }}"
       hx-trigger="intersect once"
       hx-swap="outerHTML">
    Loading more...
  </div>
</div>
```

### Inline Editing

```html
<div id="field-1">
  <span>{{ value }}</span>
  <button hx-get="/edit/1" hx-target="#field-1">Edit</button>
</div>

<!-- Response replaces with form -->
<form id="field-1" hx-put="/save/1" hx-target="this" hx-swap="outerHTML">
  <input name="value" value="{{ value }}">
  <button type="submit">Save</button>
  <button hx-get="/view/1" hx-target="#field-1">Cancel</button>
</form>
```

### Confirmation Dialogs

```html
<button hx-delete="/item/1"
        hx-confirm="Are you sure you want to delete this item?"
        hx-target="closest .item"
        hx-swap="outerHTML">
  Delete
</button>
```

### Out-of-Band Updates

Update multiple page sections from one response:

```html
<!-- Server response -->
<div id="main-content">
  Updated main content
</div>

<div id="notification" hx-swap-oob="true">
  Item saved successfully!
</div>

<div id="item-count" hx-swap-oob="innerHTML">
  42 items
</div>
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Using `<div>` for clickable elements | Not keyboard accessible | Use `<button>` or `<a>` |
| Omitting `aria-live` on dynamic regions | Screen readers miss updates | Add appropriate ARIA attributes |
| Loading every section via HTMX | Pop-in effect, slow perceived load | Server-render initial content |
| No debounce on text inputs | Request flooding | Use `delay:Xms` modifier |
| Ignoring `hx-disabled-elt` | Double submissions | Disable during requests |
| Raw string interpolation | XSS vulnerabilities | Use template auto-escaping |
| Missing CSRF tokens | Security vulnerability | Include in `hx-headers` |
| Fighting React/Vue for DOM control | Conflicts and bugs | Choose one approach per page section |
