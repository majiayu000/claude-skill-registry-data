---
name: agent-browser
description: >
  Automates real browser interactions: navigating websites, clicking buttons,
  filling forms, taking screenshots, extracting data, and testing web apps.
  Activate whenever the user asks to open a URL, check how a page looks, fill
  out a form, scrape or extract content from a live page, record a demo video,
  debug a front-end issue visually, or run any task that requires a real
  browser rather than curl/fetch. Also activate when the user says "browse",
  "open this site", "screenshot", "check the UI", "test in the browser", or
  asks to interact with a web page in any way. Prefer this over WebFetch when
  the page requires JavaScript rendering, login, or multi-step interaction.
---

# Browser Automation with agent-browser

## How it works

`agent-browser` controls a headless Chromium instance. The core loop is:

1. **Open** a page.
2. **Snapshot** the accessibility tree to discover interactive elements. Each
   element gets a short ref like `@e1`.
3. **Act** on elements using their refs.
4. **Re-snapshot** after any action that changes the DOM (navigation, form
   submit, tab switch, dynamic content load).

Refs are ephemeral — they become stale after DOM changes. Always re-snapshot
before acting on a changed page.

```bash
agent-browser open https://example.com
agent-browser snapshot -i          # interactive elements only
agent-browser fill @e2 "hello"
agent-browser click @e3
agent-browser snapshot -i          # re-snapshot after click
```

---

## Choosing locators: refs vs semantic find

Use **refs** (`@e1`) by default — they are fast, unambiguous, and come directly
from `snapshot -i`. Use **semantic `find`** when:

- You know the label/text but have not taken a snapshot yet.
- You need to target an element by role, label, or visible text across
  page changes without re-snapshotting.
- You are writing a reusable automation sequence where refs would be fragile.

```bash
# Ref-based (preferred in interactive sessions)
agent-browser click @e3

# Semantic (useful for scripted flows)
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
```

---

## Common workflows

### Fill and submit a form

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Read the output: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i   # verify the result page
```

### Log in once, reuse the session

```bash
# Initial login
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later — skip login
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

### Record a polished demo video

Explore the page first (so you know which refs to use), then start recording
for a clean take. Recording creates a fresh context but preserves cookies and
storage from your session.

```bash
# Rehearse
agent-browser open https://app.example.com
agent-browser snapshot -i

# Record
agent-browser record start ./demo.webm      # captures from current page
agent-browser click @e1
agent-browser fill @e2 "demo input"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser record stop                    # saves video

agent-browser record restart ./take2.webm    # stop current + start fresh
```

### Extract data from a page

```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e4              # single element text
agent-browser get attr @e5 href         # link target
agent-browser get html @e6              # raw innerHTML
agent-browser get count ".product-card" # how many items matched
agent-browser eval "JSON.stringify([...document.querySelectorAll('.price')].map(e => e.textContent))"
```

### Take a screenshot or PDF

```bash
agent-browser screenshot              # to stdout (inline in conversation)
agent-browser screenshot page.png     # save to file
agent-browser screenshot --full       # full-page capture
agent-browser pdf output.pdf          # export as PDF
```

---

## When to re-snapshot

Re-snapshot (`agent-browser snapshot -i`) whenever:

- You clicked a link or submitted a form (page navigation).
- A button triggered dynamic content (modal, accordion, tab switch).
- You scrolled and expect lazy-loaded elements.
- An action returned an error about a stale ref.

You do **not** need to re-snapshot after `fill`, `type`, `hover`, `focus`, or
reading data with `get` — these do not change the element tree.

---

## Error recovery

| Symptom | Likely cause | Fix |
|---|---|---|
| "ref @eN not found" | Stale refs after DOM change | Re-snapshot, use new refs |
| Click does nothing | Element obscured or not yet visible | `scrollintoview @eN` then click, or `wait @eN` first |
| Page blank after open | SPA still loading | `wait --load networkidle` or `wait --text "expected"` |
| Cannot find element | Element inside iframe | `frame "#iframe-id"` then snapshot |
| Dialog blocking interaction | Unhandled alert/confirm | `dialog accept` or `dialog dismiss` |
| Need to debug visually | Headless mode hides UI | `open <url> --headed` to watch live |

---

## Command reference

### Navigation

```bash
agent-browser open <url>              # navigate (add --headed to see the browser)
agent-browser back                    # history back
agent-browser forward                 # history forward
agent-browser reload                  # reload page
agent-browser close                   # close browser
```

### Snapshot

```bash
agent-browser snapshot                # full accessibility tree
agent-browser snapshot -i             # interactive elements only (recommended)
agent-browser snapshot -c             # compact output
agent-browser snapshot -d 3           # limit tree depth
agent-browser snapshot -s "#main"     # scope to CSS selector
```

### Interactions

```bash
agent-browser click @e1               # click
agent-browser dblclick @e1            # double-click
agent-browser fill @e2 "text"         # clear field then type
agent-browser type @e2 "text"         # type without clearing
agent-browser press Enter             # press key
agent-browser press Control+a         # key combo
agent-browser keydown Shift           # hold key
agent-browser keyup Shift             # release key
agent-browser hover @e1               # hover
agent-browser focus @e1               # focus element
agent-browser check @e1               # check checkbox
agent-browser uncheck @e1             # uncheck checkbox
agent-browser select @e1 "value"      # select dropdown option
agent-browser scroll down 500         # scroll page
agent-browser scrollintoview @e1      # scroll element into view
agent-browser drag @e1 @e2            # drag and drop
agent-browser upload @e1 file.pdf     # upload file
```

### Read data

```bash
agent-browser get text @e1            # element text
agent-browser get html @e1            # innerHTML
agent-browser get value @e1           # input value
agent-browser get attr @e1 href       # attribute value
agent-browser get title               # page title
agent-browser get url                 # current URL
agent-browser get count ".item"       # count matching elements
agent-browser get box @e1             # bounding box
```

### Check state

```bash
agent-browser is visible @e1          # visibility check
agent-browser is enabled @e1          # enabled check
agent-browser is checked @e1          # checked state
```

### Wait

```bash
agent-browser wait @e1                # wait for element to appear
agent-browser wait 2000               # wait milliseconds
agent-browser wait --text "Success"   # wait for text on page
agent-browser wait --url "**/dash"    # wait for URL pattern
agent-browser wait --load networkidle # wait for network idle
agent-browser wait --fn "window.ready" # wait for JS condition
```

### Mouse (low-level)

```bash
agent-browser mouse move 100 200     # move cursor
agent-browser mouse down left        # press button
agent-browser mouse up left          # release button
agent-browser mouse wheel 100        # scroll wheel
```

### Browser settings

```bash
agent-browser set viewport 1920 1080     # viewport size
agent-browser set device "iPhone 14"     # device emulation
agent-browser set geo 37.77 -122.42      # geolocation
agent-browser set offline on             # offline mode
agent-browser set headers '{"X-Key":"v"}'# extra HTTP headers
agent-browser set credentials user pass  # HTTP basic auth
agent-browser set media dark             # color scheme
```

### Cookies and storage

```bash
agent-browser cookies                    # list cookies
agent-browser cookies set name value     # set cookie
agent-browser cookies clear              # clear cookies
agent-browser storage local              # list localStorage
agent-browser storage local key          # get key
agent-browser storage local set k v      # set key
agent-browser storage local clear        # clear all
```

### Network interception

```bash
agent-browser network route <url>              # intercept requests
agent-browser network route <url> --abort      # block requests
agent-browser network route <url> --body '{}'  # mock response
agent-browser network unroute [url]            # remove route
agent-browser network requests                 # list tracked requests
agent-browser network requests --filter api    # filter by pattern
```

### Tabs, frames, dialogs

```bash
agent-browser tab                    # list tabs
agent-browser tab new [url]          # open new tab
agent-browser tab 2                  # switch to tab
agent-browser tab close              # close tab
agent-browser window new             # new window
agent-browser frame "#iframe"        # switch to iframe
agent-browser frame main             # back to main frame
agent-browser dialog accept [text]   # accept alert/confirm/prompt
agent-browser dialog dismiss         # dismiss dialog
```

### JavaScript

```bash
agent-browser eval "document.title"  # run arbitrary JS
```

### Debugging

```bash
agent-browser open <url> --headed    # show visible browser window
agent-browser console                # view console messages
agent-browser console --clear        # clear console log
agent-browser errors                 # view page errors
agent-browser errors --clear         # clear error log
agent-browser highlight @e1          # visually highlight element
agent-browser trace start            # start trace recording
agent-browser trace stop trace.zip   # stop and save trace
agent-browser --cdp 9222 snapshot    # connect via CDP
```

### Sessions (parallel browsers)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

### JSON output

Add `--json` to any command for machine-readable output:

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```
