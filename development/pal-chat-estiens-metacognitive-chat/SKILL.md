---
name: pal-chat
description: Collaborative thinking partner for brainstorming, development discussion, and exploring ideas using PAL MCP. Use when you need a second opinion, want to brainstorm, or need help thinking through a problem. Triggers on brainstorming requests, discussion needs, or when exploring ideas.
---

# PAL Chat - Collaborative Thinking

General-purpose collaboration for brainstorming, discussion, and exploring ideas.

## When to Use

- Brainstorming solutions
- Getting a second opinion
- Discussing trade-offs
- Exploring ideas
- Validating approaches
- Rubber duck debugging

## Quick Start

```python
result = mcp__pal__chat(
    prompt="I'm designing a rate limiting system. What approaches should I consider?",
    working_directory_absolute_path="/path/to/project"
)
```

## Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | Your question or idea |
| `working_directory_absolute_path` | string | Project directory |

## Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `absolute_file_paths` | list | Files to share for context |
| `model` | string | Override model (default: openai/gpt-5) |
| `temperature` | float | 0 = deterministic, 1 = creative |
| `thinking_mode` | enum | minimal/low/medium/high/max |
| `continuation_id` | string | Continue conversation |
| `images` | list | Image paths for visual context |

## Example Uses

### Brainstorming

```python
mcp__pal__chat(
    prompt="""
    I need to design a notification system that:
    - Supports email, SMS, push notifications
    - Handles user preferences
    - Allows batching to prevent spam
    - Scales to 1M users

    What architecture would you recommend?
    """,
    working_directory_absolute_path="/app"
)
```

### Code Discussion

```python
mcp__pal__chat(
    prompt="""
    I'm trying to decide between these approaches for the payment processor:

    Option A: Strategy pattern with separate classes per provider
    Option B: Single class with provider-specific methods

    What are the trade-offs? Which would you recommend?
    """,
    working_directory_absolute_path="/app",
    absolute_file_paths=[
        "/app/payments/processor.py",
        "/app/payments/stripe.py",
        "/app/payments/paypal.py"
    ]
)
```

### Validating Approach

```python
mcp__pal__chat(
    prompt="""
    I'm planning to implement caching like this:

    1. Check Redis for cached result
    2. If miss, query database
    3. Store in Redis with 5 min TTL
    4. Invalidate on writes

    Am I missing anything? Any edge cases to consider?
    """,
    working_directory_absolute_path="/app",
    thinking_mode="high"
)
```

### Multi-turn Discussion

```python
# Start conversation
result = mcp__pal__chat(
    prompt="Let's discuss microservices vs monolith for our startup",
    working_directory_absolute_path="/app"
)

# Continue with context
result = mcp__pal__chat(
    prompt="Good points. What about the team size factor? We have 4 developers.",
    working_directory_absolute_path="/app",
    continuation_id=result["continuation_id"]
)
```

## Temperature Guide

| Value | Use Case |
|-------|----------|
| 0.0 | Technical analysis, debugging |
| 0.3 | General discussion (default) |
| 0.7 | Creative brainstorming |
| 1.0 | Blue sky thinking |

## Thinking Modes

| Mode | Description |
|------|-------------|
| `minimal` | Quick responses |
| `low` | Light reasoning |
| `medium` | Balanced (default) |
| `high` | Deep analysis |
| `max` | Maximum reasoning |

## Available Models

Top models for chat:
- `openai/gpt-5` - Strong reasoning (default)
- `deepseek/deepseek-v3.2` - Thinking-enabled
- `google/gemini-3-flash-preview` - Fast, 1M context
- `x-ai/grok-4.1` - 2M context

## Best Practices

1. **Provide context** - Share relevant files
2. **Be specific** - Clear questions get better answers
3. **Use continuation_id** - Maintain conversation flow
4. **Adjust thinking_mode** - Match complexity to problem
5. **Include constraints** - Timeline, team size, tech stack
