---
name: state-crud
description: CRUD patterns for state slices — consistent `domain/create|read|update|delete` action naming, request/success/failure triples per operation, and normalised `{ byId, allIds }` entity shapes for O(1) lookups. Use when designing a new entity slice, standardising action-type names, or refactoring array-shaped state.
when_to_use: Designing a new entity slice (todos, users, products); standardising request/success/failure naming across async operations; normalising state from arrays to byId/allIds; wiring RTK createAsyncThunks for all four CRUD ops.
paths:
  - "**/store/**/*.{js,ts}"
  - "**/slices/**/*.{js,ts}"
  - "**/*Actions*.{js,ts}"
---

# CRUD

## What is CRUD?

CRUD (Create, Read, Update, Delete) are the four basic operations for persistent data. In state management, CRUD patterns standardize action naming and reducer logic for consistent data manipulation across your application.

## Key Principles

1. **Consistent Naming**: Use `domain/operation` pattern—`todos/create`, `todos/read`, `todos/update`, `todos/delete`. Consistency aids debugging.

2. **Request/Success/Failure**: Each CRUD operation needs three action types for async handling: `todos/createRequest`, `todos/createSuccess`, `todos/createFailure`.

3. **Normalized State**: Store entities by ID for efficient CRUD. `{ byId: { '1': {...} }, allIds: ['1'] }` enables O(1) lookups.

## Best Practices

✅ **DO**:
- Follow `domain/operationName` convention
- Define action types as constants
- Use request/success/failure for async
- Normalize state for entities
- Handle optimistic updates thoughtfully

❌ **DON'T**:
- Use generic names (`UPDATE`, `SET_DATA`)
- Mix naming conventions
- Forget error handling in CRUD operations
- Store data in arrays when objects are better
- Skip loading/error states

## Code Patterns

### Action Naming Convention

```javascript
// Constants prevent typos
const TODO_ACTIONS = {
  CREATE_REQUEST: 'todos/createRequest',
  CREATE_SUCCESS: 'todos/createSuccess',
  CREATE_FAILURE: 'todos/createFailure',
  
  READ_REQUEST: 'todos/readRequest',
  READ_SUCCESS: 'todos/readSuccess',
  READ_FAILURE: 'todos/readFailure',
  
  UPDATE_REQUEST: 'todos/updateRequest',
  UPDATE_SUCCESS: 'todos/updateSuccess',
  UPDATE_FAILURE: 'todos/updateFailure',
  
  DELETE_REQUEST: 'todos/deleteRequest',
  DELETE_SUCCESS: 'todos/deleteSuccess',
  DELETE_FAILURE: 'todos/deleteFailure',
};
```

### RTK CRUD Slice

```javascript
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunks for CRUD
export const createTodo = createAsyncThunk(
  'todos/create',
  async (todoData) => await api.createTodo(todoData)
);

export const fetchTodos = createAsyncThunk(
  'todos/read',
  async () => await api.getTodos()
);

export const updateTodo = createAsyncThunk(
  'todos/update',
  async ({ id, changes }) => await api.updateTodo(id, changes)
);

export const deleteTodo = createAsyncThunk(
  'todos/delete',
  async (id) => { await api.deleteTodo(id); return id; }
);

const todosSlice = createSlice({
  name: 'todos',
  initialState: {
    byId: {},
    allIds: [],
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // CREATE
      .addCase(createTodo.fulfilled, (state, action) => {
        const todo = action.payload;
        state.byId[todo.id] = todo;
        state.allIds.push(todo.id);
      })
      // READ
      .addCase(fetchTodos.fulfilled, (state, action) => {
        action.payload.forEach(todo => {
          state.byId[todo.id] = todo;
          if (!state.allIds.includes(todo.id)) {
            state.allIds.push(todo.id);
          }
        });
      })
      // UPDATE
      .addCase(updateTodo.fulfilled, (state, action) => {
        const { id, ...changes } = action.payload;
        state.byId[id] = { ...state.byId[id], ...changes };
      })
      // DELETE
      .addCase(deleteTodo.fulfilled, (state, action) => {
        const id = action.payload;
        delete state.byId[id];
        state.allIds = state.allIds.filter(i => i !== id);
      });
  }
});
```

### Component Usage

```jsx
function TodoManager() {
  const dispatch = useDispatch();
  
  useEffect(() => {
    dispatch(fetchTodos());  // READ
  }, [dispatch]);
  
  const handleCreate = (text) => {
    dispatch(createTodo({ text, completed: false }));
  };
  
  const handleUpdate = (id, changes) => {
    dispatch(updateTodo({ id, changes }));
  };
  
  const handleDelete = (id) => {
    dispatch(deleteTodo(id));
  };
  
  return (
    <TodoList
      onAdd={handleCreate}
      onEdit={handleUpdate}
      onDelete={handleDelete}
    />
  );
}
```

### Normalized State Shape

```javascript
// Good: Normalized
{
  todos: {
    byId: {
      '1': { id: '1', text: 'Learn Redux', completed: false },
      '2': { id: '2', text: 'Build app', completed: true }
    },
    allIds: ['1', '2']
  }
}

// Bad: Array (slow lookups)
{
  todos: [
    { id: '1', text: 'Learn Redux', completed: false },
    { id: '2', text: 'Build app', completed: true }
  ]
}
```

## Related Terminologies

- **Actions** (State) - CRUD actions trigger state changes
- **Reducer** (State) - Handles CRUD action cases
- **Ajax** (State) - CRUD typically involves API calls
- **Operations** (State) - Async CRUD handling

## Quality Gates

- [ ] Consistent naming convention
- [ ] Request/success/failure for async
- [ ] Normalized state for entities
- [ ] Loading/error states handled
- [ ] Optimistic updates considered
- [ ] Action type constants used

**Source**: `/docs/state/crud.md`
