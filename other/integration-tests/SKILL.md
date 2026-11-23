---
name: integration-tests
description: How integration tests run against a real SQLite database - a private in-memory database per repository test, and a per-test application host with its own database for presentation tests. Use when testing the repository, migrations, startup wiring or a real request through the presentation layer.
metadata:
  scope: shared
---

# Integration tests

## The rule

Integration tests use the real database engine, built from the real migrations, and every test gets its own database. No test can see another test's changes, and nothing is written to disk.

| Project | Fixture | Database |
| --- | --- | --- |
| `tests/Infrastructure.Tests.Integration` | `MovieReviewsTestDatabase` | `Data Source=:memory:` held open for one test, with the hand-written test data (`sample-data`) and a `FakeTimeProvider` fixed at 2009-12-31 23:51:01 UTC |
| `tests/Presentation.Tests.Integration` | The presentation layer's application host (a `WebApplicationFactory<Program>` in web templates, the `Handler` itself in Lambda) | `Data Source=Tests-{Guid};Mode=Memory;Cache=Shared` with sample data on |

## Steps

1. Repository tests: make the test class `sealed` and `IDisposable`, create `private readonly MovieReviewsTestDatabase database = new();` and dispose it. Use `this.database.Repository`, and `this.database.Context` to find known rows.
2. Find rows by their known values, not by position.
3. For time-dependent results, assert against `this.database.TimeProvider`.
4. Presentation tests: create a new application host per test class instance, pass settings in through its constructor, and make real requests (in Lambda, real calls to the handler). Assert the status code, then the body.
5. Override settings in memory through the host's constructor, never by editing appsettings files or leaving environment variables set.
6. The details of this template's application host are in `presentation-integration-tests`.

## Example

```csharp
// tests/Infrastructure.Tests.Integration/Databases/MovieReviews/EntityFrameworkMovieReviewsRepositoryTests.cs
public sealed class EntityFrameworkMovieReviewsRepositoryTests : IDisposable
{
    private readonly MovieReviewsTestDatabase database = new();

    public void Dispose()
    {
        this.database.Dispose();
    }

    [Fact]
    public async Task GetAuthorById_ShouldReturn_Author()
    {
        // Arrange
        var repository = this.database.Repository;
        using var tokenSource = new CancellationTokenSource();
        var token = tokenSource.Token;
        var author = this.database.Context.Authors.First(a => a.FirstName == "One");

        // Act
        var result = await repository.GetAuthorById(author.Id, token);

        // Assert
        _ = result.ShouldNotBeNull();
        result.Reviews.Count.ShouldBe(3);
    }
}
```

## Don't

- Use the EF Core InMemory provider. It isn't relational and lets through queries SQLite rejects.
- Share one database across tests with `IClassFixture` or `ICollectionFixture`.
- Write to `movie-reviews.db` or any file.
- Depend on test order.

## Check

``` bash
dotnet test tests/Infrastructure.Tests.Integration
dotnet test tests/Presentation.Tests.Integration
```
