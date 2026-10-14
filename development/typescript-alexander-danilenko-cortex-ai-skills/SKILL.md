---
name: typescript
description: "Apply these opinionated TypeScript conventions whenever writing or reviewing TypeScript: branded types for domain modeling, discriminated unions for state, `satisfies` over `as`, const objects instead of enums, type-only imports, and the strict tsconfig baseline beyond `strict: true`. Also use for monorepo project references and incremental build setup."
---

# TypeScript

House conventions for TypeScript 5+. Apply them to code you are writing or changing — don't refactor untouched files to match unless asked.

## Conventions

- **Model the domain in types, not in checks.** Branded types (`type UserId = string & { readonly __brand: 'UserId' }`) and discriminated unions push errors to compile time, where they cost nothing. A runtime guard catches the same bug in production.
- **Discriminated unions for anything with states** — request lifecycles, form state, parse results. The compiler then forces every state to be handled, so a new variant surfaces as an error rather than a silent fallthrough.
- **`satisfies` over `as`.** `satisfies` validates against a type while keeping the narrow inferred literal; `as` throws the check away. Reach for `as` only when you know something the compiler cannot, and say why in a comment.
- **Const objects over `enum`.** `as const` objects are plain values with no emit and no nominal-typing surprises; `enum` generates runtime code and `const enum` breaks under `isolatedModules`.
- **`any` is a bug report.** Use `unknown` and narrow. If `any` is genuinely unavoidable at a boundary, isolate it in one adapter function rather than letting it spread through call sites.
- **Separate type-only imports** (`import type { … }`). Bundlers erase them cleanly; mixed imports can keep a runtime dependency alive that you meant to drop.
- **Let inference work.** Annotate exported/public signatures and let everything internal infer — over-annotation is noise that drifts from the real type.
- **Ship `.d.ts` for anything consumed as a library** (`declaration: true`). Without it, consumers fall back to `any` and your type work stops at the package boundary.
- **Monorepos: project references + `composite`.** Incremental builds only rebuild what changed; a single flat `tsconfig` recompiles the world on every edit.

## The two idioms worth showing

Exhaustiveness only actually holds if you force it. A `switch` over a union compiles fine when a new variant appears — `assertNever` is what turns that into a build error at every site that needed updating:

```typescript
function assertNever(x: never): never {
  throw new Error(`Unhandled variant: ${JSON.stringify(x)}`);
}

function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.r ** 2;
    case "rect":
      return s.w * s.h;
    default:
      return assertNever(s); // add a variant → compile error here
  }
}
```

A brand is only worth having if the sole way to obtain one is a function that validates:

```typescript
type Brand<T, B> = T & { readonly __brand: B };
type Email = Brand<string, "Email">;

export function toEmail(raw: string): Email {
  if (!raw.includes("@")) throw new Error(`Not an email: ${raw}`);
  return raw as Email;
}
```

The `as` inside the constructor is the one legitimate use — it's the boundary where validation converts an unverified value into a verified one. Casting to `Email` anywhere else defeats the whole type.

## tsconfig baseline

`strict: true` does not enable everything worth having. Add these — each one catches a class of bug the default set misses:

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "isolatedModules": true,
    "declaration": true,
    "skipLibCheck": true
  }
}
```

`noUncheckedIndexedAccess` is the highest-value one and the most disruptive to adopt: it makes `arr[i]` return `T | undefined`, which is the truth. Turn it on for new projects; for existing ones, expect a migration.

Module resolution: `NodeNext` when Node runs the output, `bundler` when a bundler does.
