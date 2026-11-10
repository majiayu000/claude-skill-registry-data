---
name: clarila-dev
description: "Run, inspect or repair the local development environment and its supervisor in the current project or verified worktree. Use for process ownership, multiple local instances, start and stop safety, and the dedicated HeyAmara stack procedure."
metadata:
  version: "2.0"
---

# Run the current project's development environment

Read the [shared workflow contract](../clarila/references/contract.md). Resolve the actual project/worktree and requested action before starting or stopping anything.

1. Read repository instructions, package scripts, workspace configuration, runtime documentation and existing process/port state. Identify the project's own toolchain, entrypoints, required services and configured URLs. Use the requested worktree's code. Do not assume every project uses Bun, Expo, Docker or the HeyAmara ports.
2. For HeyAmara, follow the [HeyAmara supervisor procedure](references/heyamara.md) and its deterministic scripts. Its staging-env refresh, slot formulas, output contract and safeguards apply to that adapter only.
3. For other projects, use the existing documented development commands and dependency manager. Inspect the actual package/workspace scripts before choosing a command. Reuse a healthy matching instance; preserve unrelated listeners and other worktrees. When the project has no executable documented path, report the concrete prerequisite instead of inventing one.
4. Announce starts, stops, installs and environment-file changes. Use a persistent task-owned process/session when needed; retain its identity, log and configured ports. An inspect/list/doctor request does not authorize startup. Install a missing dependency only when necessary and authorized; use existing lockfiles. Environment pulls/replacements, migrations, seeds, public exposure and external-effect workers require their actual task authority.
5. Wait for observable readiness, then exercise the relevant local health or smoke path. Verify frontend/API/worker connections when applicable. A listening port alone does not establish application readiness; Metro alone does not prove a native app is installed or connected. Use [clarila-capture](../clarila-capture/SKILL.md) for requested browser/device evidence.
6. Stop only positively identified task-owned processes on request and verify the selected target stopped. Never kill an unknown port owner, reset data or terminate a shared service just to free a port.

Use the project's documented readiness check with a bounded wait. On failure, retain the same process identity and inspect its log and failing dependency before selecting a retry or configuration change. Verify that a reused endpoint serves the intended worktree and environment. Record an actual health observation or action that reaches the relevant dependency.

Return the actual project/worktree, command, observed state, usable URLs, process/log ownership, checks and remaining prerequisites. Keep secrets out of output. Read-only inspection remains useful when startup is blocked.
