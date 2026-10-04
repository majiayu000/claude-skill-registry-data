---
name: spec-driven-build
description: Methodology for transforming a technical specification into a verified implementation plan. Use when starting non-trivial features.
version: "1.0.0"
verified_date: 2026-04-29
category: core
---

# Spec-Driven Build

## Purpose
Ensure that implementation follows the architectural plan and meets all technical requirements without feature creep or design drift.

## When to Use This Skill
Use at the start of the BUILD phase after the initial PLANNING is complete.

## Phase 1: Requirement Mapping
1. Cross-reference the user request with the implementation plan.
2. Identify potential technical risks or missing edge cases.

## Phase 2: Component Blueprinting & XML Plan Generation
1. Define the interface for every new component or service.
2. If structuring roadmaps or multi-step executions, use the strict XML `<task>` format.
3. **XML Structure**: Wrap the global plan in `<implementation_plan>`. Use `<phase>` blocks, containing `<task>` blocks. Each task must have a `status="pending|in-progress|completed"`. Add strict constraints to XML outputs so CI/CD pipelines and automated test runners can parse them natively.
4. When starting a **new project**, establish structural scaffolding first. Verify `package.json`, environment configurations, and core layout shells before jumping to atomic components.

## Output Format / Delivery
- Implementation plan artifact.
- Verified component blueprints.

## Behavior Rules
1. **Stick to the Spec**. Do not add features that weren't in the approved plan.
2. **Pre-Implementation Review**. Verify the plan one last time before writing code.

## Maintenance Notes
- Initial global core skill.
- Absorbed `gsd-xml-plan-generation` and `gsd-new-project-planning` to unify roadmap and scaffolding protocols into a single master skill.
