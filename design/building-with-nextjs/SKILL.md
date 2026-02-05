---
name: building-with-nextjs
description: Use when building web UIs with Next.js 15+ and React 19 - covers Server Components, App Router, testing with Vitest and Playwright, and accessibility standards
---

# Building with Next.js

## Overview

Modern web UI with **Next.js 15+** (App Router) + **React 19** (Server Components) + **TypeScript** (strict mode).

Extends `configuring-javascript-stack` with web-specific patterns.

## Additional Tooling

```bash
pnpm add -D @playwright/test @axe-core/playwright
pnpm add -D @testing-library/react @testing-library/jest-dom jsdom
pnpm exec playwright install
```

## Project Structure

```
app/                    # Next.js App Router
├── page.tsx            # Homepage
├── layout.tsx          # Root layout
├── globals.css         # Global styles
└── [route]/page.tsx    # Additional pages

components/
├── layout/             # Nav, footer, container
├── sections/           # Hero, CTA, features
├── ui/                 # Buttons, headings, cards
├── forms/              # Form components
└── providers/          # Context providers

lib/                    # Utility functions
types/                  # TypeScript definitions
public/                 # Static assets
tests/
├── e2e/                # Playwright tests
└── components/         # Component tests
```

## Component Architecture

**Server Components (default):**
```typescript
// app/page.tsx - Server Component
export default function HomePage() {
  // Can use Node.js APIs, database queries
  return <div>Server-rendered content</div>
}
```

**Client Components (only when needed):**
```typescript
// components/ui/Button.tsx
'use client'

import { useState } from 'react'

export default function Button() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

## Component Organization

- **layout/** - Page structure (nav, footer, container) - usually Server
- **sections/** - Large sections (hero, CTA) - usually Server
- **ui/** - Small reusable components - Server or Client
- **forms/** - Form-specific - usually Client (state)
- **providers/** - Context providers - always Client

## Testing

**Component tests (Vitest + React Testing Library):**
```typescript
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Button from './Button'

describe('Button', () => {
  it('renders with primary variant', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button')).toBeInTheDocument()
  })
})
```

**E2E tests (Playwright):**
```typescript
import { test, expect } from '@playwright/test'

test('navigation works', async ({ page }) => {
  await page.goto('/')
  await page.click('text=About')
  await expect(page).toHaveURL('/about')
})
```

**Accessibility tests:**
```typescript
import AxeBuilder from '@axe-core/playwright'

test('homepage has no a11y violations', async ({ page }) => {
  await page.goto('/')
  const results = await new AxeBuilder({ page }).analyze()
  expect(results.violations).toEqual([])
})
```

## Configuration Files

**vitest.config.ts:**
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      thresholds: { lines: 80, functions: 80, branches: 80 },
    },
  },
})
```

**playwright.config.ts:**
```typescript
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  use: {
    baseURL: 'http://localhost:3000',
  },
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3000',
  },
})
```

## Quality Gates

All from `configuring-javascript-stack` plus:
- **Component tests:** All UI components tested
- **E2E tests:** Critical user flows pass
- **Accessibility:** Zero Axe violations

## justfile Commands

```just
dev:
    pnpm install
    pnpm dev

build:
    pnpm build

test-e2e:
    pnpm playwright test

a11y:
    pnpm playwright test accessibility.spec.ts

check-all: format lint typecheck test coverage test-e2e a11y
    @echo "✅ All checks passed"
```

## Common Patterns

**Data fetching in Server Components:**
```typescript
async function getPosts() {
  const res = await fetch('https://api.example.com/posts')
  return res.json()
}

export default async function BlogPage() {
  const posts = await getPosts()
  return <div>{posts.map(post => <article key={post.id}/>)}</div>
}
```

**Client/Server composition:**
```typescript
// Navigation.tsx (Server Component)
import NavigationClient from './NavigationClient'

export default function Navigation() {
  const links = [{ href: '/', label: 'Home' }]
  return <NavigationClient links={links} />
}

// NavigationClient.tsx
'use client'
import { useState } from 'react'

export default function NavigationClient({ links }) {
  const [isOpen, setIsOpen] = useState(false)
  // Interactive UI
}
```

## Performance Best Practices

1. **Server Components by default** - Smaller JS bundle
2. **Code splitting** - Automatic with App Router
3. **Image optimization** - Use `<Image>` component
4. **Font optimization** - Use `next/font`
5. **Lazy loading** - Use `dynamic()` for heavy components

## Accessibility Best Practices

1. **Semantic HTML** - Use `<button>`, `<nav>`, etc.
2. **Keyboard navigation** - All interactive elements accessible
3. **ARIA labels** - When semantic HTML isn't enough
4. **Focus management** - Visible indicators, logical tab order
5. **Alt text** - All images descriptive
6. **Color contrast** - WCAG AA minimum (4.5:1)
