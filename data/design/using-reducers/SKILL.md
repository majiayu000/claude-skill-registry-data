---
name: using-reducers
description: Teaches useReducer for complex state logic in React 19. Use when state updates depend on previous state, multiple related state values, or complex update logic.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# useReducer Patterns

## When to Use useReducer

**Use `useReducer` when:**
- Multiple related state values
- Complex state update logic
- Next state depends on previous state
- State transitions follow patterns

**Use `useState` when:**
- Simple independent values
- Basic toggle or counter logic
- No complex interdependencies

## Basic Pattern

```javascript
import { useReducer } from 'react';

const initialState = { count: 0, step: 1 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'decrement':
      return { ...state, count: state.count - state.step };
    case 'setStep':
      return { ...state, step: action.payload };
    case 'reset':
      return initialState;
    default:
      throw new Error(`Unknown action: ${action.type}`);
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <>
      <p>Count: {state.count}</p>
      <p>Step: {state.step}</p>

      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>

      <input
        type="number"
        value={state.step}
        onChange={(e) => dispatch({ type: 'setStep', payload: +e.target.value })}
      />

      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </>
  );
}
```

## Complex Example: Todo List

```javascript
const initialState = {
  todos: [],
  filter: 'all',
};

function todosReducer(state, action) {
  switch (action.type) {
    case 'added':
      return {
        ...state,
        todos: [...state.todos, { id: Date.now(), text: action.text, done: false }],
      };
    case 'toggled':
      return {
        ...state,
        todos: state.todos.map(t =>
          t.id === action.id ? { ...t, done: !t.done } : t
        ),
      };
    case 'deleted':
      return {
        ...state,
        todos: state.todos.filter(t => t.id !== action.id),
      };
    case 'filterChanged':
      return {
        ...state,
        filter: action.filter,
      };
    default:
      throw new Error(`Unknown action: ${action.type}`);
  }
}
```

For comprehensive useReducer patterns, see: `research/react-19-comprehensive.md` lines 506-521.
