---
name: state-ajax
description: Async data-fetching patterns — Fetch vs Axios, service-layer organisation, AbortController cancellation, and integration with Redux Toolkit's createAsyncThunk for pending/fulfilled/rejected state transitions. Use when writing or reviewing HTTP call sites, standardising loading/error handling, or wiring request cancellation in effects.
when_to_use: Choosing between fetch and axios; setting up an apiClient with interceptors; integrating async requests with Redux/NgRx slices; cancelling in-flight requests on unmount via AbortController; handling loading/error/success state uniformly.
paths:
  - "**/api/**/*.{js,ts}"
  - "**/services/**/*.{js,ts}"
  - "**/store/**/*.{js,ts}"
---

# AJAX

## What is AJAX?

AJAX (Asynchronous JavaScript and XML) enables fetching data from servers without page reloads. Modern implementations use Fetch API or Axios instead of XMLHttpRequest, returning JSON instead of XML.

## Key Principles

1. **Asynchronous by Design**: AJAX doesn't block UI. Fire request, continue rendering, update when response arrives.

2. **State Integration**: AJAX results flow into state management. Track loading, success, and error states for each request.

3. **Fetch API or Axios**: Fetch is native (no dependencies). Axios adds interceptors, request cancellation, and better error handling.

## Best Practices

✅ **DO**:
- Use async/await for cleaner code
- Handle loading, success, and error states
- Implement request cancellation (AbortController)
- Use axios interceptors for auth/error handling
- Cache responses appropriately

❌ **DON'T**:
- Forget error handling (network failures happen)
- Ignore loading states (show feedback)
- Leave requests hanging on unmount
- Hardcode API URLs (use environment variables)
- Skip request/response transformation

## Code Patterns

### Fetch API

```javascript
// Basic fetch
async function getUsers() {
  try {
    const response = await fetch('/api/users');
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error;
  }
}
```

### Axios Setup

```javascript
// apiClient.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
});

// Request interceptor
apiClient.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      logout();
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### Service Layer

```javascript
// userService.js
import apiClient from './apiClient';

const UserService = {
  getAll: () => apiClient.get('/users'),
  getById: (id) => apiClient.get(`/users/${id}`),
  create: (data) => apiClient.post('/users', data),
  update: (id, data) => apiClient.put(`/users/${id}`, data),
  delete: (id) => apiClient.delete(`/users/${id}`)
};

export default UserService;
```

### With Redux Thunk

```javascript
import { createAsyncThunk } from '@reduxjs/toolkit';
import UserService from '../services/userService';

export const fetchUsers = createAsyncThunk(
  'users/fetch',
  async (_, { rejectWithValue }) => {
    try {
      return await UserService.getAll();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Slice handles pending/fulfilled/rejected
extraReducers: (builder) => {
  builder
    .addCase(fetchUsers.pending, (state) => {
      state.status = 'loading';
    })
    .addCase(fetchUsers.fulfilled, (state, action) => {
      state.status = 'succeeded';
      state.items = action.payload;
    })
    .addCase(fetchUsers.rejected, (state, action) => {
      state.status = 'failed';
      state.error = action.payload;
    });
}
```

### Request Cancellation

```javascript
// Cancel on unmount
function UserList() {
  useEffect(() => {
    const controller = new AbortController();
    
    fetch('/api/users', { signal: controller.signal })
      .then(r => r.json())
      .then(setUsers)
      .catch(e => {
        if (e.name !== 'AbortError') console.error(e);
      });
    
    return () => controller.abort();
  }, []);
}

// With axios
const source = axios.CancelToken.source();
axios.get('/users', { cancelToken: source.token });
source.cancel('Cancelled');
```

## API Comparison

| Feature | Fetch | Axios |
|---------|-------|-------|
| Native | ✅ | ❌ (3rd party) |
| Interceptors | ❌ | ✅ |
| Auto JSON | ❌ | ✅ |
| Timeout | Manual | Built-in |
| Cancel | AbortController | CancelToken |

## Related Terminologies

- **API** (Server) - Service layer abstraction
- **Middleware** (State) - Async action handling
- **Operations** (State) - Async state patterns
- **CRUD** (State) - AJAX for data operations

## Quality Gates

- [ ] Loading/error states handled
- [ ] Request cancellation on unmount
- [ ] Error handling with user feedback
- [ ] Centralized API client
- [ ] Environment-based URLs
- [ ] Interceptors for cross-cutting concerns

**Source**: `/docs/state/ajax.md`
