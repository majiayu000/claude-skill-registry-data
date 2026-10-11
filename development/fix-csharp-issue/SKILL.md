---
name: fix-csharp-issue
description: >
  Debug and explain how to fix C# and .NET errors step by step in a way that teaches as it fixes.
  Use this skill whenever a user shares a C# compiler error, .NET runtime exception, or build
  failure — regardless of how they phrase it (e.g. "CS0103", "why is this broken", "getting a
  red squiggle", "this doesn't compile", "NullReferenceException", "dotnet build fails",
  "help with my C#"). Also trigger when the user pastes a C# snippet with a visible issue,
  even if they haven't mentioned an error explicitly. Covers all C# error categories: compiler
  diagnostics (CS codes), runtime exceptions, nullable reference type warnings, async/await
  misuse, LINQ errors, EF Core failures, interface violations, and MSBuild/project issues.
---

# Fix C# / .NET Errors

This skill guides clear, educational debugging of C# and .NET errors. The goal is to fix the issue _and_ help the user understand what went wrong — especially the underlying language or framework concept — so they can recognise it next time.

## What the user provides

- The error message (ideally the full `dotnet build` output or IDE tooltip, including the error code like `CS0103`)
- The file and/or location where the error appears (e.g. "line 42 in `OrderService.cs`")
- The relevant code — either pasted inline or available in the workspace

If code is missing from the conversation, check the workspace before asking the user to paste it.

---

## Response structure

Always follow this exact structure. Keep each step brief but clear — one to three sentences per step. The user should learn from the explanation, not just copy-paste the fix.

### Step 1 — Identify the error type

Name the error code and category (e.g. `CS0103 — Name does not exist in current context`) and explain in one sentence what that class of error means in C#.

### Step 2 — Pinpoint the cause

Point to the specific expression or declaration that triggered it. Explain _why_ it fails — what the compiler expected or what the runtime encountered versus what it received.

### Step 3 — Show the fix

Present the corrected code in a code block. Show the relevant lines with enough surrounding context to locate them. Where multiple valid fixes exist, show the most idiomatic one first and briefly mention alternatives.

### Step 4 — Explain why the fix works

In one to two sentences, explain the mechanism: what does the corrected code do differently, and why does it satisfy the compiler or runtime?

### Summary

End with a short bullet-point summary (no tables) covering:

- What the root cause was
- What the fix does
- Any general C# / .NET principle worth remembering (e.g. "use `ArgumentNullException.ThrowIfNull` at method entry", "don't use sync-over-async", "nullable reference types require explicit null checks")

---

## Tone and style guidelines

- **Teach the language, don't just patch.** Errors often reflect a misunderstanding of the type system, async model, or framework contract. Surface that clearly.
- **Be concise.** Avoid lengthy preambles. Get to the diagnosis quickly.
- **Use plain language.** If you use a C#-specific term (e.g. "value type", "boxing", "captured variable", "discriminated union via pattern matching"), define it briefly inline.
- **No tables in the summary.** Use bullet points only.
- **Match the user's level.** Beginners need the concept explained; experienced .NET developers want the precise reasoning.
- **One fix at a time.** If there are multiple errors, address the most fundamental one first — fixing it often resolves the others. Mention remaining issues at the end.
- **Don't suppress warnings blindly.** Avoid `#pragma warning disable` or `!` null-forgiving operators as quick fixes; prefer proper null checks, guard clauses, or accurate type annotations.
- **Use context7 to follow modern documentation guidelines.**

---

## Common C# / .NET error patterns — quick reference

**Compiler errors (CS codes)**

- **CS0103 — Name does not exist in current context**: Variable, type, or method is out of scope, not imported, or misspelled. Check `using` directives and namespace declarations.
- **CS0246 — Type or namespace not found**: Missing `using`, missing NuGet package, or a typo in the type name. Check project references and installed packages.
- **CS0029 — Cannot implicitly convert type**: Assigning an incompatible type without an explicit cast. Add a cast, use `.ToString()`, or align the types.
- **CS0161 — Not all code paths return a value**: A non-void method has a branch that falls through without a `return`. Add the missing return or throw.
- **CS1998 — Async method lacks `await`**: A method is marked `async` but never awaits anything — it runs synchronously. Either add `await` or remove `async`/`Task`.
- **CS4014 — Call not awaited**: An async call result is discarded without `await`. This silently swallows exceptions. Add `await` or explicitly assign to `_ =` if fire-and-forget is intentional.
- **CS8600 / CS8602 / CS8604 — Nullable reference warnings**: Assigning `null` to a non-nullable reference, dereferencing a possibly-null value, or passing a nullable to a non-nullable parameter. Add null checks, use `?.`, or annotate with `?`.
- **CS0168 / CS0169 — Unused variable / field**: Declared but never used. Either use it, prefix a discard with `_`, or remove it.

**Runtime exceptions**

- **NullReferenceException**: Dereferencing an object that is `null`. Use null-conditional operators (`?.`), `ArgumentNullException.ThrowIfNull`, or guard clauses at method entry.
- **InvalidCastException**: Unsafe cast between incompatible types. Use `is` / `as` with a null/pattern check rather than direct `(T)` casts.
- **InvalidOperationException**: Calling a method on an object in an invalid state (e.g. enumerating a modified collection, using a disposed resource). Check preconditions before calling.
- **StackOverflowException**: Infinite recursion without a base case, or accidental infinite property getter. Trace the call chain and add a termination condition.
- **TaskCanceledException / OperationCanceledException**: A `CancellationToken` was signalled. Handle gracefully at call sites that may cancel; don't swallow it silently.
- **DbUpdateConcurrencyException (EF Core)**: Optimistic concurrency conflict. Implement a retry or last-write-wins strategy; never silently discard.
- **ObjectDisposedException**: Using a resource after `Dispose()` has been called. Ensure `using` scopes are correct and services aren't stored past their lifetime.

**Build / project issues**

- **MSBuild target framework mismatch**: Project references a library targeting a newer framework. Align `<TargetFramework>` values or use multi-targeting.
- **Duplicate assembly attribute**: Two files declare `[assembly: ...]` for the same attribute. Remove one, or add `<GenerateAssemblyInfo>false</GenerateAssemblyInfo>` if auto-generated.
- **Ambiguous reference**: Two `using` directives bring in the same type name. Use a fully-qualified name or a `using Alias = Full.Namespace.Type` alias.

---

## C# / .NET debugging tips

**Read the full error output.** `dotnet build` prints the innermost error last in the chain. Read all lines — secondary messages often contain the exact property or type that mismatched.

**Nullable annotations.** With `<Nullable>enable</Nullable>`, the compiler tracks nullability flow. `CS8602` on a dereference means the compiler can't prove the value is non-null at that point — add a null check rather than a `!` suppressor unless you have a genuine guarantee.

**Async pitfalls.** Never use `.Result` or `.Wait()` on a `Task` in ASP.NET Core — it causes deadlocks. Always `await`. If a method can't be `async`, restructure instead of using sync-over-async escape hatches.

**LINQ errors.** "Sequence contains no elements" means `.First()` / `.Single()` was called on an empty sequence — use `.FirstOrDefault()` and check for `null`. "LINQ to Entities does not support..." means a client-side method was used inside an EF Core query — move it to a separate `AsEnumerable()` step.

**Pattern matching over casting.** Prefer `if (obj is MyType t) { ... }` over `(MyType)obj` — it combines the type check and cast safely and is the idiomatic .NET approach.

---

## Handling incomplete information

If the user gives an error but no code:

1. Check the workspace for relevant `.cs` / `.csproj` files before asking.
2. If no code is found, ask for the minimal snippet that reproduces the error — ideally including relevant type definitions or interfaces.

If the error originates inside a NuGet package or generated code, focus on the _call site in user-owned code_ — that's almost always where the real mistake is.

If the error is environment-related (wrong SDK version, missing package, path issue), state so clearly and provide the exact command to fix it (e.g. `dotnet add package Foo` or `dotnet tool install --global dotnet-ef`).
