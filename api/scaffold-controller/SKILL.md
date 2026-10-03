---
name: scaffold-controller
description: Scaffold REST API Controller với full CRUD endpoints, authorization, MediatR integration
argument-hint: [ServiceName EntityName]
allowed-tools: Write, Read, Edit
---

# Scaffold Controller `$ARGUMENTS`

Usage: `/scaffold-controller ServiceName EntityName`

## File: `Api/Controllers/{Entity}Controller.cs`

```csharp
using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using {Service}.Application.Commands.{Entity}Create;
using {Service}.Application.Commands.{Entity}Update;
using {Service}.Application.Commands.{Entity}Delete;
using {Service}.Application.Commands.{Entity}Restore;
using {Service}.Application.Queries.{Entity}GetList;
using {Service}.Application.Queries.{Entity}GetById;

namespace {Service}.Api.Controllers;

[ApiController]
[Route("api/{entities}")]  // lowercase, plural, kebab-case
public class {Entity}Controller : ControllerBase
{
    private readonly IMediator _mediator;

    public {Entity}Controller(IMediator mediator) => _mediator = mediator;

    [HttpGet]
    public async Task<IActionResult> GetAll([FromQuery] {Entity}GetListQuery query)
        => Ok(await _mediator.Send(query));

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(Guid id, [FromQuery] string? fields,
        [FromQuery] bool? hasParent, [FromQuery] bool? hasChildren)
        => Ok(await _mediator.Send(new {Entity}GetByIdQuery
        {
            Id = id, Fields = fields,
            HasParent = hasParent ?? true, HasChildren = hasChildren ?? true,
        }));

    [HttpPost]
    [Authorize]  // Adjust: [Authorize(Policy = "AdminOnly")] or [Authorize(Policy = "ManagerOnly")]
    public async Task<IActionResult> Create([FromBody] {Entity}CreateCommand command)
        => Ok(await _mediator.Send(command));

    [HttpPut("{id}")]
    [Authorize]
    public async Task<IActionResult> Update(Guid id, [FromBody] {Entity}UpdateCommand command)
    { command.Id = id; return Ok(await _mediator.Send(command)); }

    [HttpDelete("{id}")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Delete(Guid id)
        => Ok(await _mediator.Send(new {Entity}DeleteCommand { Id = id }));

    [HttpPatch("{id}")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Restore(Guid id)
        => Ok(await _mediator.Send(new {Entity}RestoreCommand { Id = id }));
}
```

## HTTP Method Mapping

| Action | Method | Route | Auth |
|--------|--------|-------|------|
| List | GET | `/` | Public |
| Detail | GET | `/{id}` | Public |
| Create | POST | `/` | Auth |
| Update | PUT | `/{id}` | Auth |
| Delete (soft) | DELETE | `/{id}` | AdminOnly |
| Restore | PATCH | `/{id}` | AdminOnly |
| Custom action | PATCH | `/{id}/action` | Varies |

## Authorization

- `[Authorize]` — any authenticated user (Staff, Manager, Admin)
- `[Authorize(Policy = "AdminOnly")]` — Role = "1"
- `[Authorize(Policy = "ManagerOnly")]` — Role = "2"
- `[AllowAnonymous]` — internal/public endpoints
- No attribute = public (GET list/detail usually public)

## Rules
- Controller THIN — chỉ `_mediator.Send()`, KHÔNG chứa business logic
- `[FromBody]` cho POST/PUT, `[FromQuery]` cho GET
- Route: lowercase, plural, kebab-case
- Return `Ok(result)` — wrapper handles success/failure
