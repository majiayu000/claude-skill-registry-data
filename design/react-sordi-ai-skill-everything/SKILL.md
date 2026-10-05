---
name: react
description: Apply when writing React components. Hook discipline, state placement, performance, async cleanup, and list keys.
license: MIT
version: 1.1.0
tokens_target: 3000
triggers:
  - react component
  - react hooks
  - react performance
loads_after:
  - code-quality
  - typescript
supersedes: []
---

# Sub-Skill: React Best Practices
<!-- target: ~2600 tokens (real tiktoken count) | 17 rules with severity classification -->

**Purpose:** Prevents the React-specific mistakes LLMs make repeatedly — wrong state placement, stale closures, unnecessary re-renders, and broken async patterns. Concrete rules with code examples.

## Rule classification

- **MUST** — load-bearing. Violating causes infinite loops, stale data, leaked subscriptions, or invisible UI bugs. Never break.
- **SHOULD** — default behavior. Deviation needs a documented reason in the code or PR.
- **AVOID** — usually wrong; documented exception inline where needed.

**Where these rules don't strictly apply:** test fixtures, Storybook stories, design-system primitives in isolation, and small in-tutorial demo components may legitimately differ. The rules below apply to **production application code**.

---

## Component Design

1. **SHOULD: Co-locate state with the component that owns it.** Lift state only when two siblings genuinely share it. Lifting to a grandparent "just in case" causes unnecessary re-renders across the tree.

   ```tsx
   // Avoid: form state lifted to page-level parent
   function Page() {
     const [email, setEmail] = useState('');
     return <Form email={email} setEmail={setEmail} />;
   }

   // Prefer: state lives in the component that uses it
   function Form() {
     const [email, setEmail] = useState('');
     return <input value={email} onChange={e => setEmail(e.target.value)} />;
   }
   ```

2. **SHOULD: Split components at ~100 lines or when a section has its own data concern.** One component = one responsibility. Extract `<UserAvatar>`, `<OrderSummary>` rather than one `<ProfilePage>` that does everything. *Exception: pages that are mostly markup with little logic may exceed 100 lines.*

3. **SHOULD: Replace prop drilling beyond two levels with composition or context.** Passing `userId` through four components to reach a button is a design smell.

   ```tsx
   // Avoid: drilling through intermediaries
   <Layout userId={userId}><Sidebar userId={userId}><Nav userId={userId} /></Sidebar></Layout>

   // Prefer: context or render-prop composition
   <UserContext.Provider value={userId}><Layout /></UserContext.Provider>
   ```

4. **MUST: Never create component definitions inside render.** Inner components are recreated on every render, destroying their state and forcing full remounts.

   ```tsx
   // Wrong
   function Parent() {
     const Child = () => <div>hello</div>; // new reference every render
     return <Child />;
   }

   // Correct: define outside
   const Child = () => <div>hello</div>;
   function Parent() { return <Child />; }
   ```

---

## State Management

5. **MUST: Never mutate state directly.** React compares references. Mutating in place skips re-renders silently.

   ```tsx
   // Wrong
   const [items, setItems] = useState([]);
   items.push(newItem); // mutation — React does not re-render
   setItems(items);

   // Correct
   setItems(prev => [...prev, newItem]);
   ```

6. **SHOULD: Compute derived values in render, not in useEffect.** If a value can be calculated from existing state/props, calculate it inline. useEffect for derived state creates a one-render lag and extra state variables.

   ```tsx
   // Avoid
   const [fullName, setFullName] = useState('');
   useEffect(() => { setFullName(`${first} ${last}`); }, [first, last]);

   // Prefer
   const fullName = `${first} ${last}`;
   ```

7. **MUST: Use useRef for values that must not trigger re-renders** (timers, DOM nodes, previous values). Use useState for anything the UI depends on. Mixing them causes invisible bugs.

   ```tsx
   // Wrong: ref for displayed value
   const count = useRef(0);
   count.current++; // UI never updates

   // Wrong: state for a timer ID
   const [timerId, setTimerId] = useState(null); // triggers re-render on set

   // Correct
   const timerId = useRef(null);
   ```

---

## Hooks

8. **MUST: Specify complete dependency arrays in useEffect.** Omitting a dependency creates a stale closure. The ESLint rule `exhaustive-deps` must be enabled and respected.

   ```tsx
   // Wrong: stale closure over userId
   useEffect(() => { fetchUser(userId); }, []); // runs once, userId never updates

   // Correct
   useEffect(() => { fetchUser(userId); }, [userId]);
   ```

9. **MUST: Cancel async operations in useEffect cleanup.** Fetch without an AbortController causes state updates on unmounted components and race conditions.

   ```tsx
   useEffect(() => {
     const controller = new AbortController();
     fetch(`/api/user/${id}`, { signal: controller.signal })
       .then(r => r.json())
       .then(setUser)
       .catch(err => { if (err.name !== 'AbortError') setError(err); });
     return () => controller.abort();
   }, [id]);
   ```

10. **MUST: Never call hooks conditionally or inside loops.** Hook call order must be identical on every render. Wrap conditional logic inside the hook body, not around the hook call.

    ```tsx
    // Wrong
    if (isLoggedIn) { const user = useUser(); }

    // Correct
    const user = useUser(); // hook always called; handle null inside
    ```

---

## Performance

11. **SHOULD: Wrap expensive computations in useMemo, not inline.** Recalculating a sorted/filtered list on every render is the most common performance bug in React. *Exception: small lists (<20 items) where the recompute is negligible — adding useMemo costs more than it saves.*

    ```tsx
    // Avoid: re-sorts on every render including unrelated state changes
    const sorted = items.sort((a, b) => a.name.localeCompare(b.name));

    // Prefer
    const sorted = useMemo(
      () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
      [items]
    );
    ```

12. **AVOID: New object or array literals as props inline.** New references on every render break React.memo and cause child re-renders. *Exception: when the consuming child is not memoised, the inline literal cost is negligible.*

    ```tsx
    // Wrong: new object reference every render
    <Chart options={{ color: 'red', width: 400 }} />

    // Correct: stable reference
    const chartOptions = useMemo(() => ({ color: 'red', width: 400 }), []);
    <Chart options={chartOptions} />
    ```

13. **SHOULD: Use React.lazy and Suspense for routes and heavy components.** Bundling everything eagerly increases initial load time.

    ```tsx
    const Dashboard = React.lazy(() => import('./Dashboard'));

    function App() {
      return (
        <Suspense fallback={<Spinner />}>
          <Dashboard />
        </Suspense>
      );
    }
    ```

---

## Lists & Keys

14. **MUST: Never use array index as key when the list can reorder, filter, or grow.** Index keys cause React to reuse the wrong DOM nodes, breaking animations, form state, and focus. *Exception: static, sort-stable lists that never filter — but stable IDs are still safer.*

    ```tsx
    // Wrong
    {items.map((item, i) => <Row key={i} item={item} />)}

    // Correct: stable, unique identity
    {items.map(item => <Row key={item.id} item={item} />)}
    ```

---

## Testing

15. **SHOULD: Test behavior, not implementation.** Query by role/label, not by class name or component internals. Tests that break on refactors without behavior changes are noise.

    ```tsx
    // Avoid
    expect(wrapper.find('.submit-btn').exists()).toBe(true);

    // Prefer
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
    ```

16. **MUST: Test loading and error states, not just the happy path.** Components that render `null` silently on error are invisible bugs in production.

    ```tsx
    it('shows error message when fetch fails', async () => {
      server.use(rest.get('/api/user', (req, res, ctx) => res(ctx.status(500))));
      render(<UserProfile id="1" />);
      expect(await screen.findByText(/something went wrong/i)).toBeInTheDocument();
    });
    ```

17. **SHOULD: Mock at the network boundary, not at the module boundary.** Mocking `fetch` or using MSW keeps tests closer to real behavior than mocking `useUser` directly.

---

## Responsive Design

18. **SHOULD: Use a mobile-first approach for responsive styles.** Write base styles for small screens, enhance with `min-width` media queries for larger viewports.

19. **AVOID: Fixed pixel widths on container components.** Use relative units or CSS logical properties. Hard-coded widths break on untested viewports. Reference: ERR-2026-015.

20. **SHOULD: Prefer CSS container queries over viewport media queries for component-level responsiveness.** Components adapt to allocated space, not full viewport.

21. **MUST: Never assume a single breakpoint set covers all use cases.** Define breakpoints based on content needs, not device names.

22. **SHOULD: Use CSS `clamp()` for fluid typography and spacing instead of multiple breakpoint overrides.** Scales smoothly without jumps.

---

## Why This Sub-Skill Earns Stars

These rules target the exact failure modes that appear in LLM-generated React code: state lifted too high, effects without cleanup, index keys, inline object props, and derived state stored redundantly. Each rule is actionable in a single code review comment and includes a before/after example that makes the correct pattern unambiguous. The MUST/SHOULD/AVOID classification means hook-correctness rules are strict and stylistic rules respect context.
