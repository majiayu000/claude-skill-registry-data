---
name: explainability-planning
description: Plan explainable AI (XAI) requirements including SHAP, LIME, attention visualization, and regulatory explainability needs.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Explainability Planning

## When to Use This Skill

Use this skill when:

- **Explainability Planning tasks** - Working on plan explainable ai (xai) requirements including shap, lime, attention visualization, and regulatory explainability needs
- **Planning or design** - Need guidance on Explainability Planning approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Explainability (XAI) is the ability to understand and communicate how AI systems make decisions. Explainability requirements vary by domain, stakeholder, and regulatory context. Effective planning balances explanation fidelity with usability.

## Explainability Framework

```text
┌─────────────────────────────────────────────────────────────────┐
│                   EXPLAINABILITY SPECTRUM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INHERENTLY INTERPRETABLE ◄─────────────────► BLACK BOX         │
│                                                                  │
│  Linear Models         Decision Trees      Neural Networks      │
│  Rule-Based            Random Forest       Deep Learning        │
│  Decision Tables       Gradient Boosting   Transformers         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    XAI TECHNIQUES                        │    │
│  │                                                          │    │
│  │  LOCAL (per prediction)     GLOBAL (model-wide)         │    │
│  │  ├── LIME                   ├── Feature importance      │    │
│  │  ├── SHAP values            ├── Partial dependence      │    │
│  │  ├── Attention weights      ├── SHAP summary plots      │    │
│  │  ├── Counterfactuals        ├── Global surrogates       │    │
│  │  └── Anchors                └── Concept explanations    │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Explainability Requirements by Domain

### Domain-Specific Requirements

| Domain | Explainability Need | Audience | Regulation |
|--------|---------------------|----------|------------|
| **Healthcare** | High - life/death decisions | Clinicians, patients | FDA, HIPAA |
| **Finance** | High - adverse action notice | Regulators, customers | ECOA, FCRA |
| **Legal** | High - due process | Judges, defendants | Varies by jurisdiction |
| **HR/Hiring** | High - discrimination risk | Candidates, auditors | Title VII, EEOC |
| **Insurance** | Medium-High | Underwriters, regulators | State insurance laws |
| **Marketing** | Low-Medium | Analysts | GDPR (right to explanation) |
| **Fraud Detection** | Medium | Investigators | Internal policy |

### GDPR Right to Explanation

The GDPR (Article 22) provides rights related to automated decision-making:

- Right to obtain human intervention
- Right to express point of view
- Right to contest the decision
- Right to meaningful information about logic involved

```csharp
public class GdprExplanation
{
    public string DecisionLogic { get; set; }         // High-level process description
    public string SignificantFactors { get; set; }   // Key features influencing decision
    public string ConsequencesEnvisaged { get; set; } // Expected outcomes
    public string ContestProcess { get; set; }       // How to challenge decision
}
```

## XAI Techniques

### SHAP (SHapley Additive exPlanations)

```csharp
public class ShapExplainer
{
    private readonly IModel _model;
    private readonly Dataset _backgroundData;

    public async Task<ShapExplanation> Explain(
        DataRow instance,
        CancellationToken ct)
    {
        // Calculate SHAP values using Kernel SHAP for model-agnostic explanation
        var shapValues = await CalculateKernelShap(instance, ct);

        return new ShapExplanation
        {
            Instance = instance,
            BaseValue = CalculateBaseValue(),
            ShapValues = shapValues,
            TopFeatures = GetTopFeatures(shapValues, 10),
            Visualization = GenerateWaterfallPlot(shapValues)
        };
    }

    public async Task<GlobalShapAnalysis> GlobalExplanation(
        Dataset testSet,
        CancellationToken ct)
    {
        var allShapValues = new List<Dictionary<string, double>>();

        foreach (var instance in testSet.Rows)
        {
            var shapValues = await CalculateKernelShap(instance, ct);
            allShapValues.Add(shapValues);
        }

        return new GlobalShapAnalysis
        {
            MeanAbsoluteShap = CalculateMeanAbsShap(allShapValues),
            FeatureImportanceRanking = RankFeatures(allShapValues),
            SummaryPlot = GenerateSummaryPlot(allShapValues),
            DependencePlots = GenerateDependencePlots(allShapValues, testSet)
        };
    }

    private async Task<Dictionary<string, double>> CalculateKernelShap(
        DataRow instance,
        CancellationToken ct)
    {
        var shapValues = new Dictionary<string, double>();
        var numSamples = 1000;

        foreach (var feature in instance.Features)
        {
            var coalitions = GenerateCoalitions(instance, feature, numSamples);
            var predictions = await _model.PredictBatch(coalitions, ct);

            // Calculate marginal contribution
            shapValues[feature.Name] = CalculateMarginalContribution(predictions);
        }

        return shapValues;
    }
}
```

### LIME (Local Interpretable Model-agnostic Explanations)

```csharp
public class LimeExplainer
{
    public async Task<LimeExplanation> Explain(
        DataRow instance,
        IModel model,
        int numSamples = 5000,
        CancellationToken ct = default)
    {
        // Generate perturbed samples around instance
        var perturbedData = GeneratePerturbations(instance, numSamples);

        // Get model predictions for perturbed samples
        var predictions = await model.PredictBatch(perturbedData, ct);

        // Calculate distances/weights
        var weights = CalculateKernelWeights(instance, perturbedData);

        // Fit interpretable model (linear regression)
        var localModel = FitWeightedLinearModel(
            perturbedData,
            predictions,
            weights);

        return new LimeExplanation
        {
            Instance = instance,
            LocalModel = localModel,
            FeatureWeights = localModel.Coefficients,
            Intercept = localModel.Intercept,
            R2Score = localModel.R2Score,
            TopPositive = GetTopPositiveFeatures(localModel, 5),
            TopNegative = GetTopNegativeFeatures(localModel, 5)
        };
    }

    private double[] CalculateKernelWeights(DataRow original, Dataset perturbed)
    {
        // Exponential kernel based on distance
        return perturbed.Rows
            .Select(row => Math.Exp(-CalculateDistance(original, row) / _kernelWidth))
            .ToArray();
    }
}
```

### LLM-Specific Explanations

```csharp
public class LlmExplainer
{
    public async Task<LlmExplanation> ExplainCompletion(
        string prompt,
        string completion,
        ILlmClient llm,
        CancellationToken ct)
    {
        // Self-explanation via chain-of-thought
        var cotExplanation = await llm.Complete(
            $"""
            Original prompt: {prompt}
            Your response: {completion}

            Please explain your reasoning for this response:
            1. What key information in the prompt influenced your response?
            2. What assumptions did you make?
            3. What alternative responses did you consider?
            4. Why did you choose this particular response?
            """,
            ct);

        // Token-level attribution (if available)
        var tokenAttribution = await GetTokenAttribution(prompt, completion, ct);

        return new LlmExplanation
        {
            Prompt = prompt,
            Completion = completion,
            ChainOfThought = cotExplanation,
            TokenAttribution = tokenAttribution,
            KeyFactors = ExtractKeyFactors(cotExplanation)
        };
    }

    public async Task<AttentionExplanation> ExplainAttention(
        string prompt,
        string completion,
        CancellationToken ct)
    {
        // Get attention weights from model (requires access to internals)
        var attentionWeights = await GetAttentionWeights(prompt, completion, ct);

        return new AttentionExplanation
        {
            Prompt = prompt,
            Completion = completion,
            AttentionMatrix = attentionWeights,
            HighAttentionTokens = GetHighAttentionTokens(attentionWeights),
            AttentionVisualization = GenerateAttentionHeatmap(attentionWeights)
        };
    }
}
```

## Counterfactual Explanations

### Generating Counterfactuals

```csharp
public class CounterfactualExplainer
{
    public async Task<CounterfactualExplanation> GenerateCounterfactual(
        DataRow instance,
        IModel model,
        int desiredClass,
        CancellationToken ct)
    {
        var currentPrediction = await model.Predict(instance, ct);

        if (currentPrediction.Class == desiredClass)
        {
            return CounterfactualExplanation.AlreadyDesiredClass();
        }

        // Find minimal changes to flip prediction
        var counterfactual = await FindMinimalCounterfactual(
            instance,
            model,
            desiredClass,
            ct);

        return new CounterfactualExplanation
        {
            Original = instance,
            Counterfactual = counterfactual,
            OriginalPrediction = currentPrediction,
            CounterfactualPrediction = await model.Predict(counterfactual, ct),
            Changes = CalculateChanges(instance, counterfactual),
            NaturalLanguage = GenerateExplanation(instance, counterfactual)
        };
    }

    private string GenerateExplanation(DataRow original, DataRow counterfactual)
    {
        var changes = CalculateChanges(original, counterfactual);
        var sb = new StringBuilder("To change the outcome, the following changes would be needed:\n");

        foreach (var change in changes)
        {
            sb.AppendLine($"- {change.Feature}: change from {change.OriginalValue} to {change.NewValue}");
        }

        return sb.ToString();
    }
}
```

## Explanation Presentation

### Audience-Appropriate Explanations

| Audience | Explanation Style | Content |
|----------|-------------------|---------|
| **Technical** | Detailed, quantitative | SHAP values, feature importance |
| **Business** | High-level, actionable | Key drivers, recommendations |
| **End User** | Simple, natural language | "Because X, Y, Z..." |
| **Regulator** | Complete, auditable | Full methodology, validation |

### Explanation Templates

```csharp
public class ExplanationGenerator
{
    public string GenerateUserExplanation(
        Prediction prediction,
        ShapExplanation shap)
    {
        var topFactors = shap.TopFeatures.Take(3).ToList();

        var template = prediction.IsPositive
            ? "Your application was approved primarily because: {factors}"
            : "Your application was not approved. The main factors were: {factors}";

        var factorList = string.Join(", ", topFactors.Select(FormatFactor));

        return template.Replace("{factors}", factorList);
    }

    public string GenerateTechnicalExplanation(
        Prediction prediction,
        ShapExplanation shap)
    {
        var sb = new StringBuilder();
        sb.AppendLine($"Prediction: {prediction.Class} (probability: {prediction.Probability:F3})");
        sb.AppendLine($"Base value: {shap.BaseValue:F3}");
        sb.AppendLine("Feature contributions:");

        foreach (var (feature, value) in shap.ShapValues.OrderByDescending(x => Math.Abs(x.Value)))
        {
            var direction = value > 0 ? "+" : "";
            sb.AppendLine($"  {feature}: {direction}{value:F4}");
        }

        return sb.ToString();
    }

    public AdverseActionNotice GenerateAdverseActionNotice(
        Prediction prediction,
        ShapExplanation shap)
    {
        // For credit decisions - FCRA/ECOA compliance
        var topNegativeFactors = shap.ShapValues
            .Where(kv => kv.Value < 0)
            .OrderBy(kv => kv.Value)
            .Take(4)  // Up to 4 principal reasons required
            .Select(kv => MapToReason(kv.Key))
            .ToList();

        return new AdverseActionNotice
        {
            Decision = "Application Denied",
            PrincipalReasons = topNegativeFactors,
            CreditBureauInfo = GetCreditBureauInfo(),
            DisputeProcess = GetDisputeInstructions()
        };
    }
}
```

## Explainability Requirements Template

```markdown
# Explainability Requirements: [System Name]

## 1. System Overview
- **Model Type**: [Type]
- **Decision Domain**: [Domain]
- **Risk Level**: [High/Medium/Low]

## 2. Regulatory Requirements
| Regulation | Requirement | Applicability |
|------------|-------------|---------------|
| [Reg 1] | [Requirement] | [Yes/No/Partial] |

## 3. Stakeholder Needs
| Stakeholder | Explanation Need | Format |
|-------------|-----------------|--------|
| [Stakeholder 1] | [Need] | [Format] |

## 4. Explainability Approach

### Model Selection
- [ ] Considered inherently interpretable models
- [ ] Justified use of black-box model (if applicable)

### Explanation Techniques
| Technique | Purpose | Implementation |
|-----------|---------|----------------|
| [SHAP] | [Feature importance] | [Library/approach] |
| [LIME] | [Local explanations] | [Library/approach] |

### Explanation Delivery
| Audience | Delivery Method | Frequency |
|----------|-----------------|-----------|
| [Audience 1] | [Method] | [Frequency] |

## 5. Validation
- [ ] Explanation faithfulness tested
- [ ] User comprehension validated
- [ ] Regulatory review completed

## 6. Monitoring
- [ ] Explanation quality metrics defined
- [ ] Drift detection for explanations
- [ ] Periodic review scheduled
```

## Validation Checklist

- [ ] Regulatory requirements identified
- [ ] Stakeholder explanation needs documented
- [ ] Explanation techniques selected
- [ ] Model interpretability assessed
- [ ] Local explanations implemented
- [ ] Global explanations available
- [ ] Counterfactuals considered
- [ ] Audience-appropriate formats created
- [ ] Explanation fidelity validated
- [ ] Documentation complete

## Integration Points

**Inputs from**:

- Regulatory requirements → Explanation mandates
- `ai-safety-planning` skill → Transparency requirements
- `bias-assessment` skill → Fairness explanations

**Outputs to**:

- `hitl-design` skill → Explanation in review UI
- User interface → End-user explanations
- Compliance documentation → Audit evidence
