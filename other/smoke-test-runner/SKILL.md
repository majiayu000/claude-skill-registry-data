---
name: smoke-test-runner
description: Orchestrate all smoke-test categories in dependency order (API → DB → external → auth → critical paths) with early-exit.
when_to_use: Reach for this as the ENTRY POINT for release smoke testing when you want the full suite run end-to-end (~15 min, stop on first failure). For testing one slice only, invoke that category skill directly — smoke-test-api, smoke-test-database, smoke-test-external-services, smoke-test-auth, or smoke-test-critical-paths. This is the orchestrator, not a category itself.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Smoke Test Runner Skill

**Quick Reference** - Orchestrates all smoke test categories

## Mission

Orchestrate execution of all smoke test categories (API, Database, External Services, Auth, Critical Paths) in the correct order with early exit on failure.

## Core Capabilities

- **Sequential Execution**: Execute smoke tests in dependency order
- **Early Exit**: Stop on first failure to save time
- **Skill Invocation**: Invoke specialized smoke test skills
- **Result Aggregation**: Collect and report all test results
- **Performance Tracking**: Track execution time per category

## Execution Order

1. **API Health** (2-3 minutes): Validate API endpoints responding
2. **Database** (1-2 minutes): Verify database connectivity and health
3. **External Services** (2-3 minutes): Test third-party integrations
4. **Auth** (1-2 minutes): Validate authentication and authorization
5. **Critical Paths** (3-5 minutes): Test end-to-end user journeys

**Total Target**: ≤15 minutes (all 5 categories)

## Quick Start

```javascript
const { SmokeTestRunner } = require('./scripts/orchestrate-smoke-tests.js');

const runner = new SmokeTestRunner({
  environment: 'staging',
  stopOnFirstFailure: true
});

const result = await runner.executeAll();

if (result.passed) {
  console.log('✅ All smoke tests passed');
  console.log(`Total time: ${result.totalDuration}ms`);
}
```

## Pass/Fail Criteria

**Pass**: All 5 smoke test categories must pass
- ✅ API health checks passing
- ✅ Database connectivity and integrity validated
- ✅ External services responding
- ✅ Auth flows working correctly
- ✅ Critical paths completing successfully

**Fail**: Any category failure blocks deployment
- ❌ Any smoke test category fails
- ❌ Execution exceeds timeout (15 minutes)

## Output Format

```javascript
{
  passed: true,
  totalDuration: 850000,  // 14 minutes 10 seconds
  categoriesExecuted: 5,
  categoriesPassed: 5,
  categoriesFailed: 0,
  results: {
    api: { passed: true, duration: 180000 },
    database: { passed: true, duration: 120000 },
    externalServices: { passed: true, duration: 200000 },
    auth: { passed: true, duration: 100000 },
    criticalPaths: { passed: true, duration: 250000 }
  }
}
```

## Need More Detail?

**Load**: `skills/smoke-test-runner/REFERENCE.md` (~5KB)
