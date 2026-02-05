---
name: workers-binding-validator
description: Automatically validates Cloudflare Workers binding configuration, ensuring code references match wrangler.toml setup and TypeScript interfaces are accurate
triggers: ["env parameter usage", "wrangler.toml changes", "TypeScript interface updates", "binding references"]
---

# Workers Binding Validator SKILL

## Activation Patterns

This SKILL automatically activates when:
- `env` parameter is used in Workers code
- wrangler.toml file is modified
- TypeScript `Env` interface is defined or updated
- New binding references are added to code
- Binding configuration patterns are detected

## Expertise Provided

### Binding Configuration Validation
- **Binding Consistency**: Ensures code references match wrangler.toml configuration
- **TypeScript Interface Validation**: Validates `Env` interface matches actual bindings
- **Binding Type Accuracy**: Ensures correct binding types (KV, R2, D1, Durable Objects)
- **Remote Binding Validation**: Checks remote binding configuration for development
- **Secret Binding Verification**: Validates secret vs environment variable bindings

### Specific Checks Performed

#### ❌ Critical Binding Mismatches
```typescript
// These patterns trigger immediate alerts:
// Code references binding that doesn't exist in wrangler.toml
const user = await env.USER_DATA.get(id);  // USER_DATA not configured

// TypeScript interface doesn't match wrangler.toml
interface Env {
  USERS: KVNamespace;     // Code expects USERS
  // wrangler.toml has USER_DATA (mismatch!)
}
```

#### ✅ Correct Binding Patterns
```typescript
// These patterns are validated as correct:
// Matching wrangler.toml and TypeScript interface
interface Env {
  USER_DATA: KVNamespace;  // Matches wrangler.toml binding name
  API_BUCKET: R2Bucket;    // Correct R2 binding type
}

// Proper usage in code
const user = await env.USER_DATA.get(id);
const object = await env.API_BUCKET.get(key);
```

## Integration Points

### Complementary to Existing Components
- **binding-context-analyzer agent**: Handles complex binding analysis, SKILL provides immediate validation
- **workers-runtime-validator SKILL**: Complements runtime checks with binding validation
- **cloudflare-security-checker SKILL**: Ensures secret bindings are properly configured

### Escalation Triggers
- Complex binding architecture questions → `binding-context-analyzer` agent
- Migration between binding types → `cloudflare-architecture-strategist` agent
- Binding performance issues → `edge-performance-oracle` agent

## Validation Rules

### P1 - Critical (Will Fail at Runtime)
- **Missing Bindings**: Code references bindings not in wrangler.toml
- **Type Mismatches**: Wrong binding types in TypeScript interface
- **Name Mismatches**: Different names in code vs configuration
- **Missing Env Interface**: No TypeScript interface for bindings

### P2 - High (Configuration Issues)
- **Remote Binding Missing**: Development bindings without `remote = true`
- **Secret vs Var Confusion**: Secrets in [vars] section or vice versa
- **Incomplete Interface**: Missing bindings in TypeScript interface

### P3 - Medium (Best Practices)
- **Binding Documentation**: Missing JSDoc comments for bindings
- **Binding Organization**: Poor organization of related bindings

## Remediation Examples

### Fixing Missing Bindings
```typescript
// ❌ Critical: Code references binding not in wrangler.toml
export default {
  async fetch(request: Request, env: Env) {
    const user = await env.USER_CACHE.get(userId); // USER_CACHE not configured!
  }
}

// wrangler.toml (missing binding)
[[kv_namespaces]]
binding = "USER_DATA"  # Different name!
id = "user-data"

// ✅ Correct: Matching names
export default {
  async fetch(request: Request, env: Env) {
    const user = await env.USER_DATA.get(userId); // Matches wrangler.toml
  }
}

// wrangler.toml (correct binding)
[[kv_namespaces]]
binding = "USER_DATA"  # Matches code!
id = "user-data"
```

### Fixing TypeScript Interface Mismatches
```typescript
// ❌ Critical: Interface doesn't match wrangler.toml
interface Env {
  USERS: KVNamespace;      // Code expects USERS
  SESSIONS: KVNamespace;    // Code expects SESSIONS
}

// wrangler.toml has different names
[[kv_namespaces]]
binding = "USER_DATA"      # Different!
id = "user-data"

[[kv_namespaces]]
binding = "SESSION_DATA"    # Different!
id = "session-data"

// ✅ Correct: Matching interface and configuration
interface Env {
  USER_DATA: KVNamespace;   # Matches wrangler.toml
  SESSION_DATA: KVNamespace; # Matches wrangler.toml
}

// wrangler.toml (matching names)
[[kv_namespaces]]
binding = "USER_DATA"       # Matches interface!
id = "user-data"

[[kv_namespaces]]
binding = "SESSION_DATA"     # Matches interface!
id = "session-data"
```

### Fixing Binding Type Mismatches
```typescript
// ❌ Critical: Wrong binding type
interface Env {
  MY_BUCKET: KVNamespace;    # Wrong type - should be R2Bucket
  MY_DB: D1Database;        # Wrong type - should be KVNamespace
}

// wrangler.toml
[[r2_buckets]]
binding = "MY_BUCKET"       # R2 bucket, not KV!

[[kv_namespaces]]
binding = "MY_DB"           # KV namespace, not D1!

// ✅ Correct: Proper binding types
interface Env {
  MY_BUCKET: R2Bucket;      # Correct type for R2 bucket
  MY_DB: KVNamespace;       # Correct type for KV namespace
}

// wrangler.toml (same as above)
[[r2_buckets]]
binding = "MY_BUCKET"

[[kv_namespaces]]
binding = "MY_DB"
```

### Fixing Remote Binding Configuration
```typescript
// ❌ High: Missing remote binding for development
// wrangler.toml
[[kv_namespaces]]
binding = "USER_DATA"
id = "user-data"
# Missing remote = true for development!

// ✅ Correct: Remote binding configured
[[kv_namespaces]]
binding = "USER_DATA"
id = "user-data"
remote = true  # Enables remote binding for development
```

### Fixing Secret vs Environment Variable Confusion
```typescript
// ❌ High: Secret in [vars] section (visible in git)
// wrangler.toml
[vars]
API_KEY = "sk_live_12345"  # Secret exposed in git!

// ✅ Correct: Secret via wrangler secret command
// wrangler.toml (no secrets in [vars])
[vars]
PUBLIC_API_URL = "https://api.example.com"  # Non-secret config only

# Set secret via command line:
# wrangler secret put API_KEY
# (prompt: enter secret value)

// Code accesses both correctly
interface Env {
  API_KEY: string;           # From wrangler secret
  PUBLIC_API_URL: string;    # From wrangler.toml [vars]
}
```

## MCP Server Integration

When Cloudflare MCP server is available:
- Query actual binding configuration from Cloudflare account
- Verify bindings exist and are accessible
- Check binding permissions and limits
- Get latest binding configuration best practices

## Benefits

### Immediate Impact
- **Prevents Runtime Failures**: Catches binding mismatches before deployment
- **Reduces Debugging Time**: Immediate feedback on configuration issues
- **Ensures Type Safety**: Validates TypeScript interfaces match reality

### Long-term Value
- **Consistent Configuration**: Ensures all code uses correct binding patterns
- **Better Developer Experience**: Clear error messages for binding issues
- **Reduced Deployment Issues**: Configuration validation prevents failed deployments

## Usage Examples

### During Binding Usage
```typescript
// Developer types: const data = await env.CACHE.get(key);
// SKILL immediately activates: "❌ CRITICAL: CACHE binding not found in wrangler.toml. Add [[kv_namespaces]] binding = 'CACHE' or check spelling."
```

### During Interface Definition
```typescript
// Developer types: interface Env { USERS: R2Bucket; }
// SKILL immediately activates: "⚠️ HIGH: USERS binding type mismatch. wrangler.toml shows USERS as KVNamespace, not R2Bucket."
```

### During Configuration Changes
```typescript
// Developer modifies wrangler.toml binding name
// SKILL immediately activates: "⚠️ HIGH: Binding name changed from USER_DATA to USERS. Update TypeScript interface and code references."
```

## Binding Type Reference

### KV Namespace
```typescript
interface Env {
  MY_KV: KVNamespace;
}
// Usage: await env.MY_KV.get(key)
```

### R2 Bucket
```typescript
interface Env {
  MY_BUCKET: R2Bucket;
}
// Usage: await env.MY_BUCKET.get(key)
```

### D1 Database
```typescript
interface Env {
  MY_DB: D1Database;
}
// Usage: await env.MY_DB.prepare(query).bind(params).all()
```

### Durable Object
```typescript
interface Env {
  MY_DO: DurableObjectNamespace;
}
// Usage: env.MY_DO.get(id)
```

### AI Binding
```typescript
interface Env {
  AI: Ai;
}
// Usage: await env.AI.run(model, params)
```

### Vectorize
```typescript
interface Env {
  VECTORS: VectorizeIndex;
}
// Usage: await env.VECTORS.query(vector, options)
```

This SKILL ensures Workers binding configuration is correct by providing immediate, autonomous validation of binding patterns, preventing runtime failures and configuration mismatches.