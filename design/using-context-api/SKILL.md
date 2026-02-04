---
name: using-context-api
description: Teaches Context API patterns in React 19 including use() hook for conditional context access. Use when implementing Context, avoiding prop drilling, or managing global state.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Context API Patterns in React 19

## Basic Pattern

```javascript
import { createContext, use, useState } from 'react';

const UserContext = createContext(null);

export function UserProvider({ children }) {
  const [user, setUser] = useState(null);

  return (
    <UserContext value={{ user, setUser }}>
      {children}
    </UserContext>
  );
}

export function useUser() {
  const context = use(UserContext);

  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }

  return context;
}
```

## React 19: Conditional Context Access

`use()` allows context access inside conditionals (unlike `useContext`):

```javascript
function Component({ isPremium }) {
  let theme;

  if (isPremium) {
    theme = use(ThemeContext);
  }

  return <div className={theme}>Content</div>;
}
```

## Splitting Contexts

Avoid unnecessary re-renders by splitting contexts:

```javascript
const UserContext = createContext(null);
const ThemeContext = createContext('light');

function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');

  return (
    <UserContext value={{ user, setUser }}>
      <ThemeContext value={{ theme, setTheme }}>
        <Layout />
      </ThemeContext>
    </UserContext>
  );
}
```

Now theme changes don't re-render components only using UserContext.

For comprehensive Context patterns, see: `research/react-19-comprehensive.md` lines 288-303, 1326-1342, 1644-1670.
