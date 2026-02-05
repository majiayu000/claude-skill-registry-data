---
name: controller-patterns
description: ASP.NET Core controller patterns including thin controllers, routing, parameter binding, response types, and DTOs. Use when creating or reviewing API controllers.
---

# Controller Patterns

## Overview
Controllers should be thin - they handle HTTP concerns only. All business logic belongs in services.

## Thin Controller Pattern

### The Rule
Each controller action should be 2-3 lines maximum:
1. Call the service
2. Return the result

```csharp
// Good - thin controller
[HttpGet("{id:guid}")]
public async Task<ActionResult<TaskResponse>> GetById(Guid id, CancellationToken cancellationToken)
{
    var result = await taskService.GetByIdAsync(id, cancellationToken);
    return result is null ? NotFound() : Ok(result);
}

// Bad - fat controller with business logic
[HttpGet("{id:guid}")]
public async Task<ActionResult<TaskResponse>> GetById(Guid id)
{
    if (id == Guid.Empty) return BadRequest("Invalid ID");
    var task = await repository.GetByIdAsync(id);
    if (task is null) return NotFound();
    var response = new TaskResponse(task.Id, task.Title, task.Description);
    logger.LogInformation("Retrieved task {Id}", id);
    return Ok(response);
}
```

## Route Conventions

### Resource Naming
- Use plural nouns: `/api/tasks`, `/api/users`
- Use kebab-case for multi-word resources: `/api/task-items`

### Route Attributes
```csharp
[ApiController]
[Route("api/[controller]")]
public class TasksController(ITaskService taskService) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<List<TaskResponse>>> GetAll(CancellationToken cancellationToken)

    [HttpGet("{id:guid}")]
    public async Task<ActionResult<TaskResponse>> GetById(Guid id, CancellationToken cancellationToken)

    [HttpPost]
    public async Task<ActionResult<TaskResponse>> Create([FromBody] CreateTaskRequest request, CancellationToken cancellationToken)

    [HttpPut("{id:guid}")]
    public async Task<ActionResult<TaskResponse>> Update(Guid id, [FromBody] UpdateTaskRequest request, CancellationToken cancellationToken)

    [HttpDelete("{id:guid}")]
    public async Task<IActionResult> Delete(Guid id, CancellationToken cancellationToken)
}
```

## Parameter Binding

### FromBody for Complex Types
```csharp
[HttpPost]
public async Task<ActionResult<TaskResponse>> Create([FromBody] CreateTaskRequest request)
```

### FromQuery for Filtering/Pagination
```csharp
[HttpGet]
public async Task<ActionResult<PagedResult<TaskResponse>>> GetAll(
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 10,
    [FromQuery] string? status = null,
    CancellationToken cancellationToken = default)
```

### FromRoute for Resource IDs
```csharp
[HttpGet("{id:guid}")]
public async Task<ActionResult<TaskResponse>> GetById([FromRoute] Guid id)
```

## Response Types

### ActionResult<T> for All Responses
```csharp
// Good - explicit return type
public async Task<ActionResult<TaskResponse>> GetById(Guid id)

// Avoid - IActionResult loses type info
public async Task<IActionResult> GetById(Guid id)
```

### Proper Status Codes
```csharp
// 200 OK - successful GET
return Ok(result);

// 201 Created - successful POST
return CreatedAtAction(nameof(GetById), new { id = task.Id }, response);

// 204 No Content - successful DELETE
return NoContent();

// 400 Bad Request - validation failure
return BadRequest(ModelState);

// 404 Not Found - resource doesn't exist
return NotFound();
```

## Request/Response DTOs

### Separate Request and Response Types
```csharp
// Request DTO - what client sends
public record CreateTaskRequest(
    [Required] string Title,
    string? Description);

// Response DTO - what API returns
public record TaskResponse(
    Guid Id,
    string Title,
    string? Description,
    bool IsCompleted,
    DateTime CreatedAt);
```

### Never Expose Domain Models Directly
```csharp
// Bad - exposes internal model
[HttpGet("{id:guid}")]
public async Task<ActionResult<TaskItem>> GetById(Guid id)

// Good - uses response DTO
[HttpGet("{id:guid}")]
public async Task<ActionResult<TaskResponse>> GetById(Guid id)
```

## Validation

### Use Data Annotations on DTOs
```csharp
public record CreateTaskRequest(
    [Required]
    [StringLength(200, MinimumLength = 1)]
    string Title,

    [StringLength(2000)]
    string? Description);
```

### Model State is Automatic
With `[ApiController]`, invalid model state returns 400 automatically - no manual checks needed.

## Complete Controller Example

```csharp
using Microsoft.AspNetCore.Mvc;

namespace TaskApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TasksController(ITaskService taskService) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<List<TaskResponse>>> GetAll(CancellationToken cancellationToken)
    {
        var tasks = await taskService.GetAllAsync(cancellationToken);
        return Ok(tasks);
    }

    [HttpGet("{id:guid}")]
    public async Task<ActionResult<TaskResponse>> GetById(Guid id, CancellationToken cancellationToken)
    {
        var task = await taskService.GetByIdAsync(id, cancellationToken);
        return task is null ? NotFound() : Ok(task);
    }

    [HttpPost]
    public async Task<ActionResult<TaskResponse>> Create([FromBody] CreateTaskRequest request, CancellationToken cancellationToken)
    {
        var task = await taskService.CreateAsync(request, cancellationToken);
        return CreatedAtAction(nameof(GetById), new { id = task.Id }, task);
    }

    [HttpPut("{id:guid}")]
    public async Task<ActionResult<TaskResponse>> Update(Guid id, [FromBody] UpdateTaskRequest request, CancellationToken cancellationToken)
    {
        var task = await taskService.UpdateAsync(id, request, cancellationToken);
        return task is null ? NotFound() : Ok(task);
    }

    [HttpDelete("{id:guid}")]
    public async Task<IActionResult> Delete(Guid id, CancellationToken cancellationToken)
    {
        var deleted = await taskService.DeleteAsync(id, cancellationToken);
        return deleted ? NoContent() : NotFound();
    }
}
```
