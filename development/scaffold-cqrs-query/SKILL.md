---
name: scaffold-cqrs-query
description: Scaffold CQRS Query + Handler (GetList phân trang + GetById) với filters, sorting, data shaping
argument-hint: [ServiceName EntityName GetList|GetById]
allowed-tools: Write, Read, Edit
---

# Scaffold Query `$ARGUMENTS`

Usage: `/scaffold-cqrs-query ServiceName EntityName GetList`  
       `/scaffold-cqrs-query ServiceName EntityName GetById`

---

## GetList

### Query: `Application/Queries/{Entity}GetList/{Entity}GetListQuery.cs`

```csharp
namespace {Service}.Application.Queries.{Entity}GetList;

public class {Entity}GetListQuery : PaginationRequest, IRequest<{Entity}GetListResponse>
{
    public string? SearchTerm { get; set; }
    public {Entity}StatusEnum? Status { get; set; }
    public Guid? ParentId { get; set; }
    public bool? IsDeleted { get; set; }
    public bool? IsDescending { get; set; }
    public string? Fields { get; set; }         // Data shaping: ?fields=id,name
    public bool? HasParent { get; set; } = false;   // Conditional include (default false cho list)
}
```

### Handler: `Application/Queries/{Entity}GetList/{Entity}GetListQueryHandler.cs`

```csharp
public class {Entity}GetListQueryHandler : IRequestHandler<{Entity}GetListQuery, {Entity}GetListResponse>
{
    private readonly IServiceUnitOfWork _unitOfWork;

    public async Task<{Entity}GetListResponse> Handle({Entity}GetListQuery request, CancellationToken ct)
    {
        // 1. BUILD QUERYABLE
        var query = _unitOfWork.{Entity}s.GetAllAsync()  // ⚠️ SYNC — không await
            .Include(x => x.Parent)
            .AsQueryable();

        // 2. FILTERS
        if (request.IsDeleted.HasValue)
            query = request.IsDeleted.Value
                ? query.Where(x => x.IsDeleted)
                : query.Where(x => !x.IsDeleted);

        if (!string.IsNullOrWhiteSpace(request.SearchTerm))
            query = query.Where(x => x.Name.ToLower().Contains(request.SearchTerm.ToLower()));

        if (request.Status.HasValue)
            query = query.Where(x => x.Status == request.Status);

        if (request.ParentId != null && request.ParentId != Guid.Empty)
            query = query.Where(x => x.ParentId == request.ParentId);

        // 3. ORDERING
        query = request.IsDescending == true
            ? query.OrderByDescending(x => x.CreatedAt)
            : query.OrderBy(x => x.CreatedAt);

        // 4. PAGINATE + MAP + SHAPE
        var pagedList = await QueryableExtensions.ToPagedListAsync(
            query, request.PageNumber, request.PageSize,
            entity => new {Entity}DTO
            {
                Id = entity.Id.ToString(),
                Name = entity.Name,
                Status = entity.Status,
                CreatedAt = entity.CreatedAt,
                Parent = (entity.Parent != null && request.HasParent == true)
                    ? new {Entity}ParentDTO { Id = entity.Parent.Id, Name = entity.Parent.Name }
                    : null,
            },
            request.Fields);

        return new {Entity}GetListResponse { IsSuccess = true, Data = pagedList };
    }
}
```

---

## GetById

### Query: `Application/Queries/{Entity}GetById/{Entity}GetByIdQuery.cs`

```csharp
public class {Entity}GetByIdQuery : IRequest<{Entity}GetByIdResponse>
{
    [JsonIgnore][BindNever]
    public Guid Id { get; set; }

    public string? Fields { get; set; }
    public bool? HasParent { get; set; } = true;   // Default TRUE cho GetById
    public bool? HasChildren { get; set; } = true;
}
```

### Handler: `Application/Queries/{Entity}GetById/{Entity}GetByIdQueryHandler.cs`

```csharp
public async Task<{Entity}GetByIdResponse> Handle({Entity}GetByIdQuery request, CancellationToken ct)
{
    var entity = await _unitOfWork.{Entity}s.GetAllAsync()
        .Include(x => x.Parent)
        .Include(x => x.Children)
        .FirstOrDefaultAsync(x => x.Id == request.Id);

    if (entity == null) return new {Entity}GetByIdResponse { IsSuccess = false, Message = "Not found" };
    if (entity.IsDeleted) return new {Entity}GetByIdResponse { IsSuccess = false, Message = "Is deleted" };

    var dto = new {Entity}DTO
    {
        Id = entity.Id.ToString(),
        Name = entity.Name,
        Parent = (entity.Parent != null && request.HasParent == true)
            ? new {Entity}ParentDTO { Id = entity.Parent.Id, Name = entity.Parent.Name }
            : null,
    };

    var shapedData = DataShaper.ShapeData(dto, request.Fields);
    return new {Entity}GetByIdResponse { IsSuccess = true, Data = shapedData };
}
```

## Key Patterns
- GetList: `HasXxx = false` mặc định (opt-in includes, tiết kiệm bandwidth)
- GetById: `HasXxx = true` mặc định (show full data)
- Text search: `.ToLower().Contains()` (case-insensitive)
- Guid filter: check `!= null && != Guid.Empty`
- `GetAllAsync()` là SYNC — không bao giờ `await`
