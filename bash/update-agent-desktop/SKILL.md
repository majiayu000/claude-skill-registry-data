---
name: update-agent-desktop
description: Bump the agent-desktop CLI that runs agents' computer use on the host, and regenerate the agent-facing computer-use guides from its bundled skills. Use when a new agent-desktop release is out, when computer use misbehaves after an agent-desktop change, or when the version-stamp test in scripts/generate-computer-use-docs.test.ts fails.
---

# Update agent-desktop

Computer use runs the `agent-desktop` npm package on the host (`src/shared/lib/computer-use/`). The agents' tools are generated from each command's `--help` (`agent-desktop-tools.ts`, one copy in `src/shared/lib/computer-use/` and one in `agent-container/src/tools/`), and their guides from the skills that ship inside the same version (`agent-container/docs/computer-use.md` + `computer-use/`). A bump touches all of them, in one change.

## 1. Pick the version

- Releases and changelog: https://github.com/vercel-labs/agent-desktop/blob/main/CHANGELOG.md (`npm view agent-desktop time --json` for dates).
- The repo `.npmrc` sets `min-release-age=7`: a version younger than 7 days fails to install with `ETARGET`. **Never edit `.npmrc`.** Pick the newest version past the cooldown, or ask the user before a one-off `npm install --min-release-age=0 …` — a fresh ask each time; it is their security policy.

## 2. Read the changelog between the two versions

Look for, and fix in the same change:

- **Envelope / JSON contract** (`"version"` in every envelope, `docs/json-output.md` upstream): the Zod schemas in `src/shared/lib/computer-use/agent-desktop.ts` (envelope, snapshot, list-windows `app_name`, launch, screenshot `data`, permissions, `session start`).
- **CLI flags and commands**: the refused commands/flags, the read-only/observation sets and the target extraction (`callTargets`) in `src/shared/lib/computer-use/commands.ts`; the params → argv mapping in `command-line.ts`; in `scripts/lib/computer-use-docs.ts`, `TOOL_COMMANDS` (the commands that get their own tool), `REFUSED_COMMANDS`, `HOST_OWNED_FLAGS`, what the guides leave out (`DROPPED_SECTIONS`, `DROPPED_LINES`, `REPLACED_TEXT`) and the guide header template. A new global flag that changes what runs (like `--headed`, `--session`) belongs on the refused list.
- **Ref format** (`@<snapshot>:eN`): `QUALIFIED_REF` in `commands.ts`.
- **Binary and helper names** (`node_modules/agent-desktop/bin/`): `resolveAgentDesktopBinary()` in `agent-desktop.ts`, `extraResources` in `package.json` (mac and win) and `LEFT_OUT_RESOURCES` in `electron-builder.mas.cjs`. The packaged executable must stay named `agent-desktop` — the macOS cursor overlay is a child the CLI starts by re-running itself, and it starts none from a binary by another name.
- **The cursor overlay's socket** (`crates/macos/src/system/cursor_overlay/`: `PROTOCOL_VERSION` and the socket name in `endpoint.rs`, the `show` control in `control.rs`, `CURSOR_IDLE_REST_MS` in `crates/core/src/cursor_overlay/timing.rs`): `src/shared/lib/computer-use/cursor-keep-alive.ts` sends that control to that socket to keep the cursor on screen during a turn, which the CLI does not offer. A change to any of them leaves the cursor fading between an agent's steps, with no error. If the CLI gains a flag for the idle time, pass it on `cursor-overlay enable` and delete the keep-alive.

## 3. Install and regenerate

```bash
npm install agent-desktop@<version> --save-dev --save-exact
npm run docs:computer-use        # from the binary's `skills get` + each command's --help
git diff --stat agent-container/docs/ src/shared/lib/computer-use/agent-desktop-tools.ts agent-container/src/tools/agent-desktop-tools.ts
```

It stays a dev dependency: no bundle imports it. The packaged app runs the copy `extraResources` puts in the bundle, and a run from source finds the package's binaries in `node_modules`. In `dependencies` it fails `npm run check:runtime-deps`, which allows only packages a shipped bundle imports.

The generator falls back to the release tag on GitHub when the binary cannot run here; that source has no `--help`, so `computer-use/flags.md` is left out and the guides keep pointing at `--help`. Regenerate from the binary before merging.

Review the guide diff as an agent would read it: new commands to map in the header, advice that now contradicts what the app decides (input mode, sessions, cursor, refused flags, OS permissions: the app checks them before a call runs and asks the user, so no guide may tell an agent to check or grant one; `generate-computer-use-docs.test.ts` fails on leftovers).

## 4. Verify

```bash
npx tsc --noEmit
npm run lint
npx vitest run src/shared/lib/computer-use scripts/generate-computer-use-docs.test.ts src/main/agent-desktop-resources.test.ts src/main/mas-build-config.test.ts
npm --prefix agent-container test -- computer-use system-prompt-vars
```

Then drive one app end to end in the dev app (snapshot → click → snapshot, with the cursor on), and rebuild the agent image so the new guides ship: `npm run build:container`.
