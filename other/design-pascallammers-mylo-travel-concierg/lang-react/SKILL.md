---
name: lang-react
description: Build React SPAs where components are declarative UI consuming external state (Zustand/XState/TanStack Query). Logic lives in stores, not components.
---

# React Expert

## Core Philosophy

Components consume external state, contain no logic:

- External hooks at top (Zustand, XState, TanStack Query)
- No useState/useReducer/useEffect for complex logic
- Inline actions unless repeated 2+ times
- Test stores/machines (unit tests), not components (E2E only)

## State Management Stack

| State Type            | Solution                     |
| --------------------- | ---------------------------- |
| **Remote (REST)**     | TanStack Query               |
| **Remote (GraphQL)**  | Apollo Client                |
| **Application state** | Zustand                      |
| **Complex machines**  | XState                       |
| **Local UI state**    | useState (rare, last resort) |

## Component Pattern

```typescript
// ✅ External hooks → Early returns → JSX
function UserProfile({ userId }: { userId: string }) {
  const { user, isLoading } = useUser(userId);
  const { updateProfile } = useUserActions();

  if (isLoading) return <Spinner />;

  return (
    <div>
      <h1>{user.name}</h1>
      <button onClick={() => updateProfile({ email: 'new@example.com' })}>
        Update
      </button>
    </div>
  );
}
```

## Testing: Stores, Not Components

| What            | Tool       | Why                       |
| --------------- | ---------- | ------------------------- |
| Zustand stores  | Vitest     | Test without React        |
| XState machines | Vitest     | Deterministic transitions |
| Critical flows  | Playwright | Real browser              |
| Components      | Never      | Logic should be in stores |

```typescript
// Test store directly
const { login } = useAuthStore.getState();
await login({ email: "test@example.com", password: "pass" });
expect(useAuthStore.getState().user).toBeDefined();
```

## Unique Patterns

### Prop Ordering: Simple → Complex

```tsx
<Table
  data={items}
  loading={isLoading}
  sortable
  onSort={handleSort}
  renderRow={(item) => <Row>{item.name}</Row>}
/>
```

### Inline Props for Type Inference

```tsx
// ✅ Inline - TypeScript infers types
<SearchableList
  items={budgets}
  renderItem={(budget) => <Card name={budget.name} />}
/>;

// ❌ Extract only if repeated 2+ times
const renderItem = (budget: Budget) => <Card name={budget.name} />;
```

### Pattern Matching for Variants

```tsx
import { match } from "ts-pattern";

{
  match(state)
    .with({ _tag: "loading" }, () => <Spinner />)
    .with({ _tag: "success" }, (s) => <Data value={s.data} />)
    .exhaustive();
}
```

### Performance: Profile First

| Technique      | When                |
| -------------- | ------------------- |
| useMemo        | Profiled as slow    |
| useCallback    | Repeated 2+ times   |
| React.memo     | Props rarely change |
| Code splitting | Route-level         |

### Styled-Components: Consolidate with CSS Selectors

```typescript
// ✅ Single component with CSS selectors
const Table = styled.table`
  thead {
    background: ${(p) => p.theme.colors.header};
  }
  tbody tr:hover {
    background: ${(p) => p.theme.colors.hover};
  }
  td {
    padding: ${(p) => p.theme.space.md};
  }
`;

// ❌ Separate components for each element
const TableHeader = styled.thead`...`;
const TableRow = styled.tr`...`;
const TableCell = styled.td`...`;
```

## Version 1.0.1
