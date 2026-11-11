---
name: jobs-review
version: 1.0.0
description: |
  Steve Jobs product review. Scores the entire product 0-10, demands coherence
  across every surface. Use after any UI/UX/product decision.
  Use when asked to "product review", "jobs review", "score this product",
  "UX critique", or "product critique".
  Proactively suggest when the user has made UI/UX/product decisions
  that should be reviewed before shipping.
allowed-tools:
  - Agent
  - Read
  - Grep
  - Glob
---

Launch the `jobs-review` agent to perform the product review.

```
Use the Agent tool with subagent_type "jobs-review" to review the product.
Pass along any arguments or context the user provided.
If the user specified a URL, directory, or specific area to review, include that in the agent prompt.
```

The agent handles discovery, scoring, and persistence (DESIGN.md / TODOS.md) autonomously.
Return the agent's full output to the user.
