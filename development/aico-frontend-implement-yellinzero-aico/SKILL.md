---
name: aico-frontend-implement
description: |
  Execute frontend implementation with TDD. Read all constraint files before coding, write failing test first, verify after each step.

  Use this skill when:
  - User asks to "implement this", "implement the plan", "start implementation", "execute plan"
  - Have an implementation plan ready and need to execute it
  - Executing steps from /frontend.plan output
  - User says "start coding", "write the code", "begin implementation"
  - User asks to "use TDD", "write test first", "test-driven" for frontend code
  - User asks to "write tests", "add tests", "create tests"
  - Fixing UI bugs (write failing test that reproduces bug first)

  TDD Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
  TDD Cycle: RED (write failing test) → Verify fails → GREEN (minimal code) → Verify passes → REFACTOR

  Prerequisites:
  - MUST have task file in docs/reference/frontend/tasks/ (use /frontend.tasks first if not exists)
  - MUST read design-system.md, constraints.md, and design spec before writing any code.
  Flow: Check Task File → Read Constraints → TDD Cycle (RED→GREEN→REFACTOR) → Verify Each → Test → Update Task Status → Notify PM
---

# Implement

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

0. **Check task file EXISTS** (MANDATORY):
   - Look for `docs/reference/frontend/tasks/{story-id}.md`
   - If NOT exists → STOP and tell user: "Please run /frontend.tasks first to break down the story"
   - If exists → proceed to step 1

1. **Read constraints FIRST** (before any code):
   - `docs/reference/frontend/design-system.md` - Colors, typography, spacing
   - `docs/reference/frontend/constraints.md` - Tech stack, patterns
   - `docs/reference/frontend/designs/{name}.md` - Component specs
2. **Execute each step in order**:
   - Run the action
   - Run verification command
   - If fail → fix before proceeding
   - If pass → continue to next step
3. **After all steps**:
   - Run unit tests
   - Run build check
4. **Update task status** in `docs/reference/frontend/tasks/{story}.md`
5. **Notify PM for acceptance** - Notify PM to verify (PM checks all related tasks and updates Story status)
6. **Commit changes** (user decides when to commit)

## Execution Flow

```
Check Task File → Read Constraints → Execute Steps → Verify Each → Test → Mark Complete → Notify PM → Commit
```

## Step Execution Rules

### Rule 1: Follow Constraints Exactly

```tsx
// ❌ Wrong: Ignore design system
<button className="bg-blue-500 text-white">

// ✅ Right: Use design tokens
<button className="bg-primary text-primary-foreground">
```

### Rule 2: Verify Before Proceeding

Each step has a Verify section - MUST run it and confirm expected output before moving on.

### Rule 3: No Skipping

- Execute ALL steps in order
- Do NOT combine steps
- Do NOT skip verification

## Post-Implementation Checklist

1. **Run tests**: `npm test [component]`
2. **Run build**: `npm run build`
3. **Update task status** in tasks file
4. **Notify PM**: Tell PM frontend tasks are complete, request acceptance
5. **Commit** (user decides when): `git commit -m "feat([scope]): [description]"`

## Error Handling

| Error Type           | Action                                 |
| -------------------- | -------------------------------------- |
| TypeScript error     | Fix type issues, re-verify             |
| Test failure         | Debug test, fix implementation or test |
| Build failure        | Check imports, fix errors              |
| Constraint violation | Re-read constraints, align code        |

## Key Rules

- ALWAYS read all constraint files before writing any code
- MUST run verification command for each step
- ALWAYS run tests before marking task complete
- MUST update task status in tasks/{story}.md
- MUST notify PM after completing all tasks (PM handles story verification)
- Let user decide when to commit

## Common Mistakes

- ❌ Implement without task file → ✅ ALWAYS run /frontend.tasks first to break down story
- ❌ Skip reading constraints → ✅ ALWAYS read before coding
- ❌ Skip verification → ✅ Run verify command for each step
- ❌ Skip tests → ✅ Run tests before marking complete
- ❌ Forget to update task status → ✅ Update tasks/{story}.md
- ❌ Directly update story status → ✅ Notify PM, let PM verify and update story

---

## TDD Deep Dive

### The TDD Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? **Delete it. Start over.**

### Red-Green-Refactor Cycle

```
RED → Verify Fails → GREEN → Verify Passes → REFACTOR → Repeat
```

#### 1. RED - Write Failing Test

```typescript
test('Button shows loading state when clicked', async () => {
  render(<SubmitButton onClick={mockSubmit} />)
  await userEvent.click(screen.getByRole('button'))
  expect(screen.getByRole('button')).toBeDisabled()
  expect(screen.getByTestId('spinner')).toBeInTheDocument()
})
```

#### 2. Verify RED - Watch It Fail

```bash
npm test -- --watch ComponentName
```

#### 3. GREEN - Write Minimal Code

Write simplest code to pass the test. Don't add features not in test.

#### 4. Verify GREEN - Watch It Pass

#### 5. REFACTOR - Clean Up

Only after green. Keep tests passing.

### Testing Library Query Priority

1. `getByRole` - accessible by everyone
2. `getByLabelText` - form fields
3. `getByText` - non-interactive elements
4. `getByTestId` - last resort

### Test Coverage Requirements

| Component Type | Required Tests                   |
| -------------- | -------------------------------- |
| UI Component   | Render, props, variants          |
| Form           | Validation, submit, error states |
| Interactive    | User events, callbacks           |
| Data Display   | Loading, error, empty states     |

### TDD Red Flags - STOP and Start Over

- Code before test
- Test passes immediately
- Testing implementation details
- `querySelector` everywhere

---

## Iron Law

**NO CODE WITHOUT APPROVED PLAN**

This rule is non-negotiable. Before writing code:

1. Task breakdown must exist and be approved
2. Acceptance criteria must be defined
3. Dependencies must be identified and available

### Rationalization Defense

| Excuse                         | Reality                                     |
| ------------------------------ | ------------------------------------------- |
| "It's a simple change"         | Simple changes often have hidden complexity |
| "I'll document after coding"   | Post-hoc documentation is always incomplete |
| "Tests can wait until later"   | Untested code is broken code                |
| "I know what needs to be done" | Assumptions without validation cause bugs   |
