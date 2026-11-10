---
name: rozenite
description: Inspect the live Apex Factory app through Rozenite for Agents — network requests, console messages, the React component tree and renders, performance traces, heap snapshots, and the app's own tools — on a debug build with Metro started by .agents/scripts/device-lane.sh metro start. Use to collect evidence for a failing simulator check or a bug report, or when someone asks to debug the running app.
---

# Rozenite in this repo

Vendored from `callstackincubator/rozenite` v2.4.0 (see `SOURCE.md`) and adapted. Rozenite
for Agents is a JSON CLI over Metro's `/rozenite/agent/*` routes; there is no MCP server. The
CLI and its plugins are `apps/mobile` devDependencies, pinned.

It sees only a **debug build connected to a Metro started with `WITH_ROZENITE=true`**. A
Release build, the booth binary and OTA bundles contain no Rozenite code, so Rozenite is a
diagnosis tool: the Release run decides pass or fail, a debug run explains a failure.

## Set it up on a lane

```bash
.agents/scripts/device-lane.sh build ios debug        # detached; wait for <log>.exit (needs no lease)
.agents/scripts/device-lane.sh lease ios
.agents/scripts/device-lane.sh install
.agents/scripts/device-lane.sh metro start            # this lane's own port, WITH_ROZENITE=true APPDUCT_ENABLED=1
.agents/scripts/device-lane.sh ad open com.callstack.apexfactory --foreground   # the lane points the app at its Metro
```

## The loop

```bash
.agents/scripts/device-lane.sh rozenite targets                   # every app on this Metro
.agents/scripts/device-lane.sh rozenite session                   # creates (once) and prints the lane's session id
.agents/scripts/device-lane.sh rozenite domains                   # console, network, react, performance, memory, app, controls, …
.agents/scripts/device-lane.sh rozenite network call --tool startRecording
# reproduce the problem with device-lane.sh ad …, then:
.agents/scripts/device-lane.sh rozenite network call --tool listRequests
.agents/scripts/device-lane.sh rozenite console call --tool getMessages
.agents/scripts/device-lane.sh rozenite app call --tool app.app_info   # the appduct tools, through Metro
.agents/scripts/device-lane.sh rozenite reset                     # forget the session (after an app reload)
```

The lane appends `--session <id>` and puts `--port <metro port>` before the subcommand, so do
not pass either. A target is named after its device (`simlock-<id>` on a leased simulator).
The lane's Metro has a port of its own, so normally its app is the only target; the lane takes
it, and stops when there are several (`APEX_ROZENITE_TARGET=<part of a name>` picks one).
Another app connected to the same Metro would show up in `targets` too: check the data
(`rozenite app call --tool app.app_info`) before trusting a target.

`ad open com.callstack.apexfactory` on a debug build hands the dev client the lane's Metro and
answers iOS's "Open in" prompt itself. The first load bundles over Metro and shows the splash
screen: `device-lane.sh ad wait text "On purpose." 60000` before the next step.

- Calls within a session are serial: never run two Rozenite commands at once.
- A session created before the app (re)loaded misses the plugin domains (`app`, `controls`,
  `network-activity`): `rozenite reset`, then `rozenite session` again.
- `session stop` can hang on 2.4.0; `reset` only forgets the id, and the session ends with
  Metro or the app (`device-lane.sh release` stops Metro).
- An agent session takes the app's one debugger connection, so it disconnects a person's
  React Native DevTools.
- Traces and heap snapshots are written under `apps/mobile/.rozenite/` (gitignored). Name the
  file in a report; never commit it.

## The docs ship with the CLI

The real content is bundled with the installed CLI, so it matches the pinned version. Read it
from `apps/mobile` (pnpm, never `npx`):

```bash
cd apps/mobile && pnpm exec rozenite skills list         # id and one line per doc
cd apps/mobile && pnpm exec rozenite skills show core    # ground truths; read this first
cd apps/mobile && pnpm exec rozenite skills show cli     # command syntax, sessions, pagination
cd apps/mobile && pnpm exec rozenite skills show network # then the domain you need
```

Those docs write commands as `npx rozenite agent …`; here each one is
`.agents/scripts/device-lane.sh rozenite …` without `--port` and `--session`.
