---
name: qruiq-mcp-init
description: |
  Add MCP (Model Context Protocol) server to a Next.js app with OAuth2 auth and Streamable HTTP transport.
  Creates /api/mcp endpoint, Dynamic Client Registration, tool scaffolding, and favicon.
  Compatible with Claude.ai, ChatGPT, Gemini, Cursor, and any MCP client.
  Use this skill whenever the user asks to "add MCP", "setup MCP server", "add MCP support",
  "integrate with Claude MCP", "make my app work with Claude", "add AI integration",
  "connect to Claude.ai", or mentions MCP in the context of a Next.js project.
  Also use when the user has an existing OAuth2 setup and wants to add MCP on top of it.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# qruiq-mcp-init

> Add a production-ready MCP server to a Next.js app. Based on real deployment experience with xdone.app on TKE/Cloudflare.

## What this creates

| File | Purpose |
|---|---|
| `app/api/mcp/route.ts` | MCP endpoint — stateless Streamable HTTP transport |
| `app/oauth/register/route.ts` | Dynamic Client Registration (RFC 7591) |
| `lib/mcp-server.ts` | Tool definitions scaffold |
| OAuth metadata update | Adds `registration_endpoint` |
| `public/favicon.ico` | Icon for MCP client display |

## Prerequisites

**Check all before proceeding. Stop and prompt user if any fail:**

### 1. Project checks

```bash
# Must be Next.js App Router
ls app/layout.tsx

# Must have OAuth2 discovery endpoints
ls app/.well-known/oauth-authorization-server/route.ts
ls app/.well-known/oauth-protected-resource/route.ts

# Must have API auth helper with authenticateRequest()
ls lib/api-auth.ts

# Must have OAuth token endpoint
find app -path "*/oauth/token/route.ts" -o -path "*/oauth/token/route.ts" | head -1

# Must have OAuth authorize page
find app -path "*/oauth/authorize*" | head -1

# Must have Prisma with OAuthClient model
grep "model OAuthClient" prisma/schema.prisma
```

### 2. Auto-detect parameters

```bash
cat package.json | grep '"name"'
```

## Parameters

| Parameter | Required | Auto-detect | Example |
|---|---|---|---|
| `APP_NAME` | Yes | `package.json` name | `xdone` |

## Steps

**Execute all steps directly. Do not list as TODOs.**

### Step 1: Install MCP SDK

```bash
npm install @modelcontextprotocol/sdk --legacy-peer-deps
```

If peer dep conflicts, always use `--legacy-peer-deps`.

### Step 2: Copy template files

```bash
mkdir -p app/api/mcp app/oauth/register
cp ~/.qruiq/skills/skills/qruiq-mcp-init/template/app/api/mcp/route.ts app/api/mcp/route.ts
cp ~/.qruiq/skills/skills/qruiq-mcp-init/template/app/oauth/register/route.ts app/oauth/register/route.ts
cp ~/.qruiq/skills/skills/qruiq-mcp-init/template/lib/mcp-server.ts lib/mcp-server.ts
```

### Step 3: Replace placeholders

```bash
sed -i '' "s/__APP_NAME__/<APP_NAME>/g" lib/mcp-server.ts
```

### Step 4: Add `registration_endpoint` to OAuth metadata

Edit `app/.well-known/oauth-authorization-server/route.ts` and add to the response JSON object:

```typescript
registration_endpoint: `${baseUrl}/oauth/register`,
```

This tells MCP clients where to register themselves before starting the OAuth flow.

### Step 5: Make OAuthClient.userId optional

MCP clients register dynamically before any user authenticates, so `OAuthClient` must allow `userId = null`.

Check `prisma/schema.prisma`:

```prisma
model OAuthClient {
  // userId must be optional (String? not String)
  userId  String?
  user    User?     @relation(...)
}
```

If `userId` is required, make it optional and push:

```bash
npx prisma db push
npx prisma generate
```

### Step 6: Ensure favicon exists

MCP clients fetch `/favicon.ico` for the connector icon. Without it, you get a generic globe.

```bash
# Check if favicon exists
ls public/favicon.ico 2>/dev/null

# If not, generate from SVG icon (if available)
ls app/icon.svg 2>/dev/null && rsvg-convert -w 32 -h 32 app/icon.svg -o public/favicon.ico

# Or create a simple placeholder
# touch public/favicon.ico
```

### Step 7: Populate MCP tools

**This is the most important step.** Edit `lib/mcp-server.ts` and add tools for every API resource.

The golden rule: **every v1 API endpoint should have a corresponding MCP tool**. If a resource supports CRUD via REST, it needs CRUD tools in MCP. When Claude connects via MCP, the tool list is the only way it knows what your app can do. Missing tools = missing capabilities.

**Audit API coverage:**

```bash
# List all v1 API routes
find app/api/v1 -name "route.ts" | sort

# Each route's HTTP methods = tools needed
# GET /api/v1/items → list_items
# GET /api/v1/items/[id] → get_item
# POST /api/v1/items → create_item
# PATCH /api/v1/items/[id] → update_item
# DELETE /api/v1/items/[id] → delete_item
```

**Tool writing pattern:**

```typescript
import { z } from "zod";

// List with optional filters
server.tool("list_items", "List all items, optionally filtered by category", {
  categoryId: z.string().optional().describe("Filter by category ID"),
}, async ({ categoryId }) => {
  const items = await prisma.item.findMany({
    where: { userId, ...(categoryId ? { categoryId } : {}) },
  });
  return { content: [{ type: "text" as const, text: JSON.stringify(items, null, 2) }] };
});

// Get by ID with ownership check
server.tool("get_item", "Get a specific item by ID", {
  id: z.string().describe("Item ID"),
}, async ({ id }) => {
  const item = await prisma.item.findUnique({ where: { id } });
  if (!item || item.userId !== userId) {
    return { content: [{ type: "text" as const, text: "Item not found" }], isError: true };
  }
  return { content: [{ type: "text" as const, text: JSON.stringify(item, null, 2) }] };
});

// Create
server.tool("create_item", "Create a new item", {
  name: z.string().describe("Item name"),
  description: z.string().optional().describe("Item description"),
}, async ({ name, description }) => {
  const item = await prisma.item.create({
    data: { name: name.trim(), userId, ...(description ? { description } : {}) },
  });
  return { content: [{ type: "text" as const, text: JSON.stringify(item, null, 2) }] };
});
```

**Tool description guidelines:**
- Be specific about what the tool does and its constraints
- Mention system rules inline (e.g. "System statuses Done/Deleted cannot be renamed")
- Describe relationships (e.g. "Tasks belong to projects and have a status")
- The AI has no other documentation — the description IS the documentation

### Step 8: Verify MCP route doesn't conflict

Next.js App Router can conflict if a page and route share the same path.

```bash
# Check for conflicts — if app/(marketing)/mcp/page.tsx exists, /mcp route will clash
find app -path "*/mcp/page.*" 2>/dev/null
```

If conflict found, the API route is already at `/api/mcp` so this shouldn't be an issue.

### Step 9: Build and test

```bash
npm run build
```

Test unauthenticated request (should return 401 with WWW-Authenticate):

```bash
curl -s -D - -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -d '{}' 2>&1 | grep -E "HTTP|www-authenticate|Unauthorized"
```

Test with API key (should return SSE with server info):

```bash
curl -X POST http://localhost:3000/api/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-api-key>" \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

Test Dynamic Client Registration:

```bash
curl -X POST http://localhost:3000/oauth/register \
  -H "Content-Type: application/json" \
  -d '{"client_name":"Test","redirect_uris":["https://example.com/callback"]}'
```

## Critical Lessons (from production)

These are not theoretical — each one caused a real deployment failure.

### Use stateless transport

```typescript
const transport = new WebStandardStreamableHTTPServerTransport({
  sessionIdGenerator: undefined, // stateless
});
```

In-memory session maps don't survive across serverless invocations (Vercel, TKE, Lambda). Each request must create a fresh server + transport. The MCP SDK supports this natively — the client handles repeated initialization transparently.

### Use WebStandard transport, not Node.js transport

`StreamableHTTPServerTransport` expects Node.js `IncomingMessage`/`ServerResponse` — incompatible with Next.js App Router which uses Web Standard `Request`/`Response`. Always use `WebStandardStreamableHTTPServerTransport`.

### 401 must include WWW-Authenticate header

```
WWW-Authenticate: Bearer resource_metadata="https://your-app/.well-known/oauth-protected-resource"
```

This header is how MCP clients discover your OAuth endpoints. Without it, Claude.ai shows "Couldn't reach the MCP server" because it can't start the auth flow.

### Dynamic Client Registration is mandatory

MCP clients register themselves before OAuth. Without `/oauth/register` + `registration_endpoint` in metadata:
- Claude.ai shows "Couldn't reach the MCP server"
- The client has no `client_id` to begin authorization

### OAuthClient.userId must be nullable

Registration happens before user authentication. The client record is created with no user association — the user only appears later during the authorization step.

### Tool descriptions are the AI's only documentation

The MCP client reads tool names and descriptions to understand what your app can do. If the description says "Update a status" but doesn't mention that system statuses can't be renamed, the AI will try to rename them and fail. Be explicit about constraints and relationships.

### Ensure /favicon.ico exists

MCP clients fetch it for the connector icon. Without it, you get a generic globe icon instead of your app's branding.

## Connection flow

This is what happens when a user clicks "Connect" in Claude.ai:

```
1. POST /api/mcp (no auth)
   → 401 + WWW-Authenticate header
   
2. GET /.well-known/oauth-protected-resource
   → { resource, authorization_servers }
   
3. GET /.well-known/oauth-authorization-server
   → { endpoints..., registration_endpoint }
   
4. POST /oauth/register
   → { client_id, client_secret }
   
5. Browser opens /oauth/authorize?client_id=...&code_challenge=...
   → User logs in and approves
   → Redirect with ?code=xxx
   
6. POST /oauth/token (exchange code for access token)
   → { access_token, refresh_token }
   
7. POST /api/mcp (with Bearer token)
   → JSON-RPC: initialize → tools/list → tools/call
```

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "Couldn't reach the MCP server" | Missing `/oauth/register` or `registration_endpoint` | Add Dynamic Client Registration (Step 4 + 5) |
| "This connector has no tools available" | Stateful transport lost session state | Switch to stateless mode (sessionIdGenerator: undefined) |
| 401 but client doesn't start OAuth | Missing `WWW-Authenticate` header | Add header to 401 response |
| Tools work locally but not deployed | Used `StreamableHTTPServerTransport` | Use `WebStandardStreamableHTTPServerTransport` |
| Generic globe icon | No `/favicon.ico` | Add favicon to `public/` |
| "no tools" despite tools registered | Route path conflicts with page | Move to `/api/mcp` to avoid conflict |
| Build error: type mismatch | SDK expects Node.js types | Use WebStandard variant of transport |
