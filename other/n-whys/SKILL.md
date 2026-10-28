---
name: n-whys
description: Generate a why-chain exactly n levels deep for any topic, question, observation, problem, or idea. Invoke like `n-whys n=8 q=<my question>`. The general form of five-whys — use this when you want an explicit depth.
compatibility: Created for Zo Computer
metadata:
  author: rob.zo.computer
---

# N Whys

Use this skill when the user invokes `n-whys` or asks for a why-chain of a specified depth.

**Relationship to `five-whys`:** `five-whys` is a preset of this skill — depth ~5, root-cause orientation, flexible stopping. Use `n-whys` when the user wants a deliberate, exact depth or an unusually deep chain.

## Invocation

Expected form:

```text
n-whys n=<integer> q=<question or topic>
```

Examples:

```text
n-whys n=8 q=Why do people procrastinate on work they care about?
n-whys n=4 q=Why is this product hard to explain?
n-whys n=10 q=AI agents feel brittle
```

## Arguments

- `n`: required integer depth for the chain.
- `q`: required question, topic, statement, problem, or observation to analyze.

If `n` or `q` is missing, ask for the missing argument. If `n` is very large, proceed unless the user asks for something impractically long; keep each layer concise.

## Purpose

N Whys generalizes the Five Whys. It repeatedly asks "why?" exactly `n` times to expose deeper causes, assumptions, mechanisms, incentives, constraints, or principles beneath a surface question.

The chain can take several forms depending on the topic:

- **causal** — event chains, mechanisms, failures
- **conceptual** — deeper premises behind a claim
- **incentive-based** — who benefits, what pressures exist
- **psychological** — motivations, fears, needs
- **philosophical** — grounding values and assumptions

## Canonical questions

- Why do people procrastinate on work they care about? (n=8)
- Why is the sky blue? (n=6, physics chain)
- Why do startups die? (n=10)
- Why does this abstraction feel wrong? (n=5)

## Procedure

1. Parse `n` and `q` from the invocation.
2. Restate `q` as the surface question or topic.
3. Produce exactly `n` numbered why-layers.
4. Each layer should:
   - ask a natural "why" question about the previous layer,
   - answer it directly,
   - go one level deeper than the prior answer.
5. Keep facts, hypotheses, and interpretations distinct.
6. After the chain, synthesize the deepest insight or principle.
7. End with implications: what this suggests doing, checking, reframing, or asking next.

## Output format

```markdown
## Topic
<q>

## Why chain
1. **Why ...?**
   - ...
2. **Why ...?**
   - ...
...
N. **Why ...?**
   - ...

## Deepest principle
...

## Implications
- ...
```

## Guardrails

- Produce exactly `n` why-layers unless the user changes the request.
- Do not pad with fake certainty. If a link is speculative, label it as a hypothesis.
- Avoid blame in human or organizational topics; prefer systems, incentives, constraints, and feedback loops.
- If the chain becomes circular, name the loop and continue by asking why the loop persists.
- If the topic is conceptual rather than causal, interpret "why" as "what deeper premise explains this?"
