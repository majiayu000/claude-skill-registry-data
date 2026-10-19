---
name: react-performance
description: >
  Diagnose and fix React rendering, bundle, and data-loading performance using
  measurement first (React DevTools Profiler, Chrome Performance panel, bundle analysis)
  and modern React idioms (Suspense, transitions; React Compiler; and the React 19 features use(), Actions, useActionState, useOptimistic). Use when
  a React UI feels slow, INP/LCP regress, re-renders are excessive, lists lag, bundles
  are large, or someone proposes useMemo/useCallback/React.memo without evidence. Do not
  use for generic JS profiling outside React (use performance-profiling), CSS layout
  issues (web-html-css), or component API design (react-composition-patterns).
compatibility: >
  React 18.3+/19 applications (Vite, Next.js, or similar) and a Chromium browser with
  DevTools; examples are TypeScript/TSX.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "react, performance, profiler, react-compiler, suspense, memoization, core-web-vitals, bundle"
  topics: "frontend, performance, react"
---

# React Performance

Fix what you measured, not what you suspect. Most React slowness comes from a few causes: work done at the wrong time (large renders on every keystroke), too much JavaScript shipped, and serial data waterfalls. Memoization is a tool for one of those causes, not a default.

Related skills: `performance-profiling` (language-agnostic profiling method), `react-composition-patterns` (restructuring components, which often removes re-render problems for free), `browser-debugging` (DevTools mechanics), `typescript-development`, `web-html-css`.

## When to use / not use

Use for: slow interactions (typing, filtering, tab switches), slow first load, janky scroll in long lists, large bundles, unexpected re-render counts, reviewing a PR that adds memoization.

Do not use for: server-side latency with no React involvement, database tuning, pure CSS paint problems, or "make it faster" with no symptom (ask for the symptom and a repro first).

## Non-negotiable rules

1. **Measure before and after.** Record the baseline (Profiler commit time, INP in the Performance panel, bundle size) and the same measurement after the change. No number, no claim.
2. **Profile a production-like build.** Development builds run StrictMode double renders and extra checks, so they overstate cost. Use a production build with profiling enabled (framework docs describe how), or compare relative changes only.
3. **Do not add `useMemo`/`useCallback`/`React.memo` speculatively.** If React Compiler covers the code, hand-written memoization is mostly redundant; otherwise add it only where the Profiler shows a costly, avoidable render and the props are actually stable.
4. **Keep semantics.** Never trade correctness (stale closures, missing effect deps) for speed. Do not silence `react-hooks/exhaustive-deps` to make memoization "work".
5. **Do not share traces containing secrets or real user data**; profiles can contain URLs and payloads.

## Workflow

### 1. Classify the symptom

| Symptom | Likely class | First tool |
|---|---|---|
| Typing/clicking feels laggy | Expensive or over-broad re-render on interaction | React DevTools Profiler + Performance panel (INP) |
| Slow first paint / LCP | Bundle size, waterfalls, large images | Network panel, Lighthouse, bundle analyzer |
| Scroll jank in a long list | Too many DOM nodes | Performance panel, element count |
| Memory grows over time | Leaks (listeners, timers, caches) | Memory panel heap snapshots |
| Layout jumps | CLS: unsized images, late-injected content | Performance panel layout shifts |

### 2. Reproduce and record

In the React DevTools Profiler: start recording, perform the single slow interaction, stop. Inspect the ranked/flame view for components with large self time and for components that rendered although nothing relevant changed (enable "record why each component rendered" in profiler settings). Cross-check with the browser Performance panel to see whether the time is in React render, in your handlers, or in layout/paint. Throttle the CPU to approximate real devices.

### 3. Pick the fix by cause

**A. State lives too high, so unrelated subtrees re-render.** Move state down to the component that uses it, or pass the expensive static subtree as `children`. This usually beats memoizing.

```tsx
// Before: every keystroke re-renders <ExpensiveTree />
function Page() {
  const [q, setQ] = useState("");
  return (
    <>
      <input value={q} onChange={(e) => setQ(e.target.value)} />
      <ExpensiveTree />
    </>
  );
}

// After: state isolated in the component that needs it
function SearchBox() {
  const [q, setQ] = useState("");
  return <input value={q} onChange={(e) => setQ(e.target.value)} />;
}
function Page() {
  return (
    <>
      <SearchBox />
      <ExpensiveTree />
    </>
  );
}
```

**B. Expensive render caused by user input (filtering a big list).** Keep the input urgent and defer the heavy part: `useDeferredValue(query)` for the derived rendering, or wrap the state update that triggers the heavy render in `startTransition`. These keep typing responsive but do not reduce total work; if the work itself is wasteful, fix the algorithm or virtualize.

**C. Long lists.** Virtualize (render only visible rows) with a maintained library such as TanStack Virtual or react-window; use stable keys (ids, not array index, for reorderable data).

**D. Derived data.** Compute during render if cheap. Do not mirror props into state with an effect (`useEffect` + `setState` forces an extra render). If a calculation is measurably expensive and the compiler is not handling it, use `useMemo` with correct deps.

**E. Memoization and React Compiler.** React Compiler is a build-time plugin (`babel-plugin-react-compiler`) that auto-memoizes components and hooks that follow the Rules of React. Adopt incrementally: `compilationMode: 'annotation'` with `"use memo"` per function, or `infer`. Keep components pure. Use `"use no memo"` only as a temporary, commented escape hatch. Keep existing `useMemo`/`useCallback` where they define effect-dependency identity. Use the React Hooks lint rules to find code the compiler will skip (which compiler-related rules exist depends on the installed `eslint-plugin-react-hooks` version, so check its docs), and confirm in React DevTools that components are compiled. Check the installed compiler version and its docs; behavior evolves.

**F. Data loading waterfalls.** Fetch in parallel at the route/loader level instead of in nested components after render. In React 19 (not available in 18), `use(promise)` reads a promise during render and suspends, but the promise must come from a cache or framework: a promise created inside render is unsupported. Prefer your framework's data APIs or a query library with caching. Wrap slow sections in `<Suspense fallback>` so the shell paints first.

**G. Bundle size.** Run a bundle visualizer (Vite: `rollup-plugin-visualizer`; webpack: `webpack-bundle-analyzer`; Next.js: `@next/bundle-analyzer`). Fix in order: remove unused dependencies; import specific modules when tree-shaking fails on barrels; `React.lazy` + `<Suspense>` for routes and rarely used heavy widgets (editors, charts, maps); replace heavy libraries with lighter ones.

**H. Forms and mutations (React 19).** Use Actions with `useActionState` (React 19) and `useOptimistic` (React 19) for pending and optimistic UI instead of hand-rolled loading state plus effect chains. Optimistic state reverts automatically when the action fails.

**I. Effects.** Effects that fetch, subscribe, or derive state cause extra renders and races. Remove effects that only transform data; clean up subscriptions and abort fetches with `AbortController`.

### 4. Verify

Repeat the exact recording from step 2 and record before/after numbers. Check behavior is unchanged (tests, manual path), including with StrictMode on.

## Worked example

Symptom: filtering a 5,000-row table lags on each keystroke (INP around 450 ms in the Performance panel).

1. Profiler: the `<Table>` commit takes about 300 ms per keystroke; every `<Row>` renders.
2. Cause: filter state in `Page`, all rows rendered unconditionally, and `Row` receives a fresh inline object every render.
3. Fix in order of leverage: (a) virtualize rows so about 30 render; (b) `useDeferredValue(query)` for the filtered list so typing stays urgent; (c) only then consider `memo(Row)` with stable props.
4. Re-record: commit time drops sharply; INP is under 200 ms (the "good" threshold at the 75th percentile of field data).
5. Report before/after numbers, the change list, and that field data should confirm after release (lab numbers are only a proxy).

## Anti-patterns

- Wrapping everything in `useMemo`/`useCallback` "just in case" (adds cost, hides causes).
- `memo()` on a component whose props include fresh object/array/function literals each render (never skips).
- Array index as key in a reorderable list.
- Syncing props to state through effects.
- Measuring in the dev build and shipping conclusions.
- Fetching in effects in nested components, creating waterfalls.
- Creating a promise inside render and passing it to `use()`.
- A context holding a fast-changing value consumed by many components (split the context or move the state).

## Verification checklist

- [ ] Symptom reproduced with steps and a baseline number recorded
- [ ] Cause identified with Profiler/Performance evidence
- [ ] Fix addresses the cause (structure first, memoization last)
- [ ] After-number recorded with the same method; improvement stated honestly
- [ ] No lint suppressions added for hooks rules; tests pass
- [ ] Bundle changes verified with analyzer output where relevant

## References

- [Metrics, tools, and thresholds](references/measurement.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
