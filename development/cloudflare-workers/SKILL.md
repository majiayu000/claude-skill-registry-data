---
name: cloudflare-workers
description: Edge function development patterns for Cloudflare Workers. Use when creating API endpoints, handling requests, or working with bindings.
---

# Cloudflare Workers Development

## Quick Patterns

### Basic Worker Handler
```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // Enable CORS
    const corsHeaders = {
      'Access-Control-Allow-Origin': env.FRONTEND_URL || '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }
    
    try {
      // Route handling
      if (url.pathname.startsWith('/api/')) {
        const response = await handleApi(request, env);
        return new Response(response.body, {
          ...response,
          headers: { ...response.headers, ...corsHeaders }
        });
      }
      
      return new Response('Not found', { status: 404 });
    } catch (error) {
      console.error('Worker error:', error);
      return new Response('Internal Server Error', { status: 500 });
    }
  }
};
```

### Hyperdrive Database Connection
```typescript
import postgres from 'postgres';

// ALWAYS use Hyperdrive connection string, never Neon serverless driver
export function getDb(env: Env) {
  return postgres(env.HYPERDRIVE.connectionString, {
    prepare: false, // Required for Hyperdrive
  });
}

// Usage in handler
async function handleDatabaseQuery(env: Env) {
  const sql = getDb(env);
  const results = await sql`
    SELECT * FROM users 
    WHERE created_at > ${new Date(Date.now() - 86400000)}
    LIMIT 10
  `;
  await sql.end(); // Important: close connection
  return results;
}
```

### R2 Storage Operations
```typescript
// Upload to R2
async function handleUpload(request: Request, env: Env) {
  const formData = await request.formData();
  const file = formData.get('file') as File;
  
  if (!file) {
    return new Response('No file provided', { status: 400 });
  }
  
  const key = `uploads/${crypto.randomUUID()}-${file.name}`;
  const arrayBuffer = await file.arrayBuffer();
  
  await env.R2_BUCKET.put(key, arrayBuffer, {
    httpMetadata: {
      contentType: file.type,
    },
    customMetadata: {
      uploadedBy: 'user-id',
      uploadedAt: new Date().toISOString(),
    },
  });
  
  return new Response(JSON.stringify({ key, url: `/api/files/${key}` }));
}

// Retrieve from R2
async function handleGetFile(key: string, env: Env) {
  const object = await env.R2_BUCKET.get(key);
  
  if (!object) {
    return new Response('File not found', { status: 404 });
  }
  
  return new Response(object.body, {
    headers: {
      'Content-Type': object.httpMetadata?.contentType || 'application/octet-stream',
    },
  });
}
```

### KV Cache Pattern
```typescript
async function getCachedData(key: string, env: Env, fetcher: () => Promise<any>) {
  // Try cache first
  const cached = await env.KV_NAMESPACE.get(key, 'json');
  if (cached) return cached;
  
  // Fetch fresh data
  const data = await fetcher();
  
  // Cache with TTL
  await env.KV_NAMESPACE.put(key, JSON.stringify(data), {
    expirationTtl: 300, // 5 minutes
  });
  
  return data;
}
```

### Durable Objects for WebSockets
```typescript
export class WebSocketRoom {
  state: DurableObjectState;
  sessions: Map<WebSocket, any> = new Map();
  
  constructor(state: DurableObjectState) {
    this.state = state;
  }
  
  async fetch(request: Request) {
    if (request.headers.get('Upgrade') !== 'websocket') {
      return new Response('Expected WebSocket', { status: 400 });
    }
    
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);
    
    this.handleSession(server);
    
    return new Response(null, {
      status: 101,
      webSocket: client,
    });
  }
  
  handleSession(ws: WebSocket) {
    ws.accept();
    this.sessions.set(ws, { connected: Date.now() });
    
    ws.addEventListener('message', async (event) => {
      // Broadcast to all sessions
      for (const [session] of this.sessions) {
        if (session !== ws && session.readyState === WebSocket.OPEN) {
          session.send(event.data);
        }
      }
    });
    
    ws.addEventListener('close', () => {
      this.sessions.delete(ws);
    });
  }
}
```

## Configuration Best Practices

### wrangler.jsonc Structure
```jsonc
{
  "name": "pitchey-api",
  "main": "src/index.ts",
  "compatibility_date": "2024-01-01",
  "compatibility_flags": ["nodejs_compat"],
  
  // Bindings
  "kv_namespaces": [
    { "binding": "CACHE", "id": "kv-id" }
  ],
  
  "r2_buckets": [
    { "binding": "R2_BUCKET", "bucket_name": "pitchey-uploads" }
  ],
  
  "hyperdrive": [
    { "binding": "HYPERDRIVE", "id": "hyperdrive-config-id" }
  ],
  
  "durable_objects": {
    "bindings": [
      { "name": "WEBSOCKET_ROOMS", "class_name": "WebSocketRoom" }
    ]
  },
  
  // Secrets (set via CLI)
  // wrangler secret put JWT_SECRET
  // wrangler secret put SENTRY_DSN
}
```

## Common Pitfalls to Avoid

1. **Never use Neon serverless driver with Hyperdrive** - causes connection conflicts
2. **Always close database connections** - prevents connection pool exhaustion  
3. **Set Content-Type headers explicitly** - especially for R2 uploads
4. **Handle CORS properly** - include OPTIONS method handler
5. **Use ExecutionContext.waitUntil()** - for background tasks that shouldn't block response
6. **Respect subrequest limits** - max 50 per request in free tier
7. **Watch CPU time** - 10ms limit on free tier, 50ms on paid