---
name: admin-debug-context
description: "Admin debug system wiring for the floating AdminIndicator's live debug data and Copy Full Context. Use when adding debug visibility to a route or feature, wiring useDebugContext or the debug panel, capturing console errors, or enabling the copy-context workflow for a page."
---

# Admin Debug Context

## Performance guarantee

The entire debug system is **zero cost for non-admins**:
- `AdminIndicatorWrapper` checks `selectIsAdmin` from Redux and returns `null` immediately if false
- Both `AdminIndicatorIsland` (ssr layout) and `DynamicAdminIndicatorWrapper` (authenticated layout) use `dynamic(..., { ssr: false })` — the admin bundle never downloads for non-admins
- `useDebugContext` is a no-op when `isAdmin` is false — no dispatch, no effect, no render cost

---

## Architecture — four layers

```
Layout (server)
  └── AdminIndicatorWrapper (client, admin-only)
        ├── AdminDebugContextCollector   ← auto: pathname, searchParams, viewport,
        │                                        console errors, unhandledrejection
        └── AdminIndicator (Small/Medium/Large)
              ├── MediumIndicator
              │     └── debugModules icons → DebugModulePanel modal
              └── LargeIndicator
                    ├── API config + health grid
                    ├── Recent API calls log
                    ├── [Copy Full Context] button ← assembles everything for AI agent
                    ├── Console Errors panel        ← captured automatically
                    └── Debug Data (JSON)           ← written via useDebugContext
```

---

## What is auto-captured (no route work needed)

`AdminDebugContextCollector` runs at layout level inside `AdminIndicatorWrapper`. For every admin session it automatically captures:

| Data | How |
|---|---|
| Current pathname | `usePathname()` on every navigation |
| Search params | `useSearchParams()` on every navigation |
| Browser viewport | `window.innerWidth/Height` |
| User agent | `navigator.userAgent` |
| Navigation count | increments on each pathname change |
| `console.error` calls | patches `console.error` while mounted |
| `unhandledrejection` events | `window.addEventListener` |
| `window.error` events | `window.addEventListener` |

This is available instantly in the "Copy Full Context" snapshot even for routes that add zero custom debug code.

---

## Adding route/feature debug data

### The hook — use this everywhere

```tsx
import { useDebugContext } from '@/hooks/useDebugContext';

export default function MyComponent({ sessionId }: { sessionId: string }) {
    const session = useAppSelector(s => selectSession(s, sessionId));
    const { publish, isActive } = useDebugContext('Chat');  // namespace

    useEffect(() => {
        publish({
            'Session ID': sessionId,
            'Status': session?.status,
            'Message Count': session?.messages.length,
            'Conversation ID': session?.conversationId,
        });
    }, [isActive, session?.status, session?.messages.length, sessionId]);
}
```

**Key rules:**
- First arg is the **namespace** — appears as group header in the debug panel
- Keys are auto-prefixed: `"Chat:Session ID"`, `"Chat:Status"`, etc.
- `isActive` is `true` only when `isAdmin && isDebugMode` — use it in `useEffect` deps to gate expensive collection
- The hook **auto-clears all namespace keys on unmount** — no manual cleanup needed
- Safe in any component tree — pure no-op for non-admins

### Hook API

```ts
const { publish, publishKey, isActive } = useDebugContext('Namespace');

publish({ 'Key': value, 'Other Key': otherValue });  // merge namespaced data
publishKey('Key', value);                             // set single key
isActive  // boolean — true only when admin AND debug mode is on
```

---

## Adding a debug module panel

For richer feature-specific UIs (not just JSON data), create a debug module:

### Step 1 — Create the component

```tsx
// components/admin/debug/MyFeatureDebug.tsx
'use client';
import { useAppSelector } from '@/lib/redux/hooks';

export default function MyFeatureDebug() {
    // Read exclusively from Redux selectors — no local fetch, no useState for data
    const data = useAppSelector(selectSomething);
    return <div className="p-4 text-xs font-mono">{JSON.stringify(data, null, 2)}</div>;
}
```

### Step 2 — Register in the registry

```tsx
// components/admin/debug/debugModuleRegistry.tsx
import MyFeatureDebug from './MyFeatureDebug';
import { Zap } from 'lucide-react';

export const debugModules: DebugModule[] = [
    // ... existing modules ...
    {
        id: 'my-feature',
        name: 'My Feature',
        icon: Zap,
        component: MyFeatureDebug,
        description: 'Live state of my feature',
        color: 'text-purple-400',
    },
];
```

The icon appears in the MediumIndicator debug row. Clicking opens the panel modal. Component only mounts when the panel is open — zero overhead when closed.

---

## Copy Full Context — the AI agent workflow

The **Copy** button in LargeIndicator assembles a complete markdown snapshot:

```markdown
# Admin Debug Context Snapshot
Generated: 2026-03-27T10:42:00.000Z
Admin: admin@example.com

## Route
- **Path:** /demos/chat/c/abc-123
- **Viewport:** 1440×900
- **Render Count:** 3

## API Config
- **Active Server:** localhost
- **Backend URL:** http://localhost:8000
- **Health:** healthy (42ms)

## Feature Debug Data
### Chat
- **Session ID:** sess-xyz
- **Status:** streaming
- **Message Count:** 7

## Recent API Calls
| Status | Method | Path | HTTP | Duration |
...

## Console Errors
No errors captured.
```

**Workflow:** Admin sees a bug → opens LargeIndicator → clicks Copy → pastes into AI agent chat. Agent gets full context: what page, what state, what the API is doing, any errors.

---

## Data sources reference

| What | Selector | Slice |
|---|---|---|
| Is admin | `selectIsAdmin` | `userSlice` |
| Debug mode on | `selectIsDebugMode` | `adminDebugSlice` |
| Route context | `selectRouteContext` | `adminDebugSlice` |
| Console errors | `selectConsoleErrors` | `adminDebugSlice` |
| Debug data (JSON) | `selectDebugData` | `adminDebugSlice` |
| Active server | `selectActiveServer` | `apiConfigSlice` |
| Backend URL | `selectResolvedBaseUrl` | `apiConfigSlice` |
| Server health | `selectActiveServerHealth` | `apiConfigSlice` |
| Recent API calls | `selectRecentApiCalls` | `apiConfigSlice` |
| Active chat session | `selectActiveChatSessionId` | `activeChatSlice` |
| Chat session object | `selectSession(state, sessionId)` | `chatConversations` |
| Chat messages | `selectMessages(state, sessionId)` | `chatConversations` |

---

## Viewing debug context

1. **Small indicator** — two colored dots (server env, health)
2. **Medium indicator** — debug icon row; click any icon for that feature's panel
3. **Large indicator** — full admin dashboard:
   - **Copy** button (always visible) — one click to copy everything for an AI agent
   - **Console Errors** panel — auto-captured, collapsible, shows stack traces
   - **Debug Data** section (debug mode on) — namespaced JSON from `useDebugContext`
   - **API calls log** and **all environments health grid**

Enable debug mode: click the **Debug** toggle in MediumIndicator or LargeIndicator.
