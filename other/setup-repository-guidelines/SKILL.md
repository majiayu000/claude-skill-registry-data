---
name: setup-repository-guidelines
description: v1.0.0 — Use only when the user requests repository initialization or explicitly invokes this skill by name or tag. Missing repository guidelines, a new directory, and ordinary coding or installer work do not authorize invocation. Detects membership from scripts/repository_manifest.sh and enforces owner routing, selectable installer integration, clean-install compatibility, safe deployment, and prompt-free keyring handling.
---

# Setup Repository Guidelines

This skill is **not** mandatory for every task. Invoke it only when:

- the user requests repository initialization (creating or initializing a
  repository), or
- the user explicitly invokes this skill by name or tag, such as
  `$setup-repository-guidelines` or `/setup-repository-guidelines`.

Missing `AGENTS.md` or other repository guidelines, a new or empty directory,
and ordinary coding, dependency, or installer tasks do not authorize invocation.
A request to inspect or edit this skill is not a request to initialize the target
repository or apply its setup workflow.
Check this user-intent gate before manifest discovery or any setup action. If
neither condition holds, continue the requested task without invoking this skill
or initiating repository setup. Manifest membership determines scope only after
the invocation gate passes; it is not an invocation trigger.

## Determine scope dynamically

1. Resolve the current Git root and repository basename.
2. Locate `installation_scripts/scripts/repository_manifest.sh` either in the
   current repository or in a sibling checkout under the same projects folder.
3. Source that manifest in a Bash subprocess and read `CLONE_REPOS`. The current
   repository is in scope when its basename is `installation_scripts` or occurs
   in that array.
4. Do not maintain a copied repository-name list in this skill. New repositories
   added to `CLONE_REPOS` are in scope when this skill is invoked under the
   user-intent gate above.
5. If the current repository is not in scope, stop applying this skill.

## Route before editing

- Read `installation_scripts/AGENTS.md`, `DEPENDENCIES.md`, and the current
  repository's own `AGENTS.md` before editing.
- Implement each concern in its owning repository. Update the orchestrator only
  for membership, ordering, aggregate selection, or setup-chain documentation.
- Inspect all affected sibling repositories; a feature may span several owners.

## Integrate every installed feature

- A user-visible feature is incomplete until its owning `install.sh` reproduces
  it on a clean machine.
- Component-aware repositories expose each independently selectable feature in
  `installer/components.sh`. New components are default-on unless the product
  requirement explicitly makes them optional.
- Keep listing side-effect free and support `--list-components`, `--select`,
  `--default`, and `--all` through the shared framework.
- Add focused tests for source behavior, installer idempotence, and clean-home
  installation before deployment.
- Run only the narrow owning installer or selected component; never run the
  master installer merely to deploy one child change.

## Prevent keyring prompts

When a task involves GNOME Keyring, Secret Service, automatic-login unlock
dialogs, or a keychain prompt while opening Claude Code:

- Ownership is `linux_configuration_setup`.
- Preserve Secret Service functionality and existing credential items.
- Ensure the default-on `passwordless_keyring` component is present and selected
  by the clean installation path.
- Migrate text and binary secrets without printing or logging secret values.
- Verify the resulting Login collection accepts the empty automatic-login
  password and remains the default collection.
- State the security tradeoff: removing prompts makes keyring contents no longer
  protected by an at-rest password.

## Deploy safely

The `linux-configuration` skill owns deployment for desktop settings, services,
extensions, hotkeys, and installers — including which reload is sanctioned and
which session actions are forbidden. Load it and follow it as written; this
skill deliberately does not restate its rules, so a copy here cannot drift out
of step with the owner. What belongs here is only the repository-setup side:
apply the narrowest owning installer and verify installed state against source.
