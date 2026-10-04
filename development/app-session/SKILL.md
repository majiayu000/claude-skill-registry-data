---
name: app-session
description: "Census/launch/teardown for a repo's declared app."
version: 1.0.0
allowed-tools: ["Read", "Bash"]
---

# App Session

Stateful lifecycle around a repo-declared app: three named verbs, keyed by target, backed by
per-repo config declared in `coordinator.local.md`'s `app_session` mapping.

<!-- TEMPLATE: illustrative config shape, not a literal value to invoke -->
```yaml
app_session:
  desktop:
    runtime: electron
    command: pnpm dev
```

Each key under `app_session` is a **target name** (`desktop` above); its value is an object
carrying a `runtime` discriminator (`electron | command | server | ...`) plus runtime-specific
fields. An unrecognised or absent `runtime` degrades to a plain argv command with no resolution
step -- the electron-specific resolution mechanics are out of this skill's scope (wiki).

## Verbs

Each verb dispatches through the `app-session` trampoline, one binary three verbs, which routes
to the control-plane engine's `app_session.census` / `app_session.launch` / `app_session.teardown`
ops and prints that op's own result object verbatim as JSON.

- **census** -- reports the current state of a target: whether it is running, and (where the
  runtime resolver supports it) which process/port it occupies. Read-only; makes no state
  change. `--key` is optional -- omitted, it lists every persisted handle in the repo.

  Invoke through the `.exe` launcher by absolute path via the PowerShell call operator (Shape W).
  Ladder and shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.

  `& "$env:COORDINATOR_SETTINGS_HOME\bin\app-session.exe" census --key <target>`

  `& "$env:COORDINATOR_SETTINGS_HOME\bin\app-session.exe" census`

- **launch** -- starts a target per its `app_session` config and records that it is running, so a
  later `census` or `teardown` call can find it. Fails loudly on a launch error -- this verb's
  failures propagate rather than being swallowed.

  `& "$env:COORDINATOR_SETTINGS_HOME\bin\app-session.exe" launch --key <target>`

- **teardown** -- stops a previously launched target and clears its recorded state. Matches the
  specific command line it launched rather than a blanket process kill, because this machine
  routinely runs concurrent sessions against the same runtimes (wiki).

  `& "$env:COORDINATOR_SETTINGS_HOME\bin\app-session.exe" teardown --key <target>`

`<target>` is the `app_session` mapping key (`desktop` above). `--repo-root <path>` is accepted on
every verb but normally omitted -- it defaults to the git toplevel. Exit code 0 covers both a real
result and a structured "not configured" one (see § No config, no effect); 2 is a usage error; 3
is a transport/op failure.

This is a lifecycle, not a one-shot action: `launch` without a later `teardown` leaves state
behind for `census` to report and a future `teardown` to clear.

## Config resolution

Each op resolves its target's config via `cs_read_local_md_mapping(repo_root, key) -> dict`
(`coordinator_core/resolve_validation_cmd.py`), not `cs_read_local_md_key`: the `app_session`
value is a mapping of target name to a nested per-target object (`runtime`, `command`, ...), and
`cs_read_local_md_key`'s flat-string/flow-list reads can't see into that nesting -- only the
mapping reader can. The resolver returns a bare `dict` for a present, well-formed target key, and
`None` for an absent or malformed one -- there is no typed dataclass in this path, unlike
`doc_registry.py`'s `DocRegistryConfig`. Callers turn the `None` case into the structured
"not configured" result described below rather than raising.

## No config, no effect

A repo whose `coordinator.local.md` declares no `app_session` keys is not an error -- every verb
degrades to a silent no-op, because `app_session` is opt-in capability, not an assertion the repo
is verifiable. This is a deliberate divergence from `fast_test_cmd`, which fails loud on an
absent key at a cadence gate (`validate/SKILL.md`) -- that gate asserts the repo is verifiable,
and `app_session` makes no such assertion for a repo that never opted in. Concretely, this is a
`cs_read_local_md_mapping` empty-dict result, the target key absent from it, and `None` from the
resolver with no configured command to run, which the launch/teardown ops turn into the structured
`{"ok": true, "configured": false, ...}` result rather than an error -- exit 0, not a failure exit.

`app_session` also deliberately carries no environment-variable override rung, unlike
`fast_test_cmd`'s env -> frontmatter -> skip-with-notice ladder. The configured value spawns a
process rather than running a test command, and an env-settable spawn target is a materially
worse blast radius than an env-settable test command -- so resolution reads only
`coordinator.local.md`, never an environment variable. Both of these are stated defaults the ops
ship with, not gaps this skill works around.

## Relationship to the platform's `run` skill

The harness ships a built-in `run` skill that states a preference for a project skill over its
own built-in fallbacks (CLI, server, TUI, Electron, browser-driven, library) -- this is the
platform's stated preference, not a verified registration relationship; the exact discovery
mechanism is unconfirmed. `app-session` is complementary to `run`, not competing with it: `run` is
one-shot "start it and look at it", while `app-session` is the stateful, multi-verb
census/launch/teardown lifecycle around a target with per-repo config. `app-session` is not named
`run`, `run-app`, or `run-desktop` because `run` is a taken platform primitive -- the name
`app-session` names the lifecycle itself, not the launch verb.
