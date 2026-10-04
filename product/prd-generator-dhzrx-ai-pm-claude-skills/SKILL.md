---
name: prd-generator
description: Generate comprehensive Product Requirements Documents with AI PM best practices for new features and products
---

# PRD Generator

## Overview

The PRD Generator skill helps AI Product Managers create comprehensive, well-structured Product Requirements Documents (PRDs) that incorporate industry best practices, PM frameworks, and AI-specific considerations. It transforms high-level feature ideas into detailed specifications ready for engineering and stakeholder review.

## When to Use This Skill

- Starting a new feature or product initiative
- Need to document requirements for engineering team
- Preparing for stakeholder review or approval
- Creating specification for AI/ML features
- Transitioning from discovery to delivery phase
- Documenting complex features with multiple components

## PM Frameworks Applied

- **Jobs-to-be-Done (JTBD)**: Frames problem from user's perspective
- **SMART Goals**: Ensures success criteria are Specific, Measurable, Achievable, Relevant, Time-bound
- **RICE Prioritization**: Calculates expected impact (Reach × Impact / Effort)
- **User Story Format**: "As a... I want... So that..." structure
- **MoSCoW Method**: Categorizes requirements as Must/Should/Could/Won't have
- **RACI Matrix**: Defines stakeholder roles and responsibilities
- **AI Product Canvas**: Structured approach for AI feature requirements

## Inputs Required

```json
{
  "feature_name": "string",
  "problem_statement": "string",
  "target_users": "string or array",
  "business_goals": "array of strings",
  "user_research_summary": "string (optional)",
  "competitive_landscape": "string (optional)",
  "technical_constraints": "array of strings (optional)",
  "success_metrics": "array of objects (optional)",
  "ai_ml_requirements": {
    "model_type": "string (optional)",
    "data_requirements": "string (optional)",
    "performance_targets": "object (optional)"
  }
}
```

## Outputs Produced

A comprehensive PRD document in Markdown format containing:

1. **Executive Summary** - One-page overview
2. **Problem Statement** - JTBD-framed user problem
3. **Opportunity Sizing** - Market size and impact potential
4. **Success Metrics** - Quantifiable KPIs with targets
5. **User Stories** - Detailed scenarios with acceptance criteria
6. **Functional Requirements** - Must/Should/Could/Won't have features
7. **Technical Requirements** - Architecture, APIs, dependencies
8. **AI/ML Specifications** - Model requirements, data needs, bias mitigation
9. **User Experience** - Key flows and interactions
10. **Risk Assessment** - Potential issues and mitigations
11. **Launch Plan** - Phased rollout strategy
12. **Stakeholder Matrix** - RACI chart
13. **Appendix** - Research summary, competitive analysis

## Usage Instructions

### Basic Invocation

```
Create a PRD for [feature name] that solves [problem] for [user segment]
```

### Detailed Invocation

```
Generate a comprehensive PRD with the following details:
- Feature: AI-powered recommendation engine
- Problem: Users spend too much time searching for relevant products
- Target Users: E-commerce shoppers, focus on returning customers
- Business Goals: Increase conversion rate by 15%, improve average order value
- Include AI/ML requirements and ethical considerations
```

### With Structured Input

Provide JSON input matching the schema above for most detailed results.

## Best Practices

- **Start with the problem, not the solution** - Focus on user needs first
- **Be specific about success metrics** - Include baseline, target, and timeline
- **Document assumptions** - Make implicit knowledge explicit
- **Include alternatives considered** - Show why this approach was chosen
- **Address "why now?"** - Explain timing and urgency
- **Consider edge cases** - Don't just focus on happy path
- **Plan for failure** - Include rollback strategy
- **Quantify impact** - Use data wherever possible
- **Keep it living** - PRD should evolve as you learn

## Composition with Other Skills

### Recommended Workflow

1. **Before PRD Creation**:
   - `user-research-analyzer` → Extract insights from research
   - `competitive-analyzer` → Understand market positioning
   - `feature-prioritizer` → Validate this should be built now

2. **During PRD Creation**:
   - Use this skill (`prd-generator`) → Create initial PRD
   - `ai-ethics-assessor` → For AI features, evaluate ethical implications
   - `metrics-dashboard-builder` → Define measurement approach

3. **After PRD Creation**:
   - `user-story-generator` → Break down into development tickets
   - `stakeholder-communicator` → Generate alignment updates
   - `gtm-strategy-builder` → Plan launch approach

## Common Pitfalls to Avoid

- **Solution before problem** - Jumping to "how" before establishing "why"
- **Vague success metrics** - "Improve user satisfaction" vs. "Increase NPS from 45 to 60"
- **Skipping alternatives** - Not documenting why other approaches were rejected
- **Ignoring constraints** - Technical, resource, or timeline limitations
- **Missing dependencies** - Other teams, systems, or features required
- **Unclear scope** - What's in v1 vs. future versions
- **No rollback plan** - How to handle if feature underperforms
- **Stakeholder assumptions** - Not validating who needs to approve what

## AI/ML Specific Considerations

When generating PRDs for AI features, the skill ensures:

- **Model Performance Requirements**: Accuracy, latency, throughput targets
- **Data Requirements**: Training data size, quality, labeling needs
- **Bias & Fairness**: Evaluation criteria across user demographics
- **Explainability**: How users understand AI decisions
- **Monitoring**: Ongoing model performance tracking
- **Fallback Behavior**: What happens when model fails or is uncertain
- **Ethical Guidelines**: Privacy, transparency, accountability measures
- **Regulatory Compliance**: GDPR, AI Act, industry-specific regulations

## Python Functions

This skill uses the following Python functions:

### `generate_prd(input_data: dict) -> str`
Main function that orchestrates PRD generation.

**Parameters**:
- `input_data`: Dictionary containing feature requirements

**Returns**: Complete PRD in Markdown format

### `calculate_opportunity_size(reach: int, impact: float, market_size: float) -> dict`
Estimates market opportunity using TAM/SAM/SOM framework.

### `generate_success_metrics(business_goals: list, baseline_data: dict) -> list`
Creates SMART metrics with targets and measurement methods.

### `extract_user_stories(requirements: list, user_personas: list) -> list`
Converts functional requirements into user story format with acceptance criteria.

### `assess_risks(feature_scope: dict, technical_complexity: str) -> list`
Identifies potential risks and suggests mitigation strategies.

### `create_launch_phases(scope: dict, dependencies: list) -> dict`
Designs phased rollout plan based on scope and dependencies.

## Output Format Example

```markdown
# PRD: [Feature Name]

## Executive Summary
[One-page overview with problem, solution, impact, and ask]

## Problem Statement
**Job-to-be-Done**: When [situation], I want to [motivation], so I can [outcome].

**Current Experience**: [Pain points]

**Desired Experience**: [Vision]

## Opportunity Sizing
- **TAM** (Total Addressable Market): [size]
- **SAM** (Serviceable Addressable Market): [size]
- **SOM** (Serviceable Obtainable Market): [size]
- **Expected Impact**: [RICE calculation]

## Success Metrics
| Metric | Baseline | Target | Timeline | Measurement |
|--------|----------|--------|----------|-------------|
| [Metric 1] | [value] | [value] | [date] | [method] |

[... continues with all PRD sections]
```

## Related Documentation

- See `user-research-analyzer` for analyzing research before writing PRD
- See `feature-prioritizer` for validating feature should be built
- See `ai-ethics-assessor` for AI-specific ethical evaluation
- See `stakeholder-communicator` for sharing PRD with stakeholders

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Skill Type**: Generative (with Python)  
**Complexity**: Advanced
