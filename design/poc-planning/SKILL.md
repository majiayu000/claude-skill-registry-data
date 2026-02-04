---
name: poc-planning
description: Proof-of-concept and spike design for uncertainty reduction and technology validation
allowed-tools: Read, Glob, Grep, Write, Edit
---

# POC Planning Skill

## When to Use This Skill

Use this skill when:

- **Poc Planning tasks** - Working on proof-of-concept and spike design for uncertainty reduction and technology validation
- **Planning or design** - Need guidance on Poc Planning approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design and plan proofs-of-concept (POCs), spikes, and technical experiments to validate assumptions, reduce uncertainty, and de-risk technical decisions.

## MANDATORY: Documentation-First Approach

Before providing POC planning guidance:

1. **Invoke `docs-management` skill** for methodology documentation
2. **Verify current practices** via MCP servers (perplexity for agile spike patterns)
3. **Base all guidance on proven experimentation frameworks**

## POC vs Spike vs Prototype

### Terminology Clarification

| Type | Purpose | Duration | Output |
|------|---------|----------|--------|
| **Spike** | Answer a specific technical question | Hours to days | Knowledge, decision |
| **POC** | Prove a concept is technically feasible | Days to weeks | Working demonstration |
| **Prototype** | Explore user experience and requirements | Weeks | Interactive mockup |
| **MVP** | Validate market fit with minimal investment | Weeks to months | Shippable product |
| **Pilot** | Test solution in production environment | Months | Operational feedback |

### Selection Guide

```csharp
public enum ExperimentType
{
    Spike,      // "Can we do X?" - focused technical investigation
    POC,        // "Does approach Y work?" - feasibility demonstration
    Prototype,  // "What should it look like?" - UX exploration
    MVP,        // "Will users pay for it?" - market validation
    Pilot       // "Does it work in production?" - operational validation
}

public static class ExperimentSelector
{
    public static ExperimentType Recommend(UncertaintyProfile uncertainty)
    {
        // Technical uncertainty: Spike or POC
        if (uncertainty.TechnicalUncertainty is High or VeryHigh)
        {
            return uncertainty.Scope == Scope.Narrow
                ? ExperimentType.Spike
                : ExperimentType.POC;
        }

        // UX/Requirements uncertainty: Prototype
        if (uncertainty.RequirementsUncertainty is High or VeryHigh)
            return ExperimentType.Prototype;

        // Market uncertainty: MVP
        if (uncertainty.MarketUncertainty is High or VeryHigh)
            return ExperimentType.MVP;

        // Operational uncertainty: Pilot
        if (uncertainty.OperationalUncertainty is High or VeryHigh)
            return ExperimentType.Pilot;

        return ExperimentType.Spike; // Default to smallest experiment
    }
}
```

## Spike Design

### Spike Structure

```csharp
public sealed record Spike(
    string Id,
    string Title,
    string Question,          // What we're trying to answer
    string Hypothesis,        // What we expect to find
    TimeSpan TimeBox,         // Maximum duration
    IReadOnlyList<string> Acceptance, // How we know we're done
    string Owner,
    SpikeStatus Status,
    SpikeOutcome? Outcome);

public sealed record SpikeOutcome(
    bool QuestionAnswered,
    string Finding,
    string Evidence,
    string Recommendation,
    IReadOnlyList<string> NextSteps,
    IReadOnlyList<string> LessonsLearned);

public enum SpikeStatus
{
    Planned,
    InProgress,
    Completed,
    Abandoned
}
```

### Spike Planning Template

```csharp
public static class SpikeTemplates
{
    public static Spike TechnologyEvaluationSpike(
        string technology,
        string useCase,
        TimeSpan duration)
    {
        return new Spike(
            Id: $"SPIKE-{DateTime.UtcNow:yyyyMMdd}-{Guid.NewGuid():N[..8]}",
            Title: $"Evaluate {technology} for {useCase}",
            Question: $"Can {technology} meet our requirements for {useCase}?",
            Hypothesis: $"We believe {technology} can handle our {useCase} requirements within acceptable performance bounds",
            TimeBox: duration,
            Acceptance: new[]
            {
                $"Document {technology} capabilities relevant to {useCase}",
                "Identify any blocking limitations",
                "Measure key performance characteristics",
                "Provide go/no-go recommendation with rationale"
            },
            Owner: "",
            Status: SpikeStatus.Planned,
            Outcome: null);
    }

    public static Spike IntegrationSpike(
        string sourceSystem,
        string targetSystem,
        TimeSpan duration)
    {
        return new Spike(
            Id: $"SPIKE-{DateTime.UtcNow:yyyyMMdd}-{Guid.NewGuid():N[..8]}",
            Title: $"Integration: {sourceSystem} to {targetSystem}",
            Question: $"Can we successfully integrate {sourceSystem} with {targetSystem}?",
            Hypothesis: $"We can establish bidirectional data flow between {sourceSystem} and {targetSystem} using their APIs",
            TimeBox: duration,
            Acceptance: new[]
            {
                "Successfully authenticate with both systems",
                "Read data from source system",
                "Write data to target system",
                "Document API limitations and quirks",
                "Estimate effort for full integration"
            },
            Owner: "",
            Status: SpikeStatus.Planned,
            Outcome: null);
    }

    public static Spike PerformanceSpike(
        string component,
        string performanceGoal,
        TimeSpan duration)
    {
        return new Spike(
            Id: $"SPIKE-{DateTime.UtcNow:yyyyMMdd}-{Guid.NewGuid():N[..8]}",
            Title: $"Performance: {component} - {performanceGoal}",
            Question: $"Can {component} achieve {performanceGoal}?",
            Hypothesis: $"With appropriate optimization, {component} can meet {performanceGoal}",
            TimeBox: duration,
            Acceptance: new[]
            {
                $"Benchmark current {component} performance",
                $"Identify bottlenecks preventing {performanceGoal}",
                "Test optimization approaches",
                "Measure optimized performance",
                "Document path to production performance"
            },
            Owner: "",
            Status: SpikeStatus.Planned,
            Outcome: null);
    }
}
```

## POC Design

### POC Structure

```csharp
public sealed record ProofOfConcept(
    string Id,
    string Title,
    string Objective,
    IReadOnlyList<string> Hypotheses,
    IReadOnlyList<POCScope> InScope,
    IReadOnlyList<string> OutOfScope,
    TimeSpan Duration,
    IReadOnlyList<POCMilestone> Milestones,
    IReadOnlyList<string> SuccessCriteria,
    IReadOnlyList<POCRisk> Risks,
    POCResources Resources,
    POCStatus Status);

public sealed record POCScope(
    string Feature,
    ScopeLevel Level,
    string Description);

public enum ScopeLevel
{
    Full,           // Complete implementation
    Partial,        // Key functionality only
    Simulated,      // Mocked/stubbed
    OutOfScope      // Explicitly excluded
}

public sealed record POCMilestone(
    string Name,
    DateOnly TargetDate,
    IReadOnlyList<string> Deliverables,
    MilestoneStatus Status);

public sealed record POCResources(
    IReadOnlyList<TeamMember> Team,
    decimal Budget,
    IReadOnlyList<string> Infrastructure,
    IReadOnlyList<string> ExternalDependencies);
```

### POC Planning Checklist

```csharp
public sealed class POCPlanningChecklist
{
    public IReadOnlyList<ChecklistItem> Items { get; } = new[]
    {
        // Objectives
        new ChecklistItem("Clear problem statement defined", Category.Objectives),
        new ChecklistItem("Success criteria are measurable", Category.Objectives),
        new ChecklistItem("Hypotheses are falsifiable", Category.Objectives),
        new ChecklistItem("Decision criteria for go/no-go established", Category.Objectives),

        // Scope
        new ChecklistItem("In-scope features clearly defined", Category.Scope),
        new ChecklistItem("Out-of-scope items explicitly listed", Category.Scope),
        new ChecklistItem("Scope is achievable within timebox", Category.Scope),
        new ChecklistItem("Dependencies identified", Category.Scope),

        // Resources
        new ChecklistItem("Team members assigned", Category.Resources),
        new ChecklistItem("Budget approved", Category.Resources),
        new ChecklistItem("Infrastructure/environment available", Category.Resources),
        new ChecklistItem("Access to required systems granted", Category.Resources),

        // Timeline
        new ChecklistItem("Duration is timeboxed", Category.Timeline),
        new ChecklistItem("Milestones defined with dates", Category.Timeline),
        new ChecklistItem("Review/demo points scheduled", Category.Timeline),
        new ChecklistItem("Extension/abort criteria defined", Category.Timeline),

        // Risks
        new ChecklistItem("Technical risks identified", Category.Risks),
        new ChecklistItem("Resource risks identified", Category.Risks),
        new ChecklistItem("Mitigation strategies defined", Category.Risks),

        // Exit Criteria
        new ChecklistItem("Success scenario defined", Category.Exit),
        new ChecklistItem("Failure scenario defined", Category.Exit),
        new ChecklistItem("Pivot criteria defined", Category.Exit),
        new ChecklistItem("Knowledge capture plan in place", Category.Exit)
    };
}
```

### POC Scoping Matrix

```csharp
public static class POCScopingMatrix
{
    /// <summary>
    /// Determine appropriate scope level for each feature in POC
    /// </summary>
    public static ScopeLevel DetermineScope(
        string feature,
        bool criticalToHypothesis,
        int implementationEffort,
        bool hasExistingAlternative)
    {
        // Critical to proving hypothesis: must be implemented
        if (criticalToHypothesis)
        {
            return implementationEffort <= 3 // days
                ? ScopeLevel.Full
                : ScopeLevel.Partial;
        }

        // Not critical but has existing solution: use it
        if (hasExistingAlternative)
            return ScopeLevel.Simulated;

        // Not critical and high effort: exclude
        if (implementationEffort > 5)
            return ScopeLevel.OutOfScope;

        return ScopeLevel.Simulated;
    }
}
```

## Hypothesis-Driven Development

### Hypothesis Structure

```csharp
public sealed record Hypothesis(
    string Id,
    string Statement,         // "We believe that..."
    string Because,           // "Because..."
    string SuccessMetric,     // "We will measure..."
    string SuccessThreshold,  // "Success means..."
    HypothesisStatus Status,
    HypothesisResult? Result);

public enum HypothesisStatus
{
    Proposed,
    Testing,
    Validated,
    Invalidated,
    Inconclusive
}

public sealed record HypothesisResult(
    string ActualMetric,
    bool MetThreshold,
    string Evidence,
    string Implications,
    IReadOnlyList<string> NextHypotheses);
```

### Hypothesis Templates

```csharp
public static class HypothesisTemplates
{
    public static Hypothesis Performance(
        string component,
        string metric,
        string threshold)
    {
        return new Hypothesis(
            Id: $"H-PERF-{Guid.NewGuid():N[..8]}",
            Statement: $"We believe that {component} can achieve {threshold} {metric}",
            Because: $"Our requirements specify {threshold} {metric} and {component} documentation suggests this is achievable",
            SuccessMetric: metric,
            SuccessThreshold: threshold,
            Status: HypothesisStatus.Proposed,
            Result: null);
    }

    public static Hypothesis Integration(
        string sourceSystem,
        string targetSystem,
        string dataFlow)
    {
        return new Hypothesis(
            Id: $"H-INT-{Guid.NewGuid():N[..8]}",
            Statement: $"We believe that {sourceSystem} can {dataFlow} with {targetSystem}",
            Because: "Both systems expose APIs that appear compatible with our integration pattern",
            SuccessMetric: "Successful end-to-end data flow",
            SuccessThreshold: "Data transfers correctly without manual intervention",
            Status: HypothesisStatus.Proposed,
            Result: null);
    }

    public static Hypothesis Scalability(
        string system,
        int targetScale,
        string scaleUnit)
    {
        return new Hypothesis(
            Id: $"H-SCALE-{Guid.NewGuid():N[..8]}",
            Statement: $"We believe that {system} can scale to {targetScale} {scaleUnit}",
            Because: "Architecture is designed for horizontal scaling and vendor claims support this scale",
            SuccessMetric: $"Concurrent {scaleUnit} supported",
            SuccessThreshold: $"{targetScale} {scaleUnit} with acceptable latency",
            Status: HypothesisStatus.Proposed,
            Result: null);
    }
}
```

## Experiment Design

### Experiment Structure

```csharp
public sealed record Experiment(
    string Id,
    ExperimentType Type,
    string Title,
    IReadOnlyList<Hypothesis> Hypotheses,
    ExperimentDesign Design,
    ExperimentTimeline Timeline,
    ExperimentResources Resources,
    IReadOnlyList<ExperimentRisk> Risks,
    ExperimentStatus Status);

public sealed record ExperimentDesign(
    string Approach,
    IReadOnlyList<string> Variables,
    IReadOnlyList<string> Controls,
    string MeasurementMethod,
    string AnalysisPlan);

public sealed record ExperimentTimeline(
    DateOnly StartDate,
    DateOnly EndDate,
    TimeSpan Timebox,
    IReadOnlyList<Checkpoint> Checkpoints);

public sealed record Checkpoint(
    string Name,
    DateOnly Date,
    string Purpose,
    IReadOnlyList<string> DecisionPoints);
```

### Experiment Lifecycle

```csharp
public sealed class ExperimentLifecycle
{
    public async Task<ExperimentResult> Execute(Experiment experiment)
    {
        // 1. Setup
        await Setup(experiment);

        // 2. Execute with checkpoints
        foreach (var checkpoint in experiment.Timeline.Checkpoints)
        {
            var progress = await ExecuteUntilCheckpoint(checkpoint);

            // Evaluate at each checkpoint
            var decision = await EvaluateCheckpoint(checkpoint, progress);
            if (decision == CheckpointDecision.Abort)
            {
                return ExperimentResult.Aborted(
                    "Experiment aborted at checkpoint",
                    progress.Findings);
            }
            if (decision == CheckpointDecision.Pivot)
            {
                await AdjustExperiment(experiment, progress.Learnings);
            }
        }

        // 3. Analyze results
        var analysis = await AnalyzeResults(experiment);

        // 4. Document learnings
        await DocumentLearnings(experiment, analysis);

        // 5. Make recommendation
        return GenerateResult(experiment, analysis);
    }
}

public enum CheckpointDecision
{
    Continue,   // Proceed as planned
    Adjust,     // Minor course correction
    Pivot,      // Major direction change
    Abort       // Stop experiment
}
```

## POC Evaluation

### Evaluation Framework

```csharp
public sealed record POCEvaluation(
    string POCId,
    DateOnly EvaluationDate,
    IReadOnlyList<HypothesisEvaluation> HypothesesResults,
    TechnicalEvaluation Technical,
    OperationalEvaluation Operational,
    IReadOnlyList<string> Strengths,
    IReadOnlyList<string> Weaknesses,
    IReadOnlyList<string> Uncertainties,
    POCVerdict Verdict,
    IReadOnlyList<string> NextSteps);

public sealed record HypothesisEvaluation(
    string HypothesisId,
    HypothesisStatus Result,
    string Evidence,
    double Confidence); // 0-1

public enum POCVerdict
{
    Proceed,            // Full implementation recommended
    ProceedWithCaution, // Proceed but address identified issues
    ExtendPOC,          // Need more investigation
    Pivot,              // Different approach needed
    Abandon             // Concept not viable
}

public sealed class POCEvaluator
{
    public POCVerdict Evaluate(POCEvaluation evaluation)
    {
        var hypothesesPassed = evaluation.HypothesesResults
            .Count(h => h.Result == HypothesisStatus.Validated);
        var hypothesesTotal = evaluation.HypothesesResults.Count;
        var passRate = (double)hypothesesPassed / hypothesesTotal;

        var technicalOk = evaluation.Technical.Rating >= TechnicalRating.Acceptable;
        var operationalOk = evaluation.Operational.Rating >= OperationalRating.Feasible;

        return (passRate, technicalOk, operationalOk) switch
        {
            (>= 0.8, true, true) => POCVerdict.Proceed,
            (>= 0.6, true, true) => POCVerdict.ProceedWithCaution,
            (>= 0.4, true, _) => POCVerdict.ExtendPOC,
            (>= 0.4, false, _) => POCVerdict.Pivot,
            _ => POCVerdict.Abandon
        };
    }
}
```

## Knowledge Capture

### Learning Documentation

```csharp
public sealed record ExperimentLearnings(
    string ExperimentId,
    DateOnly Date,
    IReadOnlyList<KeyLearning> Learnings,
    IReadOnlyList<TechnicalDiscovery> TechnicalDiscoveries,
    IReadOnlyList<string> Surprises,
    IReadOnlyList<string> WhatWorked,
    IReadOnlyList<string> WhatDidnt,
    IReadOnlyList<Recommendation> Recommendations,
    IReadOnlyList<OpenQuestion> RemainingQuestions);

public sealed record KeyLearning(
    string Topic,
    string Learning,
    LearningType Type,
    string Evidence,
    string Implications);

public enum LearningType
{
    Technical,      // How technology works
    Architectural,  // Design patterns/approaches
    Operational,    // How to run/maintain
    Process,        // How to work effectively
    Domain          // Business/domain knowledge
}
```

## Workflow

When planning experiments:

1. **Identify Uncertainty**: What don't we know that we need to know?
2. **Formulate Hypotheses**: What do we believe? How will we test it?
3. **Select Experiment Type**: Spike, POC, Prototype, or Pilot?
4. **Define Scope**: What's in/out? What's the timebox?
5. **Plan Execution**: Milestones, checkpoints, resources
6. **Execute with Checkpoints**: Evaluate progress at each checkpoint
7. **Analyze Results**: Did we validate/invalidate hypotheses?
8. **Document Learnings**: Capture knowledge for future use
9. **Make Decision**: Proceed, pivot, or abandon

## References

For detailed templates:

---

**Last Updated:** 2025-12-26
