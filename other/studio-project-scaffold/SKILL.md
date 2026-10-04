---
name: studio-project-scaffold
description: Use when running gamestudio init, status, or uninit, or bootstrapping a new or adopted game repository with AGENTS.md, HANDOFF.md, .agents/CONTRACT.md, project governance, a subsystem registry, or a per-project adapter report, plan digest, named reviewer, backup root, generated agent overlay, apply, uninstall, and .codex/config.toml preservation.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: workflow
    lifecycle_stage: build
    risk_level: medium
    packs: [studio-core, unity, cpp-lua-mmorpg]
    side_effects: files
    artifact: scaffold-report.json
    required_evidence: [detected-subsystems, created-file-list, preserved-file-list]
    owner: HoaTV Studio
    reviewer: Producer
    maturity: beta
    last_reviewed: 2026-09-07
    provenance:
      derived_from: none
      patterns_from: [sanitized multi-project governance fixtures]
      copied_text: none
---
# Studio Project Scaffold

## Overview
Create the minimum project-local governance, project profile, routing references, and agent-role overlay needed for safe multi-session work while preserving existing instructions, configuration, skills, and agents.

Newly generated profiles include optional `studio_experience` defaults for role, mode, and enabled intents. These defaults affect routing presentation only. Use `gamestudio guide` for a report-only Golden Path packet; `gamestudio init --apply` remains a separate reviewed mutation.

## When to use
Use for a new game repository, an inherited legacy project without agent governance, or a project that needs standardized ownership, evidence labels, and handoff state.

## When NOT to use
Do not overwrite a mature project-local `.agents/` system, existing `AGENTS.md`, `HANDOFF.md`, or skills. Generate a report and merge plan instead.

## Required inputs and context discovery
Collect workspace root, nested Git roots, Git state, existing governance files, Unity markers, server projects, Lua/data trees, database inputs, generated, cache, vendor, and excluded paths, project-local skill IDs, agent files, and `.codex/config.toml` state.

## Safety and risk level
Scaffolding and the per-project adapter are medium-risk because they write governance and agent files. Run report-only first, preserve every existing file by default, and never mutate external projects during kit tests.

## Workflow
1. Scan structure read-only and detect Unity, server, Lua, database, tooling, and generated subsystems.
   Completion criterion: detected subsystems and unknown areas are reported.
3. Inventory existing `AGENTS.md`, `HANDOFF.md`, `.agents/`, local skills, and ignore rules.
   Completion criterion: every existing governance artifact is marked preserve, merge, or BLOCKED.
4. Render the minimum scaffold with evidence, ownership, repeated-work tooling, mutation, generated-file, no-touch rules, project profile, workspace map, validation matrix, and adapter references.
   Completion criterion: `scaffold-report.json` lists exact proposed and preserved scaffold files without writes.
5. Run the per-project adapter report-only first. Review `plan_digest`, `proposed` planned paths, `collisions`, `activated_roles`, `scope_review`, preserved paths, and the action/hash details under `mutation_report.operations`. Broad resolved capability intersections are advisory; only out-of-scope or duplicate exact active write assignments block orchestration.
   Completion criterion: the reviewed adapter report identifies every proposed write and collision without mutation.
6. Apply only that reviewed adapter plan with a named reviewer, a disjoint project-local backup root, and the approved plan digest. Generate and review a new report when the digest is stale.
   Completion criterion: apply uses all three gates and returns its manifest and restore command.
7. Materialize roles from packaged generic agent templates plus profile and inferred specialists under `.codex/agents/`, preserving an explicit project `reasoning_effort` over the template default. The generated `.codex/agents.generated.toml` file remains inert until manual merge, and the adapter leaves `.codex/config.toml` untouched.
   Completion criterion: unmanaged agents and active configuration remain preserved, and effective scopes are reviewed only after role resolution.
8. Record per-file ownership hashes under `.agents/registry.json`, then run project-local validation and inspect the generated handoff snapshot.
   Completion criterion: scaffold output is parseable and unresolved runtime facts remain Unverified or BLOCKED.
9. Run uninstall report-only first and review its `plan_digest`, `proposed`, `preserved_drift`, and `remaining_owned` paths. Apply only with a named reviewer, a disjoint backup root, and that matching digest. Use hash-safe uninstall: remove only files matching recorded ownership hashes. Preserve drift and return `PARTIAL` with `preserved_drift` and `remaining_owned` for manual recovery when safe cleanup cannot finish.
   Completion criterion: uninstall never deletes unmanaged or drifted project content and cannot bypass the approval gates.

## Evidence and output contract
Produce `scaffold-report.json` with subsystem detection, source snapshots, proposed files, created files, preserved files, collisions, reviewer, and verification results. The separate per-project adapter report uses the implemented fields named in workflow step 4; do not rename them into the scaffold report.

## Handoff contract
Record project path, detected subsystems, existing local skills and agents, created governance files, preserved conflicts, adapter plan digest, reviewer, restore information, unresolved ownership, and the project-intake reactivation prompt.

## Pitfalls and anti-rationalization
- Similarity to golden fixtures does not authorize copying project-specific text.
- Never overwrite `project-*` or other project-local skills.
- Keep activation in the generated inert file for manual review; do not edit `.codex/config.toml`.
- Treat hash drift as preserved project content requiring manual recovery, not deletion authority.
- Do not infer service ports or DB schemas from directory names.
- Generated scaffold state is only a starting Snapshot.

## Verification checklist
- [ ] Report-only ran before apply.
- [ ] The selected apply entry point received its named reviewer and the approved digest from its reviewed report.
- [ ] Direct API, standalone script, and `gamestudio init --apply` independently enforce the same canonical approval contract; adapters forward the selected values to the API, and parity verification does not require an operator to run all three.
- [ ] Backup root is project-local and does not overlap any proposed scaffold output.
- [ ] Existing governance and local skills were preserved.
- [ ] Generic templates and profile specialists were collision-checked.
- [ ] `scope_review` separates advisory capability overlap from exact simultaneous assignment conflicts.
- [ ] Explicit project reasoning effort is preserved in generated specialist agents.
- [ ] Activation stayed inert and `.codex/config.toml` stayed untouched.
- [ ] Per-file ownership and uninstall recovery fields were recorded.
- [ ] Detected subsystems are evidence-backed.
- [ ] Created files carry generated markers where appropriate.
- [ ] Runtime facts remain Unverified or BLOCKED until checked.

## References and scripts
Use `code-intelligence-contract` with the bundled vendor-neutral [scripts/code_intelligence.py](scripts/code_intelligence.py) helper and legacy-compatible [scripts/codegraph_adapter.py](scripts/codegraph_adapter.py) adapter. Use [scripts/gamestudio_cli.py](scripts/gamestudio_cli.py) with [scripts/project_scaffold.py](scripts/project_scaffold.py), [scripts/project_complexity.py](scripts/project_complexity.py), and [scripts/project_skill_overlay.py](scripts/project_skill_overlay.py) with [scripts/project_profile.py](scripts/project_profile.py) and [scripts/safe_mutation.py](scripts/safe_mutation.py). Use [scripts/studio_experience.py](scripts/studio_experience.py) for report-only role-aware Golden Path planning and [scripts/agent_overlay.py](scripts/agent_overlay.py) as the pure planner for packaged generic roles, profile specialists, collisions, and inert activation operations. These references do not weaken report-only planning, approved plan digest, named reviewer, disjoint backup root, or restore requirements. Per-project apply and uninstall remain repository-root maintenance commands available only in a full clone. Sanitized golden fixtures are also full-clone-only resources.
