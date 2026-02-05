---
name: technology-assessment
description: Technology radar positioning, evaluation criteria, and adoption recommendations for technology decisions
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Technology Assessment Skill

## When to Use This Skill

Use this skill when:

- **Technology Assessment tasks** - Working on technology radar positioning, evaluation criteria, and adoption recommendations for technology decisions
- **Planning or design** - Need guidance on Technology Assessment approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Structured technology evaluation using radar positioning, maturity analysis, and adoption recommendations for informed technology decisions.

## MANDATORY: Documentation-First Approach

Before providing technology assessment guidance:

1. **Invoke `docs-management` skill** for methodology documentation
2. **ALWAYS verify technology status** via MCP servers (perplexity for current state, context7 for library docs)
3. **Check official sources** for deprecation notices, EOL dates
4. **Base all guidance on current, verified information**

## Technology Radar Model

### Radar Quadrants

```text
              ADOPT                    TRIAL
         ┌────────────────────────────────────┐
         │                 │                  │
         │  Production-    │   Limited        │
         │  ready, proven  │   production,    │
         │  at scale       │   high potential │
         │                 │                  │
    ─────┼─────────────────┼──────────────────┼─────
         │                 │                  │
         │  Worth          │   Monitor for    │
         │  exploring,     │   developments,  │
         │  low risk       │   high potential │
         │                 │                  │
         └────────────────────────────────────┘
              ASSESS                   HOLD
```

### Radar Ring Definitions

```csharp
public enum RadarRing
{
    Adopt,   // Recommended for use, proven benefits
    Trial,   // Worth pursuing, ready for use on projects with risk
    Assess,  // Worth exploring, understand how it affects you
    Hold     // Proceed with caution, don't start new projects
}

public enum RadarQuadrant
{
    Techniques,        // Methodologies, practices, patterns
    Tools,             // Software tools, utilities
    Platforms,         // Cloud, infrastructure, runtimes
    LanguagesFrameworks // Languages, frameworks, libraries
}

public sealed record TechnologyBlip(
    string Name,
    RadarQuadrant Quadrant,
    RadarRing Ring,
    RadarRing? PreviousRing,
    string Description,
    IReadOnlyList<string> Tags,
    DateOnly LastUpdated,
    string Rationale);

public sealed class TechnologyRadar
{
    public DateOnly Date { get; init; }
    public IReadOnlyList<TechnologyBlip> Blips { get; init; } = Array.Empty<TechnologyBlip>();

    public IReadOnlyList<TechnologyBlip> GetMovedIn()
        => Blips.Where(b => b.PreviousRing.HasValue &&
            (int)b.Ring < (int)b.PreviousRing).ToList();

    public IReadOnlyList<TechnologyBlip> GetMovedOut()
        => Blips.Where(b => b.PreviousRing.HasValue &&
            (int)b.Ring > (int)b.PreviousRing).ToList();

    public IReadOnlyList<TechnologyBlip> GetNew()
        => Blips.Where(b => !b.PreviousRing.HasValue).ToList();
}
```

## Technology Maturity Model

### Maturity Assessment

```csharp
public sealed record TechnologyMaturity(
    string Technology,
    MaturityStage Stage,
    int YearsToMainstream,
    AdoptionLevel Adoption,
    EcosystemHealth Ecosystem,
    IReadOnlyList<string> StrengthSignals,
    IReadOnlyList<string> WeaknessSignals);

public enum MaturityStage
{
    Emerging,      // Early development, experimental
    Growing,       // Gaining traction, early adopters
    Mainstream,    // Widely adopted, well-understood
    Mature,        // Stable, commoditized
    Declining      // Being replaced, legacy
}

public enum AdoptionLevel
{
    Innovators,       // <2.5% of market
    EarlyAdopters,    // 2.5-13.5%
    EarlyMajority,    // 13.5-50%
    LateMajority,     // 50-84%
    Laggards          // >84%
}

public sealed record EcosystemHealth(
    int ActiveContributors,
    int PackagesAvailable,
    int StackOverflowQuestions,
    double JobPostingsGrowth,
    bool HasMajorCorporateBackers,
    bool HasActiveConferences);
```

### Maturity Indicators

```csharp
public sealed class MaturityAssessor
{
    public TechnologyMaturity Assess(string technology, TechnologyMetrics metrics)
    {
        var stage = DetermineStage(metrics);
        var adoption = DetermineAdoption(metrics);
        var ecosystem = AssessEcosystem(metrics);

        var strengths = new List<string>();
        var weaknesses = new List<string>();

        // Positive signals
        if (metrics.GitHubStars > 50000)
            strengths.Add("High community interest");
        if (metrics.MajorCompanyUsers > 10)
            strengths.Add("Proven at scale by major companies");
        if (metrics.YearlyReleases >= 4)
            strengths.Add("Active development");
        if (metrics.StackOverflowAnswerRate > 0.8)
            strengths.Add("Strong community support");

        // Negative signals
        if (metrics.DaysSinceLastRelease > 180)
            weaknesses.Add("Slow release cadence");
        if (metrics.OpenIssues > metrics.ClosedIssuesLast90Days * 3)
            weaknesses.Add("Issue backlog growing");
        if (metrics.BreakingChangesPerYear > 4)
            weaknesses.Add("Unstable API");
        if (!metrics.HasLTS)
            weaknesses.Add("No long-term support version");

        return new TechnologyMaturity(
            technology,
            stage,
            EstimateYearsToMainstream(stage),
            adoption,
            ecosystem,
            strengths,
            weaknesses);
    }

    private MaturityStage DetermineStage(TechnologyMetrics metrics)
    {
        if (metrics.YearsOld < 2 && metrics.AdoptionPercentage < 5)
            return MaturityStage.Emerging;
        if (metrics.AdoptionPercentage < 20 && metrics.GrowthRate > 50)
            return MaturityStage.Growing;
        if (metrics.AdoptionPercentage >= 20 && metrics.GrowthRate > 0)
            return MaturityStage.Mainstream;
        if (metrics.GrowthRate <= 0 && metrics.AdoptionPercentage > 30)
            return MaturityStage.Mature;
        return MaturityStage.Declining;
    }
}
```

## Technology Evaluation Framework

### Evaluation Criteria

```csharp
public sealed record TechnologyEvaluation(
    string Technology,
    string UseCase,
    DateOnly EvaluationDate,
    TechnicalEvaluation Technical,
    EcosystemEvaluation Ecosystem,
    OrganizationalFit OrgFit,
    RiskAssessment Risks,
    double OverallScore,
    RadarRing RecommendedRing,
    string Recommendation);

public sealed record TechnicalEvaluation(
    int PerformanceScore,          // 1-5
    int ScalabilityScore,          // 1-5
    int SecurityScore,             // 1-5
    int MaintainabilityScore,      // 1-5
    int InteroperabilityScore,     // 1-5
    IReadOnlyList<string> TechnicalStrengths,
    IReadOnlyList<string> TechnicalWeaknesses);

public sealed record EcosystemEvaluation(
    int CommunityScore,            // 1-5
    int DocumentationScore,        // 1-5
    int ToolingScore,              // 1-5
    int TalentAvailabilityScore,   // 1-5
    int LongevityScore,            // 1-5
    IReadOnlyList<string> EcosystemStrengths,
    IReadOnlyList<string> EcosystemWeaknesses);

public sealed record OrganizationalFit(
    int TeamExpertiseScore,        // 1-5
    int StrategicAlignmentScore,   // 1-5
    int IntegrationEaseScore,      // 1-5
    int CostScore,                 // 1-5
    int LearningCurveScore,        // 1-5
    IReadOnlyList<string> FitStrengths,
    IReadOnlyList<string> FitChallenges);
```

### Weighted Scoring

```csharp
public sealed class TechnologyScorer
{
    public static readonly Dictionary<string, double> DefaultWeights = new()
    {
        // Technical (40%)
        ["Performance"] = 0.10,
        ["Scalability"] = 0.08,
        ["Security"] = 0.10,
        ["Maintainability"] = 0.07,
        ["Interoperability"] = 0.05,

        // Ecosystem (30%)
        ["Community"] = 0.08,
        ["Documentation"] = 0.06,
        ["Tooling"] = 0.06,
        ["TalentAvailability"] = 0.05,
        ["Longevity"] = 0.05,

        // Organizational Fit (30%)
        ["TeamExpertise"] = 0.08,
        ["StrategicAlignment"] = 0.07,
        ["IntegrationEase"] = 0.06,
        ["Cost"] = 0.05,
        ["LearningCurve"] = 0.04
    };

    public double CalculateScore(TechnologyEvaluation evaluation)
    {
        var scores = new Dictionary<string, int>
        {
            ["Performance"] = evaluation.Technical.PerformanceScore,
            ["Scalability"] = evaluation.Technical.ScalabilityScore,
            ["Security"] = evaluation.Technical.SecurityScore,
            ["Maintainability"] = evaluation.Technical.MaintainabilityScore,
            ["Interoperability"] = evaluation.Technical.InteroperabilityScore,
            ["Community"] = evaluation.Ecosystem.CommunityScore,
            ["Documentation"] = evaluation.Ecosystem.DocumentationScore,
            ["Tooling"] = evaluation.Ecosystem.ToolingScore,
            ["TalentAvailability"] = evaluation.Ecosystem.TalentAvailabilityScore,
            ["Longevity"] = evaluation.Ecosystem.LongevityScore,
            ["TeamExpertise"] = evaluation.OrgFit.TeamExpertiseScore,
            ["StrategicAlignment"] = evaluation.OrgFit.StrategicAlignmentScore,
            ["IntegrationEase"] = evaluation.OrgFit.IntegrationEaseScore,
            ["Cost"] = evaluation.OrgFit.CostScore,
            ["LearningCurve"] = evaluation.OrgFit.LearningCurveScore
        };

        return scores.Sum(s => DefaultWeights[s.Key] * s.Value);
    }

    public RadarRing RecommendRing(double score, TechnologyMaturity maturity)
    {
        return (score, maturity.Stage) switch
        {
            (>= 4.0, MaturityStage.Mainstream or MaturityStage.Mature) => RadarRing.Adopt,
            (>= 3.5, MaturityStage.Growing or MaturityStage.Mainstream) => RadarRing.Trial,
            (>= 3.0, _) => RadarRing.Assess,
            (< 3.0, MaturityStage.Declining) => RadarRing.Hold,
            _ => RadarRing.Assess
        };
    }
}
```

## Comparison Framework

### Head-to-Head Comparison

```csharp
public sealed record TechnologyComparison(
    IReadOnlyList<string> Technologies,
    string UseCase,
    IReadOnlyList<ComparisonCriterion> Criteria,
    IReadOnlyList<TechnologyScore> Scores,
    string Winner,
    string Rationale);

public sealed record ComparisonCriterion(
    string Name,
    string Description,
    double Weight,
    bool HigherIsBetter);

public sealed record TechnologyScore(
    string Technology,
    IReadOnlyDictionary<string, double> CriterionScores,
    double WeightedTotal);

public sealed class TechnologyComparator
{
    public TechnologyComparison Compare(
        IReadOnlyList<string> technologies,
        string useCase,
        IReadOnlyDictionary<string, Dictionary<string, double>> scores)
    {
        var criteria = GetCriteriaForUseCase(useCase);

        var techScores = technologies.Select(tech =>
        {
            var techCriterionScores = scores.GetValueOrDefault(tech, new());
            var weightedTotal = criteria.Sum(c =>
                c.Weight * techCriterionScores.GetValueOrDefault(c.Name, 2.5));

            return new TechnologyScore(tech, techCriterionScores, weightedTotal);
        }).ToList();

        var winner = techScores.OrderByDescending(s => s.WeightedTotal).First();

        return new TechnologyComparison(
            technologies,
            useCase,
            criteria,
            techScores,
            winner.Technology,
            GenerateRationale(winner, techScores));
    }

    private IReadOnlyList<ComparisonCriterion> GetCriteriaForUseCase(string useCase)
    {
        // Adjust criteria weights based on use case
        return useCase.ToLowerInvariant() switch
        {
            "api" or "backend" => ApiCriteria,
            "frontend" or "ui" => FrontendCriteria,
            "data" or "analytics" => DataCriteria,
            "mobile" => MobileCriteria,
            _ => DefaultCriteria
        };
    }

    private static readonly IReadOnlyList<ComparisonCriterion> DefaultCriteria = new[]
    {
        new ComparisonCriterion("Performance", "Runtime performance", 0.15, true),
        new ComparisonCriterion("Learning Curve", "Ease of learning", 0.10, true),
        new ComparisonCriterion("Community", "Size and activity", 0.12, true),
        new ComparisonCriterion("Documentation", "Quality and coverage", 0.10, true),
        new ComparisonCriterion("Tooling", "IDE, debugging, testing", 0.10, true),
        new ComparisonCriterion("Talent Pool", "Hiring ease", 0.08, true),
        new ComparisonCriterion("Maturity", "Stability and track record", 0.10, true),
        new ComparisonCriterion("Ecosystem", "Libraries, integrations", 0.10, true),
        new ComparisonCriterion("Longevity", "Future outlook", 0.08, true),
        new ComparisonCriterion("Cost", "Licensing and operational", 0.07, true)
    };
}
```

## Adoption Roadmap

### Adoption Phases

```csharp
public sealed record AdoptionRoadmap(
    string Technology,
    AdoptionStrategy Strategy,
    IReadOnlyList<AdoptionPhase> Phases,
    IReadOnlyList<string> Prerequisites,
    IReadOnlyList<AdoptionRisk> Risks,
    IReadOnlyList<SuccessMetric> SuccessMetrics);

public enum AdoptionStrategy
{
    BigBang,        // Full replacement at once
    Incremental,    // Gradual rollout
    Strangler,      // New alongside old, gradually replace
    Pilot,          // Start with single project/team
    GreenField      // Only for new projects
}

public sealed record AdoptionPhase(
    string Name,
    string Description,
    TimeSpan Duration,
    IReadOnlyList<string> Activities,
    IReadOnlyList<string> Deliverables,
    IReadOnlyList<string> GoNoGoGriteria);

public sealed class AdoptionPlanner
{
    public AdoptionRoadmap Plan(
        string technology,
        RadarRing currentRing,
        OrganizationalContext context)
    {
        var strategy = DetermineStrategy(currentRing, context);
        var phases = GeneratePhases(strategy, technology, context);

        return new AdoptionRoadmap(
            technology,
            strategy,
            phases,
            IdentifyPrerequisites(technology, context),
            IdentifyRisks(technology, strategy),
            DefineSuccessMetrics(technology, strategy));
    }

    private AdoptionStrategy DetermineStrategy(
        RadarRing ring,
        OrganizationalContext context)
    {
        return (ring, context.RiskTolerance) switch
        {
            (RadarRing.Adopt, RiskTolerance.High) => AdoptionStrategy.Incremental,
            (RadarRing.Adopt, _) => AdoptionStrategy.Pilot,
            (RadarRing.Trial, RiskTolerance.High) => AdoptionStrategy.Pilot,
            (RadarRing.Trial, _) => AdoptionStrategy.GreenField,
            (RadarRing.Assess, _) => AdoptionStrategy.GreenField,
            (RadarRing.Hold, _) => throw new InvalidOperationException("Should not adopt HOLD technologies"),
            _ => AdoptionStrategy.Pilot
        };
    }

    private IReadOnlyList<AdoptionPhase> GeneratePhases(
        AdoptionStrategy strategy,
        string technology,
        OrganizationalContext context)
    {
        return strategy switch
        {
            AdoptionStrategy.Pilot => new[]
            {
                new AdoptionPhase(
                    "Pilot Setup",
                    "Select and prepare pilot project/team",
                    TimeSpan.FromDays(14),
                    new[] { "Select pilot project", "Set up environment", "Train pilot team" },
                    new[] { "Pilot project identified", "Environment ready", "Team trained" },
                    new[] { "Team confident to proceed" }),

                new AdoptionPhase(
                    "Pilot Execution",
                    "Build pilot project with new technology",
                    TimeSpan.FromDays(60),
                    new[] { "Implement pilot", "Document learnings", "Measure metrics" },
                    new[] { "Working pilot", "Learnings document", "Metrics dashboard" },
                    new[] { "Pilot meets success criteria", "Team recommends adoption" }),

                new AdoptionPhase(
                    "Evaluation",
                    "Assess pilot results and make decision",
                    TimeSpan.FromDays(14),
                    new[] { "Review metrics", "Gather feedback", "Make recommendation" },
                    new[] { "Evaluation report", "Go/no-go decision" },
                    new[] { "Clear recommendation with evidence" }),

                new AdoptionPhase(
                    "Expansion",
                    "Roll out to additional teams/projects",
                    TimeSpan.FromDays(90),
                    new[] { "Create training program", "Establish standards", "Support expansion" },
                    new[] { "Training materials", "Standards documented", "Multiple projects using" },
                    new[] { "Adoption rate target met", "No major issues" })
            },
            // Additional strategy patterns...
            _ => Array.Empty<AdoptionPhase>()
        };
    }
}
```

## Deprecation Assessment

### Deprecation Signals

```csharp
public sealed record DeprecationAssessment(
    string Technology,
    DeprecationStatus Status,
    DateOnly? EndOfLifeDate,
    IReadOnlyList<string> WarningSignals,
    IReadOnlyList<string> MigrationOptions,
    MigrationUrgency Urgency,
    string Recommendation);

public enum DeprecationStatus
{
    Active,         // Fully supported
    Maintenance,    // Security fixes only
    Deprecated,     // Officially deprecated, still works
    EndOfLife,      // No longer supported
    Sunset          // Will be removed
}

public enum MigrationUrgency
{
    NotRequired,    // Technology is healthy
    Optional,       // Consider for new projects
    Recommended,    // Start planning migration
    Urgent,         // Migrate ASAP
    Critical        // Immediate security/compliance risk
}

public sealed class DeprecationDetector
{
    public IReadOnlyList<string> DetectWarningSignals(TechnologyMetrics metrics)
    {
        var signals = new List<string>();

        // Development activity
        if (metrics.DaysSinceLastRelease > 365)
            signals.Add("No releases in over a year");
        if (metrics.CommitsLast90Days < 10)
            signals.Add("Very low commit activity");

        // Community health
        if (metrics.GitHubStarsTrend < 0)
            signals.Add("Declining GitHub stars");
        if (metrics.StackOverflowQuestionsTrend < 0)
            signals.Add("Declining community questions");

        // Ecosystem
        if (metrics.DependentPackagesTrend < 0)
            signals.Add("Fewer packages depending on it");
        if (metrics.JobPostingsTrend < -20)
            signals.Add("Job postings declining >20%");

        // Official signals
        if (metrics.HasDeprecationNotice)
            signals.Add("Official deprecation notice");
        if (metrics.SuccessorAnnounced)
            signals.Add("Successor technology announced");
        if (metrics.MajorVendorDropping)
            signals.Add("Major vendor dropping support");

        return signals;
    }
}
```

## Workflow

When assessing technology:

1. **Define Context**: What's the use case? What are constraints?
2. **Identify Candidates**: What technologies could solve the problem?
3. **Research Current State**: Use MCP servers to verify status, versions, health
4. **Assess Maturity**: Where is each technology in its lifecycle?
5. **Evaluate Fit**: Score against technical, ecosystem, and organizational criteria
6. **Compare Options**: Head-to-head comparison with weighted scoring
7. **Check Deprecation**: Any warning signals or EOL dates?
8. **Position on Radar**: Determine appropriate ring
9. **Plan Adoption**: If adopting, create roadmap
10. **Document Decision**: Record rationale and assumptions

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
