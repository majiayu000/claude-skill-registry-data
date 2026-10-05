---
name: token-miser
description: >
  Minimize Claude token and cost waste across ALL surfaces — Claude Code subagents,
  API calls in code, and artifacts. Routes subagent model selection via the Agent
  tool's model parameter. Recommends /model switches when the current model is
  overkill or underpowered. Applies to any code importing anthropic or calling
  /v1/messages. Trigger on: "API call", "artifact", "pipeline", "multi-agent",
  "LangGraph", "which model", "save tokens", "reduce cost", "claude API", "token
  usage", "context window", any code importing anthropic or calling /v1/messages,
  subagent launches, or any discussion about optimizing Claude usage or costs.
---

# Token-Miser

Route every Claude interaction to the cheapest model that can handle it reliably.
This applies to **three surfaces**:

1. **Claude Code subagents** — set `model` param on every `Agent` tool call
2. **API calls in code** — model selection when writing code that calls Anthropic
3. **Artifacts** — model selection for API calls inside artifacts

Never mention routing decisions to the user unless asked — just apply them.

---

## Scope

| Surface | Mechanism | What Token-Miser Does |
|---------|-----------|----------------------|
| **Claude Code subagents** | `Agent` tool `model` param (`haiku`, `sonnet`, `opus`) | Route every subagent to cheapest viable model |
| **Claude Code main model** | Recommend `/model` switch to user | Flag when current model is overkill or underpowered |
| **API calls in code** | Model string in `anthropic.messages.create()` | Route to optimal model, escalation wrappers, batching, caching |
| **Artifacts** | Model string in browser API calls | Same as API calls |

---

## Model Tiers (Verified 2026-03-17)

| Tier | Model | Agent Param | API String | Cost | Context |
|------|-------|-------------|-----------|------|---------|
| 1 — Fast/Cheap | Haiku 4.5 | `haiku` | `claude-haiku-4-5-20251001` | ~1x | 200K |
| 2 — Balanced | Sonnet 4.6 | `sonnet` | `claude-sonnet-4-6` | ~3x | 200K |
| 3 — Powerful | Opus 4.6 | `opus` | `claude-opus-4-6` | ~5x | 200K (1M beta) |

See `references/model-pricing.md` for detailed token pricing.

---

## Claude Code Subagent Routing

**This is the primary cost lever.** Every `Agent` tool call accepts an optional
`model` parameter. Always set it explicitly based on the task.

### Subagent Routing Table

| Subagent Task | Model | Rationale |
|--------------|-------|-----------|
| File search, pattern matching (Explore) | `haiku` | Read-only, deterministic |
| Simple grep/glob delegation | `haiku` | Mechanical search |
| Code review (style, linting) | `haiku` | Pattern matching, checklist |
| Test runner, build validation | `haiku` | Execute + report, no reasoning |
| Research — single focused question | `sonnet` | Needs synthesis |
| Research — broad exploration | `sonnet` | Multi-step, judgment calls |
| Code generation (simple function, boilerplate) | `sonnet` | Needs correctness |
| Code generation (complex, multi-file, architectural) | `opus` | High stakes, needs reasoning |
| Planning / architecture design | `opus` | Open-ended, judgment-heavy |
| Debugging (root cause analysis) | `sonnet` | Start here, escalate if stuck |
| Writing documentation | `haiku` | Templated, low ambiguity |
| Git operations, status checks | `haiku` | Mechanical |

### When NOT to downgrade subagents

- Subagent will **write code** that gets committed — sonnet minimum
- Subagent needs to **make judgment calls** about ambiguous requirements — sonnet+
- Subagent result feeds directly into **user-facing output** — match main model tier
- Task previously failed at a lower tier — escalate, don't retry same tier

---

## Main Model Recommendations

| Situation | Recommendation |
|-----------|---------------|
| User on Opus, doing simple file edits / git ops | Suggest: `/model sonnet` would save cost |
| User on Haiku, attempting complex multi-file refactor | Suggest: `/model opus` recommended |
| User on Sonnet, task is clearly Haiku-tier | Don't mention — switching friction not worth it |
| User on Sonnet, task is clearly Opus-tier | Suggest only if quality likely to suffer |

**Rule:** Only recommend switches when the cost/quality delta is significant.
Sonnet is always an acceptable default.

---

## Freshness Protocol

1. **Read** `references/model-pricing.md` header date.
2. **If <90 days old** — use as-is.
3. **If >90 days old** — web-search `Anthropic Claude API pricing` before using prices.
4. **If prices changed** — update the reference file.

Skip when: applying routing table (no dollar amounts needed), subagent model
selection (relative tiers don't change with pricing), token efficiency rules.

---

## Routing Decision Framework

### Step 1 — Classify the task

| Task Type | Default Tier | Notes |
|-----------|-------------|-------|
| Simple Q&A, classification, extraction | 1 | Single-turn, clear answer |
| Summarization (short doc, <20K tokens) | 1 | |
| Summarization (long doc, >20K tokens) | 2 | Context pressure |
| Code generation (boilerplate, simple functions) | 1 | |
| Code generation (complex logic, multi-file) | 2 | |
| Code debugging / root cause analysis | 2 | Start here |
| Reasoning / multi-step math / analysis | 2 | Start here |
| Complex reasoning with ambiguous constraints | 3 | |
| Long-context document processing (>100K tokens) | 2 | Watch cost |
| Tool use — simple, single tool | 1 | |
| Tool use — multi-tool, agentic chains | 2 | |
| Tool use — autonomous, open-ended agent | 3 | |
| Structured output / JSON extraction | 1 | |
| Grading / judging other model outputs | 2 | Avoid circular bias |

### Step 2 — Apply modifiers

Bump **up** one tier if:
- Output is user-facing AND quality-sensitive
- Task requires multi-hop reasoning or >3 tool calls in a chain
- Input context >100K tokens
- Previous attempt at lower tier produced poor results

Bump **down** one tier if ALL of:
- Output is intermediate (not user-facing)
- Task is deterministic and templated
- Correctness is cheaply verifiable

### Step 3 — Fallback / escalation

- Malformed output — retry once at same tier, then escalate
- Logically inconsistent — escalate one tier
- Confident and well-formed — done

---

## Token Efficiency Rules

1. **Trim system prompts** — under 500 tokens unless required.
2. **Batch** — one call with 10 items beats 10 sequential calls.
3. **Cap `max_tokens`** — set to minimum plausible output length.
4. **Cache-friendly prompts** — stable content at the top.
5. **Avoid redundant context** — summarize prior turns, don't echo.
6. **Structured output** — JSON/tables over prose when consumer is a machine.
7. **Minimize calls per interaction** — batch user inputs before calling API.

---

## Multi-Call Pipeline Design

```
[Router / Planner]   → Tier 1 or 2 (classify intent, decompose task)
[Subtask Workers]    → Tier 1 (extraction, formatting, simple transforms)
[Synthesizer]        → Tier 2 (combine, reason across results)
[Quality Gate]       → Tier 1 (schema check) → escalate to Tier 2 if fail
[Final Response]     → Tier matching user-facing quality bar
```

**General rule:** cheap models do the volume work; expensive models do the judgment.

---

## Project-Specific Routing

### <your-project> (LangGraph tax pipeline)
- Intent classification: Haiku | RAG scoring: Haiku | Tax reasoning: Sonnet/Opus
- Response synthesis: Sonnet minimum | Security guardrails: Haiku

### <internal-project-3> (guest messaging pipeline)
- Webhook parsing: Haiku | Guest messages: Sonnet | Review responses: Sonnet

### <internal-project-4> (interview pipeline)
- Form extraction: Haiku | State transitions: Haiku | Tax calculation: Sonnet

### <internal-project-1> / Infrastructure
- No API calls — token-miser applies only to subagent routing during Claude Code sessions

---

## Quick Reference Card

```
SUBAGENT ROUTING (Claude Code):
  Explore/search/grep:  haiku     Research/synthesis:   sonnet
  Code gen (simple):    sonnet    Code gen (complex):   opus
  Test/build/git:       haiku     Planning/arch:        opus
  Docs/formatting:      haiku     Debugging:            sonnet

API / ARTIFACT ROUTING:
  Task complexity:   LOW  → Haiku    MED  → Sonnet    HIGH → Opus
  Context size:      <20K → Haiku    20K-100K → Sonnet  >100K → Sonnet/Opus
  User-facing:       No   → Haiku    Yes → +1 tier if quality-sensitive
  Cost ratio:        1x         ~3x              ~5x

NOTE: Opus 4.6 at $5/$25 is only 5x Haiku (not 15x like legacy Opus 4.1).
When in doubt between Sonnet and Opus, quality wins.
```
