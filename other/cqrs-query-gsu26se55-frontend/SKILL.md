---
name: cqrs-query
description: Creating a CQRS Query and QueryHandler in any backend microservice. Triggers when implementing GetList (paginated) or GetById read operations. Uses IQueryable from GetAllAsync, supports filtering, ordering, Include for navigation properties, and PaginationResponse wrapping.
---

## Nguyên tắc bắt buộc

1. **Tuân thủ tuyệt đối** cấu trúc folder, naming convention, và code pattern được định nghĩa trong skill này — không tự ý thay đổi tên file, tên class, tên method, hay thứ tự layer.
2. **Hỏi trước khi code** nếu bất kỳ yêu cầu nào chưa rõ (scope, field, filter logic, relation giữa entities). Không đoán mò — một câu hỏi ngắn tốt hơn một giờ implement sai hướng.

---

# BE CQRS Query Pattern

## Folder structure

```
Application/Queries/{Entity}Get{Scope}/
├── {Entity}Get{Scope}Query.cs
└── {Entity}Get{Scope}QueryHandler.cs
```

## GetList Query

```csharp
public class BatteryGetListQuery : IRequest<BatteryGetListResponse>
{
    public string? SearchTerm { get; set; }
    public BatteryStatusEnum? Status { get; set; }
    public bool? IsDeleted { get; set; } = false;
    public bool? IsDescending { get; set; }
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 10;
    public bool? HasLocation { get; set; }
}
```

## GetList Handler

```csharp
public class BatteryGetListQueryHandler : IRequestHandler<BatteryGetListQuery, BatteryGetListResponse>
{
    private readonly IServiceUnitOfWork _unitOfWork;

    public BatteryGetListQueryHandler(IServiceUnitOfWork unitOfWork)
        => _unitOfWork = unitOfWork;

    public async Task<BatteryGetListResponse> Handle(BatteryGetListQuery request, CancellationToken ct)
    {
        // GetAllAsync() is SYNC — returns IQueryable directly, do NOT await
        var query = _unitOfWork.Batteries.GetAllAsync()
            .Where(x => !x.IsDeleted);

        if (request.HasLocation == true)
            query = query.Include(x => x.Location);

        if (!string.IsNullOrEmpty(request.SearchTerm))
            query = query.Where(x => x.Name.Contains(request.SearchTerm));

        if (request.Status.HasValue)
            query = query.Where(x => x.Status == request.Status);

        if (request.IsDeleted.HasValue)
            query = query.Where(x => x.IsDeleted == request.IsDeleted);

        query = request.IsDescending == true
            ? query.OrderByDescending(x => x.CreatedAt)
            : query.OrderBy(x => x.CreatedAt);

        var total = await query.CountAsync(ct);
        var items = await query
            .Skip((request.PageNumber - 1) * request.PageSize)
            .Take(request.PageSize)
            .Select(x => new BatteryDTO
            {
                Id = x.Id.ToString(),
                Name = x.Name,
                Status = x.Status,
                CreatedAt = x.CreatedAt,
            })
            .ToListAsync(ct);

        return new BatteryGetListResponse
        {
            IsSuccess = true,
            Data = new PaginationResponse<object>
            {
                Items = items,
                TotalCount = total,
                PageNumber = request.PageNumber,
                PageSize = request.PageSize,
            }
        };
    }
}
```

## GetById Handler

```csharp
public async Task<BatteryGetByIdResponse> Handle(BatteryGetByIdQuery request, CancellationToken ct)
{
    var entity = await _unitOfWork.Batteries.GetAllAsync()
        .Where(x => x.Id == request.Id && !x.IsDeleted)
        .Include(x => x.Location)
        .FirstOrDefaultAsync(ct);

    if (entity == null)
        return new BatteryGetByIdResponse { IsSuccess = false, Message = "Not found" };

    return new BatteryGetByIdResponse
    {
        IsSuccess = true,
        Data = new BatteryDTO
        {
            Id = entity.Id.ToString(),
            Name = entity.Name,
            Status = entity.Status,
            Location = entity.Location != null ? new LocationDTO { Id = entity.Location.Id.ToString() } : null,
        }
    };
}
```

## Critical rules

- `GetAllAsync()` is SYNC and returns `IQueryable<T>` — NEVER await it
- Query handlers NEVER call `SaveChangesAsync`
- ALWAYS `.Where(x => !x.IsDeleted)` — project has no global query filter
- Guid → string in DTO: `x.Id.ToString()`
- No AutoMapper — inline mapping in handler
- `HasXxx = false` by default in GetList, `HasXxx = true` in GetById

## Response types

```csharp
public class BatteryGetListResponse : CommonResponse<PaginationResponse<object>> { }
public class BatteryGetByIdResponse : CommonResponse<object> { }
```
