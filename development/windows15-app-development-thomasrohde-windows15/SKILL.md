---
name: windows15-app-development
description: Build and modify apps in the Windows 15 desktop environment. Use when creating new apps, modifying existing apps in apps/, working with window management, persistence, hotkeys, notifications, or UI components.
---

# Windows 15 App Development

Use this skill when building or modifying apps under `apps/` in the Windows 15 desktop environment.

## Quick Navigation

| Task                         | Documentation                                                                                                                                |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Create a new app             | [guides/creating-simple-app.md](guides/creating-simple-app.md)                                                                               |
| Register an app / app config | [core/app-architecture.md](core/app-architecture.md)                                                                                         |
| Open/focus/minimize windows  | [core/window-lifecycle.md](core/window-lifecycle.md)                                                                                         |
| Persist app state            | [guides/adding-persistence.md](guides/adding-persistence.md)                                                                                 |
| Keyboard shortcuts           | [guides/hotkeys.md](guides/hotkeys.md)                                                                                                       |
| Toast notifications          | [guides/notifications.md](guides/notifications.md)                                                                                           |
| UI components & styling      | [guides/styling-patterns.md](guides/styling-patterns.md), [reference/ui-components.md](reference/ui-components.md)                           |
| Full API lookup              | [reference/contexts.md](reference/contexts.md), [reference/hooks.md](reference/hooks.md)                                                     |
| Learn by example             | [examples/calculator-walkthrough.md](examples/calculator-walkthrough.md), [examples/notepad-walkthrough.md](examples/notepad-walkthrough.md) |

## Codebase Landmarks

- **App registration**: `apps/registry.ts` (authoritative app registry)
- **Window lifecycle**: `context/WindowContext.tsx` and `components/Window.tsx`
- **OS wrapper hook**: `context/OSContext.tsx` (`useOS()`)
- **Common hooks**: `hooks/index.ts`
- **UI primitives**: `components/ui/`

## Essential Patterns

### Creating a New App

1. Create component in `apps/MyApp.tsx`:

```tsx
import { AppContainer } from '../components/ui/AppContainer';

export function MyApp() {
    return (
        <AppContainer padding>
            <h1>My App</h1>
        </AppContainer>
    );
}
```

2. Register in `apps/registry.ts`:

```ts
{
  id: 'myapp',
  title: 'My App',
  icon: 'apps',
  color: 'bg-slate-400',
  component: React.lazy(() => import('./MyApp').then(m => ({ default: m.MyApp }))),
  defaultWidth: 520,
  defaultHeight: 420,
}
```

### Persisting State

Use `usePersistedState()` (Dexie/IndexedDB-backed):

```tsx
const { value, setValue, isLoading } = usePersistedState<Settings>('myapp.settings', defaultSettings);
```

### Window Instance Control

Apps receive `windowId` as a prop to control their window:

```tsx
const MyApp: React.FC<{ windowId: string }> = ({ windowId }) => {
    const { setTitle, setBadge } = useWindowInstance(windowId);
    // ...
};
```

### Toast Notifications

```tsx
const notify = useNotification();
notify.success('Saved!');
notify.error('Failed');
```

### Keyboard Shortcuts

```tsx
useStandardHotkeys({
    onSave: () => handleSave(),
    onFind: () => handleFind(),
});
```

## Constraints

- Prefer existing UI primitives in `components/ui/`
- Prefer `usePersistedState()` over `useLocalStorage()` for persistence
- Don't invent new global patterns when existing hooks/contexts solve it
- Keep `id` in registry stable (used for session restore)

## Documentation Index

### Core Architecture

- [core/app-architecture.md](core/app-architecture.md) - App registration and lazy loading
- [core/window-lifecycle.md](core/window-lifecycle.md) - Window creation, focus, persistence
- [core/state-management.md](core/state-management.md) - Where state lives
- [core/data-flow.md](core/data-flow.md) - Data flow diagrams

### Guides

- [guides/creating-simple-app.md](guides/creating-simple-app.md) - Step-by-step new app
- [guides/adding-persistence.md](guides/adding-persistence.md) - Persist app state
- [guides/state-persistence.md](guides/state-persistence.md) - Detailed persistence patterns
- [guides/hotkeys.md](guides/hotkeys.md) - Keyboard shortcuts
- [guides/notifications.md](guides/notifications.md) - Toast notifications
- [guides/styling-patterns.md](guides/styling-patterns.md) - UI patterns
- [guides/building-apps.md](guides/building-apps.md) - Full integration guide
- [guides/localization.md](guides/localization.md) - Multi-language support
- [guides/db-migration.md](guides/db-migration.md) - Migrate to IndexedDB

### Reference

- [reference/hooks.md](reference/hooks.md) - All available hooks
- [reference/contexts.md](reference/contexts.md) - OS contexts and hooks
- [reference/ui-components.md](reference/ui-components.md) - UI component library
- [reference/types.md](reference/types.md) - Shared types
- [reference/os-services.md](reference/os-services.md) - OS service reference
- [reference/system-sounds.md](reference/system-sounds.md) - Sound effects
- [reference/keyboard-shortcuts.md](reference/keyboard-shortcuts.md) - Global keyboard shortcuts

### Examples

- [examples/calculator-walkthrough.md](examples/calculator-walkthrough.md) - Simple self-contained app
- [examples/notepad-walkthrough.md](examples/notepad-walkthrough.md) - Multi-view app with file props

### API Documentation

- [api/hooks/useAppState.md](api/hooks/useAppState.md) - Persistent state
- [api/hooks/useSound.md](api/hooks/useSound.md) - System sounds
- [api/hooks/useWindow.md](api/hooks/useWindow.md) - Window instance control
- [api/hooks/useTranslation.md](api/hooks/useTranslation.md) - Localization
- [api/hooks/useFilePicker.md](api/hooks/useFilePicker.md) - File dialogs
