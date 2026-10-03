---
name: scaffold-dto
description: Scaffold DTOs (main DTO, nested DTOs, response wrappers) with Guid-to-string conversion and conditional includes
argument-hint: [ServiceName EntityName]
allowed-tools: Write, Read, Edit
---

# Scaffold DTOs for `$ARGUMENTS`

Usage: `/scaffold-dto ServiceName EntityName`

## File: `Application/DTOs/Response/{Entity}Response.cs`

```csharp
using SharedContracts.Common.Wrappers;
using {Service}.Domain.Enums;

namespace {Service}.Application.DTOs.Response;

// MAIN DTO
public class {Entity}DTO
{
    public string Id { get; set; } = string.Empty;    // Guid → string
    public string? Name { get; set; }
    public string? Description { get; set; }
    public {Entity}StatusEnum Status { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public bool IsDeleted { get; set; }
    public DateTime? DeletedAt { get; set; }

    // Conditional nested DTOs (null khi HasXxx = false)
    // public {Entity}ParentDTO? Parent { get; set; }
    // public List<{Entity}ChildDTO>? Children { get; set; }
}

// NESTED DTOs (subset fields của entity liên quan)
// public class {Entity}ParentDTO
// {
//     public Guid Id { get; set; }
//     public string Name { get; set; } = string.Empty;
// }

// RESPONSE WRAPPERS
public class {Entity}GetListResponse : CommonResponse<PaginationResponse<object>> { }
public class {Entity}GetByIdResponse : CommonResponse<object> { }
public class {Entity}CreateResponse : CommonResponse<{Entity}DTO> { }
public class {Entity}UpdateResponse : CommonResponse<{Entity}DTO> { }
public class {Entity}DeleteResponse : CommonResponse<{Entity}DTO> { }
public class {Entity}RestoreResponse : CommonResponse<{Entity}DTO> { }
```

## Inline Mapping Example (trong Handler)

```csharp
var dto = new {Entity}DTO
{
    Id = entity.Id.ToString(),        // Guid → string
    Name = entity.Name,
    Status = entity.Status,
    CreatedAt = entity.CreatedAt,
    UpdatedAt = entity.UpdatedAt,
    IsDeleted = entity.IsDeleted,

    // Nullable Guid → string
    // ParentId = entity.ParentId.HasValue ? entity.ParentId.Value.ToString() : null,

    // Conditional nested include
    // Parent = (entity.Parent != null && request.HasParent == true)
    //     ? new {Entity}ParentDTO { Id = entity.Parent.Id, Name = entity.Parent.Name }
    //     : null,
};
```

## Rules
- Main DTO: Guid → string conversion
- Nested DTO: `{Parent}{Child}DTO` naming
- NO AutoMapper — inline mapping trong handler
- `PaginationResponse<object>` cho list (supports data shaping)
- `CommonResponse<object>` cho detail (supports data shaping)
- `CommonResponse<{Entity}DTO>` cho Create/Update/Delete
