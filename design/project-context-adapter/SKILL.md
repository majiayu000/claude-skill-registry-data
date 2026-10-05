---
name: project-context-adapter
description: 'Refresh local project/** facts and frontend path indexes after project or tooling changes. Excludes Kit version upgrades and reusable skill authoring.'
id: 'agents.skills.project-context-adapter.skill'
title: 'Project Context Adapter'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-context-adapter'
tags:
    - 'agents/skill-package'
    - 'agents/project-context'
    - 'frontend/project-context'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[common/project-fact-provenance-rules|Project Fact Provenance]]'
    - '[[common/readme-policy|README Read And Edit Policy]]'
    - '[[skills/project-context-adapter/references/extraction-checklist|Extraction Checklist]]'
    - '[[skills/project-context-adapter/references/sync-procedure|Sync Procedure]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[templates/context-index|Context Index Template]]'
    - '[[project/architecture-map|Architecture Map]]'
    - '[[project/stack-profile|Stack Profile]]'
    - '[[project/styling-profile|Styling Profile]]'
    - '[[project/verification-profile|Verification Profile]]'
    - '[[project/design-reference-profile|Design Reference Profile]]'
    - '[[project/mcp-profile|MCP Profile]]'
    - '[[project/approved-patterns|Approved Patterns]]'
    - '[[project/anti-patterns|Project Anti-Patterns]]'
    - '[[project/react/path-index|React Path Index]]'
    - '[[project/next/path-index|Next Path Index]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Project Context Adapter

## Purpose

Refresh factual host-project context in `project/**` so reusable skills can
implement screenshot-derived specs without scanning the whole repository.

## When To Use

- Project structure, routes, entrypoints, styling systems, assets, or
  verification commands changed.
- A new frontend stack fact was discovered during implementation.
- Current skill capability declarations, available providers, or official
  documentation choices changed.
- Design-reference boundaries, approved patterns, or anti-patterns changed.
- Path indexes no longer match actual source files.

## When Not To Use

- Upgrading the installed Kit version: use `webdev-kit-updater`; refresh only
  facts its changed contracts invalidate.
- First-time full onboarding in Plan Mode. Use `project-onboarding-adapter`.
- Reusable skill authoring. Use `agent-rules-skill-author`.
- Screenshot spec writing or implementation unless project facts changed.

## Required Context

1. Read `AGENTS.md` when shipped, or the native plugin's generated runtime prelude. Resolve local overlays under host `.agents/project/`, not inside a shared plugin installation.
2. Confirm the classified task is `project-context-refresh` or a project
   context cache update required by another task.
3. Read `common/documentation-maintenance.md`.
4. Read existing `project/**` overlays.
5. Inspect relevant manifests, configs, entrypoints, routes, components,
   styles, assets, `tool-capabilities-manifest.json`, and verification scripts.
6. Read `references/extraction-checklist.md`.
7. Read `references/sync-procedure.md`.
8. Read `common/project-fact-provenance-rules.md`; preserve unrefreshed dates and mark unexecuted checks `not-run`.

Read targeted README sections only when the refresh concerns project intent, setup guidance, or documentation drift. Use `common/readme-policy.md` and confirm cached technical facts through higher evidence.

## Tool Contract

- Use Project Context MCP when available.
- Use filesystem reads and targeted search when Project Context MCP is
  unavailable.
- Use `context7` and MDN only when refreshing official documentation choices or
  stack-specific pattern notes that depend on current external docs.
- Activate `openai_platform_docs` only when refreshed project facts depend on current OpenAI or Codex behavior.
- Do not use Figma MCP.
- Edit only `project/**` unless the user also requests bundle skill or policy
  changes.

## Workflow

1. Determine which project facts changed.
2. Update only affected overlays or path indexes.
3. Refresh `project/mcp-profile.md` when skill capabilities, validated providers
   servers, official docs choices, or verification capabilities changed.
4. Refresh `project/design-reference-profile.md` when screenshot, exported
   asset, copied inspect, or design-source boundaries changed.
5. Refresh `project/approved-patterns.md` and `project/anti-patterns.md` only
   from real project code or official documentation for the detected stack.
6. Keep graph frontmatter current with `publishable: false` and
   `local_only: true`.
7. Keep host-project facts out of `AGENTS.md`, `README.md`, `common/**`,
   manifests, and reusable `skills/**`.
8. Verify updated facts against actual files or official documentation sources.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Report:

- overlays updated;
- source facts used;
- official documentation or MCP facts refreshed;
- project paths indexed or changed;
- verification performed;
- any project facts that remain unknown.

## Product Language Context

When product terms affect the task, read `common/domain-glossary-rules.md`.
Reuse a confirmed host glossary or maintain a populated local-only
`project/domain-glossary.md`; do not create one during read-only planning.
Record consequential reasons in the existing decision log and load only the
relevant domain. Glossary maintenance never renames code or edits host docs.

## Validation Gates

- `project/**` files must remain local-only.
- Path indexes must point to existing files or explicitly mark missing owners.
- `project/mcp-profile.md` must match active declarations in
  `tool-capabilities-manifest.json` when it is touched; provider config alone
  must not be recorded as availability.
- `project/design-reference-profile.md` must distinguish successful live reads
  from image evidence and unverified historical access; preserve source/state IDs.
- Patterns and anti-patterns must cite real local code facts or official
  documentation choices, not generic preferences.
- Reusable skills must not receive host-specific facts.
- README claims must not become project facts without confirmation from source, config, CI, package scripts, lockfiles, official documentation, or real results.
- Context refresh must not edit README unless the current user explicitly requests that README change.
- Context refresh records design evidence; live acquisition belongs to
  `design-screenshot-spec`, and canvas/whiteboard writes remain outside refresh.

## Trigger Evals

Should trigger:

- "Refresh project context after this layout change."
- "Update .agents/project path indexes."
- "The styling profile is stale; sync it with the repo."

Should not trigger:

- "Create a design implementation spec from screenshots."
- "Implement this screen."
- "Plan first-time onboarding for a new project."

## Reference Map

- `references/extraction-checklist.md`
- `references/sync-procedure.md`
- `common/readme-policy.md`

## Model Routing Drift

When relevant client version, authentication mode, configuration, role paths or
model availability changes, mark affected local model-routing evidence stale.
Preserve `project/model-routing-profile.md`, request/state files and backups;
do not refresh their model bindings automatically. Approved reconfiguration
belongs to `project-onboarding-adapter` and its GPT bootstrap reference.
