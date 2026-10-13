---
name: team-combat
description: "Use this skill when a critical combat feature or product workflow needs a coordinated implementation squad spanning design, engineering, security, operations, UX, and QA."
argument-hint: "[combat feature description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

## User Guide

- When to use: Orchestrate a critical feature squad. Game: combat team with game design, gameplay, AI, VFX, audio, engine, QA. Product: critical workflow/API/CLI feature squad with lead-programmer, language specialist, security/devops as needed, UX, and QA.
- Inputs: Command arguments: `/team-combat [combat feature description]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before orchestrating the team:
- `design/cdd/game-concept.md` -> **[Game]** keep the existing combat team workflow: game design, gameplay programming, AI, VFX, audio, engine validation, QA, and balance follow-up.
- `design/cdd/product-concept.md` -> **[Product]** use this command as a critical-workflow feature squad: lead-programmer, language specialist, security-engineer if permissions/data are involved, devops-engineer if deployment/infrastructure is involved, ux-designer for user-facing flow, and qa-tester for contract/integration evidence.
- If unclear, ask whether the requested feature is game combat or a product critical workflow/API/CLI capability.

The combat workflow below remains intact for games. Product orchestration is a parallel branch for the same command.

**Argument check:** If no combat feature description is provided, output:
> "Usage: `/team-combat [combat feature description]` — Provide a description of the combat feature to design and implement (e.g., `melee parry system`, `ranged weapon spread`)."
Then stop immediately without spawning any subagents or reading any files.

When this skill is invoked with a valid argument, orchestrate the combat team through a structured pipeline.

**Decision Points:** At each phase transition, use `AskUserQuestion` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **game-designer** — Design the mechanic, define formulas and edge cases
- **gameplay-programmer** — Implement the core gameplay code
- **ai-programmer** — Implement NPC/enemy AI behavior for the feature
- **technical-artist** — Create VFX, shader effects, and visual feedback
- **sound-designer** — Define audio events, impact sounds, and ambient combat audio
- **engine specialist** (primary) — Validate architecture and implementation patterns are idiomatic for the engine (read from `standards/technical-preferences.md` Engine Specialists section)
- **qa-tester** — Write test cases and validate the implementation

## Product Team Composition
- **lead-programmer** — Own the critical workflow/API/CLI architecture and module boundaries
- **language specialist** (`python-specialist`, `typescript-specialist`, `rust-specialist`, or `go-specialist`) — Implement stack-specific code from `standards/technical-preferences.md`
- **ux-designer** — Own user workflow, CLI/API consumer journey, error recovery, and accessibility handoff
- **security-engineer** — Join when auth, permissions, secrets, tenant data, payments, or external integrations are involved
- **devops-engineer** — Join when deployment, CI/CD, migrations, infrastructure, or rollback paths are involved
- **qa-tester** — Write contract, CLI, e2e, migration, smoke, and validation evidence

## How to Delegate

Use the Task tool to spawn each team member as a subagent:
- `subagent_type: game-designer` — Design the mechanic, define formulas and edge cases
- `subagent_type: gameplay-programmer` — Implement the core gameplay code
- `subagent_type: ai-programmer` — Implement NPC/enemy AI behavior
- `subagent_type: technical-artist` — Create VFX, shader effects, visual feedback
- `subagent_type: sound-designer` — Define audio events, impact sounds, ambient audio
- `subagent_type: [primary engine specialist]` — Engine idiom validation for architecture and implementation
- `subagent_type: qa-tester` — Write test cases and validate implementation

Always provide full context in each agent's prompt (design doc path, relevant code files, constraints). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 3 agents can run simultaneously).

For Product prompts, pass:
- `design/cdd/product-concept.md` User Promise, JTBD, principles, target users, platform/stack
- Relevant Product CDD or quick spec from `design/cdd/`
- UX/workflow specs from `design/ux/` when user-facing
- ADRs and stack reference under `docs/architecture/` and `docs/reference/<stack>/`
- Existing source paths (`src/api`, `src/cli`, `src/services`, `src/app`, `migrations`, config, package/build files)
- Required tests and validation targets under `tests/` and `production/qa/evidence/user-tests/`

## Pipeline

### Phase 1: Design
Delegate to **game-designer**:
- Create or update the design document in `design/cdd/` covering: mechanic overview, player fantasy, detailed rules, formulas with variable definitions, edge cases, dependencies, tuning knobs with safe ranges, and acceptance criteria
- Output: completed design document

### Phase 2: Architecture
Delegate to **gameplay-programmer** (with **ai-programmer** if AI is involved):
- Review the design document
- Design the code architecture: class structure, interfaces, data flow
- Identify integration points with existing systems
- Output: architecture sketch with file list and interface definitions

Then spawn the **primary engine specialist** to validate the proposed architecture:
- Is the class/node/component structure idiomatic for the pinned engine? (e.g., Godot node hierarchy, Unity MonoBehaviour vs DOTS, Unreal Actor/Component design)
- Are there engine-native systems that should be used instead of custom implementations?
- Any proposed APIs that are deprecated or changed in the pinned engine version?
- Output: engine architecture notes — incorporate into the architecture before Phase 3 begins

### Phase 3: Implementation (parallel where possible)
Delegate in parallel:
- **gameplay-programmer**: Implement core combat mechanic code
- **ai-programmer**: Implement AI behaviors (if the feature involves NPC reactions)
- **technical-artist**: Create VFX and shader effects
- **sound-designer**: Define audio event list and mixing notes

### Phase 4: Integration
- Wire together gameplay code, AI, VFX, and audio
- Ensure all tuning knobs are exposed and data-driven
- Verify the feature works with existing combat systems

### Phase 5: Validation
Delegate to **qa-tester**:
- Write test cases from the acceptance criteria
- Test all edge cases documented in the design
- Verify performance impact is within budget
- File bug reports for any issues found

### Phase 6: Sign-off
- Collect results from all team members
- Report feature status: COMPLETE / NEEDS WORK / BLOCKED
- List any outstanding issues and their assigned owners

## Product Pipeline

### Product Phase 1: Workflow / Contract Design
Delegate to **lead-programmer** and **ux-designer**:
- Confirm the Product CDD or quick spec covers User Promise, JTBD, workflow steps, API/CLI/web/data contract, edge cases, configuration, and acceptance criteria
- Identify whether the feature is primarily API, CLI, web workflow, data/migration, library, or deployment tooling
- Output: implementation-ready Product spec with open questions clearly separated from agreed requirements

### Product Phase 2: Architecture and Stack Handoff
Delegate to **lead-programmer** and the selected **language specialist**:
- Propose module boundaries, public API/CLI surface, data model, error semantics, idempotency/retry behavior, and observability hooks
- Validate against ADRs and `docs/reference/<stack>/VERSION.md`
- If auth/permissions/data risk exists, spawn **security-engineer** in parallel
- If deployment/migration/rollback risk exists, spawn **devops-engineer** in parallel
- Output: architecture sketch, file list, interface contract, and risk notes

### Product Phase 3: Implementation
Delegate to the **language specialist** with lead-programmer coordination:
- Implement source changes in the appropriate stack
- Keep API/CLI/web/data contracts stable and documented
- Surface deviations from Product CDD, UX spec, or ADR before writing

### Product Phase 4: Validation
Delegate to **qa-tester**:
- Write or update contract, CLI, e2e, migration, smoke, and regression tests
- Produce evidence in the matching subdirectory under `production/qa/evidence/`
- Verify error recovery, accessibility, observability, and docs examples

### Product Phase 5: Sign-off
- Report READY / NEEDS WORK / BLOCKED
- List open Product risks by owner: lead-programmer, language specialist, security-engineer, devops-engineer, ux-designer, qa-tester
- Recommend `/code-review`, `/security-audit`, `/smoke-check`, `/content-audit`, or `/team-release` as appropriate

## Error Recovery Protocol

If any spawned agent (via Task) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via AskUserQuestion with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, CDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `/architecture-decision` first
- Scope too large → split into two stories via `/create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

All file writes (design documents, implementation files, test cases) are
delegated to sub-agents spawned via Task. Each sub-agent enforces the
"May I write to [path]?" protocol. This orchestrator does not write files directly.

## Output

A summary report covering: design completion status, implementation status per team member, test results, and any open issues.

Verdict: **COMPLETE** — combat feature designed, implemented, and validated.
Verdict: **BLOCKED** — one or more phases could not complete; partial report produced with unresolved items listed.

## Next Steps

- Run `/code-review` on the implemented combat code before closing stories.
- Run `/balance-check` to validate combat formulas and tuning values.
- Run `/team-polish` if VFX, audio, or performance polish is needed.
- Product: run `/code-review` on implemented API/CLI/web/data code.
- Product: run `/smoke-check` and relevant contract/CLI/e2e/migration tests.
- Product: run `/content-audit` if docs, generated help, schemas, or examples changed.
