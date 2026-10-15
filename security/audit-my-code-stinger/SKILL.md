---
name: audit-my-code-stinger
description: Orchestrates /audit-my-code. Five tiers (foundation, vibe, basic, full, mario) of codebase audits, dispatched to paired Drones and delivered as a Legion Code Inc. brief.
license: AGPL-3.0-or-later
compatibility: Claude Code 2.1 or newer, Cursor 2.4 or newer, Codex, Cowork. Bloat tools need Node 20 and npx; Mario tier needs the Wasp Nest core.
metadata:
  author: Legion Code Inc.
  designed-by: Legion Code Inc.
  homepage: https://www.legioncodeinc.com
  hive-tier: orchestrator
  hive-role: audit-dispatcher
  domain: code audit orchestration
  version: 1.0.0
---

# Audit My Code Stinger

Designed and built by [Legion Code Inc.](https://www.legioncodeinc.com)

Orchestrator-tier skill with no paired Drone, the same pattern as `pest-controller-suit` and `master-website-auditor`. It runs in the main session because only the main session can dispatch Drones.

## Where this skill's files are

Every path below is relative to the folder that contains this `SKILL.md`. In Claude Code that folder is `${CLAUDE_SKILL_DIR}`. If that text was not replaced with a real path, find the folder with Glob (`**/audit-my-code-stinger/SKILL.md`) and use it as the skill directory in every command.

## Requirements

- `git` and Python 3.9 or newer on every platform. The orchestrator's own steps (`scripts/make_scratch_copy.py`, `check_workspace.py`, `merge_security.py`, `build_evidence_index.py`) are plain Python and run on macOS, Linux, and Windows.
- The bloat Drone's tool commands (`code-bloat-stinger/references/tool-commands.md`) and some security Drone commands are bash. On Windows, run those Drones from Git Bash or WSL; PowerShell and cmd cannot run them. Node 20 and npx are needed for jscpd and knip.

## Purpose

Audit a codebase the way Mario audits one by hand: measure before judging, rule out false alarms before reporting, lift every tool limit that would hide the worst code, and answer the question the person actually asked. The user picks a tier; this skill dispatches the Drones that tier needs, verifies their output against one shared contract, and hands the result to the brief renderer. It never audits code itself and never changes the audited repository, except for the `library/` documents a Mario Audit user approves by name.

## When to use

- The user runs `/audit-my-code`, with or without a tier
- "Audit my code", "is this codebase bloated", "how bad is this vibe-coded app", "security audit my Next.js app", "give me a remediation plan for this repo"
- A harness cannot run the command file: this skill carries the same procedure

## When not to use

- Auditing a live website from the outside: that is `/perform-website-audit` and `master-website-auditor` in the `website-audit-tools` pack
- Capturing a running web app's UI: `/webapp-capture` and `webapp-capture-stinger` in the `browser-and-app-testing-tools` pack
- Fixing the findings: route the remediation PRDs through `/smoke-it` and IRDs through `/pest-controller`
- Reviewing a single diff before commit: `/ship-gate`

## Procedure

1. Read [references/audit-contract.md](references/audit-contract.md) in full. Every step below depends on it.
2. Intake: [guides/00-tier-menu-and-intake.md](guides/00-tier-menu-and-intake.md). Resolve the tier (show the menu if none), resolve the repository, ask the intake questions, detect stacks, create the workspace and the throwaway copy (`scripts/make_scratch_copy.py`), write `intake.json`.
3. Dispatch W1 per [guides/01-wave-dispatch.md](guides/01-wave-dispatch.md), with security routing from [guides/02-security-routing.md](guides/02-security-routing.md) for `basic` and above. Merge security output with `scripts/merge_security.py`.
4. Verify each Drone's output per [guides/05-verify-and-deliver.md](guides/05-verify-and-deliver.md) with `scripts/check_workspace.py`.
5. For `full` and `mario`, run W2 quality per [guides/03-quality-standalone.md](guides/03-quality-standalone.md).
6. For `mario`, run W3 per [guides/04-mario-tier.md](guides/04-mario-tier.md), including the consent gate.
7. Run the whole-workspace check, remove the throwaway copy, and dispatch the brief renderer (W4).
8. Deliver per [guides/05-verify-and-deliver.md](guides/05-verify-and-deliver.md).

## References map

| Path | Load when |
| --- | --- |
| `references/audit-contract.md` | Always, first |
| `references/tier-matrix.md` | Showing the menu, or deciding which dimensions and brief sections a tier gets |
| `references/intake-script.md` | Asking the intake questions |
| `references/arming-lines.md` | Dispatching any Drone |
| `references/forge-brief-for-builders.md` | Maintaining or adding a Drone and Stinger pair to this audit |
| `references/grounding.md` | Checking where this orchestrator's rules come from |
| `scripts/make_scratch_copy.py` | Making the throwaway copy at intake (guide 00, step 6) |
| `scripts/check_workspace.py` | After every Drone returns, and before the brief |
| `scripts/merge_security.py` | After the security Drones in W1 return |
| `scripts/build_evidence_index.py` | After each wave, and before the brief |

## Related drones and stingers

- [code-foundation-stinger](../code-foundation-stinger) with `code-foundation-wasp-drone`: foundation health, using `get-started-stinger` in assess mode
- [code-bloat-stinger](../code-bloat-stinger) with `code-bloat-wasp-drone`: duplication, dead code, size, structure
- [react-security-stinger](../react-security-stinger), [nextjs-security-stinger](../nextjs-security-stinger), [sveltekit-security-stinger](../sveltekit-security-stinger), [polyglot-security-stinger](../polyglot-security-stinger), each with its Drone: framework-deep security
- [code-audit-brief-stinger](../code-audit-brief-stinger) with `code-audit-brief-wasp-drone`: the branded brief
- [remediation-planning-stinger](../remediation-planning-stinger) with `remediation-planning-wasp-drone`: the Mario tier's roadmap and Library documents
- Core: `security-stinger` (generic security pass), `quality-stinger` (standalone quality), `get-started-stinger`, `library-stinger`, `knowledge-stinger`

## Critical Directive

- You must read all files and context contained within your skill.
- In the event your core knowledge does not provide sufficient guidance you must make every attempt to search the internet, related knowledge base documentation files, and other available resources to supplement your knowledge prior to proceeding with your task.
- Additional related skills can be found here:
  - `pest-controller-suit` (Wasp Nest core) - Roster and routing for the Wasp Swarm. Load it before dispatching any Drone.
  - `security-stinger` (Wasp Nest core) - Generic security pass in Basic and above.
  - `quality-stinger` (Wasp Nest core) - Standalone quality pass in Full and Mario.

<!-- Ship Gate removed: research-only orchestrator. It audits and reports; Mario-tier writes are approved library documents, not code. -->
