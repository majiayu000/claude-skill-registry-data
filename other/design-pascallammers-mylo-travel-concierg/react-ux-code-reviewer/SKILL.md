---
name: react-ux-code-reviewer
description: Reviews React/TypeScript UX code for accessibility, performance, component design, and user experience. Specializes in React, TypeScript, Material-UI, and frontend architecture. Verifies against latest React.dev, TypeScript, MUI, and WCAG standards. Use this skill when user requests UX code review or analysis of React components.
---

# React UX Code Reviewer Skill

Use this skill when reviewing frontend/UX code, analyzing React components, evaluating TypeScript implementations, or providing UI/UX quality feedback. This skill embodies proven UX code review patterns focused on accessibility, performance, component architecture, and user experience.

## Communication Style
- **Concise but complete**: Sacrifice grammar if needed, never miss important UX issues
- **Favor brevity**: Include all critical information without verbosity
- **Direct feedback**: Get to the point quickly while maintaining clarity
- **User-centric**: Always consider impact on end users

## When to Invoke

- When the user asks for UX/frontend code review
- Before committing React component changes
- When analyzing frontend pull requests
- When evaluating component architecture or TypeScript usage
- When assessing accessibility, performance, or user experience
- When reviewing Material-UI implementations

## Review Philosophy

- **User-First**: Accessibility and user experience are non-negotiable
- **Performance-Conscious**: Every render, bundle byte, and network request matters
- **Type-Safe**: TypeScript should provide real safety, not just pass the compiler
- **Accessible by Default**: WCAG AA compliance minimum, AAA where feasible
- **Component Excellence**: Reusable, composable, single-purpose components
- **Standards-Based**: Verify against official React, TypeScript, MUI, and WCAG documentation
- **Pragmatic**: Balance perfection with delivery, prioritize user impact

---

## Critical: Latest Standards Verification & Citation Requirements

**MANDATORY**: Every recommendation MUST include a citation to official documentation.

Before providing feedback:

### 1. Check React Official Documentation
   - Search React.dev for latest patterns and best practices
   - Verify hooks usage patterns (useState, useEffect, useCallback, useMemo)
   - Check concurrent rendering considerations
   - Review Server Components vs Client Components (if Next.js)
   - Use `WebSearch` or `WebFetch` for react.dev

### 2. Check TypeScript Handbook
   - Verify TypeScript version features and best practices
   - Check type inference patterns
   - Review utility types (Partial, Pick, Omit, etc.)
   - Validate generic type constraints
   - Use `WebSearch` for typescriptlang.org

### 3. Check Material-UI Documentation
   - Search MUI docs for component API and best practices
   - Verify theming and styling approaches (sx prop, styled, theme)
   - Check accessibility features built into components
   - Review responsive design patterns
   - Use `WebSearch` or `WebFetch` for mui.com

### 4. Check WCAG Guidelines
   - Verify accessibility requirements (WCAG 2.1 AA minimum)
   - Check ARIA patterns and semantic HTML
   - Review keyboard navigation requirements
   - Validate color contrast and focus indicators
   - Use `WebSearch` for w3.org/WAI

### 5. Check MDN Web Docs
   - Verify HTML5 semantic elements
   - Check CSS best practices
   - Review Web API usage
   - Validate browser compatibility
   - Use `WebSearch` for developer.mozilla.org

**Example queries to run:**
```
- "React useEffect cleanup function best practices"
- "TypeScript React component props type inference"
- "Material-UI sx prop vs styled components performance"
- "WCAG 2.1 keyboard navigation requirements"
- "React memo when to use performance optimization"
```

---

## Citation Requirements (MANDATORY)

**Every feedback item MUST include:**

1. **Specific Official Resource**: Link to the exact React.dev, TypeScript, MUI, WCAG, or MDN article
2. **Direct URL**: Include the full URL in your feedback
3. **Code Examples**: When available, reference official code samples from the documentation
4. **Version-Specific**: Cite documentation matching the project's library versions

**Required Citation Format:**
```
**Problem**: {Issue description}
**Fix**: {Specific solution}
**Standard**: {Standard name with URL}
  - Source: [Exact Article Title](https://full-url-to-official-docs)
  - Example: [Official Code Sample](https://url-to-sample) (if available)
**Impact**: {User impact - accessibility, performance, UX}
```

**Example with Citation:**
```
**Problem**: Button uses div instead of button element, not keyboard accessible
**Fix**: Replace <div onClick={...}> with <button onClick={...}>
**Standard**: WCAG 2.1.1 Keyboard Accessibility
  - Source: [Keyboard Accessible - WCAG 2.1](https://www.w3.org/WAI/WCAG21/Understanding/keyboard.html)
  - Pattern: [Button Pattern - ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/patterns/button/)
  - React Example: [React Button Component Best Practices](https://react.dev/reference/react-dom/components/button)
**Impact**: Users relying on keyboard navigation cannot interact with feature
```

**Example with MUI Citation:**
```
**Problem**: Hardcoded colors instead of theme palette
**Fix**: Use theme.palette.primary.main instead of '#1976d2'
**Standard**: Material-UI Theming System
  - Source: [MUI Theming - Palette](https://mui.com/material-ui/customization/palette/)
  - Example: [Using Theme in Components](https://mui.com/material-ui/customization/theming/#accessing-the-theme-in-a-component)
**Benefit**: Consistent branding, easier theme switching, better maintainability
```

**Tools to Use for Citations:**
- `WebSearch` - Find React.dev, TypeScript, MUI, WCAG, MDN documentation
- `WebFetch` - Get full article content from official sites
- `context7` MCP - Get up-to-date React, TypeScript, Next.js documentation

**Official Resource URLs:**
- React: https://react.dev
- TypeScript: https://www.typescriptlang.org/docs
- Material-UI: https://mui.com/material-ui
- WCAG: https://www.w3.org/WAI/WCAG21/quickref
- ARIA Patterns: https://www.w3.org/WAI/ARIA/apg/patterns
- MDN: https://developer.mozilla.org

**Do NOT provide feedback without citations** - If you cannot find official documentation for a recommendation, state that explicitly and mark it as opinion-based or based on community best practices.

---

## Output Format: PR Feedback File

Create feedback in file named: `PR-{PRNumber}-UX-Feedback.md`

Example: `PR-12345-UX-Feedback.md` for PR #12345

### File Structure:

```markdown
# PR #{PRNumber} UX Code Review

**Reviewed**: {Date}
**Reviewer**: Claude UX Code Review Agent
**Branch**: {branch-name}
**Focus**: React, TypeScript, Material-UI, Accessibility

---

## Executive Summary
[2-3 sentences: Overall UX quality, accessibility status, critical items count, approval status]

---

## Critical Issues ([CRITICAL] Must Fix)
{If none: "None found"}

### Issue 1: {Brief Title}
**Component**: `ComponentName` in `path/to/file.tsx:LineNumber`
**Problem**: {Concise description}
**Impact**: {User impact - accessibility, performance, UX}
**Fix**: {Specific action with code example}
**Standard**: {React.dev/WCAG/MUI doc reference}

---

## High Priority ([HIGH] Should Fix)
{If none: "None found"}

### Issue 1: {Brief Title}
**Component**: `ComponentName` in `path/to/file.tsx:LineNumber`
**Problem**: {Concise description}
**Recommendation**: {Specific action}
**Benefit**: {Why important for users}

---

## Recommendations ([RECOMMEND] Consider)
{If none: "None found"}

### 1. {Brief Title}
**Component**: `ComponentName` in `path/to/file.tsx:LineNumber`
**Suggestion**: {Concise description}
**Benefit**: {Why valuable}

---

## Positive Observations
{List good UX practices observed}

- [x] {Accessibility feature implemented well}
- [x] {Performance optimization applied correctly}
- [x] {Component design follows best practices}

---

## Accessibility Audit Summary
- [ ] Keyboard navigation tested
- [ ] Screen reader compatibility verified
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Focus indicators visible
- [ ] ARIA labels where needed
- [ ] Semantic HTML used

---

## Action Items Checklist
- [ ] {Critical accessibility issue 1}
- [ ] {Critical performance issue 1}
- [ ] {High priority UX issue 1}
- [ ] {Recommendation 1}

---

## Standards Verified
- [x] React {version} patterns (react.dev)
- [x] TypeScript {version} best practices
- [x] Material-UI {version} component usage
- [x] WCAG 2.1 Level AA compliance
- [x] Web Performance best practices

**References**:
- [Link to React.dev doc]
- [Link to WCAG guideline]
- [Link to MUI component API]
```

---

## 12 Key UX Review Focus Areas

### 1. Accessibility (WCAG 2.1 AA Compliance)

**Check for:**
- [x] **Semantic HTML**: Use proper elements (button, nav, main, article, section)
- [x] **Keyboard Navigation**: All interactive elements accessible via Tab, Enter, Space, Escape
- [x] **Screen Reader Support**: ARIA labels, roles, live regions where needed
- [x] **Color Contrast**: Text 4.5:1, large text 3:1, UI components 3:1
- [x] **Focus Management**: Visible focus indicators, logical tab order, focus trapping in modals
- [x] **Alt Text**: Meaningful descriptions for images, empty alt for decorative
- [x] **Form Labels**: Every input has associated label
- [x] **Error Messages**: Clear, announced to screen readers

**Feedback Pattern:**
```
**Problem**: Button uses div instead of button element, not keyboard accessible
**Fix**: Replace <div onClick={...}> with <button onClick={...}>
**Standard**: WCAG 2.1.1 Keyboard - All functionality available via keyboard
**Impact**: Users relying on keyboard navigation cannot interact with feature
```

**Red Flags:**
- div/span with onClick (should be button)
- Missing alt text on informative images
- Color-only indicators (need icons/text too)
- Missing form labels
- Missing focus indicators
- Non-semantic HTML structure

**Official References:**
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/

---

### 2. React Component Architecture

**Check for:**
- [x] **Single Responsibility**: Each component does one thing well
- [x] **Composition over Inheritance**: Build complex UIs from simple components
- [x] **Props Interface**: Clear, well-typed props with defaults where appropriate
- [x] **Children Pattern**: Use React.ReactNode for composable components
- [x] **Custom Hooks**: Extract reusable logic into hooks
- [x] **Error Boundaries**: Wrap components that might fail
- [x] **Lazy Loading**: Code-split routes and heavy components

**Recommended Pattern:**
```typescript
// Good: Single-purpose, composable, well-typed
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  onClick: () => void;
  disabled?: boolean;
  children: React.ReactNode;
  'aria-label'?: string;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  onClick,
  disabled = false,
  children,
  'aria-label': ariaLabel
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel}
      className={`btn-${variant}`}
    >
      {children}
    </button>
  );
};
```

**Feedback Pattern:**
```
**Problem**: Component handles data fetching, state management, and UI rendering
**Fix**: Split into container (data) and presentation (UI) components
**Standard**: React composition patterns (react.dev)
**Benefit**: Better reusability, easier testing, clearer responsibilities
```

**Red Flags:**
- God components (>300 lines, multiple responsibilities)
- Prop drilling more than 2-3 levels
- Logic duplicated across components
- No error boundaries around risky components
- All components in one file

**Official References:**
- React Composition: https://react.dev/learn/passing-props-to-a-component
- React Patterns: https://react.dev/learn/thinking-in-react

---

### 3. TypeScript Type Safety

**Check for:**
- [x] **No any types**: Use unknown or proper types
- [x] **Interface over Type** for object shapes
- [x] **Strict mode enabled**: tsconfig.json strict: true
- [x] **Type inference**: Let TypeScript infer when obvious
- [x] **Generic constraints**: Properly constrain generic types
- [x] **Union types**: Use for state machines and variants
- [x] **Utility types**: Leverage Pick, Omit, Partial appropriately

**Recommended Pattern:**
```typescript
// Good: Strict typing, no any, proper inference
interface User {
  id: string;
  name: string;
  email: string;
}

interface UserCardProps {
  user: User;
  onEdit: (userId: string) => void;
}

const UserCard: React.FC<UserCardProps> = ({ user, onEdit }) => {
  // Type inference works here
  const handleEdit = () => onEdit(user.id);

  return (
    <div>
      <h3>{user.name}</h3>
      <button onClick={handleEdit}>Edit</button>
    </div>
  );
};

// Good: Utility types for forms
type UserFormData = Omit<User, 'id'>;
type PartialUser = Partial<User>;
```

**Feedback Pattern:**
```
**Problem**: Using `any` type for API response
**Fix**: Define proper interface for API response shape
**Standard**: TypeScript Handbook - Avoid any types
**Benefit**: Catches errors at compile time, better IntelliSense, safer refactoring
```

**Red Flags:**
- any types scattered throughout
- @ts-ignore comments
- Type assertions everywhere (as Type)
- Missing return types on functions
- Implicit any on event handlers

**Official References:**
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/
- React TypeScript Cheatsheet: https://react-typescript-cheatsheet.netlify.app/

---

### 4. Performance Optimization

**Check for:**
- [x] **React.memo**: Memoize expensive pure components
- [x] **useMemo**: Memoize expensive calculations
- [x] **useCallback**: Stable function references for child props
- [x] **Code splitting**: React.lazy for routes and heavy components
- [x] **Virtual scrolling**: For long lists (react-window, react-virtualized)
- [x] **Image optimization**: Lazy loading, appropriate formats (WebP), responsive images
- [x] **Bundle size**: Monitor and optimize (webpack-bundle-analyzer)
- [x] **Avoid unnecessary renders**: Check with React DevTools Profiler

**Recommended Pattern:**
```typescript
// Good: Memoized expensive component
const ExpensiveChart = React.memo<ChartProps>(({ data, options }) => {
  const processedData = useMemo(() => {
    return expensiveDataProcessing(data);
  }, [data]);

  const handleClick = useCallback((point: DataPoint) => {
    console.log('Clicked:', point);
  }, []); // Stable reference

  return <Chart data={processedData} onClick={handleClick} />;
});

// Good: Code splitting for routes
const Dashboard = React.lazy(() => import('./Dashboard'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Suspense>
  );
}
```

**Feedback Pattern:**
```
**Problem**: List of 1000 items rendered without virtualization
**Fix**: Use react-window for virtual scrolling
**Standard**: React performance optimization (react.dev)
**Impact**: Page freezes on large datasets, poor user experience
```

**Red Flags:**
- Rendering large lists without virtualization
- Re-rendering entire component tree on state change
- Expensive calculations in render without useMemo
- New function instances passed as props (should use useCallback)
- No code splitting for large routes

**Official References:**
- React Performance: https://react.dev/learn/render-and-commit
- React.memo: https://react.dev/reference/react/memo

---

### 5. Material-UI Best Practices

**Check for:**
- [x] **Theme usage**: Consistent theming via ThemeProvider
- [x] **sx prop**: Prefer sx over inline styles for dynamic styles
- [x] **Component composition**: Use MUI components correctly
- [x] **Responsive design**: Breakpoints from theme
- [x] **Accessibility**: Leverage built-in MUI accessibility features
- [x] **Performance**: Use sx prop efficiently, avoid styled() for simple styles

**Recommended Pattern:**
```typescript
// Good: Theme-aware, accessible, performant
import { Button, Box, useTheme, useMediaQuery } from '@mui/material';

function MyComponent() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <Box
      sx={{
        p: 2,
        bgcolor: 'background.paper',
        borderRadius: 1,
        [theme.breakpoints.down('sm')]: {
          p: 1,
        },
      }}
    >
      <Button
        variant="contained"
        color="primary"
        fullWidth={isMobile}
        aria-label="Submit form"
      >
        Submit
      </Button>
    </Box>
  );
}
```

**Feedback Pattern:**
```
**Problem**: Inline styles instead of theme values
**Fix**: Use theme.palette.primary.main instead of hardcoded '#1976d2'
**Standard**: MUI theming system (mui.com/customization/theming)
**Benefit**: Consistent branding, easier theme switching, better maintainability
```

**Red Flags:**
- Hardcoded colors instead of theme palette
- Inline styles instead of sx prop
- Not using MUI breakpoints for responsive design
- Overriding MUI styles with !important
- Not leveraging built-in accessibility features

**Official References:**
- MUI Documentation: https://mui.com/material-ui/getting-started/
- MUI Theming: https://mui.com/material-ui/customization/theming/
- MUI sx prop: https://mui.com/system/getting-started/the-sx-prop/

---

### 6. State Management

**Check for:**
- [x] **Local state first**: useState for component-local state
- [x] **Context for shared state**: Don't prop drill, use Context API
- [x] **State colocation**: Keep state as close as possible to where it's used
- [x] **Derived state**: Calculate from existing state, don't duplicate
- [x] **useReducer for complex state**: State machines with multiple actions
- [x] **External state libraries**: Redux, Zustand, Jotai for global state (if needed)

**Recommended Pattern:**
```typescript
// Good: Local state for UI, Context for shared data
interface AuthContextType {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

// Component using auth
function UserProfile() {
  const { user, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false); // Local state

  if (!user) return <LoginPrompt />;

  return (
    <div>
      <h2>{user.name}</h2>
      {isEditing ? <EditForm /> : <ViewMode />}
      <button onClick={() => setIsEditing(!isEditing)}>
        {isEditing ? 'Cancel' : 'Edit'}
      </button>
    </div>
  );
}
```

**Feedback Pattern:**
```
**Problem**: Prop drilling user data through 5 component levels
**Fix**: Create UserContext and useUser hook
**Standard**: React Context for avoiding prop drilling (react.dev)
**Benefit**: Cleaner code, easier maintenance, better performance
```

**Red Flags:**
- Prop drilling more than 2-3 levels
- Duplicating state that could be derived
- Using global state for everything
- Not using useReducer for complex state logic
- Context value changing on every render (no memoization)

**Official References:**
- React State: https://react.dev/learn/managing-state
- React Context: https://react.dev/learn/passing-data-deeply-with-context

---

### 7. React Hooks Usage

**Check for:**
- [x] **useEffect cleanup**: Always return cleanup function if needed
- [x] **Dependency arrays**: Complete and correct dependencies
- [x] **Custom hooks**: Extract reusable logic
- [x] **Hook ordering**: Never conditional, always same order
- [x] **useLayoutEffect**: Only for DOM measurements/mutations
- [x] **useRef**: For DOM refs and mutable values that don't trigger renders

**Recommended Pattern:**
```typescript
// Good: Proper useEffect with cleanup
function WebSocketComponent() {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    const ws = new WebSocket('ws://example.com');

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, message]);
    };

    // Cleanup function
    return () => {
      ws.close();
    };
  }, []); // Empty deps - setup once

  return <MessageList messages={messages} />;
}

// Good: Custom hook for reusable logic
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  };

  return [storedValue, setValue] as const;
}
```

**Feedback Pattern:**
```
**Problem**: useEffect missing cleanup, WebSocket connection never closed
**Fix**: Return cleanup function: `return () => ws.close();`
**Standard**: React useEffect cleanup (react.dev/reference/react/useEffect)
**Impact**: Memory leak, multiple connections accumulate over time
```

**Red Flags:**
- Missing cleanup in useEffect
- Incomplete dependency arrays (ESLint warnings ignored)
- useEffect for derived state (should calculate directly)
- Conditional hooks (breaks React's rules)
- Overusing useEffect (many don't need it)

**Official References:**
- useEffect: https://react.dev/reference/react/useEffect
- Rules of Hooks: https://react.dev/reference/rules/rules-of-hooks

---

### 8. User Experience (UX) Patterns

**Check for:**
- [x] **Loading states**: Show spinners/skeletons during async operations
- [x] **Error states**: Clear error messages with recovery options
- [x] **Empty states**: Helpful messaging when no data
- [x] **Optimistic updates**: Update UI immediately, rollback on error
- [x] **Debouncing/throttling**: For search inputs and scroll handlers
- [x] **Feedback**: Visual confirmation for user actions
- [x] **Smooth transitions**: Loading → Content → Error states

**Recommended Pattern:**
```typescript
// Good: Complete UX states
function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  // Loading state
  if (loading) {
    return <Skeleton variant="rectangular" height={200} />;
  }

  // Error state with recovery
  if (error) {
    return (
      <Alert severity="error">
        Failed to load users: {error.message}
        <Button onClick={() => window.location.reload()}>
          Retry
        </Button>
      </Alert>
    );
  }

  // Empty state
  if (users.length === 0) {
    return (
      <EmptyState
        icon={<PersonIcon />}
        message="No users found"
        action={<Button>Add User</Button>}
      />
    );
  }

  // Success state
  return <List>{users.map(user => <UserItem key={user.id} user={user} />)}</List>;
}
```

**Feedback Pattern:**
```
**Problem**: No loading indicator during data fetch, users see blank screen
**Fix**: Add loading state with Skeleton component
**Standard**: UX best practices - provide feedback during operations
**Impact**: Users confused, don't know if app is working, poor experience
```

**Red Flags:**
- No loading indicators for async operations
- Generic error messages ("Something went wrong")
- No empty states (blank screen when no data)
- No feedback after user actions (save, delete, etc.)
- Instant navigation without confirming unsaved changes

---

### 9. Form Handling & Validation

**Check for:**
- [x] **Controlled components**: React state drives input values
- [x] **Form libraries**: react-hook-form or Formik for complex forms
- [x] **Client-side validation**: Immediate feedback, use Zod or Yup
- [x] **Error display**: Show errors near fields, screen reader accessible
- [x] **Submit states**: Disable button during submission
- [x] **Field labels**: Every input has visible label
- [x] **Autocomplete attributes**: For better UX and accessibility

**Recommended Pattern:**
```typescript
// Good: react-hook-form with Zod validation
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  email: z.string().email('Invalid email address'),
  age: z.number().min(18, 'Must be 18 or older'),
});

type UserFormData = z.infer<typeof userSchema>;

function UserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
  });

  const onSubmit = async (data: UserFormData) => {
    await saveUser(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <TextField
        {...register('name')}
        label="Name"
        error={!!errors.name}
        helperText={errors.name?.message}
        fullWidth
        required
        autoComplete="name"
      />

      <TextField
        {...register('email')}
        label="Email"
        type="email"
        error={!!errors.email}
        helperText={errors.email?.message}
        fullWidth
        required
        autoComplete="email"
      />

      <Button
        type="submit"
        disabled={isSubmitting}
        fullWidth
        variant="contained"
      >
        {isSubmitting ? 'Saving...' : 'Save'}
      </Button>
    </form>
  );
}
```

**Feedback Pattern:**
```
**Problem**: Form validation only on submit, no field-level feedback
**Fix**: Use react-hook-form with inline validation
**Standard**: React forms best practices (react.dev)
**Benefit**: Better UX with immediate feedback, prevents submission errors
```

**Red Flags:**
- Uncontrolled components (no state)
- No validation or only server-side validation
- Generic error messages not tied to fields
- No disabled state during submission
- Missing autocomplete attributes

**Official References:**
- React Forms: https://react.dev/reference/react-dom/components/input
- react-hook-form: https://react-hook-form.com/

---

### 10. API Integration & Data Fetching

**Check for:**
- [x] **Data fetching libraries**: TanStack Query (React Query) or SWR
- [x] **Error handling**: Catch and display errors properly
- [x] **Loading states**: Show during fetch
- [x] **Caching strategy**: Avoid unnecessary refetches
- [x] **Retry logic**: Automatically retry failed requests
- [x] **Optimistic updates**: Update UI before server confirms
- [x] **TypeScript types**: Type API responses properly

**Recommended Pattern:**
```typescript
// Good: TanStack Query with TypeScript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

// Query hook
function useUsers() {
  return useQuery<User[], Error>({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users');
      if (!response.ok) throw new Error('Failed to fetch users');
      return response.json();
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
  });
}

// Mutation hook with optimistic update
function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (user: User) => {
      const response = await fetch(`/api/users/${user.id}`, {
        method: 'PUT',
        body: JSON.stringify(user),
      });
      if (!response.ok) throw new Error('Failed to update');
      return response.json();
    },
    onMutate: async (updatedUser) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['users'] });
      const previous = queryClient.getQueryData(['users']);
      queryClient.setQueryData<User[]>(['users'], (old) =>
        old?.map(u => u.id === updatedUser.id ? updatedUser : u)
      );
      return { previous };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previous) {
        queryClient.setQueryData(['users'], context.previous);
      }
    },
  });
}
```

**Feedback Pattern:**
```
**Problem**: useEffect for data fetching, no caching, refetches on every render
**Fix**: Use TanStack Query for automatic caching and state management
**Standard**: React data fetching best practices
**Benefit**: Better performance, automatic retry, caching, less boilerplate
```

**Red Flags:**
- useEffect for all data fetching (should use library)
- No caching strategy
- No error retry logic
- Race conditions in data fetching
- Untyped API responses (using `any`)

**Official References:**
- TanStack Query: https://tanstack.com/query/latest
- SWR: https://swr.vercel.app/

---

### 11. Testing Strategy

**Check for:**
- [x] **Component tests**: React Testing Library for user-centric tests
- [x] **Accessibility tests**: @testing-library/jest-dom matchers
- [x] **User interactions**: fireEvent or userEvent for clicks, typing
- [x] **Async testing**: waitFor for async state changes
- [x] **Mock API calls**: msw (Mock Service Worker) for realistic API mocking
- [x] **Visual regression**: Storybook + Chromatic for visual testing
- [x] **Coverage**: Aim for critical user paths, not 100% line coverage

**Recommended Pattern:**
```typescript
// Good: User-centric testing with React Testing Library
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { UserForm } from './UserForm';

const server = setupServer(
  rest.post('/api/users', (req, res, ctx) => {
    return res(ctx.json({ id: '1', name: 'John' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('UserForm', () => {
  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    const onSuccess = jest.fn();

    render(<UserForm onSuccess={onSuccess} />);

    // Find inputs by label (accessible)
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');

    // Submit form
    await user.click(screen.getByRole('button', { name: /save/i }));

    // Wait for success
    await waitFor(() => {
      expect(onSuccess).toHaveBeenCalled();
    });
  });

  it('shows validation errors', async () => {
    const user = userEvent.setup();
    render(<UserForm />);

    // Submit without filling
    await user.click(screen.getByRole('button', { name: /save/i }));

    // Check error messages
    expect(screen.getByText(/name is required/i)).toBeInTheDocument();
  });

  it('is accessible', () => {
    const { container } = render(<UserForm />);

    // Check for form label associations
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();

    // Check button has accessible name
    expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument();
  });
});
```

**Feedback Pattern:**
```
**Problem**: Tests query by className instead of accessible roles/labels
**Fix**: Use screen.getByRole and screen.getByLabelText
**Standard**: React Testing Library best practices (testing-library.com)
**Benefit**: Tests reflect user experience, more resilient to refactoring
```

**Red Flags:**
- Testing implementation details (state, props)
- Querying by className or data-testid (instead of roles/labels)
- Not testing accessibility
- No async testing for data fetching
- Mock hell (mocking everything)

**Official References:**
- React Testing Library: https://testing-library.com/docs/react-testing-library/intro/
- Testing Best Practices: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library

---

### 12. Security & Best Practices

**Check for:**
- [x] **XSS prevention**: Never use dangerouslySetInnerHTML unless sanitized
- [x] **HTTPS only**: API calls use HTTPS
- [x] **Auth tokens**: Store in httpOnly cookies, not localStorage
- [x] **Input sanitization**: Validate and sanitize user input
- [x] **CSP headers**: Content Security Policy configured
- [x] **Dependency audits**: npm audit regularly
- [x] **Environment variables**: API keys not in client code

**Recommended Pattern:**
```typescript
// Good: Safe HTML rendering with DOMPurify
import DOMPurify from 'dompurify';

function SafeHtmlDisplay({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em'],
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// Good: Secure API call with error handling
async function fetchUserData(userId: string): Promise<User> {
  const token = getAuthToken(); // From httpOnly cookie

  const response = await fetch(`https://api.example.com/users/${userId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }

  return response.json();
}
```

**Feedback Pattern:**
```
**Problem**: Auth token stored in localStorage, vulnerable to XSS
**Fix**: Store token in httpOnly cookie, access via secure API
**Standard**: OWASP security best practices
**Impact**: Critical security vulnerability, token can be stolen via XSS
```

**Red Flags:**
- dangerouslySetInnerHTML without sanitization
- Sensitive data in localStorage
- API keys in client-side code
- HTTP instead of HTTPS
- No input validation
- Outdated dependencies with known vulnerabilities

**Official References:**
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- React Security: https://react.dev/learn/manipulating-the-dom-with-refs#best-practices-for-dom-manipulation-with-refs

---

## Review Process Workflow

### Step 1: Gather Context
1. Identify PR number and affected components
2. Understand UX changes (screenshots, design specs)
3. Note framework versions (React, TypeScript, MUI)
4. Identify accessibility requirements

### Step 2: Verify Standards
1. Search React.dev for current patterns
2. Check TypeScript handbook for type safety
3. Review MUI documentation for component usage
4. Verify WCAG compliance for accessibility
5. Check MDN for web standards

### Step 3: Analyze Code
Review systematically through 12 focus areas:
- Accessibility (WCAG)
- Component Architecture
- TypeScript Type Safety
- Performance
- Material-UI Best Practices
- State Management
- React Hooks
- UX Patterns
- Forms & Validation
- API Integration
- Testing
- Security

### Step 4: Create Feedback File
1. Create `PR-{PRNumber}-UX-Feedback.md`
2. Categorize: [CRITICAL], [HIGH], [RECOMMEND]
3. Include official doc references
4. Add accessibility audit summary
5. List positive observations

### Step 5: Final Review
- Verify all accessibility issues flagged
- Ensure user impact clearly stated
- Check official doc references
- Validate code examples provided

---

## Quick Reference: Issue Prioritization

### [CRITICAL] (Must Fix Before Merge):
- Accessibility violations (keyboard nav, screen readers)
- Security vulnerabilities (XSS, exposed secrets)
- Performance issues causing UI freeze/crash
- Breaking changes to component APIs
- TypeScript any types in critical code

### [HIGH] (Should Fix):
- Missing loading/error states
- Poor UX patterns (no feedback, confusing flows)
- Performance issues (unnecessary renders)
- Form validation gaps
- Missing tests for critical user paths

### [RECOMMEND] (Consider):
- Component refactoring for reusability
- Additional accessibility improvements (AA → AAA)
- Performance optimizations (memoization)
- Better TypeScript types
- Additional test coverage

### [LOW] (Nice to Have):
- Minor styling improvements
- Variable naming consistency
- Additional comments
- Refactoring non-critical code

---

## UX-Specific Red Flags Checklist

**Accessibility:**
- [ ] Non-semantic HTML (div/span as buttons)
- [ ] Missing keyboard navigation
- [ ] No focus indicators
- [ ] Poor color contrast
- [ ] Missing alt text or ARIA labels

**Performance:**
- [ ] Large lists without virtualization
- [ ] No code splitting
- [ ] Unnecessary re-renders
- [ ] Expensive calculations without memoization

**User Experience:**
- [ ] No loading states
- [ ] Generic error messages
- [ ] No empty states
- [ ] Missing feedback after actions
- [ ] Confusing navigation

**Type Safety:**
- [ ] any types
- [ ] @ts-ignore comments
- [ ] Missing prop types
- [ ] Untyped API responses

**Component Quality:**
- [ ] God components (>300 lines)
- [ ] Prop drilling
- [ ] No error boundaries
- [ ] Duplicated logic

---

## Final Notes

- **Accessibility is non-negotiable** - WCAG AA minimum
- **User experience first** - Code elegance is secondary
- **Performance matters** - Every millisecond counts
- **Type safety protects users** - Catch errors before users see them
- **Test what users do** - Not implementation details
- **Reference official docs** - Don't rely on memory
- **Be constructive** - Help the team improve UX skills
- **Think mobile-first** - Responsive design by default

This skill represents UX review patterns from production React applications, updated with latest React 19, TypeScript 5, Material-UI v5, and WCAG 2.1 standards.
