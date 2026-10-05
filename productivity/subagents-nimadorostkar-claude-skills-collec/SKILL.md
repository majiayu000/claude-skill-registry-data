---
name: subagents
description: Use when delegating work to a separate agent with its own context. Covers when delegation pays off, designing a subagent's scope and prompt, parallel fan-out, and the cost of a cold start.
metadata:
  category: agent-tooling
  version: 1.0.0
  tags: [subagents, delegation, context, parallelism]
---

# Subagents

## Purpose

Delegate work to a subagent when its own context is worth the cost of starting one. A subagent begins cold — it re-derives everything the main agent already knows — so the delegation must buy more than it costs.

## When to Use

- A search or exploration that would flood the main context with results you do not need to keep.
- Independent work that can run in parallel.
- A task requiring a different, specialized instruction set.
- Verification by an agent that has not seen the reasoning that produced the work.

## Capabilities

- Scoping a subagent's task and boundaries.
- Prompt design for a cold-start agent.
- Parallel fan-out for independent work.
- Result aggregation.
- Read-only agents for review and verification.

## Inputs

- The task, and whether it is genuinely independent.
- What the subagent needs to know, since it knows nothing.
- What it must return.

## Outputs

- A subagent that completes its task without further interaction.
- A result compact enough to be worth the round trip.

## Workflow

1. **Justify the delegation** — The valid reasons are: context isolation (the search produces 50 files of noise and one answer), parallelism (five independent tasks), and specialization (a different instruction set). "The task is big" is not a reason — a big task in the same context is usually cheaper.
2. **Write the prompt as if to a stranger** — Because it is one. The subagent has none of your context: no conversation history, no prior findings, no shared understanding of the goal. Everything it needs must be in the prompt.
3. **State exactly what to return** — A subagent that returns a wall of text has moved the context problem rather than solved it. Specify the format and the length.
4. **Fan out only genuinely independent work** — Two subagents editing the same file will conflict. Parallelism requires disjoint scopes.
5. **Use a read-only agent for verification** — An agent that did not write the code is a better reviewer of it than the one that did.

## Best Practices

- A subagent starts cold and re-derives context you already have. That is the cost. It is worth paying for isolation and parallelism, and it is not worth paying to avoid a long turn.
- The subagent's prompt is the entire interface. Include the file paths, the constraints, the definition of done, and the return format. Ambiguity produces a confidently wrong answer you then have to check.
- Search and exploration are the archetypal delegation: the subagent reads forty files and returns one paragraph. That paragraph is what you wanted; the forty files are what you were trying to avoid.
- Do not delegate a task you cannot verify. A subagent's report is a claim, not evidence.
- Parallel subagents that write to the same files will race. Give each a disjoint scope, or serialize them.
- Verification by a fresh agent is genuinely more effective than self-review — it has no attachment to the approach and no memory of why a shortcut seemed reasonable.

## Examples

**Delegation that pays for itself — exploration with a compact return:**

```text
Task for the subagent:

Find every place in this repository where an outbound HTTP call is made without
a timeout.

Search for: fetch(), axios, httpx, requests, http.Client, and any wrapper around
them in src/. For each call site, determine whether a timeout is configured —
either at the call, on the client, or by a default in a shared client factory.

Do not fix anything. Do not read files that are not relevant.

Return ONLY a markdown table with these columns, and nothing else:
| File:line | Call | Timeout configured? | Where the timeout is set (or "none") |

If there are more than 20, return the 20 with the widest blast radius (those in
request paths rather than in scripts or tests) and state the total count.
```

The subagent reads sixty files. It returns a twenty-row table. The main context receives the table.

**A delegation that is not worth it:**

```text
"Implement the refund feature."

The subagent does not know: the domain conventions, the Result type, the fact
that Money is an integer, the existing RefundService, or why the previous
approach was rejected. It will re-derive some of this, get some of it wrong,
and return code that must be reviewed line by line against context it never had.

Doing this in the main context — where all of that is already established — is
faster and produces better code.
```

**Parallel fan-out with disjoint scopes:**

```text
Three subagents, in parallel, each with a scope that cannot collide:

  1. "Audit skills/frontend/ for broken internal links. Report only."
  2. "Audit skills/backend/ for broken internal links. Report only."
  3. "Audit skills/devops/ for broken internal links. Report only."

Read-only, disjoint, independently useful. This is the shape delegation is for.
```

## Notes

- The single best use of a subagent is a search whose intermediate results you do not want. The isolation *is* the product.
- A subagent that needs to ask a follow-up question has been given an insufficient prompt. Since it usually cannot ask, it will guess. Write the prompt accordingly.
- Verification subagents are most valuable on high-stakes work: a fresh reader catches the thing the author's context made invisible.
