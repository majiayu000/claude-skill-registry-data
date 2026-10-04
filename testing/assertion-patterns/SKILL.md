---
name: assertion-patterns
description: Real output verification vs mock calls. Use when transforming T1-T4 violating tests to verify observable behavior.
user-invocable: false
allowed-tools:
  - Read
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Assertion Patterns

## Purpose

Transform T1-T4 violating assertions into real behavior verification. This skill provides
pattern libraries for converting mock-based tests to tests that verify observable output.

## When to Use

Load this skill when:
- Rewriting tests flagged by test-audit
- Generating verification scripts via bulwark-verify skill
- Implementing test-audit Step 7 rewrites

---

## Prerequisite Checks (T0) - CRITICAL

**Before checking T1-T4 violations, verify these prerequisites. Tests failing these checks
are "testing nothing real" - they pass but provide zero confidence.**

### T0.1: Production Module Imports

Test files MUST import functions from actual production modules.

| Valid | Invalid |
|-------|---------|
| `import { calculate } from '../src/calculator'` | Function defined within test file |
| `from calculator import add` | `def add(a, b): return a + b` in test |

**Detection:**
- Scan test file for function definitions
- Check if tested functions are imported vs defined inline
- Flag if test calls functions not imported from production code

**Violation Response:**
> "Test defines production logic inline. Move `{function_name}` to production module
> and import it. Tests should verify production code, not self-defined code."

### T0.2: Separation of Concerns

Test files MUST NOT contain functions representing production logic.

**Allowed in test files:**
- Test functions (`test_*`, `it()`, `describe()`)
- Test helpers/fixtures (`make_*`, `create_*`, `setup_*`)
- Mock factories (`mock_*`, `fake_*`, `stub_*`)
- Pytest fixtures (`@pytest.fixture`)

**Not allowed:**
- Business logic functions
- Utility functions that should be in production
- Any function that would make sense in `src/`

**Detection:**
- Identify all function definitions in test file
- Check naming patterns against allowed prefixes
- Flag functions that don't match test/helper patterns

### T0.3: Function Naming Conventions

Functions in test files should follow specific naming patterns.

| Legitimate Prefixes | Purpose |
|---------------------|---------|
| `test_*` | Test functions (pytest) |
| `_*` (underscore) | Private helpers |
| `pytest_*` | Pytest hooks |
| `make_*`, `create_*` | Factory helpers |
| `mock_*`, `fake_*`, `stub_*` | Mock factories |
| `setup_*`, `teardown_*` | Lifecycle helpers |

**Any other function definition raises suspicion** - likely production code incorrectly
placed in test files.

---

## Pattern Categories

### 1. Function Call Verification

| Anti-Pattern (Mock) | Real Pattern |
|---------------------|--------------|
| `expect(fn).toHaveBeenCalled()` | `const result = fn(); expect(result).toBe(expected)` |
| `expect(fn).toHaveBeenCalledWith(arg)` | `const result = fn(arg); expect(result.field).toBeDefined()` |
| `jest.spyOn(module, 'fn').mockReturnValue(x)` | `const result = module.fn(); expect(result).toBe(expected)` |

**Transformation example:**
```javascript
// BEFORE (T1 violation - mocking system under test)
jest.spyOn(calculator, 'add').mockReturnValue(5);
expect(calculator.add(2, 3)).toBe(5);

// AFTER (real verification)
expect(calculator.add(2, 3)).toBe(5);  // Actually runs add()
```

### 2. Process Spawn Verification

| Anti-Pattern (Mock) | Real Pattern |
|---------------------|--------------|
| `jest.spyOn(cp, 'spawn').mockReturnValue(mockProc)` | `const proc = spawn(...); await waitForReady(proc)` |
| `expect(spawn).toHaveBeenCalled()` | `expect(await isPortOpen(PORT)).toBe(true)` |
| `expect(spawn).toHaveBeenCalledWith(cmd, args)` | `const output = execSync(cmd); expect(output).toContain(expected)` |

**Transformation example:**
```javascript
// BEFORE (T1 violation - mocking spawn)
const mockProcess = { on: jest.fn(), stdout: mockStream };
jest.spyOn(child_process, 'spawn').mockReturnValue(mockProcess);
await startProxy();
expect(child_process.spawn).toHaveBeenCalledWith('proxy', ['--port', '8080']);

// AFTER (real verification)
await startProxy();
expect(await checkPort(8080)).toBe(true);  // Port actually open
const response = await fetch('http://localhost:8080/health');
expect(response.status).toBe(200);  // Proxy actually responds
```

### 3. File Operation Verification

| Anti-Pattern (Mock) | Real Pattern |
|---------------------|--------------|
| `jest.mock('fs')` | Use real fs with temp directory |
| `expect(fs.writeFile).toHaveBeenCalled()` | `expect(fs.existsSync(path)).toBe(true)` |
| `expect(fs.readFile).toHaveBeenCalledWith(path)` | `const content = fs.readFileSync(path); expect(content).toContain('expected')` |

**Transformation example:**
```javascript
// BEFORE (T2 violation - call-only assertion)
await saveConfig(config);
expect(fs.writeFile).toHaveBeenCalled();

// AFTER (result verification)
await saveConfig(config);
expect(fs.existsSync(configPath)).toBe(true);
const saved = JSON.parse(fs.readFileSync(configPath, 'utf8'));
expect(saved.setting).toBe(config.setting);
```

### 4. HTTP Request Verification

| Anti-Pattern (Mock) | Real Pattern |
|---------------------|--------------|
| `jest.mock('node-fetch')` | Use MSW or test server |
| `expect(fetch).toHaveBeenCalledWith(url)` | `const resp = await fetch(url); expect(resp.status).toBe(200)` |
| Mock response data | Actual response from test server |

**Transformation example:**
```javascript
// BEFORE (T3 violation - mocking integration boundary)
jest.mock('node-fetch');
fetch.mockResolvedValue({ json: () => ({ id: 1 }) });
const user = await fetchUser(1);
expect(fetch).toHaveBeenCalledWith('/api/users/1');

// AFTER (real integration with MSW)
import { setupServer } from 'msw/node';
import { rest } from 'msw';

const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: req.params.id, name: 'Test User' }));
  })
);

beforeAll(() => server.listen());
afterAll(() => server.close());

const user = await fetchUser(1);  // Real fetch, intercepted at network level
expect(user.name).toBe('Test User');
```

### 5. Database Verification

| Anti-Pattern (Mock) | Real Pattern |
|---------------------|--------------|
| `expect(db.save).toHaveBeenCalled()` | `await db.save(data); const found = await db.find(id); expect(found).toBeDefined()` |
| `expect(db.delete).toHaveBeenCalledWith(id)` | `await db.delete(id); expect(await db.find(id)).toBeNull()` |
| `jest.mock('./database')` | Use test database instance |

**Transformation example:**
```javascript
// BEFORE (T2 violation - call-only)
await saveUser(user);
expect(db.insert).toHaveBeenCalledWith('users', user);

// AFTER (result verification)
await saveUser(user);
const saved = await db.findOne('users', { id: user.id });
expect(saved).toBeDefined();
expect(saved.email).toBe(user.email);
```

---

## T1-T4 Transformation Rules

### T1: Mock System Under Test -> Remove mock, verify real output

The system under test should NEVER be mocked. Remove the mock and verify actual behavior.

```javascript
// T1 violation: Mocking the function being tested
jest.spyOn(calculator, 'add').mockReturnValue(5);
expect(calculator.add(2, 3)).toBe(5);  // Always passes regardless of implementation

// Fixed: Test real implementation
expect(calculator.add(2, 3)).toBe(5);  // Fails if add() is broken
```

### T2: Call-Only Assertion -> Add result assertion

Verifying a function was called is insufficient. Verify the RESULT of that call.

```javascript
// T2 violation: Only checks call happened
await saveConfig(config);
expect(db.save).toHaveBeenCalled();  // Passes even if wrong data saved

// Fixed: Verify the actual saved data
await saveConfig(config);
const saved = await db.find(config.id);
expect(saved.value).toBe(config.value);  // Fails if wrong data saved
```

### T3: Mock Integration Boundary -> Use test infrastructure

Integration tests should test real integration. Use MSW, test servers, or in-memory DBs.

```javascript
// T3 violation: Mocking HTTP in integration test
jest.mock('node-fetch');
const data = await fetchUserData(id);  // Not testing real HTTP

// Fixed: Use MSW to intercept at network level
const server = setupServer(rest.get('/api/user/:id', handler));
const data = await fetchUserData(id);  // Real fetch, real HTTP, controlled response
```

### T3+: Broken Integration Chain -> Chain real function outputs

Integration tests should chain real outputs through the pipeline.

```javascript
// T3+ violation: Using mock data instead of real output
const mockOrder = { id: 1, items: [{ sku: 'ABC', qty: 2 }] };
await processOrder(mockOrder);  // Not testing real order creation

// Fixed: Chain real function outputs
const order = await createOrder({ sku: 'ABC', qty: 2 });  // Real order
await processOrder(order);  // Processes real order data
const result = await getOrderStatus(order.id);
expect(result.status).toBe('processed');
```

---

## Quick Reference: Violation to Pattern

| Violation | Pattern Category | Fix Strategy |
|-----------|------------------|--------------|
| T0.1 | Prerequisites | Move function to production, import it |
| T0.2 | Prerequisites | Extract non-test functions to src/ |
| T0.3 | Prerequisites | Rename or move functions |
| T1 | Function Call | Remove mock, call real function |
| T2 | Any category | Add result assertion after call |
| T3 | HTTP/DB/Process | Use MSW, test DB, or spawn real process |
| T3+ | Integration Chain | Chain real outputs, don't pass mocks |

---

## Diagnostic Output

Write diagnostic output to `logs/diagnostics/assertion-patterns-{YYYYMMDD-HHMMSS}.yaml`:

```yaml
skill: assertion-patterns
timestamp: {ISO-8601}
diagnostics:
  t0_checks:
    t0_1_imports: pass|fail
    t0_2_separation: pass|fail
    t0_3_naming: pass|fail
  patterns_applied: [T1, T2, T3]
  transformations_suggested: 3
  files_analyzed: 1
  completion_status: success
```
