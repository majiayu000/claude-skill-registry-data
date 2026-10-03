---
name: skill-system-governance
description: Audit and optimize a skill system with evidence. Use for skill architecture, token or context waste, role and prompt boundaries, routing hits or misfires, plugin packaging, registry/docs/source drift, duplicate workflows, or deciding whether a reusable change belongs in a skill. Runs deterministic checks first and applies only authorized, minimal fixes.
---

# Skill System Governance

## Overview

Treat the skill system as a maintained product: measure discoverability, routing, context cost, ownership, generated bundles, documentation, and validation before changing it. This skill is the standard workflow for the existing `技能维护` role; it does not create another role.

When invoked, start with the baseline audit. Do not ask the user to choose a checklist and do not assume that every review must produce a change.

## Default Workflow

### 1. Establish The Baseline

- Read repository instructions, `git status`, registry/package ownership, and the relevant role/skill contracts.
- Keep this phase read-only.
- Run the deterministic quick audit from the repository root:

```bash
python skills/skill-system-governance/scripts/audit_skill_system.py --repo . --mode quick
```

- Read `references/audit-dimensions.md` only for the dimensions relevant to the task.
- If the request depends on current OpenAI model, prompt, plugin, or Codex behavior, verify it against current official documentation. Do not browse by default for repository-local drift.

### 2. Add Runtime Evidence When Available

Static checks prove structure, not runtime selection quality. When the user supplies observed routing decisions or callback artifacts, run:

```bash
python skills/skill-system-governance/scripts/audit_skill_system.py \
  --repo . --mode quick \
  --observed path/to/observed-routing.jsonl \
  --callbacks path/to/callback-a.md \
  --callbacks path/to/callback-b.md
```

Without those artifacts, report routing accuracy and skill-hit rate as `not_evaluable`. Never convert self-reported callbacks into observed router accuracy or claim a percentage from chat memory.

### 3. Produce A Verdict Before Editing

Choose one primary verdict:

- `no-change`: evidence does not justify a change.
- `docs-only`: implementation is sound but discoverability or guidance drifted.
- `routing`: trigger descriptions, role ownership, eval cases, or package selection need correction.
- `contract-script`: repeated ambiguity needs a deterministic field, enum, guard, or validator.
- `package`: Core/domain boundaries or context budgets need adjustment.
- `consolidate-deprecate`: duplicate or obsolete workflows should merge, downgrade, or retire.

Order findings by severity and leverage. For each finding, include evidence, causal mechanism, smallest useful change, and a validation path. Separate measured facts from inference.

### 4. Apply Only Authorized Minimal Changes

If the user asked only for an audit, stop after the verdict and recommendations. If the user authorized optimization:

1. Edit canonical files under `skills/`, `registry/`, `docs/`, `evals/`, or `scripts/`.
2. Do not edit generated `plugins/*/skills/` copies directly.
3. Prefer one causal fix over adding repeated prose to several prompts.
4. Add or update deterministic tests before broad documentation changes.
5. Run `python scripts/sync_plugin_bundles.py --write` after canonical changes.
6. Run the full audit:

```bash
python skills/skill-system-governance/scripts/audit_skill_system.py --repo . --mode full
```

7. Follow repository commit and PR rules. Keep generated bundles in the same PR as their canonical source.

## Governance Boundaries

- Do not create a new skill from one anecdote. First decide whether the issue belongs in an existing skill, a role contract, a script, project-local instructions, or nowhere.
- Do not move domain capability into Core merely to make it easier to discover. Core contains cross-domain routing and governance only.
- Do not load the full skill catalog when registry metadata and a scoped reference are enough.
- Do not duplicate a workflow in role prompts. Role cards should route to the owning skill.
- Do not place project-local state such as `.codex/role-windows.md` into the shared repository.
- Do not treat longer prompts, more roles, or more checks as automatic improvements. Every added instruction needs a failure mode it prevents.
- Do not mutate user installations, plugin caches, or external upstream sources during a repository audit unless separately requested.
- Preserve provenance and public-safety rules. Never add machine paths, secrets, private logs, cookies, or project data.

## Default Output

```markdown
**Verdict**
no-change / docs-only / routing / contract-script / package / consolidate-deprecate

**Evidence**
- Deterministic checks:
- Runtime evidence:
- Not evaluable:

**Findings**
| Priority | Finding | Evidence | Smallest Change | Validation |
|---|---|---|---|---|

**Decision**
- Apply now / defer / no change
- Scope and non-goals

**Verification**
- Commands and results

**Residual Risk**
- Remaining uncertainty
```

Keep a clean audit concise. Expand only findings that change a decision.

## Resources

- `scripts/audit_skill_system.py`: deterministic read-only quick/full audit and optional runtime-evidence aggregation.
- `references/audit-dimensions.md`: scoped architecture, routing, Token, packaging, lifecycle, and documentation review criteria.
