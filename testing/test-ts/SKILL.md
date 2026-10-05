---
name: test-ts
description: "Write, review, and run TypeScript/React tests for this Next.js 16 App Router project. Use whenever writing or modifying *.test.ts or *.test.tsx files, adding test coverage to components, hooks, Server Actions, or utilities, setting up Vitest configuration, or asked about testing strategy. Covers Vitest (the project's test runner, not Jest), React Testing Library v16, accessibility-first queries, user-event for interactions, AAA structure, parameterized tests with describe.each and it.each, Prisma mock patterns, next/navigation and next/headers mocking, and the RSC boundary testing strategy. Do NOT use for Playwright end-to-end tests or performance benchmarks."
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: testing
---

# TypeScript/React testing

This project uses **Vitest** as the test runner. The Next.js 16 official documentation recommends Vitest over Jest for App Router projects: native ESM and TypeScript support require no additional transformation configuration, and Vitest runs 3–5x faster than Jest on equivalent suites. Do not introduce Jest.

## Test runner commands

```bash
npm test                                   # run all tests once
npm run test:watch                         # watch mode
npm run test:coverage                      # with coverage report

# Targeted runs
npx vitest run src/components/invoice/     # run tests in a directory
npx vitest run -t "renders the client"     # filter by test name pattern
npx vitest run path/to/component.test.tsx  # run a single file
```

## Decision framework

Before writing any test, classify it:

| Category | What it covers | Vitest environment |
|---|---|---|
| **Unit** | Pure functions, utilities, Zod schemas, computed logic | `node` |
| **Component** | Client Components rendered with RTL | `jsdom` |
| **Hook** | Custom hooks via `renderHook` | `jsdom` |
| **Server Action** | `'use server'` functions with mocked Prisma | `node` |
| **Integration** | Real database or external service | `node` + env gate |

`jsdom` is the default environment configured in `vitest.config.ts`. For Server Actions and utilities, add a file-level directive to switch to `node`:

```typescript
// @vitest-environment node
import { describe, it, expect, vi, beforeEach } from 'vitest';
```

Pick the lightest category that validates the behavior. Async Server Components (RSCs) cannot be rendered by RTL; see "RSC testing strategy" below and [references/rsc-patterns.md](references/rsc-patterns.md) for full mocking recipes.

## File organization

- One test file per source file: `invoice-card.tsx` maps to `invoice-card.test.tsx`.
- Co-locate test files next to the source file, not in a separate `__tests__/` directory.
- Fixture factories live in `src/__fixtures__/<domain>.fixtures.ts`.
- All new features require tests; every bug fix requires a regression test.

## Canonical test structure

Every test file follows the Arrange/Act/Assert pattern separated by blank lines. Do NOT write `// Arrange`, `// Act`, or `// Assert` comments. Tests read like a specification.

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';

import { InvoiceCard } from './invoice-card';
import { buildInvoice } from '@/__fixtures__/invoice.fixtures';

describe('InvoiceCard', () => {
  it('renders the client name and formatted amount', () => {
    const invoice = buildInvoice({ clientName: 'Acme Corp', amount: 1500 });

    render(<InvoiceCard invoice={invoice} />);

    expect(screen.getByRole('heading', { name: 'Acme Corp' })).toBeInTheDocument();
    expect(screen.getByText('$1,500.00')).toBeInTheDocument();
  });

  it('calls onMarkPaid with the invoice id when the mark-paid button is clicked', async () => {
    const user = userEvent.setup();
    const onMarkPaid = vi.fn();
    const invoice = buildInvoice({ status: 'unpaid' });

    render(<InvoiceCard invoice={invoice} onMarkPaid={onMarkPaid} />);
    await user.click(screen.getByRole('button', { name: /mark paid/i }));

    expect(onMarkPaid).toHaveBeenCalledExactlyOnceWith(invoice.id);
  });

  it('disables the mark-paid button when isPending is true', () => {
    const invoice = buildInvoice({ status: 'unpaid' });

    render(<InvoiceCard invoice={invoice} isPending />);

    expect(screen.getByRole('button', { name: /mark paid/i })).toBeDisabled();
  });
});
```

Structural rules:
- `describe` names the component or function under test. Nest `describe` blocks to scope a scenario or method.
- `it` reads as a complete sentence: `it('disables the submit button while the mutation is pending')`.
- Each `it` block covers one logical scenario. Split complex assertions into focused tests.

## RTL query priority

Use queries in accessibility-first order:

1. `getByRole` (first choice; exercises semantic HTML)
2. `getByLabelText` (for labeled form inputs)
3. `getByPlaceholderText` (fallback for unlabeled inputs)
4. `getByText` (for non-interactive text content)
5. `getByTestId` (last resort; add `data-testid` only when no semantic query fits)

```typescript
// ✅ Accessibility-first
screen.getByRole('button', { name: /save invoice/i });
screen.getByLabelText('Invoice amount');
screen.getByRole('alert');
screen.getByRole('combobox', { name: 'Status' });

// ❌ Coupled to implementation details
screen.getByTestId('save-btn');
container.querySelector('.invoice-form');
```

## User interactions

Always use `@testing-library/user-event`, not `fireEvent`. `user-event` simulates the full browser event sequence (pointerdown, focus, input, keydown, keyup, click). `fireEvent` dispatches a single synthetic event and misses intermediary behavior that real components react to.

```typescript
const user = userEvent.setup();

await user.type(screen.getByLabelText('Client name'), 'Acme Corp');
await user.selectOptions(screen.getByRole('combobox', { name: 'Status' }), 'paid');
await user.click(screen.getByRole('button', { name: /save/i }));
await user.keyboard('{Escape}');
await user.clear(screen.getByRole('textbox', { name: 'Amount' }));
```

## Parameterized tests

Use `describe.each` or `it.each` whenever multiple inputs share the same execution logic. Never loop with `.forEach` inside a single `it` block.

```typescript
// ✅ Parameterized: each case gets its own entry in the test report
it.each([
  { status: 'paid',    label: 'Paid',    expectedClass: 'bg-green-100'  },
  { status: 'overdue', label: 'Overdue', expectedClass: 'bg-red-100'    },
  { status: 'pending', label: 'Pending', expectedClass: 'bg-yellow-100' },
  { status: 'draft',   label: 'Draft',   expectedClass: 'bg-muted'      },
])('renders "$label" badge with the correct color for $status status', ({ status, label, expectedClass }) => {
  render(<StatusBadge status={status} />);

  const badge = screen.getByRole('status');
  expect(badge).toHaveTextContent(label);
  expect(badge).toHaveClass(expectedClass);
});

// ✅ describe.each when each group needs multiple it blocks
describe.each([
  { dueDate: new Date('2025-01-01'), expectedStatus: 'overdue'  },
  { dueDate: new Date('2030-01-01'), expectedStatus: 'upcoming' },
])('invoice due $dueDate', ({ dueDate, expectedStatus }) => {
  it('displays the correct status badge', () => { ... });
  it('sorts before invoices due later', () => { ... });
});

// ❌ forEach hides failures and conflates scenarios
it('handles all badge statuses', () => {
  ['paid', 'overdue', 'pending'].forEach((status) => {
    render(<StatusBadge status={status} />);
    // ...
  });
});
```

## Fixture factories

Build domain objects with factory functions, not inline literals. Inline literals couple tests to schema shape and break silently when fields are added or renamed.

```typescript
// src/__fixtures__/invoice.fixtures.ts
import type { Invoice } from '@/types/invoice.types';

export function buildInvoice(overrides: Partial<Invoice> = {}): Invoice {
  return {
    id: 'inv_test_001',
    clientName: 'Test Client',
    amount: 1000,
    currency: 'USD',
    status: 'unpaid',
    dueDate: new Date('2026-12-31'),
    createdAt: new Date('2026-01-01'),
    userId: 'user_test_001',
    ...overrides,  // must be last so callers can override any field
  };
}
```

Co-locate factories with the domain type. One factory per domain entity. Name them `build<Entity>`.

## Server Action testing

Call the Server Action function directly. Mock the Prisma client at the module boundary.

```typescript
// @vitest-environment node
import { describe, it, expect, vi, beforeEach } from 'vitest';

import { markInvoicePaid } from '@/lib/actions/invoice-actions';

vi.mock('@/lib/db', () => ({
  db: {
    invoice: {
      findUnique: vi.fn(),
      update: vi.fn(),
    },
  },
}));

vi.mock('next/cache', () => ({
  revalidateTag: vi.fn(),
}));

describe('markInvoicePaid', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns success and revalidates the invoices cache tag', async () => {
    const { db } = await import('@/lib/db');
    const { revalidateTag } = await import('next/cache');
    vi.mocked(db.invoice.findUnique).mockResolvedValue(buildInvoice({ userId: 'user_1' }));
    vi.mocked(db.invoice.update).mockResolvedValue(buildInvoice({ status: 'paid' }));

    const result = await markInvoicePaid({ invoiceId: 'inv_test_001', paidAt: new Date('2026-03-01') });

    expect(result).toEqual({ success: true });
    expect(revalidateTag).toHaveBeenCalledWith('invoices');
  });

  it('returns field errors without calling the database when invoiceId is empty', async () => {
    const { db } = await import('@/lib/db');

    const result = await markInvoicePaid({ invoiceId: '', paidAt: new Date() });

    expect(result.success).toBe(false);
    expect(result.fieldErrors?.invoiceId).toBeDefined();
    expect(db.invoice.update).not.toHaveBeenCalled();
  });
});
```

Rules:
- `vi.clearAllMocks()` in `beforeEach` prevents state from leaking between tests.
- `vi.mocked()` provides typed access to mock functions. Never cast to `any`.
- Import mocked modules inside the test body with `await import(...)` after `vi.mock()` hoisting.
- Always test the Zod validation-failure path. Do not only cover the happy path.

For Prisma chains with relations, pagination, or `$transaction`, see [references/mocking-patterns.md](references/mocking-patterns.md).

## RSC testing strategy

Async Server Components cannot be rendered by React Testing Library. They execute on the server and return RSC payloads; `jsdom` has no mechanism for this. Use three complementary approaches.

**Extract and unit-test the data layer.** If an RSC calls `db.invoice.findMany()`, extract that into a standalone async function and test it in the `node` environment with a mocked Prisma client. The RSC becomes a thin rendering shell.

```typescript
// src/lib/data/invoice-data.ts (extracted, testable)
export async function getInvoicesForUser(userId: string): Promise<Invoice[]> {
  return db.invoice.findMany({ where: { userId }, orderBy: { createdAt: 'desc' } });
}
```

```typescript
// @vitest-environment node
it('returns an empty array when the user has no invoices', async () => {
  vi.mocked(db.invoice.findMany).mockResolvedValue([]);

  const result = await getInvoicesForUser('user_123');

  expect(result).toEqual([]);
});
```

**Test the Client Component leaves.** The interactive parts of RSC trees are Client Components. Test those normally with RTL. The RSC serves as a server-rendered shell; the interactive leaves are fully covered by component tests.

**Use E2E for full-page rendering.** Playwright renders through the real Next.js server, the only environment where RSCs execute. Use Playwright for assertions that require the full RSC pipeline: Suspense boundaries, `loading.tsx` states, streaming.

```typescript
// ❌ Async Server Components are server functions; render() does not work
render(<InvoicesPage />);

// ✅ Test the extracted data function in node environment
// ✅ Test the Client Component leaf separately
// ✅ Test the full page with Playwright
```

For mocking `next/navigation`, `next/headers`, `cookies()`, and Auth.js `auth()` in code called by RSCs or Server Actions, see [references/rsc-patterns.md](references/rsc-patterns.md).

## Hook testing

Test custom hooks with `renderHook` from React Testing Library. Wrap timer-dependent behavior with `vi.useFakeTimers()`.

```typescript
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

import { useJobPoller } from './use-job-poller';

describe('useJobPoller', () => {
  beforeEach(() => { vi.useFakeTimers(); });
  afterEach(() => { vi.useRealTimers(); });

  it('starts in pending state when a jobId is provided', () => {
    const { result } = renderHook(() => useJobPoller('job_001'));

    expect(result.current.status).toBe('pending');
  });

  it('transitions to completed when the polling interval resolves', async () => {
    const fetchStatus = vi.fn().mockResolvedValue('completed');

    const { result } = renderHook(() => useJobPoller('job_001', { fetchStatus }));
    await act(() => vi.runAllTimersAsync());

    expect(result.current.status).toBe('completed');
    expect(fetchStatus).toHaveBeenCalledWith('job_001');
  });

  it('returns null status when no jobId is provided', () => {
    const { result } = renderHook(() => useJobPoller(null));

    expect(result.current.status).toBeNull();
  });
});
```

## Forbidden patterns

| Pattern | Reason |
|---|---|
| Snapshot tests for complex UI | Brittle; asserts structure, not behavior. Allowed only for simple deterministic pure-output functions. |
| `any` in mock types | Defeats TypeScript strictness in test files. Use `vi.mocked()` for typed mocks. |
| Real database calls | Slow, order-dependent, and fragile in CI. Mock Prisma at the module boundary. |
| `fireEvent` for user interactions | Skips the full browser event sequence. Use `userEvent` instead. |
| `// Arrange`, `// Act`, `// Assert` comments | Tests should read naturally. Blank lines separate the phases. |
| Inline domain object literals | Couples tests to schema shape. Use fixture factories. |
| `.forEach` inside a single `it` block | Hides individual failures in the report. Use `it.each` instead. |
| Multiple unrelated assertions per `it` | Makes failure diagnosis harder. One scenario per test. |
| `jest.*` APIs | This project uses Vitest. The equivalent APIs are `vi.fn()`, `vi.mock()`, `vi.mocked()`, `vi.spyOn()`. |

---

## Validation checklist

After writing or modifying tests, verify:

- [ ] `npm test` passes with no failures
- [ ] `// @vitest-environment node` present on all Server Action and utility test files
- [ ] RTL queries use `getByRole`, `getByLabelText`, or `getByText` as the first choice
- [ ] All user interactions use `userEvent`, not `fireEvent`
- [ ] Multiple-input scenarios use `it.each` or `describe.each`, not `.forEach`
- [ ] Domain objects built with fixture factories; no raw inline literals
- [ ] `vi.clearAllMocks()` called in `beforeEach` when tests share mocked modules
- [ ] `vi.mocked()` used for typed mock access; no `as jest.Mock` casts
- [ ] Async Server Component logic extracted into standalone testable functions
- [ ] Zod validation-failure paths covered in Server Action tests
- [ ] New features have tests; bug fixes have regression tests
