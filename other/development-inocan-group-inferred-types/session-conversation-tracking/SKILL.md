---
name: session-conversation-tracking
description: Instrument sessions, conversations, and multi-turn interactions
triggers:
  - "session tracking"
  - "conversation instrumentation"
  - "multi-turn tracing"
  - "user session"
  - "chat history"
priority: 2
---

# Session and Conversation Tracking

Instrument sessions and conversations to understand multi-turn agent interactions.

## Core Principle

Session observability answers:
1. **Who is the user** (anonymized)?
2. **What's the conversation** context?
3. **How long** are sessions?
4. **What patterns** lead to success/failure?
5. **Where do users** drop off?

## Hierarchy

```
User (persistent)
└── Session (single sitting)
    └── Conversation (topic/thread)
        └── Turn (single exchange)
            └── Agent Run
                ├── LLM Call
                └── Tool Call
```

## Session Span Attributes

```python
# Session identity (P0)
span.set_attribute("session.id", str(uuid4()))
span.set_attribute("session.start_time", datetime.utcnow().isoformat())
span.set_attribute("session.type", "chat")  # chat, api, batch

# User context (P1 - anonymized)
span.set_attribute("user.id", hash_user_id(user_id))
span.set_attribute("user.tier", "premium")  # Safe to log
span.set_attribute("user.org_id", "org_123")

# Session metadata (P1)
span.set_attribute("session.channel", "web")  # web, mobile, api, slack
span.set_attribute("session.client_version", "2.1.0")
span.set_attribute("session.locale", "en-US")
```

## Conversation Span Attributes

```python
# Conversation identity (P0)
span.set_attribute("conversation.id", str(uuid4()))
span.set_attribute("conversation.session_id", session_id)
span.set_attribute("conversation.topic", "document_analysis")

# Turn tracking (P0)
span.set_attribute("conversation.turn_number", 5)
span.set_attribute("conversation.total_turns", 12)

# Context (P1)
span.set_attribute("conversation.messages_in_context", 10)
span.set_attribute("conversation.context_tokens", 4500)
span.set_attribute("conversation.context_window_pct", 0.15)
```

## Turn Span Attributes

```python
# Turn identity (P0)
span.set_attribute("turn.id", str(uuid4()))
span.set_attribute("turn.number", 5)
span.set_attribute("turn.role", "user")  # user, assistant

# User input (P1 - safe metadata only)
span.set_attribute("turn.input_length", 150)
span.set_attribute("turn.input_type", "question")  # question, command, feedback
span.set_attribute("turn.has_attachments", False)

# Assistant response (P1 - safe metadata only)
span.set_attribute("turn.output_length", 500)
span.set_attribute("turn.output_type", "answer")
span.set_attribute("turn.agent_runs", 1)
span.set_attribute("turn.tool_calls", 2)
span.set_attribute("turn.latency_ms", 2500)
```

## Session Lifecycle

### Session Start
```python
@observe(name="session.start")
def start_session(user_id: str, channel: str) -> str:
    session_id = str(uuid4())
    span = get_current_span()

    span.set_attribute("session.id", session_id)
    span.set_attribute("user.id", hash_user_id(user_id))
    span.set_attribute("session.channel", channel)
    span.set_attribute("session.start_time", datetime.utcnow().isoformat())

    return session_id
```

### Session End
```python
@observe(name="session.end")
def end_session(session_id: str, reason: str = "user_exit"):
    span = get_current_span()

    span.set_attribute("session.id", session_id)
    span.set_attribute("session.end_reason", reason)
    span.set_attribute("session.end_time", datetime.utcnow().isoformat())

    # Aggregate session metrics
    metrics = calculate_session_metrics(session_id)
    span.set_attribute("session.duration_ms", metrics["duration_ms"])
    span.set_attribute("session.total_turns", metrics["turns"])
    span.set_attribute("session.total_tokens", metrics["tokens"])
    span.set_attribute("session.total_cost_usd", metrics["cost"])
```

## Context Window Management

Track context usage across turns:
```python
@observe(name="conversation.manage_context")
def manage_context(conversation_id: str, new_message: str):
    span = get_current_span()

    # Current context state
    current_tokens = count_tokens(get_history(conversation_id))
    new_tokens = count_tokens(new_message)

    span.set_attribute("context.current_tokens", current_tokens)
    span.set_attribute("context.new_tokens", new_tokens)
    span.set_attribute("context.limit", MODEL_CONTEXT_LIMIT)

    # Check if pruning needed
    if current_tokens + new_tokens > MODEL_CONTEXT_LIMIT * 0.8:
        pruned = prune_context(conversation_id)
        span.set_attribute("context.pruned", True)
        span.set_attribute("context.messages_pruned", pruned)
    else:
        span.set_attribute("context.pruned", False)
```

## User Journey Tracking

Track user progression through workflows:
```python
# Journey stage tracking
span.set_attribute("journey.name", "onboarding")
span.set_attribute("journey.stage", "setup_complete")
span.set_attribute("journey.stage_number", 3)
span.set_attribute("journey.total_stages", 5)
span.set_attribute("journey.time_in_stage_ms", 45000)

# Conversion tracking
span.set_attribute("journey.converted", True)
span.set_attribute("journey.conversion_turn", 8)
span.set_attribute("journey.conversion_time_ms", 180000)
```

## Drop-off Tracking

Identify where users abandon:
```python
# Session end analysis
span.set_attribute("dropoff.detected", True)
span.set_attribute("dropoff.last_turn", 5)
span.set_attribute("dropoff.last_intent", "clarification_needed")
span.set_attribute("dropoff.agent_last_action", "asked_question")
span.set_attribute("dropoff.time_since_last_turn_ms", 300000)

# Inactivity detection
span.set_attribute("session.inactive_timeout", True)
span.set_attribute("session.idle_time_ms", 600000)
```

## Framework Integration

### Langfuse Sessions
```python
from langfuse import Langfuse

langfuse = Langfuse()

# Create session
trace = langfuse.trace(
    name="chat_session",
    session_id=session_id,
    user_id=user_id,
    metadata={"channel": "web"},
)

# Each turn creates a new trace with same session_id
turn_trace = langfuse.trace(
    name="chat_turn",
    session_id=session_id,  # Links to session
    user_id=user_id,
)
```

### LangGraph State
```python
from langgraph.graph import StateGraph
from typing import TypedDict

class ConversationState(TypedDict):
    session_id: str
    conversation_id: str
    turn_number: int
    messages: list
    context_tokens: int

@observe(name="conversation.turn")
def handle_turn(state: ConversationState):
    span = get_current_span()
    span.set_attribute("session.id", state["session_id"])
    span.set_attribute("conversation.turn_number", state["turn_number"])
    span.set_attribute("context.tokens", state["context_tokens"])
    # Process turn
```

## Aggregation Metrics

```python
# Per-session aggregates
span.set_attribute("session.avg_turn_latency_ms", 2500)
span.set_attribute("session.avg_turn_tokens", 850)
span.set_attribute("session.user_satisfaction", 0.85)

# Cross-session patterns
span.set_attribute("user.sessions_total", 15)
span.set_attribute("user.avg_session_length", 8)
span.set_attribute("user.retention_days", 30)
```

## Anti-Patterns

- Logging full conversation history (PII, storage)
- No session linking (orphaned traces)
- Missing turn numbers (can't analyze flow)
- No drop-off detection (silent failures)
- User ID without hashing (PII exposure)

## Related Skills
- `token-cost-tracking` - Session cost aggregation
- `evaluation-quality` - Session-level quality
