---
name: writing-plans
description: Write implementation plans that make coding obvious — exact file paths, full code examples, step-by-step commands, expected output. Use before any feature with 3+ files or when delegating to subagents.
license: MIT
source: https://github.com/NousResearch/hermes-agent
---

# Writing Plans

A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.

**Trigger phrases:** "write a plan", "implementation plan", "plan before coding", "spec out", "break down task", "planning phase"

---

## Plan Template

```markdown
# Plan: [Feature Name]

## Goal
One sentence: what does this plan deliver?

## Architecture
How does this fit the existing system?

## Constraints
- Language/framework versions
- Libraries to use
- Things NOT to change

---

## Task 1: [Specific Title]

**Objective:** What this accomplishes (1-2 sentences)

**Files:**
- `src/auth/token.ts` — create (new file)
- `src/auth/verify.ts` — modify (add expiry check)
- `tests/auth/token.test.ts` — create

**Implementation:**
```typescript
// src/auth/token.ts
export function createToken(userId: string, expiresIn = '24h'): string {
  return sign({ userId }, process.env.JWT_SECRET!, { expiresIn })
}
```

**Commands:**
```bash
npm test -- --testPathPattern=auth
```

**Expected output:**
```
PASS tests/auth/token.test.ts
  ✓ creates valid JWT (12ms)
```

**Acceptance criteria:**
- [ ] Token signed with JWT_SECRET
- [ ] Expiry enforced on verify
- [ ] Tests pass, no regressions
```

---

## The 5 Rules

**1. Exact file paths** — not "the auth module" but `src/auth/token.ts`

**2. Copy-pasteable code** — not pseudocode, actual working code

**3. Real commands** — not "run the tests" but `npm test -- --testPathPattern=auth`

**4. Expected output** — what does success look like, exactly?

**5. Atomic tasks** — one task = one person, no file overlap with other tasks

---

## Task Sizing

| Size | Lines changed | Time | Action |
|------|--------------|------|--------|
| Too small | < 5 lines | < 5 min | Merge with adjacent |
| Right | 10–100 lines | 15–60 min | ✓ |
| Too large | > 200 lines | > 2h | Split into 2–3 tasks |

---

## File Conflict Check

Before finalizing — verify no two tasks touch the same file:

```
Task 1: src/auth/token.ts   ✓
Task 2: src/auth/verify.ts  ✓
Task 3: src/auth/token.ts   ✗  ← conflict with Task 1 → merge or extract
```

---

## Dependency Map

```
Task 1 (no deps) ─┐
Task 2 (no deps) ─┤→ Task 4 (needs 1+2) → Task 5 (needs 4)
Task 3 (no deps) ─┘
```

Tasks without deps run in parallel. Always declare dependencies explicitly.

---

## Anti-Fake-Pass

```
❌ "Update the auth logic" — no file, no code, not actionable
❌ "Add tests" — which tests? what file? what assertions?
❌ One giant task — can't parallelize or review incrementally
❌ Task touching 5+ unrelated files — split it
❌ Expected output is "it should work" — not verifiable
❌ No dependency declaration — parallel agents conflict
```

## See Also
- `core/rules/golden-principles.md` — Principle 9: plan before code
- `core/skills/kanban-dispatcher/SKILL.md` — execute plans with task board
- `core/agents/spec-planner.md` — planning agent
