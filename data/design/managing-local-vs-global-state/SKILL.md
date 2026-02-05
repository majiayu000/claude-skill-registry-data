---
name: managing-local-vs-global-state
description: Teaches when to use local state vs global state (Context) in React 19. Use when deciding state management strategy, avoiding prop drilling, or architecting component state.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Local vs Global State

## Decision Flow

**Use Local State (useState) when:**
- State only needed in one component
- State only needed by component + direct children
- State changes frequently (avoid Context re-renders)
- State is UI-specific (form input, toggle, etc.)

**Use Lifted State when:**
- Two sibling components need to share state
- Parent coordinates between children
- Still contained to component subtree

**Use Context when:**
- Many components at different nesting levels need state
- Prop drilling through 3+ levels
- Global configuration (theme, locale, auth)
- State changes infrequently

## Examples

**Local State:**
```javascript
function Counter() {
  const [count, setCount] = useState(0);

  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```

**Lifted State:**
```javascript
function Parent() {
  const [filter, setFilter] = useState('all');

  return (
    <>
      <FilterButtons filter={filter} setFilter={setFilter} />
      <ItemList filter={filter} />
    </>
  );
}
```

**Context (React 19 with `use()`):**
```javascript
import { createContext, use } from 'react';

const ThemeContext = createContext('light');

function App() {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext value={{ theme, setTheme }}>
      <Layout />
    </ThemeContext>
  );
}

function DeepComponent() {
  const { theme, setTheme } = use(ThemeContext);

  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
    Toggle Theme
  </button>;
}
```

## Anti-Patterns

❌ **Context for frequently changing state:**
```javascript
const MousePositionContext = createContext();

function App() {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);

  return (
    <MousePositionContext value={position}>
      <App />
    </MousePositionContext>
  );
}
```

This causes re-render of entire tree on every mouse move!

✅ **Local state or ref instead:**
```javascript
function Component() {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e) => setPosition({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);

  return <div>Mouse: {position.x}, {position.y}</div>;
}
```

For comprehensive state management patterns, see: `research/react-19-comprehensive.md` lines 1293-1342.
