---
name: technical-debt-analyzer
description: Quantify, categorize, and prioritize technical debt using SQALE methodology with interest calculation and remediation planning. Use when assessing code.
---

# Technical Debt Analyzer

Systematic identification, quantification, and prioritization of technical debt across a codebase. This skill applies the SQALE (Software Quality Assessment based on Lifecycle Expectations) methodology and established debt classification frameworks to produce actionable remediation plans with effort estimates and business impact analysis.

## When to Use This Skill

Use this skill for:

- Assessing the overall technical debt posture of a codebase or system
- Quantifying debt in terms of remediation effort (hours, story points) and ongoing interest (cost of delay)
- Categorizing debt by type (code, architecture, test, documentation, infrastructure, dependency)
- Prioritizing which debt items to address first based on business impact and remediation cost
- Planning debt reduction sprints or allocating capacity for ongoing debt management
- Communicating technical debt status to non-technical stakeholders
- Establishing debt budgets and tracking trends over time
- Evaluating whether to pay down debt or accept it as a conscious trade-off

**Trigger phrases**: "technical debt", "tech debt", "debt analysis", "debt assessment", "code debt", "architecture debt", "test debt", "documentation debt", "debt prioritization", "remediation plan", "SQALE", "debt budget", "debt reduction"

## What This Skill Does

This skill provides a comprehensive debt management framework:

- **Debt Identification**: Systematically discovers debt across all categories using code analysis, architecture review, test coverage gaps, and documentation audits
- **Debt Classification**: Categorizes each debt item by type, cause (deliberate vs. accidental, reckless vs. prudent), and affected quality attribute
- **SQALE Quantification**: Applies the SQALE methodology to measure debt in terms of remediation cost and calculate the debt ratio
- **Interest Calculation**: Estimates the ongoing cost of not addressing each debt item, expressed as additional development time, increased defect rates, or reduced velocity
- **Priority Scoring**: Ranks debt items using a multi-factor model that considers business impact, remediation cost, interest rate, and strategic alignment
- **Remediation Planning**: Produces sprint-level plans for paying down debt, including dependency ordering and risk mitigation

## Instructions

### Step 1: Identify Technical Debt by Category

Systematically scan the codebase and surrounding artifacts for debt in each category.

#### Debt Category Taxonomy

| Category | Description | Common Indicators |
|----------|-------------|-------------------|
| **Code Debt** | Poor code quality, code smells, complexity | High cyclomatic complexity, duplicated code, long methods, deep nesting |
| **Architecture Debt** | Structural problems at the module or system level | Circular dependencies, god modules, layer violations, monolithic coupling |
| **Test Debt** | Insufficient, brittle, or slow test coverage | Low coverage (<60%), flaky tests, no integration tests, manual-only testing |
| **Documentation Debt** | Missing, outdated, or misleading documentation | No API docs, stale READMEs, undocumented architecture decisions |
| **Infrastructure Debt** | Outdated tools, manual processes, fragile CI/CD | Manual deployments, unsupported OS versions, no containerization |
| **Dependency Debt** | Outdated or vulnerable dependencies | EOL frameworks, unpatched CVEs, version pinning to ancient releases |

#### Python Example: Identifying Code Debt

```python
# CODE DEBT: High cyclomatic complexity (15), deep nesting (5 levels),
# magic numbers, no error handling
def process_transactions(transactions, config):
    results = []
    for t in transactions:
        if t["type"] == "purchase":
            if t["amount"] > 0:
                if t["currency"] == "USD":
                    tax = t["amount"] * 0.0875
                    total = t["amount"] + tax
                    if total > 10000:
                        if config["require_approval"]:
                            if t.get("approved_by"):
                                results.append({"id": t["id"], "total": total, "status": "processed"})
                            else:
                                results.append({"id": t["id"], "status": "pending_approval"})
                        else:
                            results.append({"id": t["id"], "total": total, "status": "processed"})
                    else:
                        results.append({"id": t["id"], "total": total, "status": "processed"})
                elif t["currency"] == "EUR":
                    tax = t["amount"] * 0.19
                    total = t["amount"] + tax
                    results.append({"id": t["id"], "total": total, "status": "processed"})
                # ... 5 more currency branches
        elif t["type"] == "refund":
            # ... 40 more lines of similar nested logic
            pass
    return results
```

**Debt items identified**:

1. Cyclomatic complexity of 15 (threshold: 10) -- code debt
2. Nesting depth of 5 (threshold: 3) -- code debt
3. Magic numbers (0.0875, 0.19, 10000) -- code debt
4. No input validation or error handling -- code debt
5. No type hints or documentation -- documentation debt
6. Dictionary-based data model instead of typed objects -- architecture debt
7. Tax calculation logic duplicated per currency -- code debt

#### JavaScript Example: Identifying Architecture Debt

```javascript
// ARCHITECTURE DEBT: This module imports from 14 other modules,
// mixes UI rendering with business logic and data access,
// and is imported by 23 other modules (high afferent + efferent coupling)
import { db } from "./database";
import { cache } from "./cache";
import { logger } from "./logger";
import { validator } from "./validator";
import { emailService } from "./email";
import { pdfGenerator } from "./pdf";
import { taxCalculator } from "./tax";
import { currencyConverter } from "./currency";
import { auditTrail } from "./audit";
import { notificationService } from "./notifications";
import { featureFlags } from "./features";
import { analyticsTracker } from "./analytics";
import { rateLimiter } from "./rateLimit";
import { permissionChecker } from "./permissions";

export class OrderService {
    // 800+ lines mixing:
    // - HTTP request handling
    // - Business rule validation
    // - Database queries
    // - PDF generation
    // - Email sending
    // - Analytics tracking
    // - Permission checking
    async createOrder(req, res) { /* ... */ }
    async renderOrderPage(req, res) { /* ... */ }
    async generateInvoicePdf(orderId) { /* ... */ }
    async sendOrderConfirmation(orderId) { /* ... */ }
    // ... 20 more methods
}
```

**Debt items identified**:

1. God module with 14 dependencies (threshold: 7) -- architecture debt
2. Mixed responsibilities: HTTP handling, business logic, data access, rendering -- architecture debt
3. 800+ lines in a single class (threshold: 300) -- code debt
4. High coupling: 23 dependents means changes here cascade widely -- architecture debt

#### Java Example: Identifying Test Debt

```java
// TEST DEBT: This critical payment processing class has:
// - 12% line coverage (threshold: 80%)
// - 0% branch coverage on error paths
// - No integration tests with actual payment gateway
// - No tests for concurrent access scenarios
// - Flaky test that depends on system clock

public class PaymentGatewayAdapter {
    // Only happy-path tested
    public PaymentResult charge(BigDecimal amount, String token) {
        // Untested: What happens when gateway returns HTTP 500?
        // Untested: What happens when amount is negative?
        // Untested: What happens when token is expired?
        // Untested: What happens under concurrent access?
        // ...
    }
}

// The single existing test:
@Test
void testCharge() {
    // FLAKY: depends on current time for idempotency key
    PaymentResult result = adapter.charge(new BigDecimal("10.00"), "tok_valid");
    assertEquals("success", result.getStatus());
}
```

**Debt items identified**:

1. 12% line coverage on critical payment code (threshold: 80%) -- test debt, critical severity
2. Zero branch coverage on error paths -- test debt, high severity
3. No integration tests with payment gateway -- test debt, high severity
4. Flaky test depending on system clock -- test debt, medium severity
5. No concurrency tests for shared resource -- test debt, medium severity

### Step 2: Classify Debt Using the Deliberate/Accidental Matrix

Use Martin Fowler's Technical Debt Quadrant to classify each debt item by its origin, which informs the appropriate response.

| | **Reckless** | **Prudent** |
|---|---|---|
| **Deliberate** | "We don't have time for design" -- taken knowingly with disregard for consequences | "We must ship now and deal with consequences" -- conscious trade-off with a plan to repay |
| **Accidental** | "What's layering?" -- taken unknowingly due to lack of knowledge | "Now we know how we should have done it" -- discovered after gaining experience |

**Classification impacts response strategy**:

- **Deliberate Prudent**: schedule remediation; the team already knows the fix
- **Deliberate Reckless**: requires intervention; may indicate systemic process problems
- **Accidental Prudent**: natural learning; plan remediation as part of ongoing improvement
- **Accidental Reckless**: requires training and mentoring in addition to remediation

### Step 3: Quantify Debt Using SQALE Methodology

The SQALE (Software Quality Assessment based on Lifecycle Expectations) method maps debt to quality characteristics and measures remediation effort.

#### SQALE Quality Model Characteristics

1. **Testability**: ability to test the software effectively
2. **Reliability**: correctness and fault tolerance
3. **Changeability**: ease of modification
4. **Efficiency**: performance and resource usage
5. **Security**: protection against vulnerabilities
6. **Maintainability**: understandability and modifiability
7. **Portability**: ability to transfer between environments
8. **Reusability**: ability to reuse components

#### Remediation Cost Estimation

For each debt item, estimate the remediation cost in developer-hours.

| Debt Item | Affected Characteristic | Remediation Effort | Confidence |
|-----------|------------------------|-------------------|------------|
| High cyclomatic complexity in `process_transactions` | Changeability, Testability | 4 hours | High |
| God module `OrderService` (800 lines, 14 deps) | Changeability, Testability, Reusability | 24 hours | Medium |
| Payment gateway 12% coverage | Testability, Reliability | 16 hours | Medium |
| Dictionary-based data model | Reliability, Changeability | 8 hours | High |
| Magic numbers in tax calculation | Changeability, Reliability | 2 hours | High |
| Missing API documentation | Maintainability, Reusability | 6 hours | Medium |

#### SQALE Debt Ratio

The SQALE debt ratio measures debt as a proportion of the total estimated development effort:

```
Debt Ratio = Total Remediation Cost / Total Development Cost

Rating scale:
  A: Debt Ratio <= 5%   (excellent)
  B: Debt Ratio <= 10%  (good)
  C: Debt Ratio <= 20%  (moderate)
  D: Debt Ratio <= 50%  (poor)
  E: Debt Ratio > 50%   (critical)
```

### Step 4: Calculate Interest

Interest is the ongoing cost of not paying down the debt. It manifests as reduced velocity, increased defect rates, longer onboarding times, and higher change failure rates.

#### Interest Calculation Model

```
Annual Interest = Frequency of Impact x Cost Per Impact

Where:
  Frequency of Impact = number of times per year the debt item causes
                        extra work (additional debugging, workarounds,
                        failed deployments, onboarding delays)
  Cost Per Impact     = average developer-hours lost per occurrence
```

#### Python Example: Interest Calculation

```python
from dataclasses import dataclass
from typing import List


@dataclass
class DebtItem:
    name: str
    category: str
    remediation_hours: float
    impact_frequency_per_year: int
    cost_per_impact_hours: float
    severity: str

    @property
    def annual_interest(self) -> float:
        return self.impact_frequency_per_year * self.cost_per_impact_hours

    @property
    def payback_period_months(self) -> float:
        if self.annual_interest == 0:
            return float("inf")
        return (self.remediation_hours / self.annual_interest) * 12

    @property
    def roi_one_year(self) -> float:
        if self.remediation_hours == 0:
            return float("inf")
        return (self.annual_interest - self.remediation_hours) / self.remediation_hours


def prioritize_debt(items: List[DebtItem]) -> List[DebtItem]:
    """Prioritize debt by ROI (highest return on investment first)."""
    return sorted(items, key=lambda item: item.roi_one_year, reverse=True)


# Example debt portfolio
debt_portfolio = [
    DebtItem("God module OrderService", "architecture", 24, 52, 2.0, "critical"),
    DebtItem("Payment gateway low coverage", "test", 16, 12, 4.0, "critical"),
    DebtItem("Magic numbers in tax calc", "code", 2, 6, 0.5, "medium"),
    DebtItem("Missing API documentation", "documentation", 6, 24, 0.5, "medium"),
    DebtItem("Dictionary data model", "code", 8, 26, 1.0, "high"),
]

prioritized = prioritize_debt(debt_portfolio)
for item in prioritized:
    print(f"{item.name}: ROI={item.roi_one_year:.1f}, "
          f"payback={item.payback_period_months:.1f} months, "
          f"interest={item.annual_interest:.0f} hrs/year")
```

### Step 5: Prioritize Using Multi-Factor Scoring

Rank debt items using a weighted scoring model that balances multiple factors.

#### Priority Scoring Matrix

| Factor | Weight | 1 (Low) | 2 (Medium) | 3 (High) | 4 (Critical) |
|--------|--------|---------|------------|----------|---------------|
| **Business Impact** | 30% | Rarely affects users | Occasional user-facing issues | Regular user-facing issues | Blocks revenue or causes outages |
| **Interest Rate** | 25% | <5 hrs/year wasted | 5-20 hrs/year | 20-100 hrs/year | >100 hrs/year |
| **Remediation Cost** | 20% | >40 hours | 20-40 hours | 8-20 hours | <8 hours (quick win) |
| **Strategic Alignment** | 15% | Not on roadmap | Tangentially related | Directly supports upcoming work | Blocks planned features |
| **Risk of Inaction** | 10% | Stable, no growth | Slow growth | Moderate growth | Compounding rapidly |

**Priority Score** = (Business Impact x 0.30) + (Interest Rate x 0.25) + (Remediation Cost x 0.20) + (Strategic Alignment x 0.15) + (Risk of Inaction x 0.10)

**Interpretation**:

- 3.5-4.0: Address immediately (current sprint)
- 2.5-3.4: Schedule for next 1-2 sprints
- 1.5-2.4: Add to backlog, address when convenient
- 1.0-1.4: Accept as low-priority or intentional trade-off

### Step 6: Create a Remediation Plan

Produce a structured plan that can be integrated into sprint planning.

#### JavaScript Example: Remediation Plan Data Structure

```javascript
const remediationPlan = {
    summary: {
        totalDebtItems: 47,
        totalRemediationHours: 312,
        totalAnnualInterest: 840,
        sqaleRating: "C",
        debtRatio: 0.18,
    },
    phases: [
        {
            name: "Phase 1: Quick Wins",
            sprint: "Sprint 24",
            capacityHours: 16,
            items: [
                {
                    name: "Extract magic numbers to constants",
                    category: "code",
                    effort: 2,
                    annualInterestSaved: 3,
                    risk: "low",
                    dependencies: [],
                },
                {
                    name: "Add type hints to core modules",
                    category: "documentation",
                    effort: 6,
                    annualInterestSaved: 12,
                    risk: "low",
                    dependencies: [],
                },
                {
                    name: "Fix flaky payment test",
                    category: "test",
                    effort: 4,
                    annualInterestSaved: 8,
                    risk: "low",
                    dependencies: [],
                },
            ],
        },
        {
            name: "Phase 2: High-Impact Structural Changes",
            sprint: "Sprint 25-26",
            capacityHours: 40,
            items: [
                {
                    name: "Split OrderService god module",
                    category: "architecture",
                    effort: 24,
                    annualInterestSaved: 104,
                    risk: "medium",
                    dependencies: ["Extract magic numbers to constants"],
                },
                {
                    name: "Increase payment gateway coverage to 80%",
                    category: "test",
                    effort: 16,
                    annualInterestSaved: 48,
                    risk: "low",
                    dependencies: ["Fix flaky payment test"],
                },
            ],
        },
        {
            name: "Phase 3: Foundation Improvements",
            sprint: "Sprint 27-28",
            capacityHours: 32,
            items: [
                {
                    name: "Replace dictionary data model with typed classes",
                    category: "code",
                    effort: 8,
                    annualInterestSaved: 26,
                    risk: "medium",
                    dependencies: ["Split OrderService god module"],
                },
                {
                    name: "Write API documentation for public interfaces",
                    category: "documentation",
                    effort: 6,
                    annualInterestSaved: 12,
                    risk: "low",
                    dependencies: ["Split OrderService god module"],
                },
            ],
        },
    ],
};
```

#### Java Example: Debt Tracking Over Time

```java
public class DebtTracker {
    private final List<DebtSnapshot> history = new ArrayList<>();

    public void recordSnapshot(LocalDate date, List<DebtItem> items) {
        double totalRemediation = items.stream()
            .mapToDouble(DebtItem::getRemediationHours)
            .sum();
        double totalInterest = items.stream()
            .mapToDouble(DebtItem::getAnnualInterest)
            .sum();
        long criticalCount = items.stream()
            .filter(i -> "critical".equals(i.getSeverity()))
            .count();

        history.add(new DebtSnapshot(date, items.size(), totalRemediation,
            totalInterest, criticalCount));
    }

    public DebtTrend analyzeTrend() {
        if (history.size() < 2) {
            return DebtTrend.INSUFFICIENT_DATA;
        }
        DebtSnapshot first = history.get(0);
        DebtSnapshot last = history.get(history.size() - 1);

        double remediationDelta = last.totalRemediation - first.totalRemediation;
        double interestDelta = last.totalInterest - first.totalInterest;

        if (remediationDelta < 0 && interestDelta < 0) {
            return DebtTrend.IMPROVING;
        } else if (remediationDelta > 0 && interestDelta > 0) {
            return DebtTrend.WORSENING;
        }
        return DebtTrend.STABLE;
    }
}
```

### Step 7: Generate the Debt Report

Produce a report for stakeholders that combines technical details with business context.

```
## Technical Debt Assessment Report

### Executive Summary
- **SQALE Rating**: {A-E}
- **Debt Ratio**: {percentage}
- **Total Remediation Cost**: {hours} ({story points})
- **Annual Interest (cost of inaction)**: {hours/year}
- **Trend**: Improving / Stable / Worsening (vs. last assessment)

### Debt Breakdown by Category
| Category | Items | Remediation (hrs) | Interest (hrs/yr) | Severity Distribution |
|----------|-------|-------------------|-------------------|----------------------|
| Code | {n} | {hrs} | {hrs/yr} | {C}C / {H}H / {M}M / {L}L |
| Architecture | {n} | {hrs} | {hrs/yr} | ... |
| Test | {n} | {hrs} | {hrs/yr} | ... |
| Documentation | {n} | {hrs} | {hrs/yr} | ... |
| Infrastructure | {n} | {hrs} | {hrs/yr} | ... |
| Dependency | {n} | {hrs} | {hrs/yr} | ... |

### Top 10 Debt Items by Priority
| # | Item | Category | Severity | Remediation | Interest | ROI |
|---|------|----------|----------|-------------|----------|-----|
| 1 | ... | ... | ... | ... | ... | ... |

### Remediation Plan
{Phased plan from Step 6}

### Recommendations
- {Strategic recommendations for debt management}
```

## Best Practices

- **Allocate a consistent percentage of capacity to debt reduction**: a common target is 15-20% of sprint capacity dedicated to technical debt; this prevents debt from compounding while still delivering features
- **Track debt as a first-class backlog item**: debt items should be visible in the same backlog as features and bugs, with clear acceptance criteria and effort estimates
- **Distinguish between debt and maintenance**: routine dependency updates, security patches, and test additions are maintenance, not debt; reserve the "debt" label for items that incur ongoing interest
- **Reassess priorities regularly**: debt priorities shift as the product roadmap evolves; an architecture debt item may become critical when a dependent feature is planned, or irrelevant when a module is deprecated
- **Communicate debt in business terms**: instead of "cyclomatic complexity of 15", say "this code takes 3x longer to modify than it should, costing us approximately 2 hours per feature that touches this area"
- **Establish a debt budget**: set a maximum acceptable debt ratio (e.g., SQALE rating B or better) and treat breaches as a signal to reduce feature work and increase remediation
- **Use automated tools for continuous measurement**: integrate static analysis (SonarQube, CodeClimate), dependency scanning (Dependabot, Renovate), and coverage tools (Codecov, Coveralls) to track debt metrics automatically
- **Celebrate debt paydown**: make debt reduction visible in sprint reviews and team dashboards to reinforce the value of quality investment

## Common Pitfalls

- **Treating all debt as equal**: a 2-hour magic number fix and a 40-hour architecture restructuring require fundamentally different planning approaches; prioritize by ROI, not by count
- **Measuring only code-level debt**: architecture debt, test debt, and infrastructure debt are often more costly than code smells but harder to detect with automated tools; include all categories in assessments
- **Using debt as an excuse to avoid refactoring**: some teams label every refactoring as "tech debt" and then deprioritize it; distinguish between debt (incurs ongoing interest) and improvement (one-time benefit)
- **Paying down debt without measuring impact**: if you cannot demonstrate that debt reduction improved velocity, reduced defects, or shortened onboarding, the business will stop funding it; track and report outcomes
- **Ignoring deliberate debt**: debt taken on deliberately with a plan to repay is healthy engineering; the problem is when the repayment plan is never executed; track deliberate debt items and enforce repayment deadlines
- **Over-investing in debt reduction**: a codebase with zero debt is not the goal; the goal is to maintain debt at a level where it does not significantly impair velocity or quality; diminishing returns apply
- **Failing to address the root cause**: if debt accumulates because of time pressure, lack of code review, or insufficient testing culture, paying down individual items without fixing the process will result in re-accumulation
- **Not accounting for the cost of remediation itself**: refactoring introduces risk; estimate not just the effort but also the potential for regressions, and factor in the cost of testing the remediation
