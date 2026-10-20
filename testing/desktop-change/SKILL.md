---
name: desktop-change
description: Change agent-office's desktop shell — tray menu, native notifications, settings, IPC channels, windows, the auto-updater, packaging/installers or icons. Use for edits under packages/desktop/ (main, preload, electron-builder.yml, e2e) or to core domain tray/attention/update/settings logic.
---

# Change the desktop shell

Rules: `PRIVACY_SECURITY.md` (Electron checklist), `ARCHITECTURE.md`, `TESTING.md`.

1. **Decide in the core first (red → green):**
   - What the tray shows: `core/src/domain/tray.ts`
   - When to notify: `core/src/domain/attention.ts`
   - Update policy: `core/src/domain/update-policy.ts`
   - Settings fields: `shared/src/desktop-api.ts` `SettingsSchema` (additive, with defaults) and `core/src/domain/settings.ts` (restart fields)
2. **IPC:** add the channel name to `shared/src/ipc-channels.ts` and the method to `AgentOfficeApi` (additive). Then add the handler in `desktop/src/main/ipc-api.ts`, zod-validated, with a test in `ipc-api.test.ts`, and the bridge in `desktop/src/preload/index.ts`.
3. **Electron adapter:** keep it thin (`desktop/src/main/adapters/electron-*.ts`). Logic stays in the core.
4. **Wiring:** `composition.ts` and `composition.test.ts` (fake `Shell`).
5. **Renderer:** view model → controller → DOM adapter (see `/scene-change` for 3D).
6. **App E2E:** add or extend a spec in `packages/desktop/e2e/` (isolated profile from `e2e/app.ts`), then `make build test-ui`.
7. **Security review** against the Electron checklist: no new permissions, no Node in the renderer, the CSP is unchanged, and the IPC is validated and sender-checked.
8. **Packaging changes:** run `make package`, launch the unpacked app once, and run the hook wrapper from Settings → Install (temp `CLAUDE_SETTINGS_FILE`). Run `make icons` after editing `build/*.svg`.

Theme: `desktop/src/main/theme.ts` (pure) applies the `theme` setting to `nativeTheme.themeSource` and the window background; `desktop/e2e/theme.spec.ts` checks both themes and contrast (drop Playwright's color-scheme emulation with `emulateMedia({ colorScheme: null })`). Quitting with managed sessions asks first (`createQuitGuard`).
