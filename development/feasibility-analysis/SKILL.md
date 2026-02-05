---
name: feasibility-analysis
description: Technical, economic, operational, and schedule feasibility evaluation for proposed initiatives
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Feasibility Analysis Skill

## When to Use This Skill

Use this skill when:

- **Feasibility Analysis tasks** - Working on technical, economic, operational, and schedule feasibility evaluation for proposed initiatives
- **Planning or design** - Need guidance on Feasibility Analysis approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Comprehensive feasibility evaluation across technical, economic, operational, schedule, and legal dimensions for proposed projects and initiatives.

## MANDATORY: Documentation-First Approach

Before providing feasibility guidance:

1. **Invoke `docs-management` skill** for any framework-specific documentation
2. **Verify financial formulas** via MCP servers (perplexity for current practices)
3. **Base all guidance on established methodologies**

## Feasibility Dimensions

### The TELOS Framework

| Dimension | Focus | Key Questions |
|-----------|-------|---------------|
| **T**echnical | Can we build it? | Technology exists? Skills available? |
| **E**conomic | Should we build it? | ROI positive? Affordable? |
| **L**egal | Are we allowed? | Regulations? Contracts? IP? |
| **O**perational | Will it work? | Processes? Culture? Support? |
| **S**chedule | Can we deliver in time? | Constraints? Dependencies? |

### Feasibility Assessment Model

```csharp
public sealed record FeasibilityAssessment(
    string ProjectName,
    DateOnly AssessmentDate,
    TechnicalFeasibility Technical,
    EconomicFeasibility Economic,
    LegalFeasibility Legal,
    OperationalFeasibility Operational,
    ScheduleFeasibility Schedule,
    FeasibilityVerdict Verdict);

public enum FeasibilityRating
{
    NotFeasible,      // Fundamental blockers exist
    HighRisk,         // Feasible but with significant challenges
    Moderate,         // Feasible with manageable challenges
    LowRisk,          // Feasible with minor challenges
    HighlyFeasible    // Clear path to success
}

public sealed record FeasibilityVerdict(
    FeasibilityRating OverallRating,
    bool Recommended,
    IReadOnlyList<string> CriticalBlockers,
    IReadOnlyList<string> KeyRisks,
    IReadOnlyList<string> SuccessFactors,
    string ExecutiveSummary);
```

## Technical Feasibility

### Assessment Areas

```csharp
public sealed record TechnicalFeasibility(
    FeasibilityRating Rating,
    TechnologyReadiness TechReadiness,
    SkillsAssessment Skills,
    IntegrationComplexity Integration,
    ScalabilityAssessment Scalability,
    SecurityAssessment Security,
    IReadOnlyList<TechnicalRisk> Risks,
    IReadOnlyList<string> Recommendations);

public sealed record TechnologyReadiness(
    TechnologyMaturity Maturity,
    bool ProvenAtScale,
    bool TeamExperience,
    bool VendorSupport,
    bool CommunitySupport,
    int TRLLevel); // Technology Readiness Level 1-9

public enum TechnologyMaturity
{
    Bleeding,    // Experimental, no production use
    Emerging,    // Early adopters only
    Growing,     // Gaining traction, some production use
    Mature,      // Widely adopted, stable
    Declining    // Being replaced, limited future
}
```

### Technology Readiness Levels (TRL)

| TRL | Stage | Description |
|-----|-------|-------------|
| 1 | Basic Research | Fundamental principles observed |
| 2 | Applied Research | Concept formulated |
| 3 | Proof of Concept | Experimental validation |
| 4 | Lab Validation | Component validated in lab |
| 5 | Relevant Environment | Component validated in realistic setting |
| 6 | Prototype | System demonstrated in relevant environment |
| 7 | Operational Demo | System prototype in operational environment |
| 8 | System Complete | System qualified through testing |
| 9 | Mission Proven | System proven in successful operations |

### Technical Feasibility Checklist

```csharp
public sealed class TechnicalFeasibilityEvaluator
{
    public TechnicalFeasibility Evaluate(TechnicalRequirements requirements)
    {
        var checks = new List<(string Area, bool Pass, string Notes)>
        {
            // Technology Stack
            ("Required technology exists", CheckTechnologyExists(requirements), ""),
            ("Technology is mature enough", CheckMaturity(requirements), ""),
            ("Technology has vendor support", CheckVendorSupport(requirements), ""),

            // Skills & Resources
            ("Team has required skills", CheckTeamSkills(requirements), ""),
            ("Training is feasible", CheckTrainingFeasibility(requirements), ""),
            ("External expertise available", CheckExternalExpertise(requirements), ""),

            // Integration
            ("Can integrate with existing systems", CheckIntegration(requirements), ""),
            ("APIs/interfaces are available", CheckAPIs(requirements), ""),
            ("Data migration is feasible", CheckDataMigration(requirements), ""),

            // Performance & Scale
            ("Can meet performance requirements", CheckPerformance(requirements), ""),
            ("Can scale to required levels", CheckScalability(requirements), ""),
            ("Infrastructure is available", CheckInfrastructure(requirements), ""),

            // Security & Compliance
            ("Security requirements achievable", CheckSecurity(requirements), ""),
            ("Compliance requirements achievable", CheckCompliance(requirements), "")
        };

        var passRate = (double)checks.Count(c => c.Pass) / checks.Count;
        var rating = passRate switch
        {
            >= 0.9 => FeasibilityRating.HighlyFeasible,
            >= 0.7 => FeasibilityRating.LowRisk,
            >= 0.5 => FeasibilityRating.Moderate,
            >= 0.3 => FeasibilityRating.HighRisk,
            _ => FeasibilityRating.NotFeasible
        };

        return BuildTechnicalFeasibility(rating, checks);
    }
}
```

## Economic Feasibility

### Financial Analysis

```csharp
public sealed record EconomicFeasibility(
    FeasibilityRating Rating,
    CostEstimate TotalCost,
    BenefitEstimate TotalBenefit,
    FinancialMetrics Metrics,
    FundingAssessment Funding,
    IReadOnlyList<EconomicRisk> Risks,
    IReadOnlyList<string> Recommendations);

public sealed record CostEstimate(
    decimal DevelopmentCost,
    decimal ImplementationCost,
    decimal AnnualOperatingCost,
    decimal TrainingCost,
    decimal ContingencyReserve,
    decimal TotalCostOfOwnership, // TCO over 3-5 years
    IReadOnlyList<CostLineItem> LineItems);

public sealed record BenefitEstimate(
    decimal AnnualCostSavings,
    decimal AnnualRevenueIncrease,
    decimal ProductivityGains,
    decimal RiskReduction,
    decimal IntangibleBenefits,
    decimal TotalAnnualBenefit,
    IReadOnlyList<BenefitLineItem> LineItems);
```

### Financial Metrics Calculation

```csharp
public sealed class FinancialMetricsCalculator
{
    public FinancialMetrics Calculate(
        CostEstimate costs,
        BenefitEstimate benefits,
        int projectYears = 5,
        double discountRate = 0.10)
    {
        var initialInvestment = costs.DevelopmentCost + costs.ImplementationCost;
        var annualCashFlow = benefits.TotalAnnualBenefit - costs.AnnualOperatingCost;

        // ROI = (Total Benefits - Total Costs) / Total Costs × 100
        var totalBenefits = benefits.TotalAnnualBenefit * projectYears;
        var totalCosts = initialInvestment + (costs.AnnualOperatingCost * projectYears);
        var roi = (totalBenefits - totalCosts) / totalCosts * 100;

        // Simple Payback Period = Initial Investment / Annual Cash Flow
        var paybackPeriod = annualCashFlow > 0
            ? initialInvestment / annualCashFlow
            : decimal.MaxValue;

        // NPV = Σ (Cash Flow / (1 + r)^t) - Initial Investment
        var npv = CalculateNPV(initialInvestment, annualCashFlow, projectYears, discountRate);

        // IRR (iterative calculation)
        var irr = CalculateIRR(initialInvestment, annualCashFlow, projectYears);

        return new FinancialMetrics(
            ROI: roi,
            PaybackPeriodYears: paybackPeriod,
            NPV: npv,
            IRR: irr,
            BreakEvenMonth: (int)(paybackPeriod * 12),
            CostBenefitRatio: totalBenefits / totalCosts);
    }

    private decimal CalculateNPV(
        decimal initialInvestment,
        decimal annualCashFlow,
        int years,
        double discountRate)
    {
        decimal npv = -initialInvestment;
        for (int t = 1; t <= years; t++)
        {
            npv += annualCashFlow / (decimal)Math.Pow(1 + discountRate, t);
        }
        return npv;
    }

    private double CalculateIRR(
        decimal initialInvestment,
        decimal annualCashFlow,
        int years)
    {
        // Newton-Raphson iteration to find IRR
        double irr = 0.10; // Initial guess
        for (int i = 0; i < 100; i++)
        {
            double npv = -(double)initialInvestment;
            double derivative = 0;

            for (int t = 1; t <= years; t++)
            {
                double discountFactor = Math.Pow(1 + irr, t);
                npv += (double)annualCashFlow / discountFactor;
                derivative -= t * (double)annualCashFlow / Math.Pow(1 + irr, t + 1);
            }

            if (Math.Abs(npv) < 0.01) break;
            irr = irr - npv / derivative;
        }
        return irr;
    }
}

public sealed record FinancialMetrics(
    decimal ROI,                // Return on Investment %
    decimal PaybackPeriodYears, // Years to recoup investment
    decimal NPV,                // Net Present Value
    double IRR,                 // Internal Rate of Return
    int BreakEvenMonth,         // Month when cumulative benefits exceed costs
    decimal CostBenefitRatio);  // Benefits / Costs
```

### Economic Decision Criteria

```csharp
public static class EconomicDecisionCriteria
{
    public static FeasibilityRating EvaluateMetrics(FinancialMetrics metrics)
    {
        // Typical thresholds (adjust for organization)
        var roiOk = metrics.ROI >= 20;           // 20%+ ROI
        var paybackOk = metrics.PaybackPeriodYears <= 3; // 3 years max
        var npvPositive = metrics.NPV > 0;       // Positive NPV
        var irrOk = metrics.IRR >= 0.10;         // 10%+ IRR

        var passCount = new[] { roiOk, paybackOk, npvPositive, irrOk }.Count(p => p);

        return passCount switch
        {
            4 => FeasibilityRating.HighlyFeasible,
            3 => FeasibilityRating.LowRisk,
            2 => FeasibilityRating.Moderate,
            1 => FeasibilityRating.HighRisk,
            _ => FeasibilityRating.NotFeasible
        };
    }
}
```

## Operational Feasibility

### Organizational Readiness

```csharp
public sealed record OperationalFeasibility(
    FeasibilityRating Rating,
    OrganizationalReadiness OrgReadiness,
    ProcessFit ProcessFit,
    ChangeManagement ChangeManagement,
    SupportModel SupportModel,
    IReadOnlyList<OperationalRisk> Risks,
    IReadOnlyList<string> Recommendations);

public sealed record OrganizationalReadiness(
    StakeholderSupport ExecutiveSupport,
    StakeholderSupport UserSupport,
    CultureAlignment CultureFit,
    bool ClearOwnership,
    bool AdequateResources);

public enum StakeholderSupport
{
    Champion,    // Active advocate
    Supporter,   // Positive, will help
    Neutral,     // Neither supports nor opposes
    Skeptic,     // Doubtful, needs convincing
    Opponent     // Actively resisting
}

public sealed record ProcessFit(
    bool AlignsWithCurrentProcesses,
    int ProcessChangesRequired,
    IReadOnlyList<string> AffectedDepartments,
    IReadOnlyList<string> RequiredPolicyChanges);

public sealed record ChangeManagement(
    int AffectedUsers,
    TrainingComplexity TrainingNeeds,
    TimeSpan TransitionPeriod,
    bool ParallelOperationRequired);
```

### Operational Feasibility Checklist

| Factor | Questions |
|--------|-----------|
| User Acceptance | Will end users accept and use the solution? |
| Process Alignment | Does it fit existing workflows or require changes? |
| Support Capability | Can the organization support and maintain it? |
| Cultural Fit | Is it compatible with organizational culture? |
| Change Capacity | Can the organization absorb this change now? |
| Training Needs | Can users be trained effectively? |
| Data Governance | Are data ownership and stewardship clear? |

## Schedule Feasibility

### Timeline Analysis

```csharp
public sealed record ScheduleFeasibility(
    FeasibilityRating Rating,
    TimeSpan EstimatedDuration,
    DateOnly TargetDeadline,
    DateOnly RealisticCompletion,
    ScheduleBuffer Buffer,
    IReadOnlyList<ScheduleConstraint> Constraints,
    IReadOnlyList<CriticalDependency> Dependencies,
    IReadOnlyList<ScheduleRisk> Risks,
    IReadOnlyList<string> Recommendations);

public sealed record ScheduleBuffer(
    TimeSpan TotalBuffer,
    double BufferPercentage,
    BufferAdequacy Adequacy);

public enum BufferAdequacy
{
    Insufficient, // <10% buffer
    Tight,        // 10-20% buffer
    Adequate,     // 20-30% buffer
    Comfortable   // >30% buffer
}

public sealed record ScheduleConstraint(
    string Name,
    ConstraintType Type,
    DateOnly? FixedDate,
    string Impact);

public enum ConstraintType
{
    HardDeadline,        // Cannot be moved
    ExternalDependency,  // Outside our control
    ResourceAvailability,
    RegulatoryMilestone,
    MarketWindow,
    ContractObligation
}
```

### Schedule Feasibility Evaluation

```csharp
public sealed class ScheduleFeasibilityEvaluator
{
    public ScheduleFeasibility Evaluate(
        TimeSpan estimatedDuration,
        DateOnly targetDeadline,
        IReadOnlyList<ScheduleConstraint> constraints,
        IReadOnlyList<CriticalDependency> dependencies)
    {
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        var availableTime = targetDeadline.DayNumber - today.DayNumber;
        var requiredDays = estimatedDuration.Days;

        var bufferDays = availableTime - requiredDays;
        var bufferPercentage = (double)bufferDays / requiredDays * 100;

        var adequacy = bufferPercentage switch
        {
            < 10 => BufferAdequacy.Insufficient,
            < 20 => BufferAdequacy.Tight,
            < 30 => BufferAdequacy.Adequate,
            _ => BufferAdequacy.Comfortable
        };

        // Check hard constraints
        var hardDeadlines = constraints
            .Where(c => c.Type == ConstraintType.HardDeadline)
            .ToList();

        var realisticCompletion = today.AddDays(requiredDays);
        var meetsDeadline = realisticCompletion <= targetDeadline;

        var rating = (meetsDeadline, adequacy) switch
        {
            (false, _) => FeasibilityRating.NotFeasible,
            (true, BufferAdequacy.Insufficient) => FeasibilityRating.HighRisk,
            (true, BufferAdequacy.Tight) => FeasibilityRating.Moderate,
            (true, BufferAdequacy.Adequate) => FeasibilityRating.LowRisk,
            (true, BufferAdequacy.Comfortable) => FeasibilityRating.HighlyFeasible
        };

        return new ScheduleFeasibility(
            Rating: rating,
            EstimatedDuration: estimatedDuration,
            TargetDeadline: targetDeadline,
            RealisticCompletion: realisticCompletion,
            Buffer: new ScheduleBuffer(
                TimeSpan.FromDays(bufferDays),
                bufferPercentage,
                adequacy),
            Constraints: constraints,
            Dependencies: dependencies,
            Risks: IdentifyScheduleRisks(constraints, dependencies),
            Recommendations: GenerateScheduleRecommendations(rating, adequacy));
    }
}
```

## Legal Feasibility

### Compliance Assessment

```csharp
public sealed record LegalFeasibility(
    FeasibilityRating Rating,
    RegulatoryCompliance Regulatory,
    ContractualConstraints Contracts,
    IntellectualProperty IP,
    DataPrivacy Privacy,
    IReadOnlyList<LegalRisk> Risks,
    IReadOnlyList<string> Recommendations);

public sealed record RegulatoryCompliance(
    IReadOnlyList<Regulation> ApplicableRegulations,
    bool AllRequirementsMet,
    IReadOnlyList<ComplianceGap> Gaps,
    DateOnly? CertificationDeadline);

public sealed record IntellectualProperty(
    bool PatentSearchCompleted,
    bool NoPatentInfringement,
    bool LicenseCompliance,
    IReadOnlyList<IPRisk> Risks);

public sealed record DataPrivacy(
    IReadOnlyList<string> JurisdictionsAffected,
    bool GDPRApplicable,
    bool CCPAApplicable,
    bool DataProcessingLegal,
    IReadOnlyList<PrivacyRequirement> Requirements);
```

## Feasibility Report Template

### Report Structure

```csharp
public sealed class FeasibilityReportGenerator
{
    public FeasibilityReport Generate(FeasibilityAssessment assessment)
    {
        return new FeasibilityReport(
            Title: $"Feasibility Study: {assessment.ProjectName}",
            Date: assessment.AssessmentDate,
            Sections: new[]
            {
                new ReportSection("Executive Summary", GenerateExecutiveSummary(assessment)),
                new ReportSection("Technical Feasibility", FormatTechnical(assessment.Technical)),
                new ReportSection("Economic Feasibility", FormatEconomic(assessment.Economic)),
                new ReportSection("Operational Feasibility", FormatOperational(assessment.Operational)),
                new ReportSection("Schedule Feasibility", FormatSchedule(assessment.Schedule)),
                new ReportSection("Legal Feasibility", FormatLegal(assessment.Legal)),
                new ReportSection("Risk Summary", FormatRiskSummary(assessment)),
                new ReportSection("Recommendations", FormatRecommendations(assessment)),
                new ReportSection("Conclusion", FormatConclusion(assessment.Verdict))
            });
    }
}
```

## Workflow

When conducting feasibility analysis:

1. **Define Scope**: Clarify what is being assessed and decision criteria
2. **Gather Requirements**: Collect technical, business, and operational requirements
3. **Assess Each Dimension**: Evaluate TELOS systematically
4. **Calculate Metrics**: Compute financial and other quantitative measures
5. **Identify Risks**: Document risks in each feasibility area
6. **Form Verdict**: Synthesize findings into go/no-go recommendation
7. **Document**: Create feasibility report with recommendations
8. **Present**: Communicate findings to stakeholders

## References

For detailed templates and examples:

---

**Last Updated:** 2025-12-26
