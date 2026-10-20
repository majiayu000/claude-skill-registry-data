---
name: refactor
description: "Safe refactoring with test guard — improve code quality without changing behavior. Use when: refactor, cleanup, restructure, simplify, extract function, improve code quality."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/coding/refactor.skill.md"
  tags: "coding"
  core: "true"
  context_cost: "low"
---
# Refactor Skill

## Goal
Improve code structure, readability, or maintainability while guaranteeing that all existing behavior is preserved. Tests are the safety net — if they fail after refactoring, the refactor was incorrect.

## Steps

1. **Establish the safety net**
   - Run the full test suite: `[test command from AGENTS.md]`
   - If tests fail before you start: STOP — fix the failing tests first (they're not a safe net)
   - Record baseline: number of passing tests, coverage %

2. **Identify the refactoring target**
   - What specific code smell is being addressed?
   - Common targets:
     - Function too long (> 30 lines) → Extract Function
     - Class too large (> 500 lines) → Extract Class / Split by Responsibility
     - Duplicated logic (> 3 occurrences) → Extract Method/Module
     - Magic numbers/strings → Extract Constants
     - Deep nesting (> 3 levels) → Early Returns / Extract Method
     - God class → Decompose to smaller, focused classes
     - Long parameter list → Introduce Parameter Object

3. **Apply ONE refactoring at a time**
   - Make the smallest possible change
   - Run tests immediately after each change
   - If tests fail: REVERT the change (don't try to fix tests and refactor simultaneously)

4. **Common refactoring patterns**

   **Extract Function:**
   ```typescript
   // Before: complex inline logic
   function processOrder(order) {
     // 40 lines of validation + calculation + notification
   }

   // After: extracted with clear names
   function processOrder(order) {
     validateOrder(order);
     const total = calculateTotal(order);
     notifyUser(order, total);
   }
   ```

   **Early Returns (reduce nesting):**
   ```typescript
   // Before: deeply nested
   function getDiscount(user) {
     if (user) {
       if (user.isPremium) {
         if (user.yearsActive > 5) {
           return 0.3;
         }
       }
     }
     return 0;
   }

   // After: early returns
   function getDiscount(user) {
     if (!user) return 0;
     if (!user.isPremium) return 0;
     if (user.yearsActive <= 5) return 0;
     return 0.3;
   }
   ```

   **Extract Constants:**
   ```typescript
   // Before: magic numbers
   if (attempts > 3) lockAccount(15 * 60 * 1000);

   // After: named constants
   const MAX_LOGIN_ATTEMPTS = 3;
   const LOCKOUT_DURATION_MS = 15 * 60 * 1000; // 15 minutes
   if (attempts > MAX_LOGIN_ATTEMPTS) lockAccount(LOCKOUT_DURATION_MS);
   ```

5. **After each refactoring step**
   - Run: `[test command]` → must pass
   - Run: `[typecheck command]` → must pass
   - Run: `[lint command]` → must pass
   - Check: complexity still < 10? Length still < 30 lines?

6. **Check architecture boundaries** (agentic-linter)
   - After significant structural changes: run agentic-linter skill
   - Ensure no new circular dependencies introduced

7. **Final verification**
   - Baseline tests passing count matches post-refactor count
   - Coverage has not decreased
   - No new lint errors or type errors

## Constraints
- NEVER change behavior during refactoring (only structure)
- NEVER refactor without a passing test suite as safety net
- NEVER combine refactoring with feature addition in the same commit
- If a refactor requires fixing tests: stop, analyze whether the tests or the logic is wrong

## Output Format
Report: "Refactored [target]. All [N] tests still passing. Coverage: [X]%. Complexity reduced from [A] to [B]."

## Security & Guardrails

### 1. Skill Security (Refactor)
- **Security Check Evasion**: When applying "Extract Function" (Step 4), the agent might accidentally extract a sensitive business operation *outside* of its surrounding authorization boundary (e.g., moving a data fetch out of an `if (isAdmin)` block). The agent must mathematically guarantee that any extracted logic remains strictly within the exact same structural authorization context as its pre-refactored state.
- **Test Suite Over-Reliance (The Blind Net)**: Step 1 establishes tests as the "safety net." If the existing test suite has poor coverage of critical security paths (e.g., only testing the "Happy Path" of user login), refactoring the code might silently introduce a vulnerability (like bypassing rate limits) that the tests won't catch. The agent must verify that Security/Audit tests explicitly exist and pass before using them as a justification that a refactor is "safe."

### 2. System Integration Security
- **Data Exposure via De-Nesting**: During "Early Returns" refactoring (Step 4), the agent attempts to flatten deep nesting. A poorly executed early return might inadvertently leak information via timing differences or distinct error messages (e.g., changing from a generic "Auth Failed" to explicitly returning exactly which condition failed first). The agent must ensure that early returns in security-critical paths do not introduce Oracle vulnerabilities or alter the established generic failure contract.
- **Log Forgetting (The Silent Refactor)**: When decomposing a "God Class" (Step 2), the agent might successfully migrate the core logic but forget to migrate the associated audit logging or SIEM (Security Information and Event Management) telemetry calls into the new, decomposed classes. The agent must execute a specific AST-based diff to guarantee 100% preservation of all `.log`, `.audit`, and `.trace` calls.

### 3. LLM & Agent Guardrails
- **The "Clever Code" Hallucination**: The LLM might refactor a highly readable, straightforward function into a hyper-dense, "clever" one-liner (e.g., using complex regex or bitwise operators) to satisfy the "minimize lines" heuristic. This destroys auditability and hides potential logical flaws from human reviewers. The agent's linting step (Step 5) must penalize excessive cognitive complexity, forcing the LLM to prioritize readability over brevity.
- **Silent Behavior Mutation**: The skill dictates "NEVER change behavior" (Constraints). However, LLMs struggle with edge cases. If refactoring a sorting algorithm, the LLM might change it from a stable to an unstable sort, which passes basic tests but causes catastrophic layout shifts in the UI. The agent must generate property-based or fuzz tests *prior* to refactoring complex algorithms to mathematically prove behavioral equivalence.
