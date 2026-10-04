---
license: Apache-2.0
name: mcp-creator
description: Expert MCP (Model Context Protocol) server developer creating safe, performant, production-ready servers with proper security, error handling, and developer experience. Activate on 'create MCP', 'MCP server', 'build MCP', 'custom tool server', 'MCP development', 'Model Context Protocol'. NOT for using existing MCPs (just invoke them), general API development (use backend-architect), or skills/agents without external state (use skill-coach/agent-creator).
allowed-tools: Read,Write,Edit,Bash,Grep,Glob,WebSearch,WebFetch
category: Agent & Orchestration
tags:
  - mcp
  - model-context-protocol
  - tools
  - integration
  - creation
pairs-with:
  - skill: agent-creator
    reason: Skills that use the MCP tools
  - skill: security-auditor
    reason: Secure MCP server development
---

# MCP Creator

Expert in building production-ready Model Context Protocol servers with security boundaries, robust error handling, and excellent developer experience.

## Decision Points

### Tool Granularity Decision Tree
```
Tool complexity assessment:
├── Multiple API endpoints needed?
    ├── Yes → Design separate tools for each endpoint
    │   └── Example: get_user, create_user, update_user
    └── No → Single tool with action parameter
        └── Example: manage_user(action: "get"|"create"|"update")

Tool execution pattern:
├── Operation takes >5 seconds?
    ├── Yes → Design as async with polling tool
    │   └── start_analysis() → check_status() → get_results()
    └── No → Direct synchronous tool
        └── analyze_data() returns results immediately

External service interaction:
├── Requires authentication?
    ├── Yes → Bundle related operations in one MCP
    │   └── Share auth config across tools
    └── No → Consider standalone tools or scripts
```

### Resource vs Tools Decision Matrix
```
Data access pattern:
├── Read-only structured data? → Use Resources
│   └── Templates, configs, documentation
├── Actions that modify state? → Use Tools
│   └── API calls, database writes, file creation
└── Interactive operations? → Use Tools with prompts
    └── Guided workflows, form filling
```

### Transport Layer Decision
```
Deployment context:
├── Local CLI integration?
    └── Use StdioTransport (simplest, most secure)
├── Multiple client support needed?
    └── Use SSE Transport (HTTP-based)
├── Custom protocol requirements?
    └── Implement custom Transport class
└── Production server deployment?
    └── SSE with proper auth middleware
```

## Failure Modes

### Schema Bloat
**Symptom**: Tools accept `any` type or overly permissive schemas
**Detection**: If schema validation catches <90% of invalid inputs
**Fix**: Implement strict Zod schemas with constraints
```typescript
// ❌ Detection rule: Schema too permissive
{ type: "object" }

// ✅ Fix: Strict validation
const schema = z.object({
  id: z.string().uuid(),
  count: z.number().min(1).max(100)
})
```

### Connection Leaks
**Symptom**: Server becomes unresponsive after extended use
**Detection**: If connection pools show >90% utilization or memory usage grows continuously
**Fix**: Implement proper resource cleanup with try/finally blocks
```typescript
// ❌ Detection: No cleanup
const client = await pool.connect();
const result = await client.query(sql);

// ✅ Fix: Guaranteed cleanup
const client = await pool.connect();
try {
  return await client.query(sql);
} finally {
  client.release();
}
```

### Secret Exposure
**Symptom**: API keys visible in logs, error messages, or responses
**Detection**: If grep finds credentials in logs or error responses
**Fix**: Sanitize all outputs and use secure environment variable loading
```typescript
// ❌ Detection rule: Secrets in error messages
throw new Error(`API call failed with key ${apiKey}`);

// ✅ Fix: Sanitized errors
throw new Error(`API call failed: ${error.message.replace(apiKey, '[REDACTED]')}`);
```

### Rate Limit Cascade
**Symptom**: External API returns 429 errors, causing tool failures
**Detection**: If >10% of external API calls return rate limit errors
**Fix**: Implement exponential backoff and circuit breaker pattern
```typescript
// ❌ Detection: No rate limiting
await fetch(url, { headers: { 'Authorization': `Bearer ${token}` } });

// ✅ Fix: Rate limiting with backoff
if (!rateLimiter.canProceed(url, 100, 60000)) {
  await exponentialBackoff(() => fetch(url, options));
}
```

### Error Swallowing
**Symptom**: Tools succeed but produce incorrect or incomplete results
**Detection**: If tool success rate is >95% but user reports failures
**Fix**: Implement structured error handling with proper propagation
```typescript
// ❌ Detection rule: Silent failures
try {
  await riskyOperation();
} catch (e) {
  // Silent failure
}

// ✅ Fix: Proper error handling
try {
  return await riskyOperation();
} catch (error) {
  throw new McpError(ErrorCode.InternalError, `Operation failed: ${error.message}`);
}
```

## Worked Example: Database Query Tool

**Scenario**: Create an MCP tool for querying a PostgreSQL database with user data.

**Step 1 - Tool Design Decision**
Looking at requirements: multiple query types (get user, list users, search users). Following the decision tree:
- Multiple endpoints? Yes → Design separate tools
- But all share auth/connection? Yes → Bundle in one MCP

Decision: Create `database-mcp` with tools: `get_user`, `list_users`, `search_users`

**Step 2 - Security Schema Design**
```typescript
const getUserSchema = z.object({
  userId: z.string().uuid(), // Prevent SQL injection
  includeDeleted: z.boolean().default(false)
});
```
Novice mistake: Using `z.string()` without validation → allows SQL injection
Expert addition: UUID validation prevents malicious input

**Step 3 - Connection Management**
```typescript
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10, // Connection limit
  idleTimeoutMillis: 30000
});
```
Novice mistake: Creating new connection per request → resource exhaustion
Expert pattern: Connection pooling with limits

**Step 4 - Error Handling Strategy**
```typescript
async function getUser(args: unknown) {
  const { userId, includeDeleted } = getUserSchema.parse(args);
  
  const client = await pool.connect();
  try {
    const query = includeDeleted 
      ? 'SELECT * FROM users WHERE id = $1'
      : 'SELECT * FROM users WHERE id = $1 AND deleted_at IS NULL';
    
    const result = await client.query(query, [userId]);
    
    if (result.rows.length === 0) {
      return { content: [{ type: "text", text: JSON.stringify({ found: false }) }] };
    }
    
    return { content: [{ type: "text", text: JSON.stringify({ 
      found: true, 
      user: result.rows[0] 
    }) }] };
    
  } catch (error) {
    throw new McpError(ErrorCode.InternalError, `Database query failed`);
  } finally {
    client.release(); // Always cleanup
  }
}
```

Novice mistake: No connection cleanup → connection leaks
Expert pattern: try/finally ensures cleanup even on error

## Quality Gates

- [ ] All tool inputs validated with Zod schemas including format constraints
- [ ] No hardcoded secrets (grep -r "sk-\|api[_-]?key\|token" returns empty)
- [ ] All database/HTTP connections properly pooled and cleaned up in finally blocks
- [ ] Rate limiting implemented with configurable limits (default: 100 req/min)
- [ ] Error responses never expose stack traces or sensitive data in production
- [ ] All async operations have explicit timeouts (default: 30s max)
- [ ] Tool responses follow consistent JSON structure with success/error indicators
- [ ] External API calls implement retry logic with exponential backoff
- [ ] Security audit passes: no SQL injection vectors, XSS prevention, CSRF protection
- [ ] Performance benchmarks: P95 latency <500ms, error rate <1%, connection pool utilization <80%

## NOT-FOR Boundaries

**Do NOT use MCP Creator for:**
- **Pure domain knowledge without external state** → Use `skill-coach` instead
- **Multi-step agent orchestration** → Use `agent-creator` instead  
- **Simple file processing without APIs** → Use Claude's built-in file tools
- **Local scripts without authentication** → Use `script-writer` instead
- **General web API development** → Use `backend-architect` instead
- **Using existing MCP servers** → Just invoke them directly, no creation needed

**Delegate to other skills when:**
- Security review needed → Hand off to `security-auditor`
- Infrastructure deployment → Hand off to `site-reliability-engineer` 
- The MCP will be used by agents → Collaborate with `agent-creator` for integration