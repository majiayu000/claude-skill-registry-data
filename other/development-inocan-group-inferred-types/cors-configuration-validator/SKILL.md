---
name: cors-configuration-validator
description: Automatically validates Cloudflare Workers CORS configuration, ensuring proper headers, OPTIONS handling, and origin validation for cross-origin requests
triggers: ["Response creation", "API endpoints", "cross-origin patterns", "CORS headers"]
---

# CORS Configuration Validator SKILL

## Activation Patterns

This SKILL automatically activates when:
- `new Response()` objects are created
- CORS-related headers are set or modified
- API endpoints that serve cross-origin requests
- OPTIONS method handling is detected
- Cross-origin request patterns are identified

## Expertise Provided

### Workers-Specific CORS Validation
- **Header Validation**: Ensures all required CORS headers are present
- **OPTIONS Handling**: Validates preflight request handling
- **Origin Validation**: Checks for proper origin validation logic
- **Method Validation**: Ensures correct allowed methods
- **Header Validation**: Validates allowed headers configuration
- **Security**: Prevents overly permissive CORS configurations

### Specific Checks Performed

#### ❌ CORS Anti-Patterns
```typescript
// These patterns trigger immediate alerts:
// Missing CORS headers
export default {
  async fetch(request: Request, env: Env) {
    return new Response(JSON.stringify(data));
    // Browsers will block cross-origin requests!
  }
}

// Overly permissive for authenticated APIs
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',  // ANY origin can call!
  'Access-Control-Allow-Credentials': 'true'  // With credentials!
};
```

#### ✅ CORS Best Practices
```typescript
// These patterns are validated as correct:
// Proper CORS with origin validation
function getCorsHeaders(origin: string) {
  const allowedOrigins = ['https://app.example.com', 'https://example.com'];
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

## Integration Points

### Complementary to Existing Components
- **cloudflare-security-checker SKILL**: Handles overall security, SKILL focuses specifically on CORS
- **workers-runtime-validator SKILL**: Ensures runtime compatibility, SKILL validates CORS patterns
- **edge-performance-oracle SKILL**: Handles performance, SKILL ensures CORS doesn't impact performance

### Escalation Triggers
- Complex CORS architecture questions → `cloudflare-security-sentinel` agent
- Advanced authentication with CORS → `cloudflare-security-sentinel` agent
- CORS troubleshooting → `cloudflare-security-sentinel` agent

## Validation Rules

### P1 - Critical (Will Break Cross-Origin Requests)
- **Missing CORS Headers**: No CORS headers on API responses
- **Missing OPTIONS Handler**: No preflight request handling
- **Invalid Header Combinations**: Conflicting CORS header combinations

### P2 - High (Security Risk)
- **Overly Permissive Origin**: `Access-Control-Allow-Origin: *` with credentials
- **Wildcard Methods**: `Access-Control-Allow-Methods: *` with sensitive operations
- **Missing Origin Validation**: Accepting any origin without validation

### P3 - Medium (Best Practices)
- **Missing Cache Headers**: No `Access-Control-Max-Age` for preflight caching
- **Incomplete Headers**: Missing some optional but recommended headers
- **Hardcoded Origins**: Origins not easily configurable

## Remediation Examples

### Fixing Missing CORS Headers
```typescript
// ❌ Critical: No CORS headers (browsers block requests)
export default {
  async fetch(request: Request, env: Env) {
    const data = { message: 'Hello from API' };
    
    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' }
      // Missing CORS headers!
    });
  }
}

// ✅ Correct: Complete CORS implementation
function getCorsHeaders(origin: string) {
  const allowedOrigins = ['https://app.example.com', 'https://example.com'];
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
    
    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: getCorsHeaders(origin) });
    }
    
    const data = { message: 'Hello from API' };
    
    return new Response(JSON.stringify(data), {
      headers: {
        'Content-Type': 'application/json',
        ...getCorsHeaders(origin)
      }
    });
  }
}
```

### Fixing Overly Permissive CORS
```typescript
// ❌ High: Overly permissive for authenticated API
export default {
  async fetch(request: Request, env: Env) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',  // ANY origin!
      'Access-Control-Allow-Credentials': 'true',  // With credentials!
      'Access-Control-Allow-Methods': '*',  // ANY method!
    };
    
    // This allows any website to make authenticated requests!
    return new Response('Sensitive data', { headers: corsHeaders });
  }
}

// ✅ Correct: Secure CORS for authenticated API
function getSecureCorsHeaders(origin: string) {
  const allowedOrigins = [
    'https://app.example.com',
    'https://admin.example.com',
    'https://example.com'
  ];
  
  // Only allow known origins
  const allowOrigin = allowedOrigins.includes(origin) ? origin : allowedOrigins[0];
  
  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',  // Specific methods
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Max-Age': '86400',
  };
}

export default {
  async fetch(request: Request, env: Env) {
    const origin = request.headers.get('Origin') || '';
    
    // Verify authentication
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !isValidAuth(authHeader)) {
      return new Response('Unauthorized', { status: 401 });
    }
    
    return new Response('Sensitive data', {
      headers: getSecureCorsHeaders(origin)
    });
  }
}
```

### Fixing Missing OPTIONS Handler
```typescript
// ❌ Critical: No OPTIONS handling (preflight fails)
export default {
  async fetch(request: Request, env: Env) {
    if (request.method === 'POST') {
      // Handle POST request
      return new Response('POST handled');
    }
    
    return new Response('Method not allowed', { status: 405 });
  }
}

// ✅ Correct: Proper OPTIONS handling
export default {
  async fetch(request: Request, env: Env) {
    const origin = request.headers.get('Origin') || '';
    
    // Handle preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': origin,
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Max-Age': '86400',
        }
      });
    }
    
    if (request.method === 'POST') {
      return new Response('POST handled', {
        headers: {
          'Access-Control-Allow-Origin': origin,
        }
      });
    }
    
    return new Response('Method not allowed', { status: 405 });
  }
}
```

### Fixing Dynamic CORS for Different Environments
```typescript
// ❌ Medium: Hardcoded origins (not flexible)
function getCorsHeaders() {
  return {
    'Access-Control-Allow-Origin': 'https://app.example.com',  // Hardcoded
    'Access-Control-Allow-Methods': 'GET, POST',
  };
}

// ✅ Correct: Configurable and secure CORS
function getCorsHeaders(origin: string, env: Env) {
  // Get allowed origins from environment
  const allowedOrigins = (env.ALLOWED_ORIGINS || 'https://app.example.com')
    .split(',')
    .map(o => o.trim());
  
  const allowOrigin = allowedOrigins.includes(origin) ? origin : allowedOrigins[0];
  
  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Methods': env.ALLOWED_METHODS || 'GET, POST, PUT, DELETE',
    'Access-Control-Allow-Headers': env.ALLOWED_HEADERS || 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
  };
}

export default {
  async fetch(request: Request, env: Env) {
    const origin = request.headers.get('Origin') || '';
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: getCorsHeaders(origin, env) });
    }
    
    return new Response('Response', {
      headers: getCorsHeaders(origin, env)
    });
  }
}
```

## CORS Header Reference

### Essential Headers
```typescript
{
  'Access-Control-Allow-Origin': 'https://example.com',  // Required
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',  // Required for preflight
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',  // Required for preflight
}
```

### Optional but Recommended Headers
```typescript
{
  'Access-Control-Max-Age': '86400',  // Cache preflight for 24 hours
  'Access-Control-Allow-Credentials': 'true',  // For cookies/auth
  'Vary': 'Origin',  // Important for caching with multiple origins
}
```

### Security Considerations
```typescript
// ❌ Don't do this for authenticated APIs:
{
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Credentials': 'true'
}

// ✅ Do this instead:
{
  'Access-Control-Allow-Origin': 'https://app.example.com',  // Specific origin
  'Access-Control-Allow-Credentials': 'true'
}
```

## MCP Server Integration

When Cloudflare MCP server is available:
- Query latest CORS best practices and security recommendations
- Get current browser CORS specification updates
- Check for common CORS vulnerabilities and mitigations

## Benefits

### Immediate Impact
- **Prevents CORS Errors**: Catches missing headers before deployment
- **Improves Security**: Prevents overly permissive CORS configurations
- **Better User Experience**: Ensures cross-origin requests work properly

### Long-term Value
- **Consistent CORS Standards**: Ensures all APIs follow proper CORS patterns
- **Reduced Debugging Time**: Immediate feedback on CORS issues
- **Security Compliance**: Prevents CORS-related security vulnerabilities

## Usage Examples

### During Response Creation
```typescript
// Developer types: new Response(data)
// SKILL immediately activates: "⚠️ HIGH: Response missing CORS headers. Cross-origin requests will be blocked by browsers."
```

### During API Development
```typescript
// Developer types: 'Access-Control-Allow-Origin': '*'
// SKILL immediately activates: "⚠️ HIGH: Overly permissive CORS with wildcard origin. Consider specific origins for security."
```

### During Method Handling
```typescript
// Developer types: if (request.method === 'POST') { ... }
// SKILL immediately activates: "⚠️ HIGH: Missing OPTIONS handler for preflight requests. Add OPTIONS method handling."
```

## CORS Checklist

### Required for Cross-Origin Requests
- [ ] `Access-Control-Allow-Origin` header set
- [ ] OPTIONS method handled for preflight requests
- [ ] `Access-Control-Allow-Methods` header for preflight
- [ ] `Access-Control-Allow-Headers` header for preflight

### Security Best Practices
- [ ] Origin validation (not wildcard for authenticated APIs)
- [ ] Specific allowed methods (not wildcard)
- [ ] Proper credentials handling
- [ ] Environment-based origin configuration

### Performance Optimization
- [ ] `Access-Control-Max-Age` header set
- [ ] `Vary: Origin` header for caching
- [ ] Efficient preflight handling

This SKILL ensures CORS is configured correctly by providing immediate, autonomous validation of CORS patterns, preventing common cross-origin issues and security vulnerabilities.