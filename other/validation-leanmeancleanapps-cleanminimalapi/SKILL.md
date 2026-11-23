---
name: validation
description: How request validation works with FluentValidation and the ValidationBehaviour pipeline, including message wording and the shared paging rules. Use when adding or changing a validator, or when a request needs a new rule.
metadata:
  scope: shared
---

# Validation

## The rule

All input rules live in one place: a FluentValidation validator next to the request in Application. `ValidationBehaviour` runs every validator for a request before its handler and throws `FluentValidation.ValidationException` with all failures. Each presentation layer turns that into its own "bad request" shape. Nothing else validates input.

Validators check the shape of a request: ids present, values in range, text the right length. Handlers check anything that needs storage, such as whether a movie exists. So validators are synchronous, take no dependencies and never call a repository.

Validators are found by `AddValidatorsFromAssembly` in `src/Application/DependencyInjection.cs`, so a new one needs no registration.

## Steps

1. Create `<UseCase>Validator.cs` beside the request: `public class XValidator : AbstractValidator<XRequest>`.
2. Add one `RuleFor` per property, each discarded with `_ =` and qualified with `this.`.
3. Write the message for a person reading an API error: what's wrong and what's allowed. End with a full stop.
4. Paged queries use the shared extensions in `src/Application/Common/Paging/PagingValidatorExtensions.cs`: `ValidOffset()`, `ValidLimit()`, `ValidSearchTerm()`.
5. Test every rule (`unit-tests`, `test-design`): one valid case, one failing case per rule, and both sides of every boundary in a `[Theory]`.

## Example

```csharp
// src/Application/Reviews/Commands/CreateReview/CreateReviewValidator.cs
public class CreateReviewValidator : AbstractValidator<CreateReviewCommand>
{
    public CreateReviewValidator()
    {
        _ = this.RuleFor(r => r.AuthorId).NotEqual(Guid.Empty).WithMessage("An author id was not supplied to create the review.");
        _ = this.RuleFor(r => r.MovieId).NotEqual(Guid.Empty).WithMessage("A movie id was not supplied to create the review.");
        _ = this.RuleFor(r => r.Stars).InclusiveBetween(1, 5).WithMessage("A star rating must be between 1 and 5.");
    }
}
```

```csharp
// src/Application/Movies/Queries/GetMovies/GetMoviesValidator.cs
_ = this.RuleFor(r => r.Query).ValidSearchTerm();
_ = this.RuleFor(r => r.Offset).ValidOffset();
_ = this.RuleFor(r => r.Limit).ValidLimit();
```

A rule shared by several requests becomes an extension method on `IRuleBuilder<T, TProperty>` returning `IRuleBuilderOptions<T, TProperty>`, with its message inside, like the paging ones.

## Don't

- Use data annotations (`[Required]`, `[Range]`) on requests.
- Check existence in a validator (does this movie exist?). That needs storage, so it's the handler's job and throws `NotFoundException` (`errors-and-exceptions`).
- Inject a repository or use `MustAsync` in a validator.
- Throw your own `ValidationException`. Let the behaviour do it.
- Write messages like "Invalid input" or "'Stars' must be between 1 and 5." (the FluentValidation default). Say it in a sentence.

## Check

``` bash
dotnet test tests/Application.Tests.Unit --filter "FullyQualifiedName~ValidatorTests"
```
