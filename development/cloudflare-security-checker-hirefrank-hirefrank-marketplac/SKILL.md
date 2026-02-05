---
name: cloudflare-security-checker
description: Automatically validates Cloudflare Workers security patterns during development, ensuring proper secret management, CORS configuration, and input validation
triggers: ["authentication code", "secret handling", "API endpoints", "response creation", "database queries"]
---

# Cloudflare Security Checker SKILL

## Activation Patterns

This SKILL automatically activates when:
- Authentication or authorization code is detected
- Secret management patterns are used
- API endpoints or response creation is implemented
- Database queries (D1) are written
- CORS-related code is added
- Input validation patterns are implemented

## Expertise Provided

### Workers-Specific Security Validation
- **Secret Management**: Ensures proper `env` parameter usage vs hardcoded secrets
- **CORS Configuration**: Validates Workers-specific CORS implementation
- **Input Validation**: Checks for proper request validation patterns
- **SQL Injection Prevention**: Ensures D1 prepared statements
- **Authentication Patterns**: Validates JWT and API key handling
- **Rate Limiting**: Identifies missing rate limiting patterns

### Specific Checks Performed

#### ❌ Critical Security Violations
```typescript
// These patterns trigger immediate alerts:
const API_KEY = "sk_live_xxx";           // Hardcoded secret
const secret = process.env.JWT_SECRET;     // process.env doesn't exist
const query = `SELECT * FROM users WHERE id = ${userId}`; // SQL injection
```

#### ✅ Secure Workers Patterns
```typescript
// These patterns are validated as correct:
const apiKey = env.API_KEY;               // Proper env parameter
const result = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(userId); // Prepared statement
```

## Integration Points

### Complementary to Existing Components
- **cloudflare-security-sentinel agent**: Handles comprehensive security audits, SKILL provides immediate validation
- **workers-runtime-validator SKILL**: Complements runtime checks with security-specific validation
- **es-deploy command**: SKILL prevents deployment of insecure code

### Escalation Triggers
- Complex security architecture questions → `cloudflare-security-sentinel` agent
- Advanced authentication patterns → `cloudflare-architecture-strategist` agent
- Security incident response → `cloudflare-security-sentinel` agent

## Validation Rules

### P1 - Critical (Immediate Security Risk)
- **Hardcoded Secrets**: API keys, passwords, tokens in code
- **SQL Injection**: String concatenation in D1 queries
- **Missing Authentication**: Sensitive endpoints without auth
- **Process Env Usage**: `process.env` for secrets (doesn't work in Workers)

### P2 - High (Security Vulnerability)
- **Missing Input Validation**: Direct use of `request.json()` without validation
- **Improper CORS**: Missing CORS headers or overly permissive origins
- **Missing Rate Limiting**: Public endpoints without rate limiting
- **Secrets in Config**: Secrets in wrangler.toml `[vars]` section

### P3 - Medium (Security Best Practice)
- **Missing Security Headers**: HTML responses without CSP/XSS protection
- **Weak Authentication**: No resource-level authorization
- **Insufficient Logging**: Security events not logged

## Remediation Examples

### Fixing Secret Management
```typescript
// ❌ Critical: Hardcoded secret
const STRIPE_KEY = "sk_live_12345";

// ❌ Critical: process.env (doesn't exist)
const apiKey = process.env.API_KEY;

// ✅ Correct: Workers secret management
export default {
  async fetch(request: Request, env: Env) {
    const apiKey = env.STRIPE_KEY; // From wrangler secret put
  }
}
```

### Fixing SQL Injection
```typescript
// ❌ Critical: SQL injection vulnerability
const userId = url.searchParams.get('id');
const result = await env.DB.prepare(`SELECT * FROM users WHERE id = ${userId}`).first();

// ✅ Correct: Prepared statement
const userId = url.searchParams.get('id');
const result = await env.DB.prepare('SELECT * FROM users WHERE id = ?').bind(userId).first();
```

### Fixing CORS Configuration
```typescript
// ❌ High: Missing CORS headers
export default {
  async fetch(request: Request, env: Env) {
    return new Response(JSON.stringify(data));
  }
}

// ✅ Correct: Workers CORS pattern
function getCorsHeaders(origin: string) {
  const allowedOrigins = ['https://app.example.com'];
  const allowOrigin = allowedOrigins.includes(origin) ? origin : allowedOrigins[0];
  
  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
  };
}

export default {
  async fetch(request: Request, env: Env) {
    const origin = request.headers.get('Origin') || '';
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: getCorsHeaders(origin) });
    }
    
    const response = new Response(JSON.stringify(data));
    Object.entries(getCorsHeaders(origin)).forEach(([k, v]) => {
      response.headers.set(k, v);
    });
    
    return response;
  }
}
```

### Fixing Input Validation
```typescript
// ❌ High: No input validation
export default {
  async fetch(request: Request, env: Env) {
    const data = await request.json(); // Could be anything
    await env.DB.prepare('INSERT INTO users (name) VALUES (?)').bind(data.name).run();
  }
}

// ✅ Correct: Input validation with Zod
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
});

export default {
  async fetch(request: Request, env: Env) {
    // Size limit
    const contentLength = request.headers.get('Content-Length');
    if (contentLength && parseInt(contentLength) > 1024 * 100) {
      return new Response('Payload too large', { status: 413 });
    }
    
    // Schema validation
    const data = await request.json();
    const result = UserSchema.safeParse(data);
    
    if (!result.success) {
      return new Response(JSON.stringify(result.error), { status: 400 });
    }
    
    // Safe to use validated data
    await env.DB.prepare('INSERT INTO users (name, email) VALUES (?, ?)')
      .bind(result.data.name, result.data.email).run();
  }
}
```

## MCP Server Integration

When Cloudflare MCP server is available:
- Query latest Cloudflare security best practices
- Verify secrets are configured in account
- Check for recent security events affecting the project
- Get current security recommendations

## Benefits

### Immediate Impact
- **Prevents Security Vulnerabilities**: Catches issues during development
- **Educates on Workers Security**: Clear explanations of Workers-specific security patterns
- **Reduces Security Debt**: Immediate feedback on security anti-patterns

### Long-term Value
- **Consistent Security Standards**: Ensures all code follows Workers security best practices
- **Faster Security Reviews**: Automated validation reduces manual review time
- **Better Security Posture**: Proactive security validation vs reactive fixes

## Usage Examples

### During Authentication Implementation
```typescript
// Developer types: const JWT_SECRET = "my-secret-key";
// SKILL immediately activates: "❌ CRITICAL: Hardcoded JWT secret detected. Use wrangler secret put JWT_SECRET and access via env.JWT_SECRET"
```

### During API Development
```typescript
// Developer types: const userId = url.searchParams.get('id');
// SKILL immediately activates: "⚠️ HIGH: URL parameter not validated. Add schema validation before using in database queries."
```

### During Database Query Writing
```typescript
// Developer types: `SELECT * FROM users WHERE id = ${userId}`
// SKILL immediately activates: "❌ CRITICAL: SQL injection vulnerability. Use prepared statement: .prepare('SELECT * FROM users WHERE id = ?').bind(userId)"
```

This SKILL ensures Workers security by providing immediate, autonomous validation of security patterns, preventing common vulnerabilities and ensuring proper Workers-specific security practices.