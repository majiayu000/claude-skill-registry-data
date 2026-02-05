---
name: tech-debt-assessment
description: Technical debt identification, quantification, and prioritization for informed remediation planning
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Technical Debt Assessment Skill

## When to Use This Skill

Use this skill when:

- **Tech Debt Assessment tasks** - Working on technical debt identification, quantification, and prioritization for informed remediation planning
- **Planning or design** - Need guidance on Tech Debt Assessment approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Systematic identification, quantification, and prioritization of technical debt to enable informed decisions about remediation investments.

## MANDATORY: Documentation-First Approach

Before providing tech debt guidance:

1. **Invoke `docs-management` skill** for code quality documentation
2. **Verify current practices** via MCP servers (perplexity for latest debt frameworks)
3. **Base all guidance on established methodologies**

## Technical Debt Quadrant (Fowler)

### Debt Classification

```text
                    Deliberate
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          │  Prudent/   │  Reckless/  │
          │  Deliberate │  Deliberate │
          │             │             │
          │ "We know    │ "We don't   │
          │ the trade-  │ have time   │
          │ offs"       │ for design" │
Prudent ──┼─────────────┼─────────────┼── Reckless
          │             │             │
          │  Prudent/   │  Reckless/  │
          │ Inadvertent │ Inadvertent │
          │             │             │
          │ "Now we     │ "What's     │
          │ know how    │ layering?"  │
          │ to do it"   │             │
          └─────────────┼─────────────┘
                        │
                   Inadvertent
```

### Debt Types

```csharp
public enum DebtQuadrant
{
    PrudentDeliberate,   // Conscious trade-off for business reasons
    PrudentInadvertent,  // Learned better approach after implementation
    RecklessDeliberate,  // Cut corners knowingly
    RecklessInadvertent  // Don't know good practices
}

public enum DebtCategory
{
    // Code Level
    CodeSmells,          // Duplications, long methods, dead code
    TestingDebt,         // Missing tests, flaky tests, slow tests
    DocumentationDebt,   // Missing/outdated docs, tribal knowledge

    // Design Level
    DesignDebt,          // Violated principles, poor abstractions
    DependencyDebt,      // Outdated libraries, version conflicts
    ConfigurationDebt,   // Hardcoded values, environment coupling

    // Architecture Level
    ArchitectureDebt,    // Violated boundaries, coupling, scalability limits
    InfrastructureDebt,  // Manual processes, poor CI/CD, missing monitoring
    SecurityDebt         // Known vulnerabilities, outdated practices
}

public sealed record TechnicalDebtItem(
    string Id,
    string Title,
    string Description,
    DebtCategory Category,
    DebtQuadrant Quadrant,
    string Location,          // File(s), module, service
    DebtSeverity Severity,
    DebtQuantification Quantification,
    DebtImpact Impact,
    string Origin,            // When/how debt was introduced
    DateOnly IdentifiedDate,
    string IdentifiedBy,
    DebtStatus Status);

public enum DebtSeverity
{
    Low,       // Minor inconvenience
    Medium,    // Noticeable slowdown
    High,      // Significant impediment
    Critical   // Blocking development
}

public enum DebtStatus
{
    Identified,
    Analyzed,
    Prioritized,
    Scheduled,
    InProgress,
    Resolved,
    Accepted    // Deliberately not addressing
}
```

## Debt Quantification

### Principal and Interest Model

```csharp
public sealed record DebtQuantification(
    decimal Principal,        // Cost to fix now (hours or $)
    decimal InterestRate,     // Additional cost per time period (%)
    TimeSpan PaymentPeriod,   // How often interest compounds
    decimal AccruedInterest,  // Interest already accumulated
    decimal TotalOwed,        // Principal + Accrued Interest
    DateOnly BreakEvenDate);  // When fixing pays for itself

public sealed class DebtCalculator
{
    /// <summary>
    /// Calculate when paying off debt becomes worthwhile
    /// </summary>
    public DebtQuantification Quantify(
        decimal fixCostHours,
        decimal hourlyRate,
        decimal weeklyInterestHours,
        int weeksAccrued)
    {
        var principal = fixCostHours * hourlyRate;
        var weeklyInterest = weeklyInterestHours * hourlyRate;
        var interestRate = weeklyInterest / principal;
        var accruedInterest = weeklyInterest * weeksAccrued;
        var totalOwed = principal + accruedInterest;

        // Break even when cumulative interest > principal
        var weeksToBreakEven = (int)Math.Ceiling(principal / weeklyInterest);

        return new DebtQuantification(
            Principal: principal,
            InterestRate: interestRate,
            PaymentPeriod: TimeSpan.FromDays(7),
            AccruedInterest: accruedInterest,
            TotalOwed: totalOwed,
            BreakEvenDate: DateOnly.FromDateTime(DateTime.UtcNow.AddDays(weeksToBreakEven * 7)));
    }
}
```

### Interest Calculation Examples

```csharp
public static class DebtInterestExamples
{
    /// <summary>
    /// Missing unit tests: extra debugging time per bug
    /// </summary>
    public static DebtQuantification MissingTestsDebt(
        int untestedMethods,
        decimal debuggingHoursPerBug,
        decimal bugsPerMonth,
        decimal testWritingHoursPerMethod)
    {
        var principal = untestedMethods * testWritingHoursPerMethod;
        var monthlyInterest = debuggingHoursPerBug * bugsPerMonth;

        return new DebtQuantification(
            Principal: principal,
            InterestRate: monthlyInterest / principal,
            PaymentPeriod: TimeSpan.FromDays(30),
            AccruedInterest: 0,
            TotalOwed: principal,
            BreakEvenDate: DateOnly.FromDateTime(DateTime.UtcNow.AddMonths(
                (int)Math.Ceiling(principal / monthlyInterest))));
    }

    /// <summary>
    /// Legacy framework: time spent on workarounds
    /// </summary>
    public static DebtQuantification LegacyFrameworkDebt(
        decimal migrationCostHours,
        decimal weeklyWorkaroundHours)
    {
        return new DebtQuantification(
            Principal: migrationCostHours,
            InterestRate: weeklyWorkaroundHours / migrationCostHours,
            PaymentPeriod: TimeSpan.FromDays(7),
            AccruedInterest: 0,
            TotalOwed: migrationCostHours,
            BreakEvenDate: DateOnly.FromDateTime(DateTime.UtcNow.AddDays(
                (int)Math.Ceiling(migrationCostHours / weeklyWorkaroundHours) * 7)));
    }
}
```

## Debt Identification

### Static Analysis Integration

```csharp
public sealed class DebtIdentifier
{
    public async Task<IReadOnlyList<TechnicalDebtItem>> IdentifyFromAnalysis(
        string projectPath)
    {
        var debts = new List<TechnicalDebtItem>();

        // Code quality tools
        debts.AddRange(await RunSonarQube(projectPath));
        debts.AddRange(await RunCodeClimate(projectPath));

        // Dependency analysis
        debts.AddRange(await AnalyzeDependencies(projectPath));

        // Test coverage gaps
        debts.AddRange(await AnalyzeTestCoverage(projectPath));

        // Documentation analysis
        debts.AddRange(await AnalyzeDocumentation(projectPath));

        // Architecture conformance
        debts.AddRange(await CheckArchitectureRules(projectPath));

        return debts;
    }

    private async Task<IEnumerable<TechnicalDebtItem>> AnalyzeDependencies(
        string projectPath)
    {
        // Check for outdated packages
        // dotnet list package --outdated
        // npm outdated

        var outdated = await GetOutdatedPackages(projectPath);

        return outdated.Select(pkg => new TechnicalDebtItem(
            Id: $"DEP-{pkg.Name}",
            Title: $"Outdated: {pkg.Name}",
            Description: $"Package {pkg.Name} is {pkg.VersionsBehind} versions behind. Current: {pkg.CurrentVersion}, Latest: {pkg.LatestVersion}",
            Category: DebtCategory.DependencyDebt,
            Quadrant: DebtQuadrant.PrudentInadvertent,
            Location: pkg.ProjectFile,
            Severity: pkg.HasSecurityIssues ? DebtSeverity.Critical : DebtSeverity.Medium,
            Quantification: EstimateUpgradeEffort(pkg),
            Impact: AssessDependencyImpact(pkg),
            Origin: "Dependency became outdated over time",
            IdentifiedDate: DateOnly.FromDateTime(DateTime.UtcNow),
            IdentifiedBy: "Automated scan",
            Status: DebtStatus.Identified));
    }
}
```

### Common Debt Patterns

```csharp
public static class CommonDebtPatterns
{
    public static IEnumerable<DebtPattern> GetPatterns()
    {
        yield return new DebtPattern(
            Name: "God Class",
            Category: DebtCategory.DesignDebt,
            Indicators: new[] { "Class > 500 lines", "Class has > 20 methods", "Low cohesion" },
            TypicalPrincipal: "8-40 hours to refactor",
            TypicalInterest: "1-2 hours/week in confusion and merge conflicts");

        yield return new DebtPattern(
            Name: "Duplicated Code",
            Category: DebtCategory.CodeSmells,
            Indicators: new[] { "Copy-paste violations", "Similar logic in multiple places" },
            TypicalPrincipal: "1-4 hours per duplication",
            TypicalInterest: "0.5-1 hours per change (must update multiple places)");

        yield return new DebtPattern(
            Name: "Missing Tests",
            Category: DebtCategory.TestingDebt,
            Indicators: new[] { "Low code coverage", "Fear of refactoring", "Bugs in production" },
            TypicalPrincipal: "0.5-2 hours per method",
            TypicalInterest: "2-4 hours per bug in debugging");

        yield return new DebtPattern(
            Name: "Hardcoded Configuration",
            Category: DebtCategory.ConfigurationDebt,
            Indicators: new[] { "Magic strings", "Environment-specific values in code" },
            TypicalPrincipal: "0.5-1 hour per instance",
            TypicalInterest: "Deployment failures, environment issues");

        yield return new DebtPattern(
            Name: "Outdated Documentation",
            Category: DebtCategory.DocumentationDebt,
            Indicators: new[] { "Docs don't match code", "Tribal knowledge", "Onboarding issues" },
            TypicalPrincipal: "4-8 hours per component",
            TypicalInterest: "1-2 hours per new team member onboarding");

        yield return new DebtPattern(
            Name: "Monolithic Architecture",
            Category: DebtCategory.ArchitectureDebt,
            Indicators: new[] { "Tight coupling", "Deployment bottleneck", "Can't scale independently" },
            TypicalPrincipal: "Months of refactoring",
            TypicalInterest: "Slower releases, harder scaling");
    }
}
```

## Debt Impact Assessment

### Impact Model

```csharp
public sealed record DebtImpact(
    DeveloperProductivityImpact Productivity,
    QualityImpact Quality,
    VelocityImpact Velocity,
    MoraleImpact Morale,
    BusinessImpact Business);

public sealed record DeveloperProductivityImpact(
    int AffectedDevelopers,
    decimal HoursLostPerWeek,
    string Description);

public sealed record QualityImpact(
    int AdditionalBugsPerMonth,
    bool IncreasesSecurityRisk,
    bool ReducesReliability,
    string Description);

public sealed record VelocityImpact(
    decimal DeliverySlowdownPercent,
    bool BlocksNewFeatures,
    int FeaturesBlocked,
    string Description);

public sealed record MoraleImpact(
    bool CausesFrustration,
    bool ContributesToBurnout,
    bool AffectsRetention,
    string Description);

public sealed record BusinessImpact(
    decimal RevenueLossPerMonth,
    decimal CustomerChurnRisk,
    bool AffectsCompliance,
    string Description);
```

### Impact Scoring

```csharp
public sealed class ImpactScorer
{
    public int CalculateImpactScore(DebtImpact impact)
    {
        var score = 0;

        // Productivity (0-25 points)
        score += Math.Min(25, impact.Productivity.AffectedDevelopers *
            (int)impact.Productivity.HoursLostPerWeek);

        // Quality (0-25 points)
        score += impact.Quality.IncreasesSecurityRisk ? 15 : 0;
        score += impact.Quality.ReducesReliability ? 10 : 0;

        // Velocity (0-25 points)
        score += impact.Velocity.BlocksNewFeatures ? 20 : 0;
        score += Math.Min(5, impact.Velocity.FeaturesBlocked);

        // Business (0-25 points)
        score += impact.Business.AffectsCompliance ? 25 : 0;
        score += impact.Business.CustomerChurnRisk > 0.1m ? 15 : 0;

        return Math.Min(100, score);
    }
}
```

## Debt Prioritization

### Prioritization Matrix

```csharp
public sealed class DebtPrioritizer
{
    public IReadOnlyList<TechnicalDebtItem> Prioritize(
        IEnumerable<TechnicalDebtItem> debts)
    {
        return debts
            .Select(d => (Debt: d, Score: CalculatePriorityScore(d)))
            .OrderByDescending(x => x.Score)
            .Select(x => x.Debt)
            .ToList();
    }

    private double CalculatePriorityScore(TechnicalDebtItem debt)
    {
        // Weighted scoring
        var impactScore = CalculateImpactScore(debt.Impact) * 0.4;
        var effortScore = (100 - CalculateEffortScore(debt.Quantification.Principal)) * 0.2;
        var interestScore = CalculateInterestScore(debt.Quantification) * 0.3;
        var ageScore = CalculateAgeScore(debt.IdentifiedDate) * 0.1;

        return impactScore + effortScore + interestScore + ageScore;
    }

    private double CalculateInterestScore(DebtQuantification quantification)
    {
        // Higher interest rate = higher priority
        return Math.Min(100, (double)quantification.InterestRate * 1000);
    }

    private double CalculateAgeScore(DateOnly identifiedDate)
    {
        // Older debt gets slightly higher priority (avoid perpetual deferral)
        var age = DateOnly.FromDateTime(DateTime.UtcNow).DayNumber - identifiedDate.DayNumber;
        return Math.Min(100, age / 3.65); // Max score at 1 year old
    }
}
```

### Cost of Delay Prioritization

```csharp
public sealed class CostOfDelayPrioritizer
{
    /// <summary>
    /// CD3: Cost of Delay Divided by Duration
    /// Higher values = higher priority
    /// </summary>
    public double CalculateCD3(TechnicalDebtItem debt)
    {
        // Cost of Delay = Weekly interest being paid
        var weeklyInterest = debt.Quantification.InterestRate *
            debt.Quantification.Principal;

        // Duration = Time to fix (in weeks)
        var durationWeeks = (double)debt.Quantification.Principal / 40; // 40 hour weeks

        return (double)weeklyInterest / durationWeeks;
    }

    public IReadOnlyList<TechnicalDebtItem> PrioritizeByCD3(
        IEnumerable<TechnicalDebtItem> debts)
    {
        return debts
            .Select(d => (Debt: d, CD3: CalculateCD3(d)))
            .OrderByDescending(x => x.CD3)
            .Select(x => x.Debt)
            .ToList();
    }
}
```

## Remediation Planning

### Remediation Strategies

```csharp
public enum RemediationStrategy
{
    PayOff,          // Fix completely
    Refinance,       // Reduce interest without full fix
    Consolidate,     // Combine multiple debts into one fix
    Accept,          // Acknowledge and don't fix
    Strangler,       // Gradually replace
    ScheduledPayment // Fix incrementally over time
}

public sealed record RemediationPlan(
    IReadOnlyList<TechnicalDebtItem> Debts,
    RemediationStrategy Strategy,
    TimeSpan EstimatedDuration,
    decimal EstimatedEffort,
    IReadOnlyList<string> Prerequisites,
    IReadOnlyList<string> Risks,
    IReadOnlyList<Milestone> Milestones);

public sealed class RemediationPlanner
{
    public RemediationStrategy RecommendStrategy(TechnicalDebtItem debt)
    {
        // High interest + low principal = Pay off
        if (debt.Quantification.InterestRate > 0.1m &&
            debt.Quantification.Principal < 40)
            return RemediationStrategy.PayOff;

        // Very high principal = Strangler or scheduled
        if (debt.Quantification.Principal > 200)
            return debt.Category == DebtCategory.ArchitectureDebt
                ? RemediationStrategy.Strangler
                : RemediationStrategy.ScheduledPayment;

        // Low interest = Consider accepting
        if (debt.Quantification.InterestRate < 0.01m)
            return RemediationStrategy.Accept;

        // Multiple related debts = Consolidate
        // (would need to analyze relationships)

        return RemediationStrategy.PayOff;
    }
}
```

## Debt Tracking

### Debt Register

```csharp
public sealed class TechnicalDebtRegister
{
    private readonly List<TechnicalDebtItem> _debts = new();

    public DebtSummary GetSummary()
    {
        var openDebts = _debts.Where(d => d.Status != DebtStatus.Resolved).ToList();

        return new DebtSummary(
            TotalDebtItems: openDebts.Count,
            TotalPrincipal: openDebts.Sum(d => d.Quantification.Principal),
            TotalAccruedInterest: openDebts.Sum(d => d.Quantification.AccruedInterest),
            WeeklyInterestPayment: openDebts.Sum(d =>
                d.Quantification.Principal * d.Quantification.InterestRate),
            ByCategory: openDebts
                .GroupBy(d => d.Category)
                .ToDictionary(g => g.Key, g => g.Count()),
            BySeverity: openDebts
                .GroupBy(d => d.Severity)
                .ToDictionary(g => g.Key, g => g.Count()),
            TopDebtors: openDebts
                .OrderByDescending(d => d.Quantification.TotalOwed)
                .Take(10)
                .ToList());
    }

    public DebtTrend GetTrend(int months = 12)
    {
        // Track debt over time
        var monthlySnapshots = GetMonthlySnapshots(months);

        return new DebtTrend(
            Snapshots: monthlySnapshots,
            IsIncreasing: monthlySnapshots.Last().TotalDebt > monthlySnapshots.First().TotalDebt,
            AverageMonthlyChange: CalculateAverageChange(monthlySnapshots));
    }
}
```

## Workflow

When assessing technical debt:

1. **Identify**: Use static analysis, code review, team input
2. **Categorize**: Classify by type and quadrant
3. **Quantify**: Estimate principal and interest
4. **Impact Assess**: Evaluate productivity, quality, velocity impacts
5. **Prioritize**: Rank by CD3 or weighted scoring
6. **Plan Remediation**: Choose strategy and create plan
7. **Track**: Monitor debt levels over time
8. **Report**: Communicate debt status to stakeholders

## References

For detailed templates:

---

**Last Updated:** 2025-12-26
