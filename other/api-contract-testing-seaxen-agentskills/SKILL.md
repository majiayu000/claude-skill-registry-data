---
name: api-contract-testing
description: API contract testing, OpenAPI schema validation, and Consumer-Driven Contracts (Pact). Use when testing inter-service communication, preventing breaking API changes, verifying schemas in CI pipelines, or creating mock servers from OpenAPI specs.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0
category: backend-api-design
---

# API Contract Testing

> **Consumer-Driven Contracts, OpenAPI Spec Validation & Zero-Breaking-Change Integration**

---

## 🏗️ Core Principles

| Principle | Rule |
|-----------|------|
| **Consumer-Driven Contracts** | Consumers define the exact subsets of fields they require. Providers verify their responses satisfy all consumer expectations. |
| **Fail in CI, Not in Prod** | Contract tests run against schemas or pact broker files during build time, completely eliminating cross-service deployment surprises. |
| **Strict OpenAPI Schema Validation** | APIs must publish machine-readable OpenAPI/Swagger specs. Request/response payloads must be validated against schemas. |
| **Additive Evolution** | APIs must evolve through addition, never breaking deletion: never rename or remove fields without formal version deprecation cycles. |

---

## 📋 Consumer-Driven Pact Test Pattern (TypeScript)

```typescript
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { fetchUserProfile } from './api-client';

const provider = new PactV3({
  consumer: 'web-frontend',
  provider: 'user-service',
});

describe('User Service Contract', () => {
  it('returns valid user profile on GET /users/:id', async () => {
    provider
      .uponReceiving('a request for an existing user')
      .withRequest({
        method: 'GET',
        path: '/api/v1/users/usr-123',
        headers: { Accept: 'application/json' },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: MatchersV3.regex(/^usr-[0-9]+$/, 'usr-123'),
          username: MatchersV3.string('alice'),
          role: MatchersV3.string('admin'),
          isActive: MatchersV3.boolean(true),
        },
      });

    await provider.executeTest(async (mockServer) => {
      const user = await fetchUserProfile(mockServer.url, 'usr-123');
      expect(user.id).toBe('usr-123');
      expect(user.username).toBe('alice');
    });
  });
});
```

---

## 📋 OpenAPI Schema Validation in CI

- Use `@stoplight/spectral-cli` to lint OpenAPI documents against corporate style guidelines.
- Use `oas-diff` / `openapi-diff` in PR pipelines to automatically block pull requests containing breaking schema changes.

---

## ❌ Anti-Patterns

- ❌ Depending on live staging environments for microservice integration testing.
- ❌ Testing entire unconstrained payloads instead of type matchers (`MatchersV3.string()`).
- ❌ Breaking field types or omitting required parameters without bumping API major versions.
