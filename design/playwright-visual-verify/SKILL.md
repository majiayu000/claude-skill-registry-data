---
name: playwright-visual-verify
description: "Use the Playwright MCP to verify the visual appearance of the site under development. Triggers on: questions about appearance, layout, UX, after editing CSS/tokens or UI components with visual impact, debugging 'why does it look like this', wanting to check interactions (click, scroll, language switch), or wanting a real screenshot. Rule: navigate to the dev server first (usually http://localhost:5173), then act — use snapshot for logical verification and screenshot for visual verification. Always use `wait_for` after navigation before acting."
---

# Skill: Visual verify via Playwright MCP

## When to use

- User reports a visual bug ("hero is too low", "submit button is in the wrong position", "looks odd on mobile")
- After a CSS / tokens.css / public.css / dashboard.css edit
- After editing a `.svelte` component whose markup affects rendered output
- After i18n changes (verify the language toggle actually changes text)
- After form changes (verify inputs render, error states visible)
- After admin gating changes (verify unauthenticated redirect)
- When verifying that a refactor (e.g., removing a `<div>` wrapper, removing a `variant` prop) doesn't visually break things

Generally NOT needed for pure type / dead-code / log changes.

## Setup: dev server

The dev server is at `http://localhost:5173` (Vite default). Check that the user has it running. If unclear, ask:

```
Is there a dev server running? If not, run `pnpm dev` in frontend/.
```

Do NOT start the dev server yourself — the user may have an active process on that port.

## Tool map

| Goal | Tool | Notes |
|---|---|---|
| Get DOM tree / accessibility snapshot | `playwright_browser_snapshot` | Cheap, structural. Default for "what's on the page" |
| See rendered pixels | `playwright_browser_take_screenshot` | png default. Use to verify visual changes. |
| Click | `playwright_browser_click` | Pass `target` from snapshot's refid |
| Type text | `playwright_browser_type` | Use for form verification |
| Navigate | `playwright_browser_navigate` | Set URL first |
| Wait for state | `playwright_browser_wait_for` | Critical after navigate |
| Resize | `playwright_browser_resize` | For mobile viewport testing |
| Read console | `playwright_browser_console_messages` | For runtime / warning checks |
| Inspect network | `playwright_browser_network_requests` | Filter with regex e.g. `/api/.*` |

## Standard flow

```
1. playwright_browser_navigate — go to the relevant URL
2. playwright_browser_wait_for — wait for content (text or time)
3. playwright_browser_snapshot — get the accessibility tree (structure)
4. (optional) playwright_browser_take_screenshot — visual confirmation
5. Act (click / type / resize) if user asked for interaction
6. snapshot or screenshot again
7. Read playwright_browser_console_messages for runtime warnings
```

## Choosing snapshot vs screenshot

- **Snapshot** (accessibility tree): structural, FAST, supports targeted interaction (the response gives `ref:` IDs that the click/type tools accept). Always snapshot first to get the structure.
- **Screenshot**: literal pixels. Use when the user asks "what does it look like" or when you need to verify visual aspects that aren't in the accessibility tree (colors, layout shifts, hover/focus styles, font).

A common pattern: snapshot to see structure + take a single screenshot to confirm visual. Don't take screenshots after every micro-interaction — they're token-heavy.

## Snapshot's `ref` IDs

The snapshot response includes lines like:
```
- button "Submit" [ref=e23]
```

Use `ref=e23` (or the full refid) as the `target` parameter for subsequent `click`, `type`, `hover`, `evaluate`, etc.

## Wait patterns

`playwright_browser_wait_for` accepts:
- `text: "Some visible text"` — wait until text appears
- `textGone: "Some text"` — wait until text disappears
- `time: 2` — wait fixed N seconds

After `navigate`, wait either with `text` (best) or `time: 1` (lazy default). Without waiting, the snapshot may show stale content.

## When flow is over navigation or login

Login flow for admin:
1. Navigate to `/admin/login`
2. Snapshot → fill form fields (`playwright_browser_fill_form` or `type`)
3. Submit
4. `wait_for` confirmation text or URL change
5. Snapshot or screenshot of dashboard

## Pitfalls

- Don't navigate before checking the dev server is up — connection refused is a common failure.
- Don't use `playwright_browser_run_code_unsafe` unless absolutely necessary. It's RCE-equivalent. Use the purpose-built tools.
- Don't skip `wait_for` after navigate. Snapshots before content settles will be misleading.
- Don't pass coordinates — pass `ref:` IDs from the snapshot output.
- Don't screenshot while a transition is mid-flight (e.g., CSS transition). Wait for `time: 0.3` or `wait_for text:` first.

## Cleanup

`playwright_browser_close` to release the page once work is done.