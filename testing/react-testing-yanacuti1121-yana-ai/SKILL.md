---
name: react-testing
description: React component testing with React Testing Library + Vitest/Jest + MSW network mocking + axe accessibility assertions. Covers unit, integration, and component vs E2E decision boundary.
license: MIT
source: https://github.com/affaan-m/ECC
---

# React Testing

Test behavior, not implementation. Query by role/label, not CSS or test-id.

**Trigger phrases:** "test React component", "RTL", "React Testing Library", "write tests for component", "MSW mock", "accessibility test"

---

## Core Principle

```tsx
// ✅ Query as users perceive
const button = screen.getByRole('button', { name: /submit/i })
const input  = screen.getByLabelText('Email address')

// ❌ Implementation details
screen.getByClassName('btn-primary')
screen.getByTestId('submit-btn')
```

---

## Component Test Template

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

describe('LoginForm', () => {
  it('calls onSubmit with credentials', async () => {
    const onSubmit = vi.fn()
    render(<LoginForm onSubmit={onSubmit} />)

    await userEvent.type(screen.getByLabelText('Email'), 'a@b.com')
    await userEvent.type(screen.getByLabelText('Password'), 'secret')
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }))

    expect(onSubmit).toHaveBeenCalledWith({ email: 'a@b.com', password: 'secret' })
  })
})
```

---

## MSW Network Mocking

```ts
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

const server = setupServer(
  http.get('/api/users', () => HttpResponse.json([{ id: 1, name: 'Alice' }])),
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

---

## Accessibility Testing

```ts
import { axe, toHaveNoViolations } from 'jest-axe'
expect.extend(toHaveNoViolations)

it('has no a11y violations', async () => {
  const { container } = render(<LoginForm onSubmit={vi.fn()} />)
  expect(await axe(container)).toHaveNoViolations()
})
```

---

## Component vs E2E Decision

| Test | Tool |
|------|------|
| Component renders + behaves | RTL |
| Network request handling | RTL + MSW |
| Full user flow across pages | Playwright |
| Visual regression | Playwright screenshots |

---

## Async Patterns

```tsx
// ✅ findBy* has built-in waitFor
const result = await screen.findByRole('status')

// ❌ Arbitrary timeouts
await new Promise(r => setTimeout(r, 1000))
```

---

## Anti-Fake-Pass

```
❌ Testing internal state (useState calls) not user-visible behavior
❌ Not using userEvent.setup() — legacy fireEvent misses pointer events
❌ Mocking fetch globally instead of MSW — brittle, order-dependent
❌ Full DOM snapshot tests — any refactor breaks them
```
