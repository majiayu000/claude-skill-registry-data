---
name: sandbox-usage
description: Use when working with the Cloudflare Sandbox SDK, container lifecycle, session management, or OpenCode integration. Covers SDK patterns, security considerations, and common operations.
---

# Cloudflare Sandbox SDK Usage

This skill covers using the Cloudflare Sandbox SDK in cloudx.sh for secure container execution.

## Core Concepts

### Sandbox Lifecycle

1. **Get sandbox instance** via Durable Object binding
2. **Execute operations** (git clone, file writes, commands)
3. **Expose ports** for user access
4. **Proxy requests** to the running container

### Session Management

Each GitHub repository gets a unique session ID (UUID). Sessions are tracked in KV:

```typescript
// Session cache keys
`session:${owner}/${repo}` → sessionId      // 2hr TTL
`info:${sessionId}` → { status, repo, ... } // 2hr TTL
`preview:${sessionId}` → previewUrl         // 2hr TTL
`lock:${owner}/${repo}` → lockValue         // 30s TTL (race prevention)
```

## SDK Patterns

### Getting a Sandbox Instance

```typescript
import { Sandbox, getSandbox, proxyToSandbox } from '@cloudflare/sandbox';

// Re-export for Durable Object registration
export { Sandbox };

// Get sandbox for a specific session
const sandbox = getSandbox(env.SANDBOX, sessionId);
```

### Safe Git Operations

**Always use `gitCheckout()` instead of shell exec for cloning:**

```typescript
// GOOD - Uses SDK method, prevents command injection
await sandbox.gitCheckout(repoUrl, {
  targetDir: '/home/user/repo',
  depth: 1,  // Shallow clone for speed
});

// BAD - Vulnerable to command injection
await sandbox.exec(`git clone ${repoUrl}`);  // NEVER DO THIS
```

### File Operations

```typescript
// Write configuration files
await sandbox.writeFile('/home/user/repo/.opencode.json', JSON.stringify({
  provider: { anthropic: { apiKey: env.ANTHROPIC_API_KEY } },
  model: { provider: 'anthropic', model: 'claude-opus-4-5-20250514' },
}, null, 2));

// Read files
const content = await sandbox.readFile('/path/to/file');
```

### Command Execution

```typescript
// Run commands with timeout
await sandbox.exec('npm install', { timeout: 60000 });

// Background processes (for servers)
await sandbox.exec(
  'cd /home/user/repo && nohup opencode serve --port 4096 > /tmp/opencode.log 2>&1 &',
  { timeout: 30000 }
);
```

### Port Exposure

```typescript
// Expose a port for external access
const portInfo = await sandbox.exposePort(4096);
console.log(portInfo.url);  // Preview URL for the service
```

### Proxying Requests

```typescript
// In fetch handler, proxy matching requests to sandbox
const proxyResponse = await proxyToSandbox(request, env);
if (proxyResponse) {
  return proxyResponse;
}
```

## Security Considerations

### Input Validation

Always validate user inputs before using them:

```typescript
// GitHub owner validation
const GITHUB_OWNER_REGEX = /^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$/;
function isValidGitHubOwner(owner: string): boolean {
  return GITHUB_OWNER_REGEX.test(owner) && !owner.includes('--');
}

// GitHub repo validation
const GITHUB_REPO_REGEX = /^[a-zA-Z0-9._-]{1,100}$/;
function isValidGitHubRepo(repo: string): boolean {
  return GITHUB_REPO_REGEX.test(repo) && repo !== '.' && repo !== '..';
}

// Session ID validation (UUID format)
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function isValidSessionId(sessionId: string): boolean {
  return UUID_REGEX.test(sessionId);
}
```

### Sanitization for Shell

When shell execution is unavoidable:

```typescript
function sanitizeForShell(input: string): string {
  return input.replace(/[^a-zA-Z0-9._-]/g, '');
}
```

### Race Condition Prevention

Use KV-based locking to prevent duplicate sessions:

```typescript
// Try to acquire lock
const lockValue = crypto.randomUUID();
const existingLock = await env.CACHE.get(lockKey);

if (existingLock) {
  // Another request is creating session, wait and retry
  await new Promise(resolve => setTimeout(resolve, 1000));
  // ... check for existing session
}

// Set lock with short TTL
await env.CACHE.put(lockKey, lockValue, { expirationTtl: 30 });

try {
  // Create session...
} finally {
  await env.CACHE.delete(lockKey);
}
```

## Container Configuration

### Wrangler Config

```jsonc
{
  "containers": [{
    "class_name": "Sandbox",
    "image": "./Dockerfile",
    "max_instances": 10
  }],
  "durable_objects": {
    "bindings": [{
      "name": "SANDBOX",
      "class_name": "Sandbox"
    }]
  },
  "migrations": [{
    "tag": "v1",
    "new_sqlite_classes": ["Sandbox"]
  }]
}
```

### Env Interface

```typescript
interface Env {
  SANDBOX: DurableObjectNamespace<Sandbox>;
  CACHE: KVNamespace;
  ANTHROPIC_API_KEY: string;
  ENVIRONMENT: string;
}
```

## Status Tracking

Track session status through initialization:

```typescript
type SessionStatus = 'initializing' | 'cloning' | 'starting' | 'running' | 'error';

async function updateSessionStatus(
  env: Env,
  sessionId: string,
  status: SessionStatus,
  error?: string
): Promise<void> {
  const infoKey = `info:${sessionId}`;
  const existing = await env.CACHE.get(infoKey, 'json');

  if (existing) {
    await env.CACHE.put(infoKey, JSON.stringify({
      ...existing,
      status,
      error,
      updatedAt: Date.now(),
    }), { expirationTtl: 7200 });
  }
}
```

## Troubleshooting

### Container Not Enabled

Check that `containers[].class_name` matches `durable_objects.bindings[].class_name`.

### Image Registry Error

Use `./Dockerfile` for image path. Cloudflare builds and pushes to their registry.

### Port Exposure Fails

Ensure the container exposes the port in Dockerfile (`EXPOSE 4096`).

### Session Not Found

Sessions expire after 2 hours. Check KV for `info:{sessionId}` to see status.
