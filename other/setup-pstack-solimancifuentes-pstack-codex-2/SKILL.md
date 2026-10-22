---
name: setup-pstack
description: "Configure supported pstack role and panel choices for Codex or Dots in an optional user profile. Use for setup-pstack, configure pstack models, or changing pstack runtime choices. Show concrete changes and preserve unrelated preferences."
---

# Setup pstack

Configure supported workflow choices without editing the installed skills or
host-global instructions. Read [CODEX.md](../../CODEX.md) to select the actual
host adapter. This skill is discoverable for configuration requests. It makes
no silent changes during ordinary work.

## 1. Inspect the current choices

Resolve the package root from this loaded skill's actual path. Read
`defaults.json` at that root and the optional local profile at
`~/.codex/pstack-codex/preferences.json`. The plugin works when the profile is
absent. To show the effective choices without writes, use the bundled launcher:

```text
python3 <PLUGIN_ROOT>/tools/runtime.py profile show
```

Substitute the observed absolute root path and quote it for the shell. No
separate `pstack-codex` installation is needed. If Python or file access is
unavailable, read the accessible defaults/profile and report the persistence
limit. Do not create settings in a different environment by guesswork.

The profile is local to the executing machine. Do not assume a connected Mac's
profile is present in a cloud Codex task. A coordinator may include the relevant
chosen preferences in a worker brief. Preserve the original task's environment
unless the user requested a migration.

Default every role to `inherit-parent`. Inspect current model and reasoning
options only when a concrete model change is requested. Cursor's source
Claude/Grok mix and fast-mode slugs are unavailable controls, not choices to
translate into invented names. A panel count is total seats, queued within
actual runtime capacity. Defaults are two arena candidates, two architect
candidates, and two independent interrogate reviewers.

## 2. Show the concrete change

State the actual profile path, current effective values, and exact proposed
changes. Preserve unrelated profile keys, `always_apply`, `implicit_invocation`,
application-driver choices, and other settings. Routing changes must come from
the user's selection or an existing authorized preference. If the user already
chose values in this session, do not ask again.

When guidance is requested, ask only what changes the outcome. Model and effort
values must come from the executing host's actual tools. Inheritance leaves
overrides absent. A persona does not select a model or grant provider diversity.
A budget label does not set an account spending limit. Capability notes do not
provision cloud computers, schedules, providers, or credentials.

## 3. Validate and apply

Write a temporary JSON file containing only the supported choices the user
selected. The launcher validates the profile structure, merges it with existing
choices, and previews the exact write:

```text
python3 <PLUGIN_ROOT>/tools/runtime.py profile set --file <CHANGE.json> --dry-run
python3 <PLUGIN_ROOT>/tools/runtime.py profile set --file <CHANGE.json> --yes
```

Use `--profile <ABSOLUTE_PATH>` only when a different profile location was
explicitly selected. Check model/effort availability against the live tool
schema before persistence; structural validation alone cannot establish that a
host accepts an override. Honor existing installation/configuration preview
preferences. Apply when the session already authorizes the concrete choice.
Do not overwrite the installed cache, global `AGENTS.md`, host configuration,
or another machine's profile. Never materialize defaults over unknown personal
settings merely to complete setup.

## 4. Confirm

Show the profile again and report its exact effective choices. A saved
preference guides future supported workflow dispatch; it does not register a
custom native agent, force automatic skill selection, or create a persistent
UI mode. Existing workers retain their launch settings. User profile data stays
outside plugin releases so package updates and rollback do not replace it.

## Optional app verification

When requested app verification lacks a project driver, use
`create-verification-skill`. Building and proving a driver is a separate task
from model configuration.
