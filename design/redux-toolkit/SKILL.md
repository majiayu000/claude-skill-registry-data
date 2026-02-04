---
name: redux-toolkit
description: Manages global state with Redux Toolkit's createSlice, createAsyncThunk, and RTK Query for data fetching and caching. Use when building large-scale applications, implementing predictable state management, or when user mentions Redux, RTK, or Redux Toolkit.
---

# Redux Toolkit

Official, opinionated, batteries-included toolset for efficient Redux development.

## Quick Start

```bash
# Install
npm install @reduxjs/toolkit react-redux

# With TypeScript types (included in RTK)
npm install @reduxjs/toolkit react-redux
```

## Store Setup

### Basic Store

```typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './slices/counterSlice';
import userReducer from './slices/userSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    user: userReducer,
  },
});

// Infer types from store
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Typed Hooks

```typescript
// store/hooks.ts
import { useDispatch, useSelector, TypedUseSelectorHook } from 'react-redux';
import type { RootState, AppDispatch } from './index';

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

### Provider Setup

```tsx
// main.tsx or app.tsx
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  return (
    <Provider store={store}>
      <YourApp />
    </Provider>
  );
}
```

## createSlice

### Basic Slice

```typescript
// store/slices/counterSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
  status: 'idle' | 'loading' | 'failed';
}

const initialState: CounterState = {
  value: 0,
  status: 'idle',
};

const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
    reset: () => initialState,
  },
});

export const { increment, decrement, incrementByAmount, reset } = counterSlice.actions;
export default counterSlice.reducer;
```

### Slice with Prepare Callback

```typescript
const todosSlice = createSlice({
  name: 'todos',
  initialState: [] as Todo[],
  reducers: {
    addTodo: {
      reducer: (state, action: PayloadAction<Todo>) => {
        state.push(action.payload);
      },
      prepare: (text: string) => ({
        payload: {
          id: nanoid(),
          text,
          completed: false,
          createdAt: new Date().toISOString(),
        },
      }),
    },
    toggleTodo: (state, action: PayloadAction<string>) => {
      const todo = state.find(t => t.id === action.payload);
      if (todo) {
        todo.completed = !todo.completed;
      }
    },
  },
});
```

### Using Selectors

```typescript
// Inline selectors
export const selectCount = (state: RootState) => state.counter.value;
export const selectStatus = (state: RootState) => state.counter.status;

// Memoized selectors with createSelector
import { createSelector } from '@reduxjs/toolkit';

export const selectTodos = (state: RootState) => state.todos.items;
export const selectFilter = (state: RootState) => state.todos.filter;

export const selectFilteredTodos = createSelector(
  [selectTodos, selectFilter],
  (todos, filter) => {
    switch (filter) {
      case 'active':
        return todos.filter(t => !t.completed);
      case 'completed':
        return todos.filter(t => t.completed);
      default:
        return todos;
    }
  }
);

// In component
import { useAppSelector } from '../store/hooks';

function TodoList() {
  const todos = useAppSelector(selectFilteredTodos);
  // ...
}
```

## createAsyncThunk

### Basic Async Thunk

```typescript
// store/slices/userSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserState {
  data: User | null;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

// Async thunk
export const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId: string) => {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) throw new Error('Failed to fetch user');
    return response.json() as Promise<User>;
  }
);

const userSlice = createSlice({
  name: 'user',
  initialState: {
    data: null,
    status: 'idle',
    error: null,
  } as UserState,
  reducers: {
    clearUser: (state) => {
      state.data = null;
      state.status = 'idle';
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(fetchUser.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.data = action.payload;
      })
      .addCase(fetchUser.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message ?? 'Unknown error';
      });
  },
});
```

### Async Thunk with ThunkAPI

```typescript
export const updateUser = createAsyncThunk(
  'user/updateUser',
  async (
    userData: Partial<User>,
    { getState, rejectWithValue, dispatch }
  ) => {
    const state = getState() as RootState;
    const userId = state.user.data?.id;

    if (!userId) {
      return rejectWithValue('No user logged in');
    }

    try {
      const response = await fetch(`/api/users/${userId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.message);
      }

      const user = await response.json();

      // Dispatch other actions
      dispatch(showNotification({ message: 'Profile updated!' }));

      return user;
    } catch (error) {
      return rejectWithValue('Network error');
    }
  }
);

// Handle custom error type
extraReducers: (builder) => {
  builder.addCase(updateUser.rejected, (state, action) => {
    state.status = 'failed';
    // action.payload is the rejectWithValue argument
    state.error = action.payload as string;
  });
}
```

### Cancelling Thunks

```typescript
export const fetchUserWithCancel = createAsyncThunk(
  'user/fetchWithCancel',
  async (userId: string, { signal }) => {
    const response = await fetch(`/api/users/${userId}`, { signal });
    return response.json();
  }
);

// In component
function UserProfile({ userId }) {
  const dispatch = useAppDispatch();

  useEffect(() => {
    const promise = dispatch(fetchUserWithCancel(userId));

    return () => {
      promise.abort(); // Cancel on unmount or userId change
    };
  }, [userId, dispatch]);
}
```

## RTK Query

### API Definition

```typescript
// store/api/apiSlice.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface Post {
  id: string;
  title: string;
  content: string;
  authorId: string;
}

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['User', 'Post'],
  endpoints: (builder) => ({
    // Query endpoints
    getUsers: builder.query<User[], void>({
      query: () => '/users',
      providesTags: ['User'],
    }),

    getUser: builder.query<User, string>({
      query: (id) => `/users/${id}`,
      providesTags: (result, error, id) => [{ type: 'User', id }],
    }),

    getPosts: builder.query<Post[], { userId?: string }>({
      query: ({ userId }) => ({
        url: '/posts',
        params: { userId },
      }),
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: 'Post' as const, id })),
              { type: 'Post', id: 'LIST' },
            ]
          : [{ type: 'Post', id: 'LIST' }],
    }),

    // Mutation endpoints
    createUser: builder.mutation<User, Omit<User, 'id'>>({
      query: (body) => ({
        url: '/users',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['User'],
    }),

    updateUser: builder.mutation<User, { id: string; data: Partial<User> }>({
      query: ({ id, data }) => ({
        url: `/users/${id}`,
        method: 'PATCH',
        body: data,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'User', id }],
    }),

    deleteUser: builder.mutation<void, string>({
      query: (id) => ({
        url: `/users/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['User'],
    }),
  }),
});

export const {
  useGetUsersQuery,
  useGetUserQuery,
  useGetPostsQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
} = apiSlice;
```

### Store Setup with RTK Query

```typescript
import { configureStore } from '@reduxjs/toolkit';
import { apiSlice } from './api/apiSlice';

export const store = configureStore({
  reducer: {
    [apiSlice.reducerPath]: apiSlice.reducer,
    // other reducers
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware),
});
```

### Using Queries

```tsx
function UserList() {
  const {
    data: users,
    isLoading,
    isError,
    error,
    refetch,
  } = useGetUsersQuery();

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error: {error.message}</div>;

  return (
    <div>
      <button onClick={refetch}>Refresh</button>
      <ul>
        {users?.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}

// With parameters
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useGetUserQuery(userId, {
    skip: !userId, // Skip if no userId
    pollingInterval: 30000, // Refetch every 30s
    refetchOnMountOrArgChange: true,
  });

  // ...
}
```

### Using Mutations

```tsx
function CreateUserForm() {
  const [createUser, { isLoading, isSuccess, isError }] = useCreateUserMutation();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    try {
      await createUser({
        name: formData.get('name') as string,
        email: formData.get('email') as string,
      }).unwrap();

      // Success!
    } catch (error) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

### Optimistic Updates

```typescript
updatePost: builder.mutation<Post, { id: string; data: Partial<Post> }>({
  query: ({ id, data }) => ({
    url: `/posts/${id}`,
    method: 'PATCH',
    body: data,
  }),
  async onQueryStarted({ id, data }, { dispatch, queryFulfilled }) {
    // Optimistically update the cache
    const patchResult = dispatch(
      apiSlice.util.updateQueryData('getPosts', undefined, (draft) => {
        const post = draft.find((p) => p.id === id);
        if (post) {
          Object.assign(post, data);
        }
      })
    );

    try {
      await queryFulfilled;
    } catch {
      // Revert on error
      patchResult.undo();
    }
  },
}),
```

### Pagination

```typescript
getPaginatedPosts: builder.query<
  { posts: Post[]; total: number },
  { page: number; limit: number }
>({
  query: ({ page, limit }) => `/posts?page=${page}&limit=${limit}`,
  serializeQueryArgs: ({ endpointName }) => endpointName,
  merge: (currentCache, newItems, { arg }) => {
    if (arg.page === 1) {
      return newItems;
    }
    currentCache.posts.push(...newItems.posts);
  },
  forceRefetch: ({ currentArg, previousArg }) => {
    return currentArg !== previousArg;
  },
}),

// In component
function InfinitePostList() {
  const [page, setPage] = useState(1);
  const { data, isFetching } = useGetPaginatedPostsQuery({ page, limit: 10 });

  return (
    <div>
      {data?.posts.map(post => <PostCard key={post.id} post={post} />)}
      <button
        onClick={() => setPage(p => p + 1)}
        disabled={isFetching}
      >
        Load More
      </button>
    </div>
  );
}
```

## Entity Adapter

```typescript
import { createSlice, createEntityAdapter, PayloadAction } from '@reduxjs/toolkit';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

const todosAdapter = createEntityAdapter<Todo>({
  selectId: (todo) => todo.id,
  sortComparer: (a, b) => a.text.localeCompare(b.text),
});

const todosSlice = createSlice({
  name: 'todos',
  initialState: todosAdapter.getInitialState({
    loading: false,
  }),
  reducers: {
    addTodo: todosAdapter.addOne,
    updateTodo: todosAdapter.updateOne,
    removeTodo: todosAdapter.removeOne,
    setAllTodos: todosAdapter.setAll,
    toggleTodo: (state, action: PayloadAction<string>) => {
      const todo = state.entities[action.payload];
      if (todo) {
        todo.completed = !todo.completed;
      }
    },
  },
});

// Selectors
export const {
  selectAll: selectAllTodos,
  selectById: selectTodoById,
  selectIds: selectTodoIds,
} = todosAdapter.getSelectors((state: RootState) => state.todos);
```

## Reference Files

- [rtk-query-advanced.md](references/rtk-query-advanced.md) - Advanced RTK Query patterns
- [middleware.md](references/middleware.md) - Custom middleware and listeners
