---
name: dotnet-api-documenter
description: Adds OpenAPI standards (Swagger) documentation to .NET ASP.NET Core APIs with Scalar UI or Swagger UI. Configures Swashbuckle, generates OpenAPI specs, and sets up interactive API documentation endpoints.
---

# .NET OpenAPI & API Documentation

Use this skill when:
- Adding OpenAPI/Swagger documentation to a .NET ASP.NET Core API
- Implementing Scalar UI or Swagger UI for interactive API exploration
- Documenting API endpoints with XML comments and annotations
- Configuring API versioning with Swashbuckle
- Generating OpenAPI specification files for external tools

## Quick Start

### 1. Add NuGet Packages

For **Swagger UI** (traditional):
```xml
<ItemGroup>
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.4.0" />
</ItemGroup>
```

For **Scalar UI** (modern alternative):
```xml
<ItemGroup>
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.4.0" />
    <PackageReference Include="Scalar.AspNetCore" Version="1.2.28" />
</ItemGroup>
```

### 2. Configure in Program.cs

**Swagger UI Setup:**
```csharp
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddControllers();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo 
    { 
        Title = "My API", 
        Version = "v1",
        Description = "API documentation"
    });
    
    // Include XML comments for documentation
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
        c.IncludeXmlComments(xmlPath);
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseAuthorization();
app.MapControllers();
app.Run();
```

**Scalar UI Setup:**
```csharp
using Scalar.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo 
    { 
        Title = "My API", 
        Version = "v1" 
    });
    
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
        c.IncludeXmlComments(xmlPath);
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.MapScalarApiReference(); // Scalar endpoint at /scalar
}

app.UseAuthorization();
app.MapControllers();
app.Run();
```

### 3. Document Endpoints with XML Comments

In your controller classes:
```csharp
/// <summary>
/// Gets a list of all items
/// </summary>
/// <param name="skip">Number of items to skip</param>
/// <param name="take">Number of items to take</param>
/// <returns>List of items</returns>
/// <response code="200">Returns the list of items</response>
/// <response code="400">If the request is invalid</response>
[HttpGet]
[ProducesResponseType(typeof(List<ItemDto>), StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status400BadRequest)]
public ActionResult<List<ItemDto>> GetItems([FromQuery] int skip = 0, [FromQuery] int take = 10)
{
    // Implementation
}

/// <summary>
/// Creates a new item
/// </summary>
/// <param name="dto">Item data</param>
/// <returns>Created item with ID</returns>
/// <response code="201">Item created successfully</response>
/// <response code="400">If validation fails</response>
[HttpPost]
[ProducesResponseType(typeof(ItemDto), StatusCodes.Status201Created)]
[ProducesResponseType(StatusCodes.Status400BadRequest)]
public async Task<ActionResult<ItemDto>> CreateItem([FromBody] CreateItemDto dto)
{
    // Implementation
}
```

### 4. Enable XML Documentation Output

Edit `.csproj`:
```xml
<PropertyGroup>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
    <DocumentationFile>bin\$(Configuration)\$(TargetFramework)\$(AssemblyName).xml</DocumentationFile>
    <NoWarn>$(NoWarn);1591</NoWarn> <!-- Suppress missing XML comments warning if desired -->
</PropertyGroup>
```

## Configuration Options

### Authentication in OpenAPI

Add JWT/Bearer token support:
```csharp
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "API", Version = "v1" });
    
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT",
        Description = "JWT Authorization header using the Bearer scheme"
    });
    
    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            new string[] { }
        }
    });
});
```

### API Versioning

Using `Asp.Versioning.Mvc`:
```csharp
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
})
.AddApiExplorer(options =>
{
    options.GroupNameFormat = "'v'VVV";
    options.SubstituteApiVersionInUrl = true;
});

builder.Services.AddSwaggerGen(options =>
{
    var provider = builder.Services.BuildServiceProvider()
        .GetRequiredService<IApiVersionDescriptionProvider>();
    
    foreach (var description in provider.ApiVersionDescriptions)
    {
        options.SwaggerDoc(
            description.GroupName,
            new OpenApiInfo
            {
                Title = "My API",
                Version = description.ApiVersion.ToString()
            });
    }
});
```

### Custom Schemas & Filters

Add custom metadata to endpoints:
```csharp
builder.Services.AddSwaggerGen(c =>
{
    c.OperationFilter<AddAuthorizationHeaderOperationFilter>();
    c.SchemaFilter<ExcludePropertiesSchemaFilter>();
});
```

## Scalar UI Advantages

- **Modern UI**: Cleaner, more intuitive interface than Swagger UI
- **Read-Only Mode**: Can hide sensitive operations in production
- **Better Performance**: Lighter bundle size
- **Dark Mode**: Built-in dark theme support
- **Request/Response Examples**: Easy mock data setup

Scalar endpoint accessible at: `https://localhost:xxxx/scalar`

## Swagger UI Advantages

- **Standard**: Industry-standard OpenAPI documentation
- **Wide Support**: Works with most API tools and generators
- **Customizable**: Extensive configuration options
- **Try-It-Out**: Built-in request executor with authentication support
- **Ecosystem**: Large community and tool support

Swagger endpoint accessible at: `https://localhost:xxxx/swagger`

## Common Tasks

### Generate OpenAPI JSON Locally
```powershell
# Using OpenAPI Generator CLI
dotnet tool install -g openapi-generator-cli

openapi-generator-cli generate `
  -i https://localhost:xxxx/swagger/v1/swagger.json `
  -g csharp-dotnet `
  -o ./generated-client
```

### Exclude Endpoints from Documentation
```csharp
[ApiExplorerSettings(IgnoreApi = true)]
[HttpGet("internal-endpoint")]
public ActionResult GetInternalData()
{
    // Won't appear in Swagger/Scalar
}
```

### Add Example Values

```csharp
/// <summary>
/// Creates an item
/// </summary>
/// <param name="dto"></param>
/// <example>
/// <code>
/// {
///   "name": "Example Item",
///   "description": "A sample item"
/// }
/// </code>
/// </example>
[HttpPost]
public async Task<ActionResult<ItemDto>> CreateItem([FromBody] CreateItemDto dto)
{
}
```

### Mark Endpoints as Deprecated

```csharp
[Obsolete("Use GetItemsV2 instead")]
[HttpGet("items")]
public ActionResult<List<ItemDto>> GetItems()
{
}
```

## Implementation Workflow

1. **Add NuGet packages** to `.csproj`
2. **Enable XML documentation** in project properties
3. **Configure Swagger/Scalar** in `Program.cs`
4. **Document controllers & endpoints** with XML comments
5. **Add response type annotations** (`[ProducesResponseType]`)
6. **Test documentation** by visiting `/swagger` or `/scalar`
7. **Configure authentication** if API is secured
8. **Export OpenAPI spec** for external tools if needed

## Validation & Testing

- Visit `https://editor.swagger.io` to validate OpenAPI JSON
- Use `[ProducesResponseType]` and `[ProducesErrorResponseType]` to document all possible responses
- Include meaningful descriptions for parameters and responses
- Test that XML comments appear in both Swagger and Scalar UIs
