---
name: swagger
description: Configure Swagger/OpenAPI documentation for affolterNET.Web.Api. Use when setting up API documentation, customizing Swagger UI, or configuring OpenAPI metadata.
---

# Swagger/OpenAPI Configuration

Configure Swagger/OpenAPI documentation for your API.

For complete reference, see [Library Guide](../../LIBRARY_GUIDE.md).

## Quick Start

### appsettings.json

```json
{
  "affolterNET": {
    "Web": {
      "Swagger": {
        "Enabled": true,
        "Title": "My API",
        "Version": "v1",
        "Description": "API documentation for My Application"
      }
    }
  }
}
```

## Configuration Options

### SwaggerOptions

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Enabled` | bool | `true` (dev) | Enable Swagger UI and endpoint |
| `Title` | string | `"API"` | API title in Swagger UI |
| `Version` | string | `"v1"` | API version |
| `Description` | string | `null` | API description |
| `RoutePrefix` | string | `"swagger"` | URL prefix for Swagger UI |

## Common Patterns

### Development Only

```json
{
  "affolterNET": {
    "Web": {
      "Swagger": {
        "Enabled": true
      }
    }
  }
}
```

In production, set `Enabled` to `false` or remove the configuration.

### Custom Route

```json
{
  "affolterNET": {
    "Web": {
      "Swagger": {
        "Enabled": true,
        "RoutePrefix": "api-docs"
      }
    }
  }
}
```

Access at: `https://your-api.com/api-docs`

### With Authentication

When authentication is enabled, Swagger UI will include the authorization header configuration for testing authenticated endpoints.

## Controller Documentation

Use XML comments for API documentation:

```csharp
/// <summary>
/// Gets all users
/// </summary>
/// <returns>List of users</returns>
/// <response code="200">Returns the list of users</response>
/// <response code="401">Unauthorized</response>
[HttpGet]
[ProducesResponseType(typeof(List<User>), 200)]
[ProducesResponseType(401)]
public IActionResult GetUsers() { ... }
```

Enable XML documentation in your `.csproj`:

```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <NoWarn>$(NoWarn);1591</NoWarn>
</PropertyGroup>
```

## Troubleshooting

### Swagger UI not loading
- Verify `Enabled` is `true` in configuration
- Check the `RoutePrefix` matches your expected URL
- Ensure no middleware is blocking the Swagger routes

### Missing endpoints
- Confirm controllers are properly registered
- Check that routes are correctly attributed
- Verify authorization doesn't block discovery
