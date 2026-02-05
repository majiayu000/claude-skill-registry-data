---
name: dotnet-clean-architecture
description: .NET Clean Architecture patterns with CQRS, DDD, and best practices. Use when implementing features in .NET solutions following Clean Architecture principles.
---

# .NET Clean Architecture

Best practices and patterns for .NET applications following Clean Architecture with CQRS.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer                                │
│  Controllers, Middleware, Filters, DTOs                         │
│  Dependencies: Application, Infrastructure                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                          │
│  EF Core, Repositories, External Services, Identity             │
│  Dependencies: Core, Application                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Application Layer                            │
│  Commands, Queries, Handlers, Validators, Behaviors             │
│  Dependencies: Core                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Core Layer                                │
│  Entities, Value Objects, Interfaces, Domain Events             │
│  Dependencies: NONE (zero external dependencies)                 │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
src/
├── Core/
│   ├── Entities/           # Domain entities with behavior
│   ├── ValueObjects/       # Immutable value objects
│   ├── Interfaces/         # Repository and service contracts
│   ├── Enums/             # Domain enumerations
│   ├── Exceptions/        # Domain-specific exceptions
│   └── Events/            # Domain events
│
├── Application/
│   ├── Commands/          # Write operations (CQRS)
│   │   └── {Entity}/
│   │       ├── Create{Entity}Command.cs
│   │       ├── Create{Entity}CommandHandler.cs
│   │       └── Create{Entity}CommandValidator.cs
│   ├── Queries/           # Read operations (CQRS)
│   │   └── {Entity}/
│   │       ├── Get{Entity}Query.cs
│   │       └── Get{Entity}QueryHandler.cs
│   ├── Behaviors/         # Cross-cutting concerns (validation, logging)
│   ├── DTOs/             # Data transfer objects
│   └── Mappings/         # AutoMapper profiles
│
├── Infrastructure/
│   ├── Persistence/
│   │   ├── AppDbContext.cs
│   │   ├── Configurations/  # EF Core configurations
│   │   └── Repositories/    # Repository implementations
│   ├── Services/           # External service implementations
│   └── Identity/           # Authentication/Authorization
│
└── Api/
    ├── Controllers/        # REST API controllers
    ├── Middleware/         # Custom middleware
    ├── Filters/           # Action filters
    └── Models/            # API request/response models

tests/
├── Core.Tests/
├── Application.Tests/
└── Integration.Tests/
```

## Entity Pattern

```csharp
// src/Core/Entities/Auction.cs
public class Auction : BaseEntity
{
    public string Title { get; private set; }
    public Money StartingPrice { get; private set; }
    public DateTime EndsAt { get; private set; }
    public AuctionStatus Status { get; private set; }

    private readonly List<Bid> _bids = new();
    public IReadOnlyList<Bid> Bids => _bids.AsReadOnly();

    private Auction() { } // EF Core

    public static Auction Create(string title, Money startingPrice, DateTime endsAt)
    {
        if (string.IsNullOrWhiteSpace(title))
            throw new DomainException("Title is required");

        if (endsAt <= DateTime.UtcNow)
            throw new DomainException("End date must be in the future");

        return new Auction
        {
            Id = Guid.NewGuid(),
            Title = title,
            StartingPrice = startingPrice,
            EndsAt = endsAt,
            Status = AuctionStatus.Active,
            CreatedAt = DateTime.UtcNow
        };
    }

    public void PlaceBid(Bid bid)
    {
        if (Status != AuctionStatus.Active)
            throw new DomainException("Auction is not active");

        if (bid.Amount <= CurrentHighBid)
            throw new DomainException("Bid must be higher than current bid");

        _bids.Add(bid);
        AddDomainEvent(new BidPlacedEvent(this, bid));
    }

    public Money CurrentHighBid => _bids.MaxBy(b => b.Amount)?.Amount ?? StartingPrice;
}
```

## Value Object Pattern

```csharp
// src/Core/ValueObjects/Money.cs
public record Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    private Money(decimal amount, string currency)
    {
        if (amount < 0)
            throw new DomainException("Amount cannot be negative");

        Amount = amount;
        Currency = currency ?? throw new ArgumentNullException(nameof(currency));
    }

    public static Money Create(decimal amount, string currency = "USD")
        => new(amount, currency);

    public static Money Zero(string currency = "USD")
        => new(0, currency);

    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new DomainException("Cannot add different currencies");

        return new Money(Amount + other.Amount, Currency);
    }

    public static bool operator >(Money left, Money right)
        => left.Currency == right.Currency && left.Amount > right.Amount;

    public static bool operator <(Money left, Money right)
        => left.Currency == right.Currency && left.Amount < right.Amount;
}
```

## Command Pattern (CQRS Write)

```csharp
// src/Application/Commands/Auction/CreateAuctionCommand.cs
public record CreateAuctionCommand : IRequest<Guid>
{
    public string Title { get; init; }
    public decimal StartingPrice { get; init; }
    public string Currency { get; init; } = "USD";
    public DateTime EndsAt { get; init; }
}

// src/Application/Commands/Auction/CreateAuctionCommandHandler.cs
public class CreateAuctionCommandHandler : IRequestHandler<CreateAuctionCommand, Guid>
{
    private readonly IAuctionRepository _repository;
    private readonly IUnitOfWork _unitOfWork;

    public CreateAuctionCommandHandler(
        IAuctionRepository repository,
        IUnitOfWork unitOfWork)
    {
        _repository = repository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Guid> Handle(
        CreateAuctionCommand request,
        CancellationToken cancellationToken)
    {
        var startingPrice = Money.Create(request.StartingPrice, request.Currency);
        var auction = Auction.Create(request.Title, startingPrice, request.EndsAt);

        await _repository.AddAsync(auction, cancellationToken);
        await _unitOfWork.SaveChangesAsync(cancellationToken);

        return auction.Id;
    }
}

// src/Application/Commands/Auction/CreateAuctionCommandValidator.cs
public class CreateAuctionCommandValidator : AbstractValidator<CreateAuctionCommand>
{
    public CreateAuctionCommandValidator()
    {
        RuleFor(x => x.Title)
            .NotEmpty().WithMessage("Title is required")
            .MaximumLength(200).WithMessage("Title must not exceed 200 characters");

        RuleFor(x => x.StartingPrice)
            .GreaterThan(0).WithMessage("Starting price must be positive");

        RuleFor(x => x.EndsAt)
            .GreaterThan(DateTime.UtcNow).WithMessage("End date must be in the future");
    }
}
```

## Query Pattern (CQRS Read)

```csharp
// src/Application/Queries/Auction/GetAuctionByIdQuery.cs
public record GetAuctionByIdQuery(Guid Id) : IRequest<AuctionDto?>;

// src/Application/Queries/Auction/GetAuctionByIdQueryHandler.cs
public class GetAuctionByIdQueryHandler : IRequestHandler<GetAuctionByIdQuery, AuctionDto?>
{
    private readonly IAppDbContext _context;
    private readonly IMapper _mapper;

    public GetAuctionByIdQueryHandler(IAppDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<AuctionDto?> Handle(
        GetAuctionByIdQuery request,
        CancellationToken cancellationToken)
    {
        var auction = await _context.Auctions
            .AsNoTracking()
            .Include(a => a.Bids)
            .FirstOrDefaultAsync(a => a.Id == request.Id, cancellationToken);

        return auction is null ? null : _mapper.Map<AuctionDto>(auction);
    }
}
```

## Repository Pattern

```csharp
// src/Core/Interfaces/IAuctionRepository.cs
public interface IAuctionRepository
{
    Task<Auction?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<Auction>> GetActiveAsync(CancellationToken cancellationToken = default);
    Task AddAsync(Auction auction, CancellationToken cancellationToken = default);
    void Update(Auction auction);
    void Delete(Auction auction);
}

// src/Infrastructure/Persistence/Repositories/AuctionRepository.cs
public class AuctionRepository : IAuctionRepository
{
    private readonly AppDbContext _context;

    public AuctionRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<Auction?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default)
    {
        return await _context.Auctions
            .Include(a => a.Bids)
            .FirstOrDefaultAsync(a => a.Id == id, cancellationToken);
    }

    public async Task<IReadOnlyList<Auction>> GetActiveAsync(CancellationToken cancellationToken = default)
    {
        return await _context.Auctions
            .Where(a => a.Status == AuctionStatus.Active)
            .OrderBy(a => a.EndsAt)
            .ToListAsync(cancellationToken);
    }

    public async Task AddAsync(Auction auction, CancellationToken cancellationToken = default)
    {
        await _context.Auctions.AddAsync(auction, cancellationToken);
    }

    public void Update(Auction auction)
    {
        _context.Auctions.Update(auction);
    }

    public void Delete(Auction auction)
    {
        _context.Auctions.Remove(auction);
    }
}
```

## Controller Pattern

```csharp
// src/Api/Controllers/AuctionsController.cs
[ApiController]
[Route("api/[controller]")]
public class AuctionsController : ControllerBase
{
    private readonly IMediator _mediator;

    public AuctionsController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(AuctionDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<AuctionDto>> GetById(
        Guid id,
        CancellationToken cancellationToken)
    {
        var result = await _mediator.Send(new GetAuctionByIdQuery(id), cancellationToken);

        if (result is null)
            return NotFound();

        return Ok(result);
    }

    [HttpPost]
    [ProducesResponseType(typeof(Guid), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<Guid>> Create(
        [FromBody] CreateAuctionRequest request,
        CancellationToken cancellationToken)
    {
        var command = new CreateAuctionCommand
        {
            Title = request.Title,
            StartingPrice = request.StartingPrice,
            Currency = request.Currency,
            EndsAt = request.EndsAt
        };

        var id = await _mediator.Send(command, cancellationToken);

        return CreatedAtAction(nameof(GetById), new { id }, id);
    }
}
```

## Validation Behavior

```csharp
// src/Application/Behaviors/ValidationBehavior.cs
public class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!_validators.Any())
            return await next();

        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));

        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();

        if (failures.Any())
            throw new ValidationException(failures);

        return await next();
    }
}
```

## Dependency Rule

The most important principle of Clean Architecture:

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   DEPENDENCIES ALWAYS POINT INWARD                          │
│                                                              │
│   Api → Infrastructure → Application → Core                 │
│                                                              │
│   Core has ZERO external dependencies                        │
│   Core NEVER references other layers                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Anti-Patterns to Avoid

### DO NOT put business logic in controllers
```csharp
// BAD
[HttpPost]
public async Task<ActionResult> Create(CreateRequest request)
{
    if (request.Price < 0) return BadRequest(); // Logic in controller!
    var entity = new Entity { Price = request.Price };
    await _context.SaveChangesAsync();
    return Ok();
}

// GOOD - Use command handler
[HttpPost]
public async Task<ActionResult<Guid>> Create(CreateRequest request)
{
    var id = await _mediator.Send(new CreateCommand(request));
    return CreatedAtAction(nameof(GetById), new { id }, id);
}
```

### DO NOT reference Infrastructure from Core
```csharp
// BAD - Core referencing EF Core
public class Auction : Entity
{
    [Required]  // EF Core attribute in domain entity!
    public string Title { get; set; }
}

// GOOD - Pure domain entity
public class Auction : Entity
{
    public string Title { get; private set; }

    public static Auction Create(string title)
    {
        if (string.IsNullOrWhiteSpace(title))
            throw new DomainException("Title required");
        return new Auction { Title = title };
    }
}
```

### DO NOT use .Result or .Wait() on async methods
```csharp
// BAD - Can cause deadlocks
var result = GetDataAsync().Result;

// GOOD - Properly await
var result = await GetDataAsync();
```

### DO NOT catch generic Exception without re-throwing
```csharp
// BAD - Hides errors
try { ... }
catch (Exception ex) { _logger.LogError(ex, "Error"); }

// GOOD - Re-throw or be specific
try { ... }
catch (ValidationException ex) { return BadRequest(ex.Errors); }
catch (Exception ex)
{
    _logger.LogError(ex, "Error");
    throw;
}
```

## EF Core Configuration

```csharp
// src/Infrastructure/Persistence/Configurations/AuctionConfiguration.cs
public class AuctionConfiguration : IEntityTypeConfiguration<Auction>
{
    public void Configure(EntityTypeBuilder<Auction> builder)
    {
        builder.HasKey(a => a.Id);

        builder.Property(a => a.Title)
            .HasMaxLength(200)
            .IsRequired();

        builder.OwnsOne(a => a.StartingPrice, price =>
        {
            price.Property(p => p.Amount).HasColumnName("StartingPriceAmount");
            price.Property(p => p.Currency).HasColumnName("StartingPriceCurrency");
        });

        builder.HasMany(a => a.Bids)
            .WithOne()
            .HasForeignKey("AuctionId")
            .OnDelete(DeleteBehavior.Cascade);

        builder.Navigation(a => a.Bids).UsePropertyAccessMode(PropertyAccessMode.Field);
    }
}
```

## Dependency Injection Setup

```csharp
// src/Api/Program.cs or DependencyInjection.cs
services.AddMediatR(cfg => {
    cfg.RegisterServicesFromAssembly(typeof(CreateAuctionCommand).Assembly);
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
});

services.AddValidatorsFromAssembly(typeof(CreateAuctionCommandValidator).Assembly);

services.AddScoped<IAuctionRepository, AuctionRepository>();
services.AddScoped<IUnitOfWork, UnitOfWork>();
```
