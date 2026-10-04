---
name: team-polish
description: "Use when a feature or area needs coordinated performance, visual, audio, and QA hardening."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

# Team Polish

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Invocation

Usage: `$codex-game-studios:team-polish [feature or area] [--review full|lean|solo]`. If the required objective cannot be inferred safely, ask for that single missing decision and wait; do not delegate yet.

## Review Mode

Read `.codex/studio.toml` as the only persistent review-mode source. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. A `--review` argument applies only to the current run. Use `../../../.codex/docs/director-gates.md` and `.codex/docs/technical-preferences.md` for native gate and engine context.

## Team Roster

- `performance-analyst`
- `technical-artist`
- `sound-designer`
- `qa-tester`

## Delegation Plan

- Delegate only tasks that are independent and bounded.
- Name the Codex custom-agent role and the exact artifact or evidence it must return.
- Team members must not spawn additional agents (`agents.max_depth = 1`).
- The parent agent synthesizes all results, resolves overlap, and communicates with the user.
- No subagent commits, publishes, or expands scope.
- Parallel delegation is read-only or draft-only until the parent presents a consolidated result.
- Any multi-file implementation requires one complete changeset approval before work begins.
- If a delegated task blocks, surface the evidence and stop dependent work while preserving independent results.

## Pipeline

Every phase before `## Parent Changeset Gate` is read-only or draft-only. Phase 1 profiles and returns evidence; it makes no source, asset, test, report, or session change.

### Phase 1: Assessment
Delegate to **performance-analyst**:
- Profile the target feature/area using `$codex-game-studios:perf-profile`
- Identify performance bottlenecks and frame budget violations
- Measure memory usage and check for leaks
- Benchmark against target hardware specs
- Output: performance report with prioritized optimization list

## Parent Changeset Gate

The parent synthesizes the performance evidence and every proposed polish change before any mutation. Present one complete proposal containing exact file paths, exact diffs, tests and evidence, and all session-state, report, and milestone writes (use `None` where no such write exists). Obtain approval for the whole changeset; a new path or material change requires a revised proposal.

## Approved Execution

Only after approval may the parent execute or delegate the exact approved changes. No subagent commits, publishes, or expands scope. Every delegate receives only its approved paths, diffs, tests, and acceptance criteria.

### Phase 2: Optimization
Delegate to **performance-analyst** to review the approved diffs, define before/after measurements, and validate results. This role recommends and measures; it does not implement optimizations.

Delegate approved rendering, shader, VFX, asset-pipeline, and visual resource changes to **technical-artist**:
- Apply only the exact approved technical-art diffs
- Optimize draw calls, overdraw, visual resource loading, and asset memory within that role's boundary
- Return the changed-file list plus profiler evidence

For gameplay, AI, networking, core-engine, or other code bottlenecks outside the four-role roster, return a bounded `$codex-game-studios:dev-story` handoff with exact recommended paths and acceptance metrics. Do not implement those changes in `$codex-game-studios:team-polish`.

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

## Error Recovery Protocol

If any delegated agent (through Codex custom-agent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via request_user_input with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$codex-game-studios:architecture-decision` first
- Scope too large → split into two stories via `$codex-game-studios:create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## Output

A summary report covering: performance before/after metrics, visual polish changes, audio polish changes, test results, and release readiness assessment.

## Next Steps

- If READY FOR RELEASE: run `$codex-game-studios:release-checklist` for the final pre-release validation.
- If NEEDS MORE WORK: schedule remaining issues in `$codex-game-studios:sprint-plan update` and re-run `$codex-game-studios:team-polish` after fixes.
- Run `$codex-game-studios:gate-check` for a formal phase gate verdict before handing off to release.
