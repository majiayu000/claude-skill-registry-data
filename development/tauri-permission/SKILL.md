---
name: tauri-permission
description: Checklist when the frontend of EasyTask starts using a new Tauri plugin command, window API, shell/opener URL or fs path - the permission in src-tauri/capabilities must be granted or the call fails only in the real app. Use when adding or changing a call to @tauri-apps/plugin-* or @tauri-apps/api, or when something works in vitest but not in `npm run tauri dev`.
---

# Tauri permissions (EasyTask)

Tauri 2 denies every plugin command that is not allowed in `src-tauri/capabilities/default.json`. Unit tests mock the plugins, so a missing permission is **not** seen by vitest, by tsc or by clippy: it shows as a rejected promise in the running app (and in the e2e), usually caught and hidden by `reportError`, so the feature silently falls back to defaults.

## Rule
Every command the frontend can reach needs its permission in the `permissions` array: `<plugin>:allow-<command>` (kebab-case of the command: `entries` -> `store:allow-entries`). One permission per command; a family permission such as `core:window:allow-...` for the window.

## Steps
1. List what the new code calls: `store.get/set/delete/save/entries/keys/has`, `sql.select/execute/close`, `fs.*`, `dialog.*`, `opener.openUrl`, `clipboard-manager.*`, `window.*`, `updater.*`, `notification.*`, and so on.
2. Open `src-tauri/capabilities/default.json` and compare. Currently the store has `load, get, entries, set, delete, save` (not `has`: it was removed because nothing uses it).
3. Add the missing permissions; remove those that nothing calls any more (least privilege). Check with `rg "\.has\(|\.keys\(|\.values\(" src` before removing one.
4. URLs opened with the opener plugin are an allowlist in the same file (`opener:allow-open-url` with `allow` urls): a new link host or path must be added there (the release notes link to the repository pages).
5. The fs plugin commands are listed too (`fs:allow-read-text-file`, `fs:allow-mkdir`, ...): a new fs call needs its own `fs:allow-<command>`. Check whether the path is also limited by a scope before assuming it is reachable.
6. Test in the real app: `npm run tauri dev`, do the action, restart if it is about persistence. The e2e (`npm run e2e` on Windows, or the CI) also catches it.
7. Add or extend an e2e step when the feature must survive a restart (see `e2e/specs/persistence.e2e.ts`).

## Symptoms
- A setting is saved but comes back as the default after a restart: the **read** command is not allowed (it happened with `store.entries()`).
- "not allowed" / "Command ... not allowed by ACL" in the dev console.
- It works in the unit tests and in the browser build but not in the Tauri window.
