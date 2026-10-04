---
name: react-expert
description: React development expertise from Meta engineers who built React for billions of users. Use when building React components, implementing hooks, managing state, optimizing performance, or debugging React issues. Triggers on React, useState, useEffect, useContext, useMemo, useCallback, component patterns, JSX, React Query, Redux, Zustand, Server Components.
---

# React Expert Skill

## Overview

React expertise from Meta engineers who built and scaled React to billions of users.

## What Qualifies as "React Expert"

### Level 10/10 (World-class)
- Contributed to React core or major ecosystem libraries
- Built systems serving billions of users
- Deep understanding of React internals (fiber, reconciliation)
- 10+ years of React experience
- Examples: React Core Team members at Meta

### Level 9/10 (Deep Expert)
- Architected large-scale React applications
- Expert in performance optimization
- Can design complex state management solutions
- 7+ years of React experience
- Examples: Tech leads at Meta, Airbnb, Netflix

### Level 8/10 (Senior)
- Can architect scalable React applications
- Strong understanding of performance
- Mentors other developers
- 5+ years of React experience

## Key Capabilities

### Core React
- Components, hooks, lifecycle
- Context API, state management
- Performance optimization (memo, useMemo, useCallback)
- Code splitting, lazy loading
- Server Components (React 18+)

### Ecosystem
- **Next.js**: SSR, SSG, App Router, Server Components
- **State Management**: Redux, Zustand, Jotai, Recoil
- **Data Fetching**: React Query, SWR, Apollo
- **Styling**: CSS-in-JS, Tailwind, Styled Components

### Advanced Topics
- React Server Components
- Concurrent Mode
- Suspense for data fetching
- Custom hooks design
- Performance profiling
- Micro-frontends with React

### Testing
- Jest
- React Testing Library
- Playwright/Cypress for E2E

## Notable React Projects at FAANG

### Meta
- Facebook.com (3B+ users)
- Instagram Web (2B+ users)
- WhatsApp Web
- React framework itself

### Netflix
- Netflix.com (200M+ subscribers)
- Advanced performance optimizations
- Server-side rendering at scale

### Airbnb
- Airbnb.com
- Design system (now deprecated but influential)

## When to Need React Experts

Projects requiring:
- Complex web applications
- High-performance UIs
- Real-time features (feeds, messaging)
- Server-side rendering
- Micro-frontend architectures
- Design systems
- Billion-user scale

## Common Patterns from FAANG

### Performance Patterns
```typescript
// Virtualized lists for large datasets (Meta pattern)
import { VirtualList } from '@/components/VirtualList';

// Optimized component with memoization
const FeedItem = memo(({ post }) => {
  // Render logic
});

// Custom hooks for data fetching
function useFeed(userId) {
  return useInfiniteQuery(['feed', userId], fetchFeed);
}
```

### Code Splitting Patterns
```typescript
// Route-based splitting (Netflix pattern)
const Dashboard = lazy(() => import('./Dashboard'));

// Component-based splitting for heavy features
const VideoPlayer = lazy(() => import('./VideoPlayer'));
```

### State Management Patterns
```typescript
// Zustand for simple global state (Meta pattern)
const useStore = create((set) => ({
  user: null,
  setUser: (user) => set({ user })
}));
```

## Typical Responsibilities

React experts at FAANG typically:
- Design component architectures
- Optimize bundle sizes
- Improve Core Web Vitals
- Build design systems
- Mentor junior developers
- Review code for performance
- Make framework decisions

## Related Skills

React experts often also have:
- **TypeScript** (type safety)
- **JavaScript** (ES6+, async patterns)
- **CSS** (responsive design, animations)
- **Testing** (Jest, RTL)
- **Build Tools** (Webpack, Vite, Turbopack)
- **Performance** (Lighthouse, profiling)
