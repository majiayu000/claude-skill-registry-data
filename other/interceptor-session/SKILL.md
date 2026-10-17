---
name: interceptor-session
description: "Signed-in browser ops via Interceptor — use the operator's real logged-in browser for authenticated checks, passive traffic inspection, and evidence capture. NOT a crawler."
category: "tooling"
version: "1.0"
author: "bountyreper-official"
tags:
  - browser
  - session
  - authenticated
  - traffic
  - websocket
tech_stack:
  - web
cwe_ids: []
chains_with:
  - attack-xss-dom
  - attack-request-smuggling
prerequisites: []
---

# Interceptor — signed-in browser sessions

## When to use Interceptor vs other browser tools

| Need | Tool |
|---|---|
| Crawl / discover URLs at scale | `katana`, `hakrawler`, `gospider` — NEVER Interceptor |
| Headless render + login-flow validation of a specific page | `mcpbrowser` |
| **Use the operator's ACTUAL signed-in browser session** (existing cookies, profiles, 2FA-complete logins) | **`interceptor`** |
| **Passive traffic inspection of a live page** (fetch/XHR/SSE/WebSocket/Beacon/BroadcastChannel, headers) | **`interceptor`** |
| Native macOS app / iOS automation | `interceptor` (Full install only; this is a browser-only install) |

Interceptor works through the operator's own Chrome/Brave via an extension — cookies,
sessions, and SSO logins already exist. That is its unique value; automation tools that
spawn a fresh browser cannot replicate it.

## Setup (once per machine)

The extension must be loaded in Chrome/Brave and the daemon running. Native messaging
manifests live under `/Library/Google/Chrome/NativeMessagingHosts/` — if commands fail
to connect, that manifest is missing (root install step; see install notes in the
repo's docs). Verify health:

```bash
interceptor status        # daemon + transport state
interceptor contexts      # connected browser profiles
```

## Core commands

```bash
# Open a managed tab (background) and read its structure
interceptor open "https://target.com/account" --group hunt-1
interceptor read --group hunt-1

# Find and act by element reference (refs come from read/find)
interceptor find "Sign in" --group hunt-1
interceptor act <ref> --group hunt-1          # click
interceptor act <ref> "text" --group hunt-1   # type

# Inspect page traffic passively (no debugger attach)
interceptor inspect --group hunt-1

# Cleanup when done — closes the task's managed tabs
interceptor group close hunt-1
```

Multiple concurrent workers: give each its own `--group`; each browser profile is a
`--context` (run `interceptor contexts` to list).

## Pentest-specific plays

1. **Authenticated surface walk (signed-in session):** operator's session is already
   logged in — `open` → `read` → map account settings, hidden admin links, role-gated
   UI. Evidence for authz testing (pair with the IDOR/authz methodology).
2. **Passive traffic capture:** `inspect` reveals internal API routes the SPA calls
   (endpoints, params, auth headers) that crawlers miss — feed them into `add_intel`
   and http_replay testing.
3. **DOM XSS verification:** load a page in the real session, then verify
   hash/postMessage payloads execute (capture console) — stronger proof than curl.
4. **Same-origin fetches from the session:** combine with CORS/postMessage analysis —
   the operator's cookies ride along, exactly what a cross-origin attacker gets.

## Field-reality notes (from a live hunt — read before driving)

These came from an engagement where Interceptor-managed capture blocked several high-value
lanes. Follow them instead of rediscovering them:

1. **Capture flows → `mcpbrowser` first.** The Interceptor net-log verbs (`monitor`, net
   capture) periodically returned `[]`/TypeErrors mid-hunt, so exact XHR shapes were LOST and
   every IDOR/business-logic lane went blind. mcpbrowser streams requests straight into the
   ingest pipeline — shapes preserved and auto-analyzed. Only fall back to `interceptor inspect`
   for a quick look; never as the evidence channel.
2. **Login funnels in managed tabs stall.** Passkey prompts hang, SSO refused to inherit into
   new managed tabs, re-login cycles cost turns. `mcpbrowser` with the saved credential beats
   Interceptor wherever authentication is required.
3. **Use Interceptor for the things that work well:** quick signed-in surface reads
   (`open`/`read`/`find`/`act`), confirming a logged-in state, DOM-level checks in the real
   session. That is its lane; capture evidence is not.
4. **Managed-tab hygiene:** verify the tab landed on the right page BEFORE acting (a repeat
   failure mode was tabs landing in error pages with the group still reporting healthy), and
   `group close <name>` the moment a lane finishes.

## Boundaries (hard rules)

- NEVER use Interceptor for bulk crawling — it drives the operator's real browser and
  tabs; that is the mcpbrowser/katana boundary, not a capacity question.
- One `--group` per logical task; close groups when done (`group close`).
- Actions run in the operator's accounts: destructive UI actions (delete, transfer,
  purchase) require explicit user authorization on the record first — same gate as any
  active testing.
- All traffic inspection is passive; never exfiltrate page data anywhere except the
  operator's evidence store.
