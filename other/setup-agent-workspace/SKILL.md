---
name: setup-agent-workspace
description:
  Set up or update portable Codex and Claude agent coordination in a Git project, with project-specific agents,
  execution policies, Backlog, versioned tooling, and standalone preview/apply commands. Use for installation, safe
  upgrades, drift checks, or moving operating skills to a plugin; not ordinary task execution.
---

# Set up an agent workspace

This skill bundles a complete starter. It does not depend on the repository where the skill was created, create source
scaffolding, launch agents, or authorize unattended implementation.

1. Inspect the target's root instructions, Git boundaries, Backlog configuration, and existing agent setup. Ask only for
   consequential missing choices: project agent names/roles, repository boundaries/read-only references, project checks,
   and desired execution defaults. Assisted is the safe default; unattended runs still require actual user authorization
   and bounded task scope.
2. Read [configuration and manual setup](references/configuration.md). Generate the closest full configuration with
   `node <skill>/scripts/init.mjs --example LAYOUT`; customize it in scratch outside the target. Layouts are
   `single-repo`, `monorepo`, `multi-repo`, and `submodules`. Existing initialized submodules are supported; setup does
   not clone, initialize, upgrade, or commit them.
3. Run `node <skill>/scripts/init.mjs --target /absolute/project --config /path/config.json --dry-run`. Inspect its
   complete planned file list and additive instruction/ignore blocks. Existing content conflicts fail without target
   writes. Fix the input or deliberately integrate existing instructions; never bypass conflicts with blanket
   overwrites.
4. When setup is already authorized, apply the same inputs using `--apply`, then run the generated schema check,
   `status`, and `backlog doctor`. Do not ask again for routine decisions within the accepted setup. If an unresolved
   material choice remains, show the concrete preview before asking.
5. Confirm tracked tooling is visible to Git and durable runtime is ignored. Report changed files,
   prerequisites/validation, any limitations, and a Conventional Commit suggestion. Leave Git staging, commits,
   branches, hooks, and remotes alone unless independently authorized.

Use the standalone script directly when no agent is desired; `--help` documents every option. Preview and apply use the
same planner. They never install project dependencies. npm/npx may populate its external cache for the pinned schema
validator; `--offline` requires a complete cache.

The template is the authoritative source of reusable schema/scripts/tests. Projects receive versioned tracked copies;
improve the template, regenerate release metadata with `scripts/bundle.mjs --write`, then update consumers. Canonical
operating skills live beside this skill. The same command refreshes their portable bundled copies; `--check` fails on
drift. Keep the whole setup skill directory for standalone distribution. Never bundle live runtime, tasks, or
source-project configuration.

## Update an installed project

Read [update and adoption guidance](references/updates.md). Inspect `install-manifest.json`, persist the maintenance
handoff, and close affected sessions before `scripts/update.mjs --target PATH --check` or `--dry-run`. Check reports
exit 2 for a safe pending update, 1 for a conflict/failed prerequisite, and 0 for an exact current installation. When
authorized, apply the same preview. Active claims/runs prevent every updater mode, including the agent performing an
update: close its session first, update as a maintenance operation, then register a new session for verification if work
remains. The installed `check-installation.mjs` remains available for read-only local drift checks during ordinary work.

Use `--skills local` (standalone default) or `--skills external` when operating skills are installed through a
plugin/user directory on every required host. Verify external skill discovery before removing local copies. Updating a
plugin does not automatically update project tooling. Missing/unsupported compatibility or modified files require
deliberate integration; never bypass them by deleting the manifest or using an invented force option.

For a pre-manifest project, use `--adopt --baseline-template /path/to/verified/legacy/assets/template`. Preview verifies
existing managed bytes against that baseline before upgrading them; only the previously absent generic guide may be
added. Preserve the baseline until successful verification. Run focused installer/updater tests and an isolated real
lifecycle after changes to the bundle or synchronization behavior.
