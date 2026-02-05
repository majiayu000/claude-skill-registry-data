---
name: workers-runtime-validator
description: Automatically validates Cloudflare Workers runtime compatibility during development, preventing Node.js API usage and ensuring proper Workers patterns
triggers: ["import statements", "file creation", "code changes", "deployment preparation"]
---

# Workers Runtime Validator SKILL

## Activation Patterns

This SKILL automatically activates when:
- New `.ts` or `.js` files are created in Workers projects
- Import statements are added or modified
- Code changes include potential runtime violations
- Before deployment commands are executed
- When `process.env`, `require()`, or Node.js APIs are detected

## Expertise Provided

### Runtime Compatibility Validation
- **Forbidden API Detection**: Identifies Node.js built-ins that don't exist in Workers
- **Environment Access**: Ensures proper `env` parameter usage vs `process.env`
- **Module System**: Validates ES modules usage (no `require()`)
- **Async Patterns**: Ensures all I/O operations are async
- **Package Compatibility**: Checks npm packages for Node.js dependencies

### Specific Checks Performed

#### ❌ Critical Violations (Will Break in Production)
```typescript
// These patterns trigger immediate alerts:
import fs from 'fs';                    // Node.js API
import { Buffer } from 'buffer';        // Node.js API
const secret = process.env.API_KEY;     // process doesn't exist
const data = require('./module');        // require() not supported
```

#### ✅ Correct Workers Patterns
```typescript
// These patterns are validated as correct:
import { z } from 'zod';                // Web-compatible package
const secret = env.API_KEY;             // Proper env parameter
const hash = await crypto.subtle.digest(); // Web Crypto API
```

## Integration Points

### Complementary to Existing Components
- **workers-runtime-guardian agent**: Handles deep runtime analysis, SKILL provides immediate validation
- **es-deploy command**: SKILL prevents deployment failures by catching issues early
- **validate command**: SKILL provides continuous validation between explicit checks

### Escalation Triggers
- Complex runtime compatibility questions → `workers-runtime-guardian` agent
- Package dependency analysis → `edge-performance-oracle` agent
- Migration from Node.js to Workers → `cloudflare-architecture-strategist` agent

## Validation Rules

### P1 - Critical (Must Fix Immediately)
- **Node.js Built-ins**: `fs`, `path`, `os`, `crypto`, `process`, `buffer`
- **CommonJS Usage**: `require()`, `module.exports`
- **Process Access**: `process.env`, `process.exit()`
- **Synchronous I/O**: Any blocking I/O operations

### P2 - Important (Should Fix)
- **Package Dependencies**: npm packages with Node.js dependencies
- **Missing Async**: I/O operations without await
- **Buffer Usage**: Using Node.js Buffer instead of Uint8Array

### P3 - Best Practices
- **TypeScript Env Interface**: Missing or incorrect Env type definition
- **Web API Usage**: Not using modern Web APIs when available

## Remediation Examples

### Fixing Node.js API Usage
```typescript
// ❌ Critical: Node.js crypto
import crypto from 'crypto';
const hash = crypto.createHash('sha256');

// ✅ Correct: Web Crypto API
const encoder = new TextEncoder();
const hash = await crypto.subtle.digest('SHA-256', encoder.encode(data));
```

### Fixing Environment Access
```typescript
// ❌ Critical: process.env
const apiKey = process.env.API_KEY;

// ✅ Correct: env parameter
export default {
  async fetch(request: Request, env: Env) {
    const apiKey = env.API_KEY;
  }
}
```

### Fixing Module System
```typescript
// ❌ Critical: CommonJS
const utils = require('./utils');

// ✅ Correct: ES modules
import { utils } from './utils';
```

## MCP Server Integration

When Cloudflare MCP server is available:
- Query latest Workers runtime API documentation
- Check for deprecated APIs before suggesting fixes
- Get current compatibility information for new features

## Benefits

### Immediate Impact
- **Prevents Runtime Failures**: Catches issues before deployment
- **Reduces Debugging Time**: Immediate feedback on violations
- **Educates Developers**: Clear explanations of Workers vs Node.js differences

### Long-term Value
- **Consistent Code Quality**: Ensures all code follows Workers patterns
- **Faster Development**: No need to wait for deployment to discover issues
- **Better Developer Experience**: Real-time guidance during coding

## Usage Examples

### During Code Creation
```typescript
// Developer types: import fs from 'fs';
// SKILL immediately activates: "❌ CRITICAL: 'fs' is a Node.js API not available in Workers runtime. Use Web APIs or Workers-specific alternatives."
```

### During Refactoring
```typescript
// Developer changes: const secret = process.env.API_KEY;
// SKILL immediately activates: "❌ CRITICAL: 'process.env' doesn't exist in Workers. Use the 'env' parameter passed to your fetch handler instead."
```

### Before Deployment
```typescript
// SKILL runs comprehensive check: "✅ Runtime validation passed. No Node.js APIs detected, all environment access uses proper env parameter."
```

This SKILL ensures Workers runtime compatibility by providing immediate, autonomous validation of code patterns, preventing common migration mistakes and runtime failures.