---
name: mocking-strategy
description: "Test isolation strategies, Mock Service Worker, in-memory fakes, and preventing mock drift in integration tests."
---

# Mocking Strategy & Test Isolation Protocol

Ensure tests remain fast and isolated without creating fragile or out-of-sync test simulations.

---

## 1. In-Memory Fakes Over Heavy Mocks

1. Prefer writing lightweight in-memory fakes implementing the real repository interface over scattering complex mock expectations throughout test files.
2. In-memory fakes maintain realistic state and allow testing business logic across multiple calls without coupling tests to implementation details.

---

## 2. Mock Service Worker for Network APIs

1. Intercept network requests at the network layer using MSW rather than monkey-patching fetch or axios.
2. Share MSW request handlers between unit tests, integration tests, and local browser development to guarantee consistency.
3. Validate mock responses against production schema contracts to prevent mock drift.
