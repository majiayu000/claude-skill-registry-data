---
name: init-csharp-project
description: Initialize a complete C#/.NET project with solution structure, testing framework, and configuration. Use when starting ASP.NET Core APIs, console.
---

# Initialize C#/.NET Project

Create a complete, production-ready C#/.NET project with solution structure, testing framework, and enterprise-standard configuration.

## When to Use This Skill

Use this skill when you need to:

- Start a new C#/.NET project from scratch
- Create ASP.NET Core Web APIs
- Build console applications or services
- Set up class libraries or NuGet packages
- Configure xUnit/NUnit testing framework
- Establish CI/CD pipelines for .NET

**Trigger phrases**: "init csharp project", "new dotnet project", "create asp.net api", "dotnet new", "csharp boilerplate", ".net project setup"

## What This Skill Does

### Project Structure Created

```
ProjectName/
├── src/
│   └── ProjectName/
│       ├── Controllers/
│       ├── Services/
│       ├── Models/
│       ├── Data/
│       ├── Configuration/
│       ├── Program.cs
│       ├── ProjectName.csproj
│       └── appsettings.json
├── tests/
│   └── ProjectName.Tests/
│       ├── Controllers/
│       ├── Services/
│       ├── ProjectName.Tests.csproj
│       └── GlobalUsings.cs
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .editorconfig
├── Directory.Build.props
├── ProjectName.sln
├── CHANGELOG.md
└── README.md
```

## Instructions

### Step 1: Gather Project Requirements

```
Project Details:
- Name: [ProjectName]
- Type: [Web API / Console / Library / Blazor]
- .NET Version: [8.0 / 7.0]
- Database: [SQL Server / PostgreSQL / SQLite]
- Authentication: [JWT / Identity / None]

Dependencies:
- EF Core
- AutoMapper
- FluentValidation
- Serilog
```

### Step 2: Create Solution Structure

```bash
# Create solution directory
mkdir ProjectName && cd ProjectName

# Create solution file
dotnet new sln -n ProjectName

# Create source project
mkdir -p src/ProjectName
dotnet new webapi -n ProjectName -o src/ProjectName

# Create test project
mkdir -p tests/ProjectName.Tests
dotnet new xunit -n ProjectName.Tests -o tests/ProjectName.Tests

# Add projects to solution
dotnet sln add src/ProjectName/ProjectName.csproj
dotnet sln add tests/ProjectName.Tests/ProjectName.Tests.csproj

# Add project reference
dotnet add tests/ProjectName.Tests/ProjectName.Tests.csproj reference src/ProjectName/ProjectName.csproj
```

### Step 3: Create Directory.Build.props

```xml
<!-- Directory.Build.props -->
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  </PropertyGroup>

  <PropertyGroup>
    <Authors>Your Name</Authors>
    <Company>Your Company</Company>
    <Copyright>Copyright © 2025</Copyright>
    <RepositoryUrl>https://github.com/username/ProjectName</RepositoryUrl>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers" Version="8.0.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
  </ItemGroup>
</Project>
```

### Step 4: Configure Main Project (.csproj)

```xml
<!-- src/ProjectName/ProjectName.csproj -->
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Version>0.1.0</Version>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
    <NoWarn>$(NoWarn);1591</NoWarn>
  </PropertyGroup>

  <ItemGroup>
    <!-- Entity Framework Core -->
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>

    <!-- Validation and Mapping -->
    <PackageReference Include="FluentValidation.AspNetCore" Version="11.3.0" />
    <PackageReference Include="AutoMapper.Extensions.Microsoft.DependencyInjection" Version="12.0.1" />

    <!-- Logging -->
    <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
    <PackageReference Include="Serilog.Sinks.Console" Version="5.0.0" />
    <PackageReference Include="Serilog.Sinks.File" Version="5.0.0" />

    <!-- API Documentation -->
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />

    <!-- Health Checks -->
    <PackageReference Include="AspNetCore.HealthChecks.UI.Client" Version="8.0.0" />
  </ItemGroup>

</Project>
```

### Step 5: Create Program.cs

```csharp
// src/ProjectName/Program.cs
using ProjectName.Configuration;
using ProjectName.Data;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .CreateLogger();

builder.Host.UseSerilog();

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new()
    {
        Title = "ProjectName API",
        Version = "v1",
        Description = "API documentation for ProjectName"
    });
});

// Configure DbContext
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Register services
builder.Services.AddApplicationServices();

// Add health checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>();

// Add AutoMapper
builder.Services.AddAutoMapper(typeof(Program));

// Add FluentValidation
builder.Services.AddValidatorsFromAssemblyContaining<Program>();

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();

// Map health checks
app.MapHealthChecks("/health", new()
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

app.MapControllers();

try
{
    Log.Information("Starting application");
    app.Run();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Application terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}
```

### Step 6: Create Configuration Extensions

```csharp
// src/ProjectName/Configuration/ServiceCollectionExtensions.cs
namespace ProjectName.Configuration;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        // Register services
        services.AddScoped<IGreetingService, GreetingService>();

        return services;
    }
}
```

### Step 7: Create Service Layer

```csharp
// src/ProjectName/Services/IGreetingService.cs
namespace ProjectName.Services;

public interface IGreetingService
{
    string Greet(string name);
}

// src/ProjectName/Services/GreetingService.cs
namespace ProjectName.Services;

public class GreetingService : IGreetingService
{
    private readonly ILogger<GreetingService> _logger;

    public GreetingService(ILogger<GreetingService> logger)
    {
        _logger = logger;
    }

    public string Greet(string name)
    {
        _logger.LogDebug("Generating greeting for: {Name}", name);
        return $"Hello, {name}!";
    }
}
```

### Step 8: Create Controller

```csharp
// src/ProjectName/Controllers/GreetingsController.cs
using Microsoft.AspNetCore.Mvc;
using ProjectName.Services;

namespace ProjectName.Controllers;

/// <summary>
/// Controller for greeting operations.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class GreetingsController : ControllerBase
{
    private readonly IGreetingService _greetingService;
    private readonly ILogger<GreetingsController> _logger;

    public GreetingsController(
        IGreetingService greetingService,
        ILogger<GreetingsController> logger)
    {
        _greetingService = greetingService;
        _logger = logger;
    }

    /// <summary>
    /// Get a greeting for the specified name.
    /// </summary>
    /// <param name="name">The name to greet.</param>
    /// <returns>A greeting message.</returns>
    [HttpGet("{name}")]
    [ProducesResponseType(typeof(string), StatusCodes.Status200OK)]
    public IActionResult Greet(string name)
    {
        _logger.LogInformation("Greeting requested for: {Name}", name);
        var greeting = _greetingService.Greet(name);
        return Ok(greeting);
    }
}
```

### Step 9: Create appsettings.json

```json
// src/ProjectName/appsettings.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=ProjectName;Trusted_Connection=True;MultipleActiveResultSets=true"
  },
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.Hosting.Lifetime": "Information",
        "Microsoft.EntityFrameworkCore": "Warning"
      }
    },
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj}{NewLine}{Exception}"
        }
      },
      {
        "Name": "File",
        "Args": {
          "path": "logs/log-.txt",
          "rollingInterval": "Day",
          "retainedFileCountLimit": 7
        }
      }
    ]
  },
  "AllowedHosts": "*"
}
```

### Step 10: Configure Test Project

```xml
<!-- tests/ProjectName.Tests/ProjectName.Tests.csproj -->
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.6.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.4">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="coverlet.collector" Version="6.0.0">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Moq" Version="4.20.70" />
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.0" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\ProjectName\ProjectName.csproj" />
  </ItemGroup>

</Project>
```

### Step 11: Create Tests

```csharp
// tests/ProjectName.Tests/Services/GreetingServiceTests.cs
using FluentAssertions;
using Microsoft.Extensions.Logging;
using Moq;
using ProjectName.Services;
using Xunit;

namespace ProjectName.Tests.Services;

public class GreetingServiceTests
{
    private readonly Mock<ILogger<GreetingService>> _loggerMock;
    private readonly GreetingService _sut;

    public GreetingServiceTests()
    {
        _loggerMock = new Mock<ILogger<GreetingService>>();
        _sut = new GreetingService(_loggerMock.Object);
    }

    [Fact]
    public void Greet_ShouldReturnGreetingWithName()
    {
        // Arrange
        var name = "World";

        // Act
        var result = _sut.Greet(name);

        // Assert
        result.Should().Be("Hello, World!");
    }

    [Theory]
    [InlineData("Alice", "Hello, Alice!")]
    [InlineData("Bob", "Hello, Bob!")]
    [InlineData("", "Hello, !")]
    public void Greet_ShouldReturnCorrectGreeting(string name, string expected)
    {
        // Act
        var result = _sut.Greet(name);

        // Assert
        result.Should().Be(expected);
    }
}
```

```csharp
// tests/ProjectName.Tests/Controllers/GreetingsControllerTests.cs
using FluentAssertions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Moq;
using ProjectName.Controllers;
using ProjectName.Services;
using Xunit;

namespace ProjectName.Tests.Controllers;

public class GreetingsControllerTests
{
    private readonly Mock<IGreetingService> _greetingServiceMock;
    private readonly Mock<ILogger<GreetingsController>> _loggerMock;
    private readonly GreetingsController _sut;

    public GreetingsControllerTests()
    {
        _greetingServiceMock = new Mock<IGreetingService>();
        _loggerMock = new Mock<ILogger<GreetingsController>>();
        _sut = new GreetingsController(_greetingServiceMock.Object, _loggerMock.Object);
    }

    [Fact]
    public void Greet_ShouldReturnOkWithGreeting()
    {
        // Arrange
        var name = "World";
        _greetingServiceMock.Setup(x => x.Greet(name)).Returns("Hello, World!");

        // Act
        var result = _sut.Greet(name);

        // Assert
        var okResult = result.Should().BeOfType<OkObjectResult>().Subject;
        okResult.Value.Should().Be("Hello, World!");
    }
}
```

### Step 12: Create .editorconfig

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.cs]
# Organize usings
dotnet_sort_system_directives_first = true
dotnet_separate_import_directive_groups = false

# this. preferences
dotnet_style_qualification_for_field = false:warning
dotnet_style_qualification_for_property = false:warning
dotnet_style_qualification_for_method = false:warning
dotnet_style_qualification_for_event = false:warning

# var preferences
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_style_var_elsewhere = true:suggestion

# Expression-bodied members
csharp_style_expression_bodied_methods = when_on_single_line:suggestion
csharp_style_expression_bodied_constructors = false:suggestion
csharp_style_expression_bodied_properties = true:suggestion

# Null checking
csharp_style_throw_expression = true:suggestion
csharp_style_conditional_delegate_call = true:suggestion

# Naming conventions
dotnet_naming_rule.private_fields_should_be_camel_case.severity = warning
dotnet_naming_rule.private_fields_should_be_camel_case.symbols = private_fields
dotnet_naming_rule.private_fields_should_be_camel_case.style = camel_case_underscore_style

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private

dotnet_naming_style.camel_case_underscore_style.capitalization = camel_case
dotnet_naming_style.camel_case_underscore_style.required_prefix = _
```

### Step 13: Create CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: 8.0.x

      - name: Restore dependencies
        run: dotnet restore

      - name: Build
        run: dotnet build --no-restore --configuration Release

      - name: Test
        run: dotnet test --no-build --configuration Release --collect:"XPlat Code Coverage" --results-directory ./coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          directory: ./coverage
```

### Step 14: Build and Run

```bash
# Restore dependencies
dotnet restore

# Build solution
dotnet build

# Run tests
dotnet test

# Run application
dotnet run --project src/ProjectName

# Or with watch mode
dotnet watch run --project src/ProjectName
```

## Quality Checklist

- [ ] Solution structure created
- [ ] Project builds without warnings
- [ ] Tests pass
- [ ] Application starts
- [ ] Swagger UI accessible
- [ ] Health checks working
- [ ] Code coverage > 80%
- [ ] CI workflow configured
- [ ] Documentation complete

## Related Skills

- `test-structure` - Set up comprehensive testing
- `csharp-cleanup` - Code cleanup
- `api-documentation` - Document APIs
- `security-review` - Security assessment

---

**Version**: 1.0.0
**Last Updated**: December 2025


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
