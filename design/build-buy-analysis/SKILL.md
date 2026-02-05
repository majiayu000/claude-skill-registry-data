---
name: build-buy-analysis
description: Make vs buy vs open source decision frameworks for technology and component acquisition
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Build vs Buy Analysis Skill

## When to Use This Skill

Use this skill when:

- **Build Buy Analysis tasks** - Working on make vs buy vs open source decision frameworks for technology and component acquisition
- **Planning or design** - Need guidance on Build Buy Analysis approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Structured decision frameworks for evaluating whether to build custom solutions, buy commercial products, or leverage open source components.

## MANDATORY: Documentation-First Approach

Before providing build/buy guidance:

1. **Invoke `docs-management` skill** for methodology documentation
2. **Verify vendor claims** via MCP servers (perplexity for market analysis, product reviews)
3. **Base all guidance on established decision frameworks**

## Decision Options

### The Build-Buy-OSS Spectrum

```text
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Build        │  Hybrid        │  OSS          │  Buy          │
│  Custom       │                │  Open Source  │  Commercial   │
│                                                                 │
│  ◄────────────────────────────────────────────────────────────► │
│  Full Control                              Minimal Maintenance  │
│  High Effort                                     Vendor Risk    │
│  Differentiating                          Commodity/Solved      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Option Definitions

```csharp
public enum AcquisitionOption
{
    BuildCustom,     // Develop from scratch in-house
    BuildOnPlatform, // Custom development on commercial platform
    OpenSource,      // Adopt open source solution
    OSSWithSupport,  // Open source with commercial support
    SaaS,            // Software as a Service
    COTS,            // Commercial off-the-shelf (on-premise)
    Outsource        // Custom development by third party
}

public sealed record AcquisitionAnalysis(
    string ComponentName,
    string BusinessNeed,
    IReadOnlyList<AcquisitionOption> OptionsAnalyzed,
    IReadOnlyList<OptionEvaluation> Evaluations,
    AcquisitionOption RecommendedOption,
    string Rationale,
    IReadOnlyList<string> Assumptions,
    IReadOnlyList<string> Risks,
    DecisionConfidence Confidence);

public enum DecisionConfidence
{
    High,      // Clear winner, well-understood domain
    Medium,    // Good option, some uncertainty
    Low,       // Close call, significant unknowns
    NeedsMore  // Insufficient information to decide
}
```

## Strategic Fit Analysis

### Core vs Context Framework

```csharp
public enum BusinessClassification
{
    Core,             // Competitive differentiator, strategic advantage
    CoreSupporting,   // Enables core but not differentiating
    Context,          // Necessary but not differentiating
    Commodity         // Utility, widely available
}

public sealed class StrategicFitAnalyzer
{
    public AcquisitionOption RecommendByStrategicFit(
        BusinessClassification classification,
        TimeToMarket timeToMarket,
        SkillsAvailability skills)
    {
        return classification switch
        {
            // Core: Build to control, differentiate
            BusinessClassification.Core when skills == SkillsAvailability.Available
                => AcquisitionOption.BuildCustom,
            BusinessClassification.Core
                => AcquisitionOption.BuildOnPlatform,

            // Core Supporting: Build if feasible, else buy with customization
            BusinessClassification.CoreSupporting when timeToMarket == TimeToMarket.Urgent
                => AcquisitionOption.SaaS,
            BusinessClassification.CoreSupporting
                => AcquisitionOption.OpenSource,

            // Context: Buy or use OSS
            BusinessClassification.Context
                => AcquisitionOption.SaaS,

            // Commodity: Buy the cheapest reliable option
            BusinessClassification.Commodity
                => AcquisitionOption.SaaS,

            _ => AcquisitionOption.OpenSource
        };
    }
}

public enum TimeToMarket
{
    Flexible,   // Months to years acceptable
    Normal,     // Weeks to months
    Urgent,     // Days to weeks
    Immediate   // Need it now
}

public enum SkillsAvailability
{
    Available,     // Team has skills and capacity
    Acquirable,    // Can hire or train in reasonable time
    Scarce,        // Difficult to obtain
    NotAvailable   // Cannot obtain
}
```

### Decision Matrix

| Classification | Build | Buy | OSS |
|----------------|-------|-----|-----|
| Core + Skills Available | ✅ Recommended | ⚠️ Risk | ⚠️ If excellent fit |
| Core + No Skills | ⚠️ With outsource | ✅ Platform | ✅ With support |
| Core Supporting | ⚠️ If simple | ✅ Recommended | ✅ Recommended |
| Context | ❌ Rarely | ✅ SaaS preferred | ⚠️ If mature |
| Commodity | ❌ Never | ✅ Commodity | ⚠️ If mature |

## Total Cost of Ownership

### TCO Model

```csharp
public sealed record TotalCostOfOwnership(
    string Option,
    decimal InitialCost,
    decimal AnnualOperatingCost,
    decimal TCOYears3,
    decimal TCOYears5,
    IReadOnlyList<CostLineItem> CostBreakdown);

public sealed record CostLineItem(
    string Category,
    CostType Type,
    decimal Amount,
    string Period,
    string Notes);

public enum CostType
{
    OneTime,
    Recurring,
    Variable
}

public sealed class TCOCalculator
{
    public TotalCostOfOwnership CalculateBuildTCO(BuildCostInputs inputs, int years)
    {
        var costs = new List<CostLineItem>();

        // Initial Development
        costs.Add(new CostLineItem(
            "Development",
            CostType.OneTime,
            inputs.DevelopmentHours * inputs.HourlyRate,
            "Initial",
            $"{inputs.DevelopmentHours} hours @ ${inputs.HourlyRate}/hr"));

        // Infrastructure Setup
        costs.Add(new CostLineItem(
            "Infrastructure Setup",
            CostType.OneTime,
            inputs.InfrastructureSetupCost,
            "Initial",
            "Servers, cloud setup, environments"));

        // Annual Maintenance (15-20% of development cost)
        var maintenanceCost = inputs.DevelopmentHours * inputs.HourlyRate * 0.18m;
        costs.Add(new CostLineItem(
            "Maintenance",
            CostType.Recurring,
            maintenanceCost,
            "Annual",
            "Bug fixes, updates, tech debt"));

        // Annual Infrastructure
        costs.Add(new CostLineItem(
            "Infrastructure",
            CostType.Recurring,
            inputs.AnnualInfrastructureCost,
            "Annual",
            "Cloud/hosting, monitoring"));

        // Annual Support/Operations
        costs.Add(new CostLineItem(
            "Operations",
            CostType.Recurring,
            inputs.AnnualOperationsCost,
            "Annual",
            "DevOps, SRE, on-call"));

        var initial = costs.Where(c => c.Type == CostType.OneTime).Sum(c => c.Amount);
        var annual = costs.Where(c => c.Type == CostType.Recurring).Sum(c => c.Amount);

        return new TotalCostOfOwnership(
            Option: "Build",
            InitialCost: initial,
            AnnualOperatingCost: annual,
            TCOYears3: initial + annual * 3,
            TCOYears5: initial + annual * 5,
            CostBreakdown: costs);
    }

    public TotalCostOfOwnership CalculateBuyTCO(BuyCostInputs inputs, int years)
    {
        var costs = new List<CostLineItem>();

        // License/Subscription
        if (inputs.IsSubscription)
        {
            costs.Add(new CostLineItem(
                "Subscription",
                CostType.Recurring,
                inputs.AnnualLicenseCost,
                "Annual",
                $"{inputs.Users} users @ ${inputs.PerUserCost}/user/year"));
        }
        else
        {
            costs.Add(new CostLineItem(
                "License",
                CostType.OneTime,
                inputs.PerpetualLicenseCost,
                "Initial",
                "Perpetual license"));

            costs.Add(new CostLineItem(
                "Maintenance",
                CostType.Recurring,
                inputs.PerpetualLicenseCost * 0.20m,
                "Annual",
                "20% annual maintenance"));
        }

        // Implementation
        costs.Add(new CostLineItem(
            "Implementation",
            CostType.OneTime,
            inputs.ImplementationCost,
            "Initial",
            "Configuration, customization, integration"));

        // Training
        costs.Add(new CostLineItem(
            "Training",
            CostType.OneTime,
            inputs.TrainingCost,
            "Initial",
            $"Training for {inputs.Users} users"));

        // Integration/Customization
        costs.Add(new CostLineItem(
            "Integration",
            CostType.Recurring,
            inputs.AnnualIntegrationCost,
            "Annual",
            "Ongoing integration maintenance"));

        var initial = costs.Where(c => c.Type == CostType.OneTime).Sum(c => c.Amount);
        var annual = costs.Where(c => c.Type == CostType.Recurring).Sum(c => c.Amount);

        return new TotalCostOfOwnership(
            Option: "Buy",
            InitialCost: initial,
            AnnualOperatingCost: annual,
            TCOYears3: initial + annual * 3,
            TCOYears5: initial + annual * 5,
            CostBreakdown: costs);
    }

    public TotalCostOfOwnership CalculateOSSTCO(OSSCostInputs inputs, int years)
    {
        var costs = new List<CostLineItem>();

        // No license cost (but maybe support contract)
        if (inputs.SupportContractCost > 0)
        {
            costs.Add(new CostLineItem(
                "Support Contract",
                CostType.Recurring,
                inputs.SupportContractCost,
                "Annual",
                "Commercial support subscription"));
        }

        // Implementation/Integration
        costs.Add(new CostLineItem(
            "Implementation",
            CostType.OneTime,
            inputs.ImplementationHours * inputs.HourlyRate,
            "Initial",
            "Integration, configuration, customization"));

        // Expertise Development
        costs.Add(new CostLineItem(
            "Training/Expertise",
            CostType.OneTime,
            inputs.ExpertiseDevelopmentCost,
            "Initial",
            "Learning curve, training"));

        // Annual Maintenance (often higher than commercial - you own it)
        costs.Add(new CostLineItem(
            "Maintenance",
            CostType.Recurring,
            inputs.AnnualMaintenanceHours * inputs.HourlyRate,
            "Annual",
            "Upgrades, security patches, customizations"));

        // Community Contribution (optional)
        if (inputs.ContributionHoursAnnual > 0)
        {
            costs.Add(new CostLineItem(
                "Community Contribution",
                CostType.Recurring,
                inputs.ContributionHoursAnnual * inputs.HourlyRate,
                "Annual",
                "Contributing back to project"));
        }

        var initial = costs.Where(c => c.Type == CostType.OneTime).Sum(c => c.Amount);
        var annual = costs.Where(c => c.Type == CostType.Recurring).Sum(c => c.Amount);

        return new TotalCostOfOwnership(
            Option: "Open Source",
            InitialCost: initial,
            AnnualOperatingCost: annual,
            TCOYears3: initial + annual * 3,
            TCOYears5: initial + annual * 5,
            CostBreakdown: costs);
    }
}
```

## Evaluation Criteria

### Weighted Scoring Model

```csharp
public sealed record EvaluationCriterion(
    string Name,
    string Description,
    double Weight,      // 0-1, all weights sum to 1
    CriterionCategory Category);

public enum CriterionCategory
{
    Cost,
    Functionality,
    Technical,
    Vendor,
    Risk,
    Strategic
}

public sealed class BuildBuyEvaluator
{
    public static IReadOnlyList<EvaluationCriterion> StandardCriteria { get; } = new[]
    {
        // Cost (25% total)
        new EvaluationCriterion("Initial Cost", "Upfront investment required", 0.10, CriterionCategory.Cost),
        new EvaluationCriterion("Ongoing Cost", "Annual operating cost", 0.10, CriterionCategory.Cost),
        new EvaluationCriterion("Hidden Costs", "Integration, training, opportunity cost", 0.05, CriterionCategory.Cost),

        // Functionality (25% total)
        new EvaluationCriterion("Feature Fit", "How well requirements are met", 0.15, CriterionCategory.Functionality),
        new EvaluationCriterion("Customizability", "Ability to adapt to specific needs", 0.10, CriterionCategory.Functionality),

        // Technical (20% total)
        new EvaluationCriterion("Integration", "Ease of integration with existing systems", 0.10, CriterionCategory.Technical),
        new EvaluationCriterion("Scalability", "Ability to grow with needs", 0.05, CriterionCategory.Technical),
        new EvaluationCriterion("Security", "Security posture and compliance", 0.05, CriterionCategory.Technical),

        // Vendor/Community (15% total)
        new EvaluationCriterion("Viability", "Long-term stability of vendor/project", 0.08, CriterionCategory.Vendor),
        new EvaluationCriterion("Support", "Quality of support available", 0.07, CriterionCategory.Vendor),

        // Risk (10% total)
        new EvaluationCriterion("Lock-in Risk", "Difficulty of switching later", 0.05, CriterionCategory.Risk),
        new EvaluationCriterion("Execution Risk", "Risk of failed implementation", 0.05, CriterionCategory.Risk),

        // Strategic (5% total)
        new EvaluationCriterion("Strategic Value", "Alignment with strategy, differentiation", 0.05, CriterionCategory.Strategic)
    };

    public OptionEvaluation Evaluate(
        AcquisitionOption option,
        IReadOnlyDictionary<string, int> scores) // criterion name -> score (1-5)
    {
        var weightedScore = StandardCriteria
            .Sum(c => c.Weight * scores.GetValueOrDefault(c.Name, 3));

        var categoryScores = StandardCriteria
            .GroupBy(c => c.Category)
            .ToDictionary(
                g => g.Key,
                g => g.Sum(c => c.Weight * scores.GetValueOrDefault(c.Name, 3)) /
                     g.Sum(c => c.Weight));

        return new OptionEvaluation(
            Option: option,
            WeightedScore: weightedScore,
            CategoryScores: categoryScores,
            Strengths: IdentifyStrengths(scores),
            Weaknesses: IdentifyWeaknesses(scores));
    }
}
```

## Vendor Evaluation

### Vendor Assessment Framework

```csharp
public sealed record VendorEvaluation(
    string VendorName,
    string Product,
    VendorViability Viability,
    ProductMaturity Maturity,
    SupportQuality Support,
    ContractTerms Terms,
    IReadOnlyList<string> RedFlags,
    IReadOnlyList<string> Strengths,
    VendorRisk OverallRisk);

public sealed record VendorViability(
    decimal AnnualRevenue,
    int YearsInBusiness,
    int TotalCustomers,
    int CustomersInYourIndustry,
    FundingStatus Funding,
    bool PubliclyTraded,
    MarketPosition Position);

public enum FundingStatus
{
    Bootstrapped,
    SeedFunded,
    VentureCapital,
    PrivateEquity,
    PubliclyTraded,
    Acquired
}

public enum MarketPosition
{
    Leader,
    Challenger,
    Niche,
    Emerging,
    Declining
}

public sealed class VendorRiskAssessor
{
    public VendorRisk AssessRisk(VendorViability viability)
    {
        var riskFactors = new List<string>();

        // Company size/stability
        if (viability.YearsInBusiness < 3)
            riskFactors.Add("Company less than 3 years old");
        if (viability.TotalCustomers < 100)
            riskFactors.Add("Limited customer base");

        // Financial health
        if (viability.Funding == FundingStatus.SeedFunded)
            riskFactors.Add("Early-stage funding - viability uncertain");

        // Market position
        if (viability.Position == MarketPosition.Declining)
            riskFactors.Add("Declining market position");
        if (viability.Position == MarketPosition.Emerging && viability.TotalCustomers < 50)
            riskFactors.Add("Emerging vendor with limited track record");

        return new VendorRisk(
            Level: riskFactors.Count switch
            {
                0 => RiskLevel.Low,
                1 or 2 => RiskLevel.Medium,
                _ => RiskLevel.High
            },
            Factors: riskFactors);
    }
}
```

## Open Source Evaluation

### OSS Health Assessment

```csharp
public sealed record OSSProjectHealth(
    string ProjectName,
    string Repository,
    OSSMetrics Metrics,
    CommunityHealth Community,
    SecurityPosture Security,
    LicenseAnalysis License,
    IReadOnlyList<string> Risks,
    OSSHealthRating Rating);

public sealed record OSSMetrics(
    int Stars,
    int Forks,
    int Contributors,
    int OpenIssues,
    int ClosedIssues,
    TimeSpan AverageIssueResolutionTime,
    DateOnly LastCommit,
    int CommitsLastYear,
    int ReleasesLastYear);

public sealed record CommunityHealth(
    bool HasCodeOfConduct,
    bool HasContributorGuidelines,
    bool ResponsiveToIssues,
    bool ActiveMaintainers,
    int MaintainerCount,
    bool HasDiscussionForum,
    bool HasDocumentation);

public sealed record LicenseAnalysis(
    string License,
    LicenseType Type,
    bool CommercialUsageAllowed,
    bool PatentGranted,
    bool CopyleftRequired,
    IReadOnlyList<string> Obligations);

public enum LicenseType
{
    Permissive,     // MIT, Apache, BSD
    WeakCopyleft,   // LGPL, MPL
    StrongCopyleft, // GPL, AGPL
    Proprietary,
    Unknown
}

public sealed class OSSEvaluator
{
    public OSSHealthRating Evaluate(OSSMetrics metrics, CommunityHealth community)
    {
        var score = 0;

        // Activity (0-30)
        score += metrics.CommitsLastYear > 100 ? 20 : metrics.CommitsLastYear / 5;
        score += metrics.ReleasesLastYear >= 4 ? 10 : metrics.ReleasesLastYear * 2;

        // Popularity/Adoption (0-20)
        score += Math.Min(10, metrics.Stars / 1000);
        score += Math.Min(10, metrics.Contributors / 10);

        // Maintenance (0-25)
        var daysSinceCommit = (DateOnly.FromDateTime(DateTime.UtcNow) - metrics.LastCommit).Days;
        score += daysSinceCommit < 30 ? 15 : daysSinceCommit < 90 ? 10 : 0;
        score += community.ActiveMaintainers ? 10 : 0;

        // Community (0-25)
        score += community.HasDocumentation ? 10 : 0;
        score += community.ResponsiveToIssues ? 10 : 0;
        score += community.MaintainerCount > 2 ? 5 : 0;

        return score switch
        {
            >= 80 => OSSHealthRating.Excellent,
            >= 60 => OSSHealthRating.Good,
            >= 40 => OSSHealthRating.Fair,
            >= 20 => OSSHealthRating.Poor,
            _ => OSSHealthRating.Risky
        };
    }
}

public enum OSSHealthRating
{
    Excellent,  // Active, well-maintained, strong community
    Good,       // Healthy with minor concerns
    Fair,       // Some red flags but usable
    Poor,       // Significant concerns
    Risky       // High risk of abandonment
}
```

## Decision Framework

### Decision Tree

```csharp
public sealed class BuildBuyDecisionTree
{
    public AcquisitionOption Recommend(DecisionContext context)
    {
        // Step 1: Strategic classification
        if (context.Classification == BusinessClassification.Core)
        {
            // Core capabilities: lean toward build
            if (context.Skills == SkillsAvailability.Available &&
                context.TimeToMarket != TimeToMarket.Urgent)
                return AcquisitionOption.BuildCustom;

            if (context.TimeToMarket == TimeToMarket.Urgent)
                return AcquisitionOption.BuildOnPlatform;
        }

        // Step 2: Check if good commercial options exist
        if (context.CommercialOptions.Any(o => o.FeatureFit >= 0.8))
        {
            // Good commercial fit exists
            if (context.Classification >= BusinessClassification.Context)
                return AcquisitionOption.SaaS;
        }

        // Step 3: Check if good OSS options exist
        if (context.OSSOptions.Any(o => o.Rating >= OSSHealthRating.Good))
        {
            var bestOSS = context.OSSOptions.OrderByDescending(o => o.Rating).First();
            return bestOSS.HasCommercialSupport
                ? AcquisitionOption.OSSWithSupport
                : AcquisitionOption.OpenSource;
        }

        // Step 4: No good options - must build
        if (context.Skills == SkillsAvailability.Available)
            return AcquisitionOption.BuildCustom;

        return AcquisitionOption.Outsource;
    }
}
```

## Workflow

When conducting build-buy analysis:

1. **Define Need**: Clarify business requirements and constraints
2. **Classify Strategically**: Core, supporting, context, or commodity?
3. **Identify Options**: What build, buy, and OSS options exist?
4. **Estimate TCO**: Calculate total cost for each option
5. **Evaluate Criteria**: Score each option against weighted criteria
6. **Assess Risks**: Vendor viability, lock-in, execution risks
7. **Compare**: Side-by-side analysis with visualization
8. **Decide**: Make recommendation with rationale
9. **Document**: Record decision and assumptions

## References

For detailed templates:

---

**Last Updated:** 2025-12-26
