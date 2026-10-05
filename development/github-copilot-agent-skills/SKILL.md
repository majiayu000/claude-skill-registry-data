---
name: github-copilot-agent-skills
description: >-
  Use for creating, reviewing, debugging, or packaging portable GitHub Copilot Agent Skills with SKILL.md, precise triggers, progressive disclosure, scripts, examples, and resources. Do not use for always-on repository rules, a single prompt command, custom agent personas, or Skill Foundry maintenance.
argument-hint: "[repeatable capability, triggers, resources, and target hosts]"
---

# GitHub Copilot Agent Skills

Build a small, portable execution contract that Copilot can discover from its
metadata and execute without reconstructing expert judgment. Inspect the
installed version and active host schema before using optional fields.

## Workflow

1. Define one repeated job, inputs, artifacts, invariants, completion evidence,
   positive triggers, boundary cases, and near-miss negatives.
2. Choose project scope (`.github/skills`, `.agents/skills`, or compatible
   location) or explicitly requested personal scope (`~/.copilot/skills`).
3. Create a lowercase kebab-case directory and matching `SKILL.md` `name`.
   Front-load the `description` with the job and nearest non-goals.
4. Write decision rules, ordered workflow, canonical examples, and verification.
   Put optional stable detail in directly linked resources.
5. Add deterministic scripts only when they remove repeated error-prone logic;
   document input, output, failure, dependencies, and safety.
6. Test explicit slash use, implicit discovery, baseline improvement, negative
   interference, and resource access separately.

## Rules

- Required metadata is `name` and `description`. Current VS Code also supports
  `argument-hint`, `user-invocable`, `disable-model-invocation`, and experimental
  `context: fork`; verify portability before using optional fields.
- Keep every normal resource one hop from `SKILL.md` and reference it explicitly.
- Use manual-only invocation when automatic matching would be unsafe or noisy.
- Never put authoring research, evaluation fixtures, secrets, or mutable status
  in the distributed skill.
- Prefer Python 3.11+ standard-library helpers when executable logic is needed.

Read [the skill contract](references/artifact-contracts.md), use [skill patterns](references/patterns.md), and apply [verification](references/verification.md).

## Completion

The name matches its folder, metadata and links validate, runtime content is
minimal and self-contained, helpers are tested, discovery boundaries are
measured, and VS Code exposes the skill in the intended project or user scope.
