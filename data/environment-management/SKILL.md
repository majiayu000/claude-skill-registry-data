---
name: environment-management
description: Environment configuration patterns, secret handling, and multi-environment management. Reference this skill when managing environments.
---

# Environment Management Skill
# Project Autopilot - Configuration and secrets patterns
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Comprehensive patterns for managing environment configurations securely.

---

## Environment File Hierarchy

### File Priority (Highest to Lowest)

```
1. .env.local          # Local overrides (never committed)
2. .env.{environment}  # Environment-specific (staging, production)
3. .env                # Default values (can be committed)
```

### Example Structure

```bash
project/
├── .env                 # Defaults (committed)
├── .env.example         # Template (committed)
├── .env.local           # Local secrets (gitignored)
├── .env.staging         # Staging config
├── .env.production      # Production config (no secrets!)
└── .gitignore
```

### .gitignore Pattern

```gitignore
# Environment files
.env.local
.env.*.local
.env.development.local
.env.staging.local
.env.production.local

# Secret files
*.pem
*.key
secrets/
```

---

## Variable Naming Conventions

### Prefixes

| Prefix | Usage | Example |
|--------|-------|---------|
| `NEXT_PUBLIC_` | Client-exposed (Next.js) | `NEXT_PUBLIC_API_URL` |
| `VITE_` | Client-exposed (Vite) | `VITE_API_URL` |
| `REACT_APP_` | Client-exposed (CRA) | `REACT_APP_API_URL` |
| (none) | Server-only | `DATABASE_URL` |

### Categories

```bash
# Application
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug

# Database
DATABASE_URL=postgres://...
REDIS_URL=redis://...

# Authentication
JWT_SECRET=...
SESSION_SECRET=...
OAUTH_CLIENT_ID=...
OAUTH_CLIENT_SECRET=...

# Third-Party Services
STRIPE_SECRET_KEY=...
SENDGRID_API_KEY=...
AWS_ACCESS_KEY_ID=...

# Feature Flags
FEATURE_NEW_CHECKOUT=true
FEATURE_DARK_MODE=false

# Public/Client
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_SITE_URL=https://example.com
```

---

## Secret Management

### Never Do This

```bash
# ❌ Hardcoded in code
const apiKey = 'sk_live_abc123';

# ❌ Committed to git
DATABASE_URL=postgres://user:realpassword@prod.db.com/app

# ❌ Logged or exposed
console.log('API Key:', process.env.API_KEY);
```

### Secure Patterns

```typescript
// ✅ Environment variable
const apiKey = process.env.API_KEY;
if (!apiKey) {
  throw new Error('API_KEY environment variable required');
}

// ✅ Validation on startup
function validateEnv() {
  const required = ['DATABASE_URL', 'JWT_SECRET', 'API_KEY'];
  const missing = required.filter(key => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(`Missing required env vars: ${missing.join(', ')}`);
  }
}

// ✅ Type-safe env with Zod
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  PORT: z.coerce.number().default(3000),
});

export const env = envSchema.parse(process.env);
```

### Secret Rotation

```typescript
// Support multiple keys during rotation
const apiKeys = [
  process.env.API_KEY_NEW,
  process.env.API_KEY_OLD,
].filter(Boolean);

function validateApiKey(key: string): boolean {
  return apiKeys.includes(key);
}
```

---

## Multi-Environment Setup

### Environment Matrix

| Variable | Development | Staging | Production |
|----------|-------------|---------|------------|
| `NODE_ENV` | development | staging | production |
| `DATABASE_URL` | localhost | staging.db | prod.db |
| `LOG_LEVEL` | debug | info | warn |
| `API_URL` | localhost:3000 | staging.api | api.com |
| `FEATURE_X` | true | true | false |

### Configuration by Environment

```typescript
// config/index.ts
const configs = {
  development: {
    api: {
      url: 'http://localhost:3000',
      timeout: 30000,
    },
    features: {
      debugMode: true,
      mockPayments: true,
    },
  },
  staging: {
    api: {
      url: 'https://staging.api.com',
      timeout: 10000,
    },
    features: {
      debugMode: true,
      mockPayments: true,
    },
  },
  production: {
    api: {
      url: 'https://api.com',
      timeout: 5000,
    },
    features: {
      debugMode: false,
      mockPayments: false,
    },
  },
};

export const config = configs[process.env.NODE_ENV || 'development'];
```

---

## .env.example Template

```bash
# Application
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug

# Database
# Format: postgres://user:password@host:port/database
DATABASE_URL=postgres://user:password@localhost:5432/myapp

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Authentication
# Generate with: openssl rand -base64 32
JWT_SECRET=your-jwt-secret-min-32-chars-here
JWT_EXPIRES_IN=7d

# OAuth (Google)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Third-Party Services
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG....

# AWS (optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET=my-bucket

# Public (safe for client)
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Feature Flags
FEATURE_NEW_DASHBOARD=false
FEATURE_DARK_MODE=true
```

---

## CI/CD Environment Management

### GitHub Actions

```yaml
# Using secrets
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  JWT_SECRET: ${{ secrets.JWT_SECRET }}

# Using environments
jobs:
  deploy:
    environment: production
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Setting Secrets

```bash
# GitHub CLI
gh secret set DATABASE_URL --body "postgres://..."

# Vercel
vercel env add DATABASE_URL production

# Railway
railway variables set DATABASE_URL="postgres://..."
```

---

## Validation Schema

```typescript
// env.schema.ts
import { z } from 'zod';

export const envSchema = z.object({
  // Application
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.coerce.number().min(1).max(65535).default(3000),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),

  // Database
  DATABASE_URL: z.string().url().startsWith('postgres'),

  // Authentication
  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 characters'),
  JWT_EXPIRES_IN: z.string().default('7d'),

  // Optional services
  REDIS_URL: z.string().url().optional(),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_').optional(),

  // Public
  NEXT_PUBLIC_API_URL: z.string().url(),
});

// Validate on import
export const env = envSchema.parse(process.env);
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Var undefined in browser | Missing public prefix | Add `NEXT_PUBLIC_` |
| Var undefined in server | Not loaded | Check dotenv config |
| Different values per env | Wrong file loaded | Check NODE_ENV |
| Secrets in logs | Logging env | Never log secrets |

### Debug Environment

```bash
# List all env vars (careful with secrets!)
printenv | grep -i "database\|api\|secret" | sed 's/=.*/=***/'

# Check specific var
echo $DATABASE_URL | head -c 30

# Verify .env loaded
node -e "require('dotenv').config(); console.log(Object.keys(process.env).filter(k => k.includes('DATABASE')))"
```

---

## Best Practices Checklist

- [ ] All secrets in environment variables
- [ ] .env.example documents all variables
- [ ] Validation on application startup
- [ ] Different configs per environment
- [ ] Secrets never logged or exposed
- [ ] .gitignore covers all secret files
- [ ] CI/CD uses secrets management
- [ ] Secret rotation plan in place
