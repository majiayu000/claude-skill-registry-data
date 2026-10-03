---
name: implement-integration-tests
description: "Use when generating cross-system integration test skeletons that verify subsystem interactions (event bus ↔ state machine, ECS lifecycle chains, input → action → ECS). Triggers: 'integration tests', 'wiring tests'."
---

# Implement Integration Tests

## 1. Overview

Generate integration test skeletons for cross-system data flow paths across 2+ subsystems. Each test file exercises one specific integration path (e.g., event emission → state transition → scene change).

**Triggers:** 'integration tests', 'cross-system tests', 'subsystem interaction tests', 'wiring tests'

## 2. Core Pattern

### 2.1 Configuration — MANDATORY FIRST STEP

1. Read `.game-dev-config.json` → extract `target_folder`, `specs_dir`
2. Read `{specs_dir}/rendering_target.md` → extract Platform, Engine, Language
3. Read `{TARGET_FOLDER}/package.json` → extract test framework (vitest, jest, etc.)
4. **If Engine not "Phaser 3" or "Three.js"** → generate unsupported placeholder and STOP
5. **If no test framework found** → default to vitest, note in output

### 3.2. Integration Path Discovery

Read specs to discover which subsystems exist and how they connect:

| Spec File | Extract |
|---|---|
| `events_spec.md` | Event names, which systems emit/subscribe |
| `state_machine_spec.md` | States, transitions, triggers |
| `ecs_spec.md` | Components, systems, entity archetypes |
| `screen_architecture_spec.md` | Screens, transitions, lifecycle |
| `input_mapping.md` | Actions, bindings |
| `system_roster.md` | Which subsystems exist (save, audio, etc.) |

**Build integration path list from specs.** For each pair of subsystems that share events or data, create one integration path. Generate tests only for subsystems present in specs.

### 3.3. Read Existing Implementations

Read actual source files in `{TARGET_FOLDER}/src/` to extract:
- Class names, constructor signatures, public method signatures
- Import paths for test file imports
- Event bus API (emit/on/off method names)
- ECS World API (createEntity, addComponent, etc.)
- State machine API (transition, getCurrentState, etc.)

### 3.4. Per-Path Test Guidance

| Integration Path | Setup | Key Assertions |
|---|---|---|
| EventBus → StateMachine | Create bus + SM, wire subscriptions | Event triggers correct state transition; invalid events handled gracefully without crashing |
| StateMachine → ScreenManager | Create SM + ScreenMgr | State transition triggers correct screen load; onEnter/onExit called |
| Input → EventBus → ECS | Create input handler + bus + world | Input action emits event; event triggers system; entity updates |
| ECS Entity Lifecycle | Create world + spawn entity | Spawn → components attached; damage → health decreases; health 0 → death event emitted |
| EventBus → SaveSystem | Create bus + save system | Save event → state serialized; load event → state restored |
| ContentFactories → ECS | Create world + call factories | Factory returns entity with all expected components; defaults match spec |

**Only generate rows that have matching subsystems in the project specs.**

### 3.5. Test File Generation

For each discovered integration path, generate one test file:
- File name: `{subsystemA}-{subsystemB}.integration.test.ts`
- Location: `{TARGET_FOLDER}/src/__tests__/integration/`
- Structure:
  1. Imports from actual source paths (§ 3.3)
  2. `describe('Integration: SubsystemA → SubsystemB', ...)` block
  3. `beforeEach`: instantiate both subsystems, wire connections
  4. `afterEach`: cleanup — destroy, unsubscribe, reset
  5. Test cases from § 3.4 Key Assertions (one `it()` per assertion)
  6. Each `it()` uses Arrange/Act/Assert with TODO for real values

**If Engine == "Phaser 3":** Scene integration tests use `Phaser.HEADLESS` mode.
**If Engine == "Three.js":** Scene integration tests mock WebGL context or use jsdom.

### 3.6. Test Runner Config

If project uses custom test config, ensure `src/__tests__/integration/` is included in test paths. No barrel export needed for test files.

## 3. Output File Structure

```
{TARGET_FOLDER}/src/__tests__/integration/
├── eventbus-statemachine.integration.test.ts
├── statemachine-screenmanager.integration.test.ts
├── input-eventbus-ecs.integration.test.ts
├── ecs-entity-lifecycle.integration.test.ts
├── eventbus-savesystem.integration.test.ts       (if save system exists)
├── content-factories-ecs.integration.test.ts     (if content data exists)
```

Files generated ONLY for subsystems that exist in the project.

## 4. Validation Checklist

- [ ] `.game-dev-config.json` read for target_folder/specs_dir
- [ ] Engine detected from rendering_target.md
- [ ] Test framework detected from package.json
- [ ] Integration paths derived from ACTUAL specs (no invented paths)
- [ ] Each test file imports from real source paths
- [ ] Each test file has beforeEach setup + afterEach teardown
- [ ] Each test file has ≥ 2 test cases (happy path + edge case)
- [ ] Correct assertion library used (vitest/jest as detected)
- [ ] No engine-specific code without engine branching
- [ ] Integration tests use real implementations (no mocks for subsystems under test)
- [ ] All subsystem pairs sharing events have a test file

## 5. Red Flags

| Signal | Action |
|---|---|
| Spec file missing for a subsystem | Skip that integration path, note in output |
| Source files not found for subsystem | STOP — cannot determine import paths |
| Test framework not detected | Default to vitest, warn user |
| Fewer than 2 integration paths discovered | STOP — insufficient subsystem connections |
| Test mocks a subsystem under test | Remove mock — integration tests use real impls |
| Hardcoded event names not from specs | Replace with spec-derived event names |

## 6. Interaction Protocol

| Common Mistake | Correction |
|---|---|
| Writing unit tests for one system | Each test MUST exercise ≥ 2 subsystems |
| Mocking one of the subsystems under test | Use real implementations — that's the point |
| Generating tests for non-existent subsystems | Only test subsystems found in specs |
| Hardcoding import paths | Read actual `src/` to get real import paths |
| Missing teardown in afterEach | Every beforeEach MUST have matching afterEach |
