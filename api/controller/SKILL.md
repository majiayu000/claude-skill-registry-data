---
name: controller
description: Creating or modifying an ASP.NET Core REST API Controller in any backend microservice. Triggers when adding a new Controller class, adding endpoints to an existing Controller, or wiring up MediatR Send calls. Controller must not contain business logic — only route to _mediator.Send().
---

## Nguyên tắc bắt buộc

1. **Tuân thủ tuyệt đối** cấu trúc folder, naming convention, và code pattern được định nghĩa trong skill này — không tự ý thay đổi route, auth policy, hay thêm logic vào controller.
2. **Hỏi trước khi code** nếu bất kỳ yêu cầu nào chưa rõ (endpoint nào cần auth, role nào được phép, method nào cần). Không đoán mò — một câu hỏi ngắn tốt hơn một giờ implement sai hướng.

---

# BE Controller Pattern

```csharp
[ApiController]
[Route("api/batteries")]
public class BatteryController : ControllerBase
{
    private readonly IMediator _mediator;

    public BatteryController(IMediator mediator) => _mediator = mediator;

    [HttpGet]
    public async Task<IActionResult> GetAll([FromQuery] BatteryGetListQuery query)
        => Ok(await _mediator.Send(query));

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(Guid id)
        => Ok(await _mediator.Send(new BatteryGetByIdQuery { Id = id }));

    [HttpPost]
    [Authorize]
    public async Task<IActionResult> Create([FromBody] BatteryCreateCommand cmd)
        => Ok(await _mediator.Send(cmd));

    [HttpPut("{id}")]
    [Authorize]
    public async Task<IActionResult> Update(Guid id, [FromBody] BatteryUpdateCommand cmd)
    { cmd.Id = id; return Ok(await _mediator.Send(cmd)); }

    [HttpDelete("{id}")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Delete(Guid id)
        => Ok(await _mediator.Send(new BatteryDeleteCommand { Id = id }));

    [HttpPatch("{id}")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Restore(Guid id)
        => Ok(await _mediator.Send(new BatteryRestoreCommand { Id = id }));
}
```

## Rules

- Route: lowercase, plural, kebab-case → `api/batteries`, `api/battery-readings`
- Only inject `IMediator` — no service, repository, or DbContext
- Never put business logic in controller
- Auth policies: `"AdminOnly"` (role=1), `"ManagerOnly"` (role=2)
- GetList uses `[FromQuery]`, Create/Update use `[FromBody]`
- PUT: assign `cmd.Id = id` before Send

## File location

`Api/Controllers/{Entity}Controller.cs`

## Standard endpoints

| Method | Route | Auth | Action |
|--------|-------|------|--------|
| GET | `/api/{entities}` | Public | GetList |
| GET | `/api/{entities}/{id}` | Public | GetById |
| POST | `/api/{entities}` | `[Authorize]` | Create |
| PUT | `/api/{entities}/{id}` | `[Authorize]` | Update |
| DELETE | `/api/{entities}/{id}` | `AdminOnly` | Delete (soft) |
| PATCH | `/api/{entities}/{id}` | `AdminOnly` | Restore |
