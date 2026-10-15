---
name: convex-http-actions
displayName: Convex HTTP Actions
description: External API integration and webhook handling including HTTP endpoint routing, request/response handling, authentication, CORS configuration, and webhook signature validation
version: 1.0.0
author: Convex
tags: [convex, http, actions, webhooks, api, endpoints]
---

# Convex HTTP Actions

Build HTTP endpoints for webhooks, external API integrations, and custom routes in Convex applications.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/functions/http-actions
- Actions Overview: https://docs.convex.dev/functions/actions
- Authentication: https://docs.convex.dev/auth
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### HTTP Actions Overview

HTTP actions allow you to define HTTP endpoints in Convex that can:

- Receive webhooks from third-party services
- Create custom API routes
- Handle file uploads
- Integrate with external services
- Serve dynamic content

### Basic HTTP Router Setup

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// Simple GET endpoint
http.route({
  path: "/health",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    return new Response(JSON.stringify({ status: "ok" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }),
});

export default http;
```

## Code Patterns

Full code samples live in the reference file. Read it before writing the matching code.

Sections in `references/patterns.md`:

- Request Handling
- Path Parameters
- CORS Configuration
- Webhook Handling
- Webhook Signature Verification
- Authentication in HTTP Actions
- Calling Mutations and Queries
- Error Handling
- File Downloads
- Complete Webhook Integration
- Schema for HTTP API

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Always validate and sanitize incoming request data
- Use internal functions for database operations
- Implement proper error handling with appropriate status codes
- Add CORS headers for browser-accessible endpoints
- Verify webhook signatures before processing
- Log webhook events for debugging
- Use environment variables for secrets
- Handle timeouts gracefully

## Common Pitfalls

1. **Missing CORS preflight handler** - Browsers send OPTIONS requests first
2. **Not validating webhook signatures** - Security vulnerability
3. **Exposing internal functions** - Use internal functions from HTTP actions
4. **Forgetting Content-Type headers** - Clients may not parse responses correctly
5. **Not handling request body errors** - Invalid JSON will throw
6. **Blocking on long operations** - Use scheduled functions for heavy processing

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- HTTP Actions: https://docs.convex.dev/functions/http-actions
- Actions: https://docs.convex.dev/functions/actions
- Authentication: https://docs.convex.dev/auth
