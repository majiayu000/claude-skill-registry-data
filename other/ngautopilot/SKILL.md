---
name: ngautopilot
description: Use when an AI coding agent needs NgAutoPilot routing, version-aware Angular guidance, frontend quality gates, skill catalog maintenance, plugin bundle validation, or safe agent adapter installation.
---

# NgAutoPilot

## Purpose

Use this root skill as the public entry point for NgAutoPilot. It explains how to approach a repository with the NgAutoPilot catalog, packs, adapters, plugin bundles, and validation gates.

NgAutoPilot is an agent-agnostic engineering toolkit for bounded Angular, TypeScript, JavaScript, frontend, and quality work. It is not an autopatcher, framework, runtime dependency, or replacement for tests and review.

## When to Use

Use this skill when:

- You are installing or using NgAutoPilot in an agent workspace.
- You need to choose an NgAutoPilot pack, adapter, or plugin bundle.
- You are maintaining the skill catalog, marketplace manifests, adapters, or bundle sync.
- You are doing Angular, frontend, TypeScript, JavaScript, RxJS, testing, quality, or upgrade work and need version-aware routing.
- You need a safe default workflow before selecting a more specific NgAutoPilot skill.

## Inputs Expected

- User goal and affected area
- Repository stack and framework versions
- Package manager and available scripts
- Installed agent adapter or target agent
- Requested pack or plugin, if any
- Current validation requirements

## Operating Model

Follow this loop:

```txt
Inspect repository -> detect stack and versions -> select smallest relevant skill -> assess compatibility and risk -> make the smallest reversible change -> validate with repository scripts -> report evidence and residual risk
```

Prefer focused packs over loading the full catalog. Every focused pack includes `ngautopilot-core` automatically.

## Core Routing

Start with these concepts:

| Need | Use |
| --- | --- |
| General workflow | `core.autopilot-orchestrator` |
| Project shape and stack | `core.project-intake`, `core.stack-version-detection` |
| Skill selection | `core.skill-router` |
| Version safety | `core.compatibility-router` |
| Change risk | `core.risk-assessment` |
| Angular upgrades | `angular.upgrades.angular-upgrade-orchestrator` |
| Angular 21 to 22 | `angular.versioning.angular-21-to-22-index` |
| Quality work | `quality.fundamentals.quality-decision-matrix` |

## Installation Entry Points

Use the CLI for bounded installation:

```bash
npm exec --package=ngautopilot -- ngautopilot adapters
npm exec --package=ngautopilot -- ngautopilot packs
npm exec --package=ngautopilot -- ngautopilot install --agent opencode --pack ngautopilot-angular-foundations --dry-run
```

Use marketplace/plugin discovery for browsing. Do not treat marketplace bundles as pack selection.

## Maintenance Rules

- Preserve separation between source skills in `skills/` and distributable bundles in `plugins/`.
- Update source skills first, then sync plugin bundles.
- Do not invent Angular compatibility data, APIs, CLI commands, or validation results.
- Keep Angular upgrade hops separate from modernization work.
- Prefer the smallest reversible change.
- Do not add dependencies unless required by the task.

## Validation

Use repository scripts that match the changed area:

```bash
npm run skills:validate
npm run skills:catalog
npm run security:scan
npm run release:validate
```

For Skill Lab changes, also run:

```bash
npm run skill-lab:validate
npm run skill-lab:test
npm run skill-lab:ci
```

## Do

- Inspect before editing.
- Route through the smallest useful skill.
- Validate source and plugin bundles together when skill content changes.
- Report exact commands run and outcomes.
- Call out residual risks and unavailable checks.

## Do Not

- Do not broadly refactor when a narrow fix works.
- Do not move or rename large skill trees without a migration plan.
- Do not mix multiple Angular major hops into one validation gate.
- Do not publish, commit, or open pull requests unless explicitly requested.
- Do not treat `npx skills add janpereira-dev/ngAutoPilot` as focused pack installation.

## Expected Output

When this skill is used, return:

1. Selected NgAutoPilot entry point or focused skill.
2. Compatibility and risk notes.
3. Files changed or inspected.
4. Validation commands and results.
5. Remaining risks or next safe step.
