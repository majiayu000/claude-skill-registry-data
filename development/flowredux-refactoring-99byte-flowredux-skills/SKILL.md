---
name: flowredux-refactoring
description: Refactor complex Android/KMP state management code to use FlowRedux state machine pattern. Use this when developers need to transform tangled state logic, multiple LiveData/StateFlow sources, or callback-heavy code into a clean, testable state machine architecture.
---

# FlowRedux State Management Refactoring

For concrete examples and code samples, see [examples.md](examples.md).

## Instructions

When a developer provides Android/KMP code with complex state management, follow these steps:

### Phase 1: Comprehensive Feature Analysis (CRITICAL - DO NOT SKIP)

**1.1 UI Inventory - Map All Interactive Elements**
Before any refactoring, create a complete inventory:
- ✅ List every button, toggle, input field, and clickable element
- ✅ Document every menu option, dropdown, dialog, and bottom sheet
- ✅ Identify swipe gestures, long-press actions, and other interactions
- ✅ Note system events (lifecycle, network changes, permissions)

**Output:** A checklist of ALL user actions this screen supports.

**1.2 Data Flow Mapping**
- Map all data sources (API, database, cache, shared preferences)
- Trace data transformations and business logic
- Identify all async operations and their dependencies
- Document error scenarios for each data operation

**1.3 State Transition Graph**
Create a comprehensive state diagram showing:
- All possible states the screen can be in
- Triggers for each state transition (user actions, events, responses)
- Invalid state transitions that should be prevented
- Edge cases and race conditions

**Output:** A complete state machine diagram or table.

### Phase 2: Test-Driven Design (TDD Approach)

**2.1 Design Test Cases First**
Before writing ANY implementation code:
- Write test cases for EVERY user action identified in Phase 1
- Write test cases for EVERY state transition
- Write test cases for error scenarios and edge cases
- Write test cases for concurrent actions (e.g., delete while loading)

**2.2 Test Case Format**
```kotlin
@Test
fun `when [action] in [current state], should transition to [expected state]`() {
    // Given: initial state
    // When: action occurs
    // Then: verify new state
}
```

**2.3 Leverage MVI Observability**
Use the state machine's deterministic nature:
- Every action → state transition is predictable and testable
- No hidden state or side effects
- Time-travel debugging possible
- Easy to reproduce bugs by replaying actions

**Output:** Complete test suite BEFORE implementation.

### Phase 3: Implement State Machine

**3.1 Define Components Based on Analysis**
- Create State sealed class covering ALL states from Phase 1
- Create Action sealed class for ALL user actions and events
- Create SideEffect handlers for async operations
- Ensure every test case from Phase 2 is covered

**3.2 Implement State Transitions**
- Write reducers for each state transition
- Implement side effect handlers with proper error handling
- Ensure all edge cases from test suite are handled

**3.3 Verify Against Tests**
- Run test suite continuously during implementation
- Use failing tests to discover missing functionality
- Refactor until all tests pass

### Phase 4: Bug Detection via Tests

**4.1 Test-Driven Bug Finding**
When bugs are discovered:
- Write a failing test that reproduces the bug
- Fix the state machine to make the test pass
- Verify no regression in existing tests

**4.2 Missing Functionality Detection**
Use test coverage to find:
- Unhandled user actions
- Missing state transitions
- Unhandled error cases
- Race conditions

### Phase 5: Code Generation & Documentation

**5.1 Generate Complete Implementation**
- All State, Action, and SideEffect sealed classes
- Complete state machine with all transitions
- Full test suite with explanations
- Integration guide for ViewModel

**5.2 Provide Traceability**
- Map each test case back to original requirements
- Document which states/actions handle which UI elements
- Create a state transition reference table

## Examples

See [examples.md](examples.md) for detailed code examples including:
- Simple list loading (before/after comparison)
- Complex multi-action scenarios (pagination, deletion, sorting)
- Complete test suites
- Common patterns and anti-patterns
- Migration guide

## Key Principles

1. **Feature-First Analysis**: Map ALL UI elements and interactions before coding
2. **State Machine Design**: Create complete state transition graph upfront
3. **Test-Driven Development**: Write tests BEFORE implementation
4. **MVI Observability**: Leverage deterministic state transitions for testing
5. **Bug Prevention**: Use failing tests to drive bug fixes and find missing features
6. **Single Source of Truth**: All state in one place
7. **Immutability**: States are immutable data classes
8. **Type Safety**: Sealed classes prevent invalid states

## Engineering Best Practices

### Practice 1: Comprehensive Feature Inventory
**Before writing any code:**
```markdown
## Feature Checklist
- [ ] Load videos button
- [ ] Pull to refresh
- [ ] Delete video (with swipe)
- [ ] Undo delete
- [ ] Play video
- [ ] Sort options (date, title)
- [ ] Filter (watched/unwatched)
- [ ] Empty state
- [ ] Error retry
- [ ] Offline mode indicator
```

**Why:** Ensures no functionality is missed in refactoring.

### Practice 2: State Transition Table
**Create before implementation:**
```
| Current State | Action         | Next State      | Side Effect       |
|---------------|----------------|-----------------|-------------------|
| Initial       | Load           | Loading         | Fetch from API    |
| Loading       | Success        | Content         | None              |
| Loading       | Error          | Error           | None              |
| Content       | Refresh        | Refreshing      | Fetch from API    |
| Content       | Delete(id)     | Content         | Delete from DB    |
| Content       | Sort(type)     | Content         | Resort locally    |
```

**Why:** Makes state machine design explicit and reviewable.

### Practice 3: Test-First Development
**Write tests before implementation:**
```kotlin
class WatchLaterStateMachineTest {
    @Test
    fun `given Initial, when Load action, should transition to Loading`() {
        val machine = createStateMachine()
        machine.dispatchAction(Action.Load)
        assertEquals(State.Loading, machine.state.value)
    }

    @Test
    fun `given Loading, when data arrives, should transition to Content`() {
        // Test the actual behavior
    }

    @Test
    fun `given Content with items, when Delete action, should remove item optimistically`() {
        // Test optimistic update
    }

    @Test
    fun `given two simultaneous Delete actions, should handle race condition`() {
        // Test edge cases
    }
}
```

**Why:** Tests document expected behavior and catch regressions.

### Practice 4: Use Tests to Find Missing Features
**When reviewing implementation:**
```kotlin
// Run test coverage report
// Missing coverage = missing functionality

@Test
fun `when offline and user triggers refresh, should show offline message`() {
    // This test fails? → Feature is missing!
}

@Test  
fun `when deleting last item, should show empty state`() {
    // This test fails? → Edge case not handled!
}
```

**Why:** Test-driven approach reveals gaps in requirements.

## Common Patterns

### Pattern: Retry Logic
See [examples.md](examples.md) for detailed pattern implementations.

### Pattern: Optimistic Updates
See [examples.md](examples.md) for detailed pattern implementations.

### Pattern: Side Effect with Error Handling
See [examples.md](examples.md) for detailed pattern implementations.

## Output Format

For each refactoring request, provide:

1. **Feature Analysis**:
   - Complete UI element inventory
   - User action checklist
   - System event list
   
2. **Data Flow Diagram**:
   - All data sources and destinations
   - Transformation pipeline
   - Error scenarios

3. **State Machine Design**:
   - State transition table or diagram
   - All states, actions, and side effects listed
   - Edge cases and race conditions identified

4. **Test Suite** (MUST PROVIDE BEFORE IMPLEMENTATION):
   - Test cases for every user action
   - Test cases for every state transition
   - Test cases for error scenarios
   - Test cases for edge cases and race conditions
   
5. **Implementation Code**:
   - All sealed classes (State, Action, SideEffect)
   - Complete state machine implementation
   - Proper error handling and coroutine management
   
6. **Integration Guide**:
   - How to use in ViewModel
   - How to collect state in UI
   - Migration steps if needed

7. **Test Execution Plan**:
   - How to run tests
   - How to use tests to find bugs
   - How to add tests for new features

## Workflow Summary

```
1. Analyze → List ALL features and interactions
            ↓
2. Design  → Create state transition graph
            ↓
3. Test    → Write test cases for EVERYTHING
            ↓
4. Verify  → Check test coverage matches feature list
            ↓
5. Implement → Write state machine to pass tests
            ↓
6. Debug   → Use failing tests to find/fix bugs
            ↓
7. Deliver → Provide complete, tested code
```

Always prefer clarity and completeness over brevity. Include proper error handling and coroutine scope management. Emphasize the test-driven approach and use of MVI's observability for quality assurance.
