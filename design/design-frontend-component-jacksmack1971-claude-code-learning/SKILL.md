---
name: design-frontend-component
description: "Use when creating React/Vue components or adding UI features. Enforces composition patterns and state management best practices."
author: "Claude Code Learning Flywheel Team"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
version: 1.0.0
last_verified: "2026-01-01"
tags: ["frontend", "react", "vue", "components", "ui", "composition"]
related-skills: ["test-driven-workflow", "refactor-legacy-code"]
---

# Skill: Design Frontend Component

## Purpose
Prevent "Prop Drilling Hell" and monolithic components. Enforce composition patterns, proper state management, and the Atomic Design methodology to create maintainable, testable UI components.

## 1. Negative Knowledge (Anti-Patterns)

| Failure Pattern | Context | Why It Fails |
| :--- | :--- | :--- |
| Prop Drilling | Passing data through 5+ layers | Tight coupling, hard to refactor |
| God Components | Files >300 lines with mixed concerns | Untestable, unmaintainable |
| Inline Styles | Hardcoded hex values and dimensions | Inconsistent design, no theming |
| Direct DOM Manipulation | `document.getElementById` in React/Vue | Breaks framework reactivity |
| Business Logic in Components | API calls and validation in render | Hard to test, violates SRP |
| Missing Key Props | List items without unique keys | Performance issues, bugs |
| Mutating Props | Changing props directly | Breaks one-way data flow |
| Excessive State | Everything in component state | Performance issues, complex logic |

## 2. Verified Component Design Procedure

### The Atomic Design Hierarchy

```
ATOMS       → Smallest units (Button, Input, Label)
  ↓
MOLECULES   → Simple groups (SearchBar = Input + Button)
  ↓
ORGANISMS   → Complex sections (Header = Logo + Nav + SearchBar)
  ↓
TEMPLATES   → Page layouts (wireframes)
  ↓
PAGES       → Actual instances with real data
```

### Phase 1: Component Planning

**Before writing code, answer these questions:**

1. **What is the single responsibility of this component?**
   - ❌ "It handles the user profile, settings, and notifications"
   - ✅ "It displays user profile information"

2. **What category is it? (Atom, Molecule, Organism)**
   - Atom: Basic building block (Button, Input, Icon)
   - Molecule: Combination of atoms (Form field with label and error)
   - Organism: Complex UI section (Navigation bar, Product card)

3. **What data does it need?**
   - Props (from parent)
   - Local state (UI-only)
   - Global state (context/store)

4. **What actions can users take?**
   - Events to emit/handle
   - Side effects (API calls, navigation)

### Phase 2: Component Structure

**File organization:**

```
components/
├── atoms/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx
│   │   ├── Button.stories.tsx  (Storybook)
│   │   └── index.ts
│   └── Input/
│       ├── Input.tsx
│       └── ...
├── molecules/
│   └── SearchBar/
│       ├── SearchBar.tsx
│       └── ...
└── organisms/
    └── Header/
        ├── Header.tsx
        └── ...
```

**Component template:**

```typescript
// components/atoms/Button/Button.tsx
import { ReactNode } from 'react';
import styles from './Button.module.css';

export interface ButtonProps {
  /** The button's content */
  children: ReactNode;
  /** Visual variant */
  variant?: 'primary' | 'secondary' | 'danger';
  /** Size of the button */
  size?: 'small' | 'medium' | 'large';
  /** Disabled state */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Additional CSS classes */
  className?: string;
}

export function Button({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
  className = '',
}: ButtonProps) {
  return (
    <button
      className={`${styles.button} ${styles[variant]} ${styles[size]} ${className}`}
      disabled={disabled}
      onClick={onClick}
      type="button"
    >
      {children}
    </button>
  );
}
```

### Phase 3: Props Design

**Principles:**

1. **Keep props flat and simple**
   ```typescript
   // ❌ BAD: Nested props
   interface BadProps {
     user: {
       profile: {
         personal: {
           name: string;
         }
       }
     }
   }

   // ✅ GOOD: Flat props
   interface GoodProps {
     userName: string;
     userEmail: string;
     userAvatar: string;
   }
   ```

2. **Use discriminated unions for variants**
   ```typescript
   // ✅ Type-safe variants
   type ButtonProps =
     | { variant: 'link'; href: string }
     | { variant: 'button'; onClick: () => void };
   ```

3. **Provide sensible defaults**
   ```typescript
   function Card({
     variant = 'outlined',  // Default value
     elevation = 1,
     padding = 'medium'
   }: CardProps) {
     // ...
   }
   ```

### Phase 4: State Management

**Decision tree for state location:**

```
Is it server data (API)?
├─ YES → Use React Query / SWR / TanStack Query
└─ NO → Continue

Does more than one component need it?
├─ YES → Use Context / Redux / Zustand
└─ NO → Continue

Is it just UI state (open/closed, hover)?
├─ YES → Use local useState
└─ NO → Reconsider if state is needed
```

**Example: Proper state management**

```typescript
// ❌ BAD: Everything in component state
function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);  // UI state
  const [theme, setTheme] = useState('light');         // Global state

  useEffect(() => {
    setLoading(true);
    fetch('/api/user')
      .then(res => res.json())
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  // ... rest of component
}

// ✅ GOOD: Separate concerns
function UserProfile() {
  // Server state (React Query)
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user'],
    queryFn: fetchUser
  });

  // Global state (Context)
  const { theme } = useTheme();

  // Local UI state
  const [isEditing, setIsEditing] = useState(false);

  // ... rest of component
}
```

### Phase 5: Composition Over Prop Drilling

**Avoid prop drilling:**

```typescript
// ❌ BAD: Prop drilling
function App() {
  const user = useUser();
  return <Dashboard user={user} />;
}

function Dashboard({ user }) {
  return <Sidebar user={user} />;
}

function Sidebar({ user }) {
  return <UserMenu user={user} />;
}

function UserMenu({ user }) {
  return <div>{user.name}</div>;
}

// ✅ GOOD: Use context for deeply nested data
const UserContext = createContext<User | null>(null);

function App() {
  const user = useUser();
  return (
    <UserContext.Provider value={user}>
      <Dashboard />
    </UserContext.Provider>
  );
}

function UserMenu() {
  const user = useContext(UserContext);
  return <div>{user.name}</div>;
}
```

**Composition patterns:**

```typescript
// ✅ Render props pattern
function DataFetcher({ url, children }) {
  const { data, loading } = useFetch(url);
  return children({ data, loading });
}

<DataFetcher url="/api/users">
  {({ data, loading }) => loading ? <Spinner /> : <UserList users={data} />}
</DataFetcher>

// ✅ Compound components pattern
function Tabs({ children }) {
  const [activeTab, setActiveTab] = useState(0);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

Tabs.List = function TabsList({ children }) { /* ... */ };
Tabs.Tab = function Tab({ children, index }) { /* ... */ };
Tabs.Panel = function TabPanel({ children, index }) { /* ... */ };

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab index={0}>Profile</Tabs.Tab>
    <Tabs.Tab index={1}>Settings</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel index={0}><ProfileContent /></Tabs.Panel>
  <Tabs.Panel index={1}><SettingsContent /></Tabs.Panel>
</Tabs>
```

### Phase 6: Performance Optimization

**Only optimize when needed, but follow these patterns:**

```typescript
// ✅ Memoize expensive calculations
function ProductList({ products, filters }) {
  const filteredProducts = useMemo(() => {
    return products.filter(p => matchesFilters(p, filters));
  }, [products, filters]);

  return <div>{filteredProducts.map(p => <ProductCard key={p.id} {...p} />)}</div>;
}

// ✅ Memoize callbacks passed to children
function ParentComponent() {
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);

  return <ChildComponent onClick={handleClick} />;
}

// ✅ Memoize components that render often
const ExpensiveComponent = memo(function ExpensiveComponent({ data }) {
  // Complex rendering logic
  return <div>{/* ... */}</div>;
});

// ❌ DON'T memoize everything (premature optimization)
const SimpleComponent = memo(function SimpleComponent({ text }) {
  return <div>{text}</div>;  // Too simple to benefit from memo
});
```

## 3. Extended Patterns and Examples

**For detailed code examples, see [reference.md](./reference.md):**

- **Component Design Patterns**: Container/Presenter, Custom Hooks, Error Boundaries
- **Styling Best Practices**: CSS Modules, Styled Components, Design Tokens
- **Testing Patterns**: Behavior-driven testing with Testing Library
- **Advanced Patterns**: HOCs, Slots, Reducers, Accessibility, Performance

**Quick reference summary:**

| Pattern | Use Case | See Reference |
| :--- | :--- | :--- |
| Container/Presenter | Separate logic from UI | reference.md §1 |
| Custom Hooks | Extract reusable logic | reference.md §2 |
| Error Boundaries | Graceful error handling | reference.md §3 |
| CSS Modules | Scoped styling | reference.md §Styling |
| Testing Library | User behavior tests | reference.md §Testing |

## 4. Failed Attempts (Negative Knowledge Evolution)

| Attempt | Context | Learning |
| :--- | :--- | :--- |
| Premature abstraction | Created reusable component after first use | Wait for 3 instances before abstracting |
| Global state for everything | Put all state in Redux store | Use local state by default, global only when needed |
| Index as key in lists | Used array index as React key | Always use unique, stable IDs as keys |
| Fetching data in components | Used useEffect for API calls | Use React Query/SWR for server state |

## 5. Component Design Checklist

Before committing: Single Responsibility ✓ | Size <300 lines ✓ | Props Typed ✓ | No Prop Drilling ✓ | Accessible ✓ | Tested ✓ | Documented ✓ | Styled with tokens ✓ | Unique keys in lists ✓

## 6. Governance
- **Token Budget:** ~390 lines (within 400 recommended limit)
- **Extended Reference:** See reference.md for detailed patterns and examples
- **Dependencies:** React 18+, TypeScript 5+, Testing Library
- **Pattern Origin:** Atomic Design (Brad Frost), React Best Practices
- **Verification Date:** 2026-01-01
