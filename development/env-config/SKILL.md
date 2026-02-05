---
name: env-config
description: Implement environment variable management with .env files, validation, and environment-specific configs. Use when setting up configuration, handling secrets, or managing different deployment environments.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Environment Configuration Skill

Manage environment variables securely across development, staging, and production environments.

## Core Principles

1. **Never commit secrets** - .env files with real values must be in .gitignore
2. **Document all variables** - .env.example shows required variables with placeholder values
3. **Validate at startup** - Fail fast if required variables are missing
4. **Type coercion** - Parse strings to appropriate types (numbers, booleans)
5. **Environment-specific** - Support different configs for dev/staging/prod

## File Structure

```
project/
├── .env                    # Local overrides (gitignored)
├── .env.example            # Template with placeholders (committed)
├── .env.development        # Development defaults (optional, committed)
├── .env.production         # Production defaults (optional, committed)
├── .env.test               # Test environment (optional, committed)
└── src/
    └── config/
        └── env.js          # Validation and export
```

## .env.example Template

Always provide a documented example:

```bash
# .env.example
# Copy to .env and fill in real values

# ===================
# Required Variables
# ===================

# Database connection
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API keys (get from provider dashboard)
API_KEY=your-api-key-here

# ===================
# Optional Variables
# ===================

# Server configuration
PORT=3000
HOST=localhost

# Feature flags
ENABLE_DEBUG=false
LOG_LEVEL=info

# External services
REDIS_URL=redis://localhost:6379
```

## Environment Validation

### Node.js Pattern (Zero Dependencies)

```javascript
// src/config/env.js

/**
 * Environment configuration with validation
 * Fails fast if required variables are missing
 */

/**
 * Get required environment variable
 * @param {string} name - Variable name
 * @returns {string} Variable value
 * @throws {Error} If variable is missing
 */
function required(name) {
  const value = process.env[name];
  if (value === undefined || value === '') {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

/**
 * Get optional environment variable with default
 * @param {string} name - Variable name
 * @param {string} defaultValue - Default if not set
 * @returns {string} Variable value or default
 */
function optional(name, defaultValue) {
  const value = process.env[name];
  return value !== undefined && value !== '' ? value : defaultValue;
}

/**
 * Parse boolean from environment variable
 * @param {string} name - Variable name
 * @param {boolean} defaultValue - Default if not set
 * @returns {boolean} Parsed boolean
 */
function bool(name, defaultValue = false) {
  const value = process.env[name];
  if (value === undefined || value === '') {
    return defaultValue;
  }
  return value.toLowerCase() === 'true' || value === '1';
}

/**
 * Parse integer from environment variable
 * @param {string} name - Variable name
 * @param {number} defaultValue - Default if not set
 * @returns {number} Parsed integer
 */
function int(name, defaultValue) {
  const value = process.env[name];
  if (value === undefined || value === '') {
    return defaultValue;
  }
  const parsed = parseInt(value, 10);
  if (Number.isNaN(parsed)) {
    throw new Error(`Invalid integer for ${name}: ${value}`);
  }
  return parsed;
}

// Export validated configuration
export const config = {
  // Environment
  nodeEnv: optional('NODE_ENV', 'development'),
  isProduction: optional('NODE_ENV', 'development') === 'production',
  isDevelopment: optional('NODE_ENV', 'development') === 'development',
  isTest: optional('NODE_ENV', 'development') === 'test',

  // Server
  port: int('PORT', 3000),
  host: optional('HOST', 'localhost'),

  // Database (required in production)
  databaseUrl: optional('NODE_ENV', 'development') === 'production'
    ? required('DATABASE_URL')
    : optional('DATABASE_URL', 'postgresql://localhost:5432/dev'),

  // Feature flags
  debug: bool('ENABLE_DEBUG', false),
  logLevel: optional('LOG_LEVEL', 'info'),
};

// Validate on import (fail fast)
export function validateEnv() {
  // Add custom validation logic here
  if (config.isProduction && !process.env.DATABASE_URL) {
    throw new Error('DATABASE_URL is required in production');
  }
}

// Auto-validate when module is imported
validateEnv();
```

### Usage

```javascript
import { config } from './config/env.js';

// Use validated config
const server = createServer();
server.listen(config.port, config.host);

console.log(`Server running in ${config.nodeEnv} mode`);
```

## Loading .env Files

### Node.js 20+ (Native Support)

```bash
# Load .env file automatically
node --env-file=.env src/server.js

# Load environment-specific file
node --env-file=.env.production src/server.js
```

### With dotenv (for older Node.js)

```javascript
// At the very top of entry point
import 'dotenv/config';

// Or with custom path
import { config } from 'dotenv';
config({ path: '.env.local' });
```

## Environment-Specific Configuration

### Pattern: Config by Environment

```javascript
// src/config/index.js
import { config as env } from './env.js';

const configs = {
  development: {
    apiUrl: 'http://localhost:3000/api',
    logLevel: 'debug',
    cacheTimeout: 0,
  },
  test: {
    apiUrl: 'http://localhost:3001/api',
    logLevel: 'error',
    cacheTimeout: 0,
  },
  production: {
    apiUrl: 'https://api.example.com',
    logLevel: 'warn',
    cacheTimeout: 3600,
  },
};

export const config = {
  ...configs[env.nodeEnv],
  ...env,
};
```

## Secret Management

### Local Development

```bash
# .env (gitignored)
DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp
API_KEY=dev-api-key-12345
```

### Production (Use Secret Manager)

Never put production secrets in files. Use:

- **Cloudflare**: Wrangler secrets or environment variables in dashboard
- **DigitalOcean**: App Platform environment variables
- **Docker**: Docker secrets or environment variables
- **CI/CD**: GitHub Actions secrets, GitLab CI variables

```yaml
# Example: GitHub Actions
jobs:
  deploy:
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      API_KEY: ${{ secrets.API_KEY }}
```

## Validation with Zod (Optional)

For complex validation, use Zod:

```javascript
// src/config/env.js
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.string().transform(Number).default('3000'),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  ENABLE_DEBUG: z.string().transform(v => v === 'true').default('false'),
});

// Parse and validate
const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error('Invalid environment variables:');
  console.error(parsed.error.format());
  process.exit(1);
}

export const config = parsed.data;
```

## .gitignore Configuration

```gitignore
# Environment files with secrets
.env
.env.local
.env.*.local

# Keep example and non-secret configs
!.env.example
!.env.development
!.env.test
```

## Checklist

Before deploying, verify:

- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` documents all required variables
- [ ] Required variables throw errors when missing
- [ ] No secrets in committed files
- [ ] Production uses secret manager, not files
- [ ] Environment-specific defaults are appropriate
- [ ] Type coercion handles edge cases

## Related Skills

- **security** - Protecting secrets and credentials
- **deployment** - Environment setup for Cloudflare/DigitalOcean
- **nodejs-backend** - Server configuration patterns
- **ci-cd** - Managing secrets in pipelines
