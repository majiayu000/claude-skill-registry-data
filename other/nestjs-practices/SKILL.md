---
name: nestjs-practices
description: >
  Apply NestJS practices for modules, services, repositories, dependency injection, configuration
  with @nestjs/config, namespaced registerAs factories, application-context registration, typed
  injection, dynamic module options, external configuration sources, bootstrap, logging and errors,
  external contracts, data integration, and standalone application contexts. Use this skill whenever
  organizing NestJS configuration, reviewing @nestjs/config usage, creating typed configuration
  namespaces, separating worker and API configuration, validating dynamic module options, isolating
  process.env access, handling secrets, or performing broader NestJS architecture and runtime work.
  Do not use this skill for end-to-end test design, test-runner orchestration, E2E fixtures, E2E
  infrastructure lifecycle, or black-box testing against a deployed API without NestJS source
  access.
license: MIT
metadata:
  author: AutanaSoft
  version: '0.4.0'
---

# NestJS Practices

Apply the smallest relevant set of NestJS decision cards. The cards own normative guidance,
examples, exceptions, and sources; this entry point activates the catalog and routes the work.

## When to Apply

Use this skill when:

- Designing NestJS modules, services, repositories, dependency injection, configuration, bootstrap,
  logging, error handling, external contracts, data integration, or standalone application contexts.
- Reviewing `@nestjs/config`, dynamic module options, typed configuration namespaces, workers, or
  CLI processes.
- Do not use it for end-to-end test design, test-runner orchestration, E2E fixtures, or E2E
  infrastructure lifecycle.
- Do not use it for black-box testing against a deployed API without NestJS source access or for
  generic TypeScript work without a NestJS-specific decision.

## Workflow

1. Identify the NestJS concern and load only the matching cards in the decision map.
2. Apply the cards using the project's existing architecture, names, providers, clients, and
   commands.
3. Run the relevant repository checks for the NestJS changes.

## Rule Categories by Priority

| Priority | Category              | Impact        | Prefix    |
| -------- | --------------------- | ------------- | --------- |
| 1        | Configuration         | CRITICAL/HIGH | `config-` |
| 2        | Application design    | CRITICAL/HIGH | `arch-`   |
| 3        | External contracts    | HIGH          | `api-`    |
| 4        | Diagnostics           | HIGH          | `error-`  |
| 5        | NestJS data lifecycle | HIGH          | `nestjs-` |

## Quick Reference

Load the first matching card for the decision. Each physical reference card appears once in this
map.

### 1. Configuration (CRITICAL/HIGH)

- `config-locate-configuration-by-ownership` - Locate configuration by architectural ownership.
- `config-build-and-validate-namespaced-configuration` - Build and validate complete namespaced
  configuration.
- `config-register-configuration-per-application-context` - Register configuration for each
  application context.
- `config-inject-namespaced-configuration` - Inject a typed configuration namespace.
- `config-isolate-external-configuration-sources` - Isolate environment and secret sources.
- `config-validate-dynamic-module-options` - Validate public dynamic module options at registration.
- `config-avoid-hardcoded-secrets` - Keep secrets out of source code and diagnostics.

### 2. Application Design (CRITICAL/HIGH)

- `arch-use-flow-coordinators` - Use coordinators for cross-module workflows.
- `arch-service-repository-responsibility` - Keep services focused on one domain.
- `arch-use-repository-pattern` - Keep Drizzle persistence access in repositories.
- `arch-use-standalone-application` - Use an application context for non-HTTP processes.

### 3. External Contracts (HIGH)

- `api-use-external-service-contracts` - Validate external service inputs and responses.

### 4. Diagnostics (HIGH)

- `error-use-structured-logging` - Use structured runtime logging.
- `error-handle-unknown-catches` - Narrow caught errors before reading properties.

### 5. NestJS Data Lifecycle (HIGH)

- `nestjs-use-drizzle-database-module` - Provide Drizzle through a database module.

## How to Use

Identify the applicable category and read only the card that owns the decision before applying it.
Follow links from that card only when the task crosses into a related concern; do not copy its
normative guidance into this entry point.
