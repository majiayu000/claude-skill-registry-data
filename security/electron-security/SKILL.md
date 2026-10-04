---
id: electron-security
version: "2.0.0"
title: "Electron Desktop Security"
description: "Harden Electron: renderer trust boundary (nodeIntegration, contextIsolation, sandbox), build-time fuses, contextBridge and IPC allowlists, shell.openExternal, navigation guards, deep-link auth, safeStorage. Use when generating main-process code, a preload script, or custom-protocol handlers, when packaging a release, or when storing tokens in an Electron app."
category: hardening
severity: critical
applies_to:
  - "when generating Electron main-process code (BrowserWindow, ipcMain, app events)"
  - "when generating a preload script or contextBridge surface"
  - "when wiring custom-protocol / deep-link handlers"
  - "when packaging or signing a release build"
  - "when storing tokens or secrets in an Electron app"
  - "when reviewing Electron IPC, navigation, or window configuration"
languages: ["javascript", "typescript"]
token_budget:
  minimal: 1700
  compact: 2250
  full: 2900
rules_path: "checklists/"
related_skills: ["frontend-security", "crypto-misuse", "secret-detection", "auth-security"]
last_updated: "2026-08-12"
sources:
  - "Electron Security Checklist (official docs)"
  - "Electron Fuses documentation"
  - "OWASP — Electron / desktop application security"
  - "CWE-78, CWE-22, CWE-250, CWE-693, CWE-829, CWE-1188"
  - "Doyensec / Electronegativity research on Electron attack surface"
external_tools:
  - name: electronegativity
    purpose: "Electron app misconfiguration & anti-pattern scan"
    command: "electronegativity -i ."
---

# Electron Desktop Security

## Rules (for AI agents)

### ALWAYS
- **Treat the renderer as untrusted.** Any renderer-side code execution — XSS in
  rendered content, a redirect, a deep link — must not be able to reach Node, the
  shell, the filesystem, or session tokens. Every other rule here follows from this
  one, and every IPC sink you expose is reachable from a compromised renderer.
- Keep the renderer's process isolation at its defaults rather than restoring them:
  `nodeIntegration: false`, `contextIsolation: true` and `sandbox: true` have been
  Electron's defaults for several major versions, so the finding is the line that
  **turns one off**. Note the coupling: under `sandbox: true` a preload gets a
  polyfilled module subset, so a preload needing `fs` fails — move that work behind
  IPC into the main process, never drop the sandbox.
- Set the packaging **fuses** on release builds: disable `RunAsNode`,
  `EnableNodeCliInspectArguments` and `EnableNodeOptionsEnvironmentVariable`. With
  `RunAsNode` on, an attacker runs your signed binary as a plain Node process and
  every renderer-side control above becomes irrelevant — a build-time setting no
  runtime hardening substitutes for.
- Expose a **minimal, typed** API from the preload via
  `contextBridge.exposeInMainWorld`. Expose named functions only — never hand the
  renderer `ipcRenderer`, `require`, `process`, or whole modules. Do not add
  `@electron/remote`: it restores the main-process object access that was removed
  from core precisely because it defeats the boundary.
- Validate **every** IPC argument in the main-process handler: type-check, bound,
  and allowlist. The renderer is an attacker-controlled input source.
- Spawn child processes with `execFile` / `spawn` and an **argument array**, never
  `exec` with a shell string built from renderer input — that is command injection.
  Allowlist each argument (e.g. `^[A-Za-z0-9_-]+$`).
- Confine filesystem paths: `path.resolve(base, input)`, then verify the result
  `startsWith(base + path.sep)`. Reject absolute paths and `..` segments.
  Concatenating a renderer-supplied path (`${BASE}${filePath}`) is path traversal
  and arbitrary file write.
- Allowlist `shell.openExternal` to `https:` (and `mailto:` if needed) after parsing
  the URL. Reject `file:`, custom schemes, and anything else — an arbitrary or
  renderer-controlled URL here is a local-launch and RCE vector.
- Add navigation guards: `app.on('web-contents-created', …)` with
  `contents.on('will-navigate', …)` and `contents.setWindowOpenHandler(…)` that
  **deny by default** against a strict origin allowlist. Keep `webviewTag: false`;
  where a `<webview>` is genuinely required, strip its `preload` and reset its
  options in `will-attach-webview`.
- Remember the contextBridge surface is exposed to **whatever origin the webContents
  currently holds** — the preload re-runs on navigation and `exposeInMainWorld` does
  not re-check origin. One missing `will-navigate` guard lets an attacker origin
  inherit your *entire* IPC surface: that is how a stored hyperlink becomes 1-click
  RCE. Gating the preload on `location` is defense in depth, not the control.
- Before attaching session tokens or cookies to an outbound request, verify the
  target host is on your own-API allowlist. Never attach credentials to a
  renderer-supplied URL — an XSS then exfiltrates the token.
- Bind custom-protocol / deep-link auth to a one-time `state` / PKCE value the app
  generated and is waiting for; validate before storing any token. Accepting
  `myapp://auth?refresh-token=…` unvalidated is login CSRF and session fixation.
- Store tokens with Electron `safeStorage`, not app-level crypto — and check
  `safeStorage.isEncryptionAvailable()` first: on Linux with no keyring the backend
  falls back to a fixed key, so the ciphertext is not confidential. Ship release
  builds code-signed, with ASAR integrity where the platform supports it (macOS and
  Windows).
- Treat **every server the app connects to** — your own API, an auto-update channel,
  a telemetry endpoint, a shared multi-tenant backend — as potentially
  attacker-controlled. Never load a server-supplied URL into a window carrying your
  preload, and never feed a server response into an IPC sink (file path, shell
  argument, `openExternal` URL) without the validation you apply to renderer input.
- Harden parsers consuming untrusted server or stream data: bound every length field
  before allocating, cap recursion and include-style expansion (circular references
  become an infinite loop), and wrap the parse in try/catch. A malicious server
  otherwise hangs the renderer even where memory safety rules out RCE.
- Consult `frontend-security` for the renderer's own browser surface — Content
  Security Policy, DOM sinks, sanitizer choice. The renderer is a browser; that
  skill owns what runs inside it, this one owns what it can reach beyond it.

### NEVER
- Set `nodeIntegration: true`, disable `contextIsolation`, disable `sandbox`,
  disable `webSecurity`, or set `allowRunningInsecureContent: true` — especially on
  a window that loads remote or navigable content.
- Leave `RunAsNode` or the Node CLI / `NODE_OPTIONS` fuses enabled in a release
  build.
- Encrypt tokens at rest with app-level crypto in place of `safeStorage`, or keep a
  `PLAINTEXT:` fallback path. `crypto-misuse` owns cipher mode, key derivation and
  the rest.
- Ship a frameless or chromeless **navigable** window (`frame: false`, no address
  bar): after a redirect the user has no visual cue they left the app, so a phished
  navigation can silently clone your UI. Frameless is acceptable only behind a hard
  navigation guard.
- Assume the renderer, or the content it renders, is the *only* untrusted input. A
  backend or update server the app trusts can itself be compromised, or in a
  multi-tenant deployment driven by another tenant.

### KNOWN FALSE POSITIVES
- Dev builds that load `http://localhost:<port>` with relaxed settings — these rules
  govern **release** builds; the finding is dev config that ships.
- A custom protocol (`myapp://`) for OAuth callbacks is expected. The control is
  `state` / PKCE validation, not the scheme's existence.
- `contextBridge`-exposed functions are intentional capabilities. Review what each
  one does and whether it validates input, not the fact that a bridge exists.
- `shell.openExternal` on a hard-coded `https://` constant, not user input.
- A frameless window loading **only** local first-party content behind a
  deny-by-default nav guard. The risk is frameless **plus** navigable to remote
  origins.
- Connecting to a backend and rendering its **data** — telemetry JSON, numbers,
  binary frames — is normal desktop behaviour. The control is bounding and
  validating that data, and never treating it as HTML, a filesystem path, or a shell
  argument. Not avoiding the connection.

## Context (for humans)

Electron ships a Chromium renderer and a Node main process in one app. The classic
misconfiguration is `nodeIntegration: true` with no navigation guards: it turns any
renderer-side bug — XSS in a report view, an open redirect, a deep link — into full
host RCE, because every IPC handler the preload exposes is then reachable by
attacker-controlled renderer code.

Two things have shifted since that framing was written. The dangerous window options
are now safe by default, so the modern finding is code that *re-enables* them rather
than code that forgets to set them. And the runtime boundary is no longer the whole
story: the packaging fuses decide whether the shipped binary can be re-launched as a
plain Node process at all, which is a hole no `webPreferences` setting can close.

The renderer is the first untrusted boundary but not the only one. A desktop app also
trusts every server it connects to. Where that server is shared — a multi-tenant
backend, a per-session remote node — a co-tenant who compromises it becomes an
attacker feeding your privileged renderer. The worst chain is the reverse of the
obvious one: server-controlled content → a navigable preload-bearing window → the
exposed API → local RCE.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/electron-hardening.md` — version gates for the window defaults, the
  fuse list and how to set it, `safeStorage` backends per platform, and the
  `<webview>` hardening options
- `checklists/electron_hardening.yaml` — machine-readable hardening checks
  (window config, IPC sinks, navigation, deep-link, token storage)
- [Electron Security Checklist](https://www.electronjs.org/docs/latest/tutorial/security).
- [Electron Fuses](https://www.electronjs.org/docs/latest/tutorial/fuses).
- [CWE-78 — OS Command Injection](https://cwe.mitre.org/data/definitions/78.html).
- [CWE-22 — Path Traversal](https://cwe.mitre.org/data/definitions/22.html).
- [CWE-250 — Execution with Unnecessary Privileges](https://cwe.mitre.org/data/definitions/250.html).
