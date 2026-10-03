---
name: smoke-test-api
description: Smoke-test API health — endpoint availability, response times, and core CRUD/search/auth endpoints.
when_to_use: Reach for this to validate the API surface only (HTTP endpoints respond, latency SLAs, key operations). For the full release suite use smoke-test-runner; for DB connectivity use smoke-test-database; for third-party APIs use smoke-test-external-services; for login/token flows use smoke-test-auth; for end-to-end user journeys use smoke-test-critical-paths.
allowed-tools: Read, Bash, Grep, Glob
---

# Smoke Test API Skill

**Quick Reference** - Load this first for fast context (~3KB)

## Mission

Execute comprehensive API health smoke tests to validate service availability, response times, and critical endpoint functionality during release workflows.

## Core Capabilities

- **Health Check Execution**: Test API endpoints for availability and response time
- **Critical Endpoint Validation**: Verify core API operations (CRUD, search, auth)
- **Response Validation**: Check status codes, response structure, error handling
- **Performance SLA Validation**: Ensure response times meet performance budgets
- **Multi-Environment Support**: Test across pre-release, staging, production environments

## When to Use This Skill

Use this skill when:
- Executing pre-release smoke tests (before staging deployment)
- Validating post-deployment health (after staging/production deployment)
- Testing canary deployments (5%, 25%, 100% traffic)
- Verifying rollback success (after rollback operations)
- Running scheduled health checks (monitoring integration)

## Quick Start

### 1. Load Skill in Agent

```yaml
skills:
  - name: smoke-test-api
    path: skills/smoke-test-api/SKILL.md
```

### 2. Execute Health Checks

```javascript
const { SmokeTestAPI } = require('./scripts/execute-health-checks.js');

const tester = new SmokeTestAPI({
  baseUrl: 'https://staging.example.com',
  timeout: 5000,
  retries: 2
});

const result = await tester.executeHealthChecks({
  environment: 'staging',
  endpoints: [
    { path: '/health', method: 'GET', expectedStatus: 200 },
    { path: '/api/v1/users', method: 'GET', expectedStatus: 200 }
  ]
});

if (result.passed) {
  console.log('✅ API health checks passed');
} else {
  console.error('❌ API health checks failed');
}
```

### 3. Configuration Template

```yaml
environment: staging
baseUrl: https://staging.example.com
timeout: 5000
retries: 2
endpoints:
  - name: health-check
    path: /health
    method: GET
    expectedStatus: 200
    sla: 100
  - name: list-users
    path: /api/v1/users
    method: GET
    expectedStatus: 200
    sla: 500
```

## API Smoke Test Categories

### 1. Health Endpoints
- System health: `/health`, `/ping`, `/status`
- Database connectivity: `/health/db`
- Cache connectivity: `/health/cache`
- External service connectivity: `/health/integrations`

### 2. Critical CRUD Operations
- Create: `POST /api/v1/resource` (201 Created)
- Read: `GET /api/v1/resource/:id` (200 OK)
- Update: `PUT /api/v1/resource/:id` (200 OK)
- Delete: `DELETE /api/v1/resource/:id` (204 No Content)

### 3. Authentication & Authorization
- Login: `POST /api/v1/auth/login` (200 OK + token)
- Token validation: `GET /api/v1/auth/me` (200 OK with user)
- Protected resource: `GET /api/v1/protected` (401 without token, 200 with token)

### 4. Search & Query Operations
- Search: `GET /api/v1/search?q=term` (200 OK with results)
- Pagination: `GET /api/v1/resource?page=1&limit=10` (200 OK with paginated results)
- Filtering: `GET /api/v1/resource?status=active` (200 OK with filtered results)

### 5. Error Handling
- Not found: `GET /api/v1/nonexistent` (404 Not Found)
- Bad request: `POST /api/v1/resource` with invalid data (400 Bad Request)
- Unauthorized: `GET /api/v1/protected` without token (401 Unauthorized)

## Performance SLAs

```javascript
const SLA_TARGETS = {
  health: 100,      // Health endpoints: ≤100ms
  read: 500,        // Read operations: ≤500ms
  write: 1000,      // Write operations: ≤1000ms
  search: 2000,     // Search operations: ≤2000ms
  timeout: 5000     // Global timeout: ≤5000ms
};
```

## Pass/Fail Criteria

**Pass**: All smoke tests must pass
- ✅ All endpoints return expected status codes
- ✅ All response times meet SLA targets
- ✅ All response structures are valid
- ✅ No unexpected errors or exceptions

**Fail**: Any smoke test failure blocks deployment
- ❌ Any endpoint returns unexpected status code
- ❌ Any response time exceeds SLA target
- ❌ Any response structure is invalid
- ❌ Any unexpected error or exception occurs

## Execution Points

API smoke tests are executed at these points in the release workflow:

1. **Pre-Release** (before staging deployment): Validate API readiness
2. **Post-Staging** (after staging deployment): Verify staging API health
3. **Canary 5%** (5% traffic): Test canary API with minimal traffic
4. **Canary 25%** (25% traffic): Test canary API with moderate traffic
5. **Canary 100%** (100% traffic): Test canary API with full traffic
6. **Post-Production** (after production deployment): Verify production API health
7. **Post-Rollback** (after rollback): Validate rollback API health

## Common Patterns

### Pattern 1: Simple Health Check

```javascript
const result = await tester.testEndpoint({
  path: '/health',
  method: 'GET',
  expectedStatus: 200,
  sla: 100
});
```

### Pattern 2: Authenticated Request

```javascript
const result = await tester.testEndpoint({
  path: '/api/v1/users',
  method: 'GET',
  expectedStatus: 200,
  sla: 500,
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

### Pattern 3: POST with Body

```javascript
const result = await tester.testEndpoint({
  path: '/api/v1/users',
  method: 'POST',
  expectedStatus: 201,
  sla: 1000,
  body: {
    name: 'Test User',
    email: 'test@example.com'
  }
});
```

## Output Format

```javascript
{
  passed: true,
  details: {
    totalEndpoints: 10,
    passed: 10,
    failed: 0,
    executionTime: 1234
  },
  reason: 'API smoke tests passed: All 10 endpoints responding',
  metrics: {
    endpointsPassed: 10,
    endpointsFailed: 0,
    averageResponseTime: 123,
    executionTime: 1234
  },
  results: [
    {
      endpoint: '/health',
      method: 'GET',
      status: 200,
      responseTime: 45,
      sla: 100,
      passed: true
    }
  ]
}
```

## Need More Detail?

For comprehensive documentation including:
- Advanced testing patterns (retry logic, circuit breakers, rate limiting)
- Multi-environment configurations
- Integration with monitoring systems
- Custom validation rules
- Performance optimization strategies

**Load**: `skills/smoke-test-api/REFERENCE.md` (~15KB)
