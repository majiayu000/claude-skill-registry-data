---
name: desktop-client-dev
description: Develop, extend, test and release the OpenMotion / OpenDesign Next cloud-first Electron desktop client, universal host bridge, local atomic capabilities, Web Connect Script, and two-tier signed configuration. Use when changing desktop shell code, native capabilities, preload/IPC contracts, environment switching, auto-update, or desktop CI/release workflows.
---

# OpenMotion Desktop Client (OD Next) Development

Use this repository-local contributor Skill for all desktop client work (`desktop/`, `packages/local-atoms/`, `packages/signed-config/`, `packages/connect-script/`, `shared/desktop-*.ts`, `shared/signed-config.ts`, and `studio/src/utils/platformHost.ts`). Read [AGENTS.md](../../../AGENTS.md) and [docs/layout-contract.md](../../../docs/layout-contract.md) alongside this Skill. For the complete file-by-file module map, capability inventory, and key-rotation runbook, read [references/architecture-map.md](references/architecture-map.md).

## Architecture at a glance

OpenDesign Next is a **cloud-first Electron thin shell** designed so product features ship via Web without waiting for desktop releases or Apple notarization:

1. **Zero bundled Studio / zero local Node sidecar.** `desktop/electron-builder.yml` packages only `desktop/dist/**/*` and `desktop/package.json`. The shell loads cloud Studio directly (`stable`: `https://motion.open-design.ai`, `test`: built-in `DEFAULT_STUDIO_URLS.test`, `dev`: `http://127.0.0.1:4173`). Do not reintroduce a bundled local server or `stage-app` flow.
2. **Frozen 4-method `UniversalHostBridge`.** `desktop/src/preload.ts` exposes only `window.__OPENMOTION_HOST__` with `info()`, `capabilities()`, `invoke(capability, method, params)`, and `subscribe(capability, event, cb)`. Main-process dispatch goes through `CapabilityRegistry` + Zod validation (`shared/desktop-schemas.ts`).
3. **Isomorphic Desktop + Browser Connect Script.** Cloud Studio (`studio/src/utils/platformHost.ts`) talks to the exact same `UniversalHostBridge` contract whether hosted inside Electron or paired in a regular browser with `packages/connect-script` over `127.0.0.1` HTTP + SSE. Both hosts execute the same `packages/local-atoms` engine and `packages/signed-config` verifier.
4. **Five atomic local capabilities.** Local host operations are composed from five audited primitives in `packages/local-atoms/`: `atom.detect`, `atom.exec`, `atom.installComponent`, `atom.credential`, and `atom.config`.
5. **Two-tier Ed25519 Signed Config.** The shell refreshes `https://releases.open-design.ai/open-motion/desktop/config/{channel}.json` on startup and every 30 minutes (falling back cleanly to last-known-good, then bundled defaults) so Agent rules, `featureFlags`, `allowedOrigins`, and `minShellVersion` can update without shipping a new shell binary.

## Decide where a change belongs

Choose the narrowest layer that avoids an unnecessary shell release:

| Need | Where to change | Shell release needed? |
| --- | --- | --- |
| Product UI, workflows, Studio pages, API/MCP features | Cloud `studio/` and `src/` | No (Web deploy only) |
| Add/update a config-file MCP Agent (JSON/TOML), feature flag, `allowedOrigins`, or `minShellVersion` | `desktop/config/{test,stable}.payload.json` + publish via `desktop-signed-config.yml` (keep `packages/signed-config/default-config.ts` aligned for offline fallback) | No (hot signed config) |
| Add a native OS feature or shell capability | `shared/desktop-contract.ts` -> `shared/desktop-schemas.ts` -> `desktop/src/capability-registry.ts` -> `desktop/src/main-capabilities.ts` -> `studio/src/utils/platformHost.ts` | Yes (additive-only) |
| Add/fix a local atomic operation shared by Desktop & Browser Connect Script | `packages/local-atoms/` (and `shared/desktop-builtin-rules.ts` if expanding built-in security bounds) | Yes for Desktop; CLI/script update for Connect Script |
| Change window chrome, safe areas, overlays, dialogs, or desktop layout | `desktop/src/platform.ts`, `studio/src/utils/platformHost.ts`, `packages/design-system/base.css` (follow `docs/layout-contract.md`) | Only if shell chrome behavior changes |

## How to add a new shell capability or method

1. **Extend contracts additively.** Add capability/method types to `shared/desktop-contract.ts` and strict Zod parameter schemas to `shared/desktop-schemas.ts`. Never rename, remove, or change the meaning of existing methods or error codes (`UNSUPPORTED`, `INVALID_PARAMS`, `UNAUTHORIZED`, `ORIGIN_DENIED`, `POLICY_DENIED`, `USER_DENIED`, `CONFLICT`, `BUSY`, `NOT_FOUND`, `VERIFICATION_FAILED`, `TIMEOUT`, `EXEC_FAILED`, `INTERNAL_ERROR`). Give every method and event exactly one name; `desktop/tests/capability-registry.test.mjs` pins the shell capability lists, so a new name is a deliberate, permanent addition and never an alias.
2. **Keep `desktop/src/main.ts` modular.** Wire capability handlers in `desktop/src/main-capabilities.ts` (and factory builders in `desktop/src/capability-registry.ts`). Put IPC channel wiring in `desktop/src/main-ipc.ts`, download/update UX in `desktop/src/main-downloads.ts`, boot splash overlay logic in `desktop/src/main-boot-overlay.ts`, and test-channel environment switching in `desktop/src/main-env-runtime.ts`.
3. **Consume via capability discovery in Studio.** In `studio/src/utils/platformHost.ts` and Studio UI, gate every new capability/method with `hasHostCapability(name, minVersion)` or `resolveCapabilityMethod(...)` so newer cloud Studio degrades gracefully on older shells (and use `minShellVersion` when an upgrade is mandatory).
4. **Update CI trigger paths if adding cross-package imports.** Any file outside `desktop/` bundled into `desktop/dist/main.mjs` or `desktop/dist/preload.cjs` must be listed under `push.paths` in `.github/workflows/desktop-release.yml` and asserted in `desktop/tests/updater.test.mjs`.

## Security and compatibility invariants

Preserve every invariant below—they are enforced by `tests/desktop-security-audit.test.ts`, `desktop/tests/capability-registry.test.mjs`, and `desktop/tests/window-auth-policy.test.mjs`:

- **Privileged IPC boundary:** Only the main window's top-level frame on an allowed Studio origin (never subframes, popups, `/auth/*`, `file://`, or active in-window auth fallback) may call `__OPENMOTION_HOST__`. Always authorize via `authorizePrivilegedIpcSender`.
- **Window & popup policy:** Allowed popups (`about:blank` or same-origin) must receive `POPUP_HARDENED_WEB_PREFERENCES` (`preload: undefined`, `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`). Billing, checkout, and external account portals always open in the system browser.
- **No arbitrary shell execution or secret leaks:** Never spawn with `shell: true`. Built-in templates use typed placeholder validation (`shared/desktop-builtin-rules.ts`); `murmur-engine` explicitly blocks launcher/exec subcommands. Credentials use OS safeStorage/Keychain, inject strictly via stdin, and are redacted from stdout/logs. Connect Script pairing tokens stay in memory only.
- **Component install verification:** `atom.installComponent` enforces allowed-domain downloads (including redirects), strict SHA-256 verification, out-of-bundle installation (`<dataDir>/components/` or `~/.murmurant/bin`), and platform code-signature verification (macOS Developer ID Team ID via `codesign`; Windows Authenticode SHA-256/SHA-1 thumbprint pinning via `Get-AuthenticodeSignature`).
- **Test environment isolation:** Environment switching (`env-switcher.ts`, `--studio-url`, `openmotion://open?env=...`) is strictly disabled (fail-closed) on `stable`. On `test`/`dev`, custom origins get isolated `persist:om-env-<hash>` session partitions so cookies and storage never bleed across lanes.
- **macOS HIG & layout safety:** Never attach macOS modal sheets (`modal: true` + `parent`) that hide traffic lights or deadlock quit dialogs. Always respect `--om-desktop-safe-top`, `--om-desktop-inset-left`, `--om-desktop-inset-right`, and `--om-workspace-top`.
- **No committed private keys:** Trust anchors (`OPENMOTION_DESKTOP_ROOT_PUBLIC_KEY_SPKI`, `OPENMOTION_MURMUR_APPLE_TEAM_ID`, `OPENMOTION_MURMUR_WIN_THUMBPRINTS`) are injected at bundle time via `desktop/scripts/build.mjs` from CI variables/secrets.

## Local development and debugging

```bash
# 1. Build desktop main + preload bundles (fast esbuild step)
npm --prefix desktop run build

# 2. Launch Electron against a local Studio server (e.g. http://127.0.0.1:4173)
MOTION_DESKTOP_CHANNEL=dev npm --prefix desktop run dev -- --studio-url=http://127.0.0.1:4173

# 3. Launch Electron against a staging / test lane
MOTION_DESKTOP_CHANNEL=test npm --prefix desktop run dev -- --studio-url=https://staging.open-design.ai

# 4. Build an unsigned local macOS arm64 .dmg/.zip for manual smoke testing
npm --prefix desktop run pack:mac:local
```

On `test` / `dev` builds you can also switch Studio origins at runtime from the **Environment** menu, via `openmotion://open?env=<url>`, or from the retry page's environment controls.

## Release and hot-config workflows

- **Desktop installers (`.github/workflows/desktop-release.yml`):**
  - Pushing desktop-coupled paths to `desktop-test` automatically verifies, builds (`macOS arm64`, `macOS x64`, `Windows x64`), signs/notarizes macOS, uploads to `releases.open-design.ai/open-motion/desktop/test/`, merges `test-mac.yml`, and notifies Feishu.
  - `stable` releases require `workflow_dispatch` on `main` with `channel=stable` and `publish=true`.
- **Hot signed config (`.github/workflows/desktop-signed-config.yml`):**
  - Updating `desktop/config/test.payload.json` on `desktop-test` automatically validates bounds, increments the live monotonic `sequence`, signs with the operational key/cert, runs `verify-config`, and uploads `open-motion/desktop/config/test.json` (`no-cache`).
  - `stable` config updates run via `workflow_dispatch` on `main` with `channel=stable` and `publish=true`.

## Verification before handing off

Run the desktop boundary checks for every desktop/shared/atoms/signed-config change:

```bash
npm --prefix desktop run typecheck
npm --prefix desktop run build
npm --prefix desktop test
node --experimental-strip-types --test \
  tests/desktop-contracts.test.ts \
  tests/signed-config.test.ts \
  tests/desktop-security-audit.test.ts \
  tests/local-atoms.test.ts \
  tests/connect-script.test.ts \
  tests/desktop-showcase-e2e.test.ts
npm run check
```

If you also touched Studio (`studio/`), run `npm run typecheck:studio`, `npm run build:studio`, and the affected Vitest files (such as `studio/src/utils/platformHost.test.tsx`, `studio/src/motion/DesktopConnectPanel.test.tsx`, `studio/src/motion/SettingsCenter.test.tsx`). Always verify `git diff --check` and keep commit messages, PR descriptions, and code comments in English.
