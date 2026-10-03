---
name: implement-qa-automation
description: "Use when you need automated smoke tests for core game subsystems after build completion. Triggers: 'smoke tests', 'automated testing'."
---

## 1. Overview
Generates smoke tests for EventBus, ECS, FSM, Input Handler; detects framework; executes; auto-fixes (max 2 retries); performs runtime behavioral testing.

## 2. Core Pattern

### Phase 1: Framework Detection
Scan config files: **Rust**: `Cargo.toml` → `cargo test` | **TS/JS**: `package.json` → `npm test` | **Python**: `pytest` | **Go**: `*_test.go` → `go test ./...` | **C++**: CMake + GTest → `ctest` | **C#**: `.csproj` → `dotnet test`. If none, initialize minimal framework.

### Phase 2: Smoke Test Generation
* **EventBus** (`events_spec.md`): publish→subscribe, payload integrity, unsubscribe
* **ECS** (`ecs_spec.md`): entity create/destroy, component attach/read, system order
* **FSM** (`state_machine_spec.md`): valid transition, guarded rejection, initial state
* **Input Handler** (`input_mapping.md`): action binding, analog range (0.0–1.0)

### Phase 3: Execution & Runtime Testing
Run framework command (timeout: 120s). Then launch app and test interactively.

**Platform**: Web → Playwright. Desktop → `bash` + `browser_evaluate`. Mobile/Console → emulator SDK. CLI → `bash` stdout.

**Steps**: 1) **Launch** (30s Web, 10s native). 2) **Verify** (exit 0, no crashes in 5s). 3) **Interact** (inputs from `input_mapping.md`, verify Menu→Playing→Paused→GameOver). 4) **Evidence** (Web → `{TARGET_FOLDER}/docs/qa_screenshots/`, Desktop → `{TARGET_FOLDER}/docs/qa_logs/`).

### Phase 4: Auto-Fix
Parse → classify (**Test Bug** / **Code Bug** / **Spec Mismatch**) → minimal fix → re-run. Max 2 cycles.

### Phase 5: Final Report
* **All Pass**: "✅ QA Complete — [N] tests passed, 0 errors."
* **Partial**: "⚠️ QA Partial — [N] passed, [M] failed. Review needed."
* **Failed**: "❌ QA Failed — [N] tests failed. Auto-fix attempted."
* **Runtime Fail**: "⚠️ Units passed, runtime failed: [issue]. Check init order."

## 3. Interaction Protocol

**Auto-Fix**: Max 2 retry cycles. Classify before fixing.

**Intercepts**:
* **[Spec Mismatch]**: "Test failure indicates spec-to-code mismatch: [description]. Review [spec file] vs [code file]."
* **[Framework Init]**: "No test framework detected for [language]. Initializing [framework]."

## 4. Red Flags
* **Consistent Results**: Same test produces same outcome across runs — investigate fundamental issues on repeated failures
* **Spec-Aligned Verification**: Tests validate correct behavior matching specifications
* **Deterministic Execution**: Tests run without race conditions or timing dependencies
* **Architectural Resolution**: Auto-fix addresses root cause; persistent failures indicate deeper issues requiring structural changes
* **Successful Launch**: Application starts and runs without critical initialization errors
* **Responsive Runtime**: Input handler, event bus, and game loop wire correctly for interactive response

## 5. Final Integrity Audit
- [ ] Smoke tests for all subsystems
- [ ] Test framework detected
- [ ] Tests execute without errors
- [ ] Auto-fix applied (if needed)
- [ ] Report accurate
- [ ] Runtime: launched, no crash, responded to inputs
- [ ] No unhandled exceptions
- [ ] Evidence saved
- [ ] Inputs trigger expected responses
- [ ] State transitions match FSM spec
- [ ] Runs within frame rate budget

## 6. Execution Command
`/implement-qa-automation`
