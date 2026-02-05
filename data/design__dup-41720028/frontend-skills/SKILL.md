---
name: frontend-skills
description: Master HTML5, CSS3, JavaScript ES6+, React, Vue, Angular, and modern web development. Learn responsive design, accessibility, and web performance optimization.
sasmp_version: "1.3.0"
skill_type: atomic
version: "2.0.0"

parameters:
  framework:
    type: string
    enum: [react, vue, angular, vanilla]
    default: react
  typescript:
    type: boolean
    default: true

validation_rules:
  - pattern: "^[a-z][a-zA-Z0-9]*$"
    target: component_names
    message: Component names must be PascalCase
  - pattern: "^use[A-Z]"
    target: hook_names
    message: Custom hooks must start with 'use'

retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 1000

logging:
  on_entry: "Starting frontend task: {task}"
  on_success: "Completed: {task}"
  on_error: "Failed: {task} - {error}"

dependencies:
  agents:
    - frontend-ui-developer
---

# Frontend Development Skills

## HTML5 Fundamentals

```html
<!-- Semantic markup -->
<header><nav></nav></header>
<main>
  <article><h1>Title</h1><p>Content</p></article>
</main>
<footer></footer>

<!-- Accessibility -->
<img alt="descriptive text" src="image.jpg">
<button aria-label="Close">×</button>
<label for="email">Email:</label>
<input id="email" type="email">
```

## CSS3 Modern Layouts

```css
/* Flexbox */
.flex-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; }
}
```

## JavaScript ES6+ Essentials

```javascript
// Arrow functions
const add = (a, b) => a + b;

// Destructuring
const {name, age} = user;
const [first, ...rest] = array;

// Async/await with error handling
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}

// Array methods
arr.map(x => x * 2)
   .filter(x => x > 5)
   .reduce((acc, x) => acc + x, 0);
```

## React Hooks Pattern

```jsx
import {useState, useEffect, useCallback} from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  const increment = useCallback(() => {
    setCount(prev => prev + 1);
  }, []);

  if (error) return <ErrorBoundary error={error} />;

  return (
    <button onClick={increment}>
      Count: {count}
    </button>
  );
}
```

## State Management

```javascript
// Context API with TypeScript
interface UserContextType {
  user: User | null;
  setUser: (user: User) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be within UserProvider');
  }
  return context;
}
```

## Performance Optimization

```javascript
// Code splitting
const LazyComponent = lazy(() => import('./Component'));

// Memoization
const MemoizedComponent = memo(Component);
const value = useMemo(() => expensiveComputation(), [deps]);

// useCallback for stable references
const handleClick = useCallback(() => {
  // handler
}, [dependencies]);
```

## Web Performance Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| LCP | < 2.5s | Largest Contentful Paint |
| FID | < 100ms | First Input Delay |
| CLS | < 0.1 | Cumulative Layout Shift |
| TTI | < 5s | Time to Interactive |
| FCP | < 1.8s | First Contentful Paint |

## Accessibility Standards

- **WCAG 2.1 Level AA** compliance
- **Keyboard navigation** support
- **Screen reader** compatibility
- **Color contrast** ratios (4.5:1 minimum)
- **Semantic HTML** structure

## Unit Test Template

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Counter Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('increments count on click', async () => {
    render(<Counter />);

    const button = screen.getByRole('button');
    await userEvent.click(button);

    expect(screen.getByText(/Count: 1/)).toBeInTheDocument();
  });

  test('handles error state', async () => {
    jest.spyOn(console, 'error').mockImplementation(() => {});

    render(<Counter initialError={new Error('Test')} />);

    expect(screen.getByRole('alert')).toBeInTheDocument();
  });
});
```

## Troubleshooting Guide

| Symptom | Cause | Solution |
|---------|-------|----------|
| Component not updating | Stale closure | Use functional setState |
| Infinite re-render | useEffect missing deps | Add all dependencies |
| Memory leak warning | Unmounted state update | Use cleanup function |
| Hydration mismatch | Server/client diff | Use useEffect for client-only |

## Key Concepts Checklist

- [ ] Semantic HTML elements
- [ ] CSS Flexbox and Grid layouts
- [ ] JavaScript async/await patterns
- [ ] React hooks (useState, useEffect, useContext)
- [ ] Component composition
- [ ] Props and state management
- [ ] Event handling
- [ ] Conditional rendering
- [ ] List rendering with keys
- [ ] Form handling
- [ ] API integration
- [ ] Error boundaries
- [ ] Performance optimization
- [ ] Accessibility compliance
- [ ] Responsive design

---

**Source**: https://roadmap.sh
**Version**: 2.0.0
**Last Updated**: 2025-01-01
