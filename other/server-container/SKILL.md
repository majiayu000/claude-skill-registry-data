---
name: server-container
description: Container/presentational component split — "smart" containers connect to the store, fetch data, and orchestrate loading/error/empty states; "dumb" children just render props. Use when extracting data logic from views, introducing custom hooks, or reviewing `*Container` components.
when_to_use: Splitting a component into container + presentational pair; connecting a view to Redux/NgRx/Pinia; extracting reusable data logic into a custom hook; reviewing whether a presentational component accidentally imports store code.
paths:
  - "**/containers/**/*.{jsx,tsx,vue}"
  - "**/*Container*.{jsx,tsx,vue}"
---

# Container

## What is a Container Component?

Containers are "smart" components that handle data fetching, state management, and business logic. They wrap "dumb" presentational components, connecting them to data sources (Redux, APIs).

## Key Principles

1. **Smart vs Dumb Separation**: Containers know about Redux, API calls, business logic. Presentational components only know about props and rendering.

2. **Data Orchestration**: Containers fetch data, manage loading/error states, transform data, and pass to presentational components.

3. **Reusability Through Separation**: Presentational components become reusable across different data sources; containers can swap presentational components.

## Best Practices

✅ **DO**:
- Connect to Redux store in containers
- Handle loading, error, empty states
- Transform API data to component props
- Keep containers focused on one feature
- Use custom hooks to extract container logic

❌ **DON'T**:
- Put data fetching in presentational components
- Mix styling concerns in containers
- Create containers that are too large (split them)
- Duplicate logic across similar containers (extract hooks)

## Code Patterns

### Container/Presentational Pattern

```jsx
// TodoListContainer.jsx - SMART (Container)
import { useSelector, useDispatch } from 'react-redux';
import { fetchTodos, toggleTodo } from '../state/todoSlice';
import TodoList from '../components/TodoList';  // DUMB

const TodoListContainer = () => {
  const dispatch = useDispatch();
  const { todos, loading, error } = useSelector(state => state.todos);
  
  useEffect(() => {
    dispatch(fetchTodos());
  }, [dispatch]);
  
  const handleToggle = (id) => dispatch(toggleTodo(id));
  
  return (
    <TodoList
      todos={todos}
      loading={loading}
      error={error}
      onToggle={handleToggle}
    />
  );
};

// TodoList.jsx - DUMB (Presentational)
const TodoList = ({ todos, loading, error, onToggle }) => {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!todos.length) return <EmptyState />;
  
  return (
    <ul>
      {todos.map(todo => (
        <TodoItem 
          key={todo.id} 
          todo={todo} 
          onToggle={() => onToggle(todo.id)} 
        />
      ))}
    </ul>
  );
};
```

### Modern Hook-Based Pattern

```jsx
// Custom hook extracts container logic
function useTodos() {
  const dispatch = useDispatch();
  const { todos, loading, error } = useSelector(state => state.todos);
  
  useEffect(() => {
    dispatch(fetchTodos());
  }, [dispatch]);
  
  const toggleTodo = (id) => dispatch(toggleTodoAction(id));
  
  return { todos, loading, error, toggleTodo };
}

// Container becomes thin wrapper
const TodoListContainer = () => {
  const { todos, loading, error, toggleTodo } = useTodos();
  
  return (
    <TodoList
      todos={todos}
      loading={loading}
      error={error}
      onToggle={toggleTodo}
    />
  );
};
```

### Testing Benefits

```jsx
// Presentational component easy to test
test('TodoList renders items', () => {
  const mockTodos = [{ id: 1, text: 'Test', completed: false }];
  
  render(<TodoList todos={mockTodos} onToggle={jest.fn()} />);
  
  expect(screen.getByText('Test')).toBeInTheDocument();
});

// No Redux mocking needed for presentational!
```

## Related Terminologies

- **Organism** (UI) - Organisms often become containers
- **Store** (State) - Containers connect to store
- **Component** (UI) - Presentational components
- **Selectors** (State) - Containers use selectors

## Quality Gates

- [ ] Data logic in container, rendering in presentational
- [ ] Loading/error/empty states handled
- [ ] Presentational components have no store connection
- [ ] Logic extracted to custom hooks when reusable
- [ ] Clear naming convention (*Container suffix)

**Source**: `/docs/server/container.md`
