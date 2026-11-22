---
name: dotnet-test
description: >
  .NET / C# test rules using NUnit with NSubstitute and Shouldly (structure, mocking,
  assertions, coverage). Use when writing or running tests in a .NET project.
---

## Prerequisites

- .NET SDK
- Test project with NUnit, NSubstitute, Shouldly NuGet packages

## Test Runner

- **Framework**: NUnit · **Mocking**: NSubstitute · **Assertions**: Shouldly
- **Run all**: `dotnet test`
- **Run single**: `dotnet test --filter "FullyQualifiedName~Namespace.Tests.ClassName"`
- **Targeted run** (per commit): `dotnet test --filter "FullyQualifiedName~<Name>"` for the test classes of the changed code (`--no-build` after an own build); unknown mapping: the unit group (`--filter "TestCategory=UnitTest"`)
- **Coverage**: `dotnet test --collect:"XPlat Code Coverage"` writes `coverage.cobertura.xml` to `TestResults/`; convert with `reportgenerator`

## Conventions

- File naming: `{ClassName}Tests.cs` in the `test/<Project>.Tests` project, mirroring `src/`
- Namespace matches the source project with `.Tests` suffix
- Test method naming: `Should_<expected>_when_<condition>`
- Categories: `[Category("UnitTest")]` for unit, `[Category("IntegrationTest")]` for integration, `[Category("ManualTest")]` + `[Explicit]` for manual
- One test class per source class; one test method per scenario; AAA structure

## Test structure

```csharp
[Test]
[Category("UnitTest")]
public async Task Should_return_user_when_valid_id()
{
    repo.GetByIdAsync("123", Arg.Any<CancellationToken>()).Returns(new User { Id = "123" });
    var result = await sut.GetUserAsync("123");
    result.ShouldNotBeNull();
    result.Id.ShouldBe("123");
}
```

## Gotchas

- Always set a `[Category(...)]` so test filtering stays consistent
- Put the test project under `test/<ProjectName>.Tests`, not alongside the source project
