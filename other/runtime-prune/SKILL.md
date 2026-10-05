---
name: runtime-prune
description: >
  Inspect, plan, and invoke safe cleanup for runtime-manager-owned state
  without binding the workflow to a specific host orchestrator or agent
  provider.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-runtime-prune
    version: "1.0.0"
    created: 2026-05-13T00:00:00Z
    category: processkit
    layer: 2
    uses:
      - skill: skill-gate
        purpose: >
          Require explicit routing and confirmation before destructive
          cleanup.
    provides:
      primitives: []
      mcp_tools:
        - analyze_disk_usage
        - plan_prune
        - apply_prune
      assets: []
---

# Runtime Prune

## Intro

`runtime-prune` gives agents a provider-neutral cleanup workflow for
runtime-manager-owned state, repo-local generated artifacts, and remote
quota surfaces. It inventories selected cleanup scopes, produces a
dry-run plan, applies low/medium-risk processkit-owned cleanup from an
explicit allowlist, and returns structured host-action evidence for
high-risk runtime-owner or provider cleanup. It does not invoke host
orchestrator or provider deletion commands from inside the processkit
runtime.

## Overview

Use this skill when a project has accumulated runtime-home caches,
build caches, repo-local release/build artifacts, package-manager
caches, agent worktree state, container storage, E2E companion state,
or remote forge storage such as CI/action artifacts, release assets, or
package/container registry versions.

The workflow is:

1. Call `analyze_disk_usage(project_root, scopes)` to inventory
   configured cleanup scopes without modifying the filesystem.
2. Call `plan_prune(project_root, scopes)` to produce a dry-run plan,
   expected reclaimed bytes, risk labels, and the exact confirmation
   token needed for apply.
3. Call `apply_prune(project_root, scopes, confirmation)` only after
   the user has explicitly approved the plan. The apply tool may remove
   only explicit processkit-owned allowlist targets; provider/runtime
   owner cleanup returns an external host-action result for the owner.
4. For external provider scopes, use each action's `inventory_command`
   and `dry_run_command` first. The `apply_command` is concrete enough
   to run after human approval when the derived-project agent has the
   required CLI, token, and environment variables.

### MCP Tools

| Tool | Purpose |
|---|---|
| `analyze_disk_usage(project_root, scopes)` | Return structured size and risk data for selected cleanup scopes. |
| `plan_prune(project_root, scopes)` | Return a dry-run prune plan and required confirmation token. |
| `apply_prune(project_root, scopes, confirmation)` | Apply processkit allowlist cleanup and return external host-action evidence for unsupported scopes. |

### Scopes

| Scope | What it covers | Apply policy |
|---|---|---|
| `runtime-home` | Bounded runtime-home cache, diagnostics, tmp, and runtime paths. | Processkit allowlist cleanup. |
| `build-cache` | Explicit build-cache paths such as Rust incremental and build subdirectories. | Processkit allowlist cleanup. |
| `repo-artifacts` | Generated local artifacts such as `dist/`, `build/`, coverage, and test caches. | Processkit allowlist cleanup. |
| `tool-caches` | Project-local package/tool caches such as pip, uv, npm, pnpm, and node build caches. | Processkit allowlist cleanup. |
| `agent-worktrees` | Provider-created or runtime-manager-owned Git worktrees discovered from Git metadata. | External host action after explicit confirmation. |
| `containers` | Host runtime container cleanup. | External host action; no direct Docker or Podman calls. |
| `e2e-companion` | Nested companion environment cleanup. | External host action; companion access must use owner-approved reachability checks. |
| `action-artifacts` | Remote CI/action artifacts, logs, and stale workflow artifacts. | External provider action; no direct deletion. |
| `release-assets` | Remote release binary assets older than the support/retention window. | External provider action; no direct deletion. |
| `package-registry` | Remote package/container registry versions. | External provider action; no direct deletion. |

### External Runbooks

For external scopes, `plan_prune()` returns a provider-adapted runbook
instead of deleting anything:

- `required_env`: variables the derived-project agent or human must set.
- `inventory_command`: read-only command that lists current artifacts.
- `dry_run_command`: read-only command that prints deletion candidates
  and, when the provider exposes sizes, a byte total.
- `apply_command`: deletion command using the same candidate logic as
  the dry run. Run it only after explicit human approval.
- `space_estimate`: how to interpret `x` and `y` for "delete x and gain
  y" advice when the provider does or does not expose byte totals.

Provider adapters currently cover GitHub, GitLab, Codeberg, Forgejo,
Gitea, and generic/unknown forges. Unknown providers intentionally
return empty commands plus a note to fill the provider API details.

## Gotchas

- **Do not treat analysis as approval.** `analyze_disk_usage()` and
  `plan_prune()` are read-only. Apply still needs the exact confirmation
  token returned by the plan.
- **Do not hand-roll destructive provider cleanup.** `apply_prune()` may
  clean processkit-owned allowlist targets, but worktrees, containers,
  and companion state must return structured external host-action
  evidence instead of invoking a host orchestrator command.
- **Dry-run external cleanup first.** For `action-artifacts`,
  `release-assets`, and `package-registry`, use `inventory_command` and
  `dry_run_command` before proposing `apply_command`.
- **Do not remove the whole runtime home.** `runtime-home` targets only
  narrow cache, diagnostics, tmp, and runtime subpaths, not the whole
  `.aibox-home` tree.
- **Do not inspect local Docker or Podman for E2E companion cleanup.**
  Companion state is remote from the devcontainer's perspective; use
  the owner-approved host workflow that checks reachability.
- **Do not count arbitrary project files as reclaimable.** Only
  explicitly scoped runtime and cache paths contribute to expected
  reclaimed bytes.
- **Do not delete remote packages by age alone.** Keep source tags,
  release metadata, active deployment tags, and the supported-version
  window; delete binary assets or package versions only after an owner
  approves the exact target list.
- **Do not use Docker big-hammer cleanup by default.** Inspect first,
  prune builder cache separately, and avoid volume deletion unless the
  volume data owner is explicit.
- **Do not delete provider worktrees by path heuristics.** Worktrees
  are inventoried for visibility, but deletion is delegated to the host
  runtime manager because it owns provider-specific safety checks.
- **Keep paths provider-neutral in user-facing output.** Report scopes
  like `agent-worktrees` and `runtime-home`, not Claude-, Codex-, or
  shell-specific state unless a discovered path itself contains that
  name.

## Best-practice briefing

- Inventory before deletion: local `du`/tool reports, Docker
  `system df`/BuildKit usage, and repository-provider API listings
  should produce the target list before any apply step.
- Separate cleanup classes: generated repo artifacts, dependency
  caches, Docker build cache, Docker images/volumes, Actions artifacts,
  release assets, and registry package versions have different owners
  and risk profiles.
- Prefer retention policy over emergency cleanup: set short
  `retention-days` for non-release Actions artifacts, keep only the
  supported release-asset window, and apply registry lifecycle rules or
  scheduled cleanup for untagged/superseded images.
- Preserve reproducibility evidence: tags, release notes, checksums,
  SBOMs, provenance, and currently supported binaries should survive
  cleanup unless a release policy says otherwise.
- Use provider-neutral scopes first. `runtime-prune` adapts host-action
  hints for GitHub, GitLab, Codeberg, Forgejo, Gitea, and generic
  providers based on the repository remote.

## Full reference

`analyze_disk_usage()` resolves `project_root` to an existing directory
and defaults to all scopes when none are supplied. It never follows
symlinks during size walks.

`plan_prune()` returns:

- `required_confirmation`, formatted as
  `apply-prune:<comma-separated-scopes>`
- per-scope actions with `risk`, `apply_owner`,
  `expected_reclaim_bytes`, `targets`, `required_env`,
  `inventory_command`, `dry_run_command`, `apply_command`, and
  `space_estimate`

`apply_prune()` accepts only the exact `required_confirmation` value
from the matching plan. For `runtime-home` and `build-cache`, it removes
only the allowlisted paths from the plan. For external scopes, it records
per-scope host-action evidence and leaves execution to the owner outside
the container.
