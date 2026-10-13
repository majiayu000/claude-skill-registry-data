---
name: estimate
description: "Estimates task effort by analyzing complexity, dependencies, historical velocity, and risk factors. Produces a structured estimate with confidence levels."
argument-hint: "[task-description]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

## User Guide

- When to use: Estimates task effort by analyzing complexity, dependencies, historical velocity, and risk factors. Produces a structured estimate with confidence levels.
- Inputs: Command arguments: `/estimate [task-description]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before estimating:
- `design/cdd/game-concept.md` -> **[Game]** estimate using game risk factors: mechanic complexity, engine integration, content production, tuning, playtest iteration, platform constraints, and asset dependencies.
- `design/cdd/product-concept.md` -> **[Product]** estimate using product risk factors: API/CLI/UI scope, data model changes, migrations, integration boundaries, security, observability, deployment, and documentation.
- If unclear, ask which risk model to use.

Keep game estimation examples; product estimates add a parallel calibration model.
## Phase 1: Understand the Task

Read the task description from the argument. If the description is too vague to estimate meaningfully, ask for clarification before proceeding.

Read AGENTS.md for project context: tech stack, coding standards, architectural patterns, and any estimation guidelines.

Read relevant design documents from `design/cdd/` if the task relates to a documented feature or system.

---

## Phase 2: Scan Affected Code

Identify files and modules that would need to change:

- Assess complexity (size, dependency count, cyclomatic complexity)
- Identify integration points with other systems
- Check for existing test coverage in the affected areas
- Read past sprint data from `production/sprints/` for similar completed tasks and historical velocity

**[Product] Product surface scan:**
- Identify API endpoints, CLI commands, UI screens, data models, migrations, config files, package/deployment files, docs, and examples that would change.
- Check `docs/architecture/`, ADRs, `design/cdd/`, `design/ux/`, and `production/qa/` for contract, evidence, and release constraints.
- Identify language specialist ownership from `standards/technical-preferences.md` and note whether a Product task needs Python, TypeScript, Rust, Go, devops, security, UX, QA, or lead-programmer review.

---

## Phase 3: Analyze Complexity Factors

**Code Complexity:**
- Lines of code in affected files
- Number of dependencies and coupling level
- Whether this touches core/engine code vs leaf/feature code
- Whether existing patterns can be followed or new patterns are needed

**Scope:**
- Number of systems touched
- New code vs modification of existing code
- Amount of new test coverage required
- Data migration or configuration changes needed

**Risk:**
- New technology or unfamiliar libraries
- Unclear or ambiguous requirements
- Dependencies on unfinished work
- Cross-system integration complexity
- Performance sensitivity

**[Product] Product complexity factors:**
- API/CLI/UI contract shape and backward compatibility
- Data model or migration impact
- Auth, permission, privacy, or security boundary changes
- Observability, logging, alerting, and operational runbook updates
- Deployment/package/release coupling
- Documentation and SDK/example updates required for public surfaces
- Integration dependencies on third-party APIs, queues, storage, or external services
- Test evidence needed: contract, integration, migration, smoke, load, or user-workflow validation

**[Product] Product risk model:**
- **Low**: Internal-only change, no contract/schema/migration, tests already cover the module, docs not affected.
- **Medium**: One public API/CLI/UI surface changes, docs/examples need updates, one integration or config path is touched.
- **High**: Breaking contract risk, migration or auth change, deployment impact, multiple modules, data loss/security/privacy exposure, or uncertain stack API.
- **Spike required**: Unknown third-party API behavior, unverified framework version behavior, unclear migration path, or no existing pattern for the product surface.

---

## Phase 4: Generate the Estimate

```markdown
## Task Estimate: [Task Name]
Generated: [Date]

### Task Description
[Restate the task clearly in 1-2 sentences]

### Complexity Assessment

| Factor | Assessment | Notes |
|--------|-----------|-------|
| Systems affected | [List] | [Core, gameplay, UI, etc.] |
| Files likely modified | [Count] | [Key files listed below] |
| New code vs modification | [Ratio] | |
| Integration points | [Count] | [Which systems interact] |
| Test coverage needed | [Low / Medium / High] | |
| Existing patterns available | [Yes / Partial / No] | |

**Key files likely affected:**
- `[path/to/file1]` -- [what changes here]

### Effort Estimate

| Scenario | Days | Assumption |
|----------|------|------------|
| Optimistic | [X] | Everything goes right, no surprises |
| Expected | [Y] | Normal pace, minor issues, one round of review |
| Pessimistic | [Z] | Significant unknowns surface, blocked for a day |

**Recommended budget: [Y days]**

### Confidence: [High / Medium / Low]

[Explain which factors drive the confidence level for this specific task.]

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

### Dependencies

| Dependency | Status | Impact if Delayed |
|-----------|--------|-------------------|

### Suggested Breakdown

| # | Sub-task | Estimate | Notes |
|---|----------|----------|-------|
| 1 | [Research / spike] | [X days] | |
| 2 | [Core implementation] | [X days] | |
| 3 | [Testing and validation] | [X days] | |
| | **Total** | **[Y days]** | |

### Notes and Assumptions
- [Key assumption that affects the estimate]
- [Any caveats about scope boundaries]
```

For product tasks, include this Product-specific extension in the estimate:

```markdown
### Product Surface Assessment

| Factor | Assessment | Notes |
|--------|------------|-------|
| Public surface changed | [API / CLI / UI / Data / Config / Docs / None] | [contract names] |
| Compatibility impact | [None / additive / breaking-risk / breaking] | [migration or fallback notes] |
| Data or migration impact | [None / small / significant] | [schemas/tables/files] |
| Security/privacy impact | [None / low / medium / high] | [auth/permissions/data exposure] |
| Operational impact | [None / deploy / monitoring / on-call / rollback] | [runbook/evidence needed] |
| Documentation/examples | [None / update / new docs required] | [paths likely affected] |

### Product Test Evidence Needed

| Evidence Type | Needed? | Notes |
|---------------|---------|-------|
| Contract/API or CLI tests | [Yes/No] | |
| Integration tests | [Yes/No] | |
| Migration/config validation | [Yes/No] | |
| Smoke/user-workflow test | [Yes/No] | |
| Performance/load check | [Yes/No] | |
| Docs/example verification | [Yes/No] | |
```

Output the estimate with a brief summary: recommended budget, confidence level, and the single biggest risk factor.

This skill is read-only — no files are written. Verdict: **COMPLETE** — estimate generated.

---

## Phase 5: Next Steps

- If confidence is Low: recommend a time-boxed spike (`/prototype`) before committing.
- If the task is > 10 days: recommend breaking it into smaller stories via `/create-stories`.
- To schedule the task: run `/sprint-plan update` to add it to the next sprint.

**[Product] Product next steps:**
- If the task changes a public API/CLI/UI/data contract, recommend `/propagate-design-change` before implementation.
- If the task changes migration, deployment, or package behavior, recommend `/release-checklist` or `/hotfix` depending on urgency.
- If the task has unknown stack behavior, recommend `/prototype` or `/setup-engine refresh [stack]` before committing to the estimate.

### Guidelines

- Always give a range (optimistic / expected / pessimistic), never a single number
- The recommended budget should be the expected estimate, not the optimistic one
- Round to half-day increments — estimating in hours implies false precision for tasks longer than a day
- Do not pad estimates silently — call out risk explicitly so the team can decide
