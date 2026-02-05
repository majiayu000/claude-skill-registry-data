---
name: dotnet-minimal-api-templates
description: Create production-ready ASP.NET Core Minimal API projects with async patterns, dependency injection, and comprehensive error handling. Use when building new .NET API applications or setting up backend API projects with .NET 8+.
---

# .NET Minimal API Project Templates

Production-ready ASP.NET Core Minimal API project structures with async patterns, dependency injection, middleware, and best practices for building high-performance APIs.

## When to Use This Skill

- Starting new .NET API projects from scratch
- Implementing async REST APIs with C#
- Building high-performance web services and microservices
- Creating async applications with SQL Server, PostgreSQL, MongoDB
- Setting up API projects with proper structure and testing
- Migrating from Controller-based APIs to Minimal APIs

## Core Concepts

### 1. Project Structure

**Recommended Layout:**
```
src/
├── MyApi.Api/                 # API layer
│   ├── Endpoints/
│   │   ├── Users/
│   │   │   ├── CreateUser.cs
│   │   │   ├── GetUser.cs
│   │   │   └── UpdateUser.cs
│   │   └── Orders/
│   │       ├── CreateOrder.cs
│   │       └── GetOrders.cs
│   ├── Filters/
│   │   ├── ValidationFilter.cs
│   │   └── ExceptionFilter.cs
│   ├── Extensions/
│   │   └── EndpointExtensions.cs
│   └── Program.cs
├── MyApi.Application/         # Business logic
│   ├── Commands/
│   │   └── CreateUserCommand.cs
│   ├── Queries/
│   │   └── GetUserQuery.cs
│   ├── Handlers/
│   │   └── CreateUserHandler.cs
│   └── DTOs/
│       └── UserDto.cs
├── MyApi.Domain/              # Domain entities
│   ├── Entities/
│   │   ├── User.cs
│   │   └── Order.cs
│   └── Interfaces/
│       └── IUserRepository.cs
└── MyApi.Infrastructure/      # Data access
    ├── Data/
    │   └── ApplicationDbContext.cs
    ├── Repositories/
    │   └── UserRepository.cs
    └── Configurations/
        └── UserConfiguration.cs
```

### 2. Dependency Injection

ASP.NET Core's built-in DI system:
- Scoped services for database contexts
- Singleton services for caching
- Transient services for lightweight operations
- Keyed services (new in .NET 8)

### 3. Async Patterns

Proper async/await usage:
- Async endpoint handlers
- Async database operations (EF Core)
- Async HTTP clients
- Background services

## Implementation Patterns

### Pattern 1: Complete Minimal API Application

```csharp
// Program.cs
using Microsoft.EntityFrameworkCore;
using MyApi.Infrastructure.Data;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Database
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

// Authentication
builder.Services.AddAuthentication().AddJwtBearer();
builder.Services.AddAuthorization();

// Application services
builder.Services.AddMediatR(cfg =>
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));
builder.Services.AddScoped<IUserRepository, UserRepository>();

var app = builder.Build();

// Middleware pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();

// Map endpoints
app.MapUserEndpoints();
app.MapOrderEndpoints();

app.Run();

// Make Program accessible for testing
public partial class Program { }
```

```csharp
// Extensions/EndpointExtensions.cs
public static class UserEndpointExtensions
{
    public static RouteGroupBuilder MapUserEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/api/users")
            .WithTags("Users")
            .WithOpenApi();

        group.MapGet("/", GetUsers)
            .WithName("GetUsers")
            .Produces<PagedResult<UserDto>>(StatusCodes.Status200OK);

        group.MapGet("/{id:guid}", GetUserById)
            .WithName("GetUserById")
            .Produces<UserDto>(StatusCodes.Status200OK)
            .Produces(StatusCodes.Status404NotFound);

        group.MapPost("/", CreateUser)
            .WithName("CreateUser")
            .Produces<UserDto>(StatusCodes.Status201Created)
            .ProducesValidationProblem();

        group.MapPut("/{id:guid}", UpdateUser)
            .WithName("UpdateUser")
            .Produces<UserDto>(StatusCodes.Status200OK)
            .Produces(StatusCodes.Status404NotFound)
            .RequireAuthorization();

        group.MapDelete("/{id:guid}", DeleteUser)
            .WithName("DeleteUser")
            .Produces(StatusCodes.Status204NoContent)
            .RequireAuthorization("AdminOnly");

        return group;
    }

    private static async Task<IResult> GetUsers(
        [AsParameters] PaginationParams pagination,
        IMediator mediator,
        CancellationToken ct)
    {
        var query = new GetUsersQuery(pagination.Page, pagination.PageSize);
        var result = await mediator.Send(query, ct);
        return Results.Ok(result);
    }

    private static async Task<IResult> GetUserById(
        Guid id,
        IMediator mediator,
        CancellationToken ct)
    {
        var query = new GetUserByIdQuery(id);
        var result = await mediator.Send(query, ct);
        return result is not null
            ? Results.Ok(result)
            : Results.NotFound();
    }

    private static async Task<IResult> CreateUser(
        CreateUserRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var command = new CreateUserCommand(request.Email, request.Name);
        var result = await mediator.Send(command, ct);
        return Results.Created($"/api/users/{result.Id}", result);
    }

    private static async Task<IResult> UpdateUser(
        Guid id,
        UpdateUserRequest request,
        IMediator mediator,
        CancellationToken ct)
    {
        var command = new UpdateUserCommand(id, request.Name, request.Email);
        var result = await mediator.Send(command, ct);
        return result is not null
            ? Results.Ok(result)
            : Results.NotFound();
    }

    private static async Task<IResult> DeleteUser(
        Guid id,
        IMediator mediator,
        CancellationToken ct)
    {
        var command = new DeleteUserCommand(id);
        await mediator.Send(command, ct);
        return Results.NoContent();
    }
}

public record PaginationParams(int Page = 1, int PageSize = 20);
public record CreateUserRequest(string Email, string Name);
public record UpdateUserRequest(string Name, string Email);
```

### Pattern 2: CQRS with MediatR

```csharp
// Application/Commands/CreateUserCommand.cs
public record CreateUserCommand(string Email, string Name) : IRequest<UserDto>;

// Application/Handlers/CreateUserHandler.cs
public class CreateUserHandler : IRequestHandler<CreateUserCommand, UserDto>
{
    private readonly IUserRepository _repository;
    private readonly ILogger<CreateUserHandler> _logger;

    public CreateUserHandler(
        IUserRepository repository,
        ILogger<CreateUserHandler> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public async Task<UserDto> Handle(
        CreateUserCommand request,
        CancellationToken cancellationToken)
    {
        // Validate
        if (await _repository.ExistsByEmailAsync(request.Email, cancellationToken))
        {
            throw new ValidationException("Email already exists");
        }

        // Create entity
        var user = new User
        {
            Id = Guid.NewGuid(),
            Email = request.Email,
            Name = request.Name,
            CreatedAt = DateTime.UtcNow
        };

        // Save
        await _repository.AddAsync(user, cancellationToken);

        _logger.LogInformation("User created: {UserId}", user.Id);

        // Return DTO
        return new UserDto(user.Id, user.Email, user.Name);
    }
}

// Application/Queries/GetUserByIdQuery.cs
public record GetUserByIdQuery(Guid Id) : IRequest<UserDto?>;

public class GetUserByIdHandler : IRequestHandler<GetUserByIdQuery, UserDto?>
{
    private readonly IUserRepository _repository;

    public GetUserByIdHandler(IUserRepository repository)
    {
        _repository = repository;
    }

    public async Task<UserDto?> Handle(
        GetUserByIdQuery request,
        CancellationToken cancellationToken)
    {
        var user = await _repository.GetByIdAsync(request.Id, cancellationToken);
        return user is not null
            ? new UserDto(user.Id, user.Email, user.Name)
            : null;
    }
}
```

### Pattern 3: Repository Pattern with EF Core

```csharp
// Domain/Interfaces/IUserRepository.cs
public interface IUserRepository
{
    Task<User?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<User?> GetByEmailAsync(string email, CancellationToken ct = default);
    Task<PagedResult<User>> GetPagedAsync(
        int page,
        int pageSize,
        CancellationToken ct = default);
    Task<bool> ExistsByEmailAsync(string email, CancellationToken ct = default);
    Task AddAsync(User user, CancellationToken ct = default);
    Task UpdateAsync(User user, CancellationToken ct = default);
    Task DeleteAsync(Guid id, CancellationToken ct = default);
}

// Infrastructure/Repositories/UserRepository.cs
public class UserRepository : IUserRepository
{
    private readonly ApplicationDbContext _context;

    public UserRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetByIdAsync(Guid id, CancellationToken ct = default)
    {
        return await _context.Users
            .AsNoTracking()
            .FirstOrDefaultAsync(u => u.Id == id, ct);
    }

    public async Task<User?> GetByEmailAsync(string email, CancellationToken ct = default)
    {
        return await _context.Users
            .AsNoTracking()
            .FirstOrDefaultAsync(u => u.Email == email, ct);
    }

    public async Task<PagedResult<User>> GetPagedAsync(
        int page,
        int pageSize,
        CancellationToken ct = default)
    {
        var query = _context.Users.AsNoTracking();

        var total = await query.CountAsync(ct);
        var items = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(ct);

        return new PagedResult<User>
        {
            Items = items,
            Total = total,
            Page = page,
            PageSize = pageSize
        };
    }

    public async Task<bool> ExistsByEmailAsync(string email, CancellationToken ct = default)
    {
        return await _context.Users
            .AnyAsync(u => u.Email == email, ct);
    }

    public async Task AddAsync(User user, CancellationToken ct = default)
    {
        await _context.Users.AddAsync(user, ct);
        await _context.SaveChangesAsync(ct);
    }

    public async Task UpdateAsync(User user, CancellationToken ct = default)
    {
        _context.Users.Update(user);
        await _context.SaveChangesAsync(ct);
    }

    public async Task DeleteAsync(Guid id, CancellationToken ct = default)
    {
        await _context.Users
            .Where(u => u.Id == id)
            .ExecuteDeleteAsync(ct);
    }
}
```

### Pattern 4: Authentication & Authorization

```csharp
// appsettings.json
{
  "Jwt": {
    "Key": "your-secret-key-here-min-32-chars",
    "Issuer": "your-api",
    "Audience": "your-clients",
    "ExpiryMinutes": 60
  }
}

// Program.cs - JWT configuration
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy =>
        policy.RequireRole("Admin"));
    options.AddPolicy("UserOrAdmin", policy =>
        policy.RequireRole("User", "Admin"));
});

// Auth endpoints
app.MapPost("/api/auth/login", async (
    LoginRequest request,
    IUserRepository repository,
    IConfiguration config) =>
{
    // Validate credentials
    var user = await repository.GetByEmailAsync(request.Email);
    if (user is null || !VerifyPassword(request.Password, user.PasswordHash))
    {
        return Results.Unauthorized();
    }

    // Generate token
    var token = GenerateJwtToken(user, config);
    return Results.Ok(new { Token = token });
})
.WithName("Login")
.WithOpenApi();

static string GenerateJwtToken(User user, IConfiguration config)
{
    var key = new SymmetricSecurityKey(
        Encoding.UTF8.GetBytes(config["Jwt:Key"]!));
    var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

    var claims = new[]
    {
        new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
        new Claim(ClaimTypes.Email, user.Email),
        new Claim(ClaimTypes.Name, user.Name),
        new Claim(ClaimTypes.Role, user.Role)
    };

    var token = new JwtSecurityToken(
        issuer: config["Jwt:Issuer"],
        audience: config["Jwt:Audience"],
        claims: claims,
        expires: DateTime.UtcNow.AddMinutes(
            int.Parse(config["Jwt:ExpiryMinutes"]!)),
        signingCredentials: creds);

    return new JwtSecurityTokenHandler().WriteToken(token);
}

record LoginRequest(string Email, string Password);
```

### Pattern 5: Endpoint Filters (Middleware)

```csharp
// Filters/ValidationFilter.cs
public class ValidationFilter<T> : IEndpointFilter where T : class
{
    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var requestBody = context.Arguments
            .OfType<T>()
            .FirstOrDefault();

        if (requestBody is null)
        {
            return Results.BadRequest("Request body is required");
        }

        // Validate using FluentValidation or DataAnnotations
        var validationResults = new List<ValidationResult>();
        var validationContext = new ValidationContext(requestBody);

        if (!Validator.TryValidateObject(
            requestBody,
            validationContext,
            validationResults,
            validateAllProperties: true))
        {
            var errors = validationResults
                .Select(v => new { Field = v.MemberNames.First(), Error = v.ErrorMessage })
                .ToList();

            return Results.ValidationProblem(errors.ToDictionary(
                e => e.Field,
                e => new[] { e.Error }));
        }

        return await next(context);
    }
}

// Usage
group.MapPost("/", CreateUser)
    .AddEndpointFilter<ValidationFilter<CreateUserRequest>>();

// Global exception handling filter
public class ExceptionHandlingFilter : IEndpointFilter
{
    private readonly ILogger<ExceptionHandlingFilter> _logger;

    public ExceptionHandlingFilter(ILogger<ExceptionHandlingFilter> logger)
    {
        _logger = logger;
    }

    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        try
        {
            return await next(context);
        }
        catch (ValidationException ex)
        {
            _logger.LogWarning(ex, "Validation error");
            return Results.BadRequest(new { Error = ex.Message });
        }
        catch (NotFoundException ex)
        {
            _logger.LogWarning(ex, "Resource not found");
            return Results.NotFound(new { Error = ex.Message });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception");
            return Results.Problem("An error occurred processing your request");
        }
    }
}
```

### Pattern 6: API Versioning

```csharp
// Install: Asp.Versioning.Http
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = new UrlSegmentApiVersionReader();
})
.AddApiExplorer(options =>
{
    options.GroupNameFormat = "'v'VVV";
    options.SubstituteApiVersionInUrl = true;
});

// Version 1 endpoints
var v1 = app.NewVersionedApi("Users")
    .MapGroup("/api/v{version:apiVersion}/users")
    .HasApiVersion(1.0);

v1.MapGet("/", GetUsersV1);

// Version 2 endpoints
var v2 = app.NewVersionedApi("Users")
    .MapGroup("/api/v{version:apiVersion}/users")
    .HasApiVersion(2.0);

v2.MapGet("/", GetUsersV2);
```

### Pattern 7: Response Caching

```csharp
builder.Services.AddOutputCache(options =>
{
    options.AddBasePolicy(builder =>
        builder.Expire(TimeSpan.FromMinutes(1)));

    options.AddPolicy("UserCache", builder =>
        builder.Expire(TimeSpan.FromMinutes(5))
               .SetVaryByQuery("page", "pageSize"));
});

app.UseOutputCache();

// Apply caching
group.MapGet("/", GetUsers)
    .CacheOutput("UserCache");
```

### Pattern 8: Result Pattern (Error Handling)

```csharp
// Install: ErrorOr, FluentResults, or custom implementation

// Custom Result implementation
public class Result<T>
{
    public T? Value { get; }
    public bool IsSuccess { get; }
    public Error? Error { get; }

    private Result(T value)
    {
        Value = value;
        IsSuccess = true;
        Error = null;
    }

    private Result(Error error)
    {
        Value = default;
        IsSuccess = false;
        Error = error;
    }

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(Error error) => new(error);

    public TResult Match<TResult>(
        Func<T, TResult> onSuccess,
        Func<Error, TResult> onFailure)
    {
        return IsSuccess ? onSuccess(Value!) : onFailure(Error!);
    }
}

public record Error(string Code, string Description);

// Usage in handlers
public class CreateUserHandler : IRequestHandler<CreateUserCommand, Result<UserDto>>
{
    private readonly IUserRepository _repository;

    public async Task<Result<UserDto>> Handle(
        CreateUserCommand request,
        CancellationToken cancellationToken)
    {
        // Validate
        if (await _repository.ExistsByEmailAsync(request.Email, cancellationToken))
        {
            return Result<UserDto>.Failure(new Error(
                "User.DuplicateEmail",
                "A user with this email already exists"));
        }

        // Create user
        var user = new User
        {
            Id = Guid.NewGuid(),
            Email = request.Email,
            Name = request.Name,
            CreatedAt = DateTime.UtcNow
        };

        await _repository.AddAsync(user, cancellationToken);

        var userDto = new UserDto(user.Id, user.Email, user.Name);
        return Result<UserDto>.Success(userDto);
    }
}

// Endpoint with Result pattern
app.MapPost("/api/users", async (
    CreateUserRequest request,
    IMediator mediator,
    CancellationToken ct) =>
{
    var command = new CreateUserCommand(request.Email, request.Name);
    var result = await mediator.Send(command, ct);

    return result.Match(
        onSuccess: user => Results.Created($"/api/users/{user.Id}", user),
        onFailure: error => Results.BadRequest(new { error.Code, error.Description }));
});

// Using ErrorOr library (recommended)
// Install: ErrorOr
using ErrorOr;

public class CreateUserHandler : IRequestHandler<CreateUserCommand, ErrorOr<UserDto>>
{
    public async Task<ErrorOr<UserDto>> Handle(
        CreateUserCommand request,
        CancellationToken cancellationToken)
    {
        if (await _repository.ExistsByEmailAsync(request.Email, cancellationToken))
        {
            return Error.Conflict(
                code: "User.DuplicateEmail",
                description: "A user with this email already exists");
        }

        var user = new User
        {
            Id = Guid.NewGuid(),
            Email = request.Email,
            Name = request.Name
        };

        await _repository.AddAsync(user, cancellationToken);

        return new UserDto(user.Id, user.Email, user.Name);
    }
}

// Extension for converting ErrorOr to IResult
public static class ErrorOrExtensions
{
    public static IResult ToHttpResult<T>(this ErrorOr<T> result)
    {
        return result.Match(
            value => Results.Ok(value),
            errors => ToProblemDetails(errors));
    }

    private static IResult ToProblemDetails(List<Error> errors)
    {
        var firstError = errors[0];

        var statusCode = firstError.Type switch
        {
            ErrorType.Conflict => StatusCodes.Status409Conflict,
            ErrorType.Validation => StatusCodes.Status400BadRequest,
            ErrorType.NotFound => StatusCodes.Status404NotFound,
            ErrorType.Unauthorized => StatusCodes.Status401Unauthorized,
            _ => StatusCodes.Status500InternalServerError
        };

        return Results.Problem(
            statusCode: statusCode,
            title: firstError.Code,
            detail: firstError.Description);
    }
}
```

### Pattern 9: FluentValidation Integration

```csharp
// Install: FluentValidation.DependencyInjectionExtensions
builder.Services.AddValidatorsFromAssemblyContaining<Program>();

// Validator
public class CreateUserCommandValidator : AbstractValidator<CreateUserCommand>
{
    public CreateUserCommandValidator()
    {
        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .MaximumLength(255);

        RuleFor(x => x.Name)
            .NotEmpty()
            .MinimumLength(2)
            .MaximumLength(100);
    }
}

// Validation behavior for MediatR
public class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
    where TResponse : IErrorOr
{
    private readonly IValidator<TRequest>? _validator;

    public ValidationBehavior(IValidator<TRequest>? validator = null)
    {
        _validator = validator;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (_validator is null)
        {
            return await next();
        }

        var validationResult = await _validator.ValidateAsync(request, cancellationToken);

        if (validationResult.IsValid)
        {
            return await next();
        }

        var errors = validationResult.Errors
            .Select(failure => Error.Validation(
                code: failure.PropertyName,
                description: failure.ErrorMessage))
            .ToList();

        return (dynamic)errors;
    }
}

// Register behavior
builder.Services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly);
    cfg.AddOpenBehavior(typeof(ValidationBehavior<,>));
});

// Endpoint filter alternative
public class FluentValidationFilter<T> : IEndpointFilter where T : class
{
    private readonly IValidator<T> _validator;

    public FluentValidationFilter(IValidator<T> validator)
    {
        _validator = validator;
    }

    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var requestBody = context.Arguments.OfType<T>().FirstOrDefault();

        if (requestBody is null)
        {
            return Results.BadRequest("Request body is required");
        }

        var validationResult = await _validator.ValidateAsync(requestBody);

        if (!validationResult.IsValid)
        {
            return Results.ValidationProblem(
                validationResult.ToDictionary());
        }

        return await next(context);
    }
}
```

### Pattern 10: Mapster for Object Mapping

```csharp
// Install: Mapster, Mapster.DependencyInjection
builder.Services.AddMapster();

// Configure mappings
public class MappingConfig : IRegister
{
    public void Register(TypeAdapterConfig config)
    {
        // Simple mapping
        config.NewConfig<User, UserDto>();

        // Custom mapping
        config.NewConfig<User, UserDetailDto>()
            .Map(dest => dest.FullName, src => $"{src.FirstName} {src.LastName}")
            .Map(dest => dest.OrderCount, src => src.Orders.Count);

        // Ignore properties
        config.NewConfig<CreateUserRequest, User>()
            .Ignore(dest => dest.Id)
            .Ignore(dest => dest.CreatedAt);

        // After mapping
        config.NewConfig<User, UserDto>()
            .AfterMapping((src, dest) =>
            {
                dest.DisplayName = dest.Name.ToUpper();
            });
    }
}

// Usage in handlers
public class GetUserByIdHandler : IRequestHandler<GetUserByIdQuery, ErrorOr<UserDetailDto>>
{
    private readonly IUserRepository _repository;
    private readonly IMapper _mapper;

    public GetUserByIdHandler(IUserRepository repository, IMapper mapper)
    {
        _repository = repository;
        _mapper = mapper;
    }

    public async Task<ErrorOr<UserDetailDto>> Handle(
        GetUserByIdQuery request,
        CancellationToken cancellationToken)
    {
        var user = await _repository.GetByIdAsync(request.Id, cancellationToken);

        if (user is null)
        {
            return Error.NotFound(
                code: "User.NotFound",
                description: $"User with ID {request.Id} was not found");
        }

        // Map with Mapster
        var userDto = _mapper.Map<UserDetailDto>(user);
        return userDto;
    }
}

// ProjectToType for query optimization
public async Task<PagedResult<UserDto>> GetPagedAsync(
    int page,
    int pageSize,
    CancellationToken ct)
{
    var query = _context.Users.AsNoTracking();

    var total = await query.CountAsync(ct);

    // Project directly to DTO in database query
    var items = await query
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ProjectToType<UserDto>()
        .ToListAsync(ct);

    return new PagedResult<UserDto>
    {
        Items = items,
        Total = total,
        Page = page,
        PageSize = pageSize
    };
}
```

### Pattern 11: EF Core Specification Pattern

```csharp
// Base specification
public abstract class Specification<T>
{
    public Expression<Func<T, bool>>? Criteria { get; private set; }
    public List<Expression<Func<T, object>>> Includes { get; } = new();
    public List<string> IncludeStrings { get; } = new();
    public Expression<Func<T, object>>? OrderBy { get; private set; }
    public Expression<Func<T, object>>? OrderByDescending { get; private set; }
    public int? Take { get; private set; }
    public int? Skip { get; private set; }
    public bool AsNoTracking { get; private set; } = true;

    protected void AddCriteria(Expression<Func<T, bool>> criteria)
    {
        Criteria = criteria;
    }

    protected void AddInclude(Expression<Func<T, object>> includeExpression)
    {
        Includes.Add(includeExpression);
    }

    protected void AddInclude(string includeString)
    {
        IncludeStrings.Add(includeString);
    }

    protected void ApplyOrderBy(Expression<Func<T, object>> orderByExpression)
    {
        OrderBy = orderByExpression;
    }

    protected void ApplyOrderByDescending(Expression<Func<T, object>> orderByDescendingExpression)
    {
        OrderByDescending = orderByDescendingExpression;
    }

    protected void ApplyPaging(int skip, int take)
    {
        Skip = skip;
        Take = take;
    }

    protected void EnableTracking()
    {
        AsNoTracking = false;
    }
}

// Concrete specifications
public class ActiveUsersSpecification : Specification<User>
{
    public ActiveUsersSpecification()
    {
        AddCriteria(u => u.IsActive);
        ApplyOrderBy(u => u.Name);
    }
}

public class UserByEmailSpecification : Specification<User>
{
    public UserByEmailSpecification(string email)
    {
        AddCriteria(u => u.Email == email);
        AddInclude(u => u.Orders);
    }
}

public class UserOrdersSpecification : Specification<User>
{
    public UserOrdersSpecification(Guid userId, DateTime? from = null)
    {
        AddCriteria(u => u.Id == userId);
        AddInclude(u => u.Orders.Where(o => from == null || o.CreatedAt >= from));
    }
}

// Specification evaluator
public static class SpecificationEvaluator
{
    public static IQueryable<T> GetQuery<T>(
        IQueryable<T> inputQuery,
        Specification<T> specification) where T : class
    {
        var query = inputQuery;

        if (specification.Criteria is not null)
        {
            query = query.Where(specification.Criteria);
        }

        query = specification.Includes
            .Aggregate(query, (current, include) => current.Include(include));

        query = specification.IncludeStrings
            .Aggregate(query, (current, include) => current.Include(include));

        if (specification.OrderBy is not null)
        {
            query = query.OrderBy(specification.OrderBy);
        }
        else if (specification.OrderByDescending is not null)
        {
            query = query.OrderByDescending(specification.OrderByDescending);
        }

        if (specification.Skip.HasValue)
        {
            query = query.Skip(specification.Skip.Value);
        }

        if (specification.Take.HasValue)
        {
            query = query.Take(specification.Take.Value);
        }

        if (specification.AsNoTracking)
        {
            query = query.AsNoTracking();
        }

        return query;
    }
}

// Repository with specifications
public interface IRepository<T> where T : class
{
    Task<T?> GetBySpecificationAsync(
        Specification<T> specification,
        CancellationToken ct = default);

    Task<List<T>> ListAsync(
        Specification<T> specification,
        CancellationToken ct = default);

    Task<int> CountAsync(
        Specification<T> specification,
        CancellationToken ct = default);
}

public class Repository<T> : IRepository<T> where T : class
{
    private readonly ApplicationDbContext _context;

    public Repository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<T?> GetBySpecificationAsync(
        Specification<T> specification,
        CancellationToken ct = default)
    {
        var query = SpecificationEvaluator.GetQuery(_context.Set<T>(), specification);
        return await query.FirstOrDefaultAsync(ct);
    }

    public async Task<List<T>> ListAsync(
        Specification<T> specification,
        CancellationToken ct = default)
    {
        var query = SpecificationEvaluator.GetQuery(_context.Set<T>(), specification);
        return await query.ToListAsync(ct);
    }

    public async Task<int> CountAsync(
        Specification<T> specification,
        CancellationToken ct = default)
    {
        var query = SpecificationEvaluator.GetQuery(_context.Set<T>(), specification);
        return await query.CountAsync(ct);
    }
}

// Usage
var spec = new ActiveUsersSpecification();
var activeUsers = await _repository.ListAsync(spec, ct);

var emailSpec = new UserByEmailSpecification("test@example.com");
var user = await _repository.GetBySpecificationAsync(emailSpec, ct);
```

### Pattern 12: Event-Driven Domain Models

```csharp
// Domain event base
public abstract record DomainEvent
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public DateTime OccurredAt { get; init; } = DateTime.UtcNow;
}

// Specific domain events
public record UserCreatedEvent(Guid UserId, string Email, string Name) : DomainEvent;
public record OrderPlacedEvent(Guid OrderId, Guid UserId, decimal Total) : DomainEvent;
public record OrderCancelledEvent(Guid OrderId, string Reason) : DomainEvent;

// Entity base with domain events
public abstract class Entity
{
    private readonly List<DomainEvent> _domainEvents = new();

    public IReadOnlyCollection<DomainEvent> DomainEvents => _domainEvents.AsReadOnly();

    protected void RaiseDomainEvent(DomainEvent domainEvent)
    {
        _domainEvents.Add(domainEvent);
    }

    public void ClearDomainEvents()
    {
        _domainEvents.Clear();
    }
}

// Domain entity with events
public class Order : Entity
{
    public Guid Id { get; private set; }
    public Guid UserId { get; private set; }
    public OrderStatus Status { get; private set; }
    public decimal Total { get; private set; }
    public DateTime CreatedAt { get; private set; }

    private readonly List<OrderItem> _items = new();
    public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();

    public static Order Create(Guid userId, List<OrderItem> items)
    {
        var order = new Order
        {
            Id = Guid.NewGuid(),
            UserId = userId,
            Status = OrderStatus.Pending,
            CreatedAt = DateTime.UtcNow
        };

        order._items.AddRange(items);
        order.Total = items.Sum(i => i.Price * i.Quantity);

        // Raise domain event
        order.RaiseDomainEvent(new OrderPlacedEvent(
            order.Id,
            order.UserId,
            order.Total));

        return order;
    }

    public void Cancel(string reason)
    {
        if (Status == OrderStatus.Cancelled)
        {
            throw new InvalidOperationException("Order is already cancelled");
        }

        Status = OrderStatus.Cancelled;

        RaiseDomainEvent(new OrderCancelledEvent(Id, reason));
    }

    public void MarkAsShipped()
    {
        if (Status != OrderStatus.Confirmed)
        {
            throw new InvalidOperationException("Only confirmed orders can be shipped");
        }

        Status = OrderStatus.Shipped;
    }
}

// Domain event handler
public class OrderPlacedEventHandler : INotificationHandler<OrderPlacedEvent>
{
    private readonly IEmailService _emailService;
    private readonly ILogger<OrderPlacedEventHandler> _logger;

    public OrderPlacedEventHandler(
        IEmailService emailService,
        ILogger<OrderPlacedEventHandler> logger)
    {
        _emailService = emailService;
        _logger = logger;
    }

    public async Task Handle(OrderPlacedEvent notification, CancellationToken cancellationToken)
    {
        _logger.LogInformation(
            "Order {OrderId} placed for user {UserId}",
            notification.OrderId,
            notification.UserId);

        // Send confirmation email
        await _emailService.SendOrderConfirmationAsync(
            notification.UserId,
            notification.OrderId,
            cancellationToken);
    }
}

// Save changes with domain event publishing
public class ApplicationDbContext : DbContext
{
    private readonly IPublisher _publisher;

    public ApplicationDbContext(
        DbContextOptions<ApplicationDbContext> options,
        IPublisher publisher)
        : base(options)
    {
        _publisher = publisher;
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Get domain events before saving
        var domainEvents = ChangeTracker.Entries<Entity>()
            .Select(e => e.Entity)
            .SelectMany(e => e.DomainEvents)
            .ToList();

        // Save changes
        var result = await base.SaveChangesAsync(cancellationToken);

        // Publish domain events
        foreach (var domainEvent in domainEvents)
        {
            await _publisher.Publish(domainEvent, cancellationToken);
        }

        // Clear events
        foreach (var entity in ChangeTracker.Entries<Entity>().Select(e => e.Entity))
        {
            entity.ClearDomainEvents();
        }

        return result;
    }
}

// Register MediatR for domain events
builder.Services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly);
});
```

## Testing

```csharp
// Tests/Integration/UserEndpointsTests.cs
public class UserEndpointsTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly HttpClient _client;

    public UserEndpointsTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace database with in-memory
                services.RemoveAll<DbContextOptions<ApplicationDbContext>>();
                services.AddDbContext<ApplicationDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        });

        _client = _factory.CreateClient();
    }

    [Fact]
    public async Task GetUsers_ReturnsOk()
    {
        // Act
        var response = await _client.GetAsync("/api/users");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var users = await response.Content.ReadFromJsonAsync<PagedResult<UserDto>>();
        users.Should().NotBeNull();
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreated()
    {
        // Arrange
        var request = new CreateUserRequest("test@example.com", "Test User");

        // Act
        var response = await _client.PostAsJsonAsync("/api/users", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var user = await response.Content.ReadFromJsonAsync<UserDto>();
        user.Should().NotBeNull();
        user!.Email.Should().Be(request.Email);
    }

    [Fact]
    public async Task GetUserById_WithInvalidId_ReturnsNotFound()
    {
        // Act
        var response = await _client.GetAsync($"/api/users/{Guid.NewGuid()}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
}

// Tests/Unit/CreateUserHandlerTests.cs
public class CreateUserHandlerTests
{
    private readonly Mock<IUserRepository> _repository;
    private readonly Mock<ILogger<CreateUserHandler>> _logger;
    private readonly CreateUserHandler _handler;

    public CreateUserHandlerTests()
    {
        _repository = new Mock<IUserRepository>();
        _logger = new Mock<ILogger<CreateUserHandler>>();
        _handler = new CreateUserHandler(_repository.Object, _logger.Object);
    }

    [Fact]
    public async Task Handle_WithValidCommand_CreatesUser()
    {
        // Arrange
        var command = new CreateUserCommand("test@example.com", "Test User");
        _repository.Setup(r => r.ExistsByEmailAsync(command.Email, default))
            .ReturnsAsync(false);

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        result.Should().NotBeNull();
        result.Email.Should().Be(command.Email);
        _repository.Verify(r => r.AddAsync(
            It.IsAny<User>(),
            It.IsAny<CancellationToken>()),
            Times.Once);
    }

    [Fact]
    public async Task Handle_WithDuplicateEmail_ThrowsValidationException()
    {
        // Arrange
        var command = new CreateUserCommand("test@example.com", "Test User");
        _repository.Setup(r => r.ExistsByEmailAsync(command.Email, default))
            .ReturnsAsync(true);

        // Act & Assert
        await _handler.Invoking(h => h.Handle(command, CancellationToken.None))
            .Should().ThrowAsync<ValidationException>();
    }
}
```

## Best Practices

1. **Use Route Groups**: Organize related endpoints with `MapGroup`
2. **Leverage Endpoint Filters**: Replace middleware for endpoint-specific logic
3. **CQRS Pattern**: Separate read and write operations
4. **Async All The Way**: Use async methods for I/O operations
5. **Keyed Services**: Use .NET 8 keyed services for multiple implementations
6. **Result Pattern**: Use `IResult` for flexible responses
7. **OpenAPI**: Document with `WithOpenApi()` and attributes
8. **Testing**: Use `WebApplicationFactory` for integration tests

## Common Pitfalls

- **Blocking Code**: Using `.Result` or `.Wait()` instead of `await`
- **No Cancellation Tokens**: Not passing `CancellationToken` to async methods
- **Fat Endpoints**: Business logic in endpoint handlers
- **Missing Validation**: Not validating requests
- **Poor Error Handling**: Exposing stack traces in production
- **No API Versioning**: Breaking changes without versioning
- **Ignoring Performance**: Not using `AsNoTracking()` for read-only queries
