---
name: ai-llm-dos
description: >
  Unbounded-consumption / denial-of-wallet attacks on LLM apps — force runaway tokens, cost, or
  latency. Load when testing an LLM product's limits/billing, on "LLM DoS", cost amplification, or
  resource exhaustion. Signals: user-controlled prompts/max_tokens, agent loops, no rate/'cost caps'.
domain: ai-ml
type: technique
stability: learning
modes: [bugbounty, defense]
severity: medium
owasp_llm: [LLM10:2025-Unbounded-Consumption]
cwe: [CWE-770, CWE-400]
tools: []
schema_version: 1
---

# LLM unbounded consumption (denial-of-wallet)

## When it applies
An LLM feature lets users drive expensive computation with weak limits. Unlike classic DoS, the
damage is often financial (the provider bills per token) — "denial of wallet" — plus latency/availability.

## Why it works
Inference cost scales with tokens and calls. If the app lets users control input size, output
length (`max_tokens`), recursion (agent loops, tool chains), or call volume without hard caps, an
attacker amplifies cost/latency far beyond normal use.

## Method
1. **Input amplification**: send very long inputs, or inputs that induce very long outputs
   ("repeat X 10000 times", "write an exhaustive…"); push `max_tokens` if client-controlled.
2. **Recursion / loops**: with agents, craft prompts that trigger long tool-call loops or
   self-referential expansion (→ `ai-agent-tool-abuse`) that burn calls.
3. **Volume**: bypass rate limits (→ `web-rate-limit-bypass`) and fan out concurrent expensive requests.
4. **Retrieval blow-up**: in RAG, queries that pull huge context each call multiply token cost.
5. **Measure impact**: latency spike, error/timeout rates, or (where visible) token/cost per request × achievable rate.

## Gotchas
- Frame it as impact (cost/availability), not just "it was slow" — quantify tokens/cost or a service degradation.
- Respect RoE strictly — this can run up real bills / affect availability; prove with minimal, controlled requests, don't sustain an outage.
- Defenders: cap input/output tokens, per-user quotas & spend caps, loop/tool budgets, timeouts.

## Verify success
A single request (or a modest, controlled burst) demonstrably drives disproportionate token/cost or
latency — showing missing consumption limits.

## References
OWASP LLM Top 10 (2025) LLM10; "denial of wallet" research; provider rate/quota docs.
