---
name: hammer-quality-check
description: Runs comprehensive code quality checks for SDL3 HammerEngine including compilation warnings, static analysis (cppcheck), coding standards validation, threading safety verification, and architecture compliance. Use before commits, pull requests, or when the user wants to verify code meets project quality standards.
allowed-tools: [Bash, Read, Grep]
---

# HammerEngine Code Quality Gate

This Skill enforces SDL3 HammerEngine's quality standards as defined in `CLAUDE.md`. It performs comprehensive checks to catch issues before they reach version control.

## Quality Gate Categories

1. **Compilation Quality** - Zero warnings policy
2. **Static Analysis** - Memory safety, null pointers, threading
3. **Coding Standards** - Naming conventions, formatting
4. **Threading Safety** - Critical threading rules enforcement
5. **Architecture Compliance** - Design pattern adherence
   - 5.1 Rendering rules (no SDL_RenderClear/Present in GameStates)
   - 5.2 RAII & smart pointers
   - 5.3 Smart pointer performance (hot paths)
   - 5.4 String parameter patterns (no string_view→string conversions)
   - 5.5 Logger usage (std::format, *_IF macros)
   - 5.6 Buffer reuse (avoid per-frame allocations)
   - 5.7 UI component positioning
   - 5.8 Rendering rules (deferred transitions)
6. **Copyright & Legal** - License header validation
7. **Test Coverage** - Verify tests exist for modified code

## Detailed Checks

### 1. Compilation Quality

**Command:**
```bash
ninja -C build -v 2>&1 | grep -E "(warning|unused|error)" | head -n 100
```

**Working Directory:** `$PROJECT_ROOT/`

**Checks:**
- Count total warnings
- Categorize warning types:
  - Unused variables/parameters
  - Uninitialized members
  - Type conversion warnings
  - Shadowing warnings
  - Deprecated usage
  - Sign comparison warnings

**Quality Gate:** ✓ Zero compilation warnings required

**Common Issues:**
```cpp
// ✗ BAD
int x;  // uninitialized
void func(int unused) { }  // unused parameter

// ✓ GOOD
int x = 0;
void func([[maybe_unused]] int param) { }
```

### 2. Static Analysis (cppcheck)

**Command:**
```bash
./tests/cppcheck/cppcheck_focused.sh
```

**Or if script not available:**
```bash
cppcheck --enable=all --suppress=missingIncludeSystem \
  --std=c++20 --quiet \
  src/ include/ 2>&1
```

**Checks:**
- Memory leaks
- Null pointer dereferences
- Buffer overflows
- Use after free
- Double free
- Uninitialized variables
- Dead code / unreachable code
- Thread safety issues

**Quality Gate:** ✓ Zero critical/error severity issues

**Severity Levels:**
- **error:** Must fix (blocks commit)
- **warning:** Should fix (review required)
- **style:** Optional (improve if time permits)
- **performance:** Consider optimizing
- **information:** FYI only

### 3. Coding Standards (CLAUDE.md Compliance)

#### 3.1 Naming Conventions

**Check Commands:**
```bash
# Find potential naming violations
grep -rn "class [a-z]" src/ include/  # Classes must be UpperCamelCase
grep -rn "^[A-Z][a-z]*(" src/*.cpp    # Functions should be lowerCamelCase
```

**Standards:**

| Item | Convention | Example |
|------|-----------|---------|
| Classes/Enums | UpperCamelCase | `GameEngine`, `EntityType` |
| Functions/Variables | lowerCamelCase | `updateEntity()`, `deltaTime` |
| Member Variables | `m_` prefix | `m_entityCount` |
| Member Pointers | `mp_` prefix | `mp_renderer` |
| Constants | ALL_CAPS | `MAX_ENTITIES` |
| Namespaces | lowercase | `namespace utils` |

**Automated Checks:**
```bash
# Check for member variables without m_ prefix (in .cpp files)
grep -rn "^\s*[a-z][a-zA-Z0-9]*\s*;" src/ include/ | grep -v "m_" | grep -v "mp_"

# Check for class names starting with lowercase
grep -rn "^class [a-z]" include/
```

**Quality Gate:** ✓ All naming conventions followed

#### 3.2 Formatting Standards

**Standards:**
- **Indentation:** 4 spaces (no tabs)
- **Braces:** Allman style (braces on new line)
- **Line length:** Reasonable (no hard limit, but keep readable)

**Example:**
```cpp
// ✓ GOOD - Allman braces, 4-space indent
void GameEngine::update(float deltaTime)
{
    if (m_isRunning)
    {
        processEvents();
        updateSystems(deltaTime);
    }
}

// ✗ BAD - K&R braces, wrong indent
void GameEngine::update(float deltaTime) {
  if (m_isRunning) {
    processEvents();
  }
}
```

### 4. Threading Safety (CRITICAL)

**FORBIDDEN PATTERNS:**

#### 4.1 Static Variables in Threaded Code

**Check Command:**
```bash
# Find static variables in .cpp files (potential threading hazard)
grep -rn "static [^v].*=" src/ --include="*.cpp" | grep -v "static_cast" | grep -v "static const"
```

**Rule from CLAUDE.md:**
> **NEVER static vars in threaded code** (use instance vars, thread_local, or atomics)

**Why This is Critical:**
- HammerEngine uses separate update/render threads
- Static variables cause data races
- Non-deterministic behavior and crashes

**Example Violations:**
```cpp
// ✗ FORBIDDEN - static variable in threaded code
void AIManager::updateBehaviors()
{
    static int frameCount = 0;  // RACE CONDITION!
    frameCount++;
}

// ✓ GOOD - instance variable
class AIManager
{
    int m_frameCount = 0;  // Thread-safe with proper locking
};

// ✓ GOOD - thread_local if needed per-thread
void AIManager::updateBehaviors()
{
    thread_local int threadFrameCount = 0;
    threadFrameCount++;
}
```

**Quality Gate:** ✓ Zero static variables in threaded code (BLOCKING)

#### 4.2 Raw std::thread Usage

**Check Command:**
```bash
grep -rn "std::thread" src/ include/ | grep -v "ThreadSystem"
```

**Rule from CLAUDE.md:**
> Use ThreadSystem (not raw std::thread)

**Why:**
- ThreadSystem provides WorkerBudget priorities
- Prevents thread explosion
- Better resource management

**Quality Gate:** ✓ No raw std::thread usage

#### 4.3 Mutex Protection

**Check Command:**
```bash
# Find managers that should have mutex protection
grep -rn "class.*Manager" include/managers/
```

**For each manager, verify:**
- Has `std::mutex m_mutex;` member
- Update functions use `std::lock_guard<std::mutex> lock(m_mutex);`
- Render access uses proper locking

**Quality Gate:** ✓ All managers have proper mutex protection

### 5. Architecture Compliance

#### 5.1 No Background Thread Rendering

**Check Command:**
```bash
# Find potential rendering calls outside main render function
grep -rn "SDL_Render" src/ | grep -v "GameEngine::render" | grep -v "//.*SDL_Render"
```

**Rule from CLAUDE.md:**
> Render (main thread only, double-buffered)

**Quality Gate:** ✓ No rendering outside GameEngine::render()

#### 5.2 RAII & Smart Pointers

**Check Command:**
```bash
# Find raw new/delete usage (prefer smart pointers)
grep -rn "new " src/ include/ | grep -v "std::make_" | grep -v "//"
grep -rn "delete " src/ include/ | grep -v "//"
```

**Rule from CLAUDE.md:**
> RAII + smart pointers

**Prefer:**
- `std::unique_ptr` for exclusive ownership
- `std::shared_ptr` for shared ownership
- `std::make_unique` / `std::make_shared` for creation

**Quality Gate:** ✓ Minimal raw new/delete (exceptions allowed for SDL resources)

#### 5.3 Smart Pointer Performance (CRITICAL for Hot Paths)

**Background:**
Commit a8aa267e fixed severe performance issues from unnecessary shared_ptr usage in batch processing. Shared_ptr copies trigger atomic ref-counting operations, causing 100ms+ frame spikes.

**Check Commands:**
```bash
# Find potential unnecessary shared_ptr copies in batch/update functions
grep -rn "auto.*=.*shared_ptr" src/ | grep -v ".get()" | grep -v "make_shared"

# Find lambdas capturing shared_ptr (atomic overhead in threads)
grep -rn "\[.*shared_ptr\|EntityPtr\|BehaviorPtr" src/ | grep -v ".get()"

# Find shared_ptr usage in hot-path loops (processBatch, update loops)
grep -rn "for.*EntityPtr\|for.*shared_ptr<" src/
```

**FORBIDDEN PATTERNS:**

**Pattern 1: Unnecessary shared_ptr Copies**
```cpp
// ✗ BAD - Copies shared_ptr, increments ref count unnecessarily
void update() {
    auto batchData = m_sharedBatchData;  // UNNECESSARY COPY
    for (auto& batch : *batchData) {
        // ...
    }
}

// ✓ GOOD - Use member directly
void update() {
    for (auto& batch : *m_sharedBatchData) {  // No copy
        // ...
    }
}
```

**Pattern 2: Capturing shared_ptr in Lambdas**
```cpp
// ✗ BAD - Captures shared_ptr, atomic ref-count ops in every thread
auto data = m_sharedData;
m_futures.push_back(threadSystem.enqueue([data, this]() {
    processData(*data);  // Atomic increment/decrement
}));

// ✓ GOOD - Capture raw pointer, parent keeps ownership
auto* dataPtr = m_sharedData.get();
m_futures.push_back(threadSystem.enqueue([dataPtr, this]() {
    processData(*dataPtr);  // No atomic ops
}));
```

**Pattern 3: shared_ptr in Hot-Path Loops**
```cpp
// ✗ BAD - shared_ptr in tight loop, atomic ops per iteration
for (size_t i = start; i < end; ++i) {
    EntityPtr entity = storage.entities[i];  // Atomic increment
    auto behavior = storage.behaviors[i];    // Atomic increment
    behavior->update(entity, deltaTime);     // More atomic ops
}  // Atomic decrements x 2 per iteration

// ✓ GOOD - Raw pointers in loop, shared_ptr only when needed
for (size_t i = start; i < end; ++i) {
    Entity* entity = storage.entities[i].get();        // No atomic ops
    AIBehavior* behavior = storage.behaviors[i].get(); // No atomic ops

    // Only use shared_ptr for interface requiring ownership
    if (needsSharedOwnership) {
        behavior->executeLogic(storage.entities[i], deltaTime);
    } else {
        behavior->update(entity, deltaTime);  // Raw pointer version
    }
}
```

**When to Use Raw Pointers:**
- ✓ Inside batch processing loops (parent shared_ptr keeps ownership)
- ✓ Lambda captures for thread tasks (task lifetime < parent lifetime)
- ✓ Local function scope when owner exists in caller
- ✓ When shared_lock/mutex guarantees object stability

**When to Keep shared_ptr:**
- ✓ Long-term storage (member variables, containers)
- ✓ Crossing thread boundaries with uncertain lifetimes
- ✓ Interfaces requiring shared ownership semantics
- ✓ Return values transferring ownership

**Performance Impact:**
- Unnecessary shared_ptr copies: 100ms+ frame spikes
- Lambda captures: 2-5x slowdown in parallel tasks
- Hot-path loops: 3-4x slowdown on 10K+ entities

**Quality Gate:** ✓ No unnecessary shared_ptr copies in hot paths (BLOCKING for perf-critical code)

**Reference:** See commit a8aa267e for detailed fix example in AIManager::processBatch()

#### 5.4 String Parameter Regression (CRITICAL)

**Background:**
A refactoring attempt changed `const std::string&` parameters to `std::string_view` for "modernization", but then converted back to `std::string` for map lookups. This introduces allocations where there were none - a severe performance regression.

**Check Commands:**
```bash
# Find string_view parameters that convert to std::string for lookups
grep -rn "std::string \w\+Str\(" src/ --include="*.cpp"

# Find string_view parameters in headers doing map operations
grep -rn "string_view.*find\|string_view.*\[" src/ include/
```

**FORBIDDEN PATTERN:**
```cpp
// ✗ REGRESSION - Allocates on EVERY call
bool hasEvent(std::string_view name) const {
    std::string nameStr(name);  // ALLOCATION!
    return m_map.find(nameStr) != m_map.end();
}

// ✓ CORRECT - Zero-copy when caller passes std::string
bool hasEvent(const std::string& name) const {
    return m_map.find(name) != m_map.end();  // No allocation
}
```

**When string_view is SAFE:**
- **Return types** returning string literals: `std::string_view getName() { return "literal"; }`
- **Literal comparisons only**: `if (type == "Weather")` (no map lookup)
- **constexpr constants**: `constexpr std::string_view NAME = "value";`

**When to use const std::string&:**
- Map lookups (`.find()`, `[]` operator)
- Storing to member variables
- Filesystem APIs (std::ofstream, std::filesystem)
- Any function where caller typically has a `std::string`

**Why This Matters:**
- Each `std::string(view)` conversion allocates heap memory
- Hot-path functions (lookups) called thousands of times per frame
- Frame rate impact: 5-15% degradation on string-heavy systems

**Quality Gate:** ✓ No string_view→string conversions for map lookups (BLOCKING)

#### 5.5 Logger Usage

**Check Commands:**
```bash
# Find std::cout usage (should use Logger instead)
grep -rn "std::cout" src/ | grep -v "//"
grep -rn "std::cerr" src/ | grep -v "//"
grep -rn "printf" src/ | grep -v "//"

# Find string concatenation in logging (should use std::format)
grep -rn 'LOG_.*".*" +' src/ | grep -v "//"
grep -rn 'LOG_.*+ "' src/ | grep -v "//"

# Find inefficient conditional logging (should use *_IF macros)
grep -rn "if.*{.*LOG_\|if.*{.*AI_" src/ --include="*.cpp" | grep -v "_IF("
```

**Rules from CLAUDE.md:**
> - Use Logger (not std::cout/cerr/printf)
> - Use `std::format()`, never `+` concatenation for logging
> - Use `AI_INFO_IF(cond, msg)` macros when condition only gates logging

**Correct Usage:**
```cpp
// ✗ BAD - raw console output
std::cout << "Entity count: " << count << std::endl;

// ✗ BAD - string concatenation
LOG_INFO("Entity " + name + " spawned");  // ALLOCATIONS!

// ✗ BAD - if block only for logging
if (m_debugMode) {
    AI_INFO("Debug info: " << data);
}

// ✓ GOOD - Logger with std::format
LOG_INFO(std::format("Entity count: {}", count));
LOG_ERROR(std::format("Failed to load: {}", filename));

// ✓ GOOD - conditional logging macro
AI_INFO_IF(m_debugMode, "Debug info: " << data);
```

**Quality Gate:** ✓ No raw console output, no string concat in logs, use *_IF macros

#### 5.6 Buffer Reuse & Per-Frame Allocations (CRITICAL)

**Background:**
Per-frame allocations cause GC pressure and frame spikes. CLAUDE.md requires buffer reuse patterns.

**Check Commands:**
```bash
# Find vectors created inside update/render functions (should be members)
grep -rn "std::vector<.*>" src/ --include="*.cpp" | grep -E "update|render|process" | grep -v "m_"

# Find containers without reserve() when size is known
grep -rn "\.push_back\|\.emplace_back" src/ --include="*.cpp" | head -50

# Find new allocations in hot paths
grep -rn "new \|make_unique\|make_shared" src/ --include="*.cpp" | grep -E "update|render|process"
```

**Rules from CLAUDE.md:**
> Avoid per-frame allocations. Reuse buffers.
> Always `reserve()` when size known.

**FORBIDDEN PATTERNS:**
```cpp
// ✗ BAD - Creates new vector every frame
void Manager::update() {
    std::vector<Entity*> entities;  // ALLOCATION EVERY FRAME!
    for (auto& e : m_entities) {
        entities.push_back(e.get());
    }
}

// ✓ GOOD - Reuse member buffer
class Manager {
    std::vector<Entity*> m_buffer;  // Member, reused
    void update() {
        m_buffer.clear();  // clear() keeps capacity
        for (auto& e : m_entities) {
            m_buffer.push_back(e.get());
        }
    }
};
```

**Reserve Pattern:**
```cpp
// ✗ BAD - Multiple reallocations as vector grows
std::vector<Result> results;
for (int i = 0; i < 1000; ++i) {
    results.push_back(compute(i));  // May reallocate multiple times
}

// ✓ GOOD - Single allocation upfront
std::vector<Result> results;
results.reserve(1000);  // Pre-allocate
for (int i = 0; i < 1000; ++i) {
    results.push_back(compute(i));  // No reallocations
}
```

**Quality Gate:** ✓ No local containers in hot paths, use reserve() when size known (BLOCKING)

#### 5.7 UI Component Positioning (CRITICAL)

**Background:**
UI components need proper positioning modes for resize/fullscreen support.

**Check Commands:**
```bash
# Find UI component creation without setComponentPositioning
grep -rn "createButton\|createLabel\|createPanel\|createSlider" src/gameStates/ --include="*.cpp" -A 3 | grep -v "setComponentPositioning"

# Find UI creation in game states
grep -rn "ui\.create\|m_ui\.create\|m_uiManager\.create" src/gameStates/ --include="*.cpp"
```

**Rule from CLAUDE.md:**
> **Always** call `setComponentPositioning()` after creating components for resize/fullscreen support.

**Available Helpers:**
- `createTitleAtTop()`
- `createButtonAtBottom()`
- `createCenteredButton()`
- `createCenteredDialog()`

**Position Modes:**
- `TOP_ALIGNED`, `BOTTOM_ALIGNED`
- `LEFT_ALIGNED`, `RIGHT_ALIGNED`
- `BOTTOM_RIGHT`
- `CENTERED_H`, `CENTERED_BOTH`

**Correct Pattern:**
```cpp
// ✓ GOOD - Using helper (handles positioning automatically)
ui.createCenteredButton("start_btn", rect, "Start Game");

// ✓ GOOD - Manual with positioning
ui.createButton("settings_btn", rect, "Settings");
ui.setComponentPositioning("settings_btn", {UIPositionMode::BOTTOM_ALIGNED, ...});

// ✗ BAD - No positioning (breaks on resize/fullscreen)
ui.createButton("broken_btn", rect, "Broken");
// Missing setComponentPositioning!
```

**Quality Gate:** ✓ All UI components have positioning set

#### 5.8 Rendering Rules (CRITICAL)

**Background:**
HammerEngine uses double-buffered rendering with one Present() per frame.

**Check Commands:**
```bash
# Find SDL_RenderPresent outside GameEngine (FORBIDDEN)
grep -rn "SDL_RenderPresent" src/ | grep -v "GameEngine.cpp" | grep -v "//"

# Find SDL_RenderClear outside GameEngine (FORBIDDEN)
grep -rn "SDL_RenderClear" src/ | grep -v "GameEngine.cpp" | grep -v "//"

# Find blocking renders in loading states (should use LoadingState pattern)
grep -rn "while.*SDL_Render\|for.*SDL_Render" src/ --include="*.cpp"
```

**Rules from CLAUDE.md:**
> - **One Present() per frame** via `GameEngine::render()` → `GameStateManager::render()` → `GameState::render()`
> - **NEVER** call SDL_RenderClear/Present in GameStates
> - Use `LoadingState` with async ThreadSystem ops, not blocking manual rendering
> - Set flag in `enter()`, transition in `update()` to avoid timing issues (deferred transitions)

**FORBIDDEN PATTERNS:**
```cpp
// ✗ FORBIDDEN - Calling Present in GameState
void MyState::render(SDL_Renderer* renderer) {
    // ... draw stuff ...
    SDL_RenderPresent(renderer);  // NEVER DO THIS!
}

// ✗ FORBIDDEN - Blocking render loop in loading
void LoadingScreen::show() {
    while (loading) {
        SDL_RenderClear(renderer);
        // draw progress
        SDL_RenderPresent(renderer);  // BREAKS FRAME TIMING!
    }
}

// ✗ FORBIDDEN - Immediate transition in enter()
void MyState::enter() {
    mp_stateManager->pushState<NextState>();  // TIMING ISSUES!
}
```

**Correct Patterns:**
```cpp
// ✓ GOOD - Let GameEngine handle Present
void MyState::render(SDL_Renderer* renderer) {
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    // Draw content only, no Clear/Present
}

// ✓ GOOD - Use LoadingState with ThreadSystem
void LoadingState::enter() {
    m_loadingTask = ThreadSystem::enqueue([this]() {
        loadResources();  // Async
    });
}

// ✓ GOOD - Deferred transition
void MyState::enter() {
    m_shouldTransition = true;  // Set flag
}
void MyState::update(float dt) {
    if (m_shouldTransition) {
        m_shouldTransition = false;
        mp_stateManager->pushState<NextState>();  // Safe in update
    }
}
```

**Quality Gate:** ✓ No SDL_RenderClear/Present outside GameEngine (BLOCKING)

### 6. Copyright & Legal Compliance

**Check Command:**
```bash
# Find files missing copyright header
find src/ include/ -type f \( -name "*.cpp" -o -name "*.hpp" \) -exec grep -L "Copyright (c) 2025 Hammer Forged Games" {} \;
```

**Required Header:**
```cpp
/* Copyright (c) 2025 Hammer Forged Games
 * All rights reserved.
 * Licensed under the MIT License - see LICENSE file for details
*/
```

**Quality Gate:** ✓ All source files have copyright header

### 7. Test Coverage

**Check Command:**
```bash
# For modified files, check if corresponding test exists
# Example: if src/managers/NewManager.cpp exists, check for tests/NewManager_tests.cpp
```

**Rules:**
- New managers must have test file in `tests/`
- New managers must have test script in `tests/test_scripts/run_*_tests.sh`
- Test script must be added to `run_all_tests.sh`

**Quality Gate:** ✓ New code has corresponding tests

## Quality Report Format

```markdown
=== HAMMERENGINE QUALITY GATE REPORT ===
Generated: YYYY-MM-DD HH:MM:SS
Branch: <current-branch>

## Compilation Quality
✓/✗ Status: <PASSED/FAILED>
  Warnings: <count>
  Errors: <count>

<details if failures>

## Static Analysis (cppcheck)
✓/✗ Status: <PASSED/FAILED>
  Errors: <count>
  Warnings: <count>

<list of issues>

## Coding Standards
✓/✗ Naming Conventions: <PASSED/FAILED>
  <violations if any>

✓/✗ Formatting: <PASSED/FAILED>
  <violations if any>

## Threading Safety (CRITICAL)
✓/✗ Static Variables: <PASSED/FAILED>
  <violations - BLOCKING>

✓/✗ ThreadSystem Usage: <PASSED/FAILED>
  <violations if any>

✓/✗ Mutex Protection: <PASSED/FAILED>
  <violations if any>

## Architecture Compliance
✓/✗ Rendering Rules: <PASSED/FAILED>
  <violations - BLOCKING if SDL_RenderClear/Present outside GameEngine>
✓/✗ RAII/Smart Pointers: <PASSED/FAILED>
✓/✗ Smart Pointer Performance: <PASSED/FAILED>
  <violations if any - BLOCKING for perf-critical code>
✓/✗ Logger Usage: <PASSED/FAILED>
  <check for std::format usage, *_IF macros>
✓/✗ Buffer Reuse: <PASSED/FAILED>
  <violations if any - BLOCKING for hot paths>
✓/✗ UI Positioning: <PASSED/FAILED>
  <missing setComponentPositioning calls>

## Legal Compliance
✓/✗ Copyright Headers: <PASSED/FAILED>
  Missing: <count> files
  <list files>

## Test Coverage
✓/✗ Tests Exist: <PASSED/FAILED>
  <missing tests>

---
## OVERALL STATUS: ✓ PASSED / ✗ FAILED

✓ Ready to commit
✗ Fix <count> violations before commit

### Critical Issues (BLOCKING)
<list blocking issues>

### Warnings (Review Required)
<list warnings>

### Recommendations
<specific fixes>
```

## Exit Codes

- **0:** All checks passed
- **1:** Critical violations (static vars, threading issues)
- **2:** Compilation warnings/errors
- **3:** Static analysis failures
- **4:** Missing copyright headers
- **5:** Multiple categories failed

## Usage as Git Pre-Commit Hook

This Skill can be integrated as a git hook:

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Ask Claude to run quality check
claude-code "run quality check on my changes"

if [ $? -ne 0 ]; then
    echo "Quality check failed. Fix issues before committing."
    exit 1
fi
```

## Usage Examples

When the user says:
- "check code quality"
- "run quality gate"
- "verify my code before commit"
- "make sure code follows standards"
- "check for threading violations"

Activate this Skill automatically.

## Performance Expectations

- **Compilation Check:** 10-30 seconds
- **Static Analysis:** 30-60 seconds
- **Standards Checks:** 5-10 seconds
- **Total:** ~1-2 minutes

## Quick Fix Guide

**Most Common Violations:**

1. **Unused parameters:**
   ```cpp
   void func([[maybe_unused]] int param) { }
   ```

2. **Static variable in threaded code:**
   ```cpp
   // Move to class member or use thread_local
   ```

3. **Missing copyright:**
   ```cpp
   /* Copyright (c) 2025 Hammer Forged Games
    * All rights reserved.
    * Licensed under the MIT License - see LICENSE file for details
   */
   ```

4. **Using std::cout:**
   ```cpp
   LOG_INFO("message");  // instead of std::cout
   ```

5. **Raw new/delete:**
   ```cpp
   auto ptr = std::make_unique<Type>();  // instead of new
   ```

6. **Unnecessary shared_ptr copies:**
   ```cpp
   // Instead of: auto copy = m_sharedPtr;
   // Use member directly or capture raw pointer in lambdas
   auto* rawPtr = m_sharedPtr.get();
   ```

7. **shared_ptr in hot-path loops:**
   ```cpp
   // Inside batch processing loops, use raw pointers
   Entity* entity = storage.entities[i].get();
   // Keep shared_ptr in storage, use raw in tight loops
   ```

8. **String concatenation in logging:**
   ```cpp
   // Instead of: LOG_INFO("Value: " + std::to_string(x));
   LOG_INFO(std::format("Value: {}", x));
   ```

9. **Conditional logging without *_IF macro:**
   ```cpp
   // Instead of: if (debug) { AI_INFO("msg"); }
   AI_INFO_IF(debug, "msg");
   ```

10. **Per-frame allocations:**
    ```cpp
    // Instead of: void update() { std::vector<T> temp; ... }
    // Use member buffer: m_buffer.clear(); m_buffer.push_back(...);
    ```

11. **Missing reserve() for known sizes:**
    ```cpp
    std::vector<T> vec;
    vec.reserve(knownSize);  // Add before push_back loop
    ```

12. **UI component without positioning:**
    ```cpp
    ui.createButton("id", rect, "text");
    ui.setComponentPositioning("id", {UIPositionMode::CENTERED_BOTH, ...});
    ```

13. **SDL_RenderPresent in GameState:**
    ```cpp
    // NEVER call SDL_RenderPresent/Clear in GameState::render()
    // Only draw content, GameEngine handles Present
    ```

14. **Immediate state transition in enter():**
    ```cpp
    // Instead of: void enter() { pushState<Next>(); }
    // Use deferred: m_shouldTransition = true; // then transition in update()
    ```

## Integration with Workflow

Use this Skill:
- **Before every commit** - Catch issues early
- **During PR review** - Validate code quality
- **After merging** - Ensure standards maintained
- **When adding new systems** - Verify compliance

## Severity Classification

**BLOCKING (Must Fix):**
- Static variables in threaded code
- Unnecessary shared_ptr copies in hot paths (perf-critical code)
- Per-frame allocations in hot paths (local containers in update/render)
- SDL_RenderClear/Present outside GameEngine
- Compilation errors
- Critical cppcheck errors
- Missing copyright headers on new files

**WARNING (Should Fix):**
- Compilation warnings
- cppcheck warnings
- Naming convention violations
- Missing tests for new code
- String concatenation in logging (use std::format)
- Conditional blocks only for logging (use *_IF macros)
- Missing UI component positioning
- Missing reserve() calls for known sizes

**INFO (Consider Fixing):**
- Style suggestions
- Performance hints
- Code organization recommendations
- Deferred transition patterns in GameStates
