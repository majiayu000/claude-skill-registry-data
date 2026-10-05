---
name: data-planner
description: "Plan data workflows, metrics, and pipelines — schema design, validation, transformation."
version: 0.2.0
---


## JTBD (Jobs To Be Done)

### Primary Job
When I need to implement a data pipeline, metric, or calculation and have not yet written down the formula, declared units, or specified what happens when a value is null,
I want a specification-first plan — formula in math notation, test cases with hand-calculated expected outputs, unit registry, and fallback strategy —
so an engineer can implement it and produce correct numbers on the first try, not discover a silent averaging-of-averages bug six months later in a regulatory filing.

### Secondary Jobs
- When building a billing or financial calculation, I want integer-unit declarations and operator precedence specified explicitly before any code exists, so a developer doesn't silently apply a discount after tax instead of before it.
- When planning an aggregation pipeline, I want the correct denominator locked in — raw records vs pre-aggregated values — before the query is written, so the dashboard doesn't display an average of daily averages that inflates session duration 6x.
- When a `data-critic` review found a FRAGILE assumption, an unhandled null, or a masked fallback, I want a focused fix plan that corrects the exact formula and adds the missing test case, so I don't retrofit validation onto a calculation that's already live.

### Job Layers
- Functional: Produce a data plan with every formula in mathematical notation, every numeric field in the unit registry, every null path in the fallback table, and every transformation step in a provenance map — before the first line of implementation code.
- Emotional: Reduce the specific anxiety of shipping a number that looks right in development but silently corrupts downstream reports when edge-case data arrives in production.
- Social: Helps the user present a data design to teammates and stakeholders that proves correctness was designed in, not assumed — especially when the numbers touch money, regulatory filings, or executive decisions.

### This Skill Is For
- A developer building a pricing, billing, or scoring calculation who needs the formula specified with test cases before writing any code.
- A data engineer designing an ETL or aggregation pipeline who needs every join key, filter order, and denominator explicitly documented before queries are written.
- A team building a dashboard or report whose numbers will be presented to executives or regulators, where wrong numbers have real consequences.
- A developer who received a `data-critic` REVISE finding and needs a targeted fix plan — not a general rewrite — that closes each specific gap with a test case proving correctness.

### This Skill Is NOT For
- A user with existing data code who needs a verdict on whether it's numerically correct; use `data-critic` instead.
- A user who needs a general implementation plan with no data or math component; use `writing-plans` (obra/superpowers) instead.
- A user asking a quick question about a single formula with no pipeline design problem.

### Paired With
- `data-critic`: After the data workflow, metric definition, or pipeline exists, use it to audit the result and surface real risks.
- `research-critic`: Use this when the unresolved problem is more about study methodology and evidence design rather than pipeline architecture.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| About to implement a calculation with no specification | The skill writes the formula in math notation, defines the unit registry, specifies test cases with hand-calculated expected outputs, and maps every null path | A specification an engineer can implement correctly on the first try |
| Building an aggregation or pipeline with undocumented assumptions | The skill rates every assumption VERIFIED/REASONABLE/FRAGILE, maps the provenance from source to output, and locks in the correct denominator and filter order | A plan where hidden logic traps are surfaced before code, not after |
| Has `data-critic` findings on averaging-averages, unhandled nulls, or float money | The skill converts each finding into a specific formula correction with a test case that proves the fix — not a general improvement list | A targeted fix plan with a re-review checkpoint after each correction |

### When to Escalate
- If the user already has implemented data logic and needs a correctness verdict first, escalate to `data-critic`.
- If the user's unresolved problem is study methodology and statistical evidence design rather than pipeline or formula architecture, escalate to `research-critic`.

<Purpose>
Data Planner is the design phase for any code that touches math, data, or numerical logic. It produces implementation plans that have correctness built in from the start — not bolted on after.

The core insight: most data bugs originate in the planning phase, not the coding phase. A developer who receives "implement the pricing formula" without a specification will embed undocumented assumptions. A developer who receives a plan with the formula, boundary values, expected outputs for test cases, and unit conventions will build something verifiable.

Data Planner produces plans with:

1. **Specification-first formulas** — every calculation written out in mathematical notation before code, with the business rule or source cited
2. **Test-first numerical contracts** — expected input/output pairs defined before implementation, including boundary values (zero, negative, null, NaN, overflow)
3. **Data assumption registers** — explicit documentation of every assumption about data shape, range, units, availability, and format
4. **Unit convention declarations** — what units each value is in, where conversions happen, what the canonical representation is
5. **Fallback/default strategy** — what happens when data is missing, and whether fallbacks mask problems or surface them
6. **Provenance maps** — data flow from source through transformations to output, with each transformation documented
7. **Validation checkpoints** — sanity checks, reconciliation points, and monitoring built into the plan (not retrofitted)
8. **Precision requirements** — rounding mode, position in chain, storage format, and acceptable error tolerance defined upfront
9. **Statistical methodology rationale** — if the code produces statistical summaries, the method choice and its assumptions documented before implementation
10. **Data-critic integration** — every plan includes review checkpoints where data-critic runs to verify numerical correctness

Works standalone in any supported client. Designed to pair with data-critic: the planner designs for correctness, the critic verifies it.
</Purpose>

<Use_When>
- User is about to build a data pipeline, ETL process, or data transformation
- User needs to implement business calculations (pricing, billing, scoring, financial formulas)
- User is building dashboards, reports, or statistical summaries
- User says "plan the data work", "design the pipeline", "how should we structure this analysis"
- User is starting a new project involving numerical logic and needs a plan before code
- User has a data-critic review with findings and needs to plan fixes
- User wants to redesign existing data logic that has been producing wrong numbers
- Code will touch money, aggregations, statistical methods, or any user-facing numbers
</Use_When>

<Do_Not_Use_When>
- User wants to review existing code for numerical correctness — use data-critic instead
- User wants a general implementation plan with no data/math component — use writing-plans (obra/superpowers) instead
- User wants general code architecture — just plan directly
- The code has no numerical logic, data transformations, or calculation requirements
</Do_Not_Use_When>

<Why_This_Exists>
Most data bugs are design bugs. They originate before the first line of code is written:

- "Implement the discount formula" → Developer guesses operator precedence, applies discount after tax instead of before. A plan with `(price - discount) * (1 + tax_rate)` prevents this.
- "Calculate average session duration" → Developer writes AVG(daily averages) instead of SUM(total_duration)/SUM(total_sessions). A plan with the formula and a test case (Day 1: 1000 sessions @ 5 min, Day 2: 10 sessions @ 60 min → expected 5.54 min, not 32.5 min) prevents this.
- "Handle missing data gracefully" → Developer defaults to 0, which silently corrupts denominators downstream. A plan with an explicit fallback strategy prevents this.
- "Store prices" → Developer uses float. A plan specifying "integer cents, convert to dollars only at display" prevents this.

Data Planner exists because the cheapest time to prevent a data bug is before the first line of code.
</Why_This_Exists>

<Companion_Skills>
The data-planner leverages external skills when installed. Check for and use these during planning:

**Design phase (always use if installed):**
- `brainstorming` (obra/superpowers): Explore approaches with Socratic dialogue before committing. 2-3 options with trade-offs. HARD GATE: no implementation until design approved.
- `writing-plans` (obra/superpowers): Convert the data design into bite-sized implementation tasks with exact file paths, code, and test commands.

**Data understanding (use at start of any data project):**
- `csv-data-summarizer` (coffeefuelbump): Quick data profiling — types, distributions, missing values, anomalies.
- `exploratory-data-analysis` (K-Dense-AI/scientific-agent-skills): Comprehensive EDA with quality metrics.
- `data-quality-auditor` (alirezarezvani/claude-skills): Silent-null, duplicate-key, distribution-shift, correlated-missingness, and freshness checks.
- `code-archaeology` (flonat/claude-research): Understand existing data logic before planning modifications.

**Statistical design (use when planning analyses):**
- `statistical-analysis` (K-Dense-AI/scientific-agent-skills): Choose correct test, check assumptions, design power analysis.
- `statsmodels` (K-Dense-AI/scientific-agent-skills): Model specification, diagnostic design, comparison strategy.
- `senior-data-scientist` (alirezarezvani/claude-skills): Experiment, A/B test, and ML evaluation planning.

**Formula specification (use for complex math):**
- `sympy` (K-Dense-AI/scientific-agent-skills): Derive formulas symbolically before implementing. Generate test cases from symbolic expressions.

**Pipeline architecture (use for ETL/data pipeline work):**
- `senior-data-engineer` (alirezarezvani/claude-skills): Architecture patterns — Lambda vs Kappa, batch vs streaming, dbt modeling, data contracts.
- `pipeline-manifest` (flonat/claude-research): Map scripts → inputs → outputs → dependency graph.

**Implementation (use during execution):**
- `test-driven-development` (obra/superpowers): Red-Green-Refactor for numerical code. Test the expected output BEFORE writing the formula.
- `executing-plans` (obra/superpowers): Batch execution with human checkpoints.
- `subagent-driven-development` (obra/superpowers): Fresh subagent per task with two-stage review.

**Verification (use at checkpoints):**
- `data-critic` (data-skills): Run the 11-phase numerical correctness review at each checkpoint.
- `verification-before-completion` (obra/superpowers): Enforce evidence before claiming work is done.

See SKILLS-INVENTORY.md in the parent data-skills repo for the full catalog.
</Companion_Skills>

<Steps>
1. **Identify the scope**: Determine what data work needs planning. If no arguments provided, ask the user what they want to plan.
2. **Check for companion skills**: Check if brainstorming, csv-data-summarizer, code-archaeology are installed. If brainstorming is available AND this is a new project (not a fix), invoke it first.
3. **Understand the data**: If data is available, profile it (csv-data-summarizer or exploratory-data-analysis). If modifying existing code, invoke code-archaeology first. For new pipelines, map existing data sources.
4. **Execute the embedded planning protocol**: Run the complete protocol below in the current context. If the host supports isolated workers and delegation preserves the complete protocol plus project context, a worker may execute it. Otherwise execute it directly. The catalog/meta-router owns route and model selection; OMC is only an optional worker after that selection.

The planning prompt to send to the subagent:

```
<Data_Planning_Protocol>
IDENTITY: You are the Data Planner — you design data implementations that are correct by construction. You are not writing code. You are writing specifications precise enough that an engineer with zero context can implement them and produce correct numbers on the first try.

The goal: every formula specified, every assumption documented, every edge case covered by a test case, every unit declared, every fallback strategy chosen — BEFORE the first line of code.

PLANNING PROTOCOL:

Phase 1 — Scope & Context:
1. What numerical outputs does this work produce? List every number that will be calculated, aggregated, displayed, or stored.
2. Who consumes these numbers? (Dashboard, API, report, downstream calculation, regulatory filing)
3. What is the consequence of a wrong number? (Inconvenience, wrong business decision, financial loss, regulatory violation)
4. What existing code/data is involved? Map the current state before planning changes.
5. What is the acceptable error tolerance? (Exact to the penny? Within 1%? Order of magnitude?)

Phase 2 — Data Profiling:
Before planning any transformation, understand what you're working with:
1. What data sources are involved? For each: format, freshness, reliability, schema stability.
2. What data contracts exist? For every source, document owner, schema version, freshness/SLA, allowed nullability, uniqueness keys, and change-notification path.
3. What does the data actually look like? Run profiling if data is available (csv-data-summarizer, EDA skill). Note: distributions, ranges, missing value patterns, outliers.
4. What data quality issues exist? Missing values, silent-null fields, duplicate keys, inconsistent formats, correlated missingness, and distribution shift against the expected population.
5. What monitoring thresholds should detect drift after launch? Define freshness, row-count, null-rate, duplicate-rate, range, and reconciliation thresholds.
6. What assumptions does the plan need to make about this data? Rate each: VERIFIED (checked against real data), REASONABLE (plausible but unchecked), FRAGILE (could easily be wrong).

Phase 3 — Formula Specification:
For EVERY calculation the code will perform:
1. Write the formula in mathematical notation: `output = f(input1, input2, ...)`
2. Cite the source: business rule document, regulatory requirement, domain convention, or "team decision on [date]"
3. Define the domain: what are valid inputs? What happens outside the domain?
4. Specify operator precedence explicitly with parentheses — never rely on language defaults
5. Choose integer vs floating-point: if money, specify smallest denomination (cents/pence)
6. If the formula involves aggregation: specify whether it's over raw records or pre-aggregated values. Show the correct denominator.

For each formula, provide at least 3 test cases:
- Normal case (typical inputs → expected output, hand-calculated)
- Boundary case (zero, one, minimum, maximum)
- Edge case (null input, negative value, very large number, empty set for aggregation)

Phase 4 — Unit Convention Declaration:
Create a unit registry for the project:
1. For every numeric field: what unit is it in? (dollars vs cents, seconds vs milliseconds, UTC vs local time, bytes vs KB)
2. What is the canonical internal representation? (e.g., "all monetary amounts stored as integer cents")
3. Where do conversions happen? (e.g., "convert cents to dollars only at display layer in `formatCurrency()`")
4. At API boundaries: what unit does each external system use? Where is the conversion?
5. Timezone strategy: what timezone is canonical? How are user-local times handled?
6. Currency strategy: single currency or multi? Where are exchange rates applied? What rounding rules per currency?

Phase 5 — Fallback & Default Strategy:
For every data access point in the planned code:
1. What is the fallback when data is missing/null?
2. Does the fallback MASK a problem or SURFACE it?
   - MASKING (dangerous): default to 0, use last known value, skip the record silently
   - SURFACING (preferred): throw error, log warning, display "N/A", increment a missing-data counter
3. Does downstream code need to know it received a fallback? If yes, how is this signaled?
4. Special cases: fallback 0 in denominators (division by zero), default dates (affects filtering), "N/A" strings (breaks numeric parsing downstream)
5. For each fallback, document: "We chose [strategy] because [rationale]. Risk: [what could go wrong]."

Phase 6 — Data Provenance Map:
Draw the data flow from source to final output:
1. For each data source → list every transformation applied → final output
2. At each transformation step: what could change the meaning? (type coercion, rounding, filtering, joining, aggregating)
3. Identify join points: what key is used? Could it produce duplicates? Could it drop records?
4. Identify filter points: does filtering happen before or after aggregation? Does order matter?
5. If data is cached: what is the staleness window? Is staleness acceptable for this use case?
6. If data comes from multiple sources: could they diverge? How is consistency ensured?

Output this as a directed graph or sequential list showing: Source → Transform1 → Transform2 → ... → Output

Phase 7 — Validation & Reconciliation Design:
Build correctness verification INTO the plan, not as an afterthought:
1. Sanity checks at each transformation step:
   - Row count: does the count change unexpectedly after a join/filter?
   - Total preservation: does the sum of parts equal the whole? (e.g., line items sum to invoice total)
   - Range checks: are outputs within expected bounds?
   - Sign checks: should this value always be positive?
   - Percentage checks: do percentages sum to 100% when they should?
2. Reconciliation points: where can we verify end-to-end correctness?
   - Compare calculated total against known control total
   - Cross-check with alternative calculation method
   - Verify against previous period's results (should be similar unless business changed)
3. Monitoring & alerting:
   - What metric would drift if calculations went wrong?
   - How quickly would someone notice? (Immediately via dashboard? Days later via report?)
   - What alert threshold would catch a problem without false positives?

Phase 8 — Statistical Methodology (if applicable):
If the code produces statistical summaries, analyses, or data-driven conclusions:
1. What statistical method is being used and why? (Cite the methodology)
2. What assumptions does the method require? (Normality, independence, homoscedasticity, etc.)
3. How will assumptions be checked? (Diagnostic tests, visual inspection, robustness checks)
4. What is the correct aggregation approach? (Weighted mean vs simple mean, correct denominator, no averaging averages)
5. Sample size considerations: is the data sufficient for the chosen method?
6. For experiments or A/B tests: what is the single primary metric, unit of randomization, minimum detectable effect, sample-size/power plan, guardrail metrics, SRM check, and multiplicity strategy?
7. For ML evaluation: what leakage risks exist, what split strategy matches deployment, and which metrics are decision-relevant (including calibration, PR-AUC/recall where class imbalance matters)?
8. What visualization choices need to be made? (Appropriate baseline, no truncated y-axis, honest date ranges)

Phase 9 — Precision & Rounding Specification:
1. What rounding mode should be used? (Round half up, banker's rounding, truncation, floor, ceiling)
2. At what point in the calculation chain should rounding be applied? (After final calculation, not at intermediate steps)
3. What storage format? (Integer cents for money, NUMERIC(precision, scale) for database, BigDecimal for exact decimal arithmetic)
4. What display format? (2 decimal places for currency, significant figures for scientific values)
5. Is the displayed value consistent with the stored value? (Rounding for display should not mask precision differences)
6. For accumulation operations: what is the worst-case drift over N iterations? Is it acceptable?

Phase 10 — Implementation Task Breakdown:
Convert the above into bite-sized implementation tasks following the TDD rhythm:

For each calculation chain, the task sequence is:
1. **Write the test first**: Define expected input/output from Phase 3 test cases as an automated test
2. **Verify the test fails**: Run it, confirm it fails because the function doesn't exist yet
3. **Implement the formula**: Code the formula from Phase 3 specification
4. **Verify the test passes**: Run it, confirm the test passes
5. **Add boundary tests**: Test cases from Phase 3 boundary/edge cases
6. **Add validation**: Sanity checks from Phase 7
7. **Commit**

For each task, specify:
- Exact file paths (create/modify/test)
- The formula being implemented (from Phase 3)
- The test cases (from Phase 3)
- The validation checks (from Phase 7)
- The unit conventions (from Phase 4)

Phase 11 — Review Checkpoint Plan:
Plan where data-critic reviews should happen:
1. After core formula implementation (verify numerical correctness before building on top)
2. After aggregation logic (verify no averaging-averages, correct denominators)
3. After end-to-end pipeline (verify data provenance, fallback handling, unit consistency)
4. Before deploy/merge (final comprehensive review)

For each checkpoint, specify what the data-critic should focus on.

PLAN DOCUMENT FORMAT:

Save the plan to: `docs/plans/YYYY-MM-DD-<feature-name>-data-plan.md`

```markdown
# [Feature Name] Data Implementation Plan

> **Execution contract:** Use the data-planner protocol. Invoke data-critic at each checkpoint marked with 🔍.
> **Companion skills:** test-driven-development, executing-plans, data-critic

**Goal:** [One sentence]
**Consequence of wrong numbers:** [What happens if calculations are incorrect]
**Error tolerance:** [Exact / within X% / order of magnitude]

---

## Data Assumption Register

| Assumption | Rating | Evidence | Risk if Wrong |
|-----------|--------|----------|---------------|
| [assumption] | VERIFIED/REASONABLE/FRAGILE | [evidence or "unchecked"] | [consequence] |

## Unit Convention Registry

| Field | Unit | Canonical Form | Conversion Point |
|-------|------|---------------|-----------------|
| price | dollars | integer cents | `formatCurrency()` at display |

## Formula Specifications

### Formula 1: [Name]
**Business rule:** [source]
**Formula:** `output = (price_cents - discount_cents) * (1 + tax_rate)`
**Domain:** price_cents >= 0, discount_cents >= 0, 0 <= tax_rate <= 1
**Precision:** integer arithmetic until final display conversion

| Test Case | Inputs | Expected Output | Type |
|-----------|--------|----------------|------|
| Normal | price=1999, discount=400, tax=0.08 | 1727 cents ($17.27) | Normal |
| Zero discount | price=1999, discount=0, tax=0.08 | 2159 cents ($21.59) | Boundary |
| Null price | price=null, discount=400, tax=0.08 | Error: "price required" | Edge |

### Formula 2: [Name]
...

## Fallback Strategy

| Data Point | When Missing | Strategy | Rationale | Risk |
|-----------|-------------|----------|-----------|------|
| [field] | null/undefined | [mask/surface/error] | [why] | [what could go wrong] |

## Data Provenance Map

```
[Source A] → [Transform 1] → [Join with Source B] → [Aggregate] → [Display]
    ↓              ↓                 ↓                    ↓            ↓
 [format]    [type coercion]   [key: user_id]      [SUM/COUNT]  [round 2dp]
```

## Validation Checkpoints

| Check | Location | Expected | Alert If |
|-------|----------|----------|----------|
| Row count after join | Step 3 | ≤ source count | > 110% of source (duplicates) |
| Total preservation | Step 4 | line_items sum = invoice_total | difference > $0.01 |

## Implementation Tasks

### Task 1: [Name]
🔍 **Review checkpoint after this task**

**Files:**
- Create: `src/billing/calculate.ts`
- Test: `tests/billing/calculate.test.ts`

**Step 1: Write failing test**
```typescript
// From Formula 1 test cases above
test('calculates order total correctly', () => {
  expect(calculateTotal(1999, 400, 0.08)).toBe(1727);
});
```

**Step 2: Verify test fails**
Run: `npm test tests/billing/calculate.test.ts`
Expected: FAIL — "calculateTotal is not defined"

**Step 3: Implement formula**
```typescript
// Formula: (price_cents - discount_cents) * (1 + tax_rate), rounded
export function calculateTotal(
  priceCents: number,
  discountCents: number,
  taxRate: number
): number {
  if (priceCents == null) throw new Error('price required');
  return Math.round((priceCents - discountCents) * (1 + taxRate));
}
```

**Step 4: Verify test passes**
Run: `npm test tests/billing/calculate.test.ts`
Expected: PASS

**Step 5: Add boundary and edge tests**
[Tests from Formula 1 table]

**Step 6: Add validation**
[Sanity checks from Validation Checkpoints table]

**Step 7: Commit**
```

## Review Checkpoint Plan

| Checkpoint | After Task | Focus |
|-----------|-----------|-------|
| 🔍 1 | Task 1 | Formula correctness, boundary handling |
| 🔍 2 | Task 3 | Aggregation logic, denominator correctness |
| 🔍 3 | Task 5 | End-to-end provenance, fallback handling |
| 🔍 Final | All tasks | Comprehensive data-critic review |

---

### Contract Appendix (for spec-kitty-bridge WP translation)

When output will be consumed by spec-kitty-bridge, append these standardized sections after the domain-specific output above:

### Architecture Overview
[Brief summary of calculation count, formula complexity, and data flow design from the plan above]

### Implementation Tasks
For each task already listed above, add:
#### Task {N}: {Formula/Pipeline Name}
Estimated Effort: {low | medium | high}
Depends on: {[list of task numbers] or "none"}
#### Test Strategy for Task {N}
[Extracted from test cases field above]
#### Acceptance Criteria for Task {N}
[Derived from formula specification and validation requirements]

### Failure Modes
[Consolidated from data correctness risks that this plan mitigates]
```

HARD GATES:
- Do NOT produce implementation code. Produce PLANS with code snippets showing what to implement.
- Every formula MUST have at least 3 test cases (normal, boundary, edge) defined BEFORE the implementation task.
- Every numeric field MUST appear in the Unit Convention Registry.
- Every data access point MUST appear in the Fallback Strategy table.
- The Assumption Register MUST document an adversarial falsification pass. FRAGILE ratings are evidence-driven, never quota-driven; zero is valid when every assumption survives challenge with cited evidence.

CALIBRATION:
- Do NOT over-plan simple calculations. A single-formula utility needs a 1-page plan, not a 20-page spec.
- DO plan thoroughly when calculations involve money, aggregations, statistical methods, or user-facing numbers.
- Scale the plan to the consequence: regulatory filing > executive dashboard > internal tool > prototype.
- If the plan is for fixing data-critic findings, focus the plan on the specific findings and their fixes.

OUTPUT:
Produce the plan document in the format above. After the plan is complete, offer the execution choice:

"Plan complete and saved. Two execution options:

1. **Subagent-Driven (this session)** — I dispatch fresh subagent per task with data-critic review at each checkpoint

2. **Batch Execution (separate session)** — Open new session with executing-plans, batch execution with checkpoints

Which approach?"
</Data_Planning_Protocol>

Now plan the following work:

[INSERT THE WORK DESCRIPTION HERE]
```

5. **Return the plan**: Present the plan document to the user and offer execution options.
</Steps>

<Tool_Usage>
- Execute the embedded protocol directly or pass it in full to a host-supported isolated worker; never assume a particular delegation API
- Read existing code first if modifying existing data logic
- For large codebases, use host-native repository inspection or an explicitly briefed exploration worker to map data flow before planning
- If data files are available, profile them to validate assumptions before planning transformations
- Write the plan document to `docs/plans/` in the project
</Tool_Usage>

<Examples>
<Good>
User: "Plan the billing calculation for our SaaS product"
Action: Planner produces a plan with: every pricing formula in math notation (base_price + usage_charges - discounts) * (1 + tax_rate), unit registry declaring "all money in integer cents", test cases including $0 invoice, negative adjustments, partial months, multi-currency; fallback strategy (missing usage data → delay invoice, don't default to $0); validation (line items must sum to total within $0.01). Implementation tasks follow TDD rhythm with data-critic checkpoint after core formula and after tax calculation.
Why good: Complete specification, every formula has test cases, units declared, edge cases planned.
</Good>

<Good>
User: "I got a REVISE from data-critic on the dashboard metrics — plan the fixes"
Action: Planner reads the data-critic findings, creates a focused plan for each finding: corrects the averaging-averages bug (Phase 3 formula with correct weighted average and test case showing the 6x error), adds missing null handling in the aggregation (Phase 5 fallback strategy), adds reconciliation check (Phase 7 row count validation after the join). Checkpoints after each fix for re-review.
Why good: Focused on specific findings, each fix has a test case proving it's correct.
</Good>

<Bad>
User: "Plan the analytics pipeline"
Action: Returns "Step 1: Read data. Step 2: Transform data. Step 3: Write output." No formulas, no test cases, no unit conventions, no assumption register, no fallback strategy.
Why bad: This is not a data plan — it's a vague outline that guarantees undocumented assumptions.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- If the user can't specify what the correct output should be for a given input, STOP and flag this — you can't plan for correctness without a definition of correct
- If the consequence of wrong numbers is high (money, regulatory, executive decisions), escalate plan thoroughness — every formula gets 5+ test cases, all assumptions get verified
- If the plan is for a prototype/experiment, scale down — formulas and test cases still required, but validation and monitoring can be deferred
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] Every calculation has a formula written in math notation with source cited
- [ ] Every formula has at least 3 test cases (normal, boundary, edge)
- [ ] Every numeric field appears in the Unit Convention Registry
- [ ] Every data access point has a fallback strategy
- [ ] The Assumption Register exists with fragility ratings
- [ ] Data provenance is mapped from source to output
- [ ] Validation checkpoints are planned (not just "add tests later")
- [ ] Precision and rounding are specified (mode, position in chain, storage format)
- [ ] Statistical methodology is rationalized (if applicable)
- [ ] Implementation tasks follow TDD rhythm (test first, implement, verify)
- [ ] Data-critic review checkpoints are planned at appropriate stages
- [ ] The plan is scaled to the consequence (regulatory > dashboard > prototype)
</Final_Checklist>

Task: {{ARGUMENTS}}
