---
name: service-patterns
description: Service layer patterns including interface-based design, ServiceResult pattern, business logic encapsulation, structured logging, and error handling. Use when creating or reviewing service classes.
---

# Service Patterns

## Overview
Services contain all business logic. They are the heart of the application, orchestrating operations between controllers and data access.

## Service Structure

### Interface-Based Design
Always define an interface for each service:

```csharp
public interface ITaskService
{
    Task<List<TaskResponse>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<TaskResponse?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
    Task<TaskResponse> CreateAsync(CreateTaskRequest request, CancellationToken cancellationToken = default);
    Task<TaskResponse?> UpdateAsync(Guid id, UpdateTaskRequest request, CancellationToken cancellationToken = default);
    Task<bool> DeleteAsync(Guid id, CancellationToken cancellationToken = default);
}
```

### Primary Constructor for DI
```csharp
public class TaskService(ITaskRepository repository, ILogger<TaskService> logger) : ITaskService
{
    // Implementation
}
```

## ServiceResult Pattern

For operations that can fail in expected ways, use a result pattern:

```csharp
public record ServiceResult<T>
{
    public bool IsSuccess { get; init; }
    public T? Value { get; init; }
    public string? Error { get; init; }
    public ServiceErrorType? ErrorType { get; init; }

    public static ServiceResult<T> Success(T value) => new() { IsSuccess = true, Value = value };
    public static ServiceResult<T> NotFound(string error) => new() { IsSuccess = false, Error = error, ErrorType = ServiceErrorType.NotFound };
    public static ServiceResult<T> ValidationError(string error) => new() { IsSuccess = false, Error = error, ErrorType = ServiceErrorType.Validation };
}

public enum ServiceErrorType
{
    NotFound,
    Validation,
    Conflict,
    Forbidden
}
```

## Business Logic Encapsulation

### All Logic in Services
```csharp
// Good - business rules in service
public async Task<TaskResponse> CreateAsync(CreateTaskRequest request, CancellationToken cancellationToken)
{
    var task = new TaskItem
    {
        Id = Guid.NewGuid(),
        Title = request.Title.Trim(),
        Description = request.Description?.Trim(),
        Status = TaskStatus.Pending,
        CreatedAt = DateTime.UtcNow
    };

    // Business rule: Set default due date if not provided
    task.DueDate ??= DateTime.UtcNow.AddDays(7);

    await repository.CreateAsync(task, cancellationToken);
    logger.LogInformation("Created task {TaskId} with title {Title}", task.Id, task.Title);

    return MapToResponse(task);
}
```

### Never in Controllers
Controllers should only:
1. Accept HTTP request
2. Call service
3. Return HTTP response

## Structured Logging

### Use Semantic Logging
```csharp
// Good - structured with named parameters
logger.LogInformation("Created task {TaskId} with title {Title}", task.Id, task.Title);
logger.LogWarning("Task {TaskId} not found for update", id);
logger.LogError(ex, "Failed to delete task {TaskId}", id);

// Bad - string interpolation
logger.LogInformation($"Created task {task.Id} with title {task.Title}");
```

### Log Levels
- `LogDebug` - Detailed info for debugging
- `LogInformation` - General operational events
- `LogWarning` - Unexpected but handled situations
- `LogError` - Errors that need attention

## Error Handling

### Let Exceptions Bubble for Unexpected Errors
```csharp
// Don't catch unexpected exceptions in services
public async Task<TaskResponse> CreateAsync(CreateTaskRequest request, CancellationToken cancellationToken)
{
    // If repository.CreateAsync throws, let it propagate
    // Global exception handler will log and return 500
    var task = new TaskItem { /* ... */ };
    await repository.CreateAsync(task, cancellationToken);
    return MapToResponse(task);
}
```

## Mapping

### Private Mapping Methods
```csharp
public class TaskService(ITaskRepository repository, ILogger<TaskService> logger) : ITaskService
{
    // Service methods...

    private static TaskResponse MapToResponse(TaskItem task) => new(
        task.Id,
        task.Title,
        task.Description,
        task.Status == TaskStatus.Completed,
        task.CreatedAt
    );

    private static List<TaskResponse> MapToResponse(IEnumerable<TaskItem> tasks) =>
        tasks.Select(MapToResponse).ToList();
}
```

## Service Registration

Register services in `Program.cs`:

```csharp
builder.Services.AddScoped<ITaskService, TaskService>();
builder.Services.AddScoped<ITaskRepository, JsonTaskRepository>();
```
