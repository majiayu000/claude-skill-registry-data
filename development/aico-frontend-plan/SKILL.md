---
name: aico-frontend-plan
description: |
  Create ATOMIC implementation plan for a single frontend task. Each step has exact code and verification command.

  IMPORTANT: This skill creates MICRO-LEVEL atomic steps, NOT macro architecture plans.
  For architecture planning or feature scoping, use EnterPlanMode instead.

  Use this skill when:
  - Running /frontend.plan command
  - User explicitly asks for "atomic steps", "step-by-step plan with verification"
  - Have a specific task from docs/reference/frontend/tasks/ and need implementation steps
  - Need granular steps: Setup (create files) → Implementation (write code) → Test (verify) → Commit

  DO NOT use for:
  - Architecture planning (use EnterPlanMode)
  - General development planning
  - Feature scoping or estimation

  Output: Present plan to user (not saved to file), each step includes Files, Action, and Verify command.
---

# Plan

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read task**: Get task details from `docs/reference/frontend/tasks/{story}.md`
2. **Read design**: Load related design from `docs/reference/frontend/designs/`
3. **Read constraints**: Load `docs/reference/frontend/constraints.md`
4. **Break into atomic steps**:
   - Start with file creation/setup
   - One section/feature per step
   - Include verification for each step
   - End with commit
5. **Keep steps atomic**: One action per step
6. **Present plan to user** (do not save to file)

## Plan Format

````markdown
# [Task Name] - Implementation Plan

> Project: [project-name]
> Created: YYYY-MM-DD
> Task: [task description]
> Design: docs/reference/frontend/designs/[name].md
> Estimated steps: N

## Step 1: [Action]

**Files**:

- Create: `src/components/[Name].tsx`
- Modify: `src/pages/[Page].tsx:L10-L20`

**Action**:
[Exact code or action to take]

**Verify**:

```bash
[verification command]
```
````

Expected: [expected output]

---

## Step N: Commit

```bash
git add [files]
git commit -m "feat: [description]"
```

````

## Step Granularity

Each step = ONE atomic action:

| Good Steps | Bad Steps |
|------------|-----------|
| Create component file with imports | Create component with all logic |
| Add component skeleton (empty return) | Implement entire component |
| Implement single section | Implement all sections |
| Write one test case | Write all tests |

## Step Types

### Setup Step
```markdown
**Files**: Create: `src/components/ProfileCard.tsx`
**Action**: Create file with basic structure
**Verify**: `npx tsc --noEmit` → No errors
````

### Implementation Step

```markdown
**Files**: Modify: `src/components/ProfileCard.tsx:L8-L10`
**Action**: Implement header section with Avatar and name
**Verify**: `npm run dev` → Component renders correctly
```

### Test Step

```markdown
**Files**: Create: `src/components/__tests__/ProfileCard.test.tsx`
**Action**: Write unit test for profile name rendering
**Verify**: `npm test ProfileCard` → 1 test passed
```

## Key Rules

- ALWAYS include verification command for each step
- MUST keep steps to 2-5 minutes of work
- ALWAYS end with a commit step
- NEVER combine multiple actions into one step

## Common Mistakes

- ❌ Steps too large → ✅ One action per step
- ❌ Skip verification → ✅ Every step has verify command
- ❌ Vague actions → ✅ Include exact code
- ❌ No commit step → ✅ Always end with git commit
