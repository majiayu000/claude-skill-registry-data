---
name: agent-skill-management
description: Manage agent-marketplace packages, reviewed APM caches and patches, plugin materialization, and Claude, Codex, Cursor, or pi activation in this dotfiles repo. Use for skill imports or edits, package policy, the console's guarded edits, apply hooks, and related architecture docs.
---

# Agent Skill Management

Use `agent-marketplace/` for the portable source/build project. It is sorted by
origin: `vendor/` holds the single `apm.yml`, lock, and committed `apm_modules/`;
`src/` defines separate plugins with their own selections, authored content,
patches, and native metadata; `marketplace.toml` lists them in catalog order. Host activation
policy lives in `home/.chezmoidata/agent_plugins.toml`. Official marketplace sources and client defaults live in
`home/.chezmoidata/agent_upstream_plugins.toml`; prefer those direct native
installs wherever the client supports the upstream catalog and enabled defaults.
Choose the upstream maintainer's repository or marketplace ahead of curated
mirrors and third-party aggregators. Use a whole
collection payload for an adapter when the complete skill set is wanted, and
retain individual selections only for intentional curation. Native clients own their
install records and caches; `~/.agents/plugins` is the shared materialized
artifact.

1. Choose the working surface. Read the
   [project workflow](../../../agent-marketplace/README.md) for authored skills,
   APM acquisition, selections, patches, versions, and export. Read
   [materialization](references/generated-outputs.md) for chezmoi or artifact
   copy changes, and [reconciliation](references/plugin-reconcile.md) for native
   installation, enablement, or rollback.
2. Change durable inputs. Edit authored `skills/` directly and imported content
   through patches or overlays. Keep the shared cache pristine. Bump only the
   affected plugin's `version` in `agent-marketplace/marketplace.toml`; the build
   generates its `plugin.json`, derives its APM publication manifest, and removes
   that manifest after generating native metadata. The console plans
   imported edits as patches, stages paired invocation controls and native
   version bumps, then builds the staged result before guarded writes. Imported
   description/frontmatter edits fingerprint the whole marketplace source before
   planning and recheck it before writing any file. If those inputs change,
   re-plan and revalidate; `--allow-dirty-targets` does not bypass that check.
   Deleting a root dependency requires checking every plugin's skill and
   supporting-payload selections, including disabled plugins.
3. Validate the changed boundary. Run `just -f agent-marketplace/justfile -d agent-marketplace check`
   for package changes; run `just test-python -p test_packages.py -p 'test_console_*.py'` for
   consumer or console changes. Activation changes also need the Claude, Codex,
   Cursor, and pi config merge checks. Native client changes need
   `just test-agent-skill-packages-native` on a host with both clients installed.
   The consumer suite applies scripts 35/36, config entries, and managed symlinks
   together in an isolated home, then repeats apply and verifies managed targets.
   Completion means the relevant checks pass and every payload change has a
   matching native version bump.
4. Materialize and reconcile within the user's requested apply scope. Read
   [the current reference](../../../docs/references/agent-marketplace.md) for
   paths and commands. Keep the previous artifact until native inventories and
   enabled states are verified. Source changes alone do not reload an existing
   agent session. `reconcile-upstream-agent-plugins --apply --update --agent ...`
   refreshes official installations; normal apply only installs missing ones.
   Install official replacements before reconciling away local wrappers. OMP
   requires removing a matching local install first; the reconciler restores
   that install and enabled state if replacement fails.

For input recovery, restore missing committed files from Git or a complete source
export. Acquisition refuses unaccepted cache/lock changes; it is not the repair
command for a deleted committed helper. Keep disposable probes in ignored scratch
and record useful evidence in research docs.

A human-only skill needs both `disable-model-invocation: true` and the Codex
sidecar's `policy.allow_implicit_invocation: false`. The build validates the pair.
Every published skill directory must retain its root `SKILL.md`, including after
patches and overlays. Python `__pycache__` entries are ignored without traversal
and never enter the artifact; other payload symlinks are rejected.
Keep all Codex interface metadata; hook-bearing packages retain `hooks: {}` under
the current skills-only Codex policy.

Runtime inventory comes from native catalogs and selected built payloads. Treat
`agent-marketplace/vendor/apm.lock.yaml` as the upstream identity/revision source. Preserve upstream license
and notice files in the published plugin as well as the cache. Subdirectory
imports need explicit root-notice payload selections when those texts are absent
from the selected tree; see the project workflow. Generate no `SOURCE.md` or
replacement per-skill provenance store.

For acquisition edge cases, read [third-party imports](references/third-party-imports.md).
For package shapes, read [package layout](references/package-layout.md).
The [test index](../../../tests/README.md#agent-package-checks) distinguishes the
ordinary checks from native host checks, console producer parity, and authenticated
evals. Those lanes establish different guarantees.
