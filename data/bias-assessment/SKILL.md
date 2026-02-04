---
name: bias-assessment
description: Evaluate AI systems for fairness using demographic parity, equalized odds, and bias detection techniques with mitigation strategies.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Bias Assessment Framework

## When to Use This Skill

Use this skill when:

- **Bias Assessment tasks** - Working on evaluate ai systems for fairness using demographic parity, equalized odds, and bias detection techniques with mitigation strategies
- **Planning or design** - Need guidance on Bias Assessment approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Bias assessment systematically evaluates AI systems for unfair treatment across demographic groups. Effective assessment requires defining fairness criteria, measuring disparities, and implementing mitigations while documenting trade-offs.

## Fairness Definitions

### Fairness Metric Taxonomy

```text
┌─────────────────────────────────────────────────────────────────┐
│                    FAIRNESS METRICS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  GROUP FAIRNESS (Statistical Parity)                            │
│  ├── Demographic Parity: P(Ŷ=1|A=0) = P(Ŷ=1|A=1)               │
│  ├── Equalized Odds: P(Ŷ=1|Y=y,A=0) = P(Ŷ=1|Y=y,A=1)           │
│  ├── Equal Opportunity: P(Ŷ=1|Y=1,A=0) = P(Ŷ=1|Y=1,A=1)         │
│  └── Predictive Parity: P(Y=1|Ŷ=1,A=0) = P(Y=1|Ŷ=1,A=1)         │
│                                                                  │
│  INDIVIDUAL FAIRNESS                                             │
│  ├── Similar individuals → Similar predictions                  │
│  └── Counterfactual fairness                                    │
│                                                                  │
│  CAUSAL FAIRNESS                                                 │
│  ├── No direct discrimination                                   │
│  └── No indirect discrimination via proxies                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Metric Selection Guide

| Metric | Use When | Limitation |
|--------|----------|------------|
| Demographic Parity | Equal outcomes needed | Ignores base rates |
| Equalized Odds | Equal error rates needed | Requires labels |
| Equal Opportunity | Focus on true positives | Ignores false positives |
| Predictive Parity | Equal precision needed | May conflict with others |
| Calibration | Probabilistic predictions | Hard to achieve with others |

### Impossibility Theorem

**Note:** It is mathematically impossible to satisfy all fairness metrics simultaneously when base rates differ across groups. Document trade-off decisions explicitly.

## Protected Attributes

### Common Protected Categories

| Category | Examples | Legal Framework |
|----------|----------|-----------------|
| Race/Ethnicity | Self-identified, inferred | Title VII, Civil Rights Act |
| Gender | Binary, non-binary, gender identity | Title VII, Equal Pay Act |
| Age | Date of birth, age ranges | ADEA |
| Disability | Physical, mental, cognitive | ADA |
| Religion | Affiliation, practices | Title VII |
| National Origin | Country, citizenship, ancestry | Title VII |
| Sexual Orientation | Preference, identity | Varies by jurisdiction |
| Socioeconomic Status | Income, education, zip code | Often proxy for race |

### Proxy Variable Detection

```csharp
public class ProxyDetector
{
    public async Task<ProxyAnalysis> DetectProxies(
        Dataset data,
        string protectedAttribute,
        CancellationToken ct)
    {
        var proxies = new List<ProxyVariable>();
        var features = data.GetNonProtectedFeatures();

        foreach (var feature in features)
        {
            // Calculate mutual information with protected attribute
            var mutualInfo = CalculateMutualInformation(
                data.GetColumn(feature),
                data.GetColumn(protectedAttribute));

            // Calculate correlation
            var correlation = CalculateCorrelation(
                data.GetColumn(feature),
                data.GetColumn(protectedAttribute));

            if (mutualInfo > 0.3 || Math.Abs(correlation) > 0.5)
            {
                proxies.Add(new ProxyVariable
                {
                    FeatureName = feature,
                    MutualInformation = mutualInfo,
                    Correlation = correlation,
                    RiskLevel = ClassifyRisk(mutualInfo, correlation)
                });
            }
        }

        return new ProxyAnalysis
        {
            ProtectedAttribute = protectedAttribute,
            DetectedProxies = proxies,
            Recommendations = GenerateRecommendations(proxies)
        };
    }

    private RiskLevel ClassifyRisk(double mi, double corr)
    {
        var maxSignal = Math.Max(mi, Math.Abs(corr));
        return maxSignal switch
        {
            > 0.7 => RiskLevel.High,
            > 0.5 => RiskLevel.Medium,
            _ => RiskLevel.Low
        };
    }
}
```

## Bias Measurement

### Disparate Impact Analysis

```csharp
public class FairnessEvaluator
{
    public FairnessReport Evaluate(
        IEnumerable<Prediction> predictions,
        string protectedAttribute)
    {
        var groups = predictions.GroupBy(p => p.GetAttribute(protectedAttribute));

        var metrics = new Dictionary<string, GroupMetrics>();

        foreach (var group in groups)
        {
            var groupPredictions = group.ToList();

            metrics[group.Key] = new GroupMetrics
            {
                Group = group.Key,
                Count = groupPredictions.Count,
                PositiveRate = groupPredictions.Count(p => p.Predicted == 1)
                    / (double)groupPredictions.Count,
                TruePositiveRate = CalculateTPR(groupPredictions),
                FalsePositiveRate = CalculateFPR(groupPredictions),
                Precision = CalculatePrecision(groupPredictions)
            };
        }

        return new FairnessReport
        {
            GroupMetrics = metrics,
            DemographicParity = CalculateDemographicParity(metrics),
            EqualizedOdds = CalculateEqualizedOdds(metrics),
            DisparateImpact = CalculateDisparateImpact(metrics),
            Recommendations = GenerateRecommendations(metrics)
        };
    }

    private double CalculateDisparateImpact(Dictionary<string, GroupMetrics> metrics)
    {
        var rates = metrics.Values.Select(m => m.PositiveRate).ToList();
        var minRate = rates.Min();
        var maxRate = rates.Max();

        // Disparate impact ratio (4/5ths rule: should be > 0.8)
        return minRate / maxRate;
    }

    private EqualizedOddsResult CalculateEqualizedOdds(
        Dictionary<string, GroupMetrics> metrics)
    {
        var tprValues = metrics.Values.Select(m => m.TruePositiveRate).ToList();
        var fprValues = metrics.Values.Select(m => m.FalsePositiveRate).ToList();

        return new EqualizedOddsResult
        {
            TprDisparity = tprValues.Max() - tprValues.Min(),
            FprDisparity = fprValues.Max() - fprValues.Min(),
            Satisfied = tprValues.Max() - tprValues.Min() < 0.1
                && fprValues.Max() - fprValues.Min() < 0.1
        };
    }
}
```

### LLM-Specific Bias Testing

```csharp
public class LlmBiasTester
{
    public async Task<LlmBiasReport> TestBias(
        ILlmClient llm,
        BiasTestSuite testSuite,
        CancellationToken ct)
    {
        var results = new List<BiasTestResult>();

        foreach (var testCase in testSuite.TestCases)
        {
            // Generate variations with different demographic references
            var variations = GenerateDemographicVariations(testCase);
            var responses = new Dictionary<string, string>();

            foreach (var (demographic, prompt) in variations)
            {
                var response = await llm.Complete(prompt, ct);
                responses[demographic] = response;
            }

            // Analyze response consistency
            var analysis = AnalyzeResponseVariation(responses, testCase.ExpectedConsistency);

            results.Add(new BiasTestResult
            {
                TestCase = testCase,
                Responses = responses,
                ConsistencyScore = analysis.ConsistencyScore,
                BiasIndicators = analysis.BiasIndicators,
                Passed = analysis.ConsistencyScore >= testCase.Threshold
            });
        }

        return new LlmBiasReport
        {
            TestResults = results,
            OverallScore = results.Average(r => r.ConsistencyScore),
            FailedTests = results.Where(r => !r.Passed).ToList(),
            Recommendations = GenerateRecommendations(results)
        };
    }

    private Dictionary<string, string> GenerateDemographicVariations(BiasTestCase testCase)
    {
        var variations = new Dictionary<string, string>();

        // Gender variations
        variations["male"] = testCase.Template.Replace("{person}", "John");
        variations["female"] = testCase.Template.Replace("{person}", "Sarah");

        // Race/ethnicity variations (when appropriate for test)
        if (testCase.TestDemographics.Contains("race"))
        {
            variations["name_a"] = testCase.Template.Replace("{person}", "James");
            variations["name_b"] = testCase.Template.Replace("{person}", "Jamal");
            variations["name_c"] = testCase.Template.Replace("{person}", "Jose");
        }

        return variations;
    }
}
```

## Bias Mitigation Strategies

### Mitigation Approaches

| Stage | Technique | Description |
|-------|-----------|-------------|
| **Pre-processing** | Reweighting | Adjust sample weights |
| | Resampling | Over/undersample groups |
| | Data augmentation | Add synthetic examples |
| | Feature transformation | Remove proxy signals |
| **In-processing** | Constrained optimization | Add fairness constraints |
| | Adversarial debiasing | Train discriminator |
| | Fair representations | Learn fair embeddings |
| **Post-processing** | Threshold adjustment | Group-specific thresholds |
| | Calibration | Equalize calibration |
| | Reject option | Abstain on uncertain cases |

### Implementation Example

```csharp
public class BiasAwarePipeline
{
    public async Task<DebiasedModel> TrainWithFairnessConstraints(
        Dataset data,
        string protectedAttribute,
        FairnessConstraint constraint,
        CancellationToken ct)
    {
        // Pre-processing: Reweight samples
        var weights = CalculateReweightingFactors(data, protectedAttribute);

        // Split data
        var (train, validation) = data.Split(0.8);

        // Train with fairness-aware loss
        var model = new FairnessAwareClassifier(constraint);

        var options = new TrainingOptions
        {
            SampleWeights = weights,
            FairnessLambda = 0.5,  // Trade-off parameter
            EarlyStoppingMetric = "fairness_adjusted_auc"
        };

        await model.Train(train, options, ct);

        // Post-processing: Adjust thresholds
        var thresholds = OptimizeGroupThresholds(
            model,
            validation,
            protectedAttribute,
            constraint);

        return new DebiasedModel
        {
            Model = model,
            GroupThresholds = thresholds,
            FairnessMetrics = EvaluateFairness(model, validation, protectedAttribute)
        };
    }

    private Dictionary<string, double> OptimizeGroupThresholds(
        IClassifier model,
        Dataset validation,
        string protectedAttribute,
        FairnessConstraint constraint)
    {
        var groups = validation.GetUniqueValues(protectedAttribute);
        var thresholds = new Dictionary<string, double>();

        // Grid search for thresholds that satisfy constraint
        foreach (var group in groups)
        {
            var groupData = validation.Filter(protectedAttribute, group);
            var bestThreshold = 0.5;
            var bestFairness = double.MaxValue;

            for (var t = 0.1; t <= 0.9; t += 0.05)
            {
                var fairnessGap = EvaluateFairnessGap(
                    model, validation, protectedAttribute, group, t, constraint);

                if (fairnessGap < bestFairness)
                {
                    bestFairness = fairnessGap;
                    bestThreshold = t;
                }
            }

            thresholds[group] = bestThreshold;
        }

        return thresholds;
    }
}
```

## Bias Assessment Template

```markdown
# Bias Assessment: [System Name]

## 1. Scope
- **Protected Attributes**: [List attributes assessed]
- **Fairness Metrics**: [Metrics used]
- **Threshold**: [Acceptable disparity level]

## 2. Data Analysis
### Dataset Demographics
| Group | Count | Percentage | Base Rate |
|-------|-------|------------|-----------|
| [Group A] | [N] | [%] | [Rate] |
| [Group B] | [N] | [%] | [Rate] |

### Proxy Analysis
| Feature | Correlation | Risk Level | Action |
|---------|-------------|------------|--------|
| [Feature] | [Corr] | [H/M/L] | [Action] |

## 3. Fairness Metrics

### Demographic Parity
| Group | Positive Rate | Gap from Reference |
|-------|---------------|-------------------|
| [Group A] | [Rate] | - (reference) |
| [Group B] | [Rate] | [Gap] |

**Disparate Impact Ratio**: [X.XX] (Target: > 0.8)

### Equalized Odds
| Group | TPR | FPR |
|-------|-----|-----|
| [Group A] | [Rate] | [Rate] |
| [Group B] | [Rate] | [Rate] |

**TPR Disparity**: [X.XX] | **FPR Disparity**: [X.XX]

## 4. Findings

### Identified Biases
| Bias | Severity | Evidence | Affected Group |
|------|----------|----------|----------------|
| [Bias 1] | [H/M/L] | [Evidence] | [Group] |

### Root Cause Analysis
[Analysis of why bias exists]

## 5. Mitigation Plan

| Bias | Mitigation Strategy | Expected Impact | Trade-off |
|------|---------------------|-----------------|-----------|
| [Bias 1] | [Strategy] | [Impact] | [Trade-off] |

## 6. Monitoring Plan
- [ ] Automated fairness monitoring
- [ ] Periodic reassessment schedule
- [ ] Drift detection for fairness metrics

## 7. Sign-off
- [ ] Data science review
- [ ] Legal/compliance review
- [ ] Ethics board review (if applicable)
```

## Validation Checklist

- [ ] Protected attributes identified
- [ ] Proxy variables analyzed
- [ ] Fairness metrics selected
- [ ] Baseline measurements taken
- [ ] Disparate impact calculated
- [ ] Equalized odds evaluated
- [ ] Bias root causes analyzed
- [ ] Mitigation strategies defined
- [ ] Trade-offs documented
- [ ] Monitoring plan established

## Integration Points

**Inputs from**:

- Data sources → Training data demographics
- Legal/compliance → Protected attribute requirements
- `ml-project-lifecycle` skill → Project constraints

**Outputs to**:

- `ai-safety-planning` skill → Fairness requirements
- `explainability-planning` skill → Bias explanations
- Documentation → Compliance evidence
