---
name: dotnet-feature
description: Expert .NET 10 Full-Stack Developer skill. Use this when implementing new features, vertical slices, or modifying existing logic in the MoreSpeakers application. It covers Domain, Data (EF Core), Managers, and Web (Razor Pages + HTMX).
---

# .NET Feature Implementation Skill

## Overview

This skill guides the implementation of features following the Clean Architecture pattern used in MoreSpeakers.com. It ensures consistency across the Domain, Data, Managers, and Web layers.

## Architecture Flow

1.  **Domain**: Define Interfaces, Models, and Enums. (No dependencies)
2.  **Data**: Implement DataStores using EF Core. (Depends on Domain)
3.  **Managers**: Implement Business Logic. (Depends on Data + Domain)
4.  **Web**: Implement UI with Razor Pages and HTMX. (Depends on Managers)

## Coding Standards

### General C# Guidelines
-   **Namespaces**: ALWAYS use File-Scoped Namespaces (e.g., `namespace MoreSpeakers.Web;`).
-   **Injection**: ALWAYS inject Interfaces (`IUserManager`), never concrete types.
-   **Async**: ALWAYS use `async/await` throughout the stack.

### 1. Domain Layer (`src/MoreSpeakers.Domain`)
-   Models should be POCOs with DataAnnotations for validation.
-   Interfaces (`IDataStore`, `IManager`) should return `Task<T>`.

### 2. Data Layer (`src/MoreSpeakers.Data`)
-   **Pattern**: Repository/DataStore pattern.
-   **Context**: Use `MoreSpeakersDbContext`.
-   **Mapping**: Use AutoMapper to map between Entity and Domain models if they differ.
-   **NO Migrations**: Do not run EF migrations. Schema is handled by `sql-schema` skill.

```csharp
public class SpeakerDataStore : ISpeakerDataStore
{
    private readonly MoreSpeakersDbContext _context;
    // ... constructor ...

    public async Task<Speaker?> GetAsync(Guid id)
    {
        // Use AsNoTracking for read-only operations
        var entity = await _context.Speakers.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return _mapper.Map<Speaker>(entity);
    }
}
```

### 3. Manager Layer (`src/MoreSpeakers.Managers`)
-   Contains all business logic.
-   orchestrates calls between DataStores and external services (Email, etc.).

### 4. Web Layer (`src/MoreSpeakers.Web`)
-   **Framework**: Razor Pages.
-   **Interactivity**: HTMX and Hyperscript (Minimize custom JS).
-   **Partials**: Use Partial Views (`_SpeakerGrid.cshtml`) for HTMX targets.

#### HTMX Pattern

**The Container (Parent Page):**
```html
<div id="list-container">
    <partial name="_ListPartial" model="Model.Items" />
</div>

<button hx-get="@Url.Page("Index", "LoadMore")"
        hx-target="#list-container"
        hx-swap="beforeend">
    Load More
</button>
```

**The Handler (PageModel):**
```csharp
public async Task<IActionResult> OnGetLoadMoreAsync()
{
    var items = await _manager.GetNextBatchAsync();
    return Partial("_ListPartial", items);
}
```

## Checklist for New Features

1.  [ ] Defined Model in `Domain`.
2.  [ ] Created `IDataStore` interface in `Domain`.
3.  [ ] Implemented `DataStore` in `Data`.
4.  [ ] Registered `DataStore` in `Program.cs` (Scoped).
5.  [ ] Created `IManager` interface in `Domain`.
6.  [ ] Implemented `Manager` in `Managers`.
7.  [ ] Registered `Manager` in `Program.cs` (Scoped).
8.  [ ] Created Razor Page + PageModel.
9.  [ ] Implemented HTMX interactions if dynamic updates are needed.
