---
name: mcp-builder
description: Use when building a new MCP server. Covers stdio vs HTTP, tool schema, error handling.
---

# Building an MCP server

MCP (Model Context Protocol) lets Claude Code call external tools through a uniform protocol. A server exposes a set of tools; the client (Claude Code) discovers them and calls them with JSON arguments. Good MCP servers are small, named clearly, and return structured errors.

## When to trigger
- The user asks to build, scaffold, or extend an MCP server.
- A project imports `@modelcontextprotocol/sdk` (JS/TS) or the `mcp` package (Python).
- The user wants Claude to talk to a system that does not yet have a tool, and a one-off Bash command is not enough.

## Transport: stdio vs HTTP vs SSE

Pick the transport before writing any tools.

- **stdio** - default and simplest. The server is a subprocess Claude Code launches; messages go over stdin/stdout. Use this for local-only tools (filesystem, local DB, CLI wrappers). No auth, no ports.
- **HTTP** (streamable) - use when the server must be shared across machines, run inside Docker on a remote host, or sit behind auth. More moving parts: you own the port, TLS, and tokens.
- **SSE** - older HTTP variant. Avoid for new servers unless a client requires it.

Default to stdio. Upgrade to HTTP only when stdio cannot work.

## Tool schema

Each tool needs three things:

- `name` - kebab-case or snake_case, unique within the server. Short and concrete: `read_invoice`, `list_buckets`.
- `description` - the prose Claude sees when deciding whether to call the tool. This is the single most important field. See below.
- `inputSchema` - JSON Schema describing arguments. Use real types, set `required`, and prefer enums over free-form strings when the value space is small.

Example (JS):

```js
server.tool(
  "read_invoice",
  "Read a single invoice by ID. Returns line items and totals. Use when the user references an invoice number.",
  {
    invoiceId: z.string().describe("Invoice ID, e.g. INV-2024-0001"),
  },
  async ({ invoiceId }) => {
    // ...
  }
);
```

## Writing tool descriptions

The description is what makes Claude pick your tool over another. Treat it like a skill `description`:

- Start with a verb: `Read ...`, `List ...`, `Create ...`.
- State what the tool returns.
- State when to use it (`Use when ...`).
- Mention any non-obvious constraints (rate limits, idempotency, side effects).

Bad: `Gets invoice data.`

Good: `Read a single invoice by ID. Returns line items, totals, and customer info. Use when the user references a specific invoice number. Read-only.`

If you cannot describe the tool in two sentences, it is doing too much - split it.

## Error handling

Never throw raw exceptions across the protocol boundary. Return a structured error result so Claude can react:

```js
return {
  isError: true,
  content: [{ type: "text", text: `Invoice ${id} not found` }],
};
```

For Python (`mcp` package), set `isError=True` and put a human-readable message in the content. Avoid leaking stack traces unless the user explicitly asked for debug output - they pollute Claude's context.

For transient errors (network, rate limit), include enough info that a retry could succeed (`retry_after`, `request_id`).

## SDK choice

- **JS/TS**: `@modelcontextprotocol/sdk`. Mature, supports stdio and HTTP, integrates with Zod for schemas.
- **Python**: `mcp` package. Use `FastMCP` for a decorator-based style if you want minimal boilerplate.
- **Other languages**: only if a language requirement forces it - the SDKs in JS and Python are the most maintained.

## Testing

Install the server locally and exercise it through Claude Code:

```powershell
claude mcp add my-server --command "node ./dist/server.js"
```

For HTTP servers:

```powershell
claude mcp add my-server --url "https://localhost:3000/mcp" --header "Authorization: Bearer ..."
```

Then start a fresh Claude Code session and ask Claude to use one of your tools. Watch the actual call: does Claude pick the right tool? Are arguments well-formed? If the wrong tool fires, the description is the lever - tighten it.

Write a smoke-test script (in the server's own repo) that drives each tool with a known input and asserts the output shape. Run it on every change.

## Performance notes

- Cold start matters for stdio servers because Claude Code launches them per session. Keep the dependency tree small.
- Stream long outputs when the SDK supports it - large single responses inflate context fast.
- Cache expensive lookups inside the server process. Claude will happily call the same tool 5 times in a row.

## Red flags

- More than ~15 tools on a single server. Split by domain (one server for invoices, one for shipping) so Claude's tool-picking does not get overloaded.
- Tool descriptions under one sentence. Claude will pick the wrong one.
- Tools that return raw blobs (entire files, full DB tables). Paginate, summarize, or filter at the server.
- Errors thrown as native exceptions instead of `isError` results.
- HTTP transport for a tool that only ever runs on the user's own machine. Use stdio.
- Tool names that collide with another installed server (`list`, `read`, `get`). Namespace them: `gh_list_prs`, not `list`.

## References

- MCP spec: https://modelcontextprotocol.io
- `claude mcp` CLI: `claude mcp --help`
- `skill-creator` for writing the description well - same principles apply.
