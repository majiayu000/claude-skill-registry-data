---
name: dockview
description: dockview-react panel layout library. Use when building multi-panel IDE-style layouts, implementing dockable/floatable panels, persisting layout state, or debugging dockview. Triggers on DockviewReact, IDockviewPanelProps, DockviewApi, DockviewReadyEvent, addPanel, fromJSON, toJSON, onReady, components prop.
---

# Dockview

`dockview` (package: `dockview` or `dockview-react`) provides a VS Code-style dockable panel shell for React apps. The `DockviewReact` component is the root; panels are registered as React components keyed by string name.

## Critical: `components` prop identity

**The most important thing to know about dockview:** the `components` prop is compared by object reference on every render. If the reference changes, dockview treats all panels as new component types and unmounts + remounts every panel — causing a visible blank flash.

**WRONG — new object and new `React.FC` identities on every render:**
```tsx
// ❌ inline: wrapForDockview creates new function identities each render
<DockviewReact
  components={{ 'panel.id': wrapForDockview(MyPanel) }}
  onReady={onReady}
/>
```

**CORRECT — stable reference with `useMemo`:**
```tsx
// Build once at module scope OR useMemo
const COMPONENTS = {
  'panel.id': wrapForDockview(MyPanel)   // module-level = always stable
};

// If overrides come from props, memoize:
const dockviewComponents = useMemo(
  () => mergeComponents(COMPONENTS, panelComponentOverrides),
  [panelComponentOverrides]   // deps must also be stable (see below)
);

<DockviewReact components={dockviewComponents} onReady={onReady} />
```

The `panelComponentOverrides` object passed from a parent must also be stable — wrap it in `useMemo` in the parent:
```tsx
// ❌ new object literal on every parent render
<DockShell panelComponents={{ 'panel.id': MyPanel }} />

// ✅ memoized in parent
const overrides = useMemo(() => ({ 'panel.id': MyPanel }), [MyPanel]);
<DockShell panelComponents={overrides} />
```

## Setup

```tsx
import { DockviewReact } from 'dockview-react';
import type {
  DockviewApi,
  DockviewReadyEvent,
  IDockviewPanelProps,
  AddPanelOptions,
} from 'dockview-react';
import 'dockview-react/dist/styles/dockview.css';

// Panel wrapper — dockview injects { params, api } but panels
// usually don't need them; wrap to hide the signature.
function wrap<P extends object>(C: React.FC<P>): React.FC<IDockviewPanelProps> {
  return function Wrapped() { return <C {...({} as P)} />; };
}

const COMPONENTS = {
  'sidebar':  wrap(Sidebar),
  'editor':   wrap(Editor),
  'terminal': wrap(Terminal),
};

function Shell() {
  const apiRef = useRef<DockviewApi | null>(null);

  const onReady = useCallback((event: DockviewReadyEvent) => {
    apiRef.current = event.api;
    // add panels here, or call api.fromJSON(savedLayout)
    event.api.addPanel({ id: 'sidebar',  component: 'sidebar'  });
    event.api.addPanel({ id: 'editor',   component: 'editor',   position: { referencePanel: 'sidebar', direction: 'right' } });
    event.api.addPanel({ id: 'terminal', component: 'terminal', position: { referencePanel: 'editor',  direction: 'below' } });
  }, []);   // deps: only stable values — avoid layout state here (see pitfalls)

  return (
    <DockviewReact
      className="h-full"
      components={COMPONENTS}    // MUST be stable — see above
      onReady={onReady}
    />
  );
}
```

## Layout persistence (toJSON / fromJSON)

Dockview serializes its own layout as a JSON blob. Save it on every change and restore on mount:

```tsx
const onReady = useCallback((event: DockviewReadyEvent) => {
  apiRef.current = event.api;

  // Restore saved layout OR build fresh
  if (savedLayout?.dockview) {
    try {
      event.api.fromJSON(savedLayout.dockview);
    } catch {
      addDefaultPanels(event.api);   // fallback on incompatible blob
    }
  } else {
    addDefaultPanels(event.api);
  }

  // Persist on every change
  event.api.onDidLayoutChange(() => {
    onSave(event.api.toJSON());
  });
}, [savedLayout]);  // ⚠ if savedLayout is state, see pitfall below
```

**Layout migration**: dockview's native JSON is coupled to panel IDs and its own internal coordinate space. If panel IDs change across app versions, `fromJSON` may throw. Store a `shape` discriminator alongside the blob and handle both factory (addPanel) and native (fromJSON) paths.

## Accessing the API imperatively

```tsx
// Reset layout
apiRef.current?.clear();
addDefaultPanels(apiRef.current!);

// Focus a panel
apiRef.current?.getPanel('editor')?.focus();

// Close a panel
apiRef.current?.getPanel('terminal')?.api.close();
```

## Testing (jsdom / vitest)

Dockview's layout engine uses `ResizeObserver` and `getBoundingClientRect` — both unavailable in jsdom. Mock the module:

```ts
// vitest.setup.ts
vi.mock('dockview-react', () => ({
  DockviewReact: ({ children }: { children?: React.ReactNode }) => <div>{children}</div>,
}));
```

Tests should assert against accessible roles or `data-testid` on panel content; the DockviewReact stub is just a div.

## Reference

- **Common pitfalls**: [references/pitfalls.md](references/pitfalls.md)
