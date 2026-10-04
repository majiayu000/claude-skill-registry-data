---
name: bump-skill
user-invocable: false
version: 2.3.6
metadata:
  internal: true
description: >
  Internal agentic-workflow maintenance: after SKILL.md edits, bump semver,
  lint authoring rules, and synchronize changelogs, READMEs, routing metadata,
  and migrations. Triggers: "bump the skill", "update the changelog",
  "version bump".
---

## Turn contract — verify before ending the turn

```
✓ Every changed skill's version: was bumped and BOTH changelogs got their rows
✓ The lint results (all 7 authoring rules, including the two machine-surface
  parity/ordering checks and the internal-skill discovery-exclusion check)
  were reported
✓ The git add + commit command block is printed as the ABSOLUTE last output
```

About to end the turn with any box unchecked? The turn is NOT done — complete
the missing box first.

## When to use

After any edit to one or more `skills/<name>/SKILL.md` files in this repo,
before committing. Handles the full documentation surface so nothing drifts.

## Step 0 — Orientation

This skill is **specific to the `agentic-workflow` repository**. Before doing
anything, confirm you are in that repo (presence of `skills/` + `CHANGELOG.md`
+ `CHANGELOG.md`). If not, stop and tell the user.

Versioning policy (from `CHANGELOG.md`):

| Bump | When |
|---|---|
| **major** | rename, removed/renamed flag, changed contract or output shape — ships with a migration note |
| **minor** | new backward-compatible capability: new flag, new section, new routing case |
| **patch** | wording, examples, clarifications, internal tidy — no behavior change |

## Process

### Progressive loading

The reference allowlist is exactly the two paths below. After orientation:

1. Read [change discovery and authoring lint](references/DISCOVERY_AND_LINT.md).
2. For every discovered skill, read [version and documentation sync](references/VERSION_AND_DOCS.md).
3. Then print the summary below.

Both resources are normative and one hop from this file. Missing resource → stop;
never guess a bump or skip a synchronization surface.

### 10. Print a summary and the next step

Print a table:

```
skill              old → new        bump
─────────────────────────────────────────
execute-phase      1.2.0 → 1.3.0   minor
unit-lane          1.0.0 → 1.0.1   patch
```

Then print the next step:

> All documentation updated. Stage and commit:
> ```
> git add skills/<name>/SKILL.md CHANGELOG.md README.md
> git commit -m "chore(skills): bump <name> to <version> — <one-line reason>"
> ```
> If this is a major bump with a migration note, also add `docs/workflow/MIGRATION.md`.

## Guardrails

- **Never change anything in a SKILL.md except the `version:` line.**
- **Never commit or push** — this skill only edits files.
- If a skill file is not tracked by git (new file not yet added), note it and
  still update the SKILL.md version and CHANGELOG entries, but warn that the
  diff-based bump analysis is unavailable for untracked files — ask the user
  what changed.
- For the README cells, prefer updating over rewriting: keep the existing tone
  and length; change only what is factually wrong or missing.

## Portability (agents other than Claude Code)

This skill is repo-maintenance for `agentic-workflow` itself, but the repo may
be worked on from any agent:

- **No slash-command menu** — follow this `SKILL.md` directly after editing any
  skill, before committing.
- **No per-skill `model:`/`effort:`** — a mid-tier model is enough; this is
  mechanical version/changelog bookkeeping.

## Relationship to other skills

- Run after any manual edit to a skill or after `execute-phase` touches a
  skill file, and before the commit.
- `AGENTS.md` section "Version every change" is the policy this skill
  enforces mechanically.
- Major bumps that introduce renames feed into `docs/workflow/MIGRATION.md`,
  which `init-workspace` reads when installing.

## Done when

- Every modified skill's `version:` field is updated.
- `CHANGELOG.md` has a new row for every bumped skill, newest first.
- The `README.md` skills and model tables are accurate.
- Major bumps have a migration note and cross-reference updates.
- Any authoring-rule violations (missing `→ Next:` block, `S1`/"Step" phase labels,
  a `user-invocable: true` skill absent from `plugin.json`, a non-alphabetical
  machine surface) are reported for the user to fix before committing.
- **The next step is printed** — the `git add` + `git commit` command, ready
  to run.
