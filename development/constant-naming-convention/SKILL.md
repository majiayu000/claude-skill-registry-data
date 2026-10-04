---
name: constant-naming-convention
description: 'Repository-local guidance for naming constants in TypeScript/Angular. Prefer short, all-uppercase constant identifiers and lower-case runtime keys in object values.'
---

# Constant Naming Convention

## Guiding principles

- Use `ALL_UPPERCASE` for fixed, compile-time constants.
- Keep names as short as possible without losing meaning.
- Avoid long noun chains; remove redundant context.

---

## Basic usage

```ts
const MAX_RETRIES = 3;
const API_TIMEOUT_MS = 10000;
const DEFAULT_THEME = 'ocean';
const ENABLE_FEATURE_X = false;
```

For domain-specific values, keep the identifier concise:

```ts
const BASE_URL = 'https://api.example.com';
const TAB_SIZE = 2;
const ROW_GAP = '1.5rem';
```

---

## Short and descriptive

Prefer short constants when the meaning stays clear.

```ts
const TOKEN_KEY = 'auth-token';
const SSO_COOKIE = 'sso-session';
const API_PORT = 4200;
```

Avoid verbose names that repeat obvious context.

```ts
// preferred
const TOKEN_KEY = 'auth-token';

// not preferred
const USER_AUTH_TOKEN_STORAGE_KEY = 'auth-token';
```

---

## Names longer than three words

If a constant needs more than three words, shorten it using abbreviations or remove redundant qualifiers.

```ts
// preferred
const SESSION_TOKEN_KEY = 'auth-token';
const API_BASE_URL = 'https://api.example.com';

// not preferred
const USER_SESSION_TOKEN_STORAGE_KEY = 'auth-token';
const DEFAULT_APPLICATION_API_BASE_URL = 'https://api.example.com';
```

Keep longer names readable by limiting noun chains.

```ts
const SIDEBAR_MIN_WIDTH = 72;
const TOAST_AUTO_HIDE_MS = 5000;
```

---

## Objects and maps

Keep the constant identifier uppercase. Use lowercase keys when object entries represent runtime identifiers, route names, or domain values.

```ts
const STATUS_LABELS = {
  active: 'Active',
  inactive: 'Inactive',
  pending: 'Pending',
};

const ROUTE_PATHS = {
  home: '/home',
  login: '/login',
};
```

For small lookup maps, keep the name short.

```ts
const HTTP_CODES = {
  ok: 200,
  err: 500,
};
```

---

## Enum-like constants

Use uppercase for constant values that behave like enum members.

```ts
const USER_ROLE_ADMIN = 'admin';
const USER_ROLE_GUEST = 'guest';
```

For real enums, use PascalCase members.

```ts
enum ThemeMode {
  Light = 'light',
  Dark = 'dark',
}
```

---

## Dependency injection tokens

Use concise uppercase names for injection tokens.

```ts
const AUTH_TOKEN = new InjectionToken<string>('AUTH_TOKEN');
const API_BASE = new InjectionToken<string>('API_BASE');
const WINDOW_REF = new InjectionToken<Window>('WINDOW_REF');
```

---

## Feature-specific constants

Use short uppercase names that still convey the feature domain.

```ts
const SIDEBAR_MIN = 72;
const SIDEBAR_MAX = 280;
const NAV_DELAY = 150;
const TOAST_DURATION = 5000;
const TOAST_POSITION = 'top-right';
```

---

## When not to use uppercase

Do not use `ALL_UPPERCASE` for runtime variables, mutable references, or non-constant values.

```ts
let count = 0;
const service = inject(AuthService);
const theme = signal('light');
```

---

## Summary

- `ALL_UPPERCASE` is the default for constants.
- Prefer short, clear identifiers.
- Keep object/map keys lowercase for runtime or domain values.
- Use PascalCase only for actual enums and classes.
