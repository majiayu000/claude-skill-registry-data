---
name: estimation-techniques
description: Software estimation methodologies including story points, function points, T-shirt sizing, PERT, Wideband Delphi, and estimation calibration techniques.
allowed-tools: Read, Glob, Grep
---

# Estimation Techniques

Comprehensive guidance for software estimation using various methodologies suited to different contexts and accuracy requirements.

## When to Use This Skill

- Estimating feature development effort
- Planning sprints and releases
- Creating project budgets and timelines
- Comparing estimation approaches
- Improving estimation accuracy over time
- Training teams on estimation techniques

## Quick Reference

### Estimation Technique Selection

| Technique | Best For | Accuracy | Effort |
|-----------|----------|----------|--------|
| **Story Points** | Agile teams, relative sizing | Medium | Low |
| **Function Points** | Contracts, benchmarking | High | High |
| **T-Shirt Sizing** | Early-stage, roadmapping | Low | Very Low |
| **PERT** | Schedule estimation | Medium-High | Medium |
| **Wideband Delphi** | Expert consensus | Medium-High | Medium |
| **Planning Poker** | Team alignment | Medium | Low |
| **#NoEstimates** | Stable teams, flow | N/A | Zero |

### Estimation Accuracy by Phase

```text
Cone of Uncertainty:

Project Phase          Estimate Range
─────────────────────────────────────
Initial Concept        0.25x - 4x
Requirements           0.5x - 2x
Design                 0.67x - 1.5x
Implementation         0.8x - 1.25x
Completion             0.9x - 1.1x
```

## Story Point Estimation

### Fibonacci Scale Guidance

```yaml
story_point_scale:
  1:
    description: "Trivial change, well understood"
    examples:
      - "Change a label or error message"
      - "Add a simple validation rule"
      - "Update configuration value"
    risk: "Minimal"

  2:
    description: "Small, low complexity"
    examples:
      - "Add a new field to a form"
      - "Create a simple API endpoint"
      - "Write a straightforward unit test"
    risk: "Low"

  3:
    description: "Small with some complexity"
    examples:
      - "Add pagination to a list"
      - "Implement basic search/filter"
      - "Create a simple component"
    risk: "Low-Medium"

  5:
    description: "Medium complexity"
    examples:
      - "Implement CRUD for a new entity"
      - "Add OAuth integration"
      - "Create a multi-step form wizard"
    risk: "Medium"

  8:
    description: "Large, significant complexity"
    examples:
      - "Build a complex reporting dashboard"
      - "Implement real-time notifications"
      - "Create a new microservice"
    risk: "Medium-High"

  13:
    description: "Very large, high uncertainty"
    examples:
      - "Major architectural refactoring"
      - "Third-party integration with unknowns"
      - "New technology adoption"
    risk: "High"
    recommendation: "Consider splitting"

  21:
    description: "Epic-sized, should be broken down"
    recommendation: "Must be decomposed before estimation"

  infinity:
    description: "Too large or unknown to estimate"
    recommendation: "Requires research spike first"
```

### Reference Story Catalog

```csharp
namespace EstimationPlanning.StoryPoints;

/// <summary>
/// Reference stories for calibrating story point estimates.
/// </summary>
public static class ReferenceStories
{
    public static readonly ReferenceStory[] Catalog =
    [
        new(
            Points: 1,
            Title: "Update error message text",
            Scope: "Modify a single string in a resource file",
            Complexity: "None - direct change",
            Testing: "Manual verification",
            Dependencies: "None"),

        new(
            Points: 2,
            Title: "Add email format validation",
            Scope: "Add regex validation to email input field",
            Complexity: "Low - pattern matching",
            Testing: "Unit tests for valid/invalid formats",
            Dependencies: "None"),

        new(
            Points: 3,
            Title: "Add sorting to user list",
            Scope: "Column headers clickable, ascending/descending",
            Complexity: "Low-Medium - state management",
            Testing: "Unit + integration tests",
            Dependencies: "Existing list component"),

        new(
            Points: 5,
            Title: "Implement password reset flow",
            Scope: "Request form, email sending, token validation, new password form",
            Complexity: "Medium - multiple steps, security considerations",
            Testing: "Unit, integration, E2E tests",
            Dependencies: "Email service, token storage"),

        new(
            Points: 8,
            Title: "Add export to Excel feature",
            Scope: "Query data, format as XLSX, download with streaming",
            Complexity: "Medium-High - large data handling, file format",
            Testing: "Unit, integration, performance tests",
            Dependencies: "Excel library, data access"),

        new(
            Points: 13,
            Title: "Implement SSO with SAML",
            Scope: "SAML configuration, identity provider integration, session management",
            Complexity: "High - security, third-party coordination",
            Testing: "Unit, integration, security testing",
            Dependencies: "Identity provider, certificate management")
    ];
}

public sealed record ReferenceStory(
    int Points,
    string Title,
    string Scope,
    string Complexity,
    string Testing,
    string Dependencies);
```

### Planning Poker Protocol

```yaml
planning_poker_protocol:
  setup:
    - "Ensure all estimators have context"
    - "Prepare reference stories for calibration"
    - "Agree on estimation scale (Fibonacci recommended)"

  process:
    1_present:
      action: "Product owner presents user story"
      includes:
        - "Acceptance criteria"
        - "Known dependencies"
        - "Technical notes"

    2_clarify:
      action: "Team asks clarifying questions"
      guidelines:
        - "Focus on scope and complexity"
        - "Identify unknowns"
        - "Don't debate solutions yet"

    3_estimate:
      action: "All estimators select cards privately"
      rule: "No influence from others"

    4_reveal:
      action: "Simultaneously reveal all cards"

    5_discuss:
      action: "High and low estimators explain reasoning"
      focus:
        - "What complexity did you see?"
        - "What assumptions did you make?"
        - "What risks are you considering?"

    6_re_estimate:
      action: "If needed, repeat steps 3-5"
      convergence: "Usually 2-3 rounds maximum"

    7_record:
      action: "Record final estimate and key assumptions"

  facilitation_tips:
    - "Timebox discussions (2-3 minutes per round)"
    - "Prevent anchoring by simultaneous reveal"
    - "Focus on relative complexity, not hours"
    - "Use reference stories to calibrate"
    - "Record assumptions that influenced estimates"
```

## Function Point Analysis

### Function Point Counting

```yaml
function_point_analysis:
  transaction_functions:
    external_inputs:
      description: "Data entering system boundary"
      examples:
        - "User registration form"
        - "Order submission"
        - "File upload"
      complexity_factors:
        low: 3
        average: 4
        high: 6

    external_outputs:
      description: "Data leaving system boundary"
      examples:
        - "Report generation"
        - "Invoice PDF"
        - "Email notification"
      complexity_factors:
        low: 4
        average: 5
        high: 7

    external_inquiries:
      description: "Input/output combination for retrieval"
      examples:
        - "Search results"
        - "User profile view"
        - "Order status lookup"
      complexity_factors:
        low: 3
        average: 4
        high: 6

  data_functions:
    internal_logical_files:
      description: "Logical data maintained within system"
      examples:
        - "Customer database"
        - "Product catalog"
        - "Transaction history"
      complexity_factors:
        low: 7
        average: 10
        high: 15

    external_interface_files:
      description: "Logical data referenced but maintained externally"
      examples:
        - "Third-party API data"
        - "Shared database tables"
        - "External configuration"
      complexity_factors:
        low: 5
        average: 7
        high: 10
```

### Function Point Calculator

```csharp
namespace EstimationPlanning.FunctionPoints;

/// <summary>
/// Function point analysis calculator.
/// </summary>
public sealed class FunctionPointCalculator
{
    /// <summary>
    /// Calculate unadjusted function points from component counts.
    /// </summary>
    public static int CalculateUnadjusted(FunctionPointCount counts)
    {
        var ufp = 0;

        // Transaction functions
        ufp += counts.ExternalInputs.Low * 3 +
               counts.ExternalInputs.Average * 4 +
               counts.ExternalInputs.High * 6;

        ufp += counts.ExternalOutputs.Low * 4 +
               counts.ExternalOutputs.Average * 5 +
               counts.ExternalOutputs.High * 7;

        ufp += counts.ExternalInquiries.Low * 3 +
               counts.ExternalInquiries.Average * 4 +
               counts.ExternalInquiries.High * 6;

        // Data functions
        ufp += counts.InternalLogicalFiles.Low * 7 +
               counts.InternalLogicalFiles.Average * 10 +
               counts.InternalLogicalFiles.High * 15;

        ufp += counts.ExternalInterfaceFiles.Low * 5 +
               counts.ExternalInterfaceFiles.Average * 7 +
               counts.ExternalInterfaceFiles.High * 10;

        return ufp;
    }

    /// <summary>
    /// Calculate value adjustment factor from general system characteristics.
    /// </summary>
    public static double CalculateVAF(GeneralSystemCharacteristics gsc)
    {
        var totalDegreeOfInfluence = gsc.DataCommunications +
                                      gsc.DistributedDataProcessing +
                                      gsc.Performance +
                                      gsc.HeavilyUsedConfiguration +
                                      gsc.TransactionRate +
                                      gsc.OnlineDataEntry +
                                      gsc.EndUserEfficiency +
                                      gsc.OnlineUpdate +
                                      gsc.ComplexProcessing +
                                      gsc.Reusability +
                                      gsc.InstallationEase +
                                      gsc.OperationalEase +
                                      gsc.MultipleSites +
                                      gsc.FacilitateChange;

        return 0.65 + (0.01 * totalDegreeOfInfluence);
    }

    /// <summary>
    /// Calculate adjusted function points.
    /// </summary>
    public static double CalculateAdjusted(int ufp, double vaf) => ufp * vaf;

    /// <summary>
    /// Estimate effort from function points using industry productivity.
    /// </summary>
    public static EffortEstimate EstimateEffort(
        double adjustedFP,
        double hoursPerFP = 10.0, // Industry average varies 5-15
        double uncertaintyFactor = 0.25)
    {
        var nominalHours = adjustedFP * hoursPerFP;
        var lowHours = nominalHours * (1 - uncertaintyFactor);
        var highHours = nominalHours * (1 + uncertaintyFactor);

        return new EffortEstimate(
            Low: TimeSpan.FromHours(lowHours),
            Nominal: TimeSpan.FromHours(nominalHours),
            High: TimeSpan.FromHours(highHours));
    }
}

public sealed record FunctionPointCount(
    ComplexityCount ExternalInputs,
    ComplexityCount ExternalOutputs,
    ComplexityCount ExternalInquiries,
    ComplexityCount InternalLogicalFiles,
    ComplexityCount ExternalInterfaceFiles);

public sealed record ComplexityCount(int Low, int Average, int High);

/// <summary>
/// General system characteristics rated 0-5 for degree of influence.
/// </summary>
public sealed record GeneralSystemCharacteristics(
    int DataCommunications,
    int DistributedDataProcessing,
    int Performance,
    int HeavilyUsedConfiguration,
    int TransactionRate,
    int OnlineDataEntry,
    int EndUserEfficiency,
    int OnlineUpdate,
    int ComplexProcessing,
    int Reusability,
    int InstallationEase,
    int OperationalEase,
    int MultipleSites,
    int FacilitateChange);

public sealed record EffortEstimate(
    TimeSpan Low,
    TimeSpan Nominal,
    TimeSpan High);
```

## PERT Estimation

### Three-Point Estimation

```yaml
pert_estimation:
  formula:
    expected: "(Optimistic + 4*MostLikely + Pessimistic) / 6"
    standard_deviation: "(Pessimistic - Optimistic) / 6"
    variance: "StandardDeviation^2"

  interpretation:
    optimistic: "Best case if everything goes right"
    most_likely: "Normal conditions, typical experience"
    pessimistic: "Worst case without catastrophe"

  confidence_intervals:
    68_percent: "Expected +/- 1 StdDev"
    95_percent: "Expected +/- 2 StdDev"
    99_percent: "Expected +/- 3 StdDev"

  aggregation:
    tasks:
      expected_total: "Sum of expected values"
      variance_total: "Sum of variances"
      stddev_total: "Square root of variance total"
```

### PERT Calculator

```csharp
namespace EstimationPlanning.PERT;

/// <summary>
/// PERT (Program Evaluation and Review Technique) estimation calculator.
/// </summary>
public static class PertCalculator
{
    /// <summary>
    /// Calculate PERT estimate from three-point estimate.
    /// </summary>
    public static PertEstimate Calculate(
        double optimistic,
        double mostLikely,
        double pessimistic)
    {
        if (optimistic > mostLikely || mostLikely > pessimistic)
        {
            throw new ArgumentException(
                "Estimates must satisfy: Optimistic <= MostLikely <= Pessimistic");
        }

        var expected = (optimistic + 4 * mostLikely + pessimistic) / 6;
        var standardDeviation = (pessimistic - optimistic) / 6;
        var variance = standardDeviation * standardDeviation;

        return new PertEstimate(
            Optimistic: optimistic,
            MostLikely: mostLikely,
            Pessimistic: pessimistic,
            Expected: expected,
            StandardDeviation: standardDeviation,
            Variance: variance,
            Confidence68Low: expected - standardDeviation,
            Confidence68High: expected + standardDeviation,
            Confidence95Low: expected - 2 * standardDeviation,
            Confidence95High: expected + 2 * standardDeviation);
    }

    /// <summary>
    /// Aggregate multiple PERT estimates for a project.
    /// </summary>
    public static PertAggregate Aggregate(IEnumerable<PertEstimate> estimates)
    {
        var list = estimates.ToList();
        var expectedTotal = list.Sum(e => e.Expected);
        var varianceTotal = list.Sum(e => e.Variance);
        var stdDevTotal = Math.Sqrt(varianceTotal);

        return new PertAggregate(
            TaskCount: list.Count,
            ExpectedTotal: expectedTotal,
            VarianceTotal: varianceTotal,
            StandardDeviationTotal: stdDevTotal,
            Confidence68Range: (expectedTotal - stdDevTotal, expectedTotal + stdDevTotal),
            Confidence95Range: (expectedTotal - 2 * stdDevTotal, expectedTotal + 2 * stdDevTotal));
    }
}

public sealed record PertEstimate(
    double Optimistic,
    double MostLikely,
    double Pessimistic,
    double Expected,
    double StandardDeviation,
    double Variance,
    double Confidence68Low,
    double Confidence68High,
    double Confidence95Low,
    double Confidence95High);

public sealed record PertAggregate(
    int TaskCount,
    double ExpectedTotal,
    double VarianceTotal,
    double StandardDeviationTotal,
    (double Low, double High) Confidence68Range,
    (double Low, double High) Confidence95Range);
```

## Estimation Calibration

### Historical Accuracy Tracking

```yaml
estimation_calibration:
  metrics_to_track:
    accuracy:
      formula: "Actual / Estimated"
      good_range: "0.8 - 1.2"

    bias:
      formula: "Average(Actual - Estimated)"
      interpretation:
        positive: "Consistent underestimation"
        negative: "Consistent overestimation"
        near_zero: "Well calibrated"

    precision:
      formula: "Standard deviation of accuracy"
      interpretation:
        low: "Consistent (good or bad)"
        high: "Inconsistent (unpredictable)"

  analysis_dimensions:
    by_estimator: "Individual calibration"
    by_story_size: "Accuracy per point range"
    by_technology: "Domain-specific accuracy"
    by_uncertainty: "Known vs unknown work"
    over_time: "Improvement tracking"

  improvement_actions:
    underestimation:
      - "Add buffer for unknowns"
      - "Include testing/review time"
      - "Account for context switching"
      - "Review scope creep patterns"

    overestimation:
      - "Update reference stories"
      - "Reduce risk padding"
      - "Trust team capabilities"

    high_variance:
      - "Improve story decomposition"
      - "Increase clarification before estimating"
      - "Use spikes for unknowns"
```

### Estimation Retrospective Template

```yaml
estimation_retrospective:
  sprint_summary:
    committed_points: 0
    completed_points: 0
    velocity_trend: ""

  accuracy_analysis:
    stories_significantly_under:
      - story_id: ""
        estimated: 0
        actual_effort: ""
        root_cause: ""

    stories_significantly_over:
      - story_id: ""
        estimated: 0
        actual_effort: ""
        root_cause: ""

  patterns_identified:
    underestimation_causes: []
    overestimation_causes: []
    scope_changes: []

  calibration_actions:
    - action: ""
      owner: ""
      deadline: ""

  reference_story_updates:
    new_references: []
    updated_references: []
```

## References

- **Monte Carlo Methods**: See `../monte-carlo-scheduling/` for probabilistic scheduling
- **Risk Assessment**: See `../risk-assessment/` for risk-adjusted estimation

## Related Skills

- `monte-carlo-scheduling` - Probabilistic schedule estimation
- `risk-assessment` - Risk identification and quantification
- `tech-debt-assessment` - Technical debt impact estimation

---

**Last Updated:** 2025-12-26
