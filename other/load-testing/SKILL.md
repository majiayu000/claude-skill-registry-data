---
name: load-testing
description: Create and manage K6 load tests for the REST and GraphQL APIs of a PHP backend service. Use when creating load tests, writing K6 scripts, testing API performance, debugging load test failures, or setting up performance monitoring. Covers REST endpoints, GraphQL operations, data generation, IRI handling, configuration patterns, and performance troubleshooting. Skip with a note when capabilities.load_testing is false.
---

# Load Testing Skill

## Profile keys consumed

- `capabilities.load_testing`
- `make.load_tests`
- `make.start`
- `framework.graphql`
- `framework.api_platform`
- `persistence.engine`
- `persistence.mapper`
- `architecture.bounded_contexts`

## Gating

This skill is gated by `capabilities.load_testing`. When it is `false`,
or when `make.load_tests` is `null`, record a capability-absent note
("load testing not configured for this project", NFR-4) and skip — never
improvise raw `k6 run` commands against a repository that does not
declare the capability.

## Overview

This skill provides guidance for creating and managing K6 load tests for
both REST and GraphQL APIs. GraphQL scenarios apply only when
`framework.graphql` is true. IRI-handling guidance applies when
`framework.api_platform` is set (non-`false`).

## Core Principles

### 1. Individual Endpoint Testing

- Create separate test scripts for each endpoint (REST) or operation (GraphQL)
- Follow the pattern: `createResource.js`, `getResource.js`, `updateResource.js`, `deleteResource.js`
- For GraphQL (when `framework.graphql` is true): `graphQLCreateResource.js`, `graphQLGetResource.js`, etc.
- Avoid composite/random operation scripts for better debugging and clarity

### 2. Deterministic Testing

- **NEVER use random operations** in load tests
- Use predictable, iteration-based patterns (`__ITER % N`)
- Ensure reproducible results for reliable performance analysis

### 3. Proper Resource Management

- Implement `setup()` function to create test dependencies
- Implement `teardown()` function to clean up test data
- Use proper IRI handling for REST APIs (API Platform resources)
- Use proper ID handling for GraphQL queries/mutations

### 4. Automatic Integration

- All test scripts are automatically discovered from the harness scripts
  directory (conventionally `tests/Load/scripts/`)
- No separate commands needed — GraphQL and REST tests run together
- Invoke load tests only through the profile's `make` target map

## Available Commands

The full suite runs through the target mapped by `make.load_tests`.
Repositories that adopt the canonical K6 harness also expose
level-specific variants (smoke/average/stress/spike), a single-scenario
runner, and a scenario discovery script — find them in the repository
Makefile next to the `make.load_tests` target. Canonical upstream
layout:

```bash # profile-example
make load-tests            # make.load_tests → all load tests (REST + GraphQL)
make smoke-load-tests      # minimal load (2-5 VUs, 10s)
make average-load-tests    # normal load (10-20 VUs, 2-3 min)
make stress-load-tests     # high load (30-80 VUs, 5-15 min)
make spike-load-tests      # extreme load (100-200 VUs, 1-3 min)
make execute-load-tests-script scenario=createCustomer    # one scenario
./tests/Load/get-load-test-scenarios.sh                   # list scenarios
```

**Prerequisites**: service containers running (target mapped by
`make.start`); harness `.env` pointing `BASE_URL` at the running service
(see [reference/configuration.md](reference/configuration.md)).

## Quick Start Guide

### 1. Choose Test Type

- **REST API**: Use for HTTP endpoint testing
- **GraphQL**: Use for GraphQL query/mutation testing — only when
  `framework.graphql` is true

### 2. Create Test Script

```bash
# Create in the harness scripts directory
touch tests/Load/scripts/yourOperation.js         # REST
touch tests/Load/scripts/graphQLYourOperation.js  # GraphQL
```

### 3. Follow Script Structure

Use the script-structure template and operation patterns for your test type:

- REST: [reference/rest-api-patterns.md](reference/rest-api-patterns.md)
- GraphQL (when `framework.graphql` is true):
  [reference/graphql-patterns.md](reference/graphql-patterns.md)

The **Quick Reference** below summarizes the step order; **Supporting Files**
cover configuration, Utils extension, and troubleshooting.

### 4. Add Configuration

Update the scenario configuration file (`tests/Load/config.json.dist`)
with the script's VU/duration parameters — see
[reference/configuration.md](reference/configuration.md).

### 5. Test and Verify

- Run the smoke level first (lowest-load variant of `make.load_tests`)
- Verify cleanup: check no test data remains in the database

## Load Test Levels

| Level       | VUs     | Duration     | Success Rate | Purpose                           |
| ----------- | ------- | ------------ | ------------ | --------------------------------- |
| **Smoke**   | 2-5     | 10 seconds   | 100%         | Basic functionality verification  |
| **Average** | 10-20   | 2-3 minutes  | >99%         | Normal traffic simulation         |
| **Stress**  | 30-80   | 5-15 minutes | >95%         | Find breaking points              |
| **Spike**   | 100-200 | 1-3 minutes  | >90%         | Test resilience under sudden load |

## Common Pitfalls

### Don't Do This

```javascript
// Random operations - unpredictable results
const operation = Math.random();

// Hardcoded test data
const email = 'test@example.com'; // Will cause conflicts

// Missing cleanup in teardown()
```

### Do This Instead

```javascript
// Deterministic operations
const operationIndex = __ITER % 3;

// Dynamic test data
const email = `test_${Date.now()}_${randomString(6)}@example.com`;

// Proper cleanup
export function teardown(data) {
  // Clean up all created resources
}
```

## Checklist for New Load Tests

### Before Creating

- [ ] Identify the specific endpoint/operation to test
- [ ] Determine if REST or GraphQL (GraphQL only when `framework.graphql` is true)
- [ ] Identify required dependencies (related resources the endpoint needs)
- [ ] Plan realistic test data generation
- [ ] Choose appropriate load test parameters

### During Creation

- [ ] Follow the appropriate script structure template
      ([reference/rest-api-patterns.md](reference/rest-api-patterns.md) for
      REST, [reference/graphql-patterns.md](reference/graphql-patterns.md) for
      GraphQL)
- [ ] Implement proper setup/teardown functions
- [ ] Use deterministic operations (no random)
- [ ] Handle IRI/ID paths correctly
- [ ] Add configuration to the scenario config file
- [ ] Use proper naming: `graphQL` prefix for GraphQL tests

### After Creation

- [ ] Verify automatic discovery via the harness scenario-listing script
- [ ] Test with smoke load first
- [ ] Verify 100% success rate in controlled environment
- [ ] Check that cleanup works properly (no leftover data)
- [ ] Document any special requirements

## Performance Monitoring

### Success Criteria

- **Smoke Tests**: 100% success rate
- **Average Tests**: >99% success rate
- **Stress Tests**: >95% success rate
- **Response Times**: <threshold configured per endpoint

### Key Metrics

- HTTP status codes (201, 200, 204 for success)
- Response times (avg, p95, p99)
- Error rates and types
- Throughput (requests per second)

## Supporting Files

For detailed patterns, examples, and reference documentation:

- **[reference/rest-api-patterns.md](reference/rest-api-patterns.md)** - REST script-structure template and CRUD operation patterns
- **[reference/graphql-patterns.md](reference/graphql-patterns.md)** - GraphQL script-structure template and query/mutation patterns
- **[reference/configuration.md](reference/configuration.md)** - Configuration patterns and guidelines
- **[reference/utils-extensions.md](reference/utils-extensions.md)** - Extending the Utils class
- **[reference/troubleshooting.md](reference/troubleshooting.md)** - Common issues and solutions

For functional (unit/integration/E2E/mutation) testing, use the
[testing-workflow skill](../testing-workflow/SKILL.md) instead.

## Quick Reference

### REST API Test Structure

1. Import required modules
2. Create Utils and ScenarioUtils instances
3. Export options from scenarioUtils
4. Implement setup() for dependencies
5. Implement default function for main test logic
6. Implement teardown() for cleanup
7. Use IRI format for resource references (when `framework.api_platform` is set)

### GraphQL Test Structure

1. Import required modules
2. Create Utils and ScenarioUtils instances
3. Export options from scenarioUtils
4. Use REST API in setup() for faster dependency creation
5. Use GraphQL in default function for actual testing
6. Use REST API in teardown() for faster cleanup
7. Handle full IRI format in queries/mutations
8. Validate response.data and check for errors

---

This skill ensures consistent, professional, and effective load testing
for both REST and GraphQL APIs of any profiled PHP backend service.
