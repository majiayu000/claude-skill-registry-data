---
name: perf-analyzer
description: |
  WHEN: Performance analysis, bundle size optimization, rendering, Core Web Vitals, code splitting
  WHAT: Bundle analysis + large dependency detection + re-render issues + useMemo/useCallback suggestions + LCP/FID/CLS improvements
  WHEN NOT: Code quality → code-reviewer, Security → security-scanner
---

# Performance Analyzer Skill

## Purpose
Analyzes frontend application performance and suggests optimizations for bundle size, rendering, and images.

## When to Use
- Performance analysis requests
- "Slow", "long loading" mentions
- Bundle size, rendering, Core Web Vitals questions
- Pre-production performance review

## Workflow

### Step 1: Select Analysis Areas
**AskUserQuestion:**
```
"Which areas to analyze?"
Options:
- Full performance analysis (recommended)
- Bundle size analysis
- Rendering performance (re-renders)
- Image/asset optimization
- Code splitting opportunities
multiSelect: true
```

## Analysis Areas

### Bundle Size
| Item | Threshold | Severity |
|------|-----------|----------|
| Total bundle | > 500KB | HIGH |
| Initial JS | > 200KB | HIGH |
| Single chunk | > 100KB | MEDIUM |
| Unused code | Tree-shaking failures | MEDIUM |

**Large Dependencies:**
```typescript
// WARNING: Large libraries
import _ from 'lodash'         // 71KB
import moment from 'moment'    // 280KB

// BETTER: Lightweight alternatives
import debounce from 'lodash/debounce'  // 2KB
import { format } from 'date-fns'        // Only needed functions
```

**Tree-shaking Issues:**
```typescript
// BAD: Full import (no tree-shaking)
import * as utils from './utils'

// GOOD: Named import
import { specificFunction } from './utils'
```

### Rendering Performance

**Unnecessary Re-renders:**
```typescript
// WARNING: New object/array every render
function Component() {
  return <Child style={{ color: 'red' }} />  // New object each time
}

// BETTER: External definition
const style = { color: 'red' }
function Component() {
  return <Child style={style} />
}
```

**Expensive Computations:**
```typescript
// WARNING: Computed every render
function Component({ data }) {
  const processed = data.map(item => expensiveOp(item))
  return <List items={processed} />
}

// BETTER: useMemo caching
const processed = useMemo(
  () => data.map(item => expensiveOp(item)),
  [data]
)
```

**Callback Optimization:**
```typescript
// WARNING: New function every render
<Child onClick={() => handleClick()} />

// BETTER: useCallback
const handleClick = useCallback(() => { /* ... */ }, [])
<Child onClick={handleClick} />
```

### Image Optimization
| Issue | Problem | Solution |
|-------|---------|----------|
| Large image | > 200KB | Compress or WebP |
| Unoptimized format | PNG/JPG | WebP/AVIF |
| Missing lazy load | Offscreen images | loading="lazy" |
| Fixed size | Non-responsive | srcset/sizes |

```typescript
// BAD: No optimization
<img src="/hero.jpg" alt="Hero" />

// GOOD: next/image
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // LCP image
  placeholder="blur"
/>
```

### Code Splitting
```typescript
// WARNING: Unnecessary initial load
import HeavyComponent from './HeavyComponent'

// BETTER: Load on demand
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Skeleton />
})
```

### Core Web Vitals

**LCP (Largest Contentful Paint)**
| Grade | Time | Improvements |
|-------|------|--------------|
| Good | < 2.5s | - |
| Needs Work | 2.5-4s | Image optimization, server response |
| Poor | > 4s | CDN, caching, code splitting |

**FID (First Input Delay)**
| Grade | Time | Improvements |
|-------|------|--------------|
| Good | < 100ms | - |
| Needs Work | 100-300ms | Reduce main thread blocking |
| Poor | > 300ms | Split long tasks, Web Workers |

**CLS (Cumulative Layout Shift)**
| Grade | Score | Improvements |
|-------|-------|--------------|
| Good | < 0.1 | - |
| Needs Work | 0.1-0.25 | Specify image/font dimensions |
| Poor | > 0.25 | Reserve space for dynamic content |

## Response Template
```
## Performance Analysis Results

**Project**: [name]

### Bundle Size
| Item | Size | Status |
|------|------|--------|
| Total bundle | 650KB | WARNING |
| Initial JS | 180KB | OK |

**Large Dependencies:**
| Package | Size | Alternative |
|---------|------|-------------|
| moment | 280KB | date-fns (7KB) |
| lodash | 71KB | lodash-es + individual imports |

### Rendering Performance
| Component | Issue | Recommendation |
|-----------|-------|----------------|
| ProductList | Unnecessary re-renders | Add useMemo |

### Image Optimization
| Image | Size | Recommendation |
|-------|------|----------------|
| hero.jpg | 450KB | Convert to WebP, use next/image |

### Code Splitting Opportunities
| Component | Size | Recommendation |
|-----------|------|----------------|
| Dashboard | 85KB | dynamic import |

### Priority Actions
1. [ ] moment → date-fns migration (-273KB)
2. [ ] Add useMemo to ProductList
3. [ ] Convert hero.jpg to WebP
4. [ ] Dynamic import Dashboard

### Expected Improvements
- Initial bundle: 650KB → ~350KB (-46%)
- LCP: Expected improvement
- TTI: Expected improvement
```

## Best Practices
1. **Measure First**: Always measure before optimizing
2. **Incremental**: Apply one change at a time
3. **Trade-offs**: Avoid over-optimization
4. **Real Device Testing**: Test on low-end devices
5. **Continuous Monitoring**: Prevent performance regression

## Integration
- `code-reviewer` skill
- `nextjs-reviewer` skill
- `/analyze-code` command

## Notes
- Static analysis based, runtime performance may differ
- Use with Lighthouse for actual measurements
- Analyze production builds
