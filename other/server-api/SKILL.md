---
name: server-api
description: API service-layer patterns — axios/fetch client with interceptors, domain-scoped service objects (UserService, ProductService), auth-token refresh, request cancellation, and error normalisation. Use when adding or reviewing HTTP call sites, organising services under api/ or services/, or centralising cross-cutting request concerns.
when_to_use: Creating or refactoring API clients and service modules; adding auth-refresh or error interceptors; replacing scattered fetch/axios calls with a typed service layer; wiring AbortController cancellation.
paths:
  - "**/api/**/*.{js,ts}"
  - "**/services/**/*.{js,ts}"
  - "**/*Service*.{js,ts}"
  - "**/*Api*.{js,ts}"
---

# API

## What is an API Service?

API services are the centralized layer for all server communication—axios/fetch wrappers with interceptors for authentication, error handling, and request/response transformation. They eliminate scattered fetch calls.

## Key Principles

1. **Centralized HTTP Client**: Configure base URL, timeout, headers, interceptors once. All service methods inherit this configuration.

2. **Service Layer Pattern**: Create domain-specific services (UserService, ProductService) that abstract HTTP details into typed, callable methods.

3. **Interceptors for Cross-Cutting Concerns**: Request interceptors add auth headers; response interceptors handle 401 refresh, error normalization.

## Best Practices

✅ **DO**:
- Create base axios/fetch client with interceptors
- Organize services by domain (UserService, ProductService)
- Type all request/response interfaces
- Handle token refresh in response interceptor
- Implement consistent error structure
- Cancel outdated requests (AbortController)

❌ **DON'T**:
- Scatter raw fetch() calls throughout components
- Handle auth headers in every request manually
- Ignore error handling (show user-friendly messages)
- Store tokens in easily-accessible localStorage (use httpOnly cookies)
- Forget request cancellation on component unmount

## Code Patterns

### Base Client with Interceptors

```javascript
// apiClient.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.API_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
});

// Request interceptor - add auth
apiClient.interceptors.request.use(config => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle 401
apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      await refreshToken();
      return apiClient.request(error.config);
    }
    return Promise.reject(normalizeError(error));
  }
);

export default apiClient;
```

### Service Layer

```javascript
// UserService.js
import apiClient from './apiClient';

const UserService = {
  getUser: (id) => apiClient.get(`/users/${id}`),
  getUsers: (params) => apiClient.get('/users', { params }),
  createUser: (data) => apiClient.post('/users', data),
  updateUser: (id, data) => apiClient.put(`/users/${id}`, data),
  deleteUser: (id) => apiClient.delete(`/users/${id}`)
};

export default UserService;
```

### Usage in Components

```jsx
// Component consuming API service
const UserList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const { data } = await UserService.getUsers({ page: 1 });
        setUsers(data);
      } catch (error) {
        toast.error(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);
};
```

## Related Terminologies

- **Ajax** (State) - Async data fetching operations
- **Authentication** (Server) - Token management in interceptors
- **Store** (State) - API results often stored in state
- **Middleware** (State) - API calls triggered via middleware

## Quality Gates

- [ ] Centralized HTTP client with interceptors
- [ ] Services organized by domain
- [ ] Error handling consistent
- [ ] Auth token refresh handled
- [ ] Request/response typed
- [ ] Cancellation for unmounted components

**Source**: `/docs/server/api.md`
