---
name: typescript-type
description: "World Pulse: When adding new types, modifying shared interfaces, or working in `src/shared/types.ts`."
---

# TypeScript Type

**When to use:** When adding new types, modifying shared interfaces, or working in `src/shared/types.ts`.

---

## Strict Mode

The project runs TypeScript in strict mode (`tsconfig.json`):

```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}
```

Every variable, parameter, and return type must be explicitly typed or provably inferred. `noUnusedLocals`/`noUnusedParameters` cause build failures — prefix intentionally unused parameters with `_`.

---

## Shared Contract Location

All types shared between frontend, backend, and Electron live in **`src/shared/types.ts`**. Do not duplicate types in individual packages.

Changes to `src/shared/types.ts` are **high-risk surface** — they require architect review (see `risk_surface` severity gate).

---

## Core Types (`src/shared/types.ts`)

```ts
// Base event — all collector output extends this
interface Event {
  id: string;
  timestamp: number;
  type: EventType;
  source: string;
  location: GeoLocation | null;
  title: string;
  severity?: number;      // 0–10 scale
  expiresAt?: number;     // Unix ms; undefined = no expiry
  data: Record<string, unknown>;
}

type EventType =
  | 'earthquake' | 'weather' | 'news' | 'astronomy'
  | 'volcano' | 'iss' | 'aurora' | 'asteroid' | 'planet'
  | 'music' | 'ocean' | 'calendar' | 'historical';

interface GeoLocation { lat: number; lon: number; }

type ConnectionStatus =
  | 'connecting' | 'connected' | 'disconnected'
  | 'error' | 'dormant-reconnecting';
```

---

## Adding a New EventType

1. Add the string literal to the `EventType` union in `src/shared/types.ts`.
2. Create a typed interface extending `Event`:

```ts
interface MoonEvent extends Event {
  type: 'moon';
  data: {
    phase: string;
    illumination: number;
    age: number;
  };
}
```

3. Export the new interface.
4. Add the `EventType` value to collectors and tests.

---

## Discriminated Unions

Use discriminated unions for pattern matching on event type:

```ts
function renderEvent(event: Event) {
  switch (event.type) {
    case 'earthquake':
      return renderEarthquake(event as EarthquakeEvent);
    case 'weather':
      return renderWeather(event as WeatherEvent);
    default:
      return renderGeneric(event);
  }
}
```

---

## Avoiding `any`

ESLint warns on `any`. Use these alternatives:

```ts
// Unknown input from external APIs
const data: unknown = await response.json();
if (typeof data === 'object' && data !== null && 'magnitude' in data) {
  const magnitude = (data as { magnitude: number }).magnitude;
}

// Record for dynamic objects
const props: Record<string, unknown> = {};

// Generic with constraint
function processEvents<T extends Event>(events: T[]): T[] { ... }
```

---

## Path Aliases

Always use aliases for cross-package imports — never relative paths across boundaries:

```ts
import type { Event } from '@shared/types';   // correct
import type { Event } from '../../../shared/types'; // wrong
```

---

## Anti-Patterns

- Do not use `as any` — it defeats strict mode.
- Do not cast with `as T` unless you've verified the shape (use a type guard instead).
- Do not use `interface` merging to extend `Event` — extend via `extends Event`.
- Do not put frontend-only or backend-only types in `src/shared/types.ts` — only cross-boundary contracts belong there.
- Do not use `namespace` — use ES module exports.
