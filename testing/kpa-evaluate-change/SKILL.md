---
name: kpa-evaluate-change
description: Evaluate an OpenSpec change proposal before implementation - assess product value, architectural fit, spec quality, and delivery readiness
context: fork
agent: Opus
argument-hint: "[change name]"
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Evaluate an OpenSpec change proposal before implementation. Produce a grounded recommendation on whether the change should proceed, be revised, be rethought, be deferred, or be declined.

## Scope

- Review the change artifacts and the current codebase.
- Focus on product value, architectural fit, specification quality, and delivery readiness.
- Do **not** implement fixes. Recommend artifact changes, investigation, or sequencing changes only.

**Input**: Optionally specify a change name. If omitted, use the selection rules below.

## Change Selection

1. If the user provided a change name, use it.
2. Otherwise:
   - If conversation context clearly identifies exactly one active change, use it and announce: `Using change: <name>`.
   - If not clear, run `openspec list --json`, keep only active changes that have a `proposal.md`, and use the **AskUserQuestion tool** to let the user choose.
3. Never guess between multiple plausible changes.

## Evaluation Workflow

1. **Check change status**

   Run:

   ```bash
   openspec status --change "<name>" --json
   ```

   Use the result to understand:
   - the schema in use
   - which artifacts exist
   - whether the change is only partially defined

2. **Load all relevant artifacts**

   Read all available artifacts from `openspec/changes/<name>/`:
   - `proposal.md` - the what and why
   - `design.md` - the intended approach, if present
   - `tasks.md` - the delivery plan, if present
   - delta specs in `specs/**/spec.md`

   For each delta spec, also read the baseline spec it extends in `openspec/specs/`.

   If artifacts are missing, note that as evidence. Missing artifacts do not prevent evaluation.

3. **Ground the review in the codebase**

   Read the smallest relevant set of source files, tests, and supporting docs needed to answer:
   - what behavior exists today
   - what code paths and integrations would be affected
   - whether the proposal matches existing patterns and architecture
   - whether there are hidden migration, performance, data, or testing concerns

   Do not evaluate artifacts in a vacuum.

4. **Evaluate four dimensions**

   Rate each dimension as `STRONG`, `ADEQUATE`, `WEAK`, or `UNCLEAR`.

   **A. Problem & Motivation**
   - Is the problem clearly stated and real?
   - Does it solve a genuine user need or worthwhile technical debt?
   - Is the timing right, or are there prerequisites?
   - Are simpler alternatives missing?
   - What is the cost of not doing it?

   **B. Solution Design**
   - Does the design actually solve the stated problem?
   - Is it the simplest approach likely to work?
   - Are important edge cases and failure modes addressed?
   - Does it fit the current architecture and conventions?
   - Is the scope right-sized, or is it over- or under-engineered?

   **C. Spec Quality**
   - Are requirements specific, testable, and internally consistent?
   - Are scenarios and edge cases covered?
   - Do delta specs cleanly modify or extend baseline specs?
   - Are there gaps between proposal intent and spec language?
   - Could an implementer verify completion without guessing?

   **D. Delivery Plan & Readiness**
   - Do tasks follow a sensible dependency order?
   - Is task granularity appropriate?
   - Does the plan reflect TDD expectations where applicable?
   - Are important implementation, migration, validation, or rollout tasks missing?
   - Is the proposed effort proportional to the value delivered?

5. **Classify concerns**

   Capture concerns in three buckets:
   - **Blockers**: must be resolved before implementation should start
   - **Risks**: likely sources of implementation, operational, or maintenance trouble
   - **Open Questions**: ambiguities that need answers before the plan is trustworthy

   When a dimension is `WEAK` or `UNCLEAR`, there should usually be at least one item in one of these buckets explaining why.

6. **Form a recommendation**

   Choose exactly one verdict:
   - `READY`: sound and implementable as proposed
   - `REVISE`: worthwhile, but artifacts need targeted improvements first
   - `RETHINK`: the problem may be real, but the current approach is materially wrong
   - `DEFER`: not the right time, or prerequisites are missing
   - `DECLINE`: not justified or likely to create more harm than value

## Output Format

Use this structure:

```md
## Change Evaluation: <change-name>

### Verdict
<READY | REVISE | RETHINK | DEFER | DECLINE>

### Summary
<2-4 direct sentences on the overall assessment>

### Dimension Ratings
| Dimension            | Rating   | Notes                 |
|----------------------|----------|-----------------------|
| Problem & Motivation | STRONG   | <brief justification> |
| Solution Design      | ADEQUATE | <brief justification> |
| Spec Quality         | WEAK     | <brief justification> |
| Delivery Plan        | STRONG   | <brief justification> |

### Strengths
- <specific strength>

### Concerns
**Blockers**
- None, or <specific blocker with artifact/code reference>

**Risks**
- None, or <specific risk with explanation>

**Open Questions**
- None, or <specific unanswered question>

### Recommendations
- <specific next step>
- <specific artifact or area to revise>
```

## Evaluation Standards

- **Be honest, not polite** - catching a weak proposal early is a success.
- **Be specific** - cite artifact paths, requirement/scenario names, and relevant code paths.
- **Use evidence** - each meaningful concern should be grounded in an artifact or code reference.
- **Consider alternatives** - note when a simpler or more standard approach seems better.
- **Weigh value against cost** - a correct design can still be a poor investment.
- **Prefer simplicity** - extra complexity needs a clear payoff.
- **Evaluate the actual maturity** - a small change may be fine without `design.md`; a complex change usually is not.

## Guardrails

- Read the actual codebase, not just the artifacts.
- Do **not** suggest code patches or implement fixes in this command.
- Missing artifacts are part of the evaluation; do not stop just because one is absent.
- Be willing to recommend `DECLINE`.
- Keep the evaluation actionable and concise. Avoid praise padding and vague commentary.
