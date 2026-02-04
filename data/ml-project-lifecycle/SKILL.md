---
name: ml-project-lifecycle
description: Plan ML projects using CRISP-DM, TDSP, and MLOps methodologies with proper phase gates and deliverables.
allowed-tools: Read, Write, Glob, Grep, Task
---

# ML Project Lifecycle Planning

## When to Use This Skill

Use this skill when:

- **Ml Project Lifecycle tasks** - Working on plan ml projects using crisp-dm, tdsp, and mlops methodologies with proper phase gates and deliverables
- **Planning or design** - Need guidance on Ml Project Lifecycle approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

ML project lifecycle methodologies provide structured approaches for planning, executing, and deploying machine learning systems with appropriate governance and quality gates.

## CRISP-DM Methodology

### Six Phases

```text
┌─────────────────────────────────────────────────────────────────┐
│                        CRISP-DM Cycle                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│         ┌─────────────────────┐                                 │
│         │   1. Business       │                                 │
│         │   Understanding     │                                 │
│         └────────┬────────────┘                                 │
│                  │                                               │
│    ┌─────────────┼─────────────┐                                │
│    │             ▼             │                                │
│    │  ┌─────────────────────┐  │                                │
│    │  │  2. Data            │  │                                │
│    │  │  Understanding      │  │                                │
│    │  └────────┬────────────┘  │                                │
│    │           │               │                                │
│    │           ▼               │                                │
│    │  ┌─────────────────────┐  │                                │
│    │  │  3. Data            │  │                                │
│    │  │  Preparation        │  │                                │
│    │  └────────┬────────────┘  │                                │
│    │           │               │                                │
│    │           ▼               │                                │
│    │  ┌─────────────────────┐  │                                │
│    │  │  4. Modeling        │  │                                │
│    │  └────────┬────────────┘  │                                │
│    │           │               │                                │
│    │           ▼               │                                │
│    │  ┌─────────────────────┐  │                                │
│    │  │  5. Evaluation      │  │◄──── Go/No-Go Decision        │
│    │  └────────┬────────────┘  │                                │
│    │           │               │                                │
│    └───────────┼───────────────┘                                │
│                ▼                                                 │
│         ┌─────────────────────┐                                 │
│         │  6. Deployment      │                                 │
│         └─────────────────────┘                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Phase Details

| Phase | Key Activities | Deliverables |
|-------|---------------|--------------|
| Business Understanding | Define objectives, success criteria | Business requirements doc |
| Data Understanding | Explore, describe, verify data | Data quality report |
| Data Preparation | Clean, transform, feature engineer | Training datasets |
| Modeling | Select algorithms, train, tune | Model artifacts, metrics |
| Evaluation | Assess model, review process | Evaluation report |
| Deployment | Deploy, monitor, maintain | Production system |

## MLOps Maturity Levels

### Level Assessment

| Level | Description | Characteristics |
|-------|-------------|-----------------|
| 0 | Manual | No automation, ad-hoc experiments |
| 1 | ML Pipeline | Automated training, manual deployment |
| 2 | CI/CD Pipeline | Automated training and deployment |
| 3 | Full MLOps | Automated monitoring, retraining |

### MLOps Components

```text
┌─────────────────────────────────────────────────────────────────┐
│                      MLOps Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐              │
│  │ Data       │   │ Feature    │   │ Model      │              │
│  │ Pipeline   │──►│ Store      │──►│ Training   │              │
│  └────────────┘   └────────────┘   └─────┬──────┘              │
│                                          │                      │
│  ┌────────────┐   ┌────────────┐   ┌─────▼──────┐              │
│  │ Monitoring │◄──│ Model      │◄──│ Model      │              │
│  │ & Alerts   │   │ Serving    │   │ Registry   │              │
│  └────────────┘   └────────────┘   └────────────┘              │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Experiment Tracking & Versioning            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Project Planning Template

```markdown
# ML Project Plan: [Project Name]

## 1. Business Understanding

### Objectives
- Primary goal: [What business problem are we solving?]
- Success metrics: [How will we measure success?]
- Stakeholders: [Who will use/be affected by this?]

### Constraints
- Timeline: [Project duration]
- Resources: [Team, compute, budget]
- Data availability: [What data do we have access to?]

## 2. Data Understanding

### Data Sources
| Source | Type | Volume | Refresh |
|--------|------|--------|---------|
| [Source 1] | [Type] | [Size] | [Frequency] |

### Data Quality Assessment
- Completeness: [% complete]
- Accuracy: [Validation approach]
- Timeliness: [Data freshness]

## 3. Data Preparation

### Feature Engineering Plan
| Feature | Source | Transformation | Rationale |
|---------|--------|----------------|-----------|
| [Feature 1] | [Column] | [Transform] | [Why] |

### Data Pipeline
- Extraction: [Method]
- Transformation: [Tools/approach]
- Loading: [Destination]

## 4. Modeling Approach

### Algorithm Selection
| Algorithm | Pros | Cons | Priority |
|-----------|------|------|----------|
| [Algorithm 1] | [Pros] | [Cons] | [1-3] |

### Experimentation Plan
- Baseline: [Simple model for comparison]
- Iterations: [Planned experiments]
- Hyperparameter strategy: [Grid/random/bayesian]

## 5. Evaluation Criteria

### Metrics
| Metric | Target | Baseline | Importance |
|--------|--------|----------|------------|
| [Metric 1] | [Target] | [Current] | [High/Med/Low] |

### Go/No-Go Criteria
- Minimum performance: [Threshold]
- Business validation: [Process]

## 6. Deployment Plan

### Serving Architecture
- Inference type: [Real-time/Batch]
- Infrastructure: [Cloud/Edge]
- Scaling: [Strategy]

### Monitoring
- Metrics: [What to track]
- Alerts: [Thresholds]
- Retraining: [Trigger conditions]
```

## Experiment Tracking

### Tracking Requirements

| Category | Items to Track |
|----------|---------------|
| Parameters | Hyperparameters, configs |
| Metrics | Loss, accuracy, custom |
| Artifacts | Models, plots, data |
| Environment | Dependencies, hardware |
| Code | Git commit, branch |

### MLflow Integration

```csharp
// Semantic Kernel with experiment tracking
public class ExperimentTracker
{
    public async Task TrackExperiment(
        string experimentName,
        Func<Task<ExperimentResult>> experiment)
    {
        var runId = Guid.NewGuid().ToString();
        var startTime = DateTime.UtcNow;

        try
        {
            // Log parameters
            await LogParameters(runId, new Dictionary<string, object>
            {
                ["model"] = "gpt-4o",
                ["temperature"] = 0.7,
                ["max_tokens"] = 1000
            });

            // Run experiment
            var result = await experiment();

            // Log metrics
            await LogMetrics(runId, new Dictionary<string, double>
            {
                ["accuracy"] = result.Accuracy,
                ["latency_ms"] = result.LatencyMs,
                ["token_cost"] = result.TokenCost
            });

            // Log artifacts
            await LogArtifact(runId, "prompt.txt", result.Prompt);
            await LogArtifact(runId, "response.json", result.Response);
        }
        finally
        {
            var duration = DateTime.UtcNow - startTime;
            await LogMetric(runId, "duration_seconds", duration.TotalSeconds);
        }
    }
}
```

## Model Registry

### Registry Structure

```markdown
# Model Registry Entry

## Model: customer-churn-predictor

### Versions
| Version | Stage | Created | Metrics | Notes |
|---------|-------|---------|---------|-------|
| v1.0.0 | Production | 2024-01-15 | AUC: 0.85 | Baseline |
| v1.1.0 | Staging | 2024-02-01 | AUC: 0.88 | New features |
| v1.2.0 | Development | 2024-02-15 | AUC: 0.89 | Tuned |

### Promotion Criteria
- [ ] Performance >= baseline + 2%
- [ ] No regression on fairness metrics
- [ ] A/B test shows positive lift
- [ ] Stakeholder approval
```

## Validation Checklist

- [ ] Business objectives clearly defined
- [ ] Success metrics identified and measurable
- [ ] Data sources identified and accessible
- [ ] Data quality assessed
- [ ] Feature engineering strategy defined
- [ ] Modeling approach selected
- [ ] Evaluation criteria established
- [ ] Deployment architecture planned
- [ ] Monitoring strategy defined
- [ ] MLOps maturity level targeted

## Integration Points

**Inputs from**:

- Business requirements → Success criteria
- Data architecture → Data sources
- Compliance planning → Regulatory requirements

**Outputs to**:

- `model-selection` skill → Algorithm choices
- `ai-safety-planning` skill → Safety requirements
- `token-budgeting` skill → Cost estimation
