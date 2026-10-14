---
name: craft-fake
description: Crafting fakes. Let consumers test package interactions without touching internals.
---

# Skill: Craft Fake

> "A package without a fake forces every consumer to write a mock. That's a bug."

## The Standard

1. **Static `::fake()` on the Facade**: The canonical pattern. Swap the real implementation with a recording test double via the facade. The fake implements the same interface as the real service, records interactions instead of executing them, and provides assertion methods. Return the fake for optional assertion chaining.

2. **The Fake Class Contract**: Every fake follows the same anatomy. Implement the real service's interface. Accept the real implementation as a constructor parameter (for passthrough when needed). Record dispatched/sent/queued calls into an internal collection. Expose assertion methods: `assertDispatched()`, `assertDispatchedTimes()`, `assertNotDispatched()`, `assertNothingDispatched()`.

3. **Assertion Naming Convention**: Follow Taylor's naming: `assert{Action}($target)`, `assert{Action}Times($target, $count)`, `assertNot{Action}($target)`, `assertNothing{Action}ed()`. The verb matches the domain: dispatched for jobs, sent for mail, notified for notifications, stored for storage, requested for HTTP.

4. **Closure Filters on Assertions**: Accept a closure as the second argument to filter assertions. The closure receives the recorded item and returns a boolean. This lets consumers assert against specific payloads without exact matching.

5. **`preventStray()` Safety Net**: Provide a method that throws when unrecorded interactions occur. Prevents tests from accidentally hitting real services. Mirror the `Http::preventStrayRequests()` pattern.

6. **Fluent Fakes (Livewire Pattern)**: When the package provides a testable component or builder, consider the `::test()` pattern instead of `::fake()`. The test method creates the component, records interactions, and chains assertions in a single fluent call. This is the Livewire approach -- the test IS the fake.

7. **State Reset**: Fakes must reset state between tests. Use `::clearResolvedInstances()` on the facade, or provide an explicit `::reset()` method. Leaked state between tests is a category of bugs your consumers should never encounter.

8. **Custom Expectations for Pest**: Ship custom Pest expectations alongside fakes. Register them in a test helper file consumers can import. Domain-specific assertions are a feature, not an afterthought.

## The Anti-Patterns

| Don't                                               | Do                                      | Why                                                         |
|-----------------------------------------------------|-----------------------------------------|-------------------------------------------------------------|
| Force consumers to mock your internals              | Ship a `::fake()` on the facade         | Mocks couple to implementation, fakes couple to behavior    |
| Return void from `::fake()`                         | Return the fake instance                | Enables assertion chaining: `$fake = Bus::fake()`           |
| Only provide `assertDispatched()`                   | Provide the full assertion quartet      | `assertNotDispatched` and `assertNothing` catch regressions |
| Hardcode assertions to exact matches                | Accept closure filters                  | Consumers need flexible matching                            |
| Leak fake state between tests                       | Reset on `setUp` or provide `::reset()` | Coupled tests are fragile tests                             |
| Build fakes without implementing the real interface | Implement the same contract             | The fake must be a drop-in replacement                      |
| Skip `preventStray()`                               | Provide opt-in stray prevention         | Catches accidental real service calls                       |

## Real-World Examples

See [examples.md](examples.md).
