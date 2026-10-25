---
name: frontend-layer
description: >
  Frontend layer for the Gentleman-Skills project. Handles the React/TypeScript UI,
  including app shell, routing, authentication, generation streaming, and analytics dashboards.
  Owns the user-facing experience and client-side state management.
trigger: When working in `frontend/` directory — adding pages, debugging generation streams,
  or integrating auth flows in the web app.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: low
  token_estimate: 650
  dependencies: []
  related_skills: [backend-layer, build_modules-layer]
---

<!-- L1:START -->
# frontend-layer

Frontend layer for the Gentleman-Skills project. Handles the React/TypeScript UI, including app shell, routing, authentication, generation streaming, and analytics dashboards.

**Trigger**: When working in `frontend/` directory — adding pages, debugging generation streams, or integrating auth flows in the web app.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Stream generation | `useGenerationStream(generationId)` |
| Auth check | `useAuth()` |
| Start generation | `useStartGeneration(data)` |

## Critical Patterns (Summary)
- **TypeScript React Components**: Functional components with hooks; all UI components are pure functions returning JSX.
- **API Integration**: `fetchApi`, `streamGeneration`, `startGeneration` from `lib/api.ts`; auth via `AuthProvider`/`useAuth` with `VITE_API_URL` env var.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Pattern 1: TypeScript React Components

All UI components are functional components returning JSX. State is managed with React hooks (`useState`, `useQuery`, `useMutation`). Components are composed hierarchically: `App` wraps `ErrorBoundary` → `Suspense` → `LoadingSpinner`, with `Layout` and `ProtectedRoute` controlling routing and auth.

```typescript
// Example: App.tsx entry point
import { HashRouter } from 'react-router-dom';
import { ErrorBoundary } from './components/ErrorBoundary';
import { LoadingSpinner } from './components/LoadingSpinner';
import { Layout } from './components/Layout';

function App() {
  return (
    <HashRouter>
      <ErrorBoundary>
        <Suspense fallback={<LoadingSpinner />}>
          <Layout>
            {/* route children rendered here */}
          </Layout>
        </Suspense>
      </ErrorBoundary>
    </HashRouter>
  );
}
export default App;
```

### Pattern 2: Generation Streaming with useGenerationStream

Generation state is managed via `useGenerationStream` hook which tracks `StreamStatus` ('idle' | 'connecting' | 'running' | 'completed' | 'error' | 'cancelled'), `StepItem` list, and `progress`. Streaming uses SSE events from `/api/generate` endpoint. The hook provides `events`, `status`, `steps`, and `progress` for UI rendering.

```typescript
// Example: useGenerationStream hook usage
const { status, steps, progress, events } = useGenerationStream(generationId);
if (status === 'running') {
  steps.map((step) => <Step key={step.label} {...step} />);
}
```

## When to Use

- Adding a new page or view in the web app
- Debugging generation stream state or SSE event handling
- Integrating or modifying authentication flow
- Building analytics dashboards using `useAnalyticsSummary`, `useAnalyticsUsage`, `useAnalyticsModels`, `useAnalyticsRepos`

## Commands

```bash
# Start development server
cd apps/web && npm run dev

# Build for production
cd apps/web && npm run build

# Run type check
cd apps/web && npm run typecheck
```

## Anti-Patterns

### Don't: Directly fetch API without error boundaries

Directly calling `fetchApi` without wrapping in `ErrorBoundary` or handling `ApiError` types will crash the UI on network errors or auth failures. Always use `useStartGeneration`/`useCancelGeneration` mutations or wrap calls in try/catch with `ApiError` handling, and ensure `ErrorBoundary` wraps the app root to catch rendering errors from child components.

```typescript
// BAD: Unhandled fetchApi call
const data = await fetchApi('/api/generate', { method: 'POST' }); // crashes on error
```
<!-- L3:END -->