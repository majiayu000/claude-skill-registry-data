---
name: state-middleware
description: Redux middleware — the `store => next => action => {}` pipeline for side effects, logging, analytics, and async (thunk/saga). Use when writing custom middleware, wiring async thunks, ordering middleware in configureStore, or keeping side effects out of reducers.
when_to_use: Adding logger/analytics/crash-reporting middleware; writing a custom thunk-style middleware; ordering middleware in configureStore (logger last); moving side effects out of reducers.
paths:
  - "**/store/**/*.{js,ts}"
  - "**/middleware/**/*.{js,ts}"
  - "**/*Middleware*.{js,ts}"
---

# Middleware

## What is Middleware?

Middleware is Redux's "plugin system"—functions that intercept every action between dispatch and reducer. This is where async operations (API calls), logging, crash reporting, and side effects live, keeping reducers pure.

## Key Principles

1. **Action Pipeline**: Every action flows through middleware chain before reaching reducer. Each middleware can observe, modify, delay, or cancel actions.

2. **Side Effect Container**: Reducers must be pure. Middleware is where impure operations (API calls, localStorage, analytics) belong.

3. **Higher-Order Functions**: Middleware signature is `store => next => action => {}`. Call `next(action)` to pass to next middleware or reducer.

## Best Practices

✅ **DO**:
- Use redux-thunk or RTK for async actions
- Keep middleware focused (single responsibility)
- Call `next(action)` to continue the chain
- Use middleware for cross-cutting concerns
- Order middleware intentionally (logger last)

❌ **DON'T**:
- Put side effects in reducers
- Create overly complex middleware
- Forget to call `next(action)` (blocks action flow)
- Use middleware for business logic that belongs in reducers
- Mutate actions (create new ones instead)

## Code Patterns

### Custom Logger Middleware

```javascript
// loggerMiddleware.js
const loggerMiddleware = (store) => (next) => (action) => {
  console.group(action.type);
  console.log('Dispatching:', action);
  console.log('Previous State:', store.getState());
  
  const result = next(action);  // Pass to next middleware/reducer
  
  console.log('Next State:', store.getState());
  console.groupEnd();
  
  return result;
};

export default loggerMiddleware;
```

### Thunk Middleware Pattern

```javascript
// thunkMiddleware.js
const thunkMiddleware = (store) => (next) => (action) => {
  // If action is a function, call it with dispatch/getState
  if (typeof action === 'function') {
    return action(store.dispatch, store.getState);
  }
  
  // Otherwise, pass through
  return next(action);
};

// Usage: async action creator
const fetchUsers = () => async (dispatch, getState) => {
  dispatch({ type: 'users/fetchStart' });
  
  try {
    const users = await api.getUsers();
    dispatch({ type: 'users/fetchSuccess', payload: users });
  } catch (error) {
    dispatch({ type: 'users/fetchError', payload: error.message });
  }
};
```

### RTK createAsyncThunk

```javascript
import { createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUsers = createAsyncThunk(
  'users/fetch',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.getUsers();
      return response.data;  // Becomes action.payload
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Slice handles pending/fulfilled/rejected automatically
extraReducers: (builder) => {
  builder
    .addCase(fetchUsers.pending, (state) => {
      state.loading = true;
    })
    .addCase(fetchUsers.fulfilled, (state, action) => {
      state.loading = false;
      state.items = action.payload;
    })
    .addCase(fetchUsers.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload;
    });
}
```

### Analytics Middleware

```javascript
const analyticsMiddleware = (store) => (next) => (action) => {
  // Track specific actions
  if (action.type === 'cart/checkout') {
    analytics.track('Checkout Started', {
      itemCount: store.getState().cart.items.length
    });
  }
  
  return next(action);
};
```

### Applying Middleware

```javascript
// store/index.js
import { configureStore } from '@reduxjs/toolkit';
import loggerMiddleware from './loggerMiddleware';
import analyticsMiddleware from './analyticsMiddleware';

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()  // Includes thunk by default
      .concat(analyticsMiddleware)
      .concat(loggerMiddleware)  // Logger last to see final state
});
```

## Middleware Order

```
dispatch(action)
    ↓
[thunk] → handles functions
    ↓
[analytics] → tracks events
    ↓
[logger] → logs action/state
    ↓
reducer → updates state
```

## Related Terminologies

- **Actions** (State) - Flow through middleware
- **Store** (State) - Applies middleware
- **Reducer** (State) - Receives actions after middleware
- **Ajax** (State) - API calls in middleware

## Quality Gates

- [ ] Side effects in middleware, not reducers
- [ ] Middleware calls `next(action)`
- [ ] Order is intentional (logger last)
- [ ] Async thunks handle loading/error
- [ ] Cross-cutting concerns centralized
- [ ] RTK defaults preserved when extending

**Source**: `/docs/state/middleware.md`
