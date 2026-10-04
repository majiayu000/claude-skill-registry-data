---
name: stack-dotnet
description: .NET backend conventions, patterns, and test infrastructure. Use when working with C# files, .csproj projects, ASP.NET APIs, xUnit tests, FluentAssertions, Entity Framework, WebApplicationFactory, dotnet CLI, NuGet packages, .NET dependency injection, middleware, or controller patterns.
user-invocable: false
---

## Integration Tests
```csharp
// Use WebApplicationFactory<Program> + in-memory DB
public class OrdersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public OrdersApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task CreateOrder_WithValidData_ReturnsCreatedOrder()
    {
        var request = new CreateOrderRequest { /* ... */ };
        var response = await _client.PostAsJsonAsync("/api/orders", request);

        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var order = await response.Content.ReadFromJsonAsync<OrderResponse>();
        order.Id.Should().NotBeEmpty();
        order.Status.Should().Be("Pending");
    }
}
```

## Frameworks
- xUnit for tests
- FluentAssertions for assertions
- WebApplicationFactory for integration tests

## Build & Test Commands
```bash
dotnet build
dotnet test
```

## Security
- Use parameterized queries or Entity Framework — never raw SQL string concatenation
- Apply `[Authorize]` attributes on all non-public endpoints
- Validate all model inputs with data annotations or FluentValidation
- No secrets in `appsettings.json` committed to source control — use User Secrets or environment variables

Read the project's applicable agent guidance (`AGENTS.md` for Codex, `CLAUDE.md` for
Claude Code) and relevant `docs/<topic>.md` files for project-specific .NET
conventions when they exist.
