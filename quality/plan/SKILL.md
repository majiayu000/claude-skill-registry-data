---
name: Plan
description: Decompose work into small testable tasks with clear dependencies
---

# Plan Skill

## Overview
Create a concrete implementation plan by decomposing work into small, testable tasks with dependencies and acceptance criteria.

## Methodology
1. Read the spec from the epic description (`bd show <epic>`) for EARS requirements, decisions, and open questions. Verify its type is `epic` -- if it was created as `task`, fix with `bd update <id> --type=epic`
2. Search memory with `ca search` and docs with `ca knowledge "relevant topic"` for architectural patterns and past mistakes
3. Spawn **subagents** via Task tool in parallel for research (lightweight, no inter-agent coordination):
   - Available agents: `.claude/agents/compound/repo-analyst.md`, `memory-analyst.md`
   - For complex features, deploy MULTIPLE analysts per domain area
   - Synthesize all findings before decomposing into tasks
4. For decisions requiring deep technical grounding, invoke the **researcher skill** to produce a survey document. Review findings before decomposing into tasks.
5. Synthesize research findings into a coherent approach. Flag conflicts between ADRs and proposed plan.
6. Use `AskUserQuestion` to resolve ambiguities, conflicting constraints, or priority trade-offs before decomposing
7. Decompose into tasks small enough to verify individually
8. Define acceptance criteria for each task
9. Ensure each task traces back to a spec requirement for traceability
10. **Generate Acceptance Criteria table**: Extract testable criteria from EARS requirements and append to the epic description. Use this format:

    ```markdown
    ## Acceptance Criteria
    | ID | Source Req | Criterion | Verification Method |
    |----|-----------|-----------|---------------------|
    | AC-1 | EARS-N | When X, system shall Y within Z | unit test / manual / integration |
    ```

    Rules:
    - Each EARS requirement MUST map to at least one AC row
    - Criteria MUST be testable (no vague adjectives like "fast" or "good")
    - Verification method MUST be specified
    - Write the AC table to the epic via `bd update <epic-id> --description="<existing desc + AC section>"`
    - The AC section is **append-only** after plan phase; review annotates pass/fail
11. **Generate Verification Contract**: Derive a minimal, per-epic definition of done and append it to the epic description after the Acceptance Criteria section. Use this format:

    ```markdown
    ## Verification Contract
    Profile: webapp | api | cli | library | service | mixed
    Surfaces:
    - ui_surface
    Risks:
    - user_visible_quality
    Required evidence:
    - test
    - lint
    - build
    ```

    Rules:
    - Detect the profile from repo signals plus the epic's actual scope. If architect/spec work noted a default profile, use it as advisory input only.
    - Keep the contract **local to this epic**. Do NOT create repo-global config for this.
    - Start from a baseline and then tailor:
      - `webapp` -> `test`, `lint`, `build`, `runtime_startup`, `browser_evidence`
      - `api` -> `test`, `lint`, `build`, `runtime_startup`, `contract_checks`
      - `cli` -> `test`, `lint`, `build`, `help_version_check`, `command_transcript`
      - `library` -> `test`, `lint`, `build`, `examples_run`, `public_api_review`
      - `service` -> `test`, `lint`, `build`, `runtime_startup`, `config_validation`
    - Add contract-specific evidence from touched surfaces and risks:
      - `ui_surface` -> `responsive_check`, `edge_states_check`, `console_network_clean`, `a11y_smoke`, `design_craft_check`
      - `public_api` -> `contract_examples`, `backward_compat_review`
      - `persistence_schema` -> `roundtrip_test`, `migration_check`, `backcompat_check`
      - `packaging_or_distribution` -> `package_build`, `install_smoke`
      - `docs_or_examples` -> `docs_examples_sync`
      - `auth_or_security` -> `auth_failure_paths`
      - `performance_sensitive` -> `performance_budget_check`
    - Use a small, explicit vocabulary for `Surfaces` and `Risks`; prefer consistency over novelty.
    - If the profile is ambiguous **and** the choice materially changes required evidence, resolve it with `AskUserQuestion` once before finalizing the plan.
    - Write the Verification Contract to the epic via `bd update <epic-id> --description="<existing desc + AC section + Verification Contract section>"`
    - The Verification Contract is **append-only** after plan; review may escalate it explicitly if risk was underestimated.
12. Map dependencies between tasks
13. Create beads issues: `bd create --title="..." --type=task`
14. Create review and compound blocking tasks (`bd create` + `bd dep add`) that depend on work tasks — these survive compaction and surface via `bd ready` after work completes

## Memory Integration
- Run `ca search` and `ca knowledge "relevant topic"` for patterns related to the feature area
- Look for past planning mistakes (missing dependencies, unclear criteria)
- Check for preferred architectural patterns in this codebase

## Docs Integration
- Spawn docs-analyst to scan `docs/` for relevant specs, standards, and research
- Check `docs/decisions/` for existing ADRs that constrain or inform the plan
- If the plan contradicts an ADR, flag it for the user before proceeding

## Common Pitfalls
- Creating too many fine-grained tasks (aim for 3-7 per feature)
- Unclear acceptance criteria ("make it work" is not a criterion)
- Missing dependencies between tasks
- Not checking memory for past architectural decisions
- Not reviewing existing ADRs and docs for constraints
- Making architectural decisions without research backing (use the researcher skill for complex domains)
- Planning implementation details too early (stay at task level)
- Not generating Acceptance Criteria table from EARS requirements
- Not generating a Verification Contract, leaving later phases to guess what evidence is required

## Quality Criteria
- Each task has clear acceptance criteria
- Dependencies are mapped and no circular dependencies exist
- Tasks are ordered so each can be verified independently
- Memory was searched for relevant patterns and past mistakes
- Existing docs and ADRs were checked for constraints
- Ambiguities resolved via `AskUserQuestion` before decomposing
- Complexity estimates are realistic (no "should be quick")
- Each task traces back to a spec requirement
- **Acceptance Criteria table generated and appended to epic description**
- **Verification Contract generated and appended to epic description**

## POST-PLAN VERIFICATION -- MANDATORY
After creating all tasks, verify review and compound tasks exist:
- Run `bd list --status=open` and check for a "Review:" task and a "Compound:" task
- If either is missing, CREATE THEM NOW. The plan is NOT complete without these gates.
- **Verify AC table**: Run `bd show <epic-id>` and confirm the `## Acceptance Criteria` section exists in the description. If missing, the plan is NOT complete.
- **Verify contract**: Run `bd show <epic-id>` and confirm the `## Verification Contract` section exists in the description. If missing, the plan is NOT complete.
