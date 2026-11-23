---
name: packages-and-dependencies
description: How NuGet packages are managed with Central Package Management and a monthly update, and which packages are not allowed. Use when adding, updating or removing a package.
metadata:
  scope: shared
---

# Packages and dependencies

## The rule

Versions live in one file, `Directory.Packages.props`, and project files only name the package. Packages are updated once a month, all together in one pull request. If the repository has `.github/dependabot.yml`, Dependabot opens that pull request. If it doesn't, update by hand: `dotnet list package --outdated` lists what's behind. Every package must be free and open source, with no paid or commercial licence tier.

## Steps

1. Look for something already in the solution or in the .NET base libraries first.
2. Check the licence. MIT, Apache 2.0 and BSD are fine. Anything that needs a paid licence for some users is out.
3. Add `<PackageVersion Include="Name" Version="x.y.z" />` to `Directory.Packages.props`, in alphabetical order.
4. Add `<PackageReference Include="Name" />` (no version) to the project that needs it. Analysers and build-only tools get `PrivateAssets` `all`.
5. A package used by Application or Infrastructure is shared code; in the template repository it must be added to all five templates.
6. Build and test. The pipeline's dependency review fails on known vulnerabilities and disallowed licences.

## Don't

- Put `Version=` on a `PackageReference`.
- Add MediatR, MassTransit (v9 and later), AutoMapper, FluentAssertions (v8 and later), or any other library that moved to a commercial licence. Use `Mediator`, `Riok.Mapperly` and `Shouldly`.
- Add a package to quiet a warning or save a few lines.
- Update one package on its own between the monthly updates unless it fixes a vulnerability.

## Check

``` bash
dotnet restore
dotnet build
dotnet list package --vulnerable
dotnet list package --outdated
```
