---
name: dotnet-coding-standards
description: "명시적 `/dotnet-coding-standards` 호출 전용 .NET 참고서. 일반 구현에는 자동 적용하지 않고 프로젝트 구조와 네이티브 코딩 능력을 우선한다."
---

# .NET Coding Standards - 통합 패키지

## 포함 파일

```
dotnet-coding-standards/
├── SKILL.md                              # 이 파일 (상세 코드 예시)
├── references/                           # 핵심 규칙 (명시적 로드)
│   └── rules.md                          # 스킬 호출 시 읽는 규칙 본문
└── templates/                            # 코드 템플릿 (on-demand)
    ├── csharp-patterns.md                # Record DTO, Result, Pattern Matching, xUnit
    ├── aspnet-core.md                    # Program.cs, Minimal API, 미들웨어, JWT, Health
    └── efcore-patterns.md               # DbContext, DDD Entity, N+1, Migration, Audit
```

---

## 참조 로딩 규칙

1. 이 `SKILL.md`를 워크플로와 예시의 소유자로 사용합니다.
2. 스킬을 명시적으로 호출했을 때 `references/rules.md`를 읽고 현재 프로젝트에 필요한 규칙만 적용합니다.
3. C# 일반 패턴, ASP.NET Core, EF Core 중 요청과 맞는 `templates/` 파일만 추가로 읽습니다.

이 규칙 본문은 스킬 안의 참조 문서이며 커스텀 에이전트로 등록되지 않습니다.

---

## Clean Architecture 코드 예시

### Program.cs (최소 설정)

```csharp
var builder = WebApplication.CreateBuilder(args);

// 서비스 등록 (Extension Method로 정리)
builder.Services.AddApplicationServices();
builder.Services.AddInfrastructureServices(builder.Configuration);
builder.Services.AddApiServices();

var app = builder.Build();

// 미들웨어 파이프라인
app.UseExceptionHandler();
app.UseAuthentication();
app.UseAuthorization();

// 엔드포인트 매핑
app.MapControllers();
// 또는 Minimal API:
// app.MapItemEndpoints();

app.Run();
```

### DI 등록 (Extension Methods)

```csharp
// Application/Extensions/ServiceCollectionExtensions.cs
public static class ApplicationServiceExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        services.AddScoped<IItemService, ItemService>();
        services.AddScoped<IOrderService, OrderService>();
        services.AddValidatorsFromAssemblyContaining<ItemRequestValidator>();
        return services;
    }
}

// Infrastructure/Extensions/ServiceCollectionExtensions.cs
public static class InfrastructureServiceExtensions
{
    public static IServiceCollection AddInfrastructureServices(
        this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<AppDbContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("Default")));

        services.AddScoped<IItemRepository, ItemRepository>();
        services.AddMemoryCache();
        return services;
    }
}
```

---

## DTO 변환 예시

```csharp
// record DTO (불변)
public record ItemRequest(
    [Required] [StringLength(200)] string Name,
    [StringLength(2000)] string? Description);

public record ItemResponse(
    int Id,
    string Name,
    string? Description,
    string Status,
    DateTime CreatedAt);

// Extension Method로 변환
public static class ItemMappingExtensions
{
    public static ItemResponse ToResponse(this Item item) => new(
        item.Id,
        item.Name,
        item.Description,
        item.Status.ToString(),
        item.CreatedAt);

    public static Item ToEntity(this ItemRequest request) => new()
    {
        Name = request.Name,
        Description = request.Description ?? string.Empty,
        Status = ItemStatus.Active
    };
}
```

---

## FluentValidation 예시

```csharp
public class ItemRequestValidator : AbstractValidator<ItemRequest>
{
    public ItemRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("이름은 필수입니다")
            .MaximumLength(200).WithMessage("이름은 200자 이내여야 합니다");

        RuleFor(x => x.Description)
            .MaximumLength(2000).WithMessage("설명은 2000자 이내여야 합니다");
    }
}

// Program.cs에 등록
builder.Services.AddValidatorsFromAssemblyContaining<ItemRequestValidator>();
```

---

## Repository 패턴 예시

```csharp
// 인터페이스 (Domain 레이어)
public interface IItemRepository
{
    Task<Item?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<(List<Item> Items, int Total)> GetPagedAsync(int page, int size, CancellationToken ct = default);
    Task AddAsync(Item item, CancellationToken ct = default);
    Task UpdateAsync(Item item, CancellationToken ct = default);
    Task DeleteAsync(Item item, CancellationToken ct = default);
}

// 구현 (Infrastructure 레이어)
public class ItemRepository(AppDbContext context) : IItemRepository
{
    public async Task<Item?> GetByIdAsync(int id, CancellationToken ct = default)
        => await context.Items.FindAsync([id], ct);

    public async Task<(List<Item> Items, int Total)> GetPagedAsync(
        int page, int size, CancellationToken ct = default)
    {
        var query = context.Items.AsNoTracking().OrderByDescending(i => i.CreatedAt);
        var total = await query.CountAsync(ct);
        var items = await query.Skip((page - 1) * size).Take(size).ToListAsync(ct);
        return (items, total);
    }

    public async Task AddAsync(Item item, CancellationToken ct = default)
    {
        context.Items.Add(item);
        await context.SaveChangesAsync(ct);
    }

    public async Task UpdateAsync(Item item, CancellationToken ct = default)
    {
        context.Items.Update(item);
        await context.SaveChangesAsync(ct);
    }

    public async Task DeleteAsync(Item item, CancellationToken ct = default)
    {
        context.Items.Remove(item);
        await context.SaveChangesAsync(ct);
    }
}
```

---

## 공통 타입 예시

```csharp
// 페이징 결과
public record PagedResult<T>(
    List<T> Items,
    int TotalCount,
    int Page,
    int PageSize)
{
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasNext => Page < TotalPages;
    public bool HasPrevious => Page > 1;
}

// 커스텀 예외
public class NotFoundException(string message) : Exception(message);
public class ConflictException(string message) : Exception(message);
public class ForbiddenException(string message) : Exception(message);
```

---

## 잘못된 예시 (금지 패턴)

```csharp
// 금지 - Entity 직접 반환
[HttpGet("{id}")]
public async Task<Item> GetById(int id) => await context.Items.FindAsync(id);

// 금지 - 동기 DB 호출
public Item GetById(int id) => context.Items.Find(id);

// 금지 - CancellationToken 누락
public async Task<Item?> GetByIdAsync(int id) => await context.Items.FindAsync(id);

// 금지 - DateTime.Now (시간대 문제)
item.CreatedAt = DateTime.Now;

// 올바른 예
[HttpGet("{id:int}")]
public async Task<IActionResult> GetById(int id, CancellationToken ct)
{
    var result = await itemService.GetByIdAsync(id, ct);
    return Ok(result); // DTO 반환
}
```

---

## 상세 템플릿 (on-demand 로딩)

| 파일 | 내용 |
|------|------|
| `templates/csharp-patterns.md` | Record DTO, Result 패턴, Pattern Matching, Extension, Generic Repository, xUnit |
| `templates/aspnet-core.md` | Program.cs, Minimal API, Controller, 미들웨어, JWT, Options, Health Checks, Serilog |
| `templates/efcore-patterns.md` | DbContext, DDD Entity, N+1 방지, Migration, 인덱스, Soft Delete, Audit, Compiled Queries |
