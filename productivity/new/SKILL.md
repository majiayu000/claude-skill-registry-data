---
name: new
description: Create and immediately execute the appropriate ephemeral mcx optimization for MCP overhead. Use when an mcx hook identifies multiple related MCP calls or a bloated result, or when the user asks to optimize, aggregate, filter, batch, or fan out an MCP workflow. Selects an existing chain when available; otherwise runs ad-hoc script source for a multi-call workflow or configures a filter for oversized single-tool results. Never registers a chain; route explicit persistence requests to /mcx:save.
---

# Create an mcx optimization

Choose the mechanism from the work, not from terminology the user happens to
know.

## Decide

1. Run `mcx list` so you do not duplicate an existing chain.
2. Use a matching registered chain when one exists.
3. For two or more related MCP calls, a fan-out, join, pagination loop, bulk
   mutation, or aggregation, follow [references/chain.md](references/chain.md).
4. For one MCP tool whose result is dominated by unused fields, follow
   [references/filter.md](references/filter.md).
5. When both signals appear, use an ad-hoc chain first. Its intermediate MCP
   payloads remain inside the sandbox, so filtering those internal calls is
   unnecessary unless the same tool is also used directly elsewhere.
6. Create nothing for a single compact isolated call.

## Persistence boundary

Default to ad-hoc source executed with
`mcx run <args-json> <language>` and a heredoc.
Do not create a durable chain. When the user explicitly asks to save, register,
name, or reuse the workflow, invoke `/mcx:save` after proving the ephemeral run.

Keep the final output to the smallest digest that answers the task. Never emit
raw intermediate MCP payloads.
