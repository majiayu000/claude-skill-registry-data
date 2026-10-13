---
name: team-polish
description: "Orchestrate the polish team: coordinates performance-analyst, technical-artist, sound-designer, and qa-tester to optimize, polish, and harden a feature or area for release quality."
argument-hint: "[feature or area to polish]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

## User Guide

- When to use: Orchestrate the polish team: coordinates performance-analyst, technical-artist, sound-designer, and qa-tester to optimize, polish, and harden a feature or area for release quality.
- Inputs: Command arguments: `/team-polish [feature or area to polish]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before the polish pass:
- `design/cdd/game-concept.md` -> **[Game]** keep the existing polish pass across performance, audio, visuals, UX, gameplay behavior, and playtest issues.
- `design/cdd/product-concept.md` -> **[Product]** run a product polish pass across UX clarity, API/CLI ergonomics, docs accuracy, performance, observability, error messages, accessibility, deployment readiness, and reliability.
- If unclear, ask whether this polish target is game feel/content or product usability/reliability.

Do not delete game polish checks. Product polish checks are a parallel branch.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Game Concept, target CDDs, art bible, UX/HUD specs, performance budgets, playtest/bug reports, QA evidence | Product Concept, target CDDs, interaction patterns, optional style/design system docs, ADRs, performance budgets, docs/examples, QA/deployment evidence |
| Steps | Assess, optimize, polish visuals/audio/feel/UX, test edge cases, produce release-quality verdict | Assess, polish UX/API/CLI/docs/errors/observability/reliability/security/deployment readiness, test regressions, produce release-quality verdict |
| Outputs | Prioritized polish backlog, code/content fixes, profiler/evidence notes, QA retest list, READY/NEEDS MORE WORK verdict | Prioritized product polish backlog, contract/docs/deploy/test impact, hardening checklist, evidence paths, READY/NEEDS MORE WORK verdict |
| Next steps | `/asset-audit`, `/team-qa`, `/release-checklist`, `/team-release` | `/content-audit`, `/security-audit` when available or manual security review, `/team-qa`, `/release-checklist`, `/team-release` |

If no argument is provided, output usage guidance and exit without spawning any agents:
> Usage: `/team-polish [feature or area]` — specify the feature or area to polish (e.g., `combat`, `main menu`, `inventory system`, `level-1`). Do not use `AskUserQuestion` here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the polish team through a structured pipeline.

**Decision Points:** At each phase transition, use `AskUserQuestion` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **performance-analyst** — Profiling, optimization, memory analysis, frame budget
- **engine-programmer** — Engine-level bottlenecks: rendering pipeline, memory, resource loading (invoke when performance-analyst identifies low-level root causes)
- **technical-artist** — VFX polish, shader optimization, visual quality
- **sound-designer** — Audio polish, mixing, ambient layers, feedback sounds
- **tools-programmer** — Content pipeline tool verification, editor tool stability, automation fixes (invoke when content authoring tools are involved in the polished area)
- **qa-tester** — Edge case testing, regression testing, soak testing

## Product Team Composition
- **performance-analyst** — API latency, CLI runtime, web responsiveness, memory, throughput, data pipeline performance
- **lead-programmer** — Architecture cleanup, public contract polish, error semantics, module boundaries
- **language specialist** — Stack-specific implementation polish and idiom review
- **ux-designer** — Workflow clarity, API/CLI consumer ergonomics, empty/error/loading states, accessibility handoff
- **security-engineer** — Auth, permissions, secrets, dependency, and data-handling hardening
- **devops-engineer** — Build/deploy/rollback, observability, migrations, release packaging
- **qa-tester** — Regression, contract, CLI, e2e, migration, smoke, and reliability evidence

## How to Delegate

Use the Task tool to spawn each team member as a subagent:
- `subagent_type: performance-analyst` — Profiling, optimization, memory analysis
- `subagent_type: engine-programmer` — Engine-level fixes for rendering, memory, resource loading
- `subagent_type: technical-artist` — VFX polish, shader optimization, visual quality
- `subagent_type: sound-designer` — Audio polish, mixing, ambient layers
- `subagent_type: tools-programmer` — Content pipeline and editor tool verification
- `subagent_type: qa-tester` — Edge case testing, regression testing, soak testing

Always provide full context in each agent's prompt (target feature/area, performance budgets, known issues). Launch independent agents in parallel where the pipeline allows it (e.g., Phases 3 and 4 can run simultaneously).

For Product prompts, include `design/cdd/product-concept.md`, relevant Product CDDs,
UX/workflow specs, ADRs, `docs/reference/<stack>/`, existing test evidence, docs
examples, build artifacts, migration/config files, and known validation issues from
`production/qa/evidence/user-tests/`.

## Pipeline

### Phase 1: Assessment
Delegate to **performance-analyst**:
- Profile the target feature/area using `/perf-profile`
- Identify performance bottlenecks and frame budget violations
- Measure memory usage and check for leaks
- Benchmark against target hardware specs
- Output: performance report with prioritized optimization list

### Phase 2: Optimization
Delegate to **performance-analyst** (with relevant programmers as needed):
- Fix performance hotspots identified in Phase 1
- Optimize draw calls, reduce overdraw
- Fix memory leaks and reduce allocation pressure
- Verify optimizations don't change gameplay behavior
- Output: optimized code with before/after metrics

If Phase 1 identified engine-level root causes (rendering pipeline, resource loading, memory allocator), delegate those fixes to **engine-programmer** in parallel:
- Optimize hot paths in engine systems
- Fix allocation pressure in core loops
- Output: engine-level fixes with profiler validation

### Phase 3: Visual Polish (parallel with Phase 2)
Delegate to **technical-artist**:
- Review VFX for quality and consistency with art bible
- Optimize particle systems and shader effects
- Add screen shake, camera effects, and visual juice where appropriate
- Ensure effects degrade gracefully on lower settings
- Output: polished visual effects

### Phase 4: Audio Polish (parallel with Phase 2)
Delegate to **sound-designer**:
- Review audio events for completeness (are any actions missing sound feedback?)
- Check audio mix levels — nothing too loud or too quiet relative to the mix
- Add ambient audio layers for atmosphere
- Verify audio plays correctly with spatial positioning
- Output: audio polish list and mixing notes

### Phase 5: Hardening
Delegate to **qa-tester**:
- Test all edge cases: boundary conditions, rapid inputs, unusual sequences
- Soak test: run the feature for extended periods checking for degradation
- Stress test: maximum entities, worst-case scenarios
- Regression test: verify polish changes haven't broken existing functionality
- Test on minimum spec hardware (if available)
- Output: test results with any remaining issues

### Phase 6: Sign-off
- Collect results from all team members
- Compare performance metrics against budgets
- Report: READY FOR RELEASE / NEEDS MORE WORK
- List any remaining issues with severity and recommendations

## Product Pipeline

### Product Phase 1: Assessment
Delegate to **performance-analyst**, **ux-designer**, and **qa-tester**:
- Review user workflow, API/CLI ergonomics, docs accuracy, accessibility, reliability, observability, and test evidence
- Profile latency, memory, throughput, startup time, command runtime, build/package time, and migration duration as relevant
- Output: prioritized Product polish backlog with severity, owner, evidence path, and release risk

### Product Phase 2: Contract and Ergonomics Polish
Delegate to **lead-programmer**, **language specialist**, and **ux-designer**:
- Improve API/CLI/web/data error clarity, naming, defaults, idempotency/retry guidance, and state visibility
- Preserve accepted public contracts unless a CDD/ADR update is approved
- Output: implementation-ready polish changes with docs/test impact listed

### Product Phase 3: Reliability and Release Hardening
Delegate to **security-engineer** and **devops-engineer** when relevant:
- Check auth/permissions/secrets/dependencies/data handling
- Check migration dry-run/rollback, deployment health checks, logging/metrics/traces, package artifacts, and rollback plan
- Output: hardening checklist and required fixes before release

### Product Phase 4: Validation
Delegate to **qa-tester**:
- Run smoke, contract, CLI, e2e, migration, regression, load/endurance, and docs-example checks as applicable
- Write evidence to the matching subdirectory under `production/qa/evidence/`
- Output: READY FOR RELEASE / NEEDS MORE WORK with blockers and owners

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

All file writes (performance reports, test results, evidence docs) are delegated to
sub-agents spawned via Task. Each sub-agent enforces the "May I write to [path]?"
protocol. This orchestrator does not write files directly.

## Output

A summary report covering: performance before/after metrics, visual polish changes, audio polish changes, test results, and release readiness assessment.

For Product, include: performance/reliability metrics, API/CLI/web/data ergonomics
changes, docs and error-message updates, observability/deployment readiness,
test evidence, validation notes, and release readiness assessment.

## Next Steps

- If READY FOR RELEASE: run `/release-checklist` for the final pre-release validation.
- If NEEDS MORE WORK: schedule remaining issues in `/sprint-plan update` and re-run `/team-polish` after fixes.
- Run `/gate-check` for a formal phase gate verdict before handing off to release.
- Product: run `/content-audit` after docs/help/schema changes.
- Product: run `/security-audit` for auth, secrets, dependency, or data-handling risks.
- Product: run `/team-release` if deployment, migration, rollback, or package artifacts changed.
