---
name: multi-ai-orchestration
description: Use when stuck on complex problems, need architecture validation, want code review from multiple perspectives, or debugging hits a wall - guides leveraging multiple AI models in parallel for better results
---

# Multi-AI Orchestration

## When to Use

**Trigger conditions:**
- Stuck after 2+ failed attempts
- Architecture decisions with multiple valid approaches
- Code review before major commits
- Debugging with no clear root cause
- Need validation from different reasoning styles

## Quick Tools (Zero Setup)

| Tool | Models | Best For |
|------|--------|----------|
| [chat.lmstudio.ai](https://chat.lmstudio.ai) | Grok, Claude, Gemini, GPT-4o, Llama | Parallel responses in 10 seconds |
| [poe.com](https://poe.com) Multi-bot | 10+ models | Custom chains (Claude → Grok → Gemini) |
| ChatHub extension | All major models | One browser tab, one hotkey |

## Orchestration Patterns

### Pattern 1: Parallel Fan-Out (Fastest)

When you need multiple perspectives quickly:

```
User problem → [Claude, Grok, Gemini] → Compare answers → Pick best
```

**Use for:** Architecture decisions, debugging hypotheses, API design choices

### Pattern 2: Sequential Review Chain

When you need validation of work:

```
Claude writes code → Grok reviews → Gemini tests edge cases → Final version
```

**Use for:** Production code, critical bug fixes, security-sensitive changes

### Pattern 3: Specialist Routing

Route based on problem type:

| Problem Type | Best Model |
|--------------|------------|
| Complex reasoning | Claude, o1 |
| Code generation | Grok, Claude |
| Quick lookups/facts | Gemini, GPT-4o |
| Math/logic puzzles | o1, DeepSeek-R1 |
| Creative solutions | Claude, Grok |

### Pattern 4: Debate Protocol

When models disagree:

1. State the disagreement clearly
2. Ask each model to steelman the other's position
3. Ask for synthesis: "Given both perspectives, what's the best approach?"
4. Human decides based on combined insight

## Context Handoff Template

When passing context between models:

```markdown
## Context
[Brief problem description - 2-3 sentences]

## What's Been Tried
- Approach 1: [result]
- Approach 2: [result]

## Current Best Hypothesis
[What the previous model concluded]

## What I Need From You
[Specific ask: validate, find holes, alternative approach, etc.]
```

## Automation Options

**10-minute setup:**
- Poe.com custom multi-bot
- ChatHub browser extension

**30-minute setup (fully automatic):**
- LangGraph / CrewAI (Python)
- LazyLLM local orchestrator

**Example CrewAI flow:**
```python
crew = Crew(
    agents=[
        Agent("Planner", model="grok"),
        Agent("Coder", model="claude"),
        Agent("Reviewer", model="gemini"),
        Agent("Tester", model="gpt-4o")
    ],
    process="sequential"  # or "parallel"
)
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Copy-paste everything manually | Use multi-chat tools |
| Ask same question to all models | Specialize the ask per model |
| Ignore disagreements | Use debate protocol |
| Over-orchestrate simple problems | Single model is fine for routine tasks |

## When NOT to Use

- Simple, well-defined tasks
- Tasks one model handles confidently
- Time-sensitive with clear solution path
- Model-specific features (Claude artifacts, GPT DALL-E, etc.)

## Integration with Other Skills

- **systematic-debugging**: Fan out hypotheses to multiple models
- **react-architecture-enforcer**: Get extraction plan validation
- **brainstorming**: Parallel ideation across models
- **code-review**: Multi-model review before merge
