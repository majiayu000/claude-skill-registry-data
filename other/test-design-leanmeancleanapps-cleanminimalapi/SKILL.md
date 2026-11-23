---
name: test-design
description: What a complete set of tests is for a change - the happy path, every documented failure, both sides of every boundary, the cancellation token and one request per status code - written as Arrange, Act, Assert with one behaviour per test. Use when deciding which tests to write, reviewing tests, fixing a bug, or when coverage is met but you're not sure the behaviour is.
metadata:
  scope: shared
---

# Test design

## The rule

Tests prove behaviour, positive and negative. Coverage is the floor the pipeline checks, not the goal: a change is tested when every behaviour it adds or changes has a test that would fail if that behaviour broke.

Every test has `// Arrange`, `// Act` and `// Assert` sections, tests one behaviour, and is named `Method_Should<Outcome>_<Condition>` so a failure reads as a sentence.

What each kind of code needs:

| Code | Positive cases | Negative cases |
| --- | --- | --- |
| Validator | A valid request has no errors; each allowed boundary value passes | One failing case per rule, asserting the message; each value just outside a boundary fails |
| Handler | The happy path returns the expected result and passes the request's values and the token to the repository | Each documented failure (not found, conflict) throws the right exception, and later calls don't happen |
| Repository | The right rows come back or change, in the right order, with paging and search applied | Unknown ids return null or false; nothing else changes |
| Endpoint, tool, resolver or function | One test per documented success status | One test per documented failure status (validation problem, not found, unauthorised) with the problem body checked |
| Behaviour or middleware | It calls the next step and passes the result through | It stops the request when it should, and the next step isn't called |

## Steps

1. List the behaviours before writing a test: what the code promises, and every way it can say no. The XML docs and the documented response codes are a good checklist.
2. For each range or limit, test both sides: the last value allowed and the first value refused (stars `1` and `5` pass, `0` and `6` fail; limit `50` passes, `51` fails). Use a `[Theory]` with `[InlineData]` for each side.
3. Assert outcomes, not just that nothing threw: the returned value, the exception type and message, the status code and body, and the calls made with their exact arguments.
4. Assert that the cancellation token reaches every repository call (`cancellation`).
5. On a negative path, assert that the work after the failure didn't happen (`DidNotReceiveWithAnyArgs()`).
6. Fixing a bug? Write the test that shows it first, watch it fail, then fix the code.
7. Run the coverage command (`coverage`) last, to find behaviour you forgot, not to pick lines to cover.

## Example

```csharp
// tests/Application.Tests.Unit/Reviews/Commands/CreateReview/CreateReviewValidatorTests.cs
[Theory]
[InlineData(-1)]
[InlineData(0)]
[InlineData(6)]
[InlineData(100)]
[InlineData(-100)]
public void Validator_ShouldHaveValidationErrorFor_Stars(int stars)
```

```csharp
// tests/Application.Tests.Unit/Reviews/Commands/UpdateReview/UpdateReviewHandlerTests.cs
[Fact]
public async Task Handle_ShouldThrowException_ReviewDoesNotExist()
{
    // Arrange
    var command = new UpdateReviewCommand { Id = Guid.NewGuid(), Stars = 5 };
    var reviewsRepository = Substitute.For<IReviewsRepository>();
    _ = reviewsRepository.UpdateReview(default, default, default).ReturnsForAnyArgs((Review?)null);
    var handler = new UpdateReviewHandler(reviewsRepository);
    using var tokenSource = new CancellationTokenSource();
    var token = tokenSource.Token;

    // Act
    var exception = await Should.ThrowAsync<NotFoundException>(async () => await handler.Handle(command, token));

    // Assert
    exception.Message.ShouldBe("The Review with the supplied id was not found.");
    _ = await reviewsRepository.Received(1).UpdateReview(command.Id, command.Stars, command.Text, token);
}
```

## Don't

- Stop at the happy path.
- Put two behaviours in one test, or loop over unrelated cases in one `[Fact]`.
- Write a test with no assertion, or one that can't fail.
- Test only values in the middle of a range.
- Assert on log output or private state.
- Use random data where the value matters to the assertion. Pick it, or find a known row (`sample-data`).

## Check

``` bash
dotnet test
```

Then read the test names for the class you changed. Each behaviour, success and failure, should have its own line.
