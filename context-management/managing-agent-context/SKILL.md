---
name: managing-agent-context
version: "1.0.0"
description: >
  Manages context windows in long-running AI agent loops — deciding when
  to summarize vs. truncate, implementing rolling window patterns,
  preserving critical context while shedding stale state, and budgeting
  tokens across multi-turn agent interactions. Activates when an agent
  is running out of context, building autonomous loops that run many
  turns, experiencing context window errors, trying to keep agents
  focused across long sessions, managing token costs in multi-turn
  interactions, or designing agents that need to maintain state across
  hours or days. Also triggers on: context limit, token limit, context
  window full, agent loses track, agent forgets, long-running agent,
  context overflow, too many tokens, context management, rolling summary,
  compaction, context pruning.
---

# Agent Context Window Management

The context window is the agent's working memory. When it fills up, the
agent loses access to its own history. This skill covers architectural
patterns for managing that constraint in production agent loops.

Distinct from `ecc:strategic-compact` which handles Claude Code session
compaction for interactive developer sessions. This skill covers autonomous
agent loops that accumulate context across hundreds of tool calls.

---

## The Core Problem

Every turn of an agent loop adds tokens:
- The original task and system prompt (fixed)
- Each user message and assistant response (growing)
- Each tool call and tool result (growing fast)
- Accumulated reasoning and intermediate state (growing)

At some point: context limit reached → agent fails or must be restarted.
Solution: proactive context management before the limit is hit.

---

## Decision Tree

```
What's your situation?
  │
  ├─ Agent is hitting context limits in production
  │    → Section 1: Emergency Reduction Patterns
  │
  ├─ Designing a new multi-turn agent
  │    → Section 2: Context Budget Planning
  │
  ├─ Building an autonomous loop (many tool calls)
  │    → Section 3: Rolling Window Architecture
  │
  └─ Agent loses important context mid-session
       → Section 4: Critical Context Preservation
```

---

## Section 1: Emergency Reduction Patterns

If an agent is hitting context limits in production now:

**Option A: Truncate oldest messages (fastest fix)**
Drop the oldest user/assistant turns while keeping:
- The system prompt
- The last N turns (start with N=10, adjust)
- Any tool results still referenced in active reasoning

```python
def truncate_to_fit(messages: list, max_tokens: int, keep_last_n: int = 10) -> list:
    system = [m for m in messages if m["role"] == "system"]
    turns = [m for m in messages if m["role"] != "system"]
    
    # Keep last N turns
    trimmed = system + turns[-keep_last_n * 2:]  # *2 for user+assistant pairs
    
    # If still too long, reduce N
    if estimate_tokens(trimmed) > max_tokens:
        trimmed = system + turns[-6:]
    
    return trimmed
```

**Option B: Summarize and replace (better quality)**
Have the model summarize the conversation history before it exceeds
the limit, then replace the raw history with the summary.

See Section 3 for the full rolling window implementation.

---

## Section 2: Context Budget Planning

Before building a multi-turn agent, define a context budget.

**Context budget formula:**
```
Total window (e.g., 200K tokens)
  - System prompt:     ~2K tokens (reserve)
  - Task description:  ~1K tokens (reserve)
  - Tool definitions:  ~3K tokens per 10 tools (reserve)
  - Buffer (15%):      ~30K tokens (safety margin)
────────────────────────────────────────────────
Available for turns:  ~164K tokens

Typical turn cost:    ~500-2K tokens per turn
Max turns before management required: ~80-300 turns
```

**Design rule:** trigger context management at 70% of the window,
not 95%. Waiting until the window is nearly full means you're already
in a degraded state before you start managing.

```python
CONTEXT_MANAGEMENT_THRESHOLD = 0.70  # 70% of max context

def needs_context_management(messages: list, model_max_tokens: int) -> bool:
    current_tokens = estimate_tokens(messages)
    return current_tokens > (model_max_tokens * CONTEXT_MANAGEMENT_THRESHOLD)
```

---

## Section 3: Rolling Window Architecture

The standard architecture for long-running agents.

**Pattern:** maintain a rolling summary that replaces accumulated history,
keeping only the summary + recent turns in the active context.

```python
SUMMARY_TRIGGER_TOKENS = 100_000  # adjust based on model max
TURNS_TO_KEEP_AFTER_SUMMARY = 6    # keep recent turns verbatim

async def manage_context(
    messages: list,
    model_max_tokens: int,
    anthropic_client
) -> list:
    if not needs_context_management(messages, model_max_tokens):
        return messages
    
    system_msgs = [m for m in messages if m["role"] == "system"]
    turns = [m for m in messages if m["role"] != "system"]
    
    # Split: turns to summarize vs. turns to keep verbatim
    turns_to_summarize = turns[:-TURNS_TO_KEEP_AFTER_SUMMARY * 2]
    turns_to_keep = turns[-TURNS_TO_KEEP_AFTER_SUMMARY * 2:]
    
    if not turns_to_summarize:
        return messages  # nothing to compress yet
    
    # Generate a summary of the portion being discarded
    summary_response = await anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",  # use cheaper model for summarization
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"""Summarize this agent conversation history concisely.
Preserve: decisions made, actions taken, data discovered, any blockers.
Discard: conversational filler, intermediate reasoning that led to decisions.

History:
{format_turns_for_summary(turns_to_summarize)}

Produce a structured summary under 800 tokens."""
            }
        ]
    )
    
    summary_text = summary_response.content[0].text
    
    # Replace history with summary injection
    summary_msg = {
        "role": "user",
        "content": f"[CONTEXT SUMMARY — earlier conversation compressed]\n{summary_text}"
    }
    summary_ack = {
        "role": "assistant",
        "content": "Understood. I have the context from earlier in the conversation."
    }
    
    return system_msgs + [summary_msg, summary_ack] + turns_to_keep
```

**Cost note:** Use `claude-haiku` for summarization — it's 10-20x cheaper
than Sonnet for this task and adequate for compressing agent history.

---

## Section 4: Critical Context Preservation

Some context must survive summarization. Before compressing, extract
and preserve:

```python
CRITICAL_CONTEXT_FIELDS = [
    "task_objective",       # The original task the agent is solving
    "decisions_made",       # Key choices that constrain future actions
    "data_discovered",      # Facts found that will be needed later
    "actions_completed",    # What has already been done (avoid repetition)
    "active_constraints",   # Rules or limits in effect
    "current_blockers",     # Issues that still need resolution
]
```

Store critical context separately from the message history. Inject it
into the context at each turn as a structured header:

```python
def build_context_header(critical_context: dict) -> str:
    return f"""
[PERSISTENT CONTEXT]
Objective: {critical_context.get('task_objective', 'None set')}
Decisions made: {'; '.join(critical_context.get('decisions_made', []))}
Completed actions: {'; '.join(critical_context.get('actions_completed', []))}
Active constraints: {'; '.join(critical_context.get('active_constraints', []))}
[END PERSISTENT CONTEXT]
"""
```

This ensures that even after aggressive context compression, the agent
retains the information it needs to continue correctly.

---

## Self-Verification

- [ ] Context budget calculated for this agent's model and tools
- [ ] Management triggered at 70% of window, not 95%
- [ ] Rolling summary uses cheaper model (Haiku, not Sonnet)
- [ ] Critical context fields extracted before any compression
- [ ] Tested: agent continues correctly after context management fires
- [ ] Token costs for context management included in per-session budget

---

## CLAIMS
- Triggering context management at 70% rather than 95% prevents quality
  degradation that occurs when the model is operating near its limit
- Using a cheaper model for summarization reduces context management
  overhead by 10-20x without meaningful quality loss for history compression

## COUNTEREXAMPLE
- For short-lived agents (under 20 turns), context management adds
  complexity without benefit; only implement for agents expected to
  exceed 50 turns regularly

## CONTRADICTIONS
- Aggressive context compression conflicts with full auditability of
  agent reasoning; if complete audit trails are required, use external
  storage (Supabase) to persist full transcripts before compression
