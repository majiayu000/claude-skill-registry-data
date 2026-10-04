---
name: bootgs-validation
description: Documents bootgs' parameter-level validation decorators (@Min, @Max, @Email, @Pattern, @Size, @NotBlank, @NotEmpty, @AssertTrue, @AssertFalse, @Positive, @PositiveOrZero, @Negative, @NegativeOrZero), the built-in Parse pipes, and how to write custom pipes with @UsePipes. Use when adding input validation or type coercion to a bootgs controller method, or when invalid input reaches a handler unrejected. Not for requests that never reach the handler at all — an apiPrefix or event-shape problem belongs to `bootgs-client` — nor for layering rules (`bootgs-architecture`).
license: Apache-2.0
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
  framework: bootgs
---

# Bootgs Validation

## Available files

- **`references/decorators-and-pipes.md`** — full list of validation decorators and Parse pipes. Load it when you need to check whether a specific constraint exists or what a pipe coerces to; the pattern for using them is below.

## Model

bootgs validates individual **parameters**, not whole DTO classes — there is no class-validator-style `@ValidateNested`/decorated-DTO pipeline. A validation decorator stacks on top of an extraction decorator (`@Query`, `@Param`, `@Body`) and runs against the already-extracted value before the handler body executes:

```ts
@Get()
findAll(
  @Query("page") @Min(1) page: number,
  @Query("limit") @Max(100) limit: number,
) { /* page and limit are guaranteed valid here */ }
```

Multiple validators stack freely on one parameter; each runs in decorator-application order. The available decorators — `@Min`, `@Max`, `@Email`, `@Pattern`, `@Size`, `@NotBlank`, `@NotEmpty`, `@AssertTrue`/`@AssertFalse`, `@Positive`/`@PositiveOrZero`, `@Negative`/`@NegativeOrZero` — are listed with their exact checks in `references/decorators-and-pipes.md`.

## Parse pipes (extraction-time coercion)

GAS delivers every parameter as a string. Use a Parse pipe as the **second argument** to `@Param`/`@Query` to coerce it before your handler sees it — don't hand-parse `Number(value)` in the handler body:

```ts
@Get("{id}")
findOne(@Param("id", ParseNumberPipe) id: number) { /* id is a number, not "42" */ }
```

Six are available (`ParseIntPipe`, `ParseFloatPipe`, `ParseBigIntPipe`, `ParseBooleanPipe`, `ParseNumberPipe`, `ParseStringPipe`) — see `references/decorators-and-pipes.md` for what each coerces to.

## Custom pipes

```ts
import { PipeTransform, ArgumentMetadata, UsePipes } from "bootgs";

class TrimPipe implements PipeTransform<string, string> {
  transform(value: string, metadata: ArgumentMetadata): string {
    return value.trim();
  }
}

@UsePipes(TrimPipe)
@Post()
create(@Body("name") name: string) { /* name is trimmed */ }
```

`@UsePipes` applies at the class or method level and accepts multiple pipes, run in order.

## Gotcha: validation failures throw a bare `Error`, not `HttpException`

Every built-in validation decorator throws `new Error("Validation failed (...)")` on failure — **not** `AppException`/`HttpException`. If your `@ControllerAdvice`/`@ExceptionHandler` only catches `AppException`, a validation failure falls through as an unhandled 500 instead of a clean 400. Handle it explicitly:

```ts
@ControllerAdvice()
class GlobalExceptionHandler {
  @ExceptionHandler(Error)
  handleValidation(err: Error) {
    return ResponseEntity.badRequest().body({ message: err.message });
  }
}
```

Order `@ExceptionHandler` registrations from most-specific to least-specific (`AppException` before the generic `Error` catch-all) if you need different status codes for domain exceptions versus validation failures.

## Verification

For each validation decorator you add, write one test that calls the handler with a value that should fail and assert the response status/message — a decorator with no corresponding negative test is unverified surface area, since bootgs doesn't type-check the constraint against the parameter's type at compile time (e.g. `@Email()` on a `number` parameter compiles fine and fails at runtime).
