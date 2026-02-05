---
name: theming-with-tokens
description: Theming StickerNest with CSS tokens and design variables. Use when the user asks about themes, CSS variables, dark mode, skinning, color schemes, theme tokens, widget theming, or customizing appearance. Covers theme system, token inheritance, and widget styling.
---

# Theming with Tokens in StickerNest

This skill covers the theming system using CSS custom properties (tokens), enabling consistent styling across the app and widgets with full customization support.

## Philosophy

> "Everything is themeable. The canvas, components, and widgets all inherit from a unified token system."

- Themes are CSS variable collections
- Widgets inherit tokens from the host
- Users can override any token
- Multiple themes can coexist on a canvas

---

## Token Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Theme Provider                            │
│                 (sets :root variables)                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  App Shell   │  │  Components  │  │  Widgets     │
│  (inherits)  │  │  (inherits)  │  │  (inherits)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## Core Token Categories

### 1. Color Tokens

```css
:root {
  /* Base colors */
  --color-bg-primary: #0a0a0f;
  --color-bg-secondary: #12121a;
  --color-bg-tertiary: #1a1a24;

  /* Surface colors (panels, cards) */
  --color-surface: #16161f;
  --color-surface-hover: #1e1e28;
  --color-surface-active: #252530;

  /* Text colors */
  --color-text-primary: #ffffff;
  --color-text-secondary: #a1a1aa;
  --color-text-muted: #71717a;
  --color-text-disabled: #52525b;

  /* Accent colors */
  --color-accent: #6366f1;
  --color-accent-hover: #818cf8;
  --color-accent-muted: rgba(99, 102, 241, 0.2);

  /* Semantic colors */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Border colors */
  --color-border: #27272a;
  --color-border-hover: #3f3f46;
  --color-border-focus: var(--color-accent);
}
```

### 2. Typography Tokens

```css
:root {
  /* Font families */
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Font sizes */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */

  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

### 3. Spacing Tokens

```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
}
```

### 4. Layout Tokens

```css
:root {
  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.6);

  /* Transitions */
  --transition-fast: 100ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;

  /* Z-index layers */
  --z-base: 0;
  --z-widget: 10;
  --z-dropdown: 100;
  --z-modal: 200;
  --z-tooltip: 300;
  --z-toast: 400;
}
```

---

## Widget-Specific Tokens

```css
:root {
  /* Widget container */
  --widget-bg: var(--color-surface);
  --widget-border: var(--color-border);
  --widget-radius: var(--radius-lg);
  --widget-shadow: var(--shadow-md);

  /* Widget text */
  --widget-text: var(--color-text-primary);
  --widget-text-muted: var(--color-text-muted);

  /* Widget interactive */
  --widget-accent: var(--color-accent);
  --widget-item-bg: var(--color-bg-tertiary);
  --widget-item-hover: var(--color-surface-hover);

  /* Widget header */
  --widget-header-bg: var(--color-bg-secondary);
  --widget-header-height: 32px;
}
```

---

## Social-Specific Tokens

```css
:root {
  /* Social feed */
  --social-feed-bg: var(--widget-bg);
  --social-feed-item-bg: var(--widget-item-bg);
  --social-feed-item-hover: var(--widget-item-hover);

  /* Avatars */
  --social-avatar-size: 40px;
  --social-avatar-size-sm: 32px;
  --social-avatar-size-lg: 56px;
  --social-avatar-border: 2px solid var(--color-accent);

  /* Status indicators */
  --social-online-color: #22c55e;
  --social-offline-color: #6b7280;
  --social-away-color: #f59e0b;
  --social-busy-color: #ef4444;

  /* Chat */
  --social-chat-bubble-self: var(--color-accent);
  --social-chat-bubble-other: var(--color-surface-hover);
  --social-chat-text-self: #ffffff;
  --social-chat-text-other: var(--color-text-primary);

  /* Notifications */
  --social-notification-unread-bg: rgba(99, 102, 241, 0.1);
  --social-notification-badge: var(--color-error);

  /* Activity */
  --social-verb-color: var(--color-accent);
  --social-timestamp-color: var(--color-text-muted);
}
```

---

## Theme Definitions

### Default Theme (Dark)

```typescript
// src/themes/default.ts

export const defaultTheme = {
  id: 'default',
  name: 'Default',
  tokens: {
    'color-bg-primary': '#0a0a0f',
    'color-bg-secondary': '#12121a',
    'color-surface': '#16161f',
    'color-text-primary': '#ffffff',
    'color-accent': '#6366f1',
    // ... all tokens
  },
};
```

### Cyberpunk Theme

```typescript
export const cyberpunkTheme = {
  id: 'cyberpunk',
  name: 'Cyberpunk',
  tokens: {
    'color-bg-primary': '#0d0d0d',
    'color-bg-secondary': '#1a0a1a',
    'color-surface': '#1f0f1f',
    'color-text-primary': '#00ff88',
    'color-accent': '#ff00ff',
    'color-accent-hover': '#ff66ff',
    'social-online-color': '#00ff88',
    // ... cyberpunk-specific overrides
  },
};
```

### Cozy Theme (Light)

```typescript
export const cozyTheme = {
  id: 'cozy',
  name: 'Cozy',
  tokens: {
    'color-bg-primary': '#faf5f0',
    'color-bg-secondary': '#f5ede4',
    'color-surface': '#ffffff',
    'color-text-primary': '#2d2a26',
    'color-accent': '#c9a87c',
    // ... warm, light tokens
  },
};
```

---

## Theme Store

```typescript
// src/state/useThemeStore.ts

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { defaultTheme, cyberpunkTheme, cozyTheme } from '@/themes';

interface ThemeState {
  currentThemeId: string;
  customTokens: Record<string, string>;
}

interface ThemeActions {
  setTheme: (themeId: string) => void;
  setCustomToken: (key: string, value: string) => void;
  resetCustomTokens: () => void;
  getEffectiveTokens: () => Record<string, string>;
}

const themes = {
  default: defaultTheme,
  cyberpunk: cyberpunkTheme,
  cozy: cozyTheme,
};

export const useThemeStore = create<ThemeState & ThemeActions>()(
  persist(
    (set, get) => ({
      currentThemeId: 'default',
      customTokens: {},

      setTheme: (themeId) => {
        set({ currentThemeId: themeId });
        get().applyTheme();
      },

      setCustomToken: (key, value) => {
        set((state) => ({
          customTokens: { ...state.customTokens, [key]: value },
        }));
        get().applyTheme();
      },

      resetCustomTokens: () => {
        set({ customTokens: {} });
        get().applyTheme();
      },

      getEffectiveTokens: () => {
        const theme = themes[get().currentThemeId] || defaultTheme;
        return { ...theme.tokens, ...get().customTokens };
      },

      applyTheme: () => {
        const tokens = get().getEffectiveTokens();
        const root = document.documentElement;

        Object.entries(tokens).forEach(([key, value]) => {
          root.style.setProperty(`--${key}`, value);
        });
      },
    }),
    {
      name: 'theme-store',
      partialize: (state) => ({
        currentThemeId: state.currentThemeId,
        customTokens: state.customTokens,
      }),
    }
  )
);
```

---

## ThemeProvider Component

```typescript
// src/components/ThemeProvider.tsx

import { useEffect } from 'react';
import { useThemeStore } from '@/state/useThemeStore';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const applyTheme = useThemeStore((state) => state.applyTheme);

  useEffect(() => {
    // Apply theme on mount
    applyTheme();
  }, [applyTheme]);

  return <>{children}</>;
}
```

---

## Sending Tokens to Widgets

```typescript
// src/runtime/WidgetHost.ts

class WidgetHost {
  private sendThemeTokens() {
    const tokens = useThemeStore.getState().getEffectiveTokens();

    // Filter to widget-relevant tokens
    const widgetTokens = Object.fromEntries(
      Object.entries(tokens).filter(([key]) =>
        key.startsWith('widget-') ||
        key.startsWith('social-') ||
        key.startsWith('color-')
      )
    );

    this.iframe.contentWindow?.postMessage({
      type: 'widget:theme',
      payload: widgetTokens,
    }, '*');
  }

  // Subscribe to theme changes
  private setupThemeSync() {
    useThemeStore.subscribe(() => {
      this.sendThemeTokens();
    });
  }
}
```

---

## Widget Theme Consumption

```html
<!-- In widget HTML -->
<style>
  :root {
    /* Fallback values if host doesn't send tokens */
    --widget-bg: #1a1a2e;
    --widget-text: #ffffff;
    --widget-accent: #6366f1;
  }

  body {
    background: var(--widget-bg);
    color: var(--widget-text);
  }

  .button {
    background: var(--widget-accent);
  }
</style>

<script>
  // Apply tokens from host
  window.addEventListener('message', (event) => {
    if (event.data?.type === 'widget:theme') {
      const tokens = event.data.payload;
      const root = document.documentElement;

      Object.entries(tokens).forEach(([key, value]) => {
        root.style.setProperty(`--${key}`, value);
      });
    }
  });
</script>
```

---

## Component Styling Patterns

### Using Tokens in Components

```typescript
// Use CSS variables directly
const Button = styled.button`
  background: var(--color-accent);
  color: var(--color-text-primary);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  transition: background var(--transition-fast);

  &:hover {
    background: var(--color-accent-hover);
  }
`;

// Or with inline styles
function Button({ children }) {
  return (
    <button
      style={{
        background: 'var(--color-accent)',
        color: 'var(--color-text-primary)',
        padding: 'var(--space-2) var(--space-4)',
        borderRadius: 'var(--radius-md)',
      }}
    >
      {children}
    </button>
  );
}
```

### Theme-Aware Hook

```typescript
// src/hooks/useTheme.ts

export function useTheme() {
  const { currentThemeId, setTheme, setCustomToken, getEffectiveTokens } = useThemeStore();

  const getToken = (key: string): string => {
    return getComputedStyle(document.documentElement)
      .getPropertyValue(`--${key}`)
      .trim();
  };

  const isDark = () => {
    const bg = getToken('color-bg-primary');
    // Simple darkness check
    return bg.startsWith('#0') || bg.startsWith('#1') || bg.startsWith('#2');
  };

  return {
    themeId: currentThemeId,
    setTheme,
    setToken: setCustomToken,
    getToken,
    isDark: isDark(),
    tokens: getEffectiveTokens(),
  };
}
```

---

## Canvas-Level Theme Overrides

```typescript
// Each canvas can have its own theme overrides
interface Canvas {
  id: string;
  name: string;
  themeOverrides?: Record<string, string>;
}

// Apply when loading canvas
function loadCanvas(canvas: Canvas) {
  if (canvas.themeOverrides) {
    Object.entries(canvas.themeOverrides).forEach(([key, value]) => {
      document.documentElement.style.setProperty(`--${key}`, value);
    });
  }
}
```

---

## Theme Editor UI

```typescript
// src/components/ThemeEditor.tsx

function ThemeEditor() {
  const { tokens, setToken, themeId, setTheme } = useTheme();

  return (
    <div className="theme-editor">
      <select value={themeId} onChange={(e) => setTheme(e.target.value)}>
        <option value="default">Default</option>
        <option value="cyberpunk">Cyberpunk</option>
        <option value="cozy">Cozy</option>
      </select>

      <div className="token-editors">
        <ColorPicker
          label="Accent Color"
          value={tokens['color-accent']}
          onChange={(v) => setToken('color-accent', v)}
        />
        <ColorPicker
          label="Background"
          value={tokens['color-bg-primary']}
          onChange={(v) => setToken('color-bg-primary', v)}
        />
        {/* More token editors */}
      </div>
    </div>
  );
}
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `src/themes/` | Theme definitions |
| `src/state/useThemeStore.ts` | Theme state management |
| `src/components/ThemeProvider.tsx` | Theme application |
| `src/hooks/useTheme.ts` | Theme access hook |
| `src/styles/tokens.css` | Token definitions |

---

## Best Practices

1. **Use semantic names** - `--color-accent` not `--purple`
2. **Layer tokens** - Base → Component → Widget
3. **Provide fallbacks** - Widgets should work without host tokens
4. **Use CSS variables** - Not hardcoded colors
5. **Document tokens** - Clear naming conventions
6. **Test both themes** - Dark and light
7. **Consider accessibility** - Color contrast ratios
8. **Keep tokens minimal** - Only what's needed
