---
name: project-onboarding-adapter
description: 'Onboard frontend projects with local context, client and verification facts. Codex onboarding includes economical subagent setup and activation checks. Excludes model changes during updates, facts-only requests and Plan Mode; no app code or instruction replacement.'
id: 'agents.skills.project-onboarding-adapter.skill'
title: 'Project Onboarding Adapter'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'project-onboarding-adapter'
tags:
    - 'agents/skill-package'
    - 'agents/onboarding'
    - 'frontend/project-context'
parent: []
related:
    - '[[templates/project/model-routing-profile]]'
    - '[[skills/project-onboarding-adapter/references/codex-model-bootstrap]]'
    - '[[skills/project-onboarding-adapter/references/model-workload-matrix]]'
    - '[[common/host-instruction-migration-rules|Host Instruction Migration]]'
    - '[[common/project-fact-provenance-rules|Project Fact Provenance]]'
    - '[[templates/project/verification-profile|Verification Profile Template]]'
    - '[[common/core/runtime-core-policy|Portable Runtime Core Policy]]'
    - '[[common/readme-policy|README Read And Edit Policy]]'
    - '[[profiles/react-typescript/PROFILE|React TypeScript Profile]]'
    - '[[skills/project-onboarding-adapter/references/adaptation-checklist|Adaptation Checklist]]'
    - '[[skills/project-onboarding-adapter/references/path-audit-checklist|Path Audit Checklist]]'
    - '[[common/client-adaptation-policy|Client Adaptation Policy]]'
    - '[[common/tool-capability-model|Tool Capability Model]]'
    - '[[common/mcp-installation-policy|MCP Installation Policy]]'
    - '[[common/target-stack-policy|Target Stack Policy]]'
    - '[[common/skill-applicability-policy|Skill Applicability Policy]]'
    - '[[common/context-compaction-rules|Context Compaction Rules]]'
    - '[[templates/project/client-profile|Client Profile Template]]'
    - '[[templates/project/mcp-profile|MCP Profile Template]]'
    - '[[skills/project-context-adapter/SKILL|Project Context Adapter]]'
    - '[[skills/mcp-toolchain-manager/SKILL|MCP Toolchain Manager]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Project Onboarding Adapter

## Purpose

Adapt this `.agents` bundle to a host frontend project without creating application source files. For React or Next.js, cache normal target-stack facts. For a non-target frontend project, cache only the detected stack boundary and the framework-agnostic skills that remain usable.

Onboarding must also adapt natively to the installed client target. It creates or refreshes the smallest appropriate host pointer, records client facts in local-only `project/client-profile.md`, and records tool capabilities in local-only `project/mcp-profile.md`.

## Natural Language Trigger Aliases

Route adaptation, initialization, and project-context bootstrap commands here, including `адаптируйся`, `инициализируй .agents`, and `Adapt this .agents bundle to my project.` Full Codex onboarding includes model setup; explicit GPT requests also trigger that phase. A facts-only request does not.

## When To Use

- The user explicitly requests economical GPT subagent setup or reconfiguration in a supported Codex project.
- The user asks to adapt this bundle to a new React or Next.js project.
- The user asks to adapt this bundle to a non-target frontend project while keeping applicable design, QA, review, lint, planning, MCP, context, and skill-authoring workflows.
- The user asks to create or refresh the host-root pointer, native client pointer, local project overlays, MCP profile, client profile, design-reference profile, verification facts, loop memory, or path indexes.

## When Not To Use

- An existing Kit needs a version update: use `webdev-kit-updater`, preserving
  existing project overlays instead of repeating onboarding.
- Ordinary screenshot-to-code implementation.
- Narrow project overlay refresh after implementation.
- Reusable skill authoring.
- Application scaffolding, package installation, or source file creation.
- Stack-specific React/Next architecture or implementation guidance for a non-target frontend project unless the user explicitly changes the supported stack.

## Required Context

1. Read the host-root native instruction pointer if present and needed for adaptation: `AGENTS.md`, `CLAUDE.md`, or client rules. Inspect the minimal pointer section for detection; read the entire file for requested migration using `common/host-instruction-migration-rules.md`.
2. Read bundle-local `AGENTS.md` when shipped and `common/core/runtime-core-policy.md`. Native plugins use their generated skill prelude; do not require an absent shared-policy entrypoint.
3. Read `common/client-adaptation-policy.md` and only the adapter for the resolved canonical target.
4. Read `profiles/react-typescript/PROFILE.md` and its owning policies only when repository evidence confirms the profile.
5. Read `common/skill-applicability-policy.md` when the detected or suspected stack is outside the target stack.
6. Read `common/tool-capability-model.md` and `tool-capabilities-manifest.json` for capability selection.
7. Read `common/context-compaction-rules.md` when loop memory or resumable workflow setup is requested.
8. Read existing `project/**` overlays when present.
9. Inspect only relevant manifests, configs, source entrypoints, routes, styles, assets, and verification scripts.
10. Read `templates/project/client-profile.md` and `templates/project/mcp-profile.md` before creating those local-only profiles.
11. Read `common/project-fact-provenance-rules.md` and `templates/project/verification-profile.md` before caching verification or capability facts.

Read targeted README sections only when they help identify project intent, setup guidance, or documentation drift. Apply `common/readme-policy.md`, and confirm every cached technical fact through manifests, config, source, CI, package scripts, lockfiles, or real results.

## Tool Contract

- Use the `project_files` capability when available. Prefer configured filesystem/project-files MCP for direct project file reads; use host-native file tools when available; use targeted shell reads only as the fallback.
- Use MDN for HTML, CSS, Web APIs, accessibility, and browser behavior when official web platform facts matter.
- Use `context7` only for detected target-stack libraries or tooling when current docs matter.
- Activate `openai_platform_docs` only when current Codex client, plugin, skill, MCP, or configuration behavior affects onboarding.
- Determine Browser or Playwright availability from the current session tool registry or validated `project/mcp-profile.md` facts. Do not invoke either tool during onboarding or MCP detection.
- Do not infer MCP availability from `package.json`, lockfiles, `node_modules`, a running local app, or Playwright dependencies.
- Do not use Figma MCP.
- Missing MCP installation requires explicit user approval after reporting the official source.

## Workflow

1. Classify whether this is Plan Mode or approved execution.
2. Detect the installed target or current client surface. In source, resolve aliases through `bundle-manifest.json`; in a generated target, use its sole shipped adapter.
3. Read that one client adapter and apply its native discovery, pointer, tool, sandbox, and configuration rules. For a generic or unknown client, create no pointer unless the user explicitly requests one.
4. If an expected pointer already exists, preserve it unless replacement is explicitly authorized. For requested migration, preserve all host rules in reachable local overlays, retain a backup and coverage map, and validate before writing the minimal pointer. Otherwise propose a merge for nonempty or ambiguous instructions.
5. Detect whether the host project is existing, new/empty, or partially initialized.
6. Detect target-stack fit from manifests, configs, lockfiles, source roots, routes, styles, and entrypoints.
7. If the project fits the target stack, plan or write normal `project/**` overlays for stack, architecture, styling, state, data, verification, design references, MCP profile, client profile, and path indexes.
8. If the user asks for resumable iterative work or loop memory, plan or write local-only `project/loop-memory.md` using `templates/loop-memory.md` as the source pattern.
9. If the project is outside the target stack, continue with limited onboarding: record the stack boundary, skip React/Next path indexes and stack-specific patterns, and write `project/skill-applicability-profile.md` with applicable framework-agnostic skills from `common/skill-applicability-policy.md`.
10. Read `tool-capabilities-manifest.json` for declared capability needs and cache required, available, missing, optional, approved, installed, skipped, or blocked capabilities in `project/mcp-profile.md`.
11. Cache detected client target, native pointer, skill support, and MCP config locations in `project/client-profile.md`.
12. In Plan Mode, return the plan and stop.
13. In execution mode, update the approved pointer and local overlays; complete the Codex model phase below. Native plugins write host facts to host `.agents/project/`, never the installed plugin. Do not create dangling pointers or app code.

## Codex Model Setup During Onboarding

A full onboarding request authorizes missing project-local GPT role setup,
narrow native enablement and tiny read-only activation checks without a second
confirmation. Read `references/codex-model-bootstrap.md`, inspect current facts,
show the scoped change summary, then execute within that request. Preserve
existing working bindings; do not reselect models or rewrite caches on each run.
Explicit facts-only, no-model-change, preview/Plan Mode requests, kit updates
and non-Codex clients never write model settings or run canaries.

Confirm actual catalog, supported format and dispatch interface. Missing spawn
before configuration does not block preparation; runtime verification needs a
callable supported interface. Resolve genuine conflicts, missing evidence or
authority before writes; never change trust, global/primary models, MCP or
security controls. Record separate configuration, dispatch-mode and runtime
evidence in `templates/project/model-routing-profile.md`. Missing runtime
evidence leaves the affected route inactive, without an expensive fallback.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

```text
Installed package target or detected client
Native pointer action
Project type and stack facts
Target-stack fit
Applicable framework-agnostic skills when outside target stack
Docs and MCP capability choices
Client profile action
MCP profile action
Overlays to create or update
Loop memory setup
Verification commands
Validation run or blocked
Unknowns
```

## Product Language Context

When product terms affect the task, read `common/domain-glossary-rules.md`.
Reuse a confirmed host glossary or maintain a populated local-only
`project/domain-glossary.md`; do not create one during read-only planning.
Record consequential reasons in the existing decision log and load only the
relevant domain. Glossary maintenance never renames code or edits host docs.

## Validation Gates

- `project/**` overlays remain local-only.
- `project/client-profile.md` and `project/mcp-profile.md` are created from templates and marked local-only in copied overlays.
- Native pointers remain small. Claude uses the exact `@.agents/AGENTS.md` import when shared project policy is approved; other pointers reference `.agents/AGENTS.md` instead of mirroring the full policy.
- Existing host instructions are not overwritten without approval.
- README may supply targeted context but never the sole technical fact; README and host docs are not edited during onboarding unless the current user explicitly requests that documentation change.
- Loop memory stores tried, verified, and open facts only in local-only project files.
- Non-target frontend overlays do not claim React/Next implementation support.
- Non-target frontend projects list applicable framework-agnostic skills instead of reporting the whole bundle unusable.
- Capability detection uses `tool-capabilities-manifest.json` and does not depend on Codex-only `agents/openai.yaml` files.
- Full Codex onboarding includes narrow model setup; explicit exclusions and higher-level restrictions win. Written TOML is not runtime verification.
- No application source files are created during onboarding.
- No package, MCP, UI library, styling system, or framework change is made without explicit approval.
- Changed Markdown keeps graph frontmatter and English reusable rules.

## Trigger Evals

Should trigger:

- "Configure economical GPT subagents for this Codex project."
- "адаптируйся"
- "Adapt this .agents bundle to my project."
- "Plan onboarding for this frontend repo."
- "Adapt this bundle to an Astro project but keep only the skills that still apply."
- "Set up local loop memory for this project."
- "Detect whether this install is Codex, Claude, Cursor, or VS Code and create the right pointer."

Should not trigger:

- "Implement this visual spec."
- "Refresh project overlays after this component change."
- "Create a new skill package."
- "Scaffold a new React app."

## Reference Map

- `references/model-workload-matrix.md`: select capability tiers and reasoning
  efforts, including architecture and light/deep variants, during model setup.

- `common/client-adaptation-policy.md`
- `common/codex-official-docs-policy.md`
- `common/tool-capability-model.md`
- `common/mcp-installation-policy.md`
- `common/target-stack-policy.md`
- `common/skill-applicability-policy.md`
- `common/context-compaction-rules.md`
- `common/readme-policy.md`
- `tool-capabilities-manifest.json`
- `templates/project/client-profile.md`
- `templates/project/mcp-profile.md`
- `templates/loop-memory.md`
- `skills/project-context-adapter/SKILL.md`
- `skills/mcp-toolchain-manager/SKILL.md`
