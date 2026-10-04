---
id: typescript.strict-types.avoid-any
name: Avoid Any
description: >
  Improves TypeScript safety by replacing unnecessary any usage with unknown, interfaces, DTOs, type guards, or generics.
stack:
  - TypeScript
category: strict-types
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - any
  - unknown
  - strict typing
  - type guard
  - DTO
  - generic
---

# Avoid Any

## Purpose

Use this skill to remove unsafe `any` usage and preserve TypeScript's ability to detect mistakes. The goal is to make data contracts explicit without overcomplicating the code.

## When to Use

Use this skill when:

- Code declares variables, parameters, return values, or collections as `any`.
- API responses, event payloads, or external data are untyped.
- Type assertions hide unsafe assumptions.
- A function can be expressed with generics instead of `any`.
- Strict TypeScript settings are enabled or being introduced.

## Do

Use explicit domain types when the shape is known:

```ts
interface UserDto {
  id: string;
  name: string;
  enabled: boolean;
}

function mapUser(dto: UserDto): UserViewModel {
  return {
    id: dto.id,
    displayName: dto.name,
    isActive: dto.enabled,
  };
}
```

Use `unknown` for untrusted input, then narrow it:

```ts
function isUserDto(value: unknown): value is UserDto {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    "enabled" in value
  );
}
```

Use generics when the function should preserve a caller-provided type:

```ts
function firstItem<T>(items: readonly T[]): T | undefined {
  return items[0];
}
```

Use narrow temporary types at integration boundaries:

```ts
type UnknownRecord = Record<string, unknown>;
```

## Do Not

Avoid using `any` as a shortcut:

```ts
function mapUser(dto: any): any {
  return {
    id: dto.id,
    displayName: dto.name,
  };
}
```

Avoid unsafe assertions that skip validation:

```ts
const user = response as UserDto;
```

Avoid replacing `any` with broad types that still hide the contract:

```ts
const payload: object = response;
```

Use temporary `any` only when there is a clear boundary, migration reason, and follow-up path. Keep it local, documented by naming or surrounding context, and do not leak it through public APIs.

## Review Checklist

- [ ] Public function parameters and return values do not use `any`.
- [ ] External data uses `unknown` until validated or mapped.
- [ ] Known data shapes are represented with interfaces, type aliases, or DTOs.
- [ ] Reusable utilities use generics instead of `any`.
- [ ] Type guards or schema validation protect untrusted inputs.
- [ ] Type assertions are narrow and justified.
- [ ] Temporary `any` usage is isolated and does not spread through the codebase.
- [ ] Tests cover mapper or guard behavior when runtime data can vary.

## Expected Output

1. Locate unsafe `any` usage and identify the data boundary.
2. Replace `any` with the narrowest practical type.
3. Use `unknown` plus narrowing for untrusted input.
4. Add interfaces, DTOs, type guards, or generics where they improve safety.
5. Avoid broad rewrites that are unrelated to type safety.
