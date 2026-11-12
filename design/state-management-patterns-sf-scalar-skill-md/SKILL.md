---
name: state-management-patterns
description: When deciding where and how to store data in a modern web application.
version: 2.0.0
category: frontend
tags: [frontend, state, architecture]
skill_type: architecture
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 2000
dangerous: false
requires_review: false
security_level: safe
dependencies: [react-component-design]
triggers: [state, redux, context, provider, store, hooks]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: false }
  shell: { execute: false }
input_requirements: [React application, state management code]
output_contract: [URL-driven state for filters, server cache separation, no state duplication]
failure_conditions: [attempting to manually sync server data to global store, mirroring props into state]
last_updated: 2026-05-15
---

# State Management Patterns

## Purpose
Applications suffer from bugs and performance issues when state lives in the wrong place. This skill guides teams to categorize state by its nature (UI, server, URL, global) and store it appropriately, eliminating duplication, excessive re-renders, and synchronization bugs.

## When to use
- Adding new interactive features that require data persistence across views
- Refactoring an app suffering from excessive re-renders
- Integrating external data fetching with local UI state
- Deciding where a new piece of state should live
- Migrating from Redux/global store when unnecessary

## When NOT to use
- Component-level prop decisions (use React Component Design skill)
- Server caching strategy decisions (use Caching Strategies skill)
- Real-time synchronization protocols (different concern)

## Inputs required
- Existing React application with state management code
- Understanding of current state locations (Redux, Context, useState)
- List of state mutations and their trigger sources

## Workflow
1. **Categorize State**: Classify each state piece as: UI-only, Server, URL-driven, or Truly Global
2. **URL First**: Move ALL sort, filter, pagination, search, and tab parameters to URL search params
3. **Separate Server Cache**: Use React Query / SWR / Tanstack Query for ALL server data (never Redux)
4. **Localize UI State**: Keep form inputs, modals, toggles, tooltips in component `useState` only
5. **Identify Global**: ONLY theme, auth, and language user preferences go to Context/Redux
6. **Implement Separation**: Refactor code to respect these boundaries
7. **Verify Sync**: Ensure no state is duplicated across layers

## Rules
- MUST store shareable states (filters, search, pagination) in URL, not Redux/Context
- MUST use React Query/SWR for server data, NEVER Redux
- MUST NOT manually sync server data between global store and cache layer
- MUST NOT store UI-only state (modal open, form focus) in global store
- MUST NOT mirror props into local state
- MUST NOT have duplicate copies of state

## Anti-patterns
- **Mirroring State**: `const [val, setVal] = useState(props.val)` (causes sync bugs)
- **Global Everything**: Redux store bloated with UI toggles and temporary form data
- **Manual Server Sync**: Fetching data and manually updating Redux instead of using React Query
- **URL-less Navigation**: Using only React Router state for filters/search instead of URL params
- **Inverted Cache**: Using Redux as the source of truth for server data instead of cache layer

## Failure conditions
- Attempting to manually sync server data to global store
- UI-only state (modals, toggles) stored in Redux
- State duplication across URL, cache, and store
- Search/filter parameters not reflected in URL

## Validation checklist
- [ ] All shareable states (filters, search) are in URL search params
- [ ] Server data is fetched via React Query / SWR, not Redux
- [ ] No manual synchronization between global store and cache layer
- [ ] UI-only state (modals, tooltips, focus) is in component `useState`
- [ ] Global store contains ONLY: auth, theme, language, user preferences
- [ ] No prop-value mirroring in `useState`
- [ ] URL parameters drive filtering/sorting in data display
- [ ] Back button behavior works correctly with filter/search state

## Output format
- **Code structure**: Separate imports for URL hooks, server cache hooks, and Context providers
- **File organization**: State logic in custom hooks, not component bodies
- **API shape**: URL params in component mount, server cache managed by React Query
- **Validation**: Backward-compatible URL parameter parsing with defaults

## Security considerations
- URL state MUST be validated/sanitized before use (filter injection)
- Sensitive data (auth tokens, PII) MUST NEVER be in URL
- Server cache MUST respect user permissions before caching
- Global store credentials MUST be HttpOnly/secure if stored

## Agent execution notes
- Agent MAY: Refactor state to new locations, create custom hooks for state logic, migrate Redux to React Query
- Agent MUST NEVER: Store auth tokens in URL, put sensitive PII in URL, manually sync server cache
- Agent MUST ASK: Before deleting Redux/Context entirely, before moving state to global store
- Agent MUST VALIDATE: URL state validated, no state duplication, React Query properly configured

## Example

**❌ Anti-pattern (Wrong state locations, duplication, mirroring):**
```tsx
// Redux store has everything including UI state
const store = {
  filters: { search: '', sort: 'name' },   // WRONG: belongs in URL
  users: [...],                             // OK: server data
  isModalOpen: false,                       // WRONG: UI-only state
  theme: 'dark'                             // OK: truly global
};

// Component mirrors props and stores server data locally
const UserList = ({ searchQuery }) => {
  const [search, setSearch] = useState(searchQuery);  // ANTI-PATTERN: mirrors props
  const [users, setUsers] = useState([]);              // ANTI-PATTERN: manual server sync
  
  useEffect(() => {
    fetch(`/api/users?q=${search}`)
      .then(res => res.json())
      .then(data => setUsers(data));  // Manual sync to local state
  }, [search]);
  
  return <div>{users.map(u => <p>{u.name}</p>)}</div>;
};
```

**✅ Correct pattern (Proper state separation):**
```tsx
const UserList = () => {
  // 1. URL drives state (filters/search)
  const [searchParams, setSearchParams] = useSearchParams();
  const search = searchParams.get('q') || '';
  
  // 2. Server data via React Query (cached, not Redux)
  const { data: users } = useQuery({
    queryKey: ['users', search],
    queryFn: () => fetch(`/api/users?q=${search}`).then(r => r.json())
  });
  
  // 3. UI-only state stays local
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  // 4. Global state from Context/Redux
  const { theme } = useContext(ThemeContext);
  
  return (
    <div>
      <input
        value={search}
        onChange={(e) => setSearchParams({ q: e.target.value })}
      />
      <button onClick={() => setIsModalOpen(true)}>Add User</button>
      {users?.map(u => <p>{u.name}</p>)}
    </div>
  );
};
```
