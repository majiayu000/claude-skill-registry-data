---
name: implementing-code-splitting
description: Teaches code splitting with lazy() and Suspense in React 19 for reducing initial bundle size. Use when implementing lazy loading, route-based splitting, or optimizing performance.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Code Splitting with lazy() and Suspense

## Basic Pattern

```javascript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

## Route-Based Splitting

```javascript
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

## Component-Based Splitting

```javascript
import { lazy, Suspense, useState } from 'react';

const Chart = lazy(() => import('./Chart'));
const Table = lazy(() => import('./Table'));

function DataView() {
  const [view, setView] = useState('chart');

  return (
    <>
      <button onClick={() => setView('chart')}>Chart</button>
      <button onClick={() => setView('table')}>Table</button>

      <Suspense fallback={<Spinner />}>
        {view === 'chart' ? <Chart /> : <Table />}
      </Suspense>
    </>
  );
}
```

## Named Exports

```javascript
const { BarChart } = await import('./Charts');

export const BarChart = lazy(() =>
  import('./Charts').then(module => ({ default: module.BarChart }))
);
```

For comprehensive code splitting patterns, see: `research/react-19-comprehensive.md` lines 1224-1238.
