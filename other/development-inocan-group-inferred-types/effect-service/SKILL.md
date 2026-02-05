---
name: effect-service
description: Generate new Effect-TS services with proper patterns. Use when creating new services, layers, or adding methods to existing services.
---

# Effect Service Generator

Generate Effect-TS services following project conventions.

## Service Template

```ts
import * as Context from "effect/Context";
import * as Effect from "effect/Effect";
import * as Layer from "effect/Layer";

// Interface defines the contract
export interface MyServiceInterface {
  readonly doSomething: (
    input: InputType,
  ) => Effect.Effect<OutputType, MyError>;
}

// Tag for dependency injection
export class MyService extends Context.Tag("@wowlab/services/MyService")<
  MyService,
  MyServiceInterface
>() {}

// Live implementation
export const MyServiceLive: Layer.Layer<MyService, never, Dependencies> =
  Layer.effect(
    MyService,
    Effect.gen(function* () {
      const dep = yield* SomeDependency;

      return {
        doSomething: (input) =>
          Effect.gen(function* () {
            // implementation
            return result;
          }),
      } satisfies MyServiceInterface;
    }),
  );
```

## Alternative: Effect.Service Pattern

For simpler services with built-in Default layer:

```ts
export class MyService extends Effect.Service<MyService>()("MyService", {
  dependencies: [Dep1.Default, Dep2.Default],
  effect: Effect.gen(function* () {
    const dep1 = yield* Dep1;
    const dep2 = yield* Dep2;

    return {
      doSomething: (input) => Effect.gen(function* () { ... }),
    };
  }),
}) {}
```

## File Location

- New service: `packages/wowlab-services/src/internal/{domain}/`
- Re-export from: `packages/wowlab-services/src/{Domain}.ts`

## Naming Conventions

- Interface: `{Name}Interface` or `{Name}Service`
- Tag: `@wowlab/services/{Name}`
- Layer: `{Name}Live` or `{Name}.Default`
- Errors: `{Name}Error` using `Data.TaggedError`

## Instructions

1. Ask what the service should do
2. Identify dependencies needed
3. Generate interface with typed methods
4. Generate Layer implementation
5. Add re-export to barrel file
