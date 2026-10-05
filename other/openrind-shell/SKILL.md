---
name: openrind-shell
description: Launch and diagnose the required Haloop-routed PostgreSQL FUSE runtime in Openrind Desktop.
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [optional: sandbox name or workspace ID]
---

# Openrind Shell

## Supported launch flow

1. Configure PostgreSQL and the upstream provider credential in Desktop Settings.
2. In **Sandboxes**, choose **New sandbox → Claude Code** (or OpenClaw).
3. Desktop registers the scoped Haloop provider, creates the agent-home named
   volume, initializes FUSE, and issues a signed conversation context.
4. Select an existing sandbox to return to its live session. After `/exit`, use
   **Reconnect** for a new signed launch. Keep the agent-home volume for history.

Do not invent a provider ID for a standalone CLI launch. Never use
`--auto-providers`, a direct Anthropic provider, or an unsigned `claude` command
as a substitute. Missing Haloop readiness blocks launch; recovery uses Desktop's
restart/reconnect controls, never a direct-provider fallback.

## Diagnostics

Read `README.md` and `openrind-desktop/apps/desktop/OPENRIND_SHELL.md` for the
current flow and `BUILD.md` for source builds. Do not rebuild NVIDIA's base.
Never print database URLs or provider keys, or pass provider keys through `--env`.

Use the paired patched CLI and gateway for FUSE diagnostics. Run
`sandbox exec -n <sandbox-name> -- openrind-shell-fused health` through that CLI
with the managed gateway endpoint. The filesystem state must be `writable`.
`Ready` alone does not prove initialization succeeded. A manual
`sandbox connect` opens a diagnostic shell, not a signed agent launch.

## Persistence and safety

- `/sandbox/work` is PostgreSQL-backed FUSE, not a watched or mirrored folder.
- Claude uses `/sandbox/claude-home`, on a separate persistent named volume.
- One writable sandbox per workspace; do not create a duplicate to resume.
- FUSE daemon exit or lease loss ends the session. Never grant Claude mount
  capabilities, `/dev/fuse`, or a PostgreSQL/TLS-bypass fallback.
- Never delete a sandbox or volume without the user's explicit request.
- Compatibility is a separately requested legacy runtime, not recovery for a
  failed mandatory Haloop launch. Do not reuse its old provider recipe.
- Desktop captures traces only. Export them to the w8-haloop web app for analysis
  and Harbor task generation. Post-start capture is best-effort; a successful
  inference response does not prove its trace was stored.
