---
name: sdlc-requirements
description: Analyze and interrogate requirements for a TriStar feature. Asks structured questions across engineering and loyalty-domain categories before producing a validated problem specification.
allowed-tools: Read, Grep, Glob, Write, Bash, AskUserQuestion
---

# SDLC Requirements Skill

## Prime Directive

**"Ask 10 questions before you write 1 requirement."**

Never produce a problem_spec.md without first interrogating the feature request across all mandatory categories. Requirements are discovered through structured dialogue, not assumed from a feature name.

## Arguments

- `--feature=<name>` (required) - Feature name used for artifact paths and identification

## Process

### Step 1: Parse Feature Name

Extract the feature name from the `--feature` argument. This becomes the artifact directory name and document title.

```
Feature: <name>
Artifact path: docs/artifacts/<name>/problem_spec.md
```

### Step 2: Read Feature Request

Check if a feature request document exists:

1. Look for `docs/artifacts/<feature>/feature_request.md`
2. Look for any related files in `docs/artifacts/<feature>/`
3. If nothing exists, ask the user to describe the feature

Read `docs/ARCHITECTURE.md` and `.claude/CLAUDE.md` for project context.

### Step 3: Initial Assessment

Before asking questions, form an initial assessment:

- Which TriStar layers (Designer, Hub, Scout) are likely affected?
- Which OfferBrief fields might be involved?
- What Hub state transitions might be impacted?
- Are there obvious security or PII concerns?

Do NOT share this assessment yet. It informs your interrogation strategy.

### Step 4: Interrogation Phase (Round 1)

Use `AskUserQuestion` to ask questions. Present questions as multiple-choice where possible to reduce friction.

Cover ALL 6 mandatory categories in the first round. Ask 2-3 questions per category, batched by theme.

**Format each question as:**
```
Category: <category name>

Q1: <question>
  a) <option>
  b) <option>
  c) <option>
  d) Other (please specify)
```

### Step 5: Continue Interrogation (Rounds 2-3)

Based on answers from Round 1:

- Drill deeper into areas with ambiguity
- Cover recommended categories relevant to the feature
- Identify contradictions or gaps in answers
- Confirm assumptions explicitly

Maximum 3 interrogation rounds. If ambiguity remains after 3 rounds, document it as an assumption with `risk_if_wrong` level.

### Step 6: Present Draft Plan for Approval

Before writing the final spec, present a draft plan to the user using the template from `references/draft-plan-template.md`.

**Wait for explicit approval.** The user must reply with "approved" or equivalent before proceeding. If they request changes, incorporate feedback and re-present.

### Step 7: Produce problem_spec.md

Only after approval, write the final specification to:

```
docs/artifacts/<feature>/problem_spec.md
```

Validate against all quality gates in `references/quality-gates.md` before saving.

## Mandatory Categories (Must Cover)

1. **Scope & Layers** - Which of Designer (Layer 1), Hub (Layer 2), Scout (Layer 3) are affected? What features within each layer?
2. **Error States & Handling** - What can fail? Claude API timeouts, weather API downtime, invalid context signals, fraud detection blocks, Hub state conflicts.
3. **Security & Compliance** - PII handling (member_id only in logs), input validation (Zod + Pydantic), authentication requirements, OWASP concerns.
4. **Performance & Constraints** - API response targets (p95 <200ms), activation latency (<500ms), frontend FCP (<2s), caching strategy.
5. **Feature Flags & Rollout** - Environment-based rollout strategy, A/B testing for offer targeting, gradual activation.
6. **Backward Compatibility** - Impact on existing Hub states, API versioning, OfferBrief schema changes, data migration.

## Recommended Categories (Cover When Relevant)

- **Authentication** - JWT token handling, protected routes, role-based access
- **Loading States** - Suspense boundaries, optimistic updates (useOptimistic), streaming
- **Data Model** - OfferBrief schema changes, new Pydantic models, Zod schemas
- **Observability** - Structured logging (loguru), metrics, audit trail for Hub state changes
- **Accessibility** - ARIA labels, keyboard navigation, semantic HTML
- **Integration Points** - Designer->Hub->Scout flow, Claude API, Weather API, Redis
- **Testing Strategy** - Unit (Jest/pytest), integration (httpx), E2E (Playwright), coverage targets

## Iron Laws

1. **NEVER write problem_spec.md without explicit user approval** of the draft plan
2. **NEVER assume layer scope** - always ask which of Designer/Hub/Scout are affected
3. **Maximum 3 interrogation rounds** - after that, document remaining unknowns as assumptions
4. **NEVER skip mandatory categories** - all 6 must be addressed even if briefly
5. **NEVER include implementation details** - requirements describe WHAT, not HOW
6. **ALWAYS validate against quality gates** before saving the final document

## Output

Final artifact saved to: `docs/artifacts/<feature>/problem_spec.md`

## Reference Files

- `references/interrogation-questions.md` - Full question bank by category
- `references/interrogation-rules.md` - Rules governing the interrogation phase
- `references/draft-plan-template.md` - Template for draft plan presentation
- `references/quality-gates.md` - Validation criteria before saving
