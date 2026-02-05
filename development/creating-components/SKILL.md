---
name: creating-components
description: Creating React components for StickerNest. Use when the user asks to create a component, build a UI component, add a panel, create a toolbar, build a dialog, or implement any React UI element. Covers component structure, Zustand integration, theme tokens, hooks, and common UI patterns.
---

# Creating StickerNest React Components

This skill covers creating React components that follow StickerNest's patterns, including Zustand store integration, theme tokens, and custom hooks.

## Component Location

| Type | Location |
|------|----------|
| UI Components | `src/components/` |
| Shared UI | `src/shared-ui/` |
| Hooks | `src/hooks/` |

---

## Basic Component Template

```typescript
// src/components/MyComponent.tsx
import React, { useState, useCallback, useEffect } from 'react';
import { useCanvasStore } from '../state/useCanvasStore';

interface MyComponentProps {
  /** Component property */
  value?: string;
  /** Callback when value changes */
  onChange?: (value: string) => void;
  /** Optional CSS class */
  className?: string;
}

export const MyComponent: React.FC<MyComponentProps> = ({
  value = '',
  onChange,
  className,
}) => {
  // Local state
  const [localValue, setLocalValue] = useState(value);

  // Zustand store state (select only what you need)
  const canvasId = useCanvasStore((s) => s.canvasId);
  const addWidget = useCanvasStore((s) => s.addWidget);

  // Handlers
  const handleChange = useCallback((newValue: string) => {
    setLocalValue(newValue);
    onChange?.(newValue);
  }, [onChange]);

  // Effects
  useEffect(() => {
    setLocalValue(value);
  }, [value]);

  return (
    <div
      className={className}
      style={{
        backgroundColor: 'var(--sn-bg-secondary)',
        borderRadius: 'var(--sn-radius-md)',
        padding: 'var(--sn-space-4)',
        color: 'var(--sn-text-primary)',
      }}
    >
      {/* Component content */}
    </div>
  );
};
```

---

## Zustand Store Integration

### Selecting State (Optimized)

```typescript
// GOOD: Select only what you need
const canvasId = useCanvasStore((s) => s.canvasId);
const widgets = useCanvasStore((s) => s.widgets);

// BAD: Selecting entire state causes unnecessary re-renders
const store = useCanvasStore(); // Avoid this
```

### Multiple Selectors

```typescript
// Option 1: Multiple hooks (recommended for unrelated data)
const canvasId = useCanvasStore((s) => s.canvasId);
const mode = useCanvasStore((s) => s.mode);

// Option 2: Single selector for related data
const { canvasId, mode } = useCanvasStore((s) => ({
  canvasId: s.canvasId,
  mode: s.mode,
}));
```

### Accessing Actions

```typescript
// Actions are stable, safe to access directly
const addWidget = useCanvasStore((s) => s.addWidget);
const removeWidget = useCanvasStore((s) => s.removeWidget);

// Or destructure multiple
const { addWidget, removeWidget, updateWidget } = useCanvasStore((s) => ({
  addWidget: s.addWidget,
  removeWidget: s.removeWidget,
  updateWidget: s.updateWidget,
}));
```

### Available Stores

| Store | Purpose | Key State |
|-------|---------|-----------|
| `useCanvasStore` | Canvas & widgets | `canvasId`, `widgets`, `mode`, `selection` |
| `useLibraryStore` | Widget library | `searchQuery`, `selectedWidgets`, `filters` |
| `usePanelsStore` | Panel states | `isPanelOpen`, `panelPositions` |
| `useToolStore` | Active tools | `activeTool`, `shapeDefaults` |
| `useThemeStore` | Theme settings | `theme`, `customColors` |
| `useAssetStore` | Asset management | `assets`, `uploadProgress` |
| `useApiSettingsStore` | API config | `apiKey`, `endpoint` |

---

## Theme Tokens

### Color Tokens

```css
/* Backgrounds */
--sn-bg-primary: #0f0f19;
--sn-bg-secondary: #1a1a2e;
--sn-bg-tertiary: #252538;
--sn-bg-elevated: #2a2a42;

/* Text */
--sn-text-primary: #e2e8f0;
--sn-text-secondary: #94a3b8;
--sn-text-muted: #64748b;

/* Accents */
--sn-accent-primary: #8b5cf6;
--sn-accent-secondary: #a78bfa;
--sn-success: #22c55e;
--sn-error: #ef4444;
--sn-warning: #f59e0b;
--sn-info: #3b82f6;

/* Borders */
--sn-border-primary: rgba(139, 92, 246, 0.2);
--sn-border-secondary: rgba(255, 255, 255, 0.1);
```

### Spacing Tokens

```css
--sn-space-1: 4px;
--sn-space-2: 8px;
--sn-space-3: 12px;
--sn-space-4: 16px;
--sn-space-5: 20px;
--sn-space-6: 24px;
--sn-space-8: 32px;
```

### Border Radius

```css
--sn-radius-sm: 4px;
--sn-radius-md: 6px;
--sn-radius-lg: 8px;
--sn-radius-xl: 12px;
--sn-radius-full: 9999px;
```

### Elevation (Shadows)

```css
--sn-elevation-1: 0 1px 2px rgba(0, 0, 0, 0.3);
--sn-elevation-2: 0 2px 4px rgba(0, 0, 0, 0.4);
--sn-elevation-3: 0 4px 8px rgba(0, 0, 0, 0.5);
--sn-elevation-panel: 0 4px 16px rgba(0, 0, 0, 0.5);
```

### Transitions

```css
--sn-transition-fast: 150ms ease;
--sn-transition-normal: 200ms ease;
--sn-transition-slow: 300ms ease;
--sn-ease-spring-snappy: cubic-bezier(0.34, 1.56, 0.64, 1);
```

### Glass Effect

```css
--sn-glass-bg: rgba(15, 15, 25, 0.85);
--sn-glass-blur: blur(12px);
--sn-glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
```

---

## Common UI Patterns

### Panel Component

```typescript
interface PanelProps {
  title: string;
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export const Panel: React.FC<PanelProps> = ({
  title,
  isOpen,
  onClose,
  children,
}) => {
  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'absolute',
        right: 0,
        top: 0,
        bottom: 0,
        width: 320,
        background: 'var(--sn-glass-bg)',
        backdropFilter: 'var(--sn-glass-blur)',
        borderLeft: '1px solid var(--sn-border-primary)',
        boxShadow: 'var(--sn-elevation-panel)',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: 'var(--sn-space-4)',
          borderBottom: '1px solid var(--sn-border-secondary)',
        }}
      >
        <span style={{ fontWeight: 600, color: 'var(--sn-text-primary)' }}>
          {title}
        </span>
        <button
          onClick={onClose}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--sn-text-secondary)',
            cursor: 'pointer',
            padding: 'var(--sn-space-1)',
          }}
        >
          &times;
        </button>
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflow: 'auto', padding: 'var(--sn-space-4)' }}>
        {children}
      </div>
    </div>
  );
};
```

### Button Component

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children,
}) => {
  const baseStyles: React.CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 'var(--sn-radius-md)',
    fontWeight: 500,
    cursor: disabled ? 'not-allowed' : 'pointer',
    opacity: disabled ? 0.5 : 1,
    transition: 'var(--sn-transition-fast)',
    border: 'none',
  };

  const variantStyles: Record<string, React.CSSProperties> = {
    primary: {
      background: 'var(--sn-accent-primary)',
      color: 'white',
    },
    secondary: {
      background: 'var(--sn-bg-tertiary)',
      color: 'var(--sn-text-primary)',
      border: '1px solid var(--sn-border-primary)',
    },
    ghost: {
      background: 'transparent',
      color: 'var(--sn-text-secondary)',
    },
  };

  const sizeStyles: Record<string, React.CSSProperties> = {
    sm: { padding: '6px 12px', fontSize: 12 },
    md: { padding: '8px 16px', fontSize: 14 },
    lg: { padding: '12px 24px', fontSize: 16 },
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        ...baseStyles,
        ...variantStyles[variant],
        ...sizeStyles[size],
      }}
    >
      {children}
    </button>
  );
};
```

### Input Component

```typescript
interface InputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: 'text' | 'number' | 'password';
  disabled?: boolean;
}

export const Input: React.FC<InputProps> = ({
  value,
  onChange,
  placeholder,
  type = 'text',
  disabled = false,
}) => {
  return (
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      disabled={disabled}
      style={{
        width: '100%',
        padding: 'var(--sn-space-2) var(--sn-space-3)',
        background: 'var(--sn-bg-tertiary)',
        border: '1px solid var(--sn-border-primary)',
        borderRadius: 'var(--sn-radius-md)',
        color: 'var(--sn-text-primary)',
        fontSize: 14,
        outline: 'none',
        transition: 'var(--sn-transition-fast)',
      }}
    />
  );
};
```

### List Item Component

```typescript
interface ListItemProps {
  selected?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

export const ListItem: React.FC<ListItemProps> = ({
  selected = false,
  onClick,
  children,
}) => {
  return (
    <div
      onClick={onClick}
      style={{
        padding: 'var(--sn-space-3)',
        borderRadius: 'var(--sn-radius-md)',
        background: selected ? 'var(--sn-accent-primary)' : 'transparent',
        color: selected ? 'white' : 'var(--sn-text-primary)',
        cursor: 'pointer',
        transition: 'var(--sn-transition-fast)',
      }}
    >
      {children}
    </div>
  );
};
```

---

## Custom Hooks

### Creating a Custom Hook

```typescript
// src/hooks/useMyFeature.ts
import { useState, useCallback, useEffect } from 'react';
import { useCanvasStore } from '../state/useCanvasStore';

interface UseMyFeatureOptions {
  initialValue?: string;
  autoSave?: boolean;
}

interface UseMyFeatureReturn {
  value: string;
  setValue: (value: string) => void;
  isLoading: boolean;
  error: string | null;
}

export function useMyFeature(
  options: UseMyFeatureOptions = {}
): UseMyFeatureReturn {
  const { initialValue = '', autoSave = false } = options;

  // Local state
  const [value, setValueState] = useState(initialValue);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Store integration
  const canvasId = useCanvasStore((s) => s.canvasId);

  // Handlers
  const setValue = useCallback((newValue: string) => {
    setValueState(newValue);
    setError(null);

    if (autoSave) {
      // Auto-save logic
    }
  }, [autoSave]);

  // Effects
  useEffect(() => {
    // Initialization or subscription logic
    return () => {
      // Cleanup
    };
  }, [canvasId]);

  return {
    value,
    setValue,
    isLoading,
    error,
  };
}
```

### Existing Hooks Reference

| Hook | Purpose | File |
|------|---------|------|
| `useCanvasController` | Canvas control logic | `src/hooks/useCanvasController.ts` |
| `useCanvasGestures` | Pan, zoom, touch | `src/hooks/useCanvasGestures.ts` |
| `useCanvasKeyboardShortcuts` | Keyboard bindings | `src/hooks/useCanvasKeyboardShortcuts.ts` |
| `useResponsive` | Viewport detection | `src/hooks/useResponsive.ts` |
| `useWidgetCapabilities` | Capability checking | `src/hooks/useWidgetCapabilities.ts` |
| `useWidgetSync` | Widget synchronization | `src/hooks/useWidgetSync.ts` |
| `usePermission` | Permission checking | `src/hooks/usePermission.ts` |

---

## Component Best Practices

### 1. Memoization

```typescript
// Memoize expensive computations
const processedData = useMemo(() => {
  return data.map(item => expensiveProcess(item));
}, [data]);

// Memoize callbacks passed to children
const handleClick = useCallback(() => {
  doSomething(value);
}, [value]);

// Memoize components that receive stable props
const MemoizedChild = React.memo(ChildComponent);
```

### 2. Error Boundaries

```typescript
// Wrap components that might throw
<ErrorBoundary fallback={<ErrorFallback />}>
  <RiskyComponent />
</ErrorBoundary>
```

### 3. Loading States

```typescript
if (isLoading) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'var(--sn-text-secondary)',
    }}>
      Loading...
    </div>
  );
}
```

### 4. Conditional Rendering with Visibility

```typescript
// For panels that need to maintain state, use CSS instead of unmounting
<div style={{ display: isVisible ? 'block' : 'none' }}>
  <ExpensivePanel />
</div>
```

---

## Reference Files

- **Theme tokens**: `src/styles/theme-tokens.css`
- **Global styles**: `src/index.css`
- **Example components**: `src/components/PropertiesPanel.tsx`, `src/components/LayerPanel.tsx`
- **Hooks**: `src/hooks/`
- **Stores**: `src/state/`
