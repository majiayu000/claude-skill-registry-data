---
name: agent-rules-skill-author
description: 'Maintain WebDev Agent Kit source rules, skills, metadata, and validators. Excludes upgrading installed copies.'
id: 'agents.skills.agent-rules-skill-author.skill'
title: 'Agent Rules And Skill Author'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'agent-rules-skill-author'
tags:
    - 'agents/skill-package'
    - 'agents/authoring'
    - 'agents/skill'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/readme-policy|README Read And Edit Policy]]'
    - '[[common/rule-audit-findings|Rule Audit Findings]]'
    - '[[skills/agent-rules-skill-author/references/documentation-maintenance|Documentation Maintenance Workflow]]'
    - '[[skills/agent-rules-skill-author/references/codex-native-skill-contract|Codex Native Skill Contract]]'
    - '[[skills/agent-rules-skill-author/references/figma-derived-conventions|Figma Derived Conventions]]'
    - '[[skills/agent-rules-skill-author/references/rule-audit-checklist|Rule Audit Checklist]]'
    - '[[skills/agent-rules-skill-author/references/rules-writing|Rules Writing]]'
    - '[[skills/agent-rules-skill-author/references/skill-design|Skill Design]]'
    - '[[skills/agent-rules-skill-author/references/skill-quality-rubric|Skill Quality Rubric]]'
    - '[[skills/agent-rules-skill-author/references/source-backed-prompting|Source-Backed Prompting]]'
    - '[[skills/agent-rules-skill-author/references/trigger-and-metadata|Trigger And Metadata]]'
    - '[[skills/agent-rules-skill-author/references/validation-checklist|Validation Checklist]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Agent Rules And Skill Author

## Purpose

Create or revise repo-local agent rules and `.agents`-compatible skill packages without leaking project-specific instructions into the wrong layer.

## When To Use

- The user asks to create, evaluate, rename, delete, or edit skills.
- The user asks to change `AGENTS.md`, manifests, validators, `common/**`, `project/**`, or `skills/**`.
- The user explicitly asks for user-facing README documentation changes.
- The screenshot-to-frontend pipeline rules, tool contracts, or skill routing need maintenance.

## When Not To Use

- Updating an installed Kit from upstream releases: use `webdev-kit-updater`.
- The user asks to write a design implementation spec from screenshots. Use `design-screenshot-spec`.
- The user asks to implement a frontend layout from a spec. Use `frontend-layout-implementer`.
- The user asks to visually verify rendered UI. Use `frontend-visual-qa`.
- The user asks to adapt a new project in Plan Mode. Use `project-onboarding-adapter`.

## Required Context

1. Read `AGENTS.md`.
2. Confirm the classified task is `skill-documentation-refactor`, `documentation`, or another `.agents` rule-maintenance task.
3. Read `common/documentation-maintenance.md`.
4. Read affected `common/**`, `skills/**`, `project/**`, manifests, validators, templates, examples, and root pointer files for the requested change.
5. Apply `common/readme-policy.md`: read targeted README sections when the request concerns README, public setup guidance, or docs/implementation drift; verify technical claims through higher evidence.
6. Read relevant references from this skill only when their topic is in scope.
7. Read current OpenAI Codex docs when native skill behavior, `AGENTS.md`, MCP, plugins, or `agents/openai.yaml` behavior may have changed.

## Tool Contract

- Use filesystem reads and targeted search for local bundle facts.
- Activate `openai_platform_docs` when current OpenAI or Codex behavior affects the change; follow `common/codex-official-docs-policy.md`.
- Use `context7` and `mdn` only when authoring rules depend on current framework or web platform behavior.
- Rule maintenance needs source/docs reads, not live Figma access. Encode live
  design intake through `design-screenshot-spec` and the capability manifest.

## Workflow

1. Classify the target layer: `AGENTS.md`, manifests, validators, `common/**`, `project/**`, `templates/**`, `examples/**`, or `skills/**`.
2. Treat README as optional human-facing context, never runtime policy or validator truth. Do not edit it unless the current user explicitly requests that README change.
3. Confirm whether a new skill is needed or an existing skill/reference/common rule should be edited.
4. Define trigger surface, non-trigger cases, inputs, outputs, defaults, tool contract, failure modes, and validation gates.
5. Keep skill packages in the standard section order used by this bundle.
6. Keep graph frontmatter and Codex UI/invocation metadata synchronized; keep
   capability declarations in `tool-capabilities-manifest.json`.
7. Remove stale links after renames or deletions.
8. Validate changed skill packages and run documentation checks.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Report:

- files changed;
- skill routing or trigger changes;
- tool dependency changes;
- validation performed;
- unresolved risks or blocked checks.

## Validation Gates

- `name` and `description` stay first in `SKILL.md` frontmatter.
- Every skill has `Purpose`, `When To Use`, `When Not To Use`, `Required Context`, `Tool Contract`, `Workflow`, `Output Contract`, `Validation Gates`, `Trigger Evals`, and `Reference Map`.
- New references are linked from the owning `SKILL.md`.
- `agents/openai.yaml` matches skill UI and invocation policy. Only true hard
  client-tool dependencies belong there; optional providers belong in the
  capability manifest.
- Live design intake remains read-only, MCP-first with browser fallback, and
  does not introduce whiteboard/canvas writes or hard provider dependencies.
- README is not used as runtime policy, routing input, validator truth, or sole technical evidence, and is not edited without an explicit current user request.

## Trigger Evals

Should trigger:

- "Create a new skill for visual QA."
- "Audit and rewrite the .agents skill routing."
- "Update AGENTS.md, manifests, and graph links for renamed skills."

Should not trigger:

- "Implement this Design Implementation Spec."
- "Compare the rendered page to the screenshot."
- "Write a layout spec from these screenshots."

## Authoring Mode

Default to the source-bundle contract: native `name` and `description` plus local graph metadata. Use strict native-portable frontmatter only when the user explicitly requests a standalone skill outside this bundle.

Before material skill changes:

1. Use `references/skill-design.md` to choose the smallest correct intervention and package shape.
2. Use `references/trigger-and-metadata.md` to align the description, invocation policy, and `agents/openai.yaml`.
3. Use `references/skill-quality-rubric.md` for trigger and workflow evals.
4. Use `references/rules-writing.md` when policy scope or precedence changes.
5. Use `references/documentation-maintenance.md` for graph, manifest, rename, or publication changes.
6. Use `references/validation-checklist.md` before final reporting.

For new skills, use the local scaffolder only after the workflow, resources, compatibility target, and trigger boundary are defined. Keep examples and scripts only when they implement repeatable behavior.

## Reference Map

- `references/codex-native-skill-contract.md`
- `references/rules-writing.md`
- `references/skill-design.md`
- `references/skill-quality-rubric.md`
- `references/trigger-and-metadata.md`
- `references/validation-checklist.md`
- `common/readme-policy.md`
- `common/codex-official-docs-policy.md`
- `references/figma-derived-conventions.md`
- `references/source-backed-prompting.md`
- `references/documentation-maintenance.md`

## Behavioral Evidence Boundary

When editing the kit source repository, use its existing live scenario inventory
and `run_behavior_evals.py` runner for changes that affect agent decisions.
Installed host bundles need a separately authorized evaluation environment;
never assume the source-only runner is shipped in the skill package. Preserve baseline/candidate traces under
comparable client/model/effort settings and assess actual actions and file
changes, not just the final answer. Static marker/schema checks and synthetic
runner tests are not live model passes. For authorized executable tests follow
`common/test-policy.md`: a missing import is structural failure, not proof of a
behavior assertion. Record unrun live scenarios as unverified.
