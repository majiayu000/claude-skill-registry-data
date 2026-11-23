---
name: mapping-with-mapperly
description: How database models map to Application entities with the Mapperly source generator, including ignored members and RMG warnings. Use when adding a property to a model or entity, or adding a new mapping.
metadata:
  scope: shared
---

# Mapping with Mapperly

## The rule

Mapping code is generated at compile time by Mapperly (`Riok.Mapperly`), never written by hand and never done by reflection. Infrastructure's `MovieReviewsMapper` (`src/Infrastructure/Databases/MovieReviews/Mapping/MovieReviewsMapper.cs`) maps database models to Application entities. It only maps that way, because writes build the database model directly (`data-access-ef-core`). Add a mapping in the other direction only when something calls it. Presentation layers that need their own response models have their own mapper beside them.

Mapperly reports unmapped members as `RMG` warnings, and warnings fail the build, so every member is either mapped or explicitly ignored.

## Steps

1. Add the property to both sides with the same name. Mapperly maps it with no other change.
2. A property that only exists on one side gets `[MapperIgnoreSource(nameof(...))]` (it's on the source only) or `[MapperIgnoreTarget(nameof(...))]` (on the target only) on each affected method.
3. Different names on purpose? Use `[MapProperty(nameof(Source.A), nameof(Target.B))]`.
4. Use the aliases at the top of the mapper (`AppMovie`, `InfraMovie`) so it's always clear which side is which.
5. Build. Fix every `RMG` warning rather than suppressing it.

## Example

```csharp
// src/Infrastructure/Databases/MovieReviews/Mapping/MovieReviewsMapper.cs
[Mapper]
internal partial class MovieReviewsMapper
{
    [MapperIgnoreSource(nameof(InfraMovie.DateCreated))]
    [MapperIgnoreSource(nameof(InfraMovie.DateModified))]
    public partial AppMovie ToDomain(InfraMovie movie);
}
```

## Don't

- Use AutoMapper. It's commercially licensed now, and it maps by reflection at runtime.
- Write a mapping by hand when Mapperly can generate it.
- Add `<NoWarn>` for `RMG` codes.
- Map in a handler. Repositories return entities already mapped.

## Check

``` bash
dotnet build
```
