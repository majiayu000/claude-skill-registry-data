---
name: unit-tests
description: How unit tests are written with xUnit, Shouldly and NSubstitute - folder layout, naming, Arrange/Act/Assert, testing validators and handlers, and asserting the cancellation token. Use when testing a handler, validator, endpoint or any class in isolation.
metadata:
  scope: shared
---

# Unit tests

## The rule

xUnit for tests, Shouldly for assertions, NSubstitute for fakes. Test folders mirror the source folders. `test-design` says which tests a change needs; this skill says how to write them. Each test has `// Arrange`, `// Act` and `// Assert` comments and tests one thing.

| Project | Tests |
| --- | --- |
| `tests/Application.Tests.Unit` | Handlers (repositories faked with NSubstitute) and validators (`FluentValidation.TestHelper`) |
| `tests/Presentation.Tests.Unit` | Presentation classes we wrote, called directly, with `ISender` faked where they send requests. Every template has this project; what goes in it depends on what its presentation layer holds |

Test the code we wrote, not the libraries under it. A unit test that only proves ASP.NET Core, Hot Chocolate, Mapperly or the AWS serializer does its job protects nothing of ours. Test our settings, error handlers and filters, transformers, option extensions and parsing, and leave the libraries' own behaviour to the libraries.

Names read as `Method_Should<Outcome>_<Condition>`: `Handle_ShouldThrowException_ReviewDoesNotExist`, `GetReviews_ShouldReturn_Ok`, `Validator_ShouldHaveValidationErrorFor_Id`.

## Steps

1. Create `<Class>Tests.cs` in the matching folder, for example `tests/Application.Tests.Unit/Reviews/Commands/UpdateReview/UpdateReviewHandlerTests.cs`.
2. Handlers: one test for the happy path, one per failure (not found, and so on). Fake each repository with `Substitute.For<I...Repository>()` and set returns with `ReturnsForAnyArgs` or `Returns` on specific arguments.
3. Assert the result, then assert the calls: `Received(1)` with the exact arguments and token, and `DidNotReceiveWithAnyArgs()` for calls that mustn't happen.
4. Validators: a static validator instance, one valid case with `ShouldNotHaveAnyValidationErrors()`, and a `[Theory]` per rule with `ShouldHaveValidationErrorFor(...)`.
5. Use a real `CancellationTokenSource` so you can prove the token was passed on (`cancellation`).
6. To check a log message, pass a `FakeLogger<T>` (`Microsoft.Extensions.Diagnostics.Testing`) and assert on `logger.Collector`: the count, then the level, message and exception of `LatestRecord`.

## Example

```csharp
// tests/Application.Tests.Unit/Reviews/Commands/UpdateReview/UpdateReviewHandlerTests.cs
[Fact]
public async Task Handle_ShouldReturnUpdatedReview_ReviewExists()
{
    // Arrange
    var command = new UpdateReviewCommand
    {
        Id = Guid.NewGuid(),
        Stars = 1
    };

    var review = new Review(command.Id, command.Stars);
    var reviewsRepository = Substitute.For<IReviewsRepository>();

    _ = reviewsRepository.UpdateReview(default, default, default).ReturnsForAnyArgs(review);

    var handler = new UpdateReviewHandler(reviewsRepository);
    using var tokenSource = new CancellationTokenSource();
    var token = tokenSource.Token;

    // Act
    var result = await handler.Handle(command, token);

    // Assert
    result.ShouldBe(review);

    _ = await reviewsRepository.Received(1).UpdateReview(command.Id, command.Stars, token);
}
```

```csharp
// tests/Application.Tests.Unit/Reviews/Commands/UpdateReview/UpdateReviewValidatorTests.cs
var result = Validator.TestValidate(command);

_ = result.ShouldHaveValidationErrorFor(command => command.Id);
```

## Don't

- Use `Assert.Equal` or FluentAssertions. Shouldly only.
- Use Moq. NSubstitute only.
- Test private methods, or test through the database in a unit test.
- Share mutable state between tests through static fields.
- Write a test that only exists to raise coverage without asserting behaviour.
- Re-test a library's behaviour, such as a framework's model binding or a serializer's defaults.

## Check

``` bash
dotnet test tests/Application.Tests.Unit
dotnet test tests/Presentation.Tests.Unit
```
