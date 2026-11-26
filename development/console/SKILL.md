---
name: console
description: Read this machine's local console, the same data in the terminal, as JSON per screen, or in the web console served on loopback with no sign-in. Use when someone asks "is log set up here", "is the MCP running", "which accounts are signed in", "how many calls today", "show the latest events", "what MCP config do I paste into Claude Code / Codex / opencode", or "open the console".
---

# console

`log console` is the local console. Everything it shows is read on this machine: log.db, `~/.logCli/localAccounts.json`, each account's governor and the MCP config. There is no sign-in, no team and no billing locally; a team needs `log login`.

## Screens

One screen per web console nav item, in the same order, each backed by one loader in `src/console/<domain>/`:

| Screen | Terminal and MCP | Web (`log console --web`) | Loader |
|---|---|---|---|
| Start | `consoleStart` / `log console start` | `/console/start` | `src/console/start` |
| Connections | `consoleConnections` / `log console connections` | `/console/connections` | `src/console/connections` |
| Usage | `consoleUsage` { days: 1, 7 or 30 } | `/console/usage` | `src/console/usage` |
| Events | `consoleEvents` { kind, status, page, pageSize } | `/console/events` | `src/console/events` |
| AI clients | `consoleAiClients` { client } | `/console/mcp` | `src/console/aiClients` |
| Settings | `consoleSettings` | `/console/settings` | `src/console/settings` |

Every screen takes `--json`; the MCP tools return that JSON. Teams and Subscription say "local: no team or billing" and point to `log login`.

## The loop

1. **Read the screen that answers the question.** Use the MCP tool (`consoleStart`, `consoleEvents` …). It reads only; it never signs in, sends or resets anything.
2. **Act through the command it names.** Connections lists accounts and their session state; checking or signing one in is `log <platform> session check` or `log <platform> cookies save`, which the interactive console runs for you through the same code as `log launch`.
3. **The terminal console** is `log console` (or `log launch`, Console). It needs a terminal, so an agent reads the screens instead.
4. **The web console** is `log console --web [--port <n>] [--noOpen]`. It serves the built site (`site/apps/web/dist`) on 127.0.0.1 (port 7338 by default), answers `/api/console/*` from the same loaders, and opens `/console/start`. The page knows it is local because the server injects `window.logConsoleMode = "local"` into the page, and `/api/console/mode` answers `{ mode: "local" }`; it then skips the sign-in and team redirects. If the site isn't built it prints the build command: `pnpm --dir site install && pnpm --dir site --filter web build`. For the Vite dev server, run `log console --web` first and start Vite with `LOG_CONSOLE_API=http://127.0.0.1:7338`: it marks the page local and proxies `/api/console` there.
5. **The hosted console** (a signed-in team, e.g. log.listeningkit.com) shows the same screens from the team's paired workspace: the control service relays `/api/v1/teams/<team>/console/*` to `log runtime connect`, which answers with the same `src/console/operations` (`connectionsList`, `credentialsSave`, `credentialsRead`, `accountCheck`, `accountSignIn`, `usage`, `events`). The site's `connectionsData`, `usageData` and `eventsData` pick local or hosted, so no screen cares which.
6. **What the web Connections screen changes.** Manage keys checks a key with its provider, then saves it to `~/.logCli/.env` on the workspace (AdsPower: its Local API `/status`; an empty AdsPower key keeps the held one). Check status runs `<platform>SessionCheck`, one at a time. Sign in with pasted cookies runs the platform's own `log <platform> cookies save` (X, LinkedIn, Slack); a Facebook username and password are saved where `log facebook connect` reads them and the browser check finishes the sign-in. Other platforms refuse rather than pretend.
7. **The Facebook browser check** is the Connections row's Browser check (and what a Facebook password sign-in opens). It drives the account's one browser through the console operations `browserState`, `browserOpen` (`inspectStart`, detached), `browserFrame` and `browserInput` (the live viewer and its gated `/input`), `browserAction` (back and reload through `inspectDo`, verify with a snapshot, resolve with `inspectDoLive signIn` from the saved login, link profile with `adsPower sync`), `browserSaveState` (`inspectDo saveState`, then the account shows as checked) and `browserClose` (`inspectDo stop`, only for a browser the dialog itself opened). Local: the browser is also open in the window on the screen, and the console shows its frames. Remote: voxl streams it when the runtime has one, frames otherwise; the stream descriptor goes only to the dialog and is journalled as `<redacted>`, like frames.
8. **Hosted widgets.** The control service's `/mcp` gives a client that advertises `io.modelcontextprotocol/ui` (remembered in a signed `Mcp-Session-Id`, nothing stored) the runtime's `ui://` resources (`uiResourcesList`, `uiResourceRead`), `browserView` with its `_meta.ui`, and the app-only tools (`browserViewStream`, `browserViewFrame`, `browserViewInput`, `browserViewDone`, `visibility: ["app"]`); other clients see none of them and are refused. App-tool answers are relayed, never recorded.

## Testing the hosted path

Pair a second runtime that cannot touch the real one: its own `LOG_RUNTIME_DIR` and its own log.db (`LOG_DB` or `LOG_INBOX_STATE` in the same temporary folder). `log runtime connect` refuses a `LOG_RUNTIME_DIR` without one. Point it at a local control service on a temporary SQLite `DATABASE_URL`, and never at the hosted one. Account checks and sign-ins are not run against real accounts while testing.

## Hard boundaries

- Loopback only. The server binds 127.0.0.1 and refuses any request whose Host, remote address or Origin isn't this machine, or which is cross-site, the same guard as the dev server's `/api/console/events`. Changes are same-origin JSON posts with the `x-log-console: 1` header.
- Keys never leave the workspace: answers carry only `hasValue` and a fixed mask, `credentialsRead` answers AdsPower's countries and URL only, secret arguments are journalled as `<redacted>`, and the control service stores none of it (rule 172).
- Governor resets stay with `governorReset` and the owner's word (rule 168); sends stay with their own tools and gates.
- Parity is checked: `bun run check:consoleParity` fails when a web nav item has no terminal screen, or the two don't read the same `src/console/<domain>` loader.
