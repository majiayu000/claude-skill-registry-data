---
name: refactor-tests
description: Refactor test files to improve behavioral coverage, clarity, structure, assertions, fixture setup, mocking strategy, and remove implementation-detail or low-value tests. Use when asked to clean up, declutter, consolidate, or improve tests.
---

# Test Refactor

Ask the user for the test file to refactor. Work on one test file at a time.

## Process

Work through these steps in order, making a separate commit for each step that makes changes:

### 0. **Count cyclomatic complexity (DO FIRST)**
   - Read the source file being tested
   - Count decision points: `if`, `else`, `for`, `while`, `case`, `catch`, `&&`, `||`, `?:`
   - Cyclomatic complexity = 1 + decision points
   - This is your TARGET test count (approximately)
   - Report: "Cyclomatic complexity: ~N paths, currently M tests"
   - If M >> N, tests need consolidation

### 1. **Identify public API and remove tests for internals**
   - First: identify what the PUBLIC API is (what external callers use)
   - Functions exported only to enable testing are NOT public API - make them private
   - Private methods tested indirectly through public interface
   - If function A only calls function B internally, test through A, make B private
   - Example: `buildBotRequest` calls `buildToolsForAgent` → test through `buildBotRequest`, unexport `buildToolsForAgent`

### 2. **Remove tests for getters/trivial code**
   - Only test core behavior, not trivial getters/setters
   - Remove noise that doesn't provide safety net

### 3. **Remove implementation detail tests**
   - Audit/logging callbacks → implementation detail, remove
   - Caching behavior → implementation detail, remove
   - Tests that verify Promise.all/parallel execution → testing the language, remove
   - If behavior matters to users, keep; if it's internal wiring, remove

### 4. **Consolidate to match cyclomatic complexity**
   - Target: ~1 test per code path through the function
   - Merge tests covering same code path with different assertions
   - Example: "returns response" + "propagates nestedTools" + "propagates suggestedActions" → one test checking all output fields
   - Example: "MCP returns error" + "MCP throws exception" → one test for error handling

### 5. **Fix test anti-patterns**
   - Tests testing implementation → refactor to test behavior
   - Conditional logic in tests → split into separate tests
   - Order-dependent tests → make independent
   - `toHaveBeenCalledWith` on non-void functions → stub return value instead (Query Command Separation: queries are stubs, commands are mocks)
   - `expect(arr).toHaveLength(n)` followed by element check → remove length check, let element assertion fail directly
   - **Imperative scaffolding inside tests** — scan test bodies (arrange AND assert sections) for:
     - `for` loops building lookup maps/lists for assertions
     - `new HashMap<>()` / `new ArrayList<>()` followed by puts/adds purely to enable an assertion
     - Manual element lookup by index (`list.get(0)`, `list.get(1)`)
     - Reflection (`setAccessible`, `Field.set`) to populate test fixtures — replace with builders/setters on the production type
     Replace with fluent assertion idioms (AssertJ `filteredOn(...).singleElement().satisfies(...)`, `extracting(...)`, `anySatisfy`; Jest `arrayContaining`/`objectContaining`) or stream collectors (`Collectors.toMap`).
   - If test level seems wrong for component, ASK USER with recommendation

### 6. **Improve test data**
   - Move large test objects to test data builders
   - Keep only relevant data in each test
   - Keep test data close to test for readability

### 7. **Improve test names/assertions (ASK USER FIRST)**
   - Present 3 options for unclear tests:
     1. Rename test to describe behavior
     2. Improve assertion messages
     3. Both
   - Wait for user decision

### 8. **Refactor test structure**
   - Use AAA pattern (Arrange-Act-Assert)
   - Separate sections with blank lines (NO comments)
   - Extract helper functions for duplicated setup (NOT beforeEach)
   - Use beforeEach only for variables scoped to describe block

### 9. **Review mocking strategy**
   - Acceptance tests: Use mock web servers (http), TestContainers (DB)
   - Unit tests: Only mock external dependencies (filesystem, random, time, http, DB)
   - Prefer test doubles over mocking frameworks
   - Use real objects when possible

After EACH step:
- Run tests automatically
- If tests fail, revert the change immediately
- Commit using: `. t <brief description>`

## Testing Philosophy

- TDD: Write tests first
- Acceptance tests for behavior, unit tests for complex pure functions
- Acceptance level depends on component:
  - Microservices: Event or HTTP level
  - UI: Route-level component rendering
- **Test count ≈ cyclomatic complexity** (one test per code path)

## Output

- If no refactoring needed, report "No test refactoring needed"
- Otherwise provide brief summary (e.g., "Reduced 15 → 8 tests to match cyclomatic complexity, removed implementation detail tests")

## Commit Format

Use Arlo's Commit Notation (ACN):
- `. t remove tests for private methods`
- `. t consolidate tests to match cyclomatic complexity`
- `. t remove implementation detail tests`
