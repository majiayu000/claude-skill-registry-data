---
name: hoa-skill-curate
description: >-
  Trace installed skill provenance and upstream freshness using installer receipts and lock records.
  When an install warns, an imported source goes stale or last week's tasks suggest a skill to
  reuse, recommend library changes and execute only an owner-confirmed retirement, merge or
  deletion. Not for hoa-skill-set-audit.
metadata:
  revision: "7"
  areas: "software-development,self-management"
  targets: "runtime-agnostic"
  summary: "trace installer provenance, separate content drift from upstream activity, and execute only owner-confirmed library changes"
  summary_zh: "追溯安装来源，区分内容漂移与上游活动，仅执行所有者确认的技能库变更"
  kind: "entry"
---


# Curate installed skills

Provenance, content drift, upstream activity, and retirement are separate judgments.
Only execute a retirement, merge, or deletion after the owner currently approves the exact
action and targets. Archive flags, age, or low usage are evidence, not permission.

1. **Provenance.** Use installer records first: runtime hub lock, shared-store lock, then upstream
   links in the skill. Resolve and record the actual loaded location and inbound links. Mark
   unproven provenance as unknown. For a warning, locate the emitting code and scan path, then
   check the reported file and install receipt before explaining phase, impact, and evidence.
   See [installer triage](references/skills-cli-installs.md) for that installer's layout.
2. **Content drift.** Resolve the tracked upstream path and pin its comparison revision. Compare
   local content with that revision, normalizing line endings; if the question is current
   freshness, separately compare with the current upstream tip and record its revision.
   Include disabled installs unless scoped out. An old install timestamp or a recent monorepo
   push is not a content diff. For GitHub-backed shared-store SKILL.md screening, see
   [freshness details](references/source-triage-2026-11-21.md).
3. **Activity and retirement.** Record repo activity, archive state, and any independently
   verified maintainer activity separately. Apply only the operator's criteria; do not infer
   abandonment from repo push dates or low local use. Check actual dependencies and plausible
   upcoming use. Classify as keep, candidate, or needs confirmation, with reasons and gaps.
   Use [source triage](references/source-triage-2026-11-21.md) for retirement evidence.
4. **Execute only the approved list.** Back up affected directories and config; record rollback.
   For a merge, retain one reusable canonical workflow and update live callers. For a deletion,
   preserve history unless explicitly in scope. Reload only after successful edits and verify
   the actual loader set, disabled list, config validity, and live dependencies. Report the
   approved set, backup, readback, and rollback. Otherwise report that no changes were made.

For recommendations from recent work, read
[usage-based recommendations](references/usage-based-recommendations.md); never auto-install.
Set contribution and shadowing belong to the user-run hoa-skill-set-audit; judgment on one skill
belongs to hoa-skill-review; moving the canonical source belongs to hoa-skill-port.

| Variable | Resolves | Default |
|---|---|---|
| `SKILLS_HUB` | shared store and installer lock | `~/.agents` |
| `SKILLS_ROOT` | loaded skill directory | `<hub>/skills` |
| `SKILL_RUNTIME_CONFIG` | config carrying the disabled list | `${XDG_CONFIG_HOME:-~/.config}/agent/config.yaml` |

See [configuration](references/configuration.md) for the resolution order.
Only if a script command fails (for example `uv` is not found), read
[references/troubleshooting.md](references/troubleshooting.md).
