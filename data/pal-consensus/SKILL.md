---
name: pal-consensus
description: Multi-model consensus building through structured debate using PAL MCP. Use for complex decisions, architectural choices, technology evaluations, or when you need multiple perspectives. Triggers on requests for second opinions, debates, or consensus building.
---

# PAL Consensus - Multi-Model Debate

Build consensus through systematic analysis and structured debate across multiple AI models.

## When to Use

- Complex architectural decisions
- Technology selection
- Feature design trade-offs
- Risk assessment
- When you need multiple perspectives
- Validating important decisions

## Quick Start

```python
# Step 1: State the proposal and do your analysis
result = mcp__pal__consensus(
    step="Evaluate: Should we migrate from monolith to microservices?",
    step_number=1,
    total_steps=4,  # Your analysis + 2 models + synthesis
    next_step_required=True,
    findings="My initial analysis: Consider scale, team size, complexity...",
    models=[
        {"model": "openai/gpt-5", "stance": "for"},
        {"model": "deepseek/deepseek-v3.2", "stance": "against"}
    ]
)

# Step 2+: Process each model's response
result = mcp__pal__consensus(
    step="Recording pro-microservices perspective",
    step_number=2,
    total_steps=4,
    next_step_required=True,
    findings="GPT-5 argues: scalability benefits, team autonomy...",
    continuation_id=result["continuation_id"]
)
```

## Stance Types

| Stance | Description |
|--------|-------------|
| `for` | Advocate for the proposal |
| `against` | Argue against the proposal |
| `neutral` | Objective analysis without position |

## Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `step` | string | Proposal (step 1) or notes (step 2+) |
| `step_number` | int | Current step |
| `total_steps` | int | Models consulted + 2 (analysis + synthesis) |
| `next_step_required` | bool | More consultations needed? |
| `findings` | string | Your analysis or model response summary |

## Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `models` | list | Models to consult with stances |
| `current_model_index` | int | Next model to consult |
| `model_responses` | list | Internal log of responses |
| `relevant_files` | list | Supporting files |
| `continuation_id` | string | Continue session |

## Model Configuration

```python
models=[
    {
        "model": "openai/gpt-5",
        "stance": "for",
        "stance_prompt": "Focus on scalability and maintainability benefits"
    },
    {
        "model": "deepseek/deepseek-v3.2",
        "stance": "against",
        "stance_prompt": "Consider operational complexity and team capacity"
    },
    {
        "model": "google/gemini-3-flash-preview",
        "stance": "neutral"
    }
]
```

## Available Models

Top models for consensus (all score 100):
- `openai/gpt-5` - Strong reasoning
- `deepseek/deepseek-v3.2` - Thinking-enabled
- `google/gemini-3-flash-preview` - 1M context
- `x-ai/grok-4.1` - 2M context
- `bytedance-seed/seed-1.6` - Thinking-enabled

## Workflow Pattern

```
Step 1: State proposal + your independent analysis
        ↓
Step 2: First model responds (for/against/neutral)
        ↓
Step 3: Second model responds
        ↓
Step N: Synthesize all perspectives
```

## Example: Technology Decision

```python
# Debate: GraphQL vs REST
mcp__pal__consensus(
    step="Evaluate: Should we use GraphQL instead of REST for our new API?",
    step_number=1,
    total_steps=5,
    next_step_required=True,
    findings="""
    Initial analysis:
    - Current team: 5 backend devs, familiar with REST
    - Use case: Mobile app with varying data needs
    - Timeline: 3 months to launch
    - Consider: Learning curve, tooling, performance
    """,
    models=[
        {"model": "openai/gpt-5", "stance": "for"},
        {"model": "deepseek/deepseek-v3.2", "stance": "against"},
        {"model": "google/gemini-3-flash-preview", "stance": "neutral"}
    ],
    relevant_files=[
        "/docs/api-requirements.md",
        "/app/api/current_endpoints.py"
    ]
)
```

## Best Practices

1. **Frame proposals clearly** - Specific, evaluable statements
2. **Provide context** - Constraints, requirements, history
3. **Use diverse models** - Different strengths and perspectives
4. **Balance stances** - Include for, against, and neutral
5. **Document synthesis** - Capture key insights from all perspectives
