---
name: vitest
description: "Write and optimize Vitest unit and component test suites; configure workspace projects, worker thread pools, mocks, coverage, and instant watch mode."
category: testing
risk: safe
source: self
source_type: self
date_added: "2026-09-13"
tags: ["vitest", "testing", "unit-test", "vite", "typescript", "esm", "coverage", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Vitest High-Performance Testing AI Skill Guide

## Overview & Engine Architecture

Vitest is a blazing-fast, Vite-native testing framework designed for modern JavaScript and TypeScript projects. By sharing Vite's transformation pipeline, plugins, and resolve configuration (`vite.config.ts`), Vitest eliminates the complex dual-bundler overhead (e.g., Babel/ts-jest vs Webpack) common in legacy test suites. Vitest executes test suites across worker thread pools (powered by **Tinypool**), provides Jest-compatible mocking APIs, supports browser-like DOM environments (**happy-dom** / **jsdom**), and delivers sub-second watch mode feedback driven by Vite's Hot Module Replacement (HMR) graph.

Claude operates as a Principal Software Quality Engineer, specializing in **Vitest workspace setups**, **worker pool concurrency optimization**, **deterministic mock isolation (`vi.mock`, `vi.spyOn`)**, **fake timers (`vi.useFakeTimers`)**, and **V8 code coverage thresholds**.

### Vitest Test Engine Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Vitest Architecture Pipeline                │
│                                                             │
│  Test Runner CLI & Watch Engine                             │
│  ├── Vitest Config (`vitest.config.ts` or `vite.config.ts`) │
│  └── HMR Module Graph (Re-runs only touched test files)     │
│                                                             │
│  Vite Transformation Pipeline (Shared with Dev Server)      │
│  ├── Native ESM Resolution, TypeScript, JSX Transpilation   │
│  └── Path Aliases (`@/components/*`) & Asset Loaders        │
│                                                             │
│  Execution Pool (Tinypool Worker Threads / Forks)           │
│  ├── Thread Isolation & Shared Memory Sandboxing           │
│  ├── DOM Mock Environments (`happy-dom` / `jsdom`)          │
│  └── Concurrent Test Runners (`test.concurrent`)            │
│                                                             │
│  Reporters & Diagnostics                                    │
│  └── Terminal Spec Reporter | V8/Istanbul Coverage | UI Mode│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Shared Vite Configuration**: Leverage `defineConfig` from `vitest/config` to reuse frontend build aliases, environment variables, and plugins, eliminating redundant configuration drift.
2. **Speed via `happy-dom`**: For frontend component testing, prefer `environment: 'happy-dom'` over `jsdom` to achieve up to 3x faster DOM initialization unless specific unsupported Web API features strictly require jsdom.
3. **Mandatory Mock Resetting**: Always configure `clearMocks: true`, `mockReset: true`, or invoke `vi.restoreAllMocks()` in `afterEach` hooks to prevent spy pollution and leaked state across tests.
4. **Deterministic Timers**: When testing debounces, throttle functions, or timeouts, use `vi.useFakeTimers()` and advance time explicitly with `vi.advanceTimersByTime(ms)`. Never use real-time `setTimeout` sleeps in automated unit test assertions.

---

## Production TypeScript Automation: Configuration & Test Suite

### 1. Production Vitest Configuration (`vitest.config.ts`)

```typescript
import { defineConfig } from "vitest/config";
import path from "node:path";

export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  test: {
    globals: true,
    environment: "happy-dom",
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
    setupFiles: ["./src/test/setup.ts"],
    pool: "threads",
    poolOptions: {
      threads: {
        singleThread: false,
        isolate: true,
      },
    },
    coverage: {
      provider: "v8",
      reporter: ["text", "json-summary", "html"],
      thresholds: {
        lines: 85,
        functions: 85,
        branches: 80,
        statements: 85,
      },
    },
  },
});
```

### 2. Robust Test Suite with Mocks & Timers (`src/services/billing.spec.ts`)

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { processSubscriptionRenewal } from "./billing";
import { paymentGateway } from "../clients/gateway";

describe("processSubscriptionRenewal", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("successfully charges active subscription and emits audit log", async () => {
    const chargeSpy = vi.spyOn(paymentGateway, "charge").mockResolvedValue({
      transactionId: "tx_12345",
      success: true,
    });

    const resultPromise = processSubscriptionRenewal({
      subscriptionId: "sub_99",
      customerId: "cust_42",
      amountCents: 2900,
    });

    // Advance simulated time forward
    vi.advanceTimersByTime(100);
    const result = await resultPromise;

    expect(chargeSpy).toHaveBeenCalledTimes(1);
    expect(chargeSpy).toHaveBeenCalledWith("cust_42", 2900);
    expect(result).toEqual({
      status: "RENEWED",
      transactionId: "tx_12345",
    });
  });

  it("handles payment rejection gracefully", async () => {
    vi.spyOn(paymentGateway, "charge").mockRejectedValue(new Error("Insufficient funds"));

    await expect(
      processSubscriptionRenewal({
        subscriptionId: "sub_99",
        customerId: "cust_42",
        amountCents: 2900,
      })
    ).rejects.toThrow("Insufficient funds");
  });
});
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`ReferenceError: document is not defined`** | DOM APIs accessed in a test without configuring the DOM environment. | Set `environment: 'happy-dom'` in `vitest.config.ts` or add `// @vitest-environment happy-dom` docblock to test file. |
| **Flaky tests passing individually but failing in parallel** | Shared global state, database mutations, or uncleaned mocks leaking between worker threads. | 1. Enable `poolOptions.threads.isolate = true`.<br>2. Add `vi.clearAllMocks()` in `beforeEach`.<br>3. Isolate tenant IDs in test data. |
| **`Error: Cannot find module '@/...'`** | Vitest configuration missing module path aliases defined in `tsconfig.json`. | Declare path aliases in `vitest.config.ts` using `resolve.alias` or install `vite-tsconfig-paths` plugin. |
| **High CPU and slow startup on CI runners** | Excessive worker thread contention on low-core virtual machines (e.g., 2-core GitHub Actions runner). | Set `poolOptions.threads.maxThreads = 2` or pass `--no-threads` in resource-constrained CI environments. |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Run complete test suite once in CI mode with V8 coverage
npx vitest run --coverage

# 2. Run test suites matching a specific pattern in watch mode
npx vitest watch src/services/billing

# 3. Launch interactive Vitest graphical Web UI
npx vitest --ui

# 4. Update outdated snapshots
npx vitest -u
```

---

## Agent Operational Directive

> **MANDATORY**: Never introduce manual sleep promises (`await new Promise(r => setTimeout(r, ms))`) into Vitest test cases. Always use `vi.useFakeTimers()` to ensure deterministic, instantaneous test execution.
