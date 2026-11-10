---
name: appduct
description: Call the tools the running Apex Factory app registers with appduct (read app state, jump to a route, run an OTA check now, emulate the update banner, a feature's own seed tools) through .agents/scripts/device-lane.sh, and write or review those tools in apps/mobile. Use when a check needs app state or a deep screen without tapping through the UI, when a spec's Agent hooks names an appduct tool, or when someone mentions appduct.
---

# appduct in this repo

Vendored from `callstackincubator/appduct` v0.14.0 (see `SOURCE.md`) and adapted. appduct lets
an agent call functions the running app registered as **tools**. One `appduct` daemon on this
machine (`~/.appduct/daemon.sock`, TLS WebSocket on `:8443`) holds every device session; the
CLI starts it on first use. The CLI is the workspace's pinned devDependency.

appduct ships in every build of this app: the booth binary, every OTA bundle and every lane
build use `APPDUCT_ENABLED=1` (ADR 0007). So a Release build on a leased simulator has the
same tools as a debug build.

## The loop, on a lane

Factory agents reach appduct only through the lane script, which keeps each lane on its own
session id (two paired apps make a bare `appduct tools ls` fail with `ambiguous_session`):

```bash
.agents/scripts/device-lane.sh appduct link                   # pair the app running on the leased device
.agents/scripts/device-lane.sh appduct ls                     # one signature + description per tool
.agents/scripts/device-lane.sh appduct describe open_route    # one tool's full schema
.agents/scripts/device-lane.sh appduct call app_info          # input defaults to {}
.agents/scripts/device-lane.sh appduct call open_route '{"path":"/"}'
.agents/scripts/device-lane.sh appduct events ls              # events the app declares
.agents/scripts/device-lane.sh appduct events since 0 --name 'ota.*'
```

- `link` mints a one-time link (`appduct sessions link --json`, valid 5 minutes, usable once)
  and has agent-device open it inside simlock's device set, accepting iOS's "Open in Apex
  Factory?" prompt. appduct's own `--open ios-sim` cannot see that set; do not use it.
  The app must be running (`device-lane.sh ad open com.callstack.apexfactory` first).
- A session survives JS reloads and backgrounding. A relaunch (`ad open --relaunch`, a
  `replay` that relaunches) kills the process and the session: `link` again.
- `call` prints `{ "ok": true, "data": … }`; a failure is `{ "ok": false, "error": { "type": … } }`
  on stderr with a non-zero exit (71 session, 72 tool error, 77 `policy_denied`).
- `events tail` never ends, so the lane offers `events ls` and `events since <cursor>` only.

## This app's tools

| Tool                                   | Does                                                                                             |
| -------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `app_info`                             | version, platform, channel, bundle id (embedded or OTA), fingerprint, current route, every route |
| `open_route {path}`                    | navigate to a route by path, e.g. `/features/12`; refuses a path no route matches                |
| `ota_check_now`                        | run the OTA check now instead of waiting up to 30 s (`staged`, `no_update`, …)                   |
| `show_update_banner {message?, kind?}` | show the "New feature landed" banner without a deploy                                            |
| `hide_update_banner`                   | hide it                                                                                          |
| `reload_app`                           | restart into the staged bundle — destructive, denied by the operator policy unattended           |
| `api_health`                           | call `/health` through the contract client, as the footer does                                   |
| event `ota.update_staged`              | posted when a real bundle has downloaded                                                         |

A shipped feature adds its own tools under the group `features/<id>`
(`src/modules/<id>/agent-tools.ts`, listed in `src/modules/agent-tools/features.ts`). Read the live
list with `appduct ls --groups`; the app, not this table, is the source of truth.

## Output and errors

- `no_session`, `unknown_session`: the app never claimed the link (it was not running, or the
  prompt is still up). `link` again.
- `policy_denied`: the operator policy (`~/.appduct/config.json`) blocks this tool — today
  every `destructiveHint` tool such as `reload_app`. Do not retry and do not edit the policy;
  use the UI path (tap the banner) and say which tool was denied.
- `tool_timeout`: a call gets 10 s unless the tool registered `timeoutMs`. The fix is in the
  app's registration, not a longer `--timeout`.
- `session_suspended`: the app is in the background. Bring it to the foreground
  (`ad open com.callstack.apexfactory`); the session resumes by itself.
- `tool_execution_error`: the app's handler threw; report its message as evidence.

## Writing tools (implementer)

When a spec's **Agent hooks** names a tool the app does not have yet, add it in the same PR,
following `apps/mobile/AGENTS.md` ("Agent tooling rules") and
`references/writing-tools.md`:

- A feature's tools live in `src/modules/<id>/agent-tools.ts`, exported from the module's
  `index.ts` and appended to `featureAgentTools` in `src/modules/agent-tools/features.ts`;
  core tools are in `src/modules/agent-tools/`. Nothing else imports `@appduct/react-native`
  (`pnpm boundaries` checks it).
- Name by intent (`seed_cart`, not `set_state`); a zod `inputSchema` with `.describe()` on every
  field; an object `outputSchema`; `readOnlyHint` on observers; a mutation returns the new state
  and has an observer; `destructiveHint: true` on anything that deletes, resets or restarts.
- Tools ship in production builds: never return a secret or a visitor's data.
- Handlers are plain functions over injected dependencies, with Jest tests next to them. A tool
  is JS: adding one is not a native change.

## Over MCP

Only the interactive `build` agent has the `appduct` MCP server (`opencode.json`); every
factory agent is denied its tools and uses the lane script. Over MCP the same loop runs through
`appduct_connect` → `appduct_wait_for_session`, then `appduct_list_tools`,
`appduct_describe_tool`, `appduct_call_tool` and `appduct_list_events`; pass `selector` when
more than one device is paired. On a simlock device, mint the link without delivery
(`appduct_connect` with `target: "none"`) and open it with agent-device.

## References

Read a reference only when its trigger applies:

- `references/cli.md`: a command or flag not shown above, or a script with `appduct/client`.
- `references/writing-tools.md`: adding, changing or reviewing tools in the app's code.
- `references/setup.md`: upstream setup guide. This app is already set up; read it only to
  understand an existing piece (config plugin, Metro helper, build variants).
