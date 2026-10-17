---
name: tests
description: "Skill for the Tests area of paddock. 44 symbols across 6 files."
---

# Tests

44 symbols | 6 files | Cohesion: 94%

## When to Use

- Working with code in `tests/`
- Understanding how setDefaultWorkspaceSwitcherFlag, enableWorkspaceSwitcherFlagForE2E, resetProductLineVisualFixtures work
- Modifying tests-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `tests/helpers.ts` | getE2EDbPath, setDefaultWorkspaceSwitcherFlag, waitForWorkspaceSwitcherFlag, enableWorkspaceSwitcherFlagForE2E, sqlPlaceholders (+32) |
| `tests/mcp-server.spec.ts` | mcpCall, mcpRequest, mcpTool |
| `tests/product-line-switcher-ui.spec.ts` | prepareAuthenticatedPage |
| `tests/feature-flags-admin-ui.spec.ts` | prepareAuthenticatedPage |
| `tests/e2e/spec-007-ui-visual.spec.ts` | prepareAuthenticatedSpec007Page |
| `tests/e2e/spec-008/governance-fixtures.ts` | loginAsGovernanceOperator |

## Entry Points

Start here when exploring this area:

- **`setDefaultWorkspaceSwitcherFlag`** (Function) — `tests/helpers.ts:45`
- **`enableWorkspaceSwitcherFlagForE2E`** (Function) — `tests/helpers.ts:112`
- **`resetProductLineVisualFixtures`** (Function) — `tests/helpers.ts:162`
- **`resetFeatureFlagAdminVisualFixture`** (Function) — `tests/helpers.ts:212`
- **`seedProductLineE2EData`** (Function) — `tests/helpers.ts:407`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `setDefaultWorkspaceSwitcherFlag` | Function | `tests/helpers.ts` | 45 |
| `enableWorkspaceSwitcherFlagForE2E` | Function | `tests/helpers.ts` | 112 |
| `resetProductLineVisualFixtures` | Function | `tests/helpers.ts` | 162 |
| `resetFeatureFlagAdminVisualFixture` | Function | `tests/helpers.ts` | 212 |
| `seedProductLineE2EData` | Function | `tests/helpers.ts` | 407 |
| `cleanup` | Function | `tests/helpers.ts` | 417 |
| `getWorkflowTestWorkspaceId` | Function | `tests/helpers.ts` | 558 |
| `productLineScopedPath` | Function | `tests/helpers.ts` | 572 |
| `createTestTask` | Function | `tests/helpers.ts` | 500 |
| `createTestAgent` | Function | `tests/helpers.ts` | 519 |
| `createTestWorkflow` | Function | `tests/helpers.ts` | 538 |
| `deleteTestWorkflow` | Function | `tests/helpers.ts` | 551 |
| `workflowTestPath` | Function | `tests/helpers.ts` | 576 |
| `createTestWebhook` | Function | `tests/helpers.ts` | 582 |
| `createTestAlert` | Function | `tests/helpers.ts` | 604 |
| `createTestProject` | Function | `tests/helpers.ts` | 633 |
| `createTestUser` | Function | `tests/helpers.ts` | 655 |
| `freezeProductLineVisualClock` | Function | `tests/helpers.ts` | 158 |
| `loginAsE2EAdmin` | Function | `tests/helpers.ts` | 260 |
| `dismissOnboardingForE2E` | Function | `tests/helpers.ts` | 311 |

## How to Explore

1. `gitnexus_context({name: "setDefaultWorkspaceSwitcherFlag"})` — see callers and callees
2. `gitnexus_query({query: "tests"})` — find related execution flows
3. Read key files listed above for implementation details
