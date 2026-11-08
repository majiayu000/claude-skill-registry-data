---
name: platform-access-di
kind: pattern
rule: platform-access
description: Pattern of rule platform-access. Load when the window, the document or an environment check enters the code — ready-made token injects, casting to Window & typeof globalThis, the window as a parameter of a pure function, DOM initialisation after the first render. Not under libs/api and apps/api.
---
<!-- rt-kit v0.34.0 · patterns/platform-access-di.md · 1483daf56f8c · правится надстройкой, не здесь -->

# The window, the document and the environment check

Pattern of the rule `platform-access`. What must be true — the law
`docs/constitution/frontend-application.md`.

## When to use

- `window`, `document` or an environment check enters a component, a service or a directive.
- DOM work appears that must not happen before the first render.
- A pure function needs access to the window.

## Injects

```typescript
import { DOCUMENT } from '@angular/common';
import { inject, Injectable } from '@angular/core';

import { PlatformService, WINDOW } from '@rt-tools/core';

@Injectable({ providedIn: 'root' })
export class SomeService {
    readonly #document: Document = inject(DOCUMENT);
    readonly #platform: PlatformService = inject(PlatformService);
    readonly #window: Window = inject(WINDOW);
}
```

## When `Window & typeof globalThis` is needed

The `Window` interface does not describe the global constructors and namespaces —
`IntersectionObserver`, `ResizeObserver`, `google` from `@types/google.maps`. The token returns
the very same object, so the type is narrowed by a cast, and a comment with the reason is put
next to it:

```typescript
// Constructors like IntersectionObserver are declared on globalThis, not on the
// Window interface — the token returns the same object, only the type is narrowed.
readonly #window: Window & typeof globalThis = inject(WINDOW) as Window & typeof globalThis;
```

## A pure function takes the window as a parameter

There is no DI in `*.logic.ts` and `*.util.ts`, and the global is not pulled inside:

```typescript
export function mapsReady(windowRef: Window & typeof globalThis): boolean {
    return typeof windowRef.google?.maps?.importLibrary === 'function';
}
```

The calling component injects it.

## The environment check and the first render

```typescript
if (!this.#platform.isPlatformBrowser) {
    return;
}
```

```typescript
afterNextRender((): void => {
    // DOM work that must not happen before the first render
});
```

`typeof window !== 'undefined'` is no good: a check by the presence of a global is right by
accident.

## Common misses

- `isPlatformBrowser(inject(PLATFORM_ID))` instead of `PlatformService`.
- An environment check around a read and a write to storage: `StorageService` falls back to
  memory outside the browser anyway, and such an `if` is dead code.
- `WINDOW` as a class field in a service that must work without a DOM at all: there the window
  is taken inside a method under an environment check.
- An edit added `WINDOW` to a service created at startup, and it was checked by the build alone:
  the failure shows only on a running page-rendering server.
- A cast without a comment: in mappers a cast is forbidden, and the line reads as a violation.
