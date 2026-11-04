---
name: vscode-contributions
description: Add or change a LocalPilot setting, command, menu entry, keybinding or view, and keep package.json, src/config.ts, src/extension.ts, the docs and the tests in sync. USE WHEN adding a `localpilot.*` setting or command, wiring a button into the Agents view or chat title bar, changing a default, or exposing a new feature to users.
---

# Adding settings, commands and menus

A contribution touches several files that nothing checks against each other at compile time. Change them all in one go.

## Settings

1. **`package.json` → `contributes.configuration.properties`.** Put the key next to related keys, because order is the order in the Settings UI. Give it a `type` and `default`, a `minimum`/`maximum` for numbers, and `enum` plus `enumDescriptions` for choices. Use `markdownDescription` and say what the user gets. Link related settings as `` `#localpilot.other.key#` ``. If data leaves the machine, say so plainly (see `localpilot.storage.redis.enabled`).
2. **`src/config.ts`.** Add the field to `LocalPilotConfig` with a one-line doc comment, then read it in `getConfig()` with the **same default** and clamping (`Math.max/Math.min/Math.floor`). Group related keys in an object, as with `queue`, `autoMode`, `supervisor` and `memoryLimits`.
3. **Read it where it's used** with `getConfig().x`, not cached at activation, so changes apply without a reload. If something must react to a change, use `onDidChangeConfiguration` with `e.affectsConfiguration('localpilot.x')` (see `extension.ts`).
4. If the settings panel should show it, add it to `src/ui/settingsPanel.ts` and `media/settings.js` (check `scripts/settings-preview.html`).
5. **Docs:** add a row to `docs/docs/configuration.md`, and to the feature's page in `docs/docs/` if it's user-visible.

## Commands

1. **`package.json` → `contributes.commands`:** `{ command: "localpilot.x", title: "Do X…", category: "LocalPilot", icon: "$(codicon)" }`. Titles use Title Case, with "…" when the command asks for more input.
2. **Register it in `src/extension.ts`** with the local helper `cmd('localpilot.x', (arg?: unknown) => …)`. Tree-view menus pass the clicked node and the palette passes nothing, so normalise the argument (see `sessionIdArg`, `queueTaskArg`).
3. **Hide item-only commands from the palette:** add `{ "command": "localpilot.x", "when": "false" }` to `menus.commandPalette`.
4. **Placement:**
   - `menus["view/title"]` with `"when": "view =~ /^localpilot\\.agentsView/"`. Group `navigation@N` puts it in the toolbar; any other group puts it in the `…` menu.
   - `menus["view/item/context"]` matches the tree item's `contextValue` (set in `src/ui/agentsView.ts`). Use `viewItem == x` or a regex `viewItem =~ /^queue-(failed|blocked)$/`. Group `inline@N` shows as a hover icon.
   - The status bar menu is the `localpilot.statusMenu` quick pick in `extension.ts`.
5. If other extensions or the CLI need it, add it to `LocalPilotApi` at the end of `extension.ts` and to the API table in `docs/docs/development.md`.

## Editing package.json safely

Edit it with a small Node script (parse, change, `JSON.stringify(p, null, indent)`), keeping the file's existing indentation, or use exact Edit replacements. Then confirm that `git diff --stat package.json` shows only the lines you meant to change.

## Check

```bash
npx tsc --noEmit && npx eslint src && node -e "require('./package.json')"
```

`src/test/extension.test.ts` and `src/test/telemetry.test.ts` assert parts of the manifest (commands, menus, defaults). Run them (see the `run-extension-tests` skill) after renaming or removing anything. Add a `CHANGELOG.md` entry under `## Unreleased` (see the `release-changelog` skill).
