---
name: error-monitor
description: "Sets up error monitoring and tracking for the project. Detects the framework and generates integration code for Sentry, Bugsnag, or custom error tracking with proper error boundaries and middleware."
argument-hint: "[sentry, bugsnag, or 'auto']"
allowed-tools: Read, Grep, Glob, Bash, Write
---

# Error Monitoring Setup

## Detect Framework
!`ls package.json requirements.txt go.mod Cargo.toml *.csproj 2>/dev/null`
!`cat package.json 2>/dev/null | grep -E "react|next|express|fastify|koa|nest|vue|angular|svelte" | head -5`
!`cat requirements.txt pyproject.toml 2>/dev/null | grep -iE "django|flask|fastapi|starlette" 2>/dev/null | head -5`

## Existing Error Tracking
!`grep -r "sentry\|bugsnag\|rollbar\|airbrake\|errortracking\|newrelic" --include="*.json" --include="*.ts" --include="*.js" --include="*.py" -l 2>/dev/null | head -5`

---

## Setup Process

### Step 1: Choose Provider
Based on the project stack:
- **Sentry**: Best overall, supports all major languages
- **Bugsnag**: Good for mobile and frontend
- **Custom**: For projects that can't use third-party services

### Step 2: Framework-Specific Integration

**React/Next.js:**
- Error Boundary component wrapping the app
- `Sentry.init()` in entry point
- Source map upload in build step
- Client-side error capturing

**Express/Fastify/Koa:**
- Error handling middleware (must be last middleware)
- Request context enrichment (user, request ID)
- Unhandled rejection handler

**FastAPI/Django/Flask:**
- Middleware for request error capture
- Custom exception handlers
- Background task error tracking

**Go:**
- Panic recovery middleware
- Error wrapping with context
- Goroutine error capture

### Step 3: Configuration
Generate configuration file with:
- DSN/API key reference (from environment variable, never hardcoded)
- Environment detection (development, staging, production)
- Release version tracking
- Sample rate configuration
- Sensitive data scrubbing rules (strip passwords, tokens, PII)

### Step 4: Custom Error Classes
Generate project-specific error types:
- `AppError` base class with code, message, context
- `ValidationError` for input validation failures
- `NotFoundError` for missing resources
- `AuthError` for authentication/authorization failures
- `ExternalServiceError` for third-party failures

### Step 5: Alert Configuration
Recommend alert rules:
- Critical: Unhandled exceptions, auth failures, data corruption
- Warning: High error rate, slow responses, degraded service
- Info: New error types, deployment markers

## Rules
- NEVER hardcode DSN/API keys — use environment variables
- Always scrub sensitive data before sending to error tracker
- Include contextual data (user ID, request ID, action) with every error
- Set up source maps for frontend (minified code is useless in stack traces)
- Don't track expected errors (404 for invalid URLs, validation errors)
