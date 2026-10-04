---
name: go-developer
description: Applies modern Go semantics, type safety, and secure secret handling when writing or refactoring Go. Use this skill when writing or changing Go code.
---
# Go Developer (Modern Go)

Target the latest stable Go release unless the project's `go.mod` pins an older one.
Confirm the toolchain in use with `go version` and check the release notes before relying on a recent language or standard-library feature.

## Prefer Generics Over `interface{}`

- Use type parameters instead of `interface{}` (or `any` as a type) when the same logic applies to multiple concrete types.
- Reserve `any` for true heterogeneous data (e.g. JSON unmarshaling, plugin payloads).
  Do not use it to avoid defining a proper type or constraint.

### Preferred Generic Form

```go
func First[T any](s []T) (T, bool) {
    if len(s) == 0 {
        var zero T
        return zero, false
    }
    return s[0], true
}
```

### Avoided Interface Form

```go
func First(s []interface{}) (interface{}, bool) { ... }
```

- Use **constraints** for bounded generics: `comparable` (==, !=), `cmp.Ordered` (ordering), or custom interfaces.
  Use `~T` for underlying-type constraints (e.g. `~int64` for type-safe IDs).
- Prefer generic containers (e.g. `Stack[T]`, `Set[T]`) over `[]interface{}` or reflection.

## Type Parameters and Constraints

- Define small, purpose-built constraints; use `any` only when no constraint applies.
- Use the stdlib `slices`, `maps`, and `cmp` packages instead of hand-rolled loops where they improve clarity.
- Use a **generic type alias** (declared with `=`) to name an existing generic type without creating a new identity:

```go
type Set[T comparable] = map[T]struct{}  // generic alias
type StringSet = Set[string]             // instantiated alias
```

- Use a **defined type** when you want a distinct identity, such as a type-safe identifier:

```go
type UserID string  // distinct from string; use ~string in a constraint to accept it
```

## Interfaces

- **Define interfaces at the consumer**, not at the implementer.
  Keep them small (one to three methods).
- Prefer **accept interfaces, return structs**: callers depend on behavior; return concrete types for clarity and evolution.
- Do not introduce interfaces "for testing" before there is a second implementation or a clear boundary (e.g. I/O).
  Use small interfaces when a dependency is injected.
- For **heterogeneous collections** where behavior varies by type, prefer generics or a small interface with a clear contract over `interface{}`.

## Values and Pointers

- Use **values** by default.
  Use pointers when the value is large and copied often, the type must be mutable and shared, or the type has a `nil` meaning.
- Prefer **value receivers** unless the method must mutate the receiver or the struct is large.
  Consistency within a type matters more than a single large copy.
- Do not take a pointer to pass a slice, map, or string to avoid copying; they are reference-like.
  Copy the slice header only when needed (e.g. append and reassign).

## Errors

- **Wrap** with `fmt.Errorf("context: %w", err)` so callers can use `errors.Is` / `errors.As`.
- Prefer **typed errors**: define error types (structs implementing `error`, with `Unwrap() error` when wrapping) so callers can use `errors.As` to extract and handle specific cases with context.
  Use sentinel errors only when a single global identity check with no extra data is sufficient.
- Return errors; do not log and return a new error unless the log is a side effect the caller cannot perform.
  Let the caller decide logging.

## Slices and Maps

- Prefer `len(s) == 0` over comparing to `nil` when checking for "no elements"; treat nil and empty as equivalent for "no elements" in APIs.
- **Preallocate** when the final size is known: `make([]T, 0, n)`.
- Prefer `slices.Clone`, `slices.Concat`, and `maps.Clone` over manual copying when they match the intent.
- For iteration, consider range-over-func iterators and the `iter` package helpers such as `slices.All` where they simplify code; do not force iterator style where a simple `for` is clearer.

## Secret Handling With `secret.Do`

- `runtime/secret` is not generally available.
  Verify its status in the release notes for the toolchain in use before relying on it: it has shipped behind the `goexperiment.runtimesecret` build tag and only on some operating systems and architectures.
  Check with `go doc runtime/secret` and treat a build-constraint error as "unsupported on this build".
- Where the toolchain and platform do support it, code that handles credentials, tokens, keys, decrypted plaintext, or other secret-bearing data **must** run the complete secret-bearing call tree inside `secret.Do`.
- Import `runtime/secret` as `secret`; the Go API is `secret.Do` (not `secrets.Do`).
- Put the experiment check in one shared, build-tag-gated wrapper package in the module (for example `internal/secretutil`) instead of scattering experiment checks or direct `runtime/secret` imports throughout the codebase.
- Call the wrapper unconditionally from secret-bearing code so supported builds use `secret.Do` automatically and unsupported builds retain the same control flow.
- Keep secret creation, transformation, comparison, serialization, and consumption inside the callback.
  Do not return secret-bearing buffers or closures from it, because that defeats the protected lifetime.
- The unsupported-build fallback may invoke the callback directly, but it does **not** replace best-effort secure erasure.
  Prefer mutable byte buffers over strings for secrets and explicitly zero secret-bearing buffers before releasing them.
- Never log secrets, include them in errors, or retain unnecessary copies, regardless of `secret.Do` availability.
- Test that the wrapper invokes its callback in every build mode; when CI can enable the experiment, test the `runtime/secret` build-tag path too.

### Supported Build Wrapper

```go
//go:build goexperiment.runtimesecret

package secretutil

import "runtime/secret"

func RunWithSecret(f func()) {
    secret.Do(f)
}
```

### Fallback Build Wrapper

```go
//go:build !goexperiment.runtimesecret

package secretutil

// RunWithSecret preserves the call shape when runtime/secret is unavailable.
// Callers must still zero secret-bearing mutable buffers.
func RunWithSecret(f func()) {
    f()
}
```

### Recommended Wrapper Usage

Use the project wrapper around the full secret-bearing operation:

```go
secretutil.RunWithSecret(func() {
    plaintext := decrypt(ciphertext)
    defer clear(plaintext)
    consume(plaintext)
})
```

## Context and Concurrency

- Pass `context.Context` as the **first parameter**; do not store it in structs.
  Use it for cancellation and timeouts.
- Prefer **structured concurrency**: start goroutines with a clear lifecycle and ensure they exit when context is cancelled or a done channel closes.
  Avoid unbounded goroutine spawning.
- Prefer channels or sync primitives for communication; avoid shared mutable state.
  When sharing data, document who owns it and when it is safe to read or write.

## Standard Library and Modules

- Use **module-aware** builds only; set the `go` directive in `go.mod` to the oldest release that provides every language and standard-library feature the module uses, and verify that claim against the release notes rather than from memory.
- Prefer `slices`, `maps`, `cmp`, and (where helpful) `iter` over hand-written loops and third-party collections for simple cases.
- Do not use deprecated stdlib APIs; check release notes when upgrading.

## Anti-Patterns to Avoid

- **Bare `interface{}` / `any`** when a type parameter or a small interface would express the contract.
- **Reflection** for polymorphism that generics or interfaces can express.
- **Pointer to slice/map** just to pass them; pass by value unless you need to reassign the slice/map itself in the callee.
- **Init-side effects**: avoid `init()` that mutates global state or registers handlers; use explicit setup in `main` or tests.
- **Over-genericizing**: do not add type parameters "for flexibility" when there is only one concrete type today; add them when you have two or more concrete types or a clear constraint.
- **Unprotected secret handling**: do not bypass the shared `secret.Do` compatibility wrapper on systems that support `runtime/secret`, and do not omit best-effort buffer erasure on fallback systems.

## Quick Reference

- **Reusable container/algorithm over multiple types:** generics with a constraint
- **"Any type" with no operations:** `any` only when truly heterogeneous
- **Ordering or comparison:** `cmp.Ordered`, `cmp.Less`, or custom constraint
- **Slice utilities:** `slices` (Contains, Clone, Sort, etc.)
- **Map utilities:** `maps` (Clone, Keys, Values, etc.)
- **Error handling:** typed errors + `errors.As`; wrap with `%w`; use sentinels only when identity-without-context is enough
- **Secret-bearing code:** shared build-tagged wrapper that calls `secret.Do` when supported; explicit buffer erasure in every build
- **Optional value:** `T` + `bool`, or a small `Result[T]` type; avoid `*T` for "optional" unless nil is meaningful
