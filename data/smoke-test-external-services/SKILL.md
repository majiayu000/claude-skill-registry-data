---
name: smoke-test-external-services
description: Smoke-test third-party integrations — reachability/auth for payment, email/SMS, and monitoring providers (Stripe, Twilio, SendGrid...).
when_to_use: Reach for this to validate EXTERNAL dependencies only (third-party APIs reachable and authenticating). For your own API use smoke-test-api; for your DB use smoke-test-database; for auth flows use smoke-test-auth; for user journeys use smoke-test-critical-paths; for the whole suite use smoke-test-runner.
allowed-tools: Read, Bash, Grep, Glob
---

# Smoke Test External Services Skill

**Quick Reference** - Load this first for fast context (~3KB)

## Mission

Execute comprehensive external service integration smoke tests to validate third-party APIs, payment gateways, email/SMS providers, and monitoring service connectivity during release workflows.

## Core Capabilities

- **Service Connectivity**: Validate external service reachability and authentication
- **API Integration**: Test third-party API endpoints (Stripe, Twilio, SendGrid, etc.)
- **Circuit Breaker Testing**: Validate failover and graceful degradation
- **Rate Limit Handling**: Test rate limit detection and backoff strategies
- **Webhook Validation**: Verify webhook endpoints and signature validation
- **Service Health Monitoring**: Check external service status pages

## When to Use This Skill

Use this skill when:
- Executing pre-release smoke tests (validate external dependencies)
- Testing canary deployments (monitor external API quotas)
- Verifying rollback success (ensure external service connectivity restored)
- Running scheduled health checks (detect external service degradation)
- Validating disaster recovery (test failover to backup providers)

## Quick Start

### 1. Load Skill in Agent

```yaml
skills:
  - name: smoke-test-external-services
    path: skills/smoke-test-external-services/SKILL.md
```

### 2. Execute External Service Tests

```javascript
const { SmokeTestExternalServices } = require('./scripts/test-integrations.js');

const tester = new SmokeTestExternalServices({
  services: [
    {
      name: 'stripe',
      type: 'payment',
      baseUrl: 'https://api.stripe.com',
      apiKey: process.env.STRIPE_API_KEY
    },
    {
      name: 'sendgrid',
      type: 'email',
      baseUrl: 'https://api.sendgrid.com',
      apiKey: process.env.SENDGRID_API_KEY
    }
  ]
});

const result = await tester.executeTests({
  environment: 'staging',
  tests: ['connectivity', 'authentication', 'basic-operation']
});

if (result.passed) {
  console.log('✅ External service smoke tests passed');
} else {
  console.error('❌ External service smoke tests failed');
}
```

### 3. Configuration Template

```yaml
environment: staging
services:
  - name: stripe
    type: payment
    baseUrl: https://api.stripe.com
    apiKey: ${STRIPE_API_KEY}
    tests:
      - connectivity
      - authentication
      - create-test-charge
  - name: sendgrid
    type: email
    baseUrl: https://api.sendgrid.com
    apiKey: ${SENDGRID_API_KEY}
    tests:
      - connectivity
      - authentication
      - send-test-email
```

## External Service Categories

### 1. Payment Gateways
- **Stripe**: Create test charge, retrieve customer, list payment methods
- **PayPal**: Create test transaction, verify webhook signature
- **Square**: Create test payment, retrieve merchant info
- **Braintree**: Generate client token, create test transaction

### 2. Communication Services
- **SendGrid**: Send test email, verify API key, check email quota
- **Twilio**: Send test SMS, make test call, verify webhook
- **Mailgun**: Send test email, validate domain, check quota
- **Postmark**: Send test email, retrieve server info

### 3. Cloud Storage
- **AWS S3**: Upload test file, retrieve object, verify bucket access
- **Google Cloud Storage**: Upload test file, retrieve object, check quota
- **Azure Blob Storage**: Upload test blob, retrieve blob, verify container access

### 4. Monitoring & Analytics
- **Datadog**: Send test metric, create test event, verify API key
- **New Relic**: Send test transaction, create test deployment marker
- **Sentry**: Send test error, verify DSN, check project quota
- **Segment**: Send test event, verify write key

### 5. Authentication & Identity
- **Auth0**: Verify tenant, test authentication flow, check quota
- **Okta**: Verify domain, test user authentication, check API rate limits
- **Firebase Auth**: Verify project, test authentication, check quota

## Performance SLAs

```javascript
const SLA_TARGETS = {
  connectivity: 2000,      // Connection test: ≤2000ms
  authentication: 3000,    // Auth test: ≤3000ms
  basicOperation: 5000,    // Basic API operation: ≤5000ms
  webhookValidation: 1000, // Webhook validation: ≤1000ms
  timeout: 10000           // Global timeout: ≤10000ms
};
```

## Pass/Fail Criteria

**Pass**: All external service tests must pass
- ✅ All services reachable and responding
- ✅ Authentication successful for all services
- ✅ Basic operations execute successfully
- ✅ No rate limit violations
- ✅ Webhook signatures validate correctly

**Fail**: Any external service test failure blocks deployment
- ❌ Any service unreachable or timing out
- ❌ Authentication failures
- ❌ API operations failing
- ❌ Rate limit exceeded
- ❌ Webhook signature validation failures

## Execution Points

External service smoke tests are executed at these points in the release workflow:

1. **Pre-Release** (before staging deployment): Validate all external service integrations
2. **Post-Staging** (after staging deployment): Verify external services in staging environment
3. **Canary 5%** (5% traffic): Test external service rate limits with minimal load
4. **Canary 25%** (25% traffic): Validate external service performance under moderate load
5. **Canary 100%** (100% traffic): Test external services at full production load
6. **Post-Production** (after production deployment): Verify production external service health
7. **Post-Rollback** (after rollback): Validate external service connectivity after rollback

## Common Patterns

### Pattern 1: Simple Connectivity Test

```javascript
const result = await tester.testServiceConnectivity({
  name: 'stripe',
  url: 'https://api.stripe.com/v1/customers',
  timeout: 5000
});
```

### Pattern 2: Authentication Test

```javascript
const result = await tester.testAuthentication({
  name: 'sendgrid',
  url: 'https://api.sendgrid.com/v3/user/profile',
  apiKey: process.env.SENDGRID_API_KEY
});
```

### Pattern 3: Basic Operation Test

```javascript
const result = await tester.testBasicOperation({
  service: 'stripe',
  operation: 'create-test-charge',
  params: {
    amount: 100,
    currency: 'usd',
    source: 'tok_visa'
  }
});
```

### Pattern 4: Webhook Validation

```javascript
const result = await tester.testWebhookValidation({
  service: 'stripe',
  webhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
  payload: mockWebhookPayload,
  signature: mockSignature
});
```

## Output Format

```javascript
{
  passed: true,
  details: {
    totalServices: 5,
    passed: 5,
    failed: 0,
    executionTime: 3456
  },
  reason: 'External service smoke tests passed: All 5 services healthy',
  metrics: {
    servicesPassed: 5,
    servicesFailed: 0,
    averageResponseTime: 456,
    executionTime: 3456
  },
  results: [
    {
      service: 'stripe',
      type: 'payment',
      tests: {
        connectivity: { passed: true, duration: 234 },
        authentication: { passed: true, duration: 456 },
        basicOperation: { passed: true, duration: 789 }
      },
      overall: { passed: true, duration: 1479 }
    }
  ]
}
```

## Circuit Breaker Pattern

```javascript
const tester = new SmokeTestExternalServices({
  circuitBreaker: {
    enabled: true,
    failureThreshold: 3,      // Open circuit after 3 failures
    successThreshold: 2,      // Close circuit after 2 successes
    timeout: 30000,           // Half-open state after 30 seconds
    fallbackService: 'backup-provider'
  }
});
```

## Rate Limit Handling

```javascript
const tester = new SmokeTestExternalServices({
  rateLimiting: {
    detectRateLimits: true,
    retryAfterHeader: 'Retry-After',
    maxRetries: 3,
    backoffMultiplier: 2
  }
});
```

## Need More Detail?

For comprehensive documentation including:
- Advanced testing patterns (failover testing, quota monitoring, webhook security)
- Multi-provider configurations (backup providers, load balancing)
- Integration with monitoring systems (Datadog, New Relic, Sentry)
- Custom validation rules and error handling strategies
- Service-specific implementation guides

**Load**: `skills/smoke-test-external-services/REFERENCE.md` (~15KB)
