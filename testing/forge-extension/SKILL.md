---
name: forge-extension
description: "Forge: browser extensions (Chrome/Edge MV3): chrome extension, manifest v3, service worker, content script, permissions, CSP, Web Store, store policy."
---

# Forge playbook — Browser extension (Chrome MV3)

`build-boss` leads; `security-boss` co-owns the permission + messaging + CSP surface (this is a security-heavy domain and a real Codex/security trigger). Popup/options UI defers to `forge-website` (real content, responsive, a11y); anything that calls a backend defers to `forge-integration`. Scope is **Chrome/Edge Manifest V3** unless the owner asks for Firefox/Safari (those are separate ports). The honesty rule: an extension that "loads unpacked" must have its core flow actually exercised, and every permission requested must be one the code genuinely uses.

## Hard rules (non-negotiable)
- **Least-privilege permissions.** Request only the `permissions` + `host_permissions` the code actually uses; prefer `activeTab` and `optional_permissions` over a blanket `<all_urls>`. Each permission is justifiable in one sentence. Over-broad scope is both a Web Store rejection risk and a user-trust failure.
- **No remotely-hosted code (MV3 policy).** All executable JS ships inside the package — **no** `eval`, `new Function` on remote strings, or `<script src>` from a CDN. Remote code is a hard Chrome Web Store rejection.
- **Safe content-script + messaging.** Content scripts run in the page's hostile context: validate every `chrome.runtime.onMessage` payload **and check `sender`**; never trust or `eval` `window.postMessage` data from the page; keep `externally_connectable` narrow. `web_accessible_resources` scoped to specific matches, never `<all_urls>`.
- **Strict CSP kept strict.** MV3's default extension CSP (`script-src 'self'`) is not weakened — no `'unsafe-eval'`, no `'unsafe-inline'`, no remote script sources. Sandboxed pages only if genuinely required, narrowly.
- **Termination-resilient service worker.** The MV3 background is an **event-driven service worker**, not a persistent page: listeners registered at top level, no reliance on in-memory global state surviving, durable state persisted to `chrome.storage`.
- **No secrets in the package; store-policy compliance.** No API secret baked into the extension (it's extractable); real secrets sit behind a backend, OAuth via `chrome.identity` with minimal scopes. Single clear purpose, accurate description, privacy disclosure if user data is handled, no obfuscated code.

## Team (conditional by stack/level)
Lead: `build-boss`. Security: **`security-boss`** (permission surface, CSP, message validation, no-remote-code — the defining risk of this domain). Support: `typescript-reviewer` (background/content/messaging code), `test-boss` (load the unpacked extension in Playwright/Puppeteer for E2E), `ui-boss` (popup/options UI via `forge-website`). Backend calls: `forge-integration` team.

## Skills / commands / MCP
Chrome Extension **MV3** docs via Context7 (manifest v3, service-worker lifecycle, messaging + storage + identity APIs — get the current API, MV2 patterns are dead). `forge-website` for the popup/options page UI; `forge-integration` if it talks to an API; `systematic-debugging` for service-worker lifecycle bugs (the "why did my listener not fire after idle" class). `browser` skill / Playwright to load the unpacked build and drive the core flow. No special MCP required. Reuse a bundler (esbuild / Vite / webpack) with an MV3/CRX plugin — don't hand-assemble the package.

## Fan-out & flow
L2 a single-purpose extension (popup + one content script); L3 a service worker + multiple content scripts + options page + messaging + a backend.
**Serial:** manifest + permission model → service worker + messaging contract → content scripts → popup/options UI → CSP + security review → load-unpacked E2E → production zip.
**Parallel:** content script ∥ popup/options UI ∥ background logic build in parallel **once** the message contract is fixed (the message schema is the seam).

## Domain gates
- Manifest requests only permissions/`host_permissions` the code uses; `activeTab`/optional preferred over `<all_urls>` (each justified).
- No remotely-hosted code — no `eval`/`new Function`/remote `<script>`; all JS bundled.
- Runtime + content-script messages validate `sender` + payload; page-supplied data is never `eval`'d; `externally_connectable` and `web_accessible_resources` scoped to specific matches.
- Default MV3 CSP kept strict (`script-src 'self'`, no `unsafe-eval`/`unsafe-inline`).
- Service worker is event-driven and termination-resilient — listeners at top level, durable state in `chrome.storage`, no global-state reliance.
- No secrets in the package; OAuth via `chrome.identity` with minimal scopes.
- Extension **loads unpacked and the core flow works** (evidence: load + a screenshot/log), and a production zip is produced.

## Ship-readiness (unique)
Manifest permissions minimal and each justified; no remote code / `eval`; messaging validates sender + payload; MV3 CSP strict; service worker termination-resilient (state in `chrome.storage`); no secrets in the package; extension **loaded unpacked with the core flow exercised** (real output attached) and a production zip built. Store-listing prerequisites — single-purpose description, privacy policy if user data, per-permission justifications, screenshots — are noted as **owner action** (submission itself needs a developer account and is owner-gated). Firefox/Safari ports are out of scope unless requested. Advisory checklist; running `security-boss` / `codex-reviewer` on the permission + messaging surface is strongly recommended here — not a blocker, but say so if it was not run.
