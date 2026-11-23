---
name: errors-and-exceptions
description: How Application reports not found and invalid input with exceptions, and how the presentation layer turns them into responses. Use when a use case can fail, when adding a new error case, or when changing how errors reach the caller.
metadata:
  scope: shared
---

# Errors and exceptions

## The rule

Application signals failure by throwing; it never returns error codes or result objects.

| Situation | Thrown by | Exception |
| --- | --- | --- |
| Input breaks a rule | `ValidationBehaviour`, from the validator | `FluentValidation.ValidationException` |
| Something referenced doesn't exist | The handler | `NotFoundException` (`src/Application/Common/Exceptions/NotFoundException.cs`) |
| Anything else | Wherever | Left alone; the presentation layer reports it as an unexpected error |

The presentation layer maps each exception to its own shape in one place (in a web API, an `IExceptionHandler` writing RFC 9457 problem details). Messages are written for the caller and never include stack traces or internal details.

`LoggingBehaviour` logs validation failures and not found as `Information`, because the caller got an answer. The presentation layer's handler logs anything unexpected as `Error`, with the exception, in the same place it reports it (`serilog`).

## Steps

1. For a missing entity, use the helpers rather than `throw new`:
   - `NotFoundException.ThrowIfNull(result, EntityType.Movie);` after a fetch, or after an update that returns the changed entity, or `null` when no row matched.
   - `NotFoundException.Throw(EntityType.Review);` when a delete changed no rows.
   - `NotFoundException.Throw(EntityType.Author);` after an existence check. Only check first when the write itself can't tell you which thing is missing, such as a new review's author and movie.
2. A new kind of entity needs a value in `EntityType` (`src/Application/Common/Enums/EntityType.cs`).
3. Test the not-found path in the handler tests with `Should.ThrowAsync<NotFoundException>`.
4. If you add a new exception type, map it in the presentation layer's error handler in the same change, and test the mapping. If the caller should see it as an answer rather than a fault, log it in `LoggingBehaviour` too.
5. Test that the handler logs an unexpected exception once, as `Error`, and logs nothing for the ones it maps (`unit-tests`).

## Example

```csharp
// src/Application/Reviews/Commands/UpdateReview/UpdateReviewHandler.cs
var review = await reviewsRepository.UpdateReview(request.Id, request.Stars, request.Text, cancellationToken);

NotFoundException.ThrowIfNull(review, EntityType.Review);

return review;
```

```csharp
// src/Application/Reviews/Commands/CreateReview/CreateReviewHandler.cs
if (!await authorsRepository.AuthorExists(request.AuthorId, cancellationToken))
{
    NotFoundException.Throw(EntityType.Author);
}
```

`Throw` is marked `[DoesNotReturn]` and `ThrowIfNull` is marked `[NotNull]`, so the compiler knows the value isn't null afterwards and nullable warnings stay quiet.

## Don't

- Return `null`, `false` or an empty result to mean "not found" from a handler.
- Catch exceptions in a handler to turn them into something else.
- Introduce a `Result<T>` type. We use exceptions on purpose.
- Check that a row exists and then update or delete it. That's two trips and a race; let the write tell you.
- Put a stack trace, SQL or exception type name in a message.

## Check

``` bash
dotnet test --filter "FullyQualifiedName~NotFound|FullyQualifiedName~ExceptionHandler"
```
