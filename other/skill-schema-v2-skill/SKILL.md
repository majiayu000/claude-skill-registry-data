---
name: skill-schema-v2
description: "Load when creating, auditing, refactoring, or repairing an Agent Skill for reuse, governance, and runtime efficiency."
version: "2.0.0"
last_updated: "2026-06-02"
depends: []
metadata:
  author: "yinyo"
  category: "skill-engineering"
  sources:
    - "Contractual Skills, arXiv:2605.22634"
    - "What Keeps Agent Skills from Being Reusable?, Agent Skills 2026"
    - "SkillSmith, arXiv:2605.15215"
---

# Skill Schema v2

Use this skill to design, audit, or repair Agent Skills as reusable capability packages. v2 is based on three current findings:

- A skill is a **readable task contract**, not a prompt fragment.
- A skill must be **routable and reusable**, not just useful in its original chat or repo.
- A skill should expose a **minimal runtime boundary**, not inject every reference into context.

## Core Model

Every serious skill has three surfaces:

```text
Routing Surface
  name + description + frontmatter
  Decides whether the skill is loaded.

Contract Surface
  goal + inputs + permissions + evidence + output + verification + handoff
  Decides what correct behavior means.

Runtime Boundary Surface
  docs + examples + scripts + operators + fallback paths
  Decides what gets loaded or executed after selection.
```

These surfaces must not contradict each other. If the description routes one task, the contract must govern that task, and runtime resources must support that task.

## Hard Rules

1. **Description is routing metadata.** It must start with `Load when...` or an equivalent trigger phrase, describe when to load the skill, and stay short enough for startup routing.
2. **SKILL.md is not a knowledge warehouse.** Keep it as the routing and contract surface. Put detailed references, examples, templates, long rules, and papers in `docs/`, `examples/`, `templates/`, or `scripts/`.
3. **Use contract fields only when they reduce ambiguity.** Do not add enterprise fields as ceremony. Add goal, inputs, permissions, evidence, output, verification, or handoff only when they affect behavior.
4. **Runtime resources load progressively.** A skill should reveal a compact handle first, then load detailed docs or run scripts only when needed.
5. **Safety belongs in both language and enforcement.** The skill can state permissions, human gates, and evidence policy; tools, adapters, guardrails, tests, or humans must still enforce high-risk actions.
6. **No persona hijack unless persona is the product.** Avoid “you are...” identity rewrites, instruction overrides, hidden authority claims, and scope drift.
7. **No hidden local coupling.** Avoid hardcoded credentials, local-only paths, stale install instructions, repo-specific assumptions, or unportable scripts unless clearly marked.
8. **Every repair needs verification.** A repaired skill must be re-audited against routing, contract, runtime boundary, safety, portability, and self-consistency.

## Minimal Contract

For low-risk skills, use the compact contract:

```text
Goal: what the skill helps finish.
Load when: exact trigger conditions.
Inputs: required and optional user/context inputs.
Workflow: only the steps that change behavior.
Output: expected final artifact or response.
Verification: how to know the skill worked.
Boundaries: what the skill must not do.
Runtime resources: which docs/examples/scripts to load only when needed.
```

## Full Contract

Use the full contract for enterprise, tool-calling, high-risk, multi-agent, publication, finance, legal, privacy, deployment, or external-send skills:

```text
Goal
Audience
Inputs
Context sources
Workflow
Permissions
Human gates
Constraints
Evidence policy
Output contract
Quality bar
Verification
Handoff / pause rules
Runtime boundary
Fallback path
```

Do not use the full template for one-off, low-risk, no-tool skills. That creates body bloat.

## Audit Rubric

Score out of 100:

| Area | Points | Checks |
|---|---:|---|
| Routing | 15 | name, description, trigger clarity, no body-only routing |
| Contract | 20 | goal, inputs, output, verification, boundaries |
| Runtime Boundary | 15 | progressive docs/examples/scripts, minimal context, fallback |
| Reusability | 15 | portable paths, organized resources, no stale boilerplate |
| Safety | 15 | permissions, human gates, prohibited content, persona/scope |
| Signal Density | 10 | no model-known filler, no process theater |
| Versioning | 5 | SemVer, last_updated, changelog or release note |
| Self-Consistency | 5 | no conflicts across description/body/docs/scripts |

Critical failures cap the score at 60:

- missing or non-functional description
- hardcoded secrets
- destructive actions without approval boundary
- persona override unrelated to task
- SKILL.md so large that routing/contract content is buried
- output contract contradicts workflow or runtime resources

## Repair Protocol

Use risk-based repair:

```text
Low risk: frontmatter normalization, file moves, version sync, broken links
  -> repair directly, then report.

Medium risk: description rewrite, contract-field rewrite, runtime boundary rewrite
  -> show before/after and rationale.

High risk: deleting content, changing safety gates, changing permissions, changing external-send behavior
  -> list exact changes and require confirmation.
```

After repair, run a second audit and report:

```text
Before score:
After score:
Changed:
Remaining risks:
Verification evidence:
```

## Output Format

When auditing a skill, respond with:

```text
## Audit: <skill-name>

Score: <n>/100

Findings
- [FAIL/WARN/PASS] <area>: <concrete issue>

Required repairs
- <highest impact first>

Self-consistency check
- Routing vs contract:
- Contract vs runtime resources:
- Safety language vs enforcement:

Suggested next version
- version:
- changed files:
- verification:
```

## Runtime Docs

Load only what is needed:

- `docs/v2-design-spec.md` for full design rationale and paper synthesis.
- `docs/audit-rubric.md` for detailed scoring checks.
- `docs/repair-playbook.md` for repair patterns.
- `examples/v2-audit-report.md` for report shape.
