---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
tags: [meta, workflow, parallel, agents]
applies-to: [antigravity, cursor, copilot, gemini]
level: project
---

## Overview
You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work.

When you have multiple unrelated failures (different test files, different subsystems, different bugs), investigating them sequentially wastes time. Each investigation is independent and can happen in parallel.

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

## When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations
- Multiple independent features/components need building simultaneously

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other (editing same files)
- Tasks share generated code (e.g., same `build_runner` output)

## Flutter-Specific Parallel Opportunities

| Scenario | Agent 1 | Agent 2 | Agent 3 |
|----------|---------|---------|---------|
| Multi-feature sprint | Feature A (data + UI) | Feature B (data + UI) | Shared component refactor |
| Bug triage | Auth flow bug | Payment flow bug | Navigation bug |
| Test failures | Widget tests | Unit tests (BLoC) | Integration tests |
| Code review fixes | Fix data layer issues | Fix UI issues | Fix test issues |

**⚠️ Conflict warning:** Do NOT dispatch parallel agents that both modify:
- The same Cubit/BLoC state class
- The same DI registration module
- The same route configuration
- Files that share `build_runner` generated output

### 1. Identify Independent Domains
Group failures/tasks by what's affected:
- Feature A: Wallet balance display
- Feature B: Transaction history list
- Feature C: Settings preferences

Each domain is independent — fixing wallet balance doesn't affect settings.

### 2. Create Focused Agent Tasks
Each agent gets:
- **Specific scope:** One feature, test file, or subsystem
- **Clear goal:** Make these tests pass / build this component
- **Constraints:** Don't change code outside your scope
- **Expected output:** Summary of what you found and fixed

### 3. Dispatch in Parallel
```
Agent 1 → Fix wallet balance Cubit and widget tests
Agent 2 → Fix transaction history data source and repository
Agent 3 → Fix settings preferences persistence
```

### 4. Review and Integrate
When agents return:
- Read each summary
- Verify fixes don't conflict
- Run `dart run build_runner build --delete-conflicting-outputs`
- Run `flutter analyze`
- Run `flutter test`
- Integrate all changes

## Agent Prompt Structure
Good agent prompts are:
1. **Focused** — One clear problem domain
2. **Self-contained** — All context needed to understand the problem
3. **Specific about output** — What should the agent return?

```markdown
Fix the failing widget tests in test/features/wallet/presentation/wallet_page_test.dart:

1. "should display balance when loaded" — expects formatted currency
2. "should show error state" — BLoC emits wrong state type
3. "should navigate to detail on tap" — GoRouter mock not configured

These are state management issues. Your task:

1. Read the test file and the WalletCubit implementation
2. Identify root cause — state emission or test setup?
3. Fix by:
   - Correcting BLoC state emissions if buggy
   - Fixing test mocks/setup if tests are wrong
   - Ensuring freezed state classes match expectations

Do NOT change the WalletPage widget code unless the tests reveal a genuine bug.

Return: Summary of what you found and what you fixed.
```

## Common Mistakes
**❌ Too broad:** "Fix all the tests" — agent gets lost
**✅ Specific:** "Fix wallet_page_test.dart" — focused scope

**❌ No context:** "Fix the state bug" — agent doesn't know where
**✅ Context:** Paste the error messages and test names

**❌ No constraints:** Agent might refactor everything
**✅ Constraints:** "Do NOT change production code" or "Fix tests only"

**❌ Vague output:** "Fix it" — you don't know what changed
**✅ Specific:** "Return summary of root cause and changes"

## Verification
After agents return:
1. **Review each summary** — Understand what changed
2. **Check for conflicts** — Did agents edit same code?
3. **Run build_runner** — Regenerate all generated code
4. **Run flutter analyze** — Check for static analysis issues
5. **Run flutter test** — Verify all fixes work together
6. **Spot check** — Agents can make systematic errors

## Key Benefits
1. **Parallelization** — Multiple investigations happen simultaneously
2. **Focus** — Each agent has narrow scope, less context to track
3. **Independence** — Agents don't interfere with each other
4. **Speed** — 3 problems solved in time of 1
