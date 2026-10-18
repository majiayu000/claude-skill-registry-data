---
name: forge-electron
description: "Forge: Electron desktop apps: electron, desktop app, .exe, installer, IPC, contextBridge, contextIsolation, nodeIntegration, code signing, auto-update."
---

# Forge playbook — Electron / desktop app

The `electron-pro` specialist (`.claude/agents/electron-pro.md`) leads the Electron-specific work under Build Boss or Integration Boss. Renderer UI defers to `forge-website` (real content, responsive, a11y); anything that talks to a gateway/API defers to `forge-integration` / `forge-payments`. Forge context: the an accounting desktop app (accounting) desktop app — offline-first, safe IPC, an installer that opens on a clean machine. Modern Electron ships these secure defaults; **the rule is to never regress them**, and to prove they hold.

## Hard rules (verify, don't assume — cite the exact config line)
- **`contextIsolation: true` on every `BrowserWindow`** — no exceptions. Required even with nodeIntegration off; it is what separates preload/renderer JS contexts from Electron internals.
- **`nodeIntegration: false` in all renderers.** Node reaches the renderer *only* through a preload `contextBridge.exposeInMainWorld` with an explicit, minimal API — never a raw `ipcRenderer` passthrough on `window`. (Enabling `nodeIntegration:true` also disables the sandbox for that renderer.)
- **`sandbox: true` where feasible; `webSecurity` left enabled; remote module disabled; `allowRunningInsecureContent: false`.**
- **Validated IPC.** Every IPC channel validates its payload and (where relevant) sender; the exposed API surface is a small allow-list, not the whole `ipcRenderer`.
- **Strict CSP** — no `'unsafe-eval'`, no wildcard remote script sources. (CSP limits, not cures, XSS — defense in depth on top of context isolation.)
- **No secrets baked into the bundle.** Sensitive data uses OS-appropriate secure storage (Keychain/DPAPI/libsecret — in Electron the built-in `safeStorage` API, no extra package), not plain files; secrets in env / secure store, never in the packaged asar.
- **A real, signed installer that actually opens.** The build produces the intended artifact (e.g. Windows NSIS), the installer installs and launches on a clean machine (verify — don't assume), and auto-update (if in scope) verifies signatures + supports rollback. Never ship an unsigned silent updater.
- **No test/demo/mock/placeholder data in the shipped build** (Forge desktop rule).

## Team (conditional)
Lead: `build-boss` (app) or `integration-boss` (desktop wrapper over a service). Desktop work: **`electron-pro`** specialist. Support: `typescript-reviewer` (main/preload/renderer), `security-reviewer` (IPC surface + CSP — desktop is a reasonable Codex/security trigger), `database-reviewer` (local store, e.g. SQLite for an offline app). Renderer UI: `forge-website` team.

## Skills / commands / MCP
Electron + electron-builder docs via Context7 for exact API/config; `forge-website` for the renderer UI; `forge-integration` / `forge-payments` if the app calls external services or handles money; `systematic-debugging` for build/native-dep failures. Reuse `electron-builder`'s signing config — don't hand-roll packaging.

## Fan-out & flow
L2 single-window app; L3 multi-window + native integration + installer + auto-update.
**Parallel:** main-process services ∥ preload API surface ∥ renderer UI (independent once the IPC contract is fixed — the preload API is the contract).
**Serial:** process architecture (main/preload/renderer) → hardened `BrowserWindow` options → contextBridge IPC API → renderer UI → build config → signed installer → clean-machine launch test.

## Domain gates
- `contextIsolation:true`, `nodeIntegration:false`, `sandbox:true` (where feasible), `webSecurity:true` verified on every window (cite the file:line).
- Preload exposes a minimal, validated API; no raw `ipcRenderer` on `window`; IPC payloads validated.
- Strict CSP set; no `unsafe-eval`/wildcard script sources.
- No secrets in the bundle; secure OS storage used for sensitive data.
- Build produces the intended installer and it **actually installs + launches on a clean machine** (evidence, not assumption).
- Cold-start + idle-memory numbers reported are **observed**, not guessed; listeners/watchers/intervals cleaned up on window close.
- No test/demo/mock data in the shipped artifact.

## Ship-readiness (unique)
Renderer hardening flags verified with cited config lines; IPC surface minimal + validated; CSP strict; secrets in secure storage not the bundle; installer built AND launched on a clean machine (real output attached); auto-update (if any) signature-verified + rollback-capable; offline behavior works where promised; no mock data shipped; observed startup/memory numbers reported honestly. Advisory checklist; optionally run `security-reviewer` / `codex-reviewer` on the IPC + CSP surface — not a blocker; label anything not run (no signing cert / no clean-machine test) as not-run.
