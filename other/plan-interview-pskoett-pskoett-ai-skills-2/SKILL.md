---
name: plan-interview
description: 'Ensures alignment between user and Claude during feature/spec planning through a structured interview process.


  Use this skill when the user invokes /plan-interview before implementing a new feature, refactoring, or any non-trivial implementation task. The skill runs an upfront interview to gather requirements across technical constraints, scope boundaries, risk tolerance, and success criteria before any codebase exploration.


  Do NOT use this skill for: pure research/exploration tasks, simple bug fixes, or when the user just wants standard planning without the interview process.'
---

# Plan Interview Skill

## Install

```bash
gh skill install pskoett/pskoett-skills plan-interview
```

Fallback using the Agent Skills CLI:

```bash
npx skills add pskoett/pskoett-skills/skills/plan-interview
```

## Philosophy

Every skill in this collection is built around a core philosophy — a principle that agents struggle to internalize on their own.

This skill's philosophy: **"Make the change easy, then make the change."**

Agents default to plowing straight through implementation, no matter how tangled the path. They rarely pause to ask: "Would a preparatory refactor make this change simple instead of hard?" Planning is where that question gets asked. During codebase exploration and plan generation, actively look for structural friction — code that makes the target change awkward, brittle, or overly complex. When you find it, the plan should propose a preparatory step: make the change easy first, then make the change itself. Two clean steps beat one heroic slog.

## Purpose

Run a structured requirements interview before planning implementation. This ensures alignment between you and the user by gathering explicit requirements rather than making assumptions.

## When Invoked

User calls `/plan-interview <task description>`.

**Skip this skill** if the task is purely research/exploration (not implementation).

## Interview Process

### Phase 1: Upfront Interview (Before Exploration)

Check for the host's structured question tool (`ask_user`,
`AskUserQuestion`, or an equivalent). Use it for focused questions that the
user can answer before the next planning step. In hosts without a structured
question tool, ask the same question directly in chat and pause for the
response. Do not fall back to plain chat merely because the host uses a
different tool name. Respect the host schema: if the tool accepts only one
question per call, ask the domains sequentially rather than bundling them.

#### Required Question Domains

Cover ALL four domains before proceeding:

1. **Technical Constraints**
   - Performance requirements
   - Compatibility needs
   - Existing patterns to follow
   - Architecture understanding (if codebase is unfamiliar)

2. **Scope Boundaries**
   - What's explicitly OUT of scope
   - MVP vs full vision
   - Dependencies on other work

3. **Risk Tolerance**
   - Acceptable tradeoffs (speed vs quality)
   - Tech debt tolerance
   - Breaking change acceptance

4. **Success Criteria**
   - How will we know it's done?
   - What defines "working correctly"?
   - Testing/validation requirements

#### Question Generation

- Generate questions **dynamically** based on the task - no fixed template
- Group related questions into thematic batches
- **2-3 questions per batch** (do not exceed)
- Continue until you have **actionable specificity** (can describe concrete implementation steps)

#### Planning Depth Calibration

Before leaving the interview phase, classify the task and choose a planning depth:

- **Simple/trivial** (small bug fix, isolated change): minimal plan, at most 1 refinement pass
- **Moderate** (feature work in known area): standard plan, usually 1-2 refinement passes
- **Complex/high-risk** (multi-file, new architecture, unfamiliar codebase, migrations, auth, concurrency): deep plan with iterative refinement until improvements flatten

Let the user override this (`fast` vs `deep`) if they have a clear preference.

#### Handling Edge Cases

| Scenario | Action |
|----------|--------|
| Contradictory requirements | Make a recommendation with rationale, ask for confirmation |
| User pivots requirements | Restart interview fresh with new direction |
| Interrupted session | Ask user: continue where we left off or restart? |

#### Anti-Patterns to Avoid

- Do NOT ask variations of the same question
- Do NOT make major assumptions without asking
- Do NOT over-engineer plans for simple tasks

### Phase 2: Codebase Exploration

After interview completes, explore the codebase to understand:
- Existing patterns relevant to the task
- Files that will be affected
- Integration points
- Potential risks
- **Structural friction** — Is the current code shape fighting the planned change? Would a preparatory refactor (rename, extract, restructure) make the actual implementation straightforward? If yes, propose it as a distinct first step in the plan.

For complex or unfamiliar projects, do a brief context refresh before deep planning:
- Re-read `AGENTS.md` and `README.md` if present and relevant
- Identify the current architecture boundaries and conventions before refining the plan
- If the session was interrupted or context drifted, refresh these again before another refinement round

### Knowledge Audit (Between Exploration and Planning)

Before writing the plan, explicitly ask: **"Does the knowledge needed to complete this task exist somewhere I can reach?"**

For each significant implementation step, classify where the required knowledge lives:

- **Codebase** — Existing patterns, conventions, or code that demonstrates how to do it. Found during exploration.
- **Prompt/context** — User-provided requirements, constraints, or domain knowledge from the interview.
- **Training data** — General programming knowledge, well-known libraries, standard patterns the model reliably knows.
- **Nowhere reachable** — The knowledge isn't in any of the above. The agent would be guessing.

When a step falls into "nowhere reachable":
1. **Stop and surface it.** Do not fill the gap with confident-sounding guesses.
2. Ask the user to provide the missing knowledge, point to documentation, or confirm that best-effort is acceptable.
3. If the user provides a reference (docs URL, API spec, example), load it before planning that step.
4. If the gap cannot be filled, mark the step as blocked in the plan's Open Questions section.

This audit prevents the most common agent failure: confidently proceeding when the knowledge simply isn't there, producing plausible but wrong output.

### Phase 3: Plan Generation

Write plan to `docs/plans/plan-NNN-<slug>.md` where NNN is sequential.

Use a **draft -> refine** workflow. Stay in plan space while you are still finding material improvements. Planning tokens are usually much cheaper than implementation tokens for non-trivial work.

#### Draft First, Then Refine

1. Create a draft plan from the interview + exploration results.
2. Run iterative refinement passes before asking for approval (depth based on task complexity).
3. Present the refined plan for user review.

#### Iterative Plan Refinement Loop (Before User Review)

Run 1..N refinement passes depending on complexity. For each pass:

1. **Fresh-eyes start (mandatory):** Re-read the interview answers, constraints, success criteria, and the current draft plan with "fresh eyes" before revising anything.
2. Check for contradictions, missing edge cases, integration risks, and vague implementation steps.
3. Improve architecture, sequencing, and reliability where it clearly helps users.
4. Strengthen the testing and validation plan (unit + integration/e2e where applicable, plus useful diagnostics/logging).
5. Verify feature preservation:
   - **Do NOT oversimplify**
   - **Do NOT remove agreed features or functionality** unless the user explicitly approves a scope reduction
6. Record a short per-pass summary: what changed and why.

Stop iterating when any of the following is true:
- Two consecutive passes produce no material improvements
- Changes are only wording/style with no effect on execution quality
- The task is simple and the plan is already actionable
- The user asks to stop and proceed

#### Optional: Multi-Plan Synthesis ("Best of All Worlds")

If the user provides multiple competing plans (from different models or prior iterations):

- Compare them honestly against the current plan
- Extract the best ideas, tradeoffs, and risk mitigations
- Merge them into a single canonical plan that preserves agreed scope
- Prefer showing **git-diff style changes** to the existing plan when the user asks for revision output

Reusable prompt templates for the refinement loop and multi-plan synthesis live in `references/iterative-plan-refinement-prompts.md`.

#### Required Elements

Every plan MUST include:

```markdown
## Success Criteria
[Clear definition of done from interview]

## Risk Assessment
[What could go wrong + mitigations]

## Affected Files/Areas
[Which parts of codebase will be touched]

## Test Strategy
[Unit tests, integration tests, and e2e tests/scripts where applicable; include key scenarios, failure modes, and fixtures/mocks]

## Validation and Diagnostics
[How to verify the feature works after implementation; include detailed logging/diagnostics expectations in tests/scripts when useful for debugging]

## Knowledge Map
[For each major step, where does the required knowledge live?]
| Step | Knowledge Source | Confidence |
|------|-----------------|------------|
| Step 1 | Codebase (existing pattern in src/auth/) | High |
| Step 2 | Training data (standard OAuth2 flow) | High |
| Step 3 | Nowhere — need user to provide API spec | Blocked |

## Open Questions
[Uncertainties to resolve during implementation]
- [ ] Question 1 - [Blocks implementation / Can proceed]
- [ ] Question 2 - [Blocks implementation / Can proceed]

## Implementation Checklist
- [ ] Step 1
- [ ] Step 2
...
```

#### Optional Elements

Include when relevant:

- **Rejected Alternatives**: Only for major architectural decisions
- **Decision Tree**: Only when multiple valid approaches exist
- **Visual Diagrams**: ASCII or Mermaid when helpful for understanding

#### Constraints

- **No time estimates** - describe what needs doing, not how long
- **No length limits** - plan should match task complexity
- **No silent scope reduction** - do not drop agreed features to make the plan "cleaner"
- **Don't over-iterate simple work** - use the planning depth calibration above
- Freeform structure beyond required elements

### Phase 4: Post-Approval

When user approves the plan:

1. **Auto-start implementation** immediately (no separate "proceed" confirmation needed). If `intent-framed-agent` is active, flow directly into a faithful Intent Frame and reuse the plan approval. Ask again only if the frame introduces a material change or unresolved decision.
2. Populate `TodoWrite` with checklist items (if `TodoWrite` is not available, track progress via structured comments in your output)
3. At **natural breakpoints** (significant decisions), compare progress to plan

## Fast Mode

If user wants quick planning, use **draft + refine**:

1. Perform task-focused codebase search
2. Generate draft plan
3. Run abbreviated interview to refine
4. Run exactly one **fresh-eyes** refinement pass (preserve functionality, tighten steps, add test/validation coverage)

## Resume Support

If a partial plan exists in `docs/plans/`:

```
AskUserQuestion: "I found an existing partial plan. Would you like to:"
- "Continue the interview"
- "Resume plan drafting/refinement"
- "Review current plan and finalize"
- "Start fresh with a new plan"
```

If resuming refinement, first summarize the current plan state and the most recent refinement changes, then continue with the fresh-eyes refinement loop.

## Interoperability with Other Skills

### What this skill consumes
- **From the user:** Task description, requirements, and answers to interview questions.
- **From the codebase:** Existing patterns, architecture, and conventions discovered during exploration.
- **From context-surfing handoff files (on resume):** If a previous session exited due to context drift, the handoff file in `.context-surfing/` provides the re-entry point and remaining work for replanning.

### What this skill produces
- **Plan file** (`docs/plans/plan-NNN-<slug>.md`) — consumed by intent-framed-agent as context for the intent frame, and by context-surfing as part of the wave anchor. Copied verbatim into handoff files on drift exit.
- **Planning depth classification** — informs how many skills to activate (see pipeline depth table in README).

### Pipeline position
1. `plan-interview` (requirements and plan generation — you are here)
2. `intent-framed-agent` (execution contract + scope drift monitoring)
3. `context-surfing` (optional context-quality monitoring for Large,
   Long-running, or explicitly context-sensitive execution)
4. `verify-gate` (machine verification: compile + test + lint)
5. `simplify-and-harden` (post-completion quality/security pass)
6. `self-improvement` (capture recurring patterns and promote durable rules)

## Example

```
User: /plan-interview Add OAuth authentication to the API

Claude: I'll help you plan the OAuth authentication feature. Let me gather
        requirements first.

[AskUserQuestion - Scope batch]
1. Which OAuth providers need to be supported (Google, GitHub, etc.)?
2. Is this replacing existing auth or adding alongside it?

[Copilot guidance: ask the same two questions in chat and wait for responses]

User: Google and GitHub. Adding alongside existing JWT auth.

[AskUserQuestion - Technical batch]
1. Should OAuth tokens be stored in the existing session table or separately?
2. Any specific callback URL constraints from your hosting setup?

User: Separate table. We're on Vercel so callback URLs need to be configured per environment.

[AskUserQuestion - Risk/Success batch]
1. What's the acceptable degradation if an OAuth provider is down?
2. How should we handle users who already exist with the same email?

User: Fall back to standard login. Link accounts by email if user confirms.

Claude: [Explores codebase for auth patterns, session handling, database schema]

Claude: [Writes docs/plans/plan-003-oauth-authentication.md]

        Plan created. The main decision point is whether to use Passport.js
        or implement OAuth flows directly - I've documented both approaches
        with tradeoffs. Ready to review?

User: Looks good, go with Passport.js

Claude: [Auto-starts implementation with TodoWrite tracking]
```
