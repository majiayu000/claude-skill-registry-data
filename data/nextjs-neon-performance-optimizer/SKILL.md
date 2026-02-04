---
name: nextjs-neon-performance-optimizer
description: Comprehensive performance analysis and optimization for Next.js applications using Neon Postgres. Identifies bottlenecks across frontend, backend, and database layers.
triggers:
  - optimize
  - performance  
  - slow
  - faster
  - speed up
  - bottleneck
  - Core Web Vitals
  - database performance
  - query optimization
  - Neon
---

# Next.js + Neon Postgres Performance Optimizer

Comprehensive performance analysis and optimization for Next.js applications using Neon Postgres.

## When This Skill Activates

- User mentions "optimize", "performance", "slow", "faster", "bottleneck"
- User asks about Core Web Vitals, page speed, or load times
- User requests database query optimization
- User mentions Neon, PostgreSQL performance
- Before deployment reviews

## ⚠️ CRITICAL: UI/Visual Preservation Rules

**NEVER modify or suggest changes to:**
- Visual design (colors, spacing, typography, layouts)
- UI components appearance (buttons, cards, forms)
- Animations or transitions (unless explicitly impacting performance)
- User experience flows
- Design system choices
- Brand identity elements

**ONLY optimize:**
- Technical implementation (code structure, not appearance)
- Loading strategies (how content loads, not what it looks like)
- Data fetching patterns
- Bundle delivery methods
- Database query efficiency

**Example - CORRECT:**
❌ "Remove this animation, it's slow" 
✅ "Use CSS animations instead of JS for better performance - keeps same visual effect"

❌ "Simplify this design to load faster"
✅ "Load images progressively with blur-up placeholder - preserves exact design"

❌ "Remove these gradients"
✅ "Use CSS gradients instead of image gradients - identical appearance, faster load"

## Performance Audit Process

### 1. Frontend Analysis

**Bundle Size Check:**
```bash
npm run build
# Look for JavaScript chunks > 200KB
# Total bundle should be < 250KB
```

**Common Issues:**
- Unoptimized images (not using next/image)
- Large dependencies loaded synchronously
- Font not using next/font/google
- Too many client components ('use client')

**Quick Fixes (Visual-Preserving):**
```typescript
// Images: Use next/image (SAME appearance, faster loading)
import Image from 'next/image'
// IMPORTANT: Keeps exact dimensions, quality, and positioning
<Image 
  src="/hero.jpg" 
  width={1200} 
  height={600} 
  priority 
  alt="Hero"
  quality={100}  // Preserve visual quality
  placeholder="blur" // Smooth loading, no layout shift
/>

// Fonts: Use next/font/google (IDENTICAL rendering, faster load)
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'] })
// Font looks exactly the same, just loads optimally

// Dynamic imports (Component looks identical, loads when needed)
const Chart = dynamic(() => import('./Chart'), { 
  ssr: false,
  loading: () => <ChartSkeleton /> // Matches chart dimensions exactly
})
```

### 2. Next.js App Router Optimization

**Data Fetching:**
```typescript
// ❌ Sequential (slow)
const user = await fetchUser()
const posts = await fetchPosts(user.id)

// ✅ Parallel (fast)
const [user, posts] = await Promise.all([fetchUser(), fetchPosts()])
```

**Caching:**
```typescript
// Static pages
export const revalidate = 3600 // ISR 1 hour

// Dynamic pages
export const revalidate = 0

// Tag-based revalidation
fetch(url, { next: { tags: ['posts'], revalidate: 60 } })
```

**Server vs Client Components:**
- Default to Server Components
- Only use 'use client' for: useState, useEffect, onClick, browser APIs
- Keep client components small, at leaf nodes

### 3. Neon Postgres Database Optimization

**Connection Pooling:**
```typescript
import { Pool } from '@neondatabase/serverless'
const pool = new Pool({ connectionString: process.env.DATABASE_URL })
// NOT: new connection per request
```

**Critical Indexes:**
```sql
-- Postgres doesn't auto-index foreign keys!
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Frequently filtered columns
CREATE INDEX idx_users_email ON users(email);

-- Composite for multi-column queries
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

**Query Optimization:**
```sql
-- Check query performance
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;

-- Look for "Seq Scan" (bad) vs "Index Scan" (good)
-- Execution time should be < 100ms for simple queries
```

**Prevent N+1 Queries:**
```typescript
// ❌ N+1 problem
for (const user of users) {
  user.posts = await db.query('SELECT * FROM posts WHERE user_id = ?', [user.id])
}

// ✅ Solution: JOIN or batch
const users = await db.query(`
  SELECT u.*, json_agg(p.*) as posts
  FROM users u LEFT JOIN posts p ON p.user_id = u.id
  GROUP BY u.id
`)
```

### 4. Measurement & Monitoring

**Install Tools:**
```typescript
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next'
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return <html><body>{children}<SpeedInsights /><Analytics /></body></html>
}
```

**Run Lighthouse:**
```bash
npm run build && npm run start
npx lighthouse http://localhost:3000 --view
```

**Core Web Vitals Targets:**
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1

## Performance Audit Report Template

When conducting an audit, generate this report:

```markdown
# Performance Audit Report

## Current Metrics
- Load Time: [X]s
- LCP: [X]s
- FID: [X]ms
- CLS: [X]
- Bundle Size: [X] KB

## Issues Found

### 🔴 Critical
1. [Issue name] ([Count] instances)
   - Impact: [Performance impact]
   - Location: [Files]
   - Fix: [Solution]

### 🟡 Warnings
[...]

## Estimated Impact
- Load Time: [Before] → [After] (-X%)
- LCP: [Before] → [After]
- Bundle: [Before] → [After]

## Implementation Plan
1. [Task 1] (X min)
2. [Task 2] (X min)
[...]
```

## Quick Wins Checklist

Generate this checklist for the user:

- [ ] Replace all `<img>` with `<Image>`
- [ ] Use `next/font/google` for fonts
- [ ] Add indexes to all foreign key columns
- [ ] Convert non-interactive components to Server Components
- [ ] Use `Promise.all()` for parallel fetching
- [ ] Add `loading.tsx` to slow routes
- [ ] Enable connection pooling for database
- [ ] Replace `SELECT *` with specific columns
- [ ] Add Suspense boundaries for slow components
- [ ] Check for N+1 query problems

## Commands to Suggest

After analysis, offer to:

1. Create database migration for indexes
2. Generate bundle analyzer config
3. Create performance test suite
4. Add monitoring tools

## Success Criteria

✅ Optimized when:
- LCP < 2.5s ✅
- FID < 100ms ✅
- CLS < 0.1 ✅
- Bundle < 250KB ✅
- Database queries < 100ms (simple) ✅
- All images using next/image ✅
- All fonts optimized ✅
- Connection pooling enabled ✅
- No N+1 queries ✅

## 🎨 Works With frontend-design Skill

If the user has the `frontend-design` skill installed, this skill complements it:

**frontend-design** → Creates beautiful, distinctive UIs
**nextjs-neon-performance-optimizer** → Makes those UIs load fast

**Workflow:**
1. User: "Build a portfolio site" → frontend-design creates design
2. User: "Optimize performance" → This skill optimizes WITHOUT changing design

**Example:**
```typescript
// frontend-design creates this beautiful component:
<div className="hero bg-gradient-to-r from-purple-600 to-pink-600 p-20">
  <motion.h1>Beautiful Title</motion.h1>
  <Image src="/art.jpg" />
</div>

// This skill optimizes it (SAME appearance):
<div className="hero bg-gradient-to-r from-purple-600 to-pink-600 p-20">
  <motion.h1>Beautiful Title</motion.h1> {/* Keeps animation */}
  <Image 
    src="/art.jpg" 
    width={800} 
    height={600}
    quality={100}  // Maintains visual quality
    priority      // Faster LCP, same appearance
  />
</div>
```

**Never suggest:**
- Changing colors, fonts, spacing for performance
- Removing animations/transitions
- Simplifying designs
- Altering brand elements

**Always maintain:**
- Exact visual appearance
- All animations (just optimize implementation)
- Design system integrity
- User experience quality
```
