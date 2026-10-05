---
name: mcp-server
description: Use when building a Model Context Protocol server. Covers tool, resource, and prompt design, transport choice, authentication, error handling, and testing an MCP server against a real client.
metadata:
  category: ai
  version: 1.0.0
  tags: [mcp, tools, protocol, integration, agents]
---

# MCP Server

## Purpose

Build an MCP server that a model can use correctly. The protocol is straightforward; the difficulty is designing a tool surface that a language model uses well, which is a different problem from designing an API for a programmer.

## When to Use

- Exposing a system's capabilities to an LLM client.
- Wrapping an internal API for agent use.
- Improving an MCP server whose tools the model uses incorrectly.

## Capabilities

- Tool design: granularity, naming, schema, and descriptions.
- Resources for read-only context.
- Prompts as reusable, parameterized templates.
- Transports: stdio for local, HTTP/SSE for remote.
- Authentication and authorization.
- Error returns that let a model recover.

## Inputs

- The underlying system and its API.
- The tasks a model should be able to accomplish.
- The security boundary: what the model may do, and on whose behalf.

## Outputs

- A server whose tool descriptions unambiguously state when each tool applies.
- Errors that are instructive rather than merely accurate.
- A test suite exercising the tools as a model would call them.

## Workflow

1. **Design around tasks, not endpoints** — Do not mirror your REST API one-to-one. A model needs `find_order_by_customer`, not `GET /orders` with fourteen optional query parameters.
2. **Write the description as if it were the prompt** — Because it is. State what the tool does, when to use it, when *not* to use it, and what it returns. This text determines whether the model uses the tool correctly.
3. **Constrain the inputs** — Enums, not free strings. Required parameters, not optional ones the model must guess.
4. **Return errors a model can act on** — What went wrong, and what to do instead. An error that names the valid values lets the model self-correct in one step.
5. **Keep responses compact** — Return what the model needs. A tool returning a 40 KB JSON blob spends the model's context on noise.
6. **Test as a client** — Not with unit tests on the handlers. Connect a real client and watch which tools the model picks and how it uses them. It will surprise you.

## Best Practices

- The tool description is the single highest-leverage text in an MCP server. If the model calls the wrong tool, the description is wrong — not the model.
- Twelve well-designed tools beat forty thin wrappers around API endpoints. Every additional tool is a decision the model must make correctly.
- Distinguish tools (actions with side effects, model-invoked) from resources (read-only context, application-selected). Modeling read-only data as a tool forces the model to call it, which wastes a turn.
- Destructive tools should be clearly marked and, where the client supports it, require confirmation.
- Validate every input server-side. The model will send a malformed argument eventually, and the tool must not act on it.
- Never trust the model's authorization reasoning. Enforce permissions in the server, scoped to the authenticated user — not to the model's belief about who it is acting for.

## Examples

**A tool designed for a model:**

```typescript
server.registerTool(
  "find_orders",
  {
    title: "Find orders",
    description: [
      "Search for orders by customer, status, or date range.",
      "",
      "Use this when you do NOT already know the order ID. If you have an order ID,",
      "use `get_order` instead — it is faster and returns the full detail including",
      "line items and refund history.",
      "",
      "At least one filter is required. Returns up to 20 matches, most recent first,",
      "with only the order ID, status, total, and customer email. Call `get_order`",
      "with an ID from these results to see more.",
    ].join("\n"),
    inputSchema: {
      customerEmail: z.string().email().optional()
        .describe("Exact email address. Partial matches are not supported."),
      status: z.enum(["open", "paid", "shipped", "cancelled"]).optional()
        .describe("Exact status. Use 'open' for orders not yet paid."),
      placedAfter: z.string().date().optional()
        .describe("ISO date (YYYY-MM-DD). Orders placed on or after this date."),
    },
  },
  async ({ customerEmail, status, placedAfter }, { authInfo }) => {
    if (!customerEmail && !status && !placedAfter) {
      return {
        isError: true,
        content: [{
          type: "text",
          // Instructive, not merely accurate. The model can fix this on the next turn.
          text: "At least one filter is required. Provide customerEmail, status, or placedAfter.",
        }],
      };
    }

    // Authorization is enforced here, against the authenticated principal —
    // never against what the model claims.
    const orders = await db.orders.search({
      tenantId: authInfo.tenantId,
      customerEmail, status, placedAfter,
      limit: 20,
    });

    if (orders.length === 0) {
      return { content: [{ type: "text",
        text: "No orders matched. Try widening the date range or removing the status filter." }] };
    }

    // Compact: four fields per row, not the full object graph.
    return {
      content: [{
        type: "text",
        text: orders
          .map((o) => `${o.id} | ${o.status} | ${(o.totalCents / 100).toFixed(2)} ${o.currency} | ${o.customerEmail}`)
          .join("\n"),
      }],
    };
  },
);
```

**Resources for context the model should read, not call:**

```typescript
// A resource is read-only context the client can attach. Modeling this as a
// tool would force the model to spend a turn asking for something it always needs.
server.registerResource(
  "order-schema",
  "schema://orders",
  { title: "Order schema", mimeType: "text/markdown" },
  async () => ({
    contents: [{ uri: "schema://orders", text: await readFile("docs/order-schema.md") }],
  }),
);
```

## Notes

- Test by connecting a real client and giving the model realistic tasks. Unit tests confirm the handler works; only a real client shows you that the model consistently reaches for the wrong tool because two descriptions overlap.
- stdio transport is right for local, single-user servers. HTTP with SSE is right for remote, multi-user servers — and immediately raises authentication and multi-tenancy questions that stdio lets you ignore.
- If a tool's description needs to explain a workflow ("first call X, then call Y with the result"), consider whether it should be one tool that does both.
