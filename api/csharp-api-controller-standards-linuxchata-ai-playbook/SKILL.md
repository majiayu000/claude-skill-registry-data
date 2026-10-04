---
name: csharp-api-controller-standards
description: Defines the coding standards, patterns, and conventions for ASP.NET Core REST API controllers. Rules cover routing, HTTP verbs, response types, XML documentation, dependency injection, and asynchronous execution. Apply these rules uniformly to ensure a consistent, predictable, and well-documented API surface.
---

# C# ASP.NET Core API Controller Standards

## Description

Defines the coding standards, patterns, and conventions for ASP.NET Core REST API controllers. Rules cover routing, HTTP verbs, response types, XML documentation, dependency injection, and asynchronous execution. Apply these rules uniformly to ensure a consistent, predictable, and well-documented API surface.

---

## 1. Controller Structure & Inheritance

### 1.1 Base Class and Attributes

- All API controllers must inherit from `ControllerBase` (not `Controller`, which includes view rendering logic).
- Decorate all controllers with the `[ApiController]` attribute to enable automatic model validation, API behavior conventions, and attribute routing requirements.
- Use the `[Route]` attribute at the class level to define the base path.

```csharp
// ✅ Correct
[ApiController]
[Route("api/[controller]")]
public sealed class OrdersController : ControllerBase
{
}

// ❌ Wrong
public class OrdersController : Controller { }
```

---

## 2. Routing Conventions

### 2.1 Resource Naming

- Use **nouns**, not verbs, for endpoint paths.
- Prefer `[controller]` in the `Route` attribute to automatically use the controller name (minus the "Controller" suffix).

### 2.2 Route Parameters

- Specify route parameters explicitly in the HTTP verb attributes.
- Match route parameter names exactly with the method parameter names.

```csharp
[HttpGet("{id:guid}")]
public async Task<IActionResult> GetByIdAsync(Guid id, CancellationToken cancellationToken)
```

---

## 3. HTTP Methods & Attributes

### 3.1 Standard Verbs

Use the correct HTTP verb corresponding to the operation:

| Verb | Usage | Idempotent |
|---|---|---|
| `[HttpGet]` | Retrieve a resource or collection | Yes |
| `[HttpPost]` | Create a new resource or execute an action | No |
| `[HttpPut]` | Fully update an existing resource | Yes |
| `[HttpPatch]` | Partially update an existing resource | No |
| `[HttpDelete]` | Remove a resource | Yes |

### 3.2 Action Parameters Binding

Explicitly state where parameters are bound from to avoid ambiguity and improve OpenAPI generation:

- `[FromRoute]`: For IDs and path segments.
- `[FromQuery]`: For filtering, paging, and sorting parameters.
- `[FromBody]`: For complex objects in POST/PUT/PATCH requests.

```csharp
[HttpGet("{id:guid}/items")]
public async Task<IActionResult> GetItemsAsync(
    [FromRoute] Guid id, 
    [FromQuery] int page, 
    CancellationToken cancellationToken)
```

---

## 4. Responses & Status Codes

### 4.1 Explicit Action Results

- Return `IActionResult` or `ActionResult<T>`.
- Use the built-in helper methods (`Ok()`, `Created()`, `NotFound()`, `BadRequest()`, `NoContent()`) to generate responses.

### 4.2 Standard Status Codes

Always return the appropriate HTTP status code for the outcome:

- **200 OK**: Successful GET.
- **201 Created**: Successful POST that creates a resource. Might include a `Location` header pointing to the new resource.
- **204 No Content**: Successful operation that returns no body (e.g., DELETE, PUT, PATCH).
- **400 Bad Request**: Client error (validation failure, invalid input).
- **401 Unauthorized**: Authentication required.
- **403 Forbidden**: Authenticated, but lacks permission.
- **404 Not Found**: The requested resource ID does not exist.
- **409 Conflict**: Resource state conflict (e.g., trying to create a duplicate).

```csharp
[HttpPost]
public async Task<IActionResult> CreateAsync([FromBody] CreateOrderRequest request, CancellationToken cancellationToken)
{
    var id = await _service.CreateAsync(request, cancellationToken);
    return CreatedAtAction(nameof(GetByIdAsync), new { id = id }, request);
}
```

### 4.3 `[ProducesResponseType]`

Explicitly declare all possible status codes and their corresponding return types using `[ProducesResponseType]`. This is critical for generating accurate OpenAPI/Swagger documentation.

```csharp
[HttpGet("{id:guid}")]
[ProducesResponseType(typeof(OrderDto), StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<IActionResult> GetByIdAsync([FromRoute] Guid id, CancellationToken cancellationToken)
```

---

## 5. XML Documentation

### 5.1 Public API Contracts

Every controller action must be fully documented using XML comments.

XML comment tags:
- `<summary>`: A brief, single-sentence description of what the endpoint does.
- `<remarks>`: (Optional) Detailed information, usage examples, or nuances.
- `<param>`: Description of each input parameter.
- `<returns>`: Description of the HTTP response.
- `<response>`: Description of each possible HTTP status code returned.

```csharp
/// <summary>
/// Retrieves a specific order by its unique identifier.
/// </summary>
/// <param name="id">The unique identifier of the order.</param>
/// <param name="cancellationToken">A cancellation token.</param>
/// <returns>The HTTP response.</returns>
/// <response code="200">A specific order.</response>
/// <response code="404">If the order is not found.</response>
[HttpGet("{id:guid}")]
[ProducesResponseType(typeof(OrderDto), StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<IActionResult> GetByIdAsync([FromRoute] Guid id, CancellationToken cancellationToken)
{
    // ... implementation
}
```

---

## 6. Dependency Injection

### 6.1 Constructor Injection

Always use constructor injection for services required by the controller.

**If using C# 12 or later**, prefer **Primary Constructors** to eliminate boilerplate:

```csharp
// ✅ Correct (C# 12+)
[ApiController]
[Route("api/[controller]")]
public sealed class OrdersController(
    IOrderService orderService, 
    ILogger<OrdersController> logger) : ControllerBase
{
    // Dependencies are available directly as parameters
}
```

**If using C# 11 or earlier**, store dependencies in `private readonly` fields and use a traditional constructor:

```csharp
// ✅ Correct (C# 11 and earlier)
[ApiController]
[Route("api/[controller]")]
public sealed class OrdersController : ControllerBase
{
    private readonly IOrderService _orderService;
    private readonly ILogger<OrdersController> _logger;

    public OrdersController(IOrderService orderService, ILogger<OrdersController> logger)
    {
        _orderService = orderService;
        _logger = logger;
    }
}
```

---

## 7. Asynchronous Execution

### 7.1 Async All The Way

- All controller actions must be `async Task<IActionResult>` or `async Task<ActionResult<T>>`.
- Always append the `Async` suffix to the action method name. ASP.NET Core routing automatically removes the `Async` suffix when mapping route names (e.g., `CreatedAtAction`).
- Every action must accept a `CancellationToken` as its final parameter and pass it down to all async service calls.

```csharp
// ✅ Correct
[HttpDelete("{id:guid}")]
[ProducesResponseType(StatusCodes.Status204NoContent)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<IActionResult> DeleteAsync([FromRoute] Guid id, CancellationToken cancellationToken)
{
    var result = await _orderService.DeleteAsync(id, cancellationToken);
    return result ? NoContent() : NotFound();
}
```

---

## Quick Reference Checklist

Before submitting an API controller, verify:

- [ ] Inherits from `ControllerBase` and has `[ApiController]` and `[Route]` attributes
- [ ] Route uses plural nouns (e.g., `api/users`)
- [ ] Correct HTTP verb attribute used (`[HttpGet]`, `[HttpPost]`, etc.)
- [ ] Input parameters have explicit binding attributes (`[FromRoute]`, `[FromBody]`, etc.)
- [ ] Action is `async Task<IActionResult>` and method name ends with `Async`
- [ ] `CancellationToken` is the last parameter and is passed down
- [ ] XML `<summary>`, `<param>`, and `<response>` tags are complete
- [ ] `[ProducesResponseType]` covers all possible HTTP status codes returned
- [ ] Returns correct standard HTTP status codes (200, 201, 204, 400, 404, etc.)
