---
name: fix-typescript-issue
description: >
  Debug and explain TypeScript errors step by step in a way that teaches as it fixes.
  Use this skill whenever a user shares a TypeScript error, compiler diagnostic, or type
  mismatch — regardless of how they phrase it (e.g. "TS2345", "why is this broken",
  "getting a red squiggle", "this doesn't compile", "type error", "help with my TypeScript").
  Also trigger when the user pastes a TypeScript snippet with a visible type issue, even if
  they haven't explicitly mentioned an error. Covers all TypeScript error categories: type
  mismatches, missing properties, incorrect generics, strict null checks, module resolution
  failures, interface violations, and misconfigured tsconfig options.
---

# Fix TypeScript Errors

This skill guides clear, educational debugging of TypeScript errors. The goal is to fix the issue _and_ help the user understand what went wrong — especially the underlying type system concept — so they can recognise it next time.

## What the user provides

- The error message (ideally the full `tsc` output or IDE tooltip, including the error code like `TS2345`)
- The file and/or location where the error appears (e.g. "line 18 in `api.ts`")
- The relevant code — either pasted inline or available in the workspace

If code is missing from the conversation, check the workspace before asking the user to paste it.

---

## Response structure

Always follow this exact structure. Keep each step brief but clear — one to three sentences per step is usually right. The user should be able to learn from the explanation, not just copy-paste the fix.

### Step 1 — Identify the error type

Name the error code and category (e.g. `TS2345 — Argument of type mismatch`) and explain in one sentence what that class of error means in TypeScript's type system.

### Step 2 — Pinpoint the cause

Point to the specific expression or declaration that triggered it. Explain _why_ it fails — what TypeScript inferred or expected versus what it actually received.

### Step 3 — Show the fix

Present the corrected code in a code block. If the change is small, show only the relevant lines with enough surrounding context to locate them. If the change is larger (e.g. an interface refactor), show the full relevant block. Where multiple valid fixes exist, show the most idiomatic one first and briefly mention the alternatives.

### Step 4 — Explain why the fix works

In one to two sentences, explain the mechanism: what does the corrected code do differently, and why does it satisfy the TypeScript compiler?

### Summary

End with a short bullet-point summary (no tables) covering:

- What the root cause was
- What the fix does
- Any general TypeScript principle worth remembering (e.g. "use a type guard before narrowing a union", "`unknown` requires explicit narrowing before use", "optional chaining doesn't narrow the type on its own")

---

## Tone and style guidelines

- **Teach the type system, don't just patch.** TypeScript errors often reflect a misunderstanding of how types flow. Surface that misunderstanding clearly.
- **Be concise.** Avoid lengthy preambles. Get to the diagnosis quickly.
- **Use plain language.** If you use a TypeScript-specific term (e.g. "union type", "type narrowing", "structural typing", "discriminated union"), define it briefly inline.
- **No tables in the summary.** Use bullet points only.
- **Match the user's level.** Beginners need the concept explained; experienced TS developers want the precise compiler reasoning.
- **One fix at a time.** If there are multiple errors, address the most fundamental one first — fixing it often resolves the others. Mention any remaining issues at the end.
- **Don't over-type.** Avoid suggesting `any` as a fix unless it's the last resort; prefer proper narrowing, type guards, or accurate type annotations.
- **Use context7 to follow modern documentation guidelines.**

---

## Common TypeScript error patterns — quick reference

Use these as a mental checklist when diagnosing:

- **TS2345 — Argument type mismatch**: The value passed doesn't match the parameter's expected type. Check for missing properties, wrong literal types, or a union that hasn't been narrowed.
- **TS2339 — Property does not exist**: Accessing a property that isn't on the type. Often caused by a typo, a missing interface field, or operating on `unknown` / a union without narrowing first.
- **TS2322 — Type not assignable**: Trying to assign a wider or incompatible type to a narrower one (e.g. `string | null` into `string`). Usually resolved with a null check or type assertion.
- **TS2531 / TS2532 — Object is possibly null/undefined**: Strict null checks are on and the value might be `null` or `undefined`. Use optional chaining (`?.`), a null guard, or non-null assertion (`!`) only when you're certain.
- **TS2551 / TS2304 — Cannot find name**: Variable or type is out of scope, not imported, or misspelled. Check imports and `tsconfig` `lib` / `types` settings.
- **TS2554 — Expected N arguments, got M**: Called a function with the wrong number of arguments. Check the signature — some parameters may need to be made optional.
- **TS7006 — Parameter implicitly has 'any' type**: `noImplicitAny` is enabled and a parameter lacks a type annotation. Add an explicit type.
- **TS2352 — Conversion of type may be a mistake**: A type assertion (`as`) is used between two types that don't overlap. Use `as unknown as T` only as a last resort; prefer a type guard instead.
- **TS2307 — Cannot find module**: Import path is wrong, the package has no type declarations, or `@types/…` is missing. Check the path, run `npm install`, or add a `.d.ts` declaration.
- **TS1005 / TS1128 — Syntax / Declaration expected**: Malformed TypeScript syntax. Often a missing bracket, semicolon, or incorrect generic syntax.

---

## TypeScript-specific debugging tips

**Read the full error chain.** TypeScript errors often come in chains — the first message names the error, but subsequent lines (indented with "Type '…' is not assignable to type '…'") show exactly where the mismatch occurs. Always read to the bottom of the chain before diagnosing.

**Check `tsconfig.json` for strictness flags.** Many errors only appear with `strict`, `strictNullChecks`, `noImplicitAny`, or `exactOptionalPropertyTypes` enabled. If the error seems surprising, note which flag is responsible.

**Distinguish type-level from value-level fixes.** Some errors are best fixed by correcting the _type annotation_ (the type was wrong), others by correcting the _value_ (the runtime data was wrong). Be clear about which kind of fix you're applying.

**Generics errors.** When a generic type parameter is the cause, show what TypeScript inferred (`T = string`) versus what was needed, then explain how to constrain or explicitly pass the type argument.

---

## Handling incomplete information

If the user gives an error but no code:

1. Check the workspace for relevant `.ts` / `.tsx` files before asking.
2. If no code is found, ask for the minimal snippet that reproduces the error — ideally including any relevant type definitions or interfaces.

If the error originates inside `node_modules` or a `.d.ts` file, focus on the _call site in user-owned code_ — that's almost always where the real mistake is.

If the error is environment-related (missing `@types` package, wrong `moduleResolution`, outdated TypeScript version), state that clearly and give the exact command or config change needed (e.g. `npm install --save-dev @types/node` or `"moduleResolution": "bundler"` in `tsconfig.json`).
