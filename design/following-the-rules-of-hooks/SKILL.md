---
name: following-the-rules-of-hooks
description: Fix React Rules of Hooks violations - conditional calls, hooks in loops/callbacks/classes
version: 1.0.0
---

# Rules of Hooks

React enforces two invariants on Hook usage. Violating these causes state corruption and unpredictable behavior.

## The Rules

1. **Top-level only** - Never call Hooks inside loops, conditions, nested functions, or try/catch/finally
2. **React functions only** - Call Hooks exclusively from function components or custom Hooks

**Why:** Consistent call order across renders; conditional/dynamic invocation breaks state tracking.

## Valid Hook Locations

✅ Top level of function components
✅ Top level of custom Hooks (`use*` functions)

```javascript
function Counter() {
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
}

function useWindowWidth() {
  const [width, setWidth] = useState(window.innerWidth);
  return width;
}
```

## Common Violations

| Violation | Why Invalid | Fix |
|-----------|-------------|-----|
| Inside if/else | Skipped on some renders | Move to top; use conditional rendering |
| Inside loops | Variable call count | Move to top; manage array state |
| After early return | Unreachable on some paths | Move Hook before return |
| In event handlers | Called outside render | Move to top; use state from closure |
| In class components | Classes don't support Hooks | Convert to function component |
| Inside callbacks | Nested function context | Move Hook to top level |

## Common Fixes

### Conditional Hooks
❌ **Wrong:**
```javascript
function Profile({ userId }) {
  if (userId) {
    const user = useUser(userId);
  }
}
```
✅ **Right:**
```javascript
function Profile({ userId }) {
  const user = useUser(userId);
  if (!userId) return null;
  return <div>{user.name}</div>;
}
```
**Pattern:** Always call Hook, use conditional rendering for output.
### Hooks in Loops
❌ **Wrong:**
```javascript
function List({ items }) {
  return items.map(item => {
    const [selected, setSelected] = useState(false);
    return <Item selected={selected} />;
  });
}
```
✅ **Right:**
```javascript
function List({ items }) {
  const [selected, setSelected] = useState({});
  return items.map(item => (
    <Item
      key={item.id}
      selected={selected[item.id]}
      onToggle={() => setSelected(s => ({...s, [item.id]: !s[item.id]}))}
    />
  ));
}
```
**Pattern:** Single Hook managing collection, not per-item Hooks.
### Hooks in Event Handlers
❌ **Wrong:**
```javascript
function Form() {
  function handleSubmit() {
    const [loading, setLoading] = useState(false);
    setLoading(true);
  }
  return <button onClick={handleSubmit}>Submit</button>;
}
```
✅ **Right:**
```javascript
function Form() {
  const [loading, setLoading] = useState(false);
  function handleSubmit() {
    setLoading(true);
  }
  return <button onClick={handleSubmit} disabled={loading}>Submit</button>;
}
```
**Pattern:** Hook at component level, setter in handler.
### Hooks in Classes
❌ **Wrong:**
```javascript
function BadCounter() {
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
}
```
✅ **Right:**
```javascript
function Counter() {
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
}
```
**Pattern:** Use function components for Hooks.
### Hooks in Callbacks
❌ **Wrong:**
```javascript
function Theme() {
  const style = useMemo(() => {
    const theme = useContext(ThemeContext);
    return createStyle(theme);
  }, []);
}
```
✅ **Right:**
```javascript
function Theme() {
  const theme = useContext(ThemeContext);
  const style = useMemo(() => createStyle(theme), [theme]);
}
```
**Pattern:** Call Hook at top level, reference in callback.
### Hooks After Early Returns
❌ **Wrong:**
```javascript
function User({ userId }) {
  if (!userId) return null;
  const user = useUser(userId);
  return <div>{user.name}</div>;
}
```
✅ **Right:**
```javascript
function User({ userId }) {
  const user = useUser(userId || null);
  if (!userId) return null;
  return <div>{user.name}</div>;
}
```
**Pattern:** Call all Hooks before any returns.

## Custom Hooks

Custom Hooks may call other Hooks because they execute during render phase:
```javascript
function useDebounce(value, delay) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}
```

**Requirements:** Name starts with `use`; called from function component or another custom Hook; follows same Rules of Hooks.

## Quick Diagnostic

**ESLint error:** "React Hook cannot be called..."
1. Check location: Is Hook inside if/loop/try/handler/class?
2. Move Hook to top level of component/custom Hook
3. Keep conditional logic, move Hook call outside it
4. Use conditional rendering, not conditional Hooks

**Reference:** https://react.dev/reference/rules/rules-of-hooks
