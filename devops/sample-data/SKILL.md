---
name: sample-data
description: How the sample data is seeded with Bogus behind the Database:SeedSampleData setting, and how tests get their own fixed data. Use when changing seed data, adding a column that needs sample values, or writing tests that depend on known data.
metadata:
  scope: shared
---

# Sample data

## The rule

There are two kinds of data, and they never mix.

| | Where | Used by | Shape |
| --- | --- | --- | --- |
| Sample data | `src/Infrastructure/Databases/MovieReviews/Extensions/MovieReviewsDbContextExtensions.cs` (`AddData`) | Local runs, Docker and the presentation integration tests | 15 authors, 50 movies, 150 reviews from Bogus with a fixed seed |
| Test data | `tests/Infrastructure.Tests.Integration/Databases/MovieReviews/Extensions/MovieReviewsCollectionData.cs` (`AddTestData`) | Repository tests | A handful of hand-written rows named "One", "Two", "Three" so assertions can find them |

Sample data is only added when `Database:SeedSampleData` is `true` (on in `appsettings.local.json` and `appsettings.docker.json`, off in `appsettings.json`; Lambda turns it on only in `docker-compose.yml`) and the database is empty. A deployed copy never starts with fake data.

## Steps

1. New column on a model? Add a `RuleFor` to the matching `Faker<T>` in `AddData`, and a value to the rows in `AddTestData` if tests need it.
2. Movie titles and review text come from the `Titles` and `ReviewTexts` lists in `AddData`. Keep them made up, with no real films, characters or brands, and keep a few titles for common searches such as "space" or "love".
3. Keep the fixed `Seed` and `ReferenceDate`. Dates come from `f.Date.Past(refDate: ReferenceDate)`, never from the clock, so every run gives the same data.
4. Tests that need a specific row look it up by its known value (`Authors.First(a => a.FirstName == "One")`), not by position.
5. Presentation integration tests that need a row with children pick one that has them. Bogus spreads reviews at random, so a few movies and authors have none.

## Don't

- Seed in a repository constructor or on every request. Seeding happens once, in `InitialiseInfrastructure()`.
- Turn `SeedSampleData` on in `appsettings.json`.
- Use `DateTime.Now`, `Guid.NewGuid()` or an unseeded `Faker` in sample data.
- Assert exact counts of sample data in presentation tests. They depend on the random spread; repository tests use the test data for exact counts.

## Check

``` bash
dotnet test
```
