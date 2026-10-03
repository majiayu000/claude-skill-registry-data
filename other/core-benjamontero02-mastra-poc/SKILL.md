---
name: frontend-core-principles
description: Universal frontend principles and architecture patterns language-agnostic. Core foundation for frontend architects covering component design, data management, styling, accessibility, and performance across any framework or library.
license: MIT
metadata:
  author: Mastra
  version: "1.0.0"
---

# Universal Frontend Core Principles

Fundamental frontend architecture and design principles applicable across all frameworks, libraries, and styling solutions. These are the foundational rules that must guide any frontend implementation.

## When to Apply

Use this skill as the foundation for every frontend task:
- Creating new components or pages
- Refactoring existing UI code
- Implementing data fetching and state management
- Building forms and user interactions
- Optimizing performance or accessibility
- Reviewing code for architecture and usability issues

This skill complements framework-specific skills (React, Vue, Svelte, etc.) which provide concrete implementation patterns for the framework in use. Use alongside component design skills (Atomic Design, Composition Patterns) and styling skills (Tailwind, etc.).

## Core Principles by Category

### 1. Centralized HTTP Client (CRITICAL)

**Principle**: All data fetching goes through a single HTTP client. Never use fetch/axios scattered across components.

- Create a single HTTP client instance (axios, fetch wrapper) configured with base URL, headers, auth
- Implement global interceptors: request (auth token injection), response (error handling, token refresh)
- All API endpoints defined in one place (usually `api/client.ts` or `services/api.ts`)
- Each domain (users, posts, orders) has a service that uses the shared client: `userService.getUser(id)`, `postService.getPosts()`
- No direct fetch/axios calls in components; always use service layer
- Handle HTTP errors globally: 401 (redirect to login), 403 (show permission denied), 500 (show error toast)
- Implement request/response logging for debugging
- Example structure:
  ```
  api/client.ts         → HTTP client with interceptors
  api/authInterceptor   → Inject JWT token, handle 401 refresh
  services/users.ts     → export getUser(id), createUser(data), etc.
  services/posts.ts     → export getPosts(), createPost(data), etc.
  Components            → import { userService } from '@/services', call userService.getUser(id)
  ```

### 2. HTTP Interceptors: Auth & Error Handling (CRITICAL)

**Principle**: All HTTP concerns (auth, error handling) happen once in interceptors, not per component.

- **Request Interceptor**:
  - Inject JWT token from secure storage (localStorage, sessionStorage, cookie) into Authorization header
  - Add correlation ID or trace ID for logging
  - Example: `Authorization: Bearer ${token}`
- **Response Interceptor**:
  - Handle 401 Unauthorized: clear token, redirect to login, show message
  - Handle 403 Forbidden: show "Permission denied" message
  - Handle 400 Bad Request: extract validation errors, pass to form component
  - Handle 5xx Server Error: show "Service unavailable" toast, retry or redirect
  - Handle network errors: show connection lost message, enable offline mode
  - Never silently swallow errors
- Implement token refresh: on 401, use refresh token to get new access token, retry original request
- Centralize error mapping: HTTP status/code → user-friendly message (translation keys)
- Example: User makes request while offline → Error interceptor catches → Show toast "No internet connection" → Enable retry when online

### 3. Atomic Design: Component Hierarchy (HIGH)

**Principle**: Build UI bottom-up using a predictable hierarchy: Atoms → Molecules → Organisms → Templates → Pages.

**Atoms**: Smallest, reusable building blocks. No business logic.
- Button, Input, Label, Icon, Badge, Divider
- Props: style (variant, size), state (disabled, loading), handlers (onClick)
- Pure presentation; no data fetching or external dependencies
- Example: `<Button variant="primary" onClick={handleClick} />`

**Molecules**: Atoms combined into coherent units. Still mostly presentational.
- Form field (Input + Label), Search bar (Input + Button + Icon), Card header (Icon + Title + Actions)
- Props: data, handlers, state
- Example: `<FormField label="Email" value={email} onChange={setEmail} error={errors.email} />`

**Organisms**: Molecules combined into complex, feature-rich sections. May have state and light logic.
- User form (multiple FormFields + validation), Navigation bar (Logo + Menu + Auth), Product list (filter + sort + Grid of cards)
- Props: data, handlers, may manage local state
- Example: `<UserForm user={user} onSubmit={handleSubmit} errors={errors} />`

**Templates**: Page layouts without page-specific content. Composition of organisms and structural components.
- Two-column layout (Sidebar + Main), Dashboard layout (Header + Nav + Content), Single-column form layout
- Props: content slots, configuration
- Example: `<DashboardLayout header={<Header />} sidebar={<Nav />}>{content}</DashboardLayout>`

**Pages**: Concrete instances of templates filled with real data. Fetch data, call APIs.
- UserListPage (fetch users, render UserList organism in ListView template)
- ProductDetailPage (fetch product by ID, render ProductDetail organism)
- Example: `<UserListPage filter={urlParams.filter} />`

Benefits:
- Clear separation of concerns
- Easy testing: atoms/molecules testable without mocks
- Scalability: reuse organisms across pages
- Consistency: look and feel defined at atom/molecule level
- Documentation: clear component purpose and props

### 4. Presentation vs Container Components (HIGH)

**Principle**: Separate how things look from how they work.

**Presentation (Dumb) Components**:
- Receive all data as props
- No data fetching, API calls, or subscriptions
- Pure functions; same props → same output
- Focus on rendering and handling user interactions
- Easy to test: pass props, check rendered output
- Example:
  ```typescript
  // UserCard.tsx - pure presentation
  export function UserCard({ user, onEdit, onDelete }) {
    return (
      <div>
        <h2>{user.name}</h2>
        <p>{user.email}</p>
        <button onClick={() => onEdit(user.id)}>Edit</button>
        <button onClick={() => onDelete(user.id)}>Delete</button>
      </div>
    );
  }
  ```

**Container (Smart) Components**:
- Fetch data and manage state
- Wire up event handlers and logic
- Pass data to presentation components as props
- Handle side effects (API calls, subscriptions)
- Example:
  ```typescript
  // UserCardContainer.tsx - container
  export function UserCardContainer({ userId }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
      userService.getUser(userId).then(data => {
        setUser(data);
        setLoading(false);
      });
    }, [userId]);
    
    const handleEdit = (id) => navigate(`/users/${id}/edit`);
    const handleDelete = (id) => userService.deleteUser(id).then(() => reload());
    
    if (loading) return <Spinner />;
    return <UserCard user={user} onEdit={handleEdit} onDelete={handleDelete} />;
  }
  ```

Benefits:
- Presentation components are easier to test (no mocks needed)
- Container components can be refactored without changing presentation
- Easy to swap presentation library (e.g., swap custom Button for MUI Button)
- Reuse presentation components in different containers

### 5. Explicit State Management: Loading, Error, Empty (HIGH)

**Principle**: Every data-bound view must explicitly handle loading, error, and empty states.

For any async data operation (API call):
1. **Loading state**: Show spinner, skeleton, or disabled input while fetching
2. **Error state**: Display error message; offer retry or fallback
3. **Empty state**: If data is array and length === 0, show "No results" message
4. **Success state**: Render data

Example state machine:
```typescript
type DataState = 'idle' | 'loading' | 'success' | 'error';

const [state, setState] = useState<DataState>('idle');
const [data, setData] = useState(null);
const [error, setError] = useState(null);

useEffect(() => {
  setState('loading');
  fetchData()
    .then(result => {
      setData(result);
      setState('success');
    })
    .catch(err => {
      setError(err.message);
      setState('error');
    });
}, []);

return (
  <>
    {state === 'loading' && <Spinner />}
    {state === 'error' && <ErrorMessage message={error} onRetry={refetch} />}
    {state === 'success' && data.length === 0 && <EmptyState />}
    {state === 'success' && data.length > 0 && <DataList data={data} />}
  </>
);
```

Anti-pattern: Conditionally rendering data without checking loading/error first; UI jumps, confuses users.

### 6. API Contract Typing (HIGH)

**Principle**: Define types for all API contracts in one place. Update one file when API changes.

Central file: `types/api.ts` (or per-domain: `types/user.ts`, `types/post.ts`)

```typescript
// types/api.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: string;
}

export interface GetUserResponse {
  data: User;
  status: 'success';
}

export interface ListUsersResponse {
  data: User[];
  pagination: {
    limit: number;
    offset: number;
    total: number;
  };
}

export interface CreateUserRequest {
  name: string;
  email: string;
}

// services/users.ts
export const userService = {
  getUser(id: string): Promise<GetUserResponse> { ... },
  listUsers(limit: number, offset: number): Promise<ListUsersResponse> { ... },
  createUser(req: CreateUserRequest): Promise<GetUserResponse> { ... },
};

// components/UserForm.tsx
import { CreateUserRequest, User } from '@/types/api';

export function UserForm({ onSubmit }: { onSubmit: (user: CreateUserRequest) => void }) {
  // Form fields match CreateUserRequest shape
}
```

Benefits:
- Single source of truth for API contracts
- IDE autocomplete when calling services
- Type safety: catch mismatches at compile time
- Documentation: types describe expected format
- Refactoring: update type → all usages break until fixed

### 7. Avoid Duplicating Server State in Local State (HIGH)

**Principle**: Don't maintain two copies of the same data. Client state should reflect server state or be purely local UI state.

Bad pattern:
```typescript
// DON'T DO THIS
const [user, setUser] = useState(null);     // fetched from server
const [userEdited, setUserEdited] = useState(null);  // local copy, gets out of sync

fetch('/user').then(data => setUser(data));
// User edits → setUserEdited(newData)
// Original `user` is stale; two sources of truth
```

Good pattern:
```typescript
// DO THIS
const [user, setUser] = useState(null);     // from server
const [formData, setFormData] = useState({});  // only form UI state, NOT a copy

fetch('/user').then(data => setUser(data));

// In form: edit formData, submit to server
// On submit success: refetch or optimistically update `user`
// On submit error: revert formData, show error

// Or use form library (React Hook Form, Formik) that manages form state separately
```

Pattern: Server state (from API) lives in one place. Form local state is separate and temporary. On save, submit form state to server; on success, update server state.

### 8. DRY: Component Props & Reusability (MEDIUM)

**Principle**: Write components once, use everywhere. Avoid duplicating similar components.

Bad: Separate components for different use cases
```typescript
<UserButton user={user} />
<AdminButton admin={admin} />
<GuestButton />
// Three components doing same thing
```

Good: Single component with variant prop
```typescript
<UserButton user={user} variant="user" />
<UserButton user={admin} variant="admin" />
<UserButton variant="guest" />
// Or even simpler: <Button role={user.role} />
```

Reusability guidelines:
- Extract common logic to custom hooks: `useAsync`, `useFetch`, `useLocalStorage`
- Create generic components: `<List items={items} renderItem={...} />` instead of `<UserList>`, `<PostList>`
- Use composition over inheritance: pass content as children/props
- Avoid prop drilling: use context for global state (theme, user, auth)

### 9. Accessibility Basics (MEDIUM)

**Principle**: Ensure app is usable by everyone, including keyboard and screen reader users.

Semantic HTML:
- Use `<button>` for actions, `<a>` for navigation, `<main>`, `<header>`, `<nav>`, `<section>`
- Use headings correctly: `<h1>` once per page, `<h2>`, `<h3>` in hierarchy
- Use `<label htmlFor="...">` for form inputs
- Use `<form>` wrapper for form controls

Keyboard Navigation:
- All interactive elements must be focusable (buttons, links, inputs)
- Tab order should match visual order (use CSS `tab-index` rarely)
- Escape key closes modals/dropdowns
- Enter/Space activates buttons

Screen Readers:
- Provide `alt` text for images (describe purpose, not "image")
- Use `aria-label` or `aria-labelledby` for icon-only buttons
- Use `aria-hidden="true"` for decorative elements
- Use `role="..."`  sparingly; prefer semantic HTML

Color & Contrast:
- Text contrast ratio ≥ 4.5:1 for normal text (WCAG AA)
- Don't rely on color alone to convey information
- Test with tools: axe DevTools, WAVE, Lighthouse

Focus Indicators:
- Visible focus outline (don't remove default unless replacing with custom)
- High contrast focus indicator (e.g., bold border)

Example:
```typescript
// Bad: Inaccessible
<div onClick={handleClick}>Delete</div>

// Good: Accessible
<button onClick={handleClick} aria-label="Delete user">
  <TrashIcon />
</button>
```

### 10. Performance: Rendering & Optimization (MEDIUM)

**Principle**: Optimize for user perception: fast first paint, smooth interactions, no jank.

Rendering Optimization:
- **Memoization**: Use `memo()` to prevent unnecessary re-renders of expensive components
- **useMemo**: Cache computed values that depend on specific inputs
- **useCallback**: Cache function references to prevent child re-renders
- **Lazy Loading**: Code split routes and heavy components; load on demand
- **Virtual Scrolling**: For long lists, render only visible items
- **Avoid rerenders**: Don't create new object/function props each render

JavaScript Performance:
- Bundle analysis: identify and lazy-load large dependencies
- Tree-shaking: remove unused code
- Minification and compression
- Avoid blocking main thread: move heavy work to Web Workers or async

Monitoring:
- Core Web Vitals: LCP (Largest Contentful Paint), FID (First Input Delay), CLS (Cumulative Layout Shift)
- Monitor runtime performance: FPS, memory, long tasks
- Use Lighthouse, PageSpeed Insights, WebPageTest

Example optimization:
```typescript
// Bad: Re-renders child on every parent update
function Parent() {
  return <Child onClick={() => handleClick()} />;  // New function each render
}

// Good: Callback cached
function Parent() {
  const handleClick = useCallback(() => { ... }, []);
  return <Child onClick={handleClick} />;  // Same function reference
}

// Better: Memoized child
const Child = memo(function Child({ onClick }) {
  return <button onClick={onClick}>Click</button>;
});
```

### 11. Forms: Validation & Error Display (MEDIUM)

**Principle**: Forms must validate input and show clear, field-specific errors.

Form Flow:
1. **Client-side validation**: On blur or submit, validate input (required, format, length)
2. **Submit**: Send to server
3. **Server-side validation**: Server validates (auth, business rules); returns errors or success
4. **Error Display**: If errors, show field-specific messages; scroll to first error
5. **Success**: Clear form, show success message, redirect or refresh

Example:
```typescript
const [formData, setFormData] = useState({ email: '', password: '' });
const [errors, setErrors] = useState<Record<string, string>>({});
const [isSubmitting, setIsSubmitting] = useState(false);

async function handleSubmit(e) {
  e.preventDefault();
  
  // Client validation
  const newErrors = {};
  if (!formData.email) newErrors.email = 'Email required';
  if (!formData.password) newErrors.password = 'Password required';
  
  if (Object.keys(newErrors).length > 0) {
    setErrors(newErrors);
    return;
  }
  
  // Submit
  setIsSubmitting(true);
  try {
    const response = await authService.login(formData);
    // Success: clear and redirect
    setFormData({ email: '', password: '' });
    navigate('/dashboard');
  } catch (error) {
    // Server errors: show field-specific or general
    setErrors({ general: error.message });
  } finally {
    setIsSubmitting(false);
  }
}

return (
  <form onSubmit={handleSubmit}>
    {errors.general && <Alert message={errors.general} />}
    <input
      name="email"
      value={formData.email}
      onChange={(e) => setFormData({...formData, email: e.target.value})}
      aria-invalid={!!errors.email}
    />
    {errors.email && <span role="alert">{errors.email}</span>}
    {/* ... */}
    <button type="submit" disabled={isSubmitting}>
      {isSubmitting ? 'Signing in...' : 'Sign In'}
    </button>
  </form>
);
```

### 12. Styling Strategy (MEDIUM)

**Principle**: Styling must be maintainable, consistent, and avoid specificity wars.

Approaches:
- **Utility Classes** (Tailwind, Windi): Rapid development, consistent spacing/colors, but HTML bloat
- **CSS-in-JS** (Styled Components, Emotion): Scoped styles, dynamic theming, but runtime overhead
- **CSS Modules**: Scoped by default, pure CSS, good for complex layouts
- **BEM/SMACSS**: Naming conventions to manage specificity

Consistency:
- Define color palette, typography scale, spacing grid in design tokens
- Use variables/tokens, not magic numbers: `var(--spacing-4)` not `16px`
- Theme support: light/dark modes via CSS variables or context
- Responsive design: mobile-first; use breakpoints consistently

Example (Tailwind):
```typescript
<div className="flex items-center justify-between gap-4 px-4 py-2 bg-white rounded-lg shadow">
  <h3 className="text-lg font-semibold text-gray-900">Title</h3>
  <button className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">Action</button>
</div>
```

Anti-pattern: Inline styles, hardcoded colors, inconsistent spacing

## Implementation Patterns

### Pattern: Custom Hook for Data Fetching
```typescript
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    httpClient.get<T>(url)
      .then(result => { setData(result); setLoading(false); })
      .catch(err => { setError(err.message); setLoading(false); });
  }, [url]);
  
  return { data, loading, error };
}
```

### Pattern: Context for Global State
```typescript
const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  return useContext(ThemeContext);
}

// In component: const { theme, setTheme } = useTheme();
```

## Metrics & Monitoring

Track these metrics to ensure frontend health:
- **Page Load Time**: Time to First Paint, Largest Contentful Paint (LCP)
- **Interaction Responsiveness**: First Input Delay (FID), Interaction to Next Paint (INP)
- **Layout Stability**: Cumulative Layout Shift (CLS)
- **Error Rate**: % of requests failing; JS errors
- **User Interactions**: Button clicks, form submissions, navigation

## Checklist for Frontend Implementation

- [ ] Single HTTP client with centralized interceptors for auth and error handling
- [ ] All API responses typed; types defined in central location
- [ ] Components use Atomic Design hierarchy (atoms → molecules → organisms)
- [ ] Presentation components separated from containers
- [ ] All data-bound views handle loading, error, and empty states explicitly
- [ ] No duplicate server state in local state; form state is separate
- [ ] Common UI patterns extracted to reusable components
- [ ] Basic accessibility: semantic HTML, labels, keyboard navigation, alt text
- [ ] Core Web Vitals monitored and optimized
- [ ] Forms validate client-side and display server errors clearly
- [ ] Styling is consistent and maintainable (design tokens, utility classes or CSS modules)
- [ ] Large components lazy-loaded; code split by route
- [ ] Expensive components memoized; hooks used correctly
- [ ] Logging includes user context for debugging
- [ ] Dark mode or theme switching available if applicable

---

These principles are the foundation. Framework-specific skills (React, Vue, Svelte, etc.) and styling skills (Tailwind, CSS Modules, etc.) show how to implement these principles in concrete code.
