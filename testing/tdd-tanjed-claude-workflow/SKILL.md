---
name: tdd
description: >
  Write unit and integration tests for an existing file, class, or feature.
  Auto-invoke when the user says "write tests for", "add test coverage",
  "test this service", or "what's not tested here".
allowed-tools: Read, Write, Glob, Grep, Bash
argument-hint: <file-path> [unit|integration|both]
---
 
# TDD Skill
 
Write tests for the specified file or feature. Tests test **behaviour**, not implementation.
 
## Input
- `$ARGUMENTS` — target file path + optional scope (`unit`, `integration`, `both`)
- Default scope if not specified: `both`
 
## Step 1 — Read and Understand
- Read the target file fully
- Identify: what are the public methods / exported functions?
- Identify: what are the dependencies? (for mocking in unit tests)
- Identify: what are the expected behaviours for each public method?
 
## Step 2 — Detect the Stack
Check for `package.json` (Node.js/Jest/Vitest), `go.mod` (Go/testify), `composer.json` (PHP/Pest or PHPUnit).
Read the matching process file for test conventions:
- Node.js → `@~/.claude/process/node_process.md`
- Golang → `@~/.claude/process/go_process.md`
- Laravel → `@~/.claude/process/php_process.md`
 
## Step 3 — Plan the Test Cases
Before writing any code, list the test cases in this format:
 
```
[MethodName]
  ✓ should return X when Y
  ✓ should throw NotFoundError when Z is missing
  ✓ should call repository.save() once when input is valid
  ✓ should not call repository.save() when validation fails
```
 
Present this plan and wait for approval before writing tests.
 
## Step 4 — Write Unit Tests
Rules:
- Mock ALL external dependencies (repositories, HTTP clients, queues, etc.)
- Test one behaviour per test case — one logical assertion focus
- Test naming: `it('should <behaviour> when <condition>')`
- Set up mocks in `beforeEach`, reset in `afterEach`
- Assert on outputs and observable side effects — not on internal state
- Test both happy path AND all meaningful error/edge cases
 
### Node.js (Jest/Vitest)
```typescript
// src/services/__tests__/OrderService.test.ts
describe('OrderService', () => {
  let sut: OrderService;
  let mockRepo: jest.Mocked<IOrderRepository>;
 
  beforeEach(() => {
    mockRepo = { findById: jest.fn(), save: jest.fn() };
    sut = new OrderService(mockRepo);
  });
 
  it('should return order when id exists', async () => { ... });
  it('should throw OrderNotFoundError when id does not exist', async () => { ... });
});
```
 
### Go (testify)
```go
func TestOrderService(t *testing.T) {
  tests := []struct {
    name    string
    input   string
    want    *Order
    wantErr error
  }{
    {"found", "1", &Order{ID: "1"}, nil},
    {"not found", "99", nil, ErrNotFound},
  }
  for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) { ... })
  }
}
```
 
### PHP (Pest)
```php
it('should return order when id exists', function () {
    $repo = Mockery::mock(OrderRepositoryInterface::class);
    $repo->shouldReceive('findById')->with(1)->andReturn(new Order(id: 1));
    $sut = new OrderService($repo);
    expect($sut->get(1))->toBeInstanceOf(Order::class);
});
```
 
## Step 5 — Write Integration Tests (if in scope)
- Use a real test database (never mock the DB in integration tests)
- Seed required data in `beforeEach` / `setUp`
- Clean up in `afterEach` / `tearDown`
- Test the repository layer directly — does the data actually persist and query correctly?
 
## Output
- Write test files to the correct location per stack conventions
- Print a summary: number of test cases written, coverage of public methods, any behaviours that could not be tested without additional refactoring (and why)
