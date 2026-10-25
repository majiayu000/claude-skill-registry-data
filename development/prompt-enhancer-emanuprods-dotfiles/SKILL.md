---
name: prompt-enhancer"
description: Improves user prompts by adding context, clarifying intent, and structuring for better AI responses. Use when user requests are vague, incomplete, or could benefit from additional context.
---

# Prompt Enhancer Skill

## Enhancement Principles

### 1. Clarify Intent
- What is the **exact goal**?
- What does **success look like**?
- What are **constraints** (time, tech, resources)?

### 2. Add Context
- Current **codebase state** (relevant files, patterns)
- **Existing conventions** (naming, architecture, testing)
- **Related work** (previous PRs, issues, docs)

### 3. Structure Request
- Break into **atomic steps**
- Specify **output format**
- Define **acceptance criteria**

### 4. Anticipate Edge Cases
- Error scenarios
- Boundary conditions
- Performance requirements
- Security considerations

## Enhancement Patterns

### Vague → Specific

**Before:** "Fix the login bug"
**After:** "Fix login bug where users with special characters in email (e.g., `user+tag@example.com`) get 'Invalid email' error. Issue is in `src/validators/email.ts` regex pattern. Should allow RFC 5322 compliant emails. Add test case for `user+tag@example.com`."

**Before:** "Add tests"
**After:** "Add unit tests for `UserService.getUserById()` in `src/services/user.service.ts`. Cover: happy path, not found (404), database error (500), invalid ID format. Use existing test utilities in `test/utils.ts`. Target 90% coverage for this function."

### Feature Request → Implementation Plan

**Before:** "Add dark mode"
**After:** "Implement dark mode toggle for the dashboard:
1. Add `theme` context provider in `src/context/ThemeContext.tsx`
2. Create `useTheme()` hook with localStorage persistence
3. Add Tailwind dark mode classes to `src/components/Dashboard/*.tsx`
4. Add toggle button in `src/components/Header/UserMenu.tsx`
5. Test: toggle persists across refresh, respects system preference initially"

### Debug Request → Investigation Plan

**Before:** "Why is the API slow?"
**After:** "Investigate API latency on `GET /api/users` (currently 2.5s avg, target <500ms):
1. Check database query with `EXPLAIN ANALYZE`
2. Profile Node.js with `--inspect` or clinic.js
3. Check for N+1 queries in user serialization
4. Review Redis cache hit rate
5. Document findings and proposed fix"

## Enhancement Templates

### Code Generation
```
**Goal:** [What to create]
**Location:** [File/path]
**Pattern:** [Existing similar code to follow]
**Requirements:**
- [Requirement 1]
- [Requirement 2]
**Tests:** [What to test]
**Constraints:** [Tech, time, dependencies]
```

### Refactoring
```
**Target:** [File/function to refactor]
**Problem:** [Code smell, complexity, duplication]
**Approach:** [Extract method, polymorphism, etc.]
**Safety:** [Existing tests? Need characterization tests?]
**Scope:** [Single file? Cross-module?]
```

### Code Review
```
**PR:** [Link or description]
**Focus Areas:** [Security, performance, maintainability, etc.]
**Context:** [Business logic, user impact]
**Known Issues:** [Any TODOs, debt, workarounds]
```

### Debugging
```
**Symptom:** [Error, slow, wrong output]
**Environment:** [Local, staging, prod]
**Reproduction:** [Steps, frequency]
**Logs/Metrics:** [Relevant excerpts]
**Recent Changes:** [Deploy, config, data]
```

## Auto-Enhancement Rules

When user prompt matches these patterns, auto-enhance:

| Pattern | Enhancement |
|---------|-------------|
| "Fix X" | Add: file location, error details, reproduction steps, test case |
| "Add X" | Add: location, pattern to follow, requirements, tests, constraints |
| "Refactor X" | Add: target, problem, approach, safety checks, scope |
| "Review X" | Add: focus areas, context, known issues |
| "Debug X" | Add: symptom, env, reproduction, logs, recent changes |
| "Explain X" | Add: target audience, depth level, format preference |

## Context Injection

### From Codebase
```bash
# Get relevant files for context
git diff --name-only HEAD~5..HEAD
grep -r "TODO\|FIXME\|HACK" --include="*.ts" | head -20
```

### From Git History
```bash
# Recent changes to area
git log --oneline -20 -- src/auth/
git show HEAD:src/auth.ts | head -100
```

### From Project Docs
```bash
# Check for relevant docs
ls docs/adr/
cat AGENTS.md 2>/dev/null | head -50
```

## Output Format

When enhancing, present as:

```
## Enhanced Prompt

**Original:** [User's original request]

**Enhanced:**
[Structured, detailed prompt with all additions]

**Context Added:**
- [File references]
- [Pattern references]
- [Constraint references]

**Suggested Next Steps:**
1. [Step 1]
2. [Step 2]
...

**Questions for Clarification:**
- [Question 1]?
- [Question 2]?
```

## Integration

### As Pre-Processor
```typescript
// In OpenCode hook or wrapper
async function enhancePrompt(userInput: string): Promise<string> {
  const context = await gatherContext(userInput);
  return applyTemplate(userInput, context);
}
```

### As Interactive Skill
```
User: "Fix the login"
Agent: [Loads prompt-enhancer skill]
Agent: "Let me enhance that. Which login flow? Web? API? What's the error?"
User: "Web login, special chars in email fail"
Agent: [Generates enhanced prompt with file refs, test case, etc.]
```

## When to Use

- User requests are brief or ambiguous
- Starting new feature work
- Debugging unknown issues
- Requesting code reviews
- Onboarding to unfamiliar codebase
- Planning complex refactors