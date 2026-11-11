---
name: pair-capability-assess-testing
description: "Assess testing strategy using resolution cascade (Argument > Adoption > Assessment). Reads testing guidelines, proposes framework and strategy, writes testing section of tech-stack.md, composes /pair-capability-record-decision. Idempotent."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-testing — Testing Strategy Assessment

Evaluate and decide on the testing strategy: framework, pyramid distribution, coverage targets, and TDD approach. Follows the resolution cascade: explicit argument wins, then existing adoption, then full assessment from guidelines.

## Arguments

| Argument  | Required | Description                                                                          |
| --------- | -------- | ------------------------------------------------------------------------------------ |
| `$choice` | No       | Override: skip assessment, use this testing framework directly (e.g. `vitest`, `jest`) |

## Composed Skills

| Skill              | Type       | Required                                      |
| ------------------ | ---------- | --------------------------------------------- |
| `/pair-capability-record-decision` | Capability | Yes — records testing decision as ADL or ADR  |

## Proposal Target

The rendered adoption content is destined for this section — the caller writes it via `/pair-capability-record-decision`:

- **Target**: [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — **testing section only**
- **Ownership**: Testing section (shared file — /pair-capability-assess-stack owns core sections, /pair-capability-assess-ai owns AI section)

## Adoption File

- **Target**: [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — **testing section only**
- **Ownership**: Testing section (shared file — /pair-capability-assess-stack owns core sections, /pair-capability-assess-ai owns AI section)

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Confirm the choice with the developer:

   > Testing framework override: **$choice**.
   > This will be adopted without full assessment.
   > Confirm?

4. **Check**: Does [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) already have a testing section with a different framework?
   - If yes, warn: "Current testing framework is **[existing]**. Override to **$choice**?"
5. **Verify**: Developer confirms. Proceed to Step 2.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) exist and contain a populated **Testing** section?
2. **Skip**: If no testing section or section is empty/template, go to Path C.
3. **Act**: Read current testing adoption. Present:

   > Testing strategy already adopted:
   > - Framework: **[name vX.Y]**
   > - Coverage tool: **[name vX.Y]**
   > - Additional tools: **[list]**
   >
   > Adoption is current and valid.

4. **Check**: Does a corresponding decision record exist? (Scan [adoption/decision-log/](../../../.pair/adoption/decision-log) or [adoption/tech/adr/](../../../.pair/adoption/tech/adr) for `*testing*` files.)
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Adoption and decision record consistent. Done — exit skill.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2 (full assessment mode).

### Step 2: Read Guidelines

1. **Act**: Read testing guidelines:
   - [Test Strategy README](../../../.pair/knowledge/guidelines/testing/test-strategy/README.md) — strategic framework and philosophy
   - [Test Pyramid](../../../.pair/knowledge/guidelines/testing/test-strategy/test-pyramid.md) — distribution strategy
   - [Coverage Strategy](../../../.pair/knowledge/guidelines/testing/test-strategy/coverage-strategy.md) — coverage requirements
   - [TDD](../../../.pair/knowledge/guidelines/testing/test-strategy/tdd-test-driven-development.md) — TDD practices
2. **Act**: Read project context:
   - [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — language and framework (testing tools must be compatible)
   - [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — project type and quality requirements (if available)
3. **Verify**: Guidelines and project context loaded.

### Step 3: Evaluate Options

1. **Act**: Based on adopted language/framework, identify compatible testing frameworks:
   - For TypeScript/JavaScript: Vitest, Jest, Mocha, Playwright, Cypress
   - For other stacks: framework-appropriate options

2. **Act**: Evaluate frameworks against project needs:
   - Speed and DX (developer experience)
   - Compatibility with adopted tech stack
   - Coverage tooling quality
   - Community and maintenance status
   - TypeScript support quality

3. **Act**: Present recommendation with rationale:

   > **Testing Strategy Recommendation:**
   > - **Framework**: [name] v[X.Y] — [rationale]
   > - **Coverage**: [tool] v[X.Y] — [rationale]
   > - **Additional**: [e.g. path resolution plugin] — [rationale]
   > - **Pyramid**: Unit [N%] > Integration [N%] > E2E [N%]
   > - **Coverage target**: [N%] minimum

4. **Verify**: Developer approves the strategy.

### Step 4: Write Adoption File

1. **Check**: Does [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) exist?
2. **Act**: Write or update **only the Testing section** of tech-stack.md:
   - Framework name and version
   - Coverage tool and version
   - Additional testing tools with versions
   - Preserve all other sections (core, AI, etc.) untouched
3. **Verify**: Testing section written. Other sections preserved.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - `$type`: `non-architectural` (testing framework is a tooling choice, not structural)
   - `$topic`: `testing-strategy`
   - `$summary`: "[Framework] vX.Y adopted as testing framework with [coverage target]% coverage"
2. **Verify**: ADL created at `adoption/decision-log/YYYY-MM-DD-testing-strategy.md`. Adoption file consistent with ADL.

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:    Testing
├── Path:      [Argument Override | Adoption Exists | Full Assessment]
├── Decision:  [framework vX.Y + coverage tool + pyramid distribution]
├── Adoption:  [tech-stack.md testing section — written | confirmed | updated]
├── Record:    [ADL path — created | exists | backfilled]
└── Status:    [Complete | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes `/pair-capability-assess-testing` during Phase 2. May pass `$choice` if developer pre-selected.
- **Output**: Returns decision summary and adoption file path.
- `/pair-process-bootstrap` includes adoption and ADL changes in the next commit.

When invoked **independently**:

- Full interactive flow. Developer commits changes when satisfied.

## Edge Cases

- **Argument conflicts with adoption**: Warn developer, ask for confirmation. If confirmed, update testing section and create new decision record.
- **tech-stack.md exists but no testing section**: Add testing section, preserve all other content.
- **Framework incompatible with adopted language**: HALT — warn developer of incompatibility, suggest compatible alternatives.
- **Decision record already exists for same scope+decision**: Skip writing (no duplicates).
- **Multiple valid frameworks score equally**: Present top 2 with trade-off analysis, ask developer to choose.

## Graceful Degradation

- If testing guidelines are not found, use minimal assessment: ask developer for framework preference based on language.
- If `/pair-capability-record-decision` is not installed, warn and skip decision recording.
- If tech-stack.md doesn't exist, create it with testing section as initial content. Warn: "Created tech-stack.md — other sections should be populated by /pair-capability-assess-stack."

## Notes

- Testing decisions are typically **non-architectural** → produce ADL. Exception: if the testing strategy choice affects system structure (e.g. choosing contract testing that requires service boundaries), use ADR instead.
- **Section ownership**: this skill writes ONLY the Testing section of tech-stack.md. /pair-capability-assess-stack owns core sections, /pair-capability-assess-ai owns AI section.
- Version tracking: every testing tool includes specific version.
- The resolution cascade IS the idempotency mechanism: if testing section is populated, assessment is already done.
- Educational content (testing philosophy, principles, WHY) stays in guidelines. This skill references guidelines for framework comparison and strategy decisions.
