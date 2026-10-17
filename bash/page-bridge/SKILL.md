---
name: page-bridge
description: Inject a floating toolbar into a running dev page so the user can point at elements and comment on them, and have that arrive as a live notification. Use when iterating on a UI together in the browser, when the user says "page bridge", or asks to show you which element they mean.
---

# Page bridge

A floating toolbar injected into any running dev page. The human clicks
elements or types a note; the agent gets notified with the selector, computed
styles, and surrounding HTML. Nothing is added to the project's source — the
widget is injected over CDP and disappears on reload.

## Prerequisites

The caller supplies all of these; this skill starts none of them.

| Needs                        | Why                                                                          |
| ---------------------------- | ---------------------------------------------------------------------------- |
| **Node >= 24**               | Runs `bridge.mjs` (the sink and the driver).                                 |
| **`playwright-cli` on PATH** | The only way the widget reaches the page — every command shells out to it.   |
| **A headed browser session** | The human has to see the toolbar to click it. Headless is pointless here.    |
| **A running page URL**       | Passed as an argument (see below); this skill never assumes a host or port.  |
| **A persistent Monitor**     | The sink's stdout is the event stream; without one, no notifications arrive. |
| `jq` (optional)              | Pretty-printing `bridge.mjs log`.                                            |

Getting the app running and `playwright-cli` attached is the caller's job — a
project's own run skill, the generic `run` skill, or plain
`playwright-cli open --headed <url>`. Run the plugin preflight first,
`${CLAUDE_PLUGIN_ROOT}/skills/playwright-cli/check.sh`; if it fails, stop and
relay its message. `bridge.mjs` itself also refuses to run, with the install
command, when `playwright-cli` is missing.

## Pieces

Both live in this skill's directory — run them via `$CLAUDE_SKILL_DIR`.

| File         | Role                                                                                                   |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `bridge.mjs` | Node sink + driver: `serve` / `open` / `inject` / `status` / `hide` / `show` / `log` / `stop`          |
| `bridge.js`  | The in-page widget (shadow DOM, so it cannot collide with app styles)                                  |

The sink's **stdout is the event stream** — one compact line per event. Run it
under a Monitor and every click in the page becomes a notification.

## Setup

**1. Start the sink in a persistent Monitor** — this is what delivers events:

```bash
# Monitor tool, persistent: true, description: "page-bridge events"
$CLAUDE_SKILL_DIR/bridge.mjs serve
```

Every line it prints is an event notification. No filter needed; it only ever
emits events (startup and errors go to stderr).

**2. Put the widget on the page.** `open` starts a headed browser on `<url>`
and installs the widget; `<url>` is whatever the caller is running — this skill
has no default:

```bash
$CLAUDE_SKILL_DIR/bridge.mjs open <url>
```

If `playwright-cli` already has the page open (a filled form, a logged-in
session), install into it instead; nothing is lost:

```bash
$CLAUDE_SKILL_DIR/bridge.mjs inject
```

Both register the loader as an init script on the browser context, so the
widget comes back on every reload, navigation, and new tab until the browser
closes.

Then tell the user the toolbar is the pill in the bottom-right corner.

## What the user can do

Clicking the **agent** pill opens the menu; the pill is draggable.

- **Pick an element** — hover to highlight, click to send. `Alt+P` does the same
  without the menu.
- **Pick several elements** — ctrl/⌘+click to accumulate, `Enter` to send.
- **Comment on an element** — pick, then type what should change. This is the
  useful one during design review: the agent gets the selector _and_ the intent.
- **Send a note** — freeform message, no element.
- **Send viewport + scroll** — for "it breaks at this width".

`Esc` cancels any pick.

## Reading events

The notification line is a summary. For the full record — computed styles,
`data-v-*` scope ids, 800 chars of `outerHTML`, the bounding box:

```bash
$CLAUDE_SKILL_DIR/bridge.mjs log 1 | jq .
```

Go from a picked element to source with its `dataAttrs`: a Vue `data-v-<hash>`
maps to exactly one SFC (`grep -rl 'data-v-<hash>'` against the build, or match
the class name), and `data-testid` usually names the component outright.

## Stop

```bash
$CLAUDE_SKILL_DIR/bridge.mjs stop   # then TaskStop the Monitor
```

Closing the browser is the caller's business, not this skill's.

## Notes

- **Screenshots**: `bridge.mjs hide` before `playwright-cli screenshot`, then
  `bridge.mjs show` — otherwise the toolbar is in the picture.
- The widget skips itself when picking, so its own buttons are never selectable.
- The sink's own port is `BRIDGE_PORT` (default 7788) — unrelated to the app's
  port. It and `BRIDGE_DIR` (default `page-bridge` in the OS temp directory, holds
  `events.jsonl`)
  only need overriding when 7788 is taken or two bridges run at once; set them
  in the environment of both `serve` and every other subcommand.
- `BRIDGE_SESSION` names the `playwright-cli` session (`-s=`) the driver talks
  to. Leave it unset to use the default session; set it when the caller opened
  the page under a named one.
- Injection uses a `<script>` tag. A dev server with a strict `script-src` CSP
  will block it — the console shows the violation and `inject` reports failure.
- The widget is re-fetched from the sink on every load, so editing `bridge.js`
  takes effect on the next page reload — nothing to re-register.
- Persistence is `playwright-cli run-code` calling
  `page.context().addInitScript(loader)` at runtime, followed by one `eval` of
  the loader for the page that is already showing.
- Adding an action is one entry in `ACTIONS` in `bridge.js`; the menu, the
  dispatch, and `window.__bridge.actions` all read from that list. Give
  `summarize()` in `bridge.mjs` a case for it so its notification line stays
  readable.
