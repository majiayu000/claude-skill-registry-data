---
name: skill-lifecycle-manager
description: Upgrade or synchronize Agent Skills, or determine a Skill's source and ownership across runtimes and roots. Use only for those lifecycle decisions. Do not use for installation, creation or editing, validation, inventory, usage statistics, general audits, cleanup, packaging, publishing, or ordinary file and package work.
---

# Skill Lifecycle Manager

Orchestrate skill work as one evidence-backed lifecycle. Keep source,
installation, and ownership separate so an update to one copy does not silently
overwrite another.

## Invocation Boundary

Use this skill only to upgrade Skills, synchronize Skill copies, determine a
Skill's source, or determine who owns and may update a Skill. For every other
Skill-related request, continue without this skill and use the narrower
applicable workflow.

## Core Contract

Maintain three boundaries throughout the task:

- **Source**: where the skill came from, such as GitHub, skills.sh, a Skill Hub
  checkout, or a local repository.
- **Install**: where a runtime loads the active skill, such as a global user
  root or project root.
- **Ownership**: whether the path is user-maintained, project-maintained, or
  system/plugin-managed.
- **Runtime**: which loader owns the active copy, such as Codex, Claude Code,
  an Agent Skills-compatible host, or more than one runtime.

Do not treat a Skill Hub checkout, `_repos` source, plugin cache, and global
install as interchangeable even when their skill names match.

When evidence is incomplete, report known facts, candidate hypotheses,
verification paths, and temporary mitigation. Do not present an unverified
hypothesis as a cause or completed fix.

## Start With Lifecycle Triage

Create a compact internal task card before acting:

- **Intent**: discover, recommend, install, update, sync, merge, audit, cleanup,
  package, publish, validate, or create/edit.
- **Target**: skill name, source URL, repository path, installed path, or topic.
- **Scope**: project, global/user, source repository, managed root, or unknown.
- **Runtime**: Codex, Claude Code, multiple runtimes, or unknown. Do not assume
  the runtime executing this skill is the runtime whose skills are being
  managed.
- **Destructive risk**: none, overwrite, move, delete, cleanup, or ownership
  change.
- **Evidence needed**: source, version, usage, quality, or scope proof.
- **Companion skill**: `find-skills`, `skill-installer`, `skill-creator`, or no
  companion.

Proceed without asking when target, scope, and ownership are clear. Ask a short
question only when a reasonable assumption could modify the wrong skill or
cross an ownership boundary.

## Route To The Relevant Reference

Read the complete relevant reference before performing that operation:

| Operation | Required reference |
| --- | --- |
| Skill Hub pull, push, new-skill sync, junction, or index rebuild | [references/skill-hub-operations.md](references/skill-hub-operations.md) |
| Upstream comparison, `skill-upgrade`, `check_upstreams.ps1`, mirror, or local fast-forward | [references/upstream-audit.md](references/upstream-audit.md) |
| Runtime roots, Claude Code skills/plugins, scope precedence, cache ownership, or reload behavior | [references/runtime-adapters.md](references/runtime-adapters.md) |
| Discovery, recommendation, install scope, quality audit, usage cleanup, package, publish, or report format | [references/governance-and-reporting.md](references/governance-and-reporting.md) |

Read more than one reference when the task crosses those boundaries. Do not
load unrelated operational detail for a simple task.

## Discover Stores And Ownership

Discover actual roots before editing. Common roots include:

- User/global roots: current Codex user skills belong in `~/.agents/skills`.
  `$CODEX_HOME/skills` (normally `~/.codex/skills`) is a deprecated
  compatibility location for older Codex installs; migrate user-owned skills
  from it instead of choosing it for new installs. Claude Code personal skills
  live under `${CLAUDE_CONFIG_DIR:-~/.claude}/skills`.
- Project roots: current Codex project skills use `.agents/skills` from the
  working directory through the repository root. Treat project `.codex/skills`
  as compatibility state. Claude Code uses `.claude/skills` and can also
  discover nested package roots in a monorepo.
- Source checkouts: `_repos`, Skill Hub clones, submodules, or manual clones.
- Managed roots: `.system` skills and plugin caches. Claude Code marketplace
  plugins are managed through `claude plugin`, not by editing
  `~/.claude/plugins/cache`.
- Evidence indexes: a repository `_meta/skill-upstreams.json` or a local
  source index such as `~/.skill-lifecycle/skill-upstreams.json`; legacy
  `~/.agents/skill-upstreams.json` remains supported. `skills-lock.json` is an
  inventory, not proof of upstream identity.

`CLAUDE_CONFIG_DIR` relocates Claude Code's configuration and personal skills;
it does not relocate the runtime-neutral source index. Keep the default index
under the operating-system user home unless `-IndexPath` is explicit. Likewise,
`~/.agents/skills` is a shared Agent Skills root even though current Codex loads
it at user scope. Record Codex ownership only when loader or configuration
evidence establishes it; the path alone does not prove exclusive ownership.

Treat managed roots as read-only unless the user explicitly authorizes an
override. Treat source checkouts as source evidence, not automatically as the
active install target.

Keep an internal inventory:

| Skill | Runtime/scope | Source | Active install | Owner | Intended action |
| --- | --- | --- | --- | --- | --- |

## Lifecycle Safety Sequence

Use this sequence for any operation that can change state:

1. Inventory source, install, ownership, branch/ref, and dirty state.
2. Verify source and scope with evidence appropriate to the operation.
3. Compare behavior and files before deciding replace versus merge.
4. Run a dry run when supported.
5. Resolve target paths and prove they are strictly below the intended root.
6. For a verified mirror, replace the target directly by default: clear only
   the strictly-contained target directory and copy the verified source. Create
   a backup only when the user explicitly requests one; the bundled helper
   exposes this as `-WithBackup`.
7. Apply only the requested, ownership-compatible change.
8. Validate source and installed copies separately when both exist.
9. Report source, target, backup status, changed files, validation, and
   unverified items.

A path equal to the allowed root is not a valid child target. A path that only
shares the root's text prefix is also not inside that root.

## Create Or Edit Skills

Use `skill-creator` for SKILL.md design, progressive disclosure, scripts,
references, and evals. This manager owns placement and lifecycle decisions:

- Put broadly reusable, trusted workflows in a global/user root and a shared
  Skill Hub path when repository publication is intended.
- Put project-specific conventions, private workflows, or experiments in a
  project root.
- Avoid same-name duplicates across active roots unless the user explicitly
  wants scope-specific variants.
- Validate the source copy before installing it, then compare source and
  installed hashes.
- For Claude Code, use personal or project `.claude/skills` for standalone
  skills and a plugin only when namespaced distribution, versioned updates, or
  bundled agents/hooks/MCP are actually needed.

## Discovery And Installation

Use `find-skills` or the ecosystem's discovery command instead of inventing a
new search process. Use `skill-installer` when the requested installation flow
matches it.

Before recommending or installing:

- Check active roots for existing or competing skills.
- Resolve the exact repository, path, branch/ref, and skill directory.
- Read the candidate SKILL.md and inspect scripts or dependencies.
- Record observed installs, stars, license, update activity, and source
  reputation; mark unavailable evidence as unavailable.
- Choose the smallest scope that supports the repeated workflow.

Read [references/governance-and-reporting.md](references/governance-and-reporting.md)
for detailed evidence thresholds, quality checks, and report formats.

## Upgrade And Merge

Never upgrade by name alone. Separate source updates from active-install
updates:

1. Resolve the exact installed path in a source index. If no verified mapping
   exists, run the source-discovery workflow and persist the result before
   deciding whether an upgrade exists.
2. Verify upstream repository, skill subdirectory, branch/ref, and immutable
   comparison commit. A GitHub URL mentioned as a dependency or example is
   only a candidate, not source proof.
3. Compare SKILL.md, references, scripts, assets, and evals.
4. Back up the target.
5. Mirror only when policy and evidence permit exact replacement.
6. Merge when local and upstream behavior both matter.
7. Validate and report the final source/install relationship.

Treat source mapping as reusable lifecycle state, not one-off research. Key
local mappings by canonical installed path so two same-name skills cannot
inherit each other's upstream. On each later audit, refresh the verified ref,
record the observed commit, and compare the complete skill directory. Read
[references/upstream-audit.md](references/upstream-audit.md) for the bootstrap,
verification, index, and repeat-audit workflow.

For Claude Code marketplace plugins, the plugin manager is the lifecycle
authority. Inventory with `claude plugin list --json`, compare the declared
marketplace/version/source, preserve the installed scope in
`claude plugin update <plugin> --scope <scope>`, and follow the CLI's restart
instruction; never mirror files into the versioned plugin cache. Read
[references/runtime-adapters.md](references/runtime-adapters.md) before acting.

Do not invent lifecycle metadata or policy. `source`, `repository`, `version`,
or similar frontmatter fields are useful only when actually present and remain
candidate evidence until verified. Do not assume semantic versions, automatic
polling, retry-count downgrades, a `stale` classification, or time-based
thresholds unless the source index or user policy defines them.

When both versions changed, summarize behavior-level differences before
merging:

- Triggering and description
- Tools and dependencies
- Safety and destructive operations
- Output contract
- Scripts, references, assets, and evals

Read [references/upstream-audit.md](references/upstream-audit.md) before using
the bundled audit helper or applying a mirror.

## Quality, Cleanup, And Publishing

For quality audits, check frontmatter, trigger specificity, progressive
disclosure, referenced resources, script safety, dependencies, secrets,
absolute-path leakage, and objective eval coverage.

For usage cleanup, do not use filesystem `LastAccessTime` as proof. Prefer
explicit invocation evidence, session/tool logs, loadability metadata, then
filesystem presence. Quarantine uncertain candidates instead of deleting them.

For publishing, complete and save the quality and secret/privacy audit before
creating or copying the package. Scan file contents as well as names, including
quoted JSON/YAML credential keys, environment assignments, tokens, private
keys, personal paths, and identifiers. Treat an unreadable file or an
unclassified finding as a failed gate; do not package first and repair the
audit afterward. Then keep only allowlisted runtime-relevant skill files,
remove generated outputs and private data, record provenance, update indexes,
and deliberately synchronize source and installed copies.

Read [references/governance-and-reporting.md](references/governance-and-reporting.md)
for the full gates, evidence labels, and output templates.

## Validation

Use the strongest relevant validation:

- Parse frontmatter and required fields.
- Run `skill-creator` validation.
- Run bundled script self-tests or safe dry runs.
- Parse JSON indexes and compare indexed counts with actual SKILL.md files.
- Run `git diff --check` and inspect the intended file list.
- For objective workflows, create or update `evals/evals.json` and forward-test
  representative cases against the prior version.

If tooling is unavailable, state that fact and perform a manual static check.
Do not convert missing validation into a pass.

## Common Report

Use a concise report proportional to the operation:

```text
Intent:
Runtime and scope:
Source:
Target and scope:
Ownership:
Dry run or comparison:
Backup (default: not created):
Changed files:
Validation:
Unverified:
Restart needed:
```

Use the operation-specific templates in
[references/governance-and-reporting.md](references/governance-and-reporting.md)
when more detail materially helps.

## Stop Conditions

Stop and request direction when:

- Source trust is insufficient for installation or overwrite.
- Local edits would be overwritten without a backup or merge rule.
- A target cannot be proven strictly below the intended root.
- The target is system/plugin-managed without explicit override authority.
- A material merge conflict changes behavior and intent does not resolve it.
- Credentials, admin approval, license acceptance, or interactive
  authentication are required.
- The requested conclusion is stronger than the evidence.

Report facts, hypotheses, validation paths, and temporary mitigation instead
of guessing past a stop condition.
