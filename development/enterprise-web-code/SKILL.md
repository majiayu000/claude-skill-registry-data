---
name: enterprise-web-code
description: Enterprise-ready web development for Next.js 16, React, and TypeScript incorporating Kaizen (continuous improvement) and Monozukuri (meticulous craftsmanship) principles. Use this skill when building web applications, APIs, React components, Next.js projects, or when the user requests clean, efficient, fast, simple, elegant, enterprise-grade, bulletproof, or production-ready web code. This skill enforces modern web best practices, TypeScript patterns, React optimization, security, and performance.
---

# Enterprise Web Development

Build bulletproof, enterprise-ready web applications that embody Kaizen (continuous improvement) and Monozukuri (meticulous craftsmanship) principles. This skill guides development of clean, efficient, performant Next.js 16 and React code that is simple, elegant, and built to last.

## Core Philosophy

**Kaizen (改善)**: Continuous improvement through incremental refinement
**Monozukuri (ものづくり)**: The art of making things with meticulous attention to quality and craftsmanship

These principles translate to web code that is:
- **Clean**: Self-documenting, readable, and maintainable
- **Efficient**: Optimized bundles and minimal runtime overhead
- **Fast**: Performance-first architecture with sub-second load times
- **Simple**: Complexity only where justified
- **Elegant**: Beautiful solutions that feel inevitable

## Web Development Workflow

### 1. Understand Requirements Deeply

Before writing code:
- Clarify user experience and functionality goals
- Identify edge cases and error scenarios
- Consider responsive design and accessibility (WCAG 2.1)
- Understand performance budgets and SEO requirements
- Plan for internationalization if needed

### 2. Design Before Implementation

Plan the architecture:
- Choose appropriate Next.js rendering strategy (SSR, SSG, ISR, CSR)
- Design component hierarchy and data flow
- Plan API routes and data fetching patterns
- Consider state management needs (Server Components, Context, Zustand)
- Plan for type safety with TypeScript

### 3. Write Code with Craftsmanship

**Simplicity First**
- Prefer Server Components over Client Components
- Use native Web APIs when possible
- Avoid premature abstraction
- Keep components focused and composable
- YAGNI (You Aren't Gonna Need It)

**Clean Code Standards**
- Meaningful, descriptive names (components, functions, variables)
- Components should have single responsibility
- Keep components under 200 lines
- Extract complex logic into custom hooks
- Use early returns to reduce nesting
- Comments explain WHY, not WHAT

**TypeScript Best Practices**
- Use strict mode (`"strict": true`)
- Avoid `any` - use `unknown` or proper types
- Define interfaces for component props
- Use type inference where obvious
- Leverage discriminated unions for state
- Use Zod for runtime validation

**Error Handling**
- Use Error Boundaries for React errors
- Implement proper error pages (error.tsx, not-found.tsx)
- Validate user inputs on client AND server
- Provide actionable error messages
- Log errors with proper context
- Handle loading and error states

**Security Mindset**
- Sanitize user inputs (prevent XSS)
- Use CSRF tokens for mutations
- Implement proper authentication (NextAuth.js)
- Validate all API inputs with Zod
- Use environment variables for secrets
- Set proper security headers
- Implement rate limiting

### 4. Optimize for Web Performance

**Next.js 16 Optimization**
- Use Server Components by default
- Implement streaming with Suspense
- Optimize images with next/image
- Use dynamic imports for code splitting
- Implement Partial Prerendering (PPR)
- Leverage Turbopack for fast builds

**React Performance**
- Minimize client-side JavaScript
- Use React.memo for expensive components
- Implement virtual scrolling for long lists
- Debounce/throttle event handlers
- Avoid inline function definitions in JSX
- Use useCallback and useMemo judiciously

**Bundle Optimization**
- Tree-shake unused code
- Use dynamic imports for large dependencies
- Analyze bundle with @next/bundle-analyzer
- Remove unused dependencies
- Use barrel exports carefully (they prevent tree-shaking)

**Asset Optimization**
- Optimize images (WebP, AVIF formats)
- Lazy load images below the fold
- Use SVG for icons
- Implement font optimization (next/font)
- Minimize CSS with CSS modules or Tailwind

**Caching Strategy**
- Configure proper Cache-Control headers
- Use Next.js caching (fetch cache, unstable_cache)
- Implement stale-while-revalidate
- Use CDN for static assets
- Consider Redis for server-side caching

### 5. Ensure Robustness

**Comprehensive Testing**
- Unit tests for utility functions (Vitest)
- Component tests with React Testing Library
- E2E tests for critical flows (Playwright)
- Visual regression tests (Percy/Chromatic)
- API route tests

**Accessibility (A11y)**
- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Screen reader testing
- Color contrast compliance (WCAG AA)
- Focus management

**Progressive Enhancement**
- Core functionality works without JS
- Graceful degradation
- Loading states for all async operations
- Optimistic UI updates
- Error recovery strategies

**Monitoring and Observability**
- Implement error tracking (Sentry)
- Add performance monitoring (Vercel Analytics)
- Log important user actions
- Track Core Web Vitals
- Set up alerts for errors and performance

### 6. Refine Through Kaizen

Continuously improve:
- Review and refactor components
- Eliminate duplicate code
- Improve component composition
- Update dependencies regularly
- Address technical debt incrementally
- Monitor performance metrics

## Code Quality Standards

### File and Folder Structure

```
app/
├── (auth)/                 # Route groups
│   ├── login/
│   └── register/
├── (marketing)/
│   ├── page.tsx
│   └── layout.tsx
├── api/                    # API routes
│   └── users/
│       └── route.ts
├── dashboard/
│   ├── page.tsx
│   ├── loading.tsx
│   └── error.tsx
├── layout.tsx              # Root layout
└── globals.css

components/
├── ui/                     # Reusable UI components
│   ├── button.tsx
│   ├── card.tsx
│   └── input.tsx
└── features/               # Feature-specific components
    ├── auth/
    └── dashboard/

lib/
├── db.ts                   # Database client
├── auth.ts                 # Auth utilities
├── utils.ts                # Helper functions
└── validations.ts          # Zod schemas

hooks/                      # Custom React hooks
├── use-user.ts
└── use-debounce.ts

types/                      # TypeScript types
└── index.ts
```

### Naming Conventions

**Components**: PascalCase (`UserProfile.tsx`, `NavigationBar.tsx`)
**Files**: kebab-case for non-components (`api-client.ts`, `use-auth.ts`)
**Functions**: camelCase (`fetchUser`, `calculateTotal`, `handleSubmit`)
**Constants**: UPPER_SNAKE_CASE (`API_URL`, `MAX_RETRIES`)
**Types/Interfaces**: PascalCase (`User`, `ApiResponse`, `ButtonProps`)
**Props interfaces**: ComponentNameProps (`ButtonProps`, `CardProps`)

### Component Patterns

```typescript
// GOOD: Server Component (default)
export default async function UserProfile({ userId }: { userId: string }) {
  const user = await db.user.findUnique({ where: { id: userId } });
  
  return (
    <div>
      <h1>{user.name}</h1>
      <UserPosts userId={userId} />
    </div>
  );
}

// GOOD: Client Component (when needed)
'use client';

import { useState } from 'react';

interface CounterProps {
  initialCount?: number;
}

export function Counter({ initialCount = 0 }: CounterProps) {
  const [count, setCount] = useState(initialCount);
  
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}

// GOOD: Async Server Component with Suspense
export default function Page() {
  return (
    <Suspense fallback={<UserSkeleton />}>
      <UserProfile userId="123" />
    </Suspense>
  );
}
```

### TypeScript Patterns

```typescript
// Define prop types
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  isLoading?: boolean;
  children: React.ReactNode;
}

// Use discriminated unions for state
type FetchState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

// Zod for validation
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  age: z.number().min(18).max(120),
});

type User = z.infer<typeof userSchema>;
```

## Advanced Patterns

For complex scenarios, consult:
- **references/nextjs-patterns.md**: Next.js 16 specific patterns and best practices
- **references/react-performance.md**: React optimization techniques
- **references/web-security.md**: Comprehensive web security guide
- **references/typescript-patterns.md**: Advanced TypeScript patterns

## Next.js 16 Best Practices

### Server Components (Default)
- Use for data fetching
- Reduce client-side JavaScript
- Direct database access
- Better SEO

### Client Components ('use client')
Only use when you need:
- Interactivity (onClick, onChange)
- State (useState, useReducer)
- Effects (useEffect)
- Browser APIs
- Event listeners

### Data Fetching
```typescript
// Server Component - fetch in component
async function Users() {
  const users = await fetch('https://api.example.com/users', {
    next: { revalidate: 3600 } // ISR: revalidate every hour
  });
  
  return <UserList users={users} />;
}

// Server Actions - mutations
'use server';

export async function createUser(formData: FormData) {
  const data = userSchema.parse({
    name: formData.get('name'),
    email: formData.get('email'),
  });
  
  await db.user.create({ data });
  revalidatePath('/users');
}
```

### Streaming and Suspense
```typescript
export default function Page() {
  return (
    <>
      <Header />
      <Suspense fallback={<PostsSkeleton />}>
        <Posts />
      </Suspense>
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments />
      </Suspense>
    </>
  );
}
```

## Review Checklist

Before finalizing code:

- [ ] TypeScript strict mode enabled, no `any` types
- [ ] Components are Server Components unless interactivity needed
- [ ] Proper loading and error states
- [ ] Images use next/image with proper sizing
- [ ] Fonts optimized with next/font
- [ ] Forms validated on client and server
- [ ] API routes protected and validated
- [ ] Security headers configured
- [ ] Accessibility tested (keyboard, screen reader)
- [ ] Performance tested (Lighthouse score >90)
- [ ] SEO metadata complete
- [ ] Error boundaries implemented
- [ ] No console.log in production code
- [ ] Tests cover critical functionality

## When to Use This Skill

Apply this skill whenever:
- Building Next.js applications
- Creating React components
- Writing API routes
- Optimizing web performance
- Implementing authentication
- Setting up TypeScript projects
- User requests enterprise-grade web code
- User mentions Next.js, React, or web development

This skill transforms good web code into exceptional web applications—fast, secure, accessible, and delightful to use.
