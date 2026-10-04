---
name: tac-tdd
description: "MANDATORY for all non-trivial implementation in TAC Express. Enforces RED-GREEN-REFACTOR cycle with Vitest and Playwright. Write the failing test first, always."
---

# TAC Express — Test-Driven Development

Invoke this skill before writing any implementation code. The cycle is always:
**RED → GREEN → REFACTOR → COMMIT**

> **Iron Law:** Production code without a prior failing test is not TDD. Delete it and start over.

---

## The Cycle

```
1. Write failing test    ← RED   — test must fail for the right reason
2. Run test, confirm fail
3. Write minimal code    ← GREEN — only enough to pass
4. Run test, confirm pass
5. Refactor              ← clean up without breaking
6. Run test, still green
7. Commit
```

Repeat per feature/behavior. Never batch multiple RED→GREEN cycles without commits.

---

## Test File Conventions

```
Location:   Alongside source file
Naming:     ComponentName.test.tsx  |  featureName.service.test.ts
Framework:  Vitest (unit) | Playwright (E2E)
```

### Unit Test Template (Component)

```tsx
import { describe, it, expect, vi } from "vitest"
import { render, screen } from "@testing-library/react"
import { userEvent } from "@testing-library/user-event"
import { ComponentName } from "./ComponentName"

describe("ComponentName", () => {
  it("renders with default variant", () => {
    render(<ComponentName>content</ComponentName>)
    expect(screen.getByText("content")).toBeInTheDocument()
  })

  it("applies glass variant correctly", () => {
    const { container } = render(<ComponentName variant="glass" />)
    expect(container.firstChild).toHaveAttribute("data-slot", "component-name")
  })

  it("calls onClick when clicked", async () => {
    const user = userEvent.setup()
    const onClick = vi.fn()
    render(<ComponentName onClick={onClick}>click me</ComponentName>)
    await user.click(screen.getByText("click me"))
    expect(onClick).toHaveBeenCalledOnce()
  })
})
```

### Unit Test Template (Service)

```ts
import { describe, it, expect, vi, beforeEach } from "vitest"
import { createClient } from "@workspace/database"
import { getShipments } from "./shipment.service"

vi.mock("@workspace/database")

describe("shipment.service", () => {
  const mockDb = {
    from: vi.fn().mockReturnThis(),
    select: vi.fn().mockReturnThis(),
    eq: vi.fn().mockResolvedValue({ data: [], error: null }),
  }

  beforeEach(() => {
    vi.mocked(createClient).mockReturnValue(mockDb as any)
  })

  it("returns empty array when no shipments", async () => {
    const result = await getShipments({ userId: "user-1" })
    expect(result).toEqual([])
  })

  it("throws on database error", async () => {
    mockDb.eq.mockResolvedValue({ data: null, error: { message: "DB error" } })
    await expect(getShipments({ userId: "user-1" })).rejects.toThrow("DB error")
  })
})
```

---

## What to Test

### Always Test (Components)
- Default render (snapshot optional)
- Each CVA variant produces correct `data-slot`
- Interactive states (click, focus, keyboard)
- Error/loading/empty states
- Accessibility: `aria-label`, `role`, keyboard navigation

### Always Test (Services)
- Happy path with mocked DB
- Error from database → throws with message
- Invalid input → throws or returns typed error
- Data transformation (input → output shape)

### Always Test (Hooks)
- Initial state
- State after async operation (use `act`)
- Cleanup on unmount

### Never Test
- CSS class names directly (fragile, not behavior)
- Implementation details (private functions)
- Third-party library behavior (they have their own tests)
- Snapshot tests without intent (use sparingly)

---

## Mocking Rules

```
Mock at the boundary only:
  ✅ Mock packages/database in service tests
  ✅ Mock packages/services in component tests
  ❌ Never mock internal implementation details
  ❌ Never add test-only methods to production code
```

### Mock Location

```
packages/services/__mocks__/      ← auto-mocked services
packages/database/__mocks__/      ← auto-mocked db client
```

---

## Running Tests

```bash
# From monorepo root only:
pnpm test                  # all packages
pnpm test --filter ui      # specific package
pnpm test -- --watch       # watch mode

# E2E (Playwright):
pnpm test:e2e
```

---

## Quality Gate Before Commit

```bash
pnpm test                  # all tests pass
pnpm typecheck             # zero TypeScript errors
pnpm lint --max-warnings 0 # zero lint warnings
```

All three must be green. No exceptions.

---

## Anti-Patterns to Reject

| Anti-pattern | Why | Fix |
|--------------|-----|-----|
| `it.skip(...)` without comment | Masks failures | Add `// TODO: TAC-XXX — reason` |
| Testing mock behavior | Not real behavior | Test real outputs |
| `expect(true).toBe(true)` | Always passes | Write meaningful assertion |
| Test written after implementation | Not TDD | Delete impl, write test first |
| Giant test file > 300 lines | Too broad scope | Split into focused test files |

---

## TAC-Specific Testing Notes

- Violet Grid components: test `data-slot` attributes, not class names
- Services: always mock `@workspace/database`, never real Supabase in unit tests
- Icons: mock `@workspace/ui/icons` if testing components that use icons
- Tokens: don't test CSS variable values — they're design-time, not runtime
