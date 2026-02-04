---
name: token-budgeting
description: Estimate and optimize AI/ML costs including token usage, context window management, batch processing, and caching strategies.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Token Budgeting and Cost Optimization

## When to Use This Skill

Use this skill when:

- **Token Budgeting tasks** - Working on estimate and optimize ai/ml costs including token usage, context window management, batch processing, and caching strategies
- **Planning or design** - Need guidance on Token Budgeting approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Token budgeting involves estimating, monitoring, and optimizing the costs of AI/ML systems, particularly LLMs. Effective budgeting prevents cost overruns, enables accurate forecasting, and identifies optimization opportunities.

## Cost Structure

### LLM Pricing Components

```text
┌─────────────────────────────────────────────────────────────────┐
│                    LLM COST COMPONENTS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DIRECT COSTS                                                    │
│  ├── Input tokens (prompt + context)                            │
│  ├── Output tokens (completion)                                 │
│  ├── Cached input tokens (discounted)                           │
│  └── Image/audio/video processing                               │
│                                                                  │
│  INDIRECT COSTS                                                  │
│  ├── Embedding generation                                       │
│  ├── Vector storage and queries                                 │
│  ├── Fine-tuning (training + hosting)                           │
│  └── Infrastructure (compute, network)                          │
│                                                                  │
│  HIDDEN COSTS                                                    │
│  ├── Retries and error handling                                 │
│  ├── Development/testing usage                                  │
│  ├── Prompt iteration during development                        │
│  └── Monitoring and logging overhead                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Current Pricing Reference (December 2025)

| Model | Input ($/1M) | Output ($/1M) | Cached Input | Notes |
|-------|-------------|---------------|--------------|-------|
| GPT-4o | $2.50 | $10.00 | $1.25 | Standard |
| GPT-4o-mini | $0.15 | $0.60 | $0.075 | Budget |
| o1 | $15.00 | $60.00 | N/A | Reasoning |
| o1-mini | $3.00 | $12.00 | N/A | Reasoning budget |
| Claude 3.5 Sonnet | $3.00 | $15.00 | $0.30 | Prompt caching |
| Claude 3.5 Haiku | $0.25 | $1.25 | $0.03 | Fast |
| Gemini 1.5 Pro | $1.25 | $5.00 | Varies | Context caching |
| Gemini 1.5 Flash | $0.075 | $0.30 | Varies | High volume |

## Cost Estimation

### Token Counting

```csharp
public class TokenCounter
{
    private readonly Tokenizer _tokenizer;

    public TokenEstimate EstimateTokens(
        string systemPrompt,
        string userMessage,
        List<Message> conversationHistory,
        int expectedOutputTokens)
    {
        var systemTokens = _tokenizer.CountTokens(systemPrompt);
        var userTokens = _tokenizer.CountTokens(userMessage);
        var historyTokens = conversationHistory
            .Sum(m => _tokenizer.CountTokens(m.Content));

        var totalInputTokens = systemTokens + userTokens + historyTokens;

        return new TokenEstimate
        {
            SystemPromptTokens = systemTokens,
            UserMessageTokens = userTokens,
            ConversationHistoryTokens = historyTokens,
            TotalInputTokens = totalInputTokens,
            EstimatedOutputTokens = expectedOutputTokens,
            TotalTokens = totalInputTokens + expectedOutputTokens
        };
    }

    public CostEstimate EstimateCost(
        TokenEstimate tokens,
        ModelPricing pricing)
    {
        var inputCost = tokens.TotalInputTokens / 1_000_000.0m
            * pricing.InputPricePerMillion;

        var outputCost = tokens.EstimatedOutputTokens / 1_000_000.0m
            * pricing.OutputPricePerMillion;

        return new CostEstimate
        {
            InputCost = inputCost,
            OutputCost = outputCost,
            TotalCost = inputCost + outputCost,
            Breakdown = new CostBreakdown
            {
                SystemPromptCost = tokens.SystemPromptTokens / 1_000_000.0m * pricing.InputPricePerMillion,
                UserMessageCost = tokens.UserMessageTokens / 1_000_000.0m * pricing.InputPricePerMillion,
                HistoryCost = tokens.ConversationHistoryTokens / 1_000_000.0m * pricing.InputPricePerMillion,
                OutputCost = outputCost
            }
        };
    }
}
```

### Monthly Cost Projection

```csharp
public class CostProjector
{
    public MonthlyProjection ProjectMonthlyCost(
        UsagePattern usage,
        ModelPricing pricing)
    {
        // Calculate base costs
        var avgInputTokens = usage.AverageInputTokens;
        var avgOutputTokens = usage.AverageOutputTokens;
        var requestsPerDay = usage.DailyRequests;

        var costPerRequest = CalculateCostPerRequest(
            avgInputTokens, avgOutputTokens, pricing);

        var dailyCost = costPerRequest * requestsPerDay;
        var monthlyCost = dailyCost * 30;

        // Add overhead for retries and errors
        var retryOverhead = monthlyCost * (usage.ErrorRate / 100);

        // Development/testing overhead
        var devOverhead = monthlyCost * 0.15; // 15% for dev/test

        return new MonthlyProjection
        {
            BaseCost = monthlyCost,
            RetryOverhead = retryOverhead,
            DevelopmentOverhead = devOverhead,
            TotalProjected = monthlyCost + retryOverhead + devOverhead,
            CostPerRequest = costPerRequest,
            DailyBudget = (monthlyCost + retryOverhead + devOverhead) / 30,

            Assumptions = new ProjectionAssumptions
            {
                DailyRequests = requestsPerDay,
                AverageInputTokens = avgInputTokens,
                AverageOutputTokens = avgOutputTokens,
                ErrorRate = usage.ErrorRate,
                DevOverheadPercent = 15
            }
        };
    }

    public ScenarioAnalysis ProjectScenarios(
        UsagePattern baseUsage,
        ModelPricing pricing)
    {
        return new ScenarioAnalysis
        {
            Conservative = ProjectMonthlyCost(
                baseUsage with { DailyRequests = baseUsage.DailyRequests * 0.7m },
                pricing),

            Expected = ProjectMonthlyCost(baseUsage, pricing),

            Aggressive = ProjectMonthlyCost(
                baseUsage with { DailyRequests = baseUsage.DailyRequests * 1.5m },
                pricing),

            Viral = ProjectMonthlyCost(
                baseUsage with { DailyRequests = baseUsage.DailyRequests * 5m },
                pricing)
        };
    }
}
```

## Optimization Strategies

### Context Window Management

```csharp
public class ContextManager
{
    private readonly int _maxTokens;
    private readonly int _reservedForOutput;

    public ManagedContext ManageContext(
        string systemPrompt,
        string userMessage,
        List<Message> history,
        List<Document> retrievedDocs)
    {
        var available = _maxTokens - _reservedForOutput;
        var used = 0;

        var result = new ManagedContext();

        // Priority 1: System prompt (always include)
        result.SystemPrompt = systemPrompt;
        used += CountTokens(systemPrompt);

        // Priority 2: Current user message
        result.UserMessage = userMessage;
        used += CountTokens(userMessage);

        // Priority 3: Retrieved documents (most relevant first)
        result.Documents = new List<Document>();
        foreach (var doc in retrievedDocs.OrderByDescending(d => d.Relevance))
        {
            var docTokens = CountTokens(doc.Content);
            if (used + docTokens <= available * 0.6) // Reserve 40% for history
            {
                result.Documents.Add(doc);
                used += docTokens;
            }
            else break;
        }

        // Priority 4: Conversation history (most recent first)
        result.History = new List<Message>();
        foreach (var msg in history.AsEnumerable().Reverse())
        {
            var msgTokens = CountTokens(msg.Content);
            if (used + msgTokens <= available)
            {
                result.History.Insert(0, msg);
                used += msgTokens;
            }
            else break;
        }

        result.TotalTokens = used;
        result.AvailableForOutput = _maxTokens - used;

        return result;
    }
}
```

### Prompt Caching Strategy

```csharp
public class CacheOptimizer
{
    public CacheStrategy OptimizeCaching(
        PromptTemplate template,
        UsagePattern usage)
    {
        // Identify static vs dynamic content
        var staticParts = template.GetStaticParts();
        var dynamicParts = template.GetDynamicParts();

        var staticTokens = staticParts.Sum(CountTokens);
        var dynamicTokens = dynamicParts.Average(d => CountTokens(d.AverageValue));

        // Calculate cache effectiveness
        var requestsPerCachePeriod = usage.DailyRequests * (5.0 / 60 / 24); // 5-min cache
        var cacheHitRate = Math.Min(0.9, 1 - (1.0 / requestsPerCachePeriod));

        var withoutCaching = (staticTokens + dynamicTokens) * usage.InputPricePerMillion;
        var withCaching = (staticTokens * (1 - cacheHitRate) + staticTokens * cacheHitRate * 0.1)
            * usage.InputPricePerMillion + dynamicTokens * usage.InputPricePerMillion;

        var savings = (withoutCaching - withCaching) / withoutCaching;

        return new CacheStrategy
        {
            StaticPrefix = string.Join("\n", staticParts),
            StaticTokens = staticTokens,
            DynamicSuffix = "[Dynamic content here]",
            DynamicTokens = (int)dynamicTokens,
            EstimatedCacheHitRate = cacheHitRate,
            EstimatedSavings = savings,
            RecommendCaching = savings > 0.2 // >20% savings
        };
    }
}
```

### Batch Processing

```csharp
public class BatchOptimizer
{
    public BatchStrategy AnalyzeBatchPotential(
        List<PendingRequest> requests,
        LatencyRequirements latency)
    {
        if (latency.MaxLatencyMs < 5000) // Real-time requirement
        {
            return BatchStrategy.NoBatching("Real-time latency required");
        }

        // Group similar requests
        var groups = requests
            .GroupBy(r => r.TaskType)
            .Select(g => new RequestGroup
            {
                TaskType = g.Key,
                Count = g.Count(),
                AverageTokens = g.Average(r => r.EstimatedTokens)
            })
            .ToList();

        // Calculate optimal batch sizes
        var recommendations = groups.Select(g =>
        {
            var optimalBatchSize = CalculateOptimalBatchSize(g, latency);
            var savings = CalculateBatchSavings(g, optimalBatchSize);

            return new BatchRecommendation
            {
                TaskType = g.TaskType,
                OptimalBatchSize = optimalBatchSize,
                EstimatedSavings = savings,
                MaxWaitTime = latency.MaxLatencyMs
            };
        }).ToList();

        return new BatchStrategy
        {
            Enabled = true,
            Recommendations = recommendations,
            TotalEstimatedSavings = recommendations.Average(r => r.EstimatedSavings)
        };
    }

    private int CalculateOptimalBatchSize(RequestGroup group, LatencyRequirements latency)
    {
        // Balance throughput vs latency
        var maxBatchForLatency = latency.MaxLatencyMs / 100; // Rough estimate
        var idealBatch = 50; // OpenAI batch API sweet spot

        return Math.Min(maxBatchForLatency, idealBatch);
    }
}
```

### Model Selection for Cost

```csharp
public class CostAwareModelSelector
{
    public ModelRecommendation SelectCostOptimalModel(
        TaskRequirements requirements,
        List<ModelProfile> availableModels)
    {
        var qualifiedModels = availableModels
            .Where(m => MeetsRequirements(m, requirements))
            .ToList();

        if (!qualifiedModels.Any())
        {
            throw new NoQualifiedModelException("No models meet requirements");
        }

        // Calculate effective cost per quality unit
        var scored = qualifiedModels.Select(m => new
        {
            Model = m,
            QualityScore = CalculateQualityScore(m, requirements),
            EstimatedCost = EstimateCost(m, requirements.AverageTokens),
            CostEfficiency = CalculateQualityScore(m, requirements) / EstimateCost(m, requirements.AverageTokens)
        }).OrderByDescending(s => s.CostEfficiency)
          .ToList();

        var best = scored.First();

        return new ModelRecommendation
        {
            PrimaryModel = best.Model,
            CostEfficiencyScore = best.CostEfficiency,
            EstimatedMonthlyCost = best.EstimatedCost * requirements.MonthlyRequests,
            Alternatives = scored.Skip(1).Take(2).Select(s => s.Model).ToList(),
            Rationale = GenerateRationale(best, scored)
        };
    }

    public CascadeStrategy DesignModelCascade(
        TaskRequirements requirements,
        List<ModelProfile> availableModels)
    {
        // Smaller model first, escalate if needed
        var sortedByComplexity = availableModels
            .Where(m => MeetsMinimumRequirements(m, requirements))
            .OrderBy(m => m.CostPerMillionTokens)
            .ToList();

        return new CascadeStrategy
        {
            Stages = sortedByComplexity.Take(3).Select((m, i) => new CascadeStage
            {
                Order = i + 1,
                Model = m,
                EscalationCriteria = i == 0 ? "Confidence < 0.8" : $"Confidence < {0.9 + i * 0.05}"
            }).ToList(),
            ExpectedSavings = CalculateCascadeSavings(sortedByComplexity, requirements)
        };
    }
}
```

## Cost Monitoring

### Real-Time Tracking

```csharp
public class CostMonitor
{
    private readonly ICostStore _store;
    private readonly IAlertService _alerts;
    private readonly BudgetConfiguration _budget;

    public async Task RecordUsage(
        UsageRecord usage,
        CancellationToken ct)
    {
        await _store.Record(usage, ct);

        // Check budget thresholds
        var dailyTotal = await _store.GetDailyTotal(DateTime.UtcNow.Date, ct);
        var monthlyTotal = await _store.GetMonthlyTotal(DateTime.UtcNow.Month, ct);

        if (dailyTotal > _budget.DailyWarningThreshold)
        {
            await _alerts.SendWarning(new BudgetWarning
            {
                Period = "daily",
                Current = dailyTotal,
                Threshold = _budget.DailyWarningThreshold,
                Limit = _budget.DailyLimit
            });
        }

        if (monthlyTotal > _budget.MonthlyWarningThreshold)
        {
            await _alerts.SendWarning(new BudgetWarning
            {
                Period = "monthly",
                Current = monthlyTotal,
                Threshold = _budget.MonthlyWarningThreshold,
                Limit = _budget.MonthlyLimit
            });
        }

        if (dailyTotal >= _budget.DailyLimit || monthlyTotal >= _budget.MonthlyLimit)
        {
            await _alerts.SendCritical(new BudgetExceeded
            {
                Daily = dailyTotal >= _budget.DailyLimit,
                Monthly = monthlyTotal >= _budget.MonthlyLimit
            });
        }
    }

    public async Task<CostReport> GenerateReport(
        DateRange range,
        CancellationToken ct)
    {
        var usage = await _store.GetUsage(range, ct);

        return new CostReport
        {
            TotalCost = usage.Sum(u => u.Cost),
            ByModel = usage.GroupBy(u => u.Model)
                .ToDictionary(g => g.Key, g => g.Sum(u => u.Cost)),
            ByEndpoint = usage.GroupBy(u => u.Endpoint)
                .ToDictionary(g => g.Key, g => g.Sum(u => u.Cost)),
            ByUser = usage.GroupBy(u => u.UserId)
                .ToDictionary(g => g.Key, g => g.Sum(u => u.Cost)),
            DailyTrend = usage.GroupBy(u => u.Timestamp.Date)
                .OrderBy(g => g.Key)
                .Select(g => new DailyCost { Date = g.Key, Cost = g.Sum(u => u.Cost) })
                .ToList(),
            TopExpensive = usage.OrderByDescending(u => u.Cost).Take(10).ToList(),
            Recommendations = GenerateRecommendations(usage)
        };
    }
}
```

## Budget Planning Template

```markdown
# Token Budget: [Project Name]

## 1. Usage Estimates

### Request Volume
| Period | Requests | Growth Rate |
|--------|----------|-------------|
| Launch | [N/day] | - |
| Month 3 | [N/day] | [X%] |
| Month 6 | [N/day] | [X%] |
| Year 1 | [N/day] | [X%] |

### Token Estimates
| Component | Avg Tokens | Notes |
|-----------|------------|-------|
| System prompt | [N] | [Notes] |
| User input | [N] | [Notes] |
| Context/RAG | [N] | [Notes] |
| Output | [N] | [Notes] |
| **Total/request** | [N] | |

## 2. Model Selection

### Primary Model
- **Model**: [Name]
- **Rationale**: [Why this model]
- **Cost/request**: $[X.XXXX]

### Fallback Model
- **Model**: [Name]
- **Use when**: [Criteria]
- **Cost/request**: $[X.XXXX]

## 3. Cost Projections

| Scenario | Daily | Monthly | Annual |
|----------|-------|---------|--------|
| Conservative | $[X] | $[X] | $[X] |
| Expected | $[X] | $[X] | $[X] |
| Aggressive | $[X] | $[X] | $[X] |

## 4. Optimization Plan

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| Prompt caching | [X%] | [Approach] |
| Batch processing | [X%] | [Approach] |
| Model cascading | [X%] | [Approach] |
| Context pruning | [X%] | [Approach] |

## 5. Budget Controls

### Thresholds
- Daily warning: $[X]
- Daily limit: $[X]
- Monthly warning: $[X]
- Monthly limit: $[X]

### Actions
- At warning: [Action]
- At limit: [Action]

## 6. Monitoring
- Dashboard: [Link]
- Alerting: [Configuration]
- Review cadence: [Frequency]
```

## Validation Checklist

- [ ] Token estimates calculated
- [ ] Usage patterns projected
- [ ] Model pricing confirmed
- [ ] Monthly costs estimated
- [ ] Optimization strategies identified
- [ ] Caching strategy defined
- [ ] Budget thresholds set
- [ ] Monitoring configured
- [ ] Alerting established
- [ ] Review process defined

## Integration Points

**Inputs from**:

- `model-selection` skill → Model pricing
- `rag-architecture` skill → Retrieval costs
- Usage forecasts → Volume estimates

**Outputs to**:

- `ml-project-lifecycle` skill → Project budgeting
- Operations → Cost monitoring
- Finance → Budget planning
