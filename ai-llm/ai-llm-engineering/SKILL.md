---
name: ai-llm-engineering
description: Design, integrate, evaluate, and operate AI/LLM systems using model- and framework-agnostic engineering principles.
metadata:
  internal: true
---

# ai-llm-engineering

Use this skill for LLM integrations, agents, prompts, embeddings, retrieval, evaluation, model workflows, and AI pipelines.

## Principles

Treat model output as untrusted and nondeterministic.

Separate:

- model instructions
- application logic
- tools
- retrieval
- persistence
- evaluation

Define expected outputs and failure behavior.

For structured output use enforceable schemas where available.

For tool use:

- validate arguments
- enforce authorization outside the model
- limit tool capability
- verify side effects

For retrieval systems evaluate both retrieval quality and final answer quality.

For prompts:

- state the task clearly
- provide relevant context
- avoid irrelevant context
- define output constraints where useful

For evaluation use representative cases and frozen test sets when comparing changes.

Do not tune against held-out evaluation cases.

For expensive model workloads consider:

- latency
- token usage
- caching
- batching
- retries
- rate limits
- fallback behavior

Do not treat model confidence as proof of correctness.

## Adaptation

Use project evidence to determine the actual language, framework, runtime, and existing conventions.

When stack-specific implementation guidance is needed, prefer project evidence, native framework or language mechanisms, and relevant user-installed specialist skills. Technology-specific guidance must not redefine or weaken the core engineering requirement.