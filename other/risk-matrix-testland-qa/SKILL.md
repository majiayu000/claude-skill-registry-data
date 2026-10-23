---
name: risk-matrix
description: "The risk-based testing (RBT) umbrella: risk matrix and risk register authoring, likelihood x impact scoring, risk storming, calibration, and risk-to-test coverage mapping. Produces the per-feature / per-release matrix artifact (structured intake: feature, category, impact 1-5 by likelihood 1-5, score; heatmap; mitigations with owners and due dates), supporting lightweight and heavyweight (FMEA / Cost of Exposure) methods per RBT canon, plus a risk coverage mapping workflow that proves which tests, cases, or monitors back each registered risk. references/ carries the product-risk and project-risk register variants, the risk-storming facilitation guide, matrix calibration against observed defect data, and a register review checklist. Use for any risk-based-testing artifact: building a matrix or register, running a risk-storming session, calibrating ratings against defects, or mapping risks onto test coverage."
---

# risk-matrix

## Overview

Per [rbt-wiki][rbt]:

[rbt]: https://en.wikipedia.org/wiki/Risk-based_testing

> "**Risk-based testing (RBT)** is 'a type of software testing that
> functions as an organizational principle used to prioritize the
> tests of features and functions in software, based on the risk
> of failure.'"

The risk matrix is the artifact that drives RBT decisions. Without
it, prioritization is gut-feel; with it, the team has a
defensible record of "why we tested this and not that."

## When to use

- A new feature is in planning; the team needs to scope test effort.
- A release scope is set; the team needs to allocate manual + auto
  test time.
- Quarterly: the team wants to know which areas have the highest
  unmitigated risk.
- Audit / compliance: the team must show a documented risk
  assessment.

## How to use

1. **Pick the methodology** (Step 1) - lightweight impact-by-likelihood for most teams; heavyweight FMEA / Cost of Exposure only when regulation demands it.
2. **Intake each risk** (Step 2) - one row per risk with feature, category, impact 1-5, likelihood 1-5, and the resulting score.
3. **Plot the heatmap and tier the verdict** (Step 2) - block / mitigate-this-sprint / accept, using the team's block threshold (typically score 15+).
4. **Tag categories** (Step 3) - business, technical, regulatory, UX, security, performance, integration - so patterns surface over time.
5. **Read the test plan off the matrix** (Step 4) - map each top risk to its recommended test types.
6. **Set the cadence and store it in git** (Steps 6-7) - the matrix is a living document reviewed per feature, per release, and quarterly.
7. **Map risks to coverage** (Step 8) - before sign-off, show which tests, cases, or monitors back each risk and which risks are orphans.

The worked example below runs a checkout release through the full flow.
For the adjacent risk artifacts and workflows, see the
[routing table](#going-deeper-referenced-guides) at the end.

## Step 1 - Pick the methodology

Per [rbt-wiki][rbt], two approaches:

| Approach        | Method                                   | When |
|-----------------|------------------------------------------|------|
| **Lightweight** | Impact × Likelihood, simple high/medium/low | Default; most teams. |
| **Heavyweight** | FMEA / Cost of Exposure / QFD / FTA      | Regulated industries; safety-critical; insurance. |

Most teams should start lightweight - heavyweight methods need
specialized expertise.

## Step 2 - Lightweight matrix structure

```markdown
# Risk matrix - `<feature/release>`

**Date:** YYYY-MM-DD   **Owner:** _______________   **Reviewers:** _______________

## Risks

| ID  | Risk                                          | Category   | Impact (1-5) | Likelihood (1-5) | Score | Mitigation                          | Owner | Due |
|-----|-----------------------------------------------|------------|-------------:|-----------------:|------:|-------------------------------------|-------|-----|
| R-1 | Promo discount math wrong (off-by-cent)        | Business   |      5       |       3          |  15   | Add property-based tests on rounding | Alice | 2026-05-15 |
| R-2 | Stripe webhook delivery failure not retried    | Technical  |      4       |       4          |  16   | Add retry + DLQ; add chaos test     | Bob   | 2026-05-12 |
| R-3 | EU tax calculation incorrect                    | Regulatory |      5       |       2          |  10   | UAT with finance team               | Carol | 2026-05-20 |
| R-4 | Cart loses state on app restart                 | UX         |      3       |       3          |   9   | Persistent cart in localStorage     | Dave  | 2026-05-10 |

## Heatmap

| Likelihood ↓ \ Impact → | 1 (low) | 2 | 3 | 4 | 5 (high) |
|--------------------------|---------|---|---|---|----------|
| 5 (very likely)           |         |   |   |   |          |
| 4                          |         |   |   | R-2 |        |
| 3                          |         |   | R-4 |   | R-1     |
| 2                          |         |   |   |   | R-3     |
| 1                          |         |   |   |   |          |

## Verdict

- **Critical (score >=15):** R-1 (15), R-2 (16). Block release until mitigated.
- **High (score 9-14):** R-3 (10), R-4 (9). Mitigate this sprint.
- **Medium (score 5-8):** (none).
- **Low (score 1-4):** (none).
```

The 5×5 matrix yields scores 1-25; the team picks the threshold
for "block release" (typically 15+).

## Step 3 - Risk categories

Per [rbt-wiki][rbt], risks span:

> - **Business/operational**: System criticality and usage frequency
> - **Technical**: Team distribution and complexity
> - **External**: Regulatory requirements and stakeholder preferences
> - **E-business specific**: Security vulnerabilities, performance failures, and integration defects

Tag every risk with one category. Patterns emerge over time - 
"all our top risks are integration" suggests an architectural
review, not just more testing.

## Step 4 - Map risks to test types

A populated matrix drives the test plan:

| Risk class     | Recommended test types                                       |
|----------------|--------------------------------------------------------------|
| Business logic  | Unit + property-based + UAT                                  |
| Technical       | Integration + chaos + load                                    |
| Regulatory      | UAT with stakeholder + compliance review                      |
| UX              | Manual exploratory + visual regression                         |
| Security        | Threat model + SAST + DAST + pen test                         |
| Performance     | Load + perf budget + canary                                   |
| Integration     | Contract testing + integration tests + canary                 |

The test plan reads off the matrix: top-N risks → test types per
risk → estimated effort.

## Worked example - checkout redesign release

Input: the checkout-redesign release scope, lightweight methodology (Step 1).

**Intake and score (Steps 2-3).** Four risks surface, each tagged with a
category and scored impact × likelihood:

| ID  | Risk                                          | Category   | Impact | Likelihood | Score |
|-----|-----------------------------------------------|------------|-------:|-----------:|------:|
| R-1 | Promo discount math wrong (off-by-cent)        | Business   |   5    |     3      |  15   |
| R-2 | Stripe webhook delivery failure not retried    | Technical  |   4    |     4      |  16   |
| R-3 | EU tax calculation incorrect                    | Regulatory |   5    |     2      |  10   |
| R-4 | Cart loses state on app restart                 | UX         |   3    |     3      |   9   |

**Tier the verdict (Step 2).** With a block threshold of 15: R-2 (16) and
R-1 (15) block the release until mitigated; R-3 (10) and R-4 (9) are high and
get mitigated this sprint.

**Read the test plan off the matrix (Step 4).** Each risk's category selects
its test types:

- R-1 (business logic) -> unit + property-based tests on rounding, plus UAT on the promo path.
- R-2 (technical / integration) -> retry + DLQ, a chaos test on webhook delivery, and contract tests against Stripe.
- R-3 (regulatory) -> UAT with the finance team plus a compliance review of the EU tax rules.
- R-4 (UX) -> manual exploratory plus visual-regression coverage of the persisted cart.

**Outcome.** The two blocking risks (R-1, R-2) get owners and due dates before
sign-off; the matrix is committed to
`docs/risk-matrices/2026-Q2-checkout-redesign.md` and re-reviewed at the next
cadence point (Step 6).

## Step 5 - Heavyweight methods (FMEA, Cost of Exposure)

For regulated or safety-critical products where lightweight scoring is
insufficient, risk-based testing offers quantitative methods - FMEA (Risk
Priority Number = severity × occurrence × detectability) and Cost of Exposure
(annual financial risk vs mitigation cost) - per [rbt-wiki][rbt]. Both need
specialized expertise; use them only when regulation or financial
justification requires it. Full row structure, worked FMEA and
Cost-of-Exposure tables, and a when-to-use guide are in
[references/heavyweight-risk-scoring.md](references/heavyweight-risk-scoring.md).

## Step 6 - Cadence

| Cadence    | Trigger                                        |
|------------|------------------------------------------------|
| Per-feature | Before development starts                       |
| Per-release | Pre-release sign-off                            |
| Quarterly   | Strategic risk review                           |
| Post-incident | Update the matrix with the surfaced risk      |

The matrix is a **living document** - risks change as features
ship, mitigations land, and incidents reveal new failure modes.

## Step 7 - Format + storage

```
docs/risk-matrices/
├── 2026-Q2-checkout-redesign.md
├── 2026-Q2-stripe-integration.md
├── 2026-Q1-summary.md       ← rollup
└── README.md
```

Markdown files version-controlled in git. Reviews via PR; updates
tracked over time.

## Step 8 - Risk coverage mapping

A risk-coverage matrix proves every meaningful risk has a mitigation that
traces to a test or monitor - the risk-side complement to the requirements
traceability matrix (`traceability-matrix-builder`, in the qa-test-management
plugin). Per ISTQB CTAL-TM ch. 5 on risk-based test prioritisation and
ISO/IEC/IEEE 29119-3:2021 §6.3 on traceability (cite by stable ID). Run it
before a release sign-off or compliance audit, at sprint retrospectives to
find coverage debt, and in CI per PR.

### 8a - Ingest the risk register

Pull risks from the release matrix (this skill) and the product register
([references/product-risk-register.md](references/product-risk-register.md));
project risks (schedule, staffing) are typically excluded - only product /
release risks map to *test* coverage. Filter to score >= 5 (Medium+).

### 8b - Inventory coverage from three sources

Tag tests with a `risk:<ID>` marker in name / docstring / front-matter, then:

```bash
grep -r "risk:R-001\|risk:PR-001" tests/ --include="*.py" \
  --include="*.js" --include="*.ts" --include="*.java" -l
```

| Coverage source | How to collect |
|---|---|
| Automated tests | Repo scan for `risk:<ID>` tags (above) |
| Manual test cases | Query the TCM for cases whose refs field contains the risk ID |
| Production monitoring | A `risk-coverage.yaml` map of risk ID -> monitor IDs (e.g., `datadog-monitor://stripe-webhook-failure-rate`) |

### 8c - Compute depth and find orphans

Per risk, coverage depth = linked automated tests + manual cases + monitors:

| Depth | Verdict |
|---|---|
| 0 | **Orphan risk** - no coverage. Critical if risk score ≥ 10. |
| 1 | Minimal. Acceptable for low-score risks; insufficient for critical. |
| 2-4 | Reasonable. Multiple angles (unit + integration + monitor). |
| 5+ | Possibly over-tested. Audit for redundancy. |

Also run the reverse pass: tests whose `risk:<ID>` tag points at a retired /
non-existent risk are **orphan tests** - written for risks that no longer
exist. Audit for deletion.

### 8d - Emit the matrix + executive summary

Emit a Markdown document ordered by score descending: a header (total risks,
covered count and %, orphan count split critical vs low, average depth), one
row per risk (ID, title, score, automated tests, manual cases, monitors,
depth - bold any orphan), an "orphan risks (critical action)" section with a
recommended action + owner + estimate per orphan, an "over-covered (audit)"
list, and a coverage-debt trend table (orphan count and average depth over
recent months). Keep both artifacts version-controlled next to the matrix so
the trend is real history.

### 8e - CI gate

Re-build the matrix on every PR; fail if a critical-score risk becomes
uncovered:

```yaml
- name: Risk coverage check
  run: |
    python scripts/build-risk-coverage.py \
      --risks risks.yaml \
      --output risk-coverage.md \
      --fail-on-orphan-score 15
```

Caveats: tag discipline is the ceiling (untagged tests under-report
coverage); depth measures count, not test *quality*; a monitor existing does
not prove it would catch the risk; treat depth 1 as "covered" only for
low-score risks.

## Going deeper (referenced guides)

| Task | Guide |
|---|---|
| Long-lived product-quality risks (persist across releases, ISO 25010 walk) | [references/product-risk-register.md](references/product-risk-register.md) |
| Project-execution risks (schedule, staffing, vendor; Avoid / Mitigate / Transfer / Accept) | [references/project-risk-register.md](references/project-risk-register.md) |
| Facilitating the risk-storming session that fills the matrix | [references/risk-storming.md](references/risk-storming.md) |
| Calibrating an aged matrix against observed defects, escapes, and churn | [references/calibration.md](references/calibration.md) |
| Auditing a register's assessment quality before release planning | [references/risk-review-checklist.md](references/risk-review-checklist.md) |
| FMEA / Cost-of-Exposure worked tables | [references/heavyweight-risk-scoring.md](references/heavyweight-risk-scoring.md) |

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Risk matrix authored once, never updated                              | Becomes irrelevant; team stops trusting.                                 | Per-feature + quarterly cadence (Step 6). |
| Subjective scoring without examples                                   | Different reviewers score differently; matrix unreliable.                | Document score rubric (e.g., "5 = customer money loss"). |
| All-business-category matrix                                           | Misses technical / regulatory risks; gaps invisible.                     | Tag every risk with a category (Step 3). |
| Matrix without owner per row                                           | "Mitigated" never happens.                                               | Owner column required (Step 2). |
| Heavyweight FMEA on a small product                                    | Over-engineering; team disables.                                         | Lightweight default; FMEA only when regulation requires (Step 1). |
| Risk matrix in slides, not version-controlled                          | History lost; rollup impossible.                                         | Markdown + git (Step 7). |

## Limitations

- **Subjective scoring.** Even with a rubric, team members weigh
  risks differently. Multiple-reviewer consensus helps.
- **Doesn't predict unknown unknowns.** RBT addresses identified
  risks; new failure modes emerge from incidents (and update the
  matrix).
- **Heavyweight methods need expertise.** FMEA is well-defined; QFD
  / FTA require specialized training.

## References

- [rbt][rbt] - Risk-based testing definition, lightweight vs
  heavyweight methods (FMEA, Cost of Exposure, QFD, FTA), risk
  categories (business / technical / external / e-business).
- ISTQB Advanced Test Manager (CTAL-TM) syllabus, ch. 5 - risk-based
  testing + risk-coverage measurement (Step 8).
- ISTQB Glossary - [glossary.istqb.org](https://glossary.istqb.org/) -
  "coverage item", "test condition".
- ISO/IEC/IEEE 29119-3:2021 §6.3 - traceability (cite by stable ID).
- `test-strategy-author` -
  test strategy doc that references the matrix.
- `traceability-matrix-builder` (qa-test-management) - the
  requirements-side complement of the Step 8 coverage matrix.
