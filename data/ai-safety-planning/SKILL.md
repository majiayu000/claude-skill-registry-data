---
name: ai-safety-planning
description: Plan AI safety measures including alignment, guardrails, red teaming, and regulatory compliance (EU AI Act, NIST AI RMF).
allowed-tools: Read, Write, Glob, Grep, Task
---

# AI Safety Planning

## When to Use This Skill

Use this skill when:

- **Ai Safety Planning tasks** - Working on plan ai safety measures including alignment, guardrails, red teaming, and regulatory compliance (eu ai act, nist ai rmf)
- **Planning or design** - Need guidance on Ai Safety Planning approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

AI safety encompasses the practices, techniques, and governance structures needed to ensure AI systems behave as intended, avoid harm, and comply with regulations. Effective safety planning must be integrated from project inception, not bolted on afterward.

## AI Safety Framework

```text
┌─────────────────────────────────────────────────────────────────┐
│                     AI SAFETY FRAMEWORK                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    GOVERNANCE LAYER                      │    │
│  │  Risk Classification │ Policies │ Compliance │ Auditing  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    TECHNICAL LAYER                       │    │
│  │  Input Guards │ Output Filters │ Model Alignment │ Monitoring│
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    OPERATIONAL LAYER                     │    │
│  │  Red Teaming │ Incident Response │ Continuous Testing   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## EU AI Act Risk Classification

### Risk Categories

| Risk Level | Description | Requirements | Examples |
|------------|-------------|--------------|----------|
| **Unacceptable** | Banned uses | Prohibited | Social scoring, subliminal manipulation |
| **High-Risk** | Significant impact | Full compliance | HR screening, credit scoring, medical |
| **Limited Risk** | Transparency needed | Disclosure | Chatbots, emotion recognition |
| **Minimal Risk** | Low concern | Best practices | Spam filters, games |

### High-Risk System Requirements

| Requirement | Description |
|-------------|-------------|
| Risk Management | Continuous risk assessment and mitigation |
| Data Governance | Training data quality, bias testing |
| Documentation | Technical documentation, logging |
| Transparency | Clear disclosure to users |
| Human Oversight | Meaningful human control |
| Accuracy/Robustness | Performance standards, testing |
| Cybersecurity | Security by design |

### Classification Decision Tree

```csharp
public class AiActClassifier
{
    public RiskClassification Classify(AiSystemProfile profile)
    {
        // Check for prohibited uses
        if (IsProhibitedUse(profile))
            return RiskClassification.Unacceptable;

        // Check Annex III high-risk categories
        if (IsHighRiskCategory(profile))
            return RiskClassification.HighRisk;

        // Check for transparency obligations
        if (RequiresTransparency(profile))
            return RiskClassification.LimitedRisk;

        return RiskClassification.MinimalRisk;
    }

    private bool IsHighRiskCategory(AiSystemProfile profile)
    {
        var highRiskAreas = new[]
        {
            "biometric_identification",
            "critical_infrastructure",
            "education_vocational",
            "employment_hr",
            "essential_services",
            "law_enforcement",
            "migration_asylum",
            "justice_democracy"
        };

        return highRiskAreas.Contains(profile.ApplicationArea);
    }

    private bool RequiresTransparency(AiSystemProfile profile)
    {
        return profile.InteractsWithHumans
            || profile.GeneratesContent
            || profile.DetectsEmotions
            || profile.UsesDeepfakes;
    }
}
```

## NIST AI RMF Alignment

### AI RMF Core Functions

| Function | Description | Key Activities |
|----------|-------------|----------------|
| **Govern** | Culture of risk management | Policies, accountability, oversight |
| **Map** | Context and risk identification | Stakeholders, impacts, constraints |
| **Measure** | Risk assessment | Metrics, testing, monitoring |
| **Manage** | Risk treatment | Mitigations, responses, priorities |

### Risk Mapping Template

```markdown
## AI Risk Map: [System Name]

### Stakeholder Analysis
| Stakeholder | Interest | Potential Harm | Severity |
|-------------|----------|----------------|----------|
| [Group 1] | [Interest] | [Harm] | [H/M/L] |
| [Group 2] | [Interest] | [Harm] | [H/M/L] |

### Risk Categories
- **Reliability**: [Assessment]
- **Safety**: [Assessment]
- **Security**: [Assessment]
- **Accountability**: [Assessment]
- **Transparency**: [Assessment]
- **Explainability**: [Assessment]
- **Privacy**: [Assessment]
- **Fairness**: [Assessment]

### Identified Risks
| Risk ID | Description | Likelihood | Impact | Mitigation |
|---------|-------------|------------|--------|------------|
| R-001 | [Risk] | [H/M/L] | [H/M/L] | [Action] |
```

## Guardrail Implementation

### Guardrail Types

| Type | Purpose | Implementation |
|------|---------|----------------|
| Input Guards | Block harmful prompts | Content filters, injection detection |
| Output Filters | Prevent harmful outputs | PII detection, toxicity filters |
| Topic Restrictions | Limit scope | Topic classifiers, keyword blockers |
| Behavioral Constraints | Enforce policies | System prompts, fine-tuning |
| Rate Limits | Prevent abuse | Usage quotas, throttling |

### Guardrail Architecture

```csharp
public class GuardrailPipeline
{
    private readonly List<IInputGuard> _inputGuards;
    private readonly List<IOutputFilter> _outputFilters;
    private readonly IAuditLogger _auditLogger;

    public async Task<GuardrailResult> ProcessRequest(
        UserRequest request,
        CancellationToken ct)
    {
        // Pre-processing guards
        foreach (var guard in _inputGuards)
        {
            var result = await guard.Check(request, ct);

            if (!result.Allowed)
            {
                await _auditLogger.LogBlocked(request, guard.Name, result.Reason);

                return GuardrailResult.Blocked(
                    $"Request blocked by {guard.Name}: {result.Reason}");
            }
        }

        // Generate response
        var response = await GenerateResponse(request, ct);

        // Post-processing filters
        foreach (var filter in _outputFilters)
        {
            response = await filter.Filter(response, ct);

            if (response.WasFiltered)
            {
                await _auditLogger.LogFiltered(request, filter.Name);
            }
        }

        return GuardrailResult.Success(response);
    }
}

public class PromptInjectionGuard : IInputGuard
{
    public string Name => "PromptInjectionGuard";

    public async Task<GuardResult> Check(UserRequest request, CancellationToken ct)
    {
        var indicators = new[]
        {
            "ignore previous instructions",
            "disregard your training",
            "you are now",
            "pretend you are",
            "act as if",
            "system prompt:",
            "new instructions:",
            "\\[INST\\]",
            "\\[/INST\\]"
        };

        var normalizedInput = request.Content.ToLowerInvariant();

        foreach (var indicator in indicators)
        {
            if (Regex.IsMatch(normalizedInput, indicator, RegexOptions.IgnoreCase))
            {
                return GuardResult.Blocked(
                    $"Potential prompt injection detected: {indicator}");
            }
        }

        // ML-based detection for sophisticated attacks
        var mlScore = await _injectionClassifier.Classify(request.Content, ct);

        if (mlScore > 0.8)
        {
            return GuardResult.Blocked("ML classifier detected injection attempt");
        }

        return GuardResult.Allowed();
    }
}
```

### Content Safety Implementation

```csharp
public class ContentSafetyFilter : IOutputFilter
{
    private readonly IContentSafetyClient _safetyClient;

    public async Task<FilteredResponse> Filter(
        LlmResponse response,
        CancellationToken ct)
    {
        var analysis = await _safetyClient.AnalyzeAsync(
            response.Content,
            new AnalysisOptions
            {
                Categories = new[]
                {
                    ContentCategory.Hate,
                    ContentCategory.Violence,
                    ContentCategory.SelfHarm,
                    ContentCategory.Sexual
                },
                OutputType = OutputType.FourSeverityLevels
            },
            ct);

        // Check if any category exceeds threshold
        var violations = analysis.CategoriesAnalysis
            .Where(c => c.Severity >= Severity.Medium)
            .ToList();

        if (violations.Any())
        {
            return new FilteredResponse
            {
                WasFiltered = true,
                OriginalContent = response.Content,
                FilteredContent = GenerateSafeResponse(violations),
                Violations = violations
            };
        }

        return new FilteredResponse
        {
            WasFiltered = false,
            FilteredContent = response.Content
        };
    }
}
```

## Red Teaming Strategy

### Red Team Objectives

| Objective | Description | Techniques |
|-----------|-------------|------------|
| Jailbreaking | Bypass safety controls | Prompt manipulation, roleplay |
| Data Extraction | Leak training data | Completion attacks, memorization |
| Bias Exploitation | Trigger unfair outputs | Targeted demographic testing |
| Harmful Content | Generate prohibited content | Edge cases, adversarial inputs |
| Denial of Service | Degrade performance | Resource exhaustion, loops |

### Red Team Test Categories

```markdown
## Red Team Test Plan: [System Name]

### Test Categories

#### 1. Prompt Injection
- [ ] Direct injection attempts
- [ ] Indirect injection (via user content)
- [ ] Multi-turn manipulation
- [ ] Encoding tricks (base64, unicode)

#### 2. Jailbreak Attempts
- [ ] Roleplay scenarios ("pretend you are...")
- [ ] Hypothetical framing
- [ ] Translation tricks
- [ ] System prompt extraction

#### 3. Harmful Content Generation
- [ ] Violence and weapons
- [ ] Self-harm content
- [ ] Hate speech and discrimination
- [ ] Illegal activities

#### 4. Privacy Attacks
- [ ] PII extraction attempts
- [ ] Training data extraction
- [ ] Membership inference

#### 5. Bias Testing
- [ ] Demographic disparities
- [ ] Stereotype reinforcement
- [ ] Cultural bias

### Severity Classification
| Severity | Description | Response Time |
|----------|-------------|---------------|
| Critical | System compromised, severe harm | Immediate |
| High | Safety bypass, harmful output | 24 hours |
| Medium | Partial bypass, concerning output | 1 week |
| Low | Minor issues, edge cases | Next release |
```

### Automated Red Teaming

```csharp
public class AutomatedRedTeam
{
    private readonly List<IAttackGenerator> _attackGenerators;
    private readonly ITargetSystem _target;

    public async Task<RedTeamReport> Execute(
        RedTeamConfig config,
        CancellationToken ct)
    {
        var results = new List<AttackResult>();

        foreach (var generator in _attackGenerators)
        {
            var attacks = await generator.GenerateAttacks(config, ct);

            foreach (var attack in attacks)
            {
                var response = await _target.Query(attack.Prompt, ct);

                var success = await EvaluateAttackSuccess(
                    attack,
                    response,
                    ct);

                results.Add(new AttackResult
                {
                    Attack = attack,
                    Response = response,
                    Success = success,
                    Category = attack.Category
                });

                if (success)
                {
                    await LogVulnerability(attack, response);
                }
            }
        }

        return new RedTeamReport
        {
            TotalAttacks = results.Count,
            SuccessfulAttacks = results.Count(r => r.Success),
            ByCategory = results.GroupBy(r => r.Category)
                .ToDictionary(g => g.Key, g => g.Count(r => r.Success)),
            CriticalFindings = results.Where(r => r.Success && r.Attack.Severity == Severity.Critical)
        };
    }
}
```

## Safety Evaluation Metrics

### Metric Categories

| Category | Metrics | Target |
|----------|---------|--------|
| Refusal Rate | % harmful requests refused | > 99% |
| False Positive Rate | % benign requests refused | < 5% |
| Jailbreak Resistance | % jailbreak attempts blocked | > 95% |
| Toxicity Score | Average output toxicity | < 0.1 |
| Bias Score | Demographic parity | > 0.9 |

### Continuous Monitoring

```csharp
public class SafetyMonitor
{
    public async Task RecordInteraction(
        Interaction interaction,
        CancellationToken ct)
    {
        // Analyze response safety
        var safetyScore = await _safetyClassifier.Score(
            interaction.Response,
            ct);

        // Log metrics
        await _metrics.RecordAsync(new SafetyMetrics
        {
            Timestamp = DateTime.UtcNow,
            SafetyScore = safetyScore,
            WasRefused = interaction.WasRefused,
            Category = interaction.Category,
            Latency = interaction.Latency
        });

        // Alert on concerning patterns
        if (safetyScore < _thresholds.CriticalSafetyScore)
        {
            await _alerting.SendAlert(new SafetyAlert
            {
                Severity = AlertSeverity.Critical,
                Interaction = interaction,
                Score = safetyScore
            });
        }

        // Check for pattern-based attacks
        await DetectAttackPatterns(interaction, ct);
    }
}
```

## Safety Planning Template

```markdown
# AI Safety Plan: [Project Name]

## 1. Risk Classification
- **EU AI Act Category**: [Unacceptable/High/Limited/Minimal]
- **NIST AI RMF Profile**: [Reference]
- **Internal Risk Score**: [1-5]

## 2. Identified Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | [H/M/L] | [H/M/L] | [Strategy] |

## 3. Guardrails
### Input Guards
- [ ] Prompt injection detection
- [ ] Content filtering
- [ ] Rate limiting

### Output Filters
- [ ] Toxicity filtering
- [ ] PII detection
- [ ] Topic restrictions

## 4. Testing Plan
- [ ] Pre-launch red teaming
- [ ] Continuous adversarial testing
- [ ] Bias evaluation

## 5. Monitoring
- [ ] Safety metrics dashboard
- [ ] Alerting thresholds
- [ ] Incident response plan

## 6. Compliance
- [ ] Documentation complete
- [ ] Human oversight defined
- [ ] Audit trail configured
```

## Validation Checklist

- [ ] Risk classification completed
- [ ] Regulatory requirements identified
- [ ] Guardrail architecture designed
- [ ] Input guards implemented
- [ ] Output filters configured
- [ ] Red team plan created
- [ ] Safety metrics defined
- [ ] Monitoring configured
- [ ] Incident response planned
- [ ] Compliance documentation complete

## Integration Points

**Inputs from**:

- Business requirements → Use case definition
- `bias-assessment` skill → Fairness requirements
- Legal/compliance → Regulatory requirements

**Outputs to**:

- `explainability-planning` skill → Transparency requirements
- `hitl-design` skill → Human oversight design
- Application code → Guardrail implementation
