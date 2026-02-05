---
name: hitl-design
description: Design human-in-the-loop workflows including review queues, escalation patterns, feedback loops, and quality assurance for AI systems.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Human-in-the-Loop Design

## When to Use This Skill

Use this skill when:

- **Hitl Design tasks** - Working on design human-in-the-loop workflows including review queues, escalation patterns, feedback loops, and quality assurance for ai systems
- **Planning or design** - Need guidance on Hitl Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Human-in-the-Loop (HITL) design creates meaningful human oversight for AI systems. Effective HITL balances automation efficiency with human judgment, ensuring appropriate intervention points without creating bottlenecks.

## HITL Pattern Taxonomy

```text
┌─────────────────────────────────────────────────────────────────┐
│                    HITL PATTERN SPECTRUM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FULL AUTOMATION ◄───────────────────────────► FULL MANUAL       │
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│  │ AI Only  │   │ Human    │   │ Human    │   │ Human    │      │
│  │          │   │ on Loop  │   │ in Loop  │   │ Only     │      │
│  │ No human │   │ Monitor  │   │ Review   │   │ No AI    │      │
│  │ review   │   │ & audit  │   │ & decide │   │          │      │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘      │
│       │              │              │              │             │
│       ▼              ▼              ▼              ▼             │
│  Low stakes    Medium risk    High stakes    Critical/          │
│  High volume   Scalable       Accuracy       Regulated          │
│                oversight      critical                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## HITL Patterns

### Pattern 1: Human-on-the-Loop (Monitoring)

```text
                    ┌─────────────────┐
                    │  Human Monitor  │
                    │  (Dashboard)    │
                    └────────┬────────┘
                             │ Observes
                             ▼
    Input ──► AI Decision ──► Execute ──► Outcome
                    │
                    └──► Alert if anomaly
```

**Use When:**

- High volume, low individual risk
- AI performance is validated
- Rapid response not required
- Audit trail sufficient

### Pattern 2: Human-in-the-Loop (Review)

```text
                        ┌─────────────────┐
                        │  Human Review   │
                        │  Queue          │
                        └────────┬────────┘
                                 │
    Input ──► AI Recommend ──► Review ──► Decision ──► Execute
                    │                         │
                    └─── Low confidence? ─────┘
                              route
```

**Use When:**

- Decisions have significant impact
- Regulatory requirement
- Model confidence varies
- Liability concerns

### Pattern 3: Human-First with AI Assist

```text
    Input ──► Human Decision ──► AI Validation ──► Execute
                    │                   │
                    └─── Suggest ◄──────┘
                         alternatives
```

**Use When:**

- Expert domain knowledge required
- AI augments rather than replaces
- Training/onboarding scenarios
- Building trust in AI

## Decision Routing

### Confidence-Based Routing

```csharp
public class ConfidenceRouter
{
    private readonly HitlConfiguration _config;

    public async Task<RoutingDecision> Route(
        AiPrediction prediction,
        CancellationToken ct)
    {
        // High confidence: Auto-approve
        if (prediction.Confidence >= _config.AutoApproveThreshold)
        {
            return RoutingDecision.AutoApprove(prediction);
        }

        // Low confidence: Human review required
        if (prediction.Confidence <= _config.ManualReviewThreshold)
        {
            return RoutingDecision.RequireHumanReview(
                prediction,
                ReviewPriority.High,
                "Low model confidence");
        }

        // Medium confidence: Risk-based routing
        var riskScore = await CalculateRiskScore(prediction, ct);

        if (riskScore > _config.RiskThreshold)
        {
            return RoutingDecision.RequireHumanReview(
                prediction,
                ReviewPriority.Medium,
                $"Elevated risk score: {riskScore:F2}");
        }

        return RoutingDecision.AutoApproveWithAudit(prediction);
    }

    private async Task<double> CalculateRiskScore(
        AiPrediction prediction,
        CancellationToken ct)
    {
        var factors = new List<double>
        {
            1 - prediction.Confidence,                    // Uncertainty
            prediction.ImpactScore,                       // Potential impact
            prediction.NoveltyScore,                      // Out-of-distribution
            await GetRecentErrorRate(prediction.Category) // Historical errors
        };

        return factors.Average();
    }
}
```

### Rule-Based Routing

```csharp
public class RuleBasedRouter
{
    private readonly List<IRoutingRule> _rules;

    public async Task<RoutingDecision> Route(
        AiPrediction prediction,
        Context context,
        CancellationToken ct)
    {
        foreach (var rule in _rules.OrderByDescending(r => r.Priority))
        {
            if (await rule.Matches(prediction, context, ct))
            {
                return rule.GetDecision(prediction, context);
            }
        }

        return RoutingDecision.Default(prediction);
    }
}

// Example rules
public class HighValueRule : IRoutingRule
{
    public int Priority => 100;

    public Task<bool> Matches(AiPrediction prediction, Context context, CancellationToken ct)
    {
        return Task.FromResult(context.TransactionValue > 10000);
    }

    public RoutingDecision GetDecision(AiPrediction prediction, Context context)
    {
        return RoutingDecision.RequireHumanReview(
            prediction,
            ReviewPriority.High,
            "High-value transaction requires approval");
    }
}

public class RegulatedCategoryRule : IRoutingRule
{
    public int Priority => 90;

    public Task<bool> Matches(AiPrediction prediction, Context context, CancellationToken ct)
    {
        return Task.FromResult(
            context.Category is "medical" or "legal" or "financial");
    }

    public RoutingDecision GetDecision(AiPrediction prediction, Context context)
    {
        return RoutingDecision.RequireHumanReview(
            prediction,
            ReviewPriority.Normal,
            $"Regulated category: {context.Category}");
    }
}
```

## Review Queue Design

### Queue Architecture

```csharp
public class ReviewQueueService
{
    private readonly IReviewItemRepository _repository;
    private readonly IReviewerAssignment _assignment;
    private readonly INotificationService _notifications;

    public async Task<ReviewItem> EnqueueForReview(
        AiPrediction prediction,
        ReviewPriority priority,
        string reason,
        CancellationToken ct)
    {
        var item = new ReviewItem
        {
            Id = Guid.NewGuid(),
            Prediction = prediction,
            Priority = priority,
            Reason = reason,
            CreatedAt = DateTime.UtcNow,
            SlaDeadline = CalculateSla(priority),
            Status = ReviewStatus.Pending
        };

        await _repository.Create(item, ct);

        // Assign to appropriate reviewer
        var assignee = await _assignment.FindReviewer(item, ct);
        if (assignee != null)
        {
            item.AssignedTo = assignee;
            await _repository.Update(item, ct);
            await _notifications.NotifyAssignment(assignee, item, ct);
        }

        return item;
    }

    public async Task<ReviewItem> ClaimNext(
        string reviewerId,
        ReviewerCapabilities capabilities,
        CancellationToken ct)
    {
        // Find next appropriate item for reviewer
        var item = await _repository.FindNextUnassigned(
            capabilities.Categories,
            capabilities.MaxPriority,
            ct);

        if (item == null) return null;

        item.AssignedTo = reviewerId;
        item.ClaimedAt = DateTime.UtcNow;
        item.Status = ReviewStatus.InProgress;

        await _repository.Update(item, ct);

        return item;
    }

    public async Task SubmitReview(
        Guid itemId,
        string reviewerId,
        ReviewDecision decision,
        CancellationToken ct)
    {
        var item = await _repository.GetById(itemId, ct);

        if (item.AssignedTo != reviewerId)
            throw new UnauthorizedAccessException("Item not assigned to reviewer");

        item.Decision = decision;
        item.CompletedAt = DateTime.UtcNow;
        item.Status = ReviewStatus.Completed;

        await _repository.Update(item, ct);

        // Record for model improvement
        await RecordFeedback(item, decision, ct);

        // Trigger downstream actions
        await ProcessDecision(item, decision, ct);
    }

    private DateTime CalculateSla(ReviewPriority priority)
    {
        return priority switch
        {
            ReviewPriority.Critical => DateTime.UtcNow.AddMinutes(15),
            ReviewPriority.High => DateTime.UtcNow.AddHours(1),
            ReviewPriority.Normal => DateTime.UtcNow.AddHours(4),
            ReviewPriority.Low => DateTime.UtcNow.AddDays(1),
            _ => DateTime.UtcNow.AddHours(4)
        };
    }
}
```

### Review Interface Design

```markdown
## Review Interface Requirements

### Essential Information
- Original input/request
- AI prediction/recommendation
- Confidence score with explanation
- Supporting evidence/context
- Similar historical cases
- Risk indicators

### Reviewer Actions
- Approve (accept AI recommendation)
- Reject (override with reason)
- Modify (adjust AI recommendation)
- Escalate (route to specialist)
- Defer (need more information)

### Ergonomic Considerations
- Keyboard shortcuts for common actions
- Batch review mode for similar items
- Quick filters and sorting
- Time tracking for fatigue management
- Random audits of auto-approved items
```

## Escalation Patterns

### Escalation Workflow

```csharp
public class EscalationService
{
    private readonly List<EscalationLevel> _levels;

    public async Task<EscalationResult> Escalate(
        ReviewItem item,
        string reason,
        string escalatingReviewer,
        CancellationToken ct)
    {
        var currentLevel = item.EscalationLevel ?? 0;
        var nextLevel = _levels.FirstOrDefault(l => l.Level == currentLevel + 1);

        if (nextLevel == null)
        {
            return EscalationResult.MaxLevelReached();
        }

        item.EscalationLevel = nextLevel.Level;
        item.EscalationReason = reason;
        item.EscalatedBy = escalatingReviewer;
        item.EscalatedAt = DateTime.UtcNow;

        // Find appropriate escalation target
        var target = await FindEscalationTarget(nextLevel, item, ct);

        item.AssignedTo = target.ReviewerId;

        await _repository.Update(item, ct);
        await _notifications.NotifyEscalation(target, item, reason, ct);

        return EscalationResult.Escalated(nextLevel, target);
    }
}

public record EscalationLevel(
    int Level,
    string Name,
    TimeSpan SlaOverride,
    string[] RequiredCapabilities
);
```

### Escalation Triggers

| Trigger | Description | Target |
|---------|-------------|--------|
| Complexity | Requires specialized knowledge | Subject matter expert |
| Conflict | Disagreement with AI/policy | Senior reviewer |
| Risk | High-impact decision | Manager/compliance |
| Timeout | SLA approaching | Next available |
| Uncertainty | Reviewer unsure | Second opinion |

## Feedback Loops

### Learning from Human Decisions

```csharp
public class FeedbackCollector
{
    public async Task RecordFeedback(
        ReviewItem item,
        ReviewDecision decision,
        CancellationToken ct)
    {
        var feedback = new HumanFeedback
        {
            ItemId = item.Id,
            OriginalPrediction = item.Prediction,
            HumanDecision = decision,
            Agreement = decision.Action == DecisionAction.Approve,
            ReviewerId = item.AssignedTo,
            ReviewDurationMs = CalculateDuration(item),
            Context = ExtractContext(item)
        };

        await _feedbackStore.Store(feedback, ct);

        // Aggregate for model retraining
        if (ShouldTriggerRetraining())
        {
            await _retrainingService.QueueRetraining(ct);
        }

        // Alert on significant disagreement patterns
        await CheckForSystematicDisagreement(feedback, ct);
    }

    private async Task CheckForSystematicDisagreement(
        HumanFeedback feedback,
        CancellationToken ct)
    {
        var recentFeedback = await _feedbackStore.GetRecent(
            category: feedback.Context.Category,
            hours: 24,
            ct);

        var disagreementRate = recentFeedback
            .Count(f => !f.Agreement) / (double)recentFeedback.Count;

        if (disagreementRate > 0.3)
        {
            await _alerts.Send(new SystematicDisagreementAlert
            {
                Category = feedback.Context.Category,
                DisagreementRate = disagreementRate,
                SampleSize = recentFeedback.Count
            });
        }
    }
}
```

### Active Learning Integration

```csharp
public class ActiveLearningSelector
{
    public async Task<IEnumerable<ReviewItem>> SelectForLabeling(
        int count,
        CancellationToken ct)
    {
        // Uncertainty sampling: Select items where model is most uncertain
        var uncertainItems = await _predictions
            .Where(p => p.Status == PredictionStatus.Pending)
            .OrderBy(p => Math.Abs(p.Confidence - 0.5))
            .Take(count / 2)
            .ToListAsync(ct);

        // Diversity sampling: Select diverse examples
        var diverseItems = await SelectDiverseExamples(count / 2, ct);

        return uncertainItems.Concat(diverseItems);
    }
}
```

## HITL Metrics

### Key Performance Indicators

| Metric | Description | Target |
|--------|-------------|--------|
| Throughput | Reviews per hour | Varies by domain |
| Cycle Time | Queue to decision | < SLA |
| Agreement Rate | Human-AI alignment | > 85% |
| Override Rate | Human overrides AI | < 15% |
| Escalation Rate | Items escalated | < 10% |
| Reviewer Fatigue | Accuracy over time | Stable |

### Dashboard Design

```csharp
public class HitlDashboard
{
    public async Task<DashboardData> GetMetrics(
        DateRange range,
        CancellationToken ct)
    {
        return new DashboardData
        {
            // Volume metrics
            TotalReviews = await CountReviews(range, ct),
            PendingItems = await CountPending(ct),
            QueueDepthByPriority = await GetQueueDepth(ct),

            // Efficiency metrics
            AverageCycleTime = await CalculateAverageCycleTime(range, ct),
            SlaMet = await CalculateSlaCompliance(range, ct),
            ThroughputByReviewer = await GetThroughput(range, ct),

            // Quality metrics
            AgreementRate = await CalculateAgreementRate(range, ct),
            OverridesByReason = await GetOverrideReasons(range, ct),
            EscalationRate = await CalculateEscalationRate(range, ct),

            // Trends
            VolumeOverTime = await GetVolumeTrend(range, ct),
            AgreementOverTime = await GetAgreementTrend(range, ct)
        };
    }
}
```

## HITL Design Template

```markdown
# HITL Design: [System Name]

## 1. System Overview
- **AI Function**: [What the AI does]
- **Decision Impact**: [Low/Medium/High/Critical]
- **Volume**: [Expected decisions per day]

## 2. Routing Strategy

### Auto-Approve Criteria
- Confidence > [X]%
- Category in [list]
- Risk score < [threshold]

### Human Review Required
- Confidence < [X]%
- Category in [regulated list]
- First-time patterns
- [Other criteria]

## 3. Review Queue Design

### Prioritization
| Priority | SLA | Criteria |
|----------|-----|----------|
| Critical | 15 min | [Criteria] |
| High | 1 hour | [Criteria] |
| Normal | 4 hours | [Criteria] |

### Reviewer Assignment
- [Assignment strategy]
- Required capabilities: [List]

## 4. Review Interface
- Information displayed: [List]
- Available actions: [List]
- Keyboard shortcuts: [Enabled/Disabled]

## 5. Escalation Path
| Level | Role | Trigger |
|-------|------|---------|
| 1 | [Role] | [Trigger] |
| 2 | [Role] | [Trigger] |

## 6. Feedback Loop
- Training data collection: [Yes/No]
- Retraining trigger: [Criteria]
- Disagreement monitoring: [Threshold]

## 7. Metrics & Monitoring
- Dashboard: [Link]
- Alerting: [Thresholds]
```

## Validation Checklist

- [ ] HITL pattern selected
- [ ] Routing criteria defined
- [ ] Review queue designed
- [ ] Escalation path established
- [ ] Interface requirements specified
- [ ] SLAs defined
- [ ] Feedback loop implemented
- [ ] Metrics dashboard created
- [ ] Reviewer training planned
- [ ] Capacity planning completed

## Integration Points

**Inputs from**:

- `ai-safety-planning` skill → Oversight requirements
- `explainability-planning` skill → Review explanations
- Regulatory requirements → Review mandates

**Outputs to**:

- `ml-project-lifecycle` skill → Feedback for retraining
- Application code → Queue implementation
- Operations → Staffing requirements

**Last Updated:** 2025-12-27
