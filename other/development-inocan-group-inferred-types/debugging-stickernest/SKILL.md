---
name: debugging-stickernest
description: Debugging and troubleshooting StickerNest issues. Use when investigating bugs, tracing errors, understanding unexpected behavior, adding debug logging, or when the user says "it's not working", "debug this", or "why is X happening". Covers console patterns, Three.js debugging, React DevTools, network issues, and common gotchas.
---

# Debugging StickerNest

This skill provides patterns and techniques for debugging StickerNest's complex multi-layer architecture (React + Zustand + Three.js + WebXR + iframes).

## Console Logging Convention

StickerNest uses bracketed prefixes for organized logging:

```typescript
// Pattern: [ComponentName] message
console.log('[SpatialWidget] Rendering widget:', widget.id);
console.warn('[Auth] Token expired, refreshing...');
console.error('[Pipeline] Failed to execute:', error);

// With data
console.log('[CanvasStore] Viewport changed:', {
  panX: viewport.panX,
  panY: viewport.panY,
  zoom: viewport.zoom,
});
```

### Log Levels

| Level | Use For |
|-------|---------|
| `console.log` | Normal flow, state changes, lifecycle |
| `console.warn` | Recoverable issues, fallbacks triggered |
| `console.error` | Failures, exceptions, broken state |
| `console.debug` | Verbose/temporary debugging (remove before commit) |

## Debugging by System

### React Component Issues

```typescript
// 1. Check if component is rendering
useEffect(() => {
  console.log('[MyComponent] Mounted');
  return () => console.log('[MyComponent] Unmounted');
}, []);

// 2. Track prop changes
useEffect(() => {
  console.log('[MyComponent] Props changed:', { prop1, prop2 });
}, [prop1, prop2]);

// 3. Track state changes
useEffect(() => {
  console.log('[MyComponent] State:', { localState });
}, [localState]);
```

**React DevTools**:
- Components tab → inspect props/state
- Profiler tab → identify slow renders
- Highlight updates → see what's re-rendering

### Zustand Store Issues

```typescript
// 1. Log all state changes (add to store temporarily)
const useMyStore = create(
  devtools(  // <-- Enable Redux DevTools
    (set, get) => ({
      // ...
    }),
    { name: 'MyStore' }
  )
);

// 2. Subscribe to changes
useEffect(() => {
  const unsub = useCanvasStore.subscribe(
    (state) => state.widgets,
    (widgets) => console.log('[Debug] Widgets changed:', widgets.size)
  );
  return unsub;
}, []);

// 3. Get current state anywhere
console.log('[Debug] Current state:', useCanvasStore.getState());
```

### Three.js / Spatial Issues

```typescript
// 1. Log 3D positions
console.log('[SpatialWidget] Position:', {
  x: mesh.position.x,
  y: mesh.position.y,
  z: mesh.position.z,
});

// 2. Visualize invisible objects
<mesh>
  <boxGeometry args={[1, 1, 1]} />
  <meshBasicMaterial color="red" wireframe /> {/* Wireframe to see through */}
</mesh>

// 3. Add axes helper to scene
import { useHelper } from '@react-three/drei';
useHelper(meshRef, THREE.AxesHelper, 1);

// 4. Check if in XR session
const session = useXR((state) => state.session);
console.log('[Debug] XR Session:', session ? 'ACTIVE' : 'none');
```

**Three.js Inspector**: Browser extension for inspecting Three.js scenes

### WebXR Issues

```typescript
// 1. Log XR capabilities
const caps = useSpatialModeStore.getState().capabilities;
console.log('[XR] Capabilities:', caps);

// 2. Log session state changes
useEffect(() => {
  console.log('[XR] Session state:', sessionState);
}, [sessionState]);

// 3. Check reference space
console.log('[XR] Reference space:', xrSession?.referenceSpace);

// Quest-specific: Use Meta Quest Developer Hub for remote debugging
```

### Widget/iframe Issues

```typescript
// 1. In host (StickerNest):
window.addEventListener('message', (e) => {
  console.log('[Host] Message from widget:', e.data);
});

// 2. In widget iframe:
console.log('[Widget] WidgetAPI available:', !!window.WidgetAPI);
console.log('[Widget] State:', WidgetAPI.getState());

// 3. Check iframe sandbox attributes
console.log('[Debug] Iframe sandbox:', iframe.sandbox);
```

### Network/Supabase Issues

```typescript
// 1. Log Supabase queries
const { data, error } = await supabase.from('table').select();
console.log('[Supabase] Query result:', { data, error });

// 2. Check realtime connection
console.log('[Realtime] Status:', supabase.realtime.connectionState);

// 3. Network tab in DevTools:
// - Filter by "supabase" to see API calls
// - Check WebSocket frames for realtime
```

## Common Issues & Solutions

### Issue: Component not rendering
```typescript
// Checklist:
// 1. Check conditional rendering
console.log('[Debug] Should render:', condition);

// 2. Check if parent is rendering
// 3. Check for errors in console
// 4. Check if key prop is stable (for lists)
```

### Issue: State not updating
```typescript
// Checklist:
// 1. Check if action is called
console.log('[Debug] Action called with:', params);

// 2. Check if state actually changed (immutability)
set({ items: [...get().items, newItem] }); // Correct
set({ items: get().items.push(newItem) }); // WRONG - mutates

// 3. Check selector
const items = useStore((s) => s.items); // Re-renders on items change
const items = useStore.getState().items; // Does NOT re-render
```

### Issue: VR shows flat screen
```
Cause: <Html> components in XR session
Debug: console.log('[Debug] isPresenting:', !!session);
Fix: Check isPresenting before rendering Html
```

### Issue: Widget not loading
```typescript
// Checklist:
console.log('[Debug] Widget manifest:', manifest);
console.log('[Debug] Widget HTML loaded:', !!htmlContent);
console.log('[Debug] WidgetAPI injected:', !!iframe.contentWindow.WidgetAPI);
```

### Issue: Position mismatch 2D/3D
```typescript
// Check coordinate conversion
const pos2D = { x: 500, y: 300 };
const pos3D = toSpatialPosition(pos2D);
console.log('[Debug] Conversion:', { pos2D, pos3D });
// Expected: pos3D = [5, -1.4, -2] (with eye height offset)
```

## Debug Helpers

### Temporary Debug Component

```tsx
function DebugOverlay() {
  const widgets = useCanvasStore((s) => s.widgets);
  const mode = useActiveSpatialMode();

  return (
    <div style={{
      position: 'fixed',
      top: 10,
      right: 10,
      background: 'rgba(0,0,0,0.8)',
      color: 'lime',
      padding: 10,
      fontFamily: 'monospace',
      fontSize: 12,
      zIndex: 9999,
    }}>
      <div>Mode: {mode}</div>
      <div>Widgets: {widgets.size}</div>
      <div>FPS: {/* Add FPS counter */}</div>
    </div>
  );
}
```

### Performance Timing

```typescript
// Measure operation duration
console.time('[Perf] Operation');
await expensiveOperation();
console.timeEnd('[Perf] Operation');

// With labels
performance.mark('start');
// ... work ...
performance.mark('end');
performance.measure('operation', 'start', 'end');
console.log(performance.getEntriesByName('operation'));
```

## Debug Flags

Add to localStorage for persistent debug modes:

```typescript
// Enable verbose logging
localStorage.setItem('stickernest-debug', 'true');

// Check in code
const DEBUG = localStorage.getItem('stickernest-debug') === 'true';
if (DEBUG) console.log('[Debug] Verbose info...');
```

## Cleanup Checklist

Before committing, remove:
- [ ] `console.debug()` statements
- [ ] Temporary `console.log()` with `[Debug]` prefix
- [ ] Debug components/overlays
- [ ] `debugger` statements
- [ ] Performance marks (unless permanent)

Keep:
- [ ] Error logging (`console.error`)
- [ ] Warning logging (`console.warn`)
- [ ] Important lifecycle logs with proper prefixes
