---
name: skill-lifecycle-manager
description: Manage agent-skill lifecycles across local, global, project, Skill Hub, skills.sh, GitHub, plugin-cache, and system roots. Use when searching, recommending, installing, updating, upgrading, syncing, merging, auditing, deduplicating, cleaning, packaging, publishing, or validating skills; choosing project versus global scope; verifying upstream source, stars, or installs; or working with skill-upgrade, check_upstreams.ps1, sync-pull/push, junctions, skills-lock.json, or skill-upstreams.json. Do not use for ordinary software-package upgrades or non-skill file cleanup.
---

# Skill Lifecycle Manager

Orchestrate skill work as one evidence-backed lifecycle. Keep source,
installation, and ownership separate so an update to one copy does not silently
overwrite another.

## Core Contract

Maintain three boundaries throughout the task:

- **Source**: where the skill came from, such as GitHub, skills.sh, a Skill Hub
  checkout, or a local repository.
- **Install**: where a runtime loads the active skill, such as a global user
  root or project root.
- **Ownership**: whether the path is user-maintained, project-maintained, or
  system/plugin-managed.

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
| Discovery, recommendation, install scope, quality audit, usage cleanup, package, publish, or report format | [references/governance-and-reporting.md](references/governance-and-reporting.md) |

Read more than one reference when the task crosses those boundaries. Do not
load unrelated operational detail for a simple task.

## Discover Stores And Ownership

Discover actual roots before editing. Common roots include:

- User/global roots: `~/.agents/skills`, `~/.codex/skills`, or configured
  `$CODEX_HOME/skills`.
- Project roots: project-local skill directories.
- Source checkouts: `_repos`, Skill Hub clones, submodules, or manual clones.
- Managed roots: `.system` skills and plugin caches.
- Evidence indexes: `_meta/skills-lock.json` and
  `_meta/skill-upstreams.json`.

Treat managed roots as read-only unless the user explicitly authorizes an
override. Treat source checkouts as source evidence, not automatically as the
active install target.

Keep an internal inventory:

| Skill | Source | Active install | Owner | Intended action |
| --- | --- | --- | --- | --- |

## Lifecycle Safety Sequence

Use this sequence for any operation that can change state:

1. Inventory source, install, ownership, branch/ref, and dirty state.
2. Verify source and scope with evidence appropriate to the operation.
3. Compare behavior and files before deciding replace versus merge.
4. Run a dry run when supported.
5. Resolve target paths and prove they are strictly below the intended root.
6. Create a timestamped backup before overwrite, mirror, move, or deletion.
7. Apply only the requested, ownership-compatible change.
8. Validate source and installed copies separately when both exist.
9. Report source, target, backup, changed files, validation, and unverified
   items.

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

1. Verify upstream source and immutable comparison ref.
2. Compare SKILL.md, references, scripts, assets, and evals.
3. Back up the target.
4. Mirror only when policy and evidence permit exact replacement.
5. Merge when local and upstream behavior both matter.
6. Validate and report the final source/install relationship.

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
Source:
Target and scope:
Ownership:
Dry run or comparison:
Backup:
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
