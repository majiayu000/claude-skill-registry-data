---
id: angular.versioning.angular-versioning-index
name: Angular Versioning Index
description: >
  Central index for Angular versioning, compatibility gates, hop planning, and routing to the correct upgrade or modernization skill.
stack:
  - Angular
  - TypeScript
  - RxJS
category: versioning
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - Angular versioning index
  - Angular upgrade roadmap
  - versioning catalog
  - hop index
  - compatibility gate index
compatibility:
  angular:
    min: "2"
---

# Angular Versioning Index

## Purpose

Use this skill as the master index for Angular version decisions. It does not perform upgrades. It routes the agent to the correct gate, hop, or modernization skill based on detected Angular version and upgrade intent.

## When to Use

Use this skill when:

- The user asks for the Angular upgrade roadmap.
- The agent needs the canonical entry point for version-sensitive Angular work.
- A hop must be selected from the detected Angular version.
- A compatibility gate must be applied before a hop.
- The user asks which versioning skill should be used next.

## When Not to Use

Do not use this skill when:

- The task is a concrete upgrade hop already selected by another router.
- The task is a local refactor unrelated to Angular versioning.
- The compatibility decision is already resolved and the user only wants implementation.

## Required Inputs

Collect:

```txt
Current Angular version
Target Angular version
Current Node.js version
Current TypeScript version
Current RxJS version
Angular CLI version
Project package manager
Lockfile type
SSR usage
AngularJS / ngUpgrade usage
Material usage
Router customization usage
Testing strategy
```

Read these files when available:

```txt
package.json
package-lock.json
yarn.lock
pnpm-lock.yaml
angular.json
nx.json
workspace.json
tsconfig.json
tsconfig.base.json
.nvmrc
.node-version
CI workflow files
```

## Procedure

1. Detect the current Angular stack.
2. Run the Angular version compatibility gate.
3. Select the nearest upgrade hop or modernization skill.
4. Route framework-specific risks to the matching satellite.
5. Keep the hop, gate, and modernization steps separate.

## Angular 22 Routing

- For Angular 21 -> 22 upgrades, start with `skills/angular/upgrades/21-to-22/angular-21-to-22-upgrade-orchestrator/SKILL.md`.
- For Angular 22 feature adoption or remediation, select the narrow concern-first `angular-v22-*` satellite.
- Use `skills/angular/upgrades/versioning/angular-21-to-22-index/SKILL.md` for the bounded hop map.
- Use `skills/angular/versioning/angular-v22-feature-index/SKILL.md`, `angular-v22-risk-matrix`, and `angular-v22-roadmap-alignment` for post-hop routing.
- Do not create or prefer a generic `skills/angular/v22/` folder.

## Do

- Use `skills/angular/versioning/angular-version-compatibility-gate/SKILL.md` as the formal compatibility decision.
- Keep the index focused on navigation, not migration.
- Prefer one hop at a time.
- Keep the master index consistent with the catalog.

## Do Not

- Do not duplicate hop logic inside the index.
- Do not create an alternate compatibility matrix here.
- Do not mix upgrade execution with routing guidance.
- Do not bypass the compatibility gate.

## Review Checklist

- [ ] The detected Angular version is known.
- [ ] The target hop is known or explicitly unresolved.
- [ ] The compatibility gate is invoked.
- [ ] The selected hop or satellite is explicit.
- [ ] Modernization is separated from upgrade work.

## Expected Output

1. State the current Angular version and target direction.
2. Name the compatibility gate used.
3. Name the selected hop skill or satellite skill.
4. State whether the next step is blocked or allowed.

## Exit Criteria

- The agent has a single, explicit next skill or hop.
- The compatibility gate has been applied before execution.
- The index does not perform migration itself.
