---
name: verify-over-assume
description: >
  Never assume something you can cheaply verify. On the Max plan, token saving is
  NOT the priority — correctness and quality are. If a fact is knowable via an MCP
  tool, API call, file read, or command, verify it instead of guessing. Spend the
  tokens to be certain.

  Trigger this skill when:
  - You're about to state a fact that a tool/MCP/API/file/command could confirm
    (API params, model ids, config values, schema, ticket state, file contents,
    a function signature, whether something exists).
  - You catch yourself hedging ("probably", "should be", "I think", "typically")
    about something verifiable.
  - You're tempted to skip a lookup to save tokens or time.
---

## The rule

**Do not guess what you can verify.** If the answer is knowable — a tool can fetch
it, an MCP call returns it, a file contains it, a command prints it — go get it,
then answer with certainty.

Priority order, always:

1. **Quality and correctness.** The best code, content, docs, or a simple-but-strong
   answer. Being *right* beats being *cheap*.
2. **Token efficiency.** A real but *secondary* concern. Never sacrifice #1 for it.

We are on the **Max plan**. Capacity is not the constraint — wrong answers are. Never
scrimp on a verifying call just to save tokens. A confident guess that turns out wrong
costs far more than the tool call would have.

## Verify — don't assume — when

- Stating an API's parameters, return shape, model id, pricing, or limits → check the
  source / SDK / docs, don't recall from memory.
- Referencing a file, function, symbol, flag, or config value → read it.
- Reporting the state of a ticket, PR, branch, deploy, or issue → query it (ClickUp,
  GitHub, Sentry MCP, git).
- Claiming something "exists" / "doesn't exist" / "is already implemented" → search or
  use CodeGraph, don't assume.
- Any answer where you'd otherwise write "probably", "should be", "I believe".

## When an assumption is acceptable

- The thing is genuinely **unknowable** or has **no accessible source** (a future
  decision, the user's private intent, an offline third-party system).
- The verification cost is **wildly** disproportionate to a trivial, low-stakes point
  AND you clearly flag the uncertainty ("I didn't verify X").
- It's a **preference/judgment** call with no factual ground truth.

In those cases, say what you assumed and why — don't present a guess as a fact.

## The stance

Be certain of what you tell the user when the data is known or the knowledge base is
easily reachable. If you can close the gap between "I think" and "I know" with one
call, make the call. Silence-on-cost is not a virtue here — accuracy is.
