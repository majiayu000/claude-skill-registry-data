---
name: mikka-browser-qa
description: "Exercise Mikka official Web, packaged Desktop and applicable Expo UI journeys with real, source-pinned browser interactions, snapshots and persistent API/DB readback. Use for dead controls, missing actions, focus, keyboard, touch, responsive, navigation and error-recovery verification."
---

# Mikka browser QA (adapted from agent-browser)

This is a **review workflow**, not a vendored browser executable. Upstream: https://github.com/vercel-labs/agent-browser . If the authorized cloud Linux machine already has `agent-browser`, first use `agent-browser skills get core` for version-matched syntax, then inspect the accessibility snapshot before choosing element references. If not installed, use existing project browser/Playwright acceptance tools: do not silently install global software or bootstrap a second CI service.

1. Pin public/hosted SHAs, official renderer and application origin; choose disposable accounts, actual role/permissions, isolated PostgreSQL and service emulator/real daemon only as needed.
2. Build and start the paired official Web client using the [domain workflow](../../../docs/design/ux-quality-audit.md#run-one-domain) and [runtime acceptance guide](../../../docs/acceptance.md); never build or launch on the developer's Mac. Never use Vercel Preview. Do not assume the public Server-only build renders the official workspace.
3. Inspect the actual accessible tree and rendered controls; enter via the genuine user's route. Use roles/names first. Include 390px, desktop, long text, Zoom, keyboard, touch-equivalent browser interaction and light/dark when relevant.
4. Before action record visible state and input; click or press once, observe immediate pending/disabled feedback; verify command request, actual ACK/denial, effect by fresh authorized read, UI recovery and no duplicate write. Explicitly check 401/403, 409, server 503, replay/lost ACK only for the affected contract.
5. For live SSE/WebSocket pages **do not wait for permanent global `networkidle`**. Wait for a specific ready control/response and use bounded assertions; screenshot/console/network failures are evidence, not proof a domain operation persisted.
6. Package/artifact distinction: browser Chromium != packaged Electron != Expo Web != physical iPhone/TestFlight. Record platform precisely, do not claim others were tested. Clean only isolated fixtures and stop any machines used.
7. Save route, source pair, identity scope (redacted), UTC, procedure, observed UI/HTTP/DB outcome, screenshots and failure cause. Follow `verification-before-completion`.

Never add general browser E2E jobs to Mikka's PR CI, never use production customer data or bypass the #1954 release owner.
