---
name: dotnet-best-practices
description: .NET development best practices including SOLID, KISS, YAGNI, DRY principles, design patterns, and anti-patterns to avoid.
---

# .NET Best Practices

Fundamental principles and patterns for writing maintainable, scalable, and clean .NET code.

## Core Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                     GUIDING PRINCIPLES                          │
│                                                                 │
│   SOLID ─── Foundation for object-oriented design               │
│   DRY   ─── Don't Repeat Yourself                               │
│   KISS  ─── Keep It Simple, Stupid                              │
│   YAGNI ─── You Aren't Gonna Need It                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SOLID Principles

### S - Single Responsibility Principle

A class should have only one reason to change.

```csharp
// BAD - Multiple responsibilities
public class UserService
{
    public void CreateUser(User user) { /* ... */ }
    public void SendWelcomeEmail(User user) { /* ... */ }
    public void GenerateReport(User user) { /* ... */ }
    public void LogUserActivity(User user) { /* ... */ }
}

// GOOD - Single responsibility per class
public class UserService
{
    private readonly IEmailService _emailService;
    private readonly IUserRepository _repository;

    public async Task<User> CreateUserAsync(CreateUserRequest request)
    {
        var user = User.Create(request.Email, request.Name);
        await _repository.AddAsync(user);
        await _emailService.SendWelcomeEmailAsync(user);
        return user;
    }
}

public class EmailService : IEmailService
{
    public Task SendWelcomeEmailAsync(User user) { /* ... */ }
}

public class UserReportGenerator : IReportGenerator<User>
{
    public Task<Report> GenerateAsync(User user) { /* ... */ }
}
```

### O - Open/Closed Principle

Software entities should be open for extension, but closed for modification.

```csharp
// BAD - Must modify class to add new discount types
public class DiscountCalculator
{
    public decimal Calculate(Order order, string discountType)
    {
        return discountType switch
        {
            "percentage" => order.Total * 0.1m,
            "fixed" => order.Total - 10m,
            "loyalty" => order.Total * 0.15m,
            // Must add new cases here...
            _ => order.Total
        };
    }
}

// GOOD - Open for extension via new implementations
public interface IDiscountStrategy
{
    decimal Apply(Order order);
}

public class PercentageDiscount : IDiscountStrategy
{
    private readonly decimal _percentage;
    public PercentageDiscount(decimal percentage) => _percentage = percentage;
    public decimal Apply(Order order) => order.Total * _percentage;
}

public class FixedDiscount : IDiscountStrategy
{
    private readonly decimal _amount;
    public FixedDiscount(decimal amount) => _amount = amount;
    public decimal Apply(Order order) => Math.Max(0, order.Total - _amount);
}

public class LoyaltyDiscount : IDiscountStrategy
{
    public decimal Apply(Order order) => order.Total * 0.15m;
}

// New discounts added without modifying existing code
public class BulkDiscount : IDiscountStrategy
{
    public decimal Apply(Order order) =>
        order.Items.Count > 10 ? order.Total * 0.2m : order.Total;
}
```

### L - Liskov Substitution Principle

Subtypes must be substitutable for their base types.

```csharp
// BAD - Square breaks Rectangle behavior
public class Rectangle
{
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }
    public int Area => Width * Height;
}

public class Square : Rectangle
{
    public override int Width
    {
        set { base.Width = base.Height = value; }
    }
    public override int Height
    {
        set { base.Width = base.Height = value; }
    }
}

// This breaks LSP:
Rectangle rect = new Square();
rect.Width = 5;
rect.Height = 10;
// Expected: Area = 50, Actual: Area = 100

// GOOD - Separate abstractions
public interface IShape
{
    int Area { get; }
}

public class Rectangle : IShape
{
    public int Width { get; }
    public int Height { get; }
    public int Area => Width * Height;

    public Rectangle(int width, int height)
    {
        Width = width;
        Height = height;
    }
}

public class Square : IShape
{
    public int Side { get; }
    public int Area => Side * Side;

    public Square(int side) => Side = side;
}
```

### I - Interface Segregation Principle

Clients should not be forced to depend on interfaces they don't use.

```csharp
// BAD - Fat interface forces unnecessary implementations
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
    void AttendMeeting();
    void WriteReport();
}

public class Robot : IWorker
{
    public void Work() { /* ... */ }
    public void Eat() => throw new NotSupportedException(); // Forced to implement
    public void Sleep() => throw new NotSupportedException();
    public void AttendMeeting() => throw new NotSupportedException();
    public void WriteReport() => throw new NotSupportedException();
}

// GOOD - Segregated interfaces
public interface IWorkable
{
    void Work();
}

public interface IFeedable
{
    void Eat();
}

public interface IRestable
{
    void Sleep();
}

public class Human : IWorkable, IFeedable, IRestable
{
    public void Work() { /* ... */ }
    public void Eat() { /* ... */ }
    public void Sleep() { /* ... */ }
}

public class Robot : IWorkable
{
    public void Work() { /* ... */ }
}
```

### D - Dependency Inversion Principle

High-level modules should not depend on low-level modules. Both should depend on abstractions.

```csharp
// BAD - High-level depends on low-level
public class OrderService
{
    private readonly SqlDatabase _database = new SqlDatabase();
    private readonly SmtpEmailSender _emailSender = new SmtpEmailSender();

    public void ProcessOrder(Order order)
    {
        _database.Save(order);
        _emailSender.Send(order.CustomerEmail, "Order confirmed");
    }
}

// GOOD - Both depend on abstractions
public interface IOrderRepository
{
    Task SaveAsync(Order order);
}

public interface IEmailSender
{
    Task SendAsync(string to, string message);
}

public class OrderService
{
    private readonly IOrderRepository _repository;
    private readonly IEmailSender _emailSender;

    public OrderService(IOrderRepository repository, IEmailSender emailSender)
    {
        _repository = repository;
        _emailSender = emailSender;
    }

    public async Task ProcessOrderAsync(Order order)
    {
        await _repository.SaveAsync(order);
        await _emailSender.SendAsync(order.CustomerEmail, "Order confirmed");
    }
}
```

---

## DRY - Don't Repeat Yourself

Every piece of knowledge should have a single, unambiguous representation.

```csharp
// BAD - Repeated validation logic
public class UserController
{
    public IActionResult Create(UserRequest request)
    {
        if (string.IsNullOrEmpty(request.Email) || !request.Email.Contains("@"))
            return BadRequest("Invalid email");
        // ...
    }

    public IActionResult Update(UserRequest request)
    {
        if (string.IsNullOrEmpty(request.Email) || !request.Email.Contains("@"))
            return BadRequest("Invalid email");
        // ...
    }
}

// GOOD - Single source of truth
public static class EmailValidator
{
    private static readonly Regex EmailRegex = new(
        @"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        RegexOptions.Compiled);

    public static bool IsValid(string email) =>
        !string.IsNullOrWhiteSpace(email) && EmailRegex.IsMatch(email);
}

// Or use FluentValidation
public class UserRequestValidator : AbstractValidator<UserRequest>
{
    public UserRequestValidator()
    {
        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .WithMessage("Invalid email format");
    }
}
```

---

## KISS - Keep It Simple, Stupid

Prefer simple solutions over complex ones.

```csharp
// BAD - Over-engineered
public class StringHelper
{
    public string Reverse(string input)
    {
        if (input == null)
            throw new ArgumentNullException(nameof(input));

        var factory = new StringBuilderFactory();
        var builder = factory.Create(input.Length);
        var strategy = new ReverseIterationStrategy();

        foreach (var index in strategy.GetIndices(input.Length))
        {
            builder.Append(input[index]);
        }

        return builder.ToString();
    }
}

// GOOD - Simple and clear
public static class StringExtensions
{
    public static string Reverse(this string input)
    {
        if (string.IsNullOrEmpty(input))
            return input;

        var chars = input.ToCharArray();
        Array.Reverse(chars);
        return new string(chars);
    }
}
```

---

## YAGNI - You Aren't Gonna Need It

Don't add functionality until it's necessary.

```csharp
// BAD - Building for hypothetical future requirements
public class UserService
{
    private readonly ICache _cache;
    private readonly IMessageQueue _queue;
    private readonly IAnalyticsService _analytics;
    private readonly IAuditLog _auditLog;
    private readonly IFeatureFlags _featureFlags;

    public async Task<User> GetUserAsync(Guid id)
    {
        // Complex caching logic for "future scale"
        // Message queue integration "in case we need it"
        // Analytics tracking "for later"
        // Audit logging "just in case"
        // Feature flags "for flexibility"

        // When all you need is:
        return await _repository.GetByIdAsync(id);
    }
}

// GOOD - Only what's needed now
public class UserService
{
    private readonly IUserRepository _repository;

    public UserService(IUserRepository repository)
    {
        _repository = repository;
    }

    public Task<User?> GetUserAsync(Guid id) =>
        _repository.GetByIdAsync(id);
}

// Add caching WHEN you have performance issues
// Add analytics WHEN you have analytics requirements
// Add audit logging WHEN compliance requires it
```

---

## Design Patterns

### Strategy Pattern

Encapsulate algorithms and make them interchangeable.

```csharp
// Define strategy interface
public interface IPaymentStrategy
{
    Task<PaymentResult> ProcessAsync(Payment payment);
}

// Concrete strategies
public class CreditCardPayment : IPaymentStrategy
{
    private readonly IPaymentGateway _gateway;

    public CreditCardPayment(IPaymentGateway gateway) => _gateway = gateway;

    public async Task<PaymentResult> ProcessAsync(Payment payment)
    {
        var response = await _gateway.ChargeAsync(payment.Amount, payment.CardToken);
        return new PaymentResult(response.Success, response.TransactionId);
    }
}

public class PayPalPayment : IPaymentStrategy
{
    private readonly IPayPalClient _client;

    public PayPalPayment(IPayPalClient client) => _client = client;

    public async Task<PaymentResult> ProcessAsync(Payment payment)
    {
        var response = await _client.ExecutePaymentAsync(payment.PayPalOrderId);
        return new PaymentResult(response.Status == "COMPLETED", response.Id);
    }
}

public class BankTransferPayment : IPaymentStrategy
{
    public Task<PaymentResult> ProcessAsync(Payment payment)
    {
        // Generate transfer instructions
        return Task.FromResult(new PaymentResult(true, Guid.NewGuid().ToString()));
    }
}

// Context
public class PaymentProcessor
{
    private readonly IEnumerable<IPaymentStrategy> _strategies;

    public PaymentProcessor(IEnumerable<IPaymentStrategy> strategies)
    {
        _strategies = strategies;
    }

    public Task<PaymentResult> ProcessAsync(Payment payment)
    {
        var strategy = _strategies.FirstOrDefault(s =>
            s.GetType().Name.StartsWith(payment.Method.ToString()));

        return strategy?.ProcessAsync(payment)
            ?? throw new NotSupportedException($"Payment method {payment.Method} not supported");
    }
}
```

### Factory Pattern

Encapsulate object creation logic.

```csharp
// Simple Factory
public interface INotification
{
    Task SendAsync(string recipient, string message);
}

public class EmailNotification : INotification { /* ... */ }
public class SmsNotification : INotification { /* ... */ }
public class PushNotification : INotification { /* ... */ }

public class NotificationFactory
{
    private readonly IServiceProvider _serviceProvider;

    public NotificationFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public INotification Create(NotificationType type) => type switch
    {
        NotificationType.Email => _serviceProvider.GetRequiredService<EmailNotification>(),
        NotificationType.Sms => _serviceProvider.GetRequiredService<SmsNotification>(),
        NotificationType.Push => _serviceProvider.GetRequiredService<PushNotification>(),
        _ => throw new ArgumentException($"Unknown notification type: {type}")
    };
}

// Abstract Factory
public interface IUIFactory
{
    IButton CreateButton();
    ITextBox CreateTextBox();
    IDropdown CreateDropdown();
}

public class MaterialUIFactory : IUIFactory
{
    public IButton CreateButton() => new MaterialButton();
    public ITextBox CreateTextBox() => new MaterialTextBox();
    public IDropdown CreateDropdown() => new MaterialDropdown();
}

public class BootstrapUIFactory : IUIFactory
{
    public IButton CreateButton() => new BootstrapButton();
    public ITextBox CreateTextBox() => new BootstrapTextBox();
    public IDropdown CreateDropdown() => new BootstrapDropdown();
}
```

### Repository Pattern

Abstract data access logic.

```csharp
// Generic repository interface
public interface IRepository<T> where T : class, IEntity
{
    Task<T?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct = default);
    Task AddAsync(T entity, CancellationToken ct = default);
    void Update(T entity);
    void Delete(T entity);
}

// Specification pattern for complex queries
public interface ISpecification<T>
{
    Expression<Func<T, bool>> Criteria { get; }
    List<Expression<Func<T, object>>> Includes { get; }
    Expression<Func<T, object>>? OrderBy { get; }
    Expression<Func<T, object>>? OrderByDescending { get; }
    int? Take { get; }
    int? Skip { get; }
}

public interface IRepository<T> where T : class, IEntity
{
    Task<IReadOnlyList<T>> ListAsync(ISpecification<T> spec, CancellationToken ct = default);
    Task<T?> FirstOrDefaultAsync(ISpecification<T> spec, CancellationToken ct = default);
    Task<int> CountAsync(ISpecification<T> spec, CancellationToken ct = default);
}

// Usage
public class ActiveAuctionsSpec : Specification<Auction>
{
    public ActiveAuctionsSpec()
    {
        AddCriteria(a => a.Status == AuctionStatus.Active);
        AddCriteria(a => a.EndsAt > DateTime.UtcNow);
        ApplyOrderBy(a => a.EndsAt);
    }
}

var activeAuctions = await _repository.ListAsync(new ActiveAuctionsSpec());
```

### Builder Pattern

Construct complex objects step by step.

```csharp
public class EmailBuilder
{
    private string _from = string.Empty;
    private readonly List<string> _to = new();
    private readonly List<string> _cc = new();
    private string _subject = string.Empty;
    private string _body = string.Empty;
    private bool _isHtml;
    private readonly List<Attachment> _attachments = new();

    public EmailBuilder From(string email)
    {
        _from = email;
        return this;
    }

    public EmailBuilder To(string email)
    {
        _to.Add(email);
        return this;
    }

    public EmailBuilder To(IEnumerable<string> emails)
    {
        _to.AddRange(emails);
        return this;
    }

    public EmailBuilder Cc(string email)
    {
        _cc.Add(email);
        return this;
    }

    public EmailBuilder WithSubject(string subject)
    {
        _subject = subject;
        return this;
    }

    public EmailBuilder WithBody(string body, bool isHtml = false)
    {
        _body = body;
        _isHtml = isHtml;
        return this;
    }

    public EmailBuilder WithAttachment(string path, string name)
    {
        _attachments.Add(new Attachment(path, name));
        return this;
    }

    public Email Build()
    {
        if (string.IsNullOrEmpty(_from))
            throw new InvalidOperationException("From address is required");
        if (!_to.Any())
            throw new InvalidOperationException("At least one recipient is required");

        return new Email(_from, _to, _cc, _subject, _body, _isHtml, _attachments);
    }
}

// Usage
var email = new EmailBuilder()
    .From("noreply@example.com")
    .To("user@example.com")
    .Cc("manager@example.com")
    .WithSubject("Order Confirmation")
    .WithBody("<h1>Thank you for your order!</h1>", isHtml: true)
    .WithAttachment("/invoices/12345.pdf", "invoice.pdf")
    .Build();
```

### Decorator Pattern

Add behavior to objects dynamically.

```csharp
public interface IMessageSender
{
    Task SendAsync(Message message);
}

public class EmailSender : IMessageSender
{
    public Task SendAsync(Message message)
    {
        // Send email
        return Task.CompletedTask;
    }
}

// Decorators
public class LoggingMessageSender : IMessageSender
{
    private readonly IMessageSender _inner;
    private readonly ILogger<LoggingMessageSender> _logger;

    public LoggingMessageSender(IMessageSender inner, ILogger<LoggingMessageSender> logger)
    {
        _inner = inner;
        _logger = logger;
    }

    public async Task SendAsync(Message message)
    {
        _logger.LogInformation("Sending message to {Recipient}", message.Recipient);
        await _inner.SendAsync(message);
        _logger.LogInformation("Message sent successfully");
    }
}

public class RetryMessageSender : IMessageSender
{
    private readonly IMessageSender _inner;
    private readonly int _maxRetries;

    public RetryMessageSender(IMessageSender inner, int maxRetries = 3)
    {
        _inner = inner;
        _maxRetries = maxRetries;
    }

    public async Task SendAsync(Message message)
    {
        for (int i = 0; i < _maxRetries; i++)
        {
            try
            {
                await _inner.SendAsync(message);
                return;
            }
            catch when (i < _maxRetries - 1)
            {
                await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, i)));
            }
        }
    }
}

// Registration with decoration
services.AddScoped<EmailSender>();
services.AddScoped<IMessageSender>(sp =>
    new LoggingMessageSender(
        new RetryMessageSender(
            sp.GetRequiredService<EmailSender>()),
        sp.GetRequiredService<ILogger<LoggingMessageSender>>()));
```

### Observer Pattern (Events)

Define a subscription mechanism for notifications.

```csharp
// Using domain events
public interface IDomainEvent
{
    DateTime OccurredOn { get; }
}

public record OrderPlacedEvent(Order Order) : IDomainEvent
{
    public DateTime OccurredOn { get; } = DateTime.UtcNow;
}

public interface IDomainEventHandler<in TEvent> where TEvent : IDomainEvent
{
    Task HandleAsync(TEvent domainEvent, CancellationToken ct = default);
}

public class SendOrderConfirmationHandler : IDomainEventHandler<OrderPlacedEvent>
{
    private readonly IEmailService _emailService;

    public SendOrderConfirmationHandler(IEmailService emailService)
    {
        _emailService = emailService;
    }

    public Task HandleAsync(OrderPlacedEvent domainEvent, CancellationToken ct)
    {
        return _emailService.SendOrderConfirmationAsync(domainEvent.Order, ct);
    }
}

public class UpdateInventoryHandler : IDomainEventHandler<OrderPlacedEvent>
{
    private readonly IInventoryService _inventoryService;

    public UpdateInventoryHandler(IInventoryService inventoryService)
    {
        _inventoryService = inventoryService;
    }

    public Task HandleAsync(OrderPlacedEvent domainEvent, CancellationToken ct)
    {
        return _inventoryService.ReserveItemsAsync(domainEvent.Order.Items, ct);
    }
}

// Dispatcher
public class DomainEventDispatcher
{
    private readonly IServiceProvider _serviceProvider;

    public async Task DispatchAsync<TEvent>(TEvent domainEvent, CancellationToken ct)
        where TEvent : IDomainEvent
    {
        var handlers = _serviceProvider.GetServices<IDomainEventHandler<TEvent>>();

        foreach (var handler in handlers)
        {
            await handler.HandleAsync(domainEvent, ct);
        }
    }
}
```

---

## Anti-Patterns to Avoid

### God Class

A class that knows too much or does too much.

```csharp
// BAD - God class
public class ApplicationManager
{
    public void CreateUser() { }
    public void DeleteUser() { }
    public void ProcessOrder() { }
    public void GenerateInvoice() { }
    public void SendEmail() { }
    public void BackupDatabase() { }
    public void GenerateReport() { }
    public void AuthenticateUser() { }
    public void ValidatePayment() { }
    // ... 50 more methods
}

// GOOD - Separate into focused classes
public class UserService { }
public class OrderService { }
public class InvoiceService { }
public class EmailService { }
public class BackupService { }
public class ReportService { }
public class AuthenticationService { }
public class PaymentService { }
```

### Anemic Domain Model

Domain objects with only getters/setters and no behavior.

```csharp
// BAD - Anemic model
public class Order
{
    public Guid Id { get; set; }
    public List<OrderItem> Items { get; set; }
    public OrderStatus Status { get; set; }
    public decimal Total { get; set; }
}

public class OrderService
{
    public void AddItem(Order order, Product product, int quantity)
    {
        order.Items.Add(new OrderItem { Product = product, Quantity = quantity });
        order.Total = order.Items.Sum(i => i.Product.Price * i.Quantity);
    }

    public void Submit(Order order)
    {
        if (order.Items.Count == 0)
            throw new InvalidOperationException("Cannot submit empty order");
        order.Status = OrderStatus.Submitted;
    }
}

// GOOD - Rich domain model
public class Order
{
    private readonly List<OrderItem> _items = new();

    public Guid Id { get; private set; }
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();
    public OrderStatus Status { get; private set; }
    public decimal Total => _items.Sum(i => i.Subtotal);

    public void AddItem(Product product, int quantity)
    {
        var existingItem = _items.FirstOrDefault(i => i.ProductId == product.Id);

        if (existingItem != null)
            existingItem.IncreaseQuantity(quantity);
        else
            _items.Add(new OrderItem(product, quantity));
    }

    public void Submit()
    {
        if (!_items.Any())
            throw new DomainException("Cannot submit empty order");

        Status = OrderStatus.Submitted;
        AddDomainEvent(new OrderSubmittedEvent(this));
    }
}
```

### Service Locator

Using a global container to resolve dependencies.

```csharp
// BAD - Service locator anti-pattern
public class OrderProcessor
{
    public void Process(Order order)
    {
        var repository = ServiceLocator.Get<IOrderRepository>();
        var emailService = ServiceLocator.Get<IEmailService>();
        var logger = ServiceLocator.Get<ILogger>();

        repository.Save(order);
        emailService.SendConfirmation(order);
        logger.Log("Order processed");
    }
}

// GOOD - Constructor injection
public class OrderProcessor
{
    private readonly IOrderRepository _repository;
    private readonly IEmailService _emailService;
    private readonly ILogger<OrderProcessor> _logger;

    public OrderProcessor(
        IOrderRepository repository,
        IEmailService emailService,
        ILogger<OrderProcessor> logger)
    {
        _repository = repository;
        _emailService = emailService;
        _logger = logger;
    }

    public async Task ProcessAsync(Order order)
    {
        await _repository.SaveAsync(order);
        await _emailService.SendConfirmationAsync(order);
        _logger.LogInformation("Order {OrderId} processed", order.Id);
    }
}
```

### Magic Strings/Numbers

Using literals without explanation.

```csharp
// BAD - Magic values
public class DiscountService
{
    public decimal Calculate(Order order)
    {
        if (order.Total > 100)
            return order.Total * 0.1m;
        if (order.CustomerType == "gold")
            return order.Total * 0.15m;
        return 0;
    }
}

// GOOD - Named constants
public class DiscountService
{
    private const decimal MinimumOrderForDiscount = 100m;
    private const decimal StandardDiscountRate = 0.10m;
    private const decimal GoldMemberDiscountRate = 0.15m;

    public decimal Calculate(Order order)
    {
        if (order.Customer.MembershipTier == MembershipTier.Gold)
            return order.Total * GoldMemberDiscountRate;

        if (order.Total >= MinimumOrderForDiscount)
            return order.Total * StandardDiscountRate;

        return 0;
    }
}
```

### Primitive Obsession

Overusing primitives instead of small objects.

```csharp
// BAD - Primitive obsession
public class Customer
{
    public string Email { get; set; }        // No validation
    public string PhoneNumber { get; set; }  // No format
    public decimal Balance { get; set; }     // No currency
}

public void SendEmail(string email) { }  // Any string accepted

// GOOD - Value objects
public record Email
{
    public string Value { get; }

    private Email(string value) => Value = value;

    public static Email Create(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new DomainException("Email is required");
        if (!value.Contains('@'))
            throw new DomainException("Invalid email format");
        return new Email(value.ToLowerInvariant());
    }

    public static implicit operator string(Email email) => email.Value;
}

public record Money
{
    public decimal Amount { get; }
    public Currency Currency { get; }

    private Money(decimal amount, Currency currency)
    {
        if (amount < 0)
            throw new DomainException("Amount cannot be negative");
        Amount = amount;
        Currency = currency;
    }

    public static Money Create(decimal amount, Currency currency) =>
        new(amount, currency);

    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new DomainException("Cannot add different currencies");
        return new Money(Amount + other.Amount, Currency);
    }
}

public class Customer
{
    public Email Email { get; private set; }
    public PhoneNumber Phone { get; private set; }
    public Money Balance { get; private set; }
}
```

### Boolean Parameters

Using boolean flags that obscure meaning.

```csharp
// BAD - What does true mean?
SendEmail(user, "Welcome!", true, false, true);

// GOOD - Use enums or separate methods
public enum EmailPriority { Low, Normal, High }

public record EmailOptions
{
    public bool IncludeUnsubscribeLink { get; init; } = true;
    public bool TrackOpens { get; init; } = true;
    public EmailPriority Priority { get; init; } = EmailPriority.Normal;
}

SendEmail(user, "Welcome!", new EmailOptions
{
    Priority = EmailPriority.High,
    TrackOpens = true
});

// Or use separate methods
SendWelcomeEmail(user);
SendPasswordResetEmail(user);
```

---

## Industry Best Practices

### Async/Await

```csharp
// BAD
public Task<User> GetUserAsync(Guid id)
{
    return Task.Run(() => _repository.GetById(id)); // Don't wrap sync in Task.Run
}

public User GetUser(Guid id)
{
    return GetUserAsync(id).Result; // Deadlock risk
}

// GOOD
public async Task<User?> GetUserAsync(Guid id, CancellationToken ct = default)
{
    return await _repository.GetByIdAsync(id, ct);
}

// Async all the way
public async Task<IActionResult> GetUser(Guid id, CancellationToken ct)
{
    var user = await _userService.GetUserAsync(id, ct);
    return user is null ? NotFound() : Ok(user);
}
```

### Null Handling

```csharp
// BAD
public string GetDisplayName(User user)
{
    if (user != null && user.Profile != null && user.Profile.DisplayName != null)
        return user.Profile.DisplayName;
    return "Unknown";
}

// GOOD - Null-conditional and coalescing operators
public string GetDisplayName(User? user) =>
    user?.Profile?.DisplayName ?? "Unknown";

// GOOD - Nullable reference types
public class User
{
    public required string Email { get; init; }
    public string? DisplayName { get; set; }
    public Profile? Profile { get; set; }
}

// GOOD - Option/Maybe pattern for explicit optionality
public async Task<Option<User>> FindUserAsync(Guid id)
{
    var user = await _repository.GetByIdAsync(id);
    return user is null ? Option<User>.None : Option<User>.Some(user);
}
```

### Exception Handling

```csharp
// BAD - Catching and swallowing
try
{
    ProcessOrder(order);
}
catch (Exception ex)
{
    _logger.LogError(ex, "Error");
    // Silently continues...
}

// BAD - Catching too broadly
try
{
    ProcessOrder(order);
}
catch (Exception ex)
{
    return BadRequest(ex.Message); // Exposes internal errors
}

// GOOD - Catch specific, handle appropriately
try
{
    await ProcessOrderAsync(order, ct);
}
catch (ValidationException ex)
{
    _logger.LogWarning(ex, "Validation failed for order {OrderId}", order.Id);
    return BadRequest(new ProblemDetails
    {
        Title = "Validation Error",
        Detail = ex.Message,
        Status = 400
    });
}
catch (PaymentException ex)
{
    _logger.LogError(ex, "Payment failed for order {OrderId}", order.Id);
    return StatusCode(502, new ProblemDetails
    {
        Title = "Payment Processing Error",
        Detail = "Unable to process payment. Please try again.",
        Status = 502
    });
}
// Let unexpected exceptions propagate to global handler
```

### Logging

```csharp
// BAD - String interpolation (loses structured data)
_logger.LogInformation($"User {user.Id} logged in from {ipAddress}");

// BAD - Logging sensitive data
_logger.LogInformation("User login: {User}", JsonSerializer.Serialize(user));

// GOOD - Structured logging
_logger.LogInformation(
    "User {UserId} logged in from {IpAddress}",
    user.Id,
    ipAddress);

// GOOD - Log levels
_logger.LogDebug("Checking user permissions for {Resource}", resourceId);
_logger.LogInformation("User {UserId} created order {OrderId}", userId, orderId);
_logger.LogWarning("Rate limit approaching for {UserId}: {CurrentRate}/{MaxRate}", userId, current, max);
_logger.LogError(ex, "Failed to process order {OrderId}", orderId);
_logger.LogCritical(ex, "Database connection lost");
```

### Configuration

```csharp
// BAD - Hardcoded values
public class EmailService
{
    private readonly string _smtpServer = "smtp.example.com";
    private readonly int _port = 587;
}

// GOOD - Options pattern
public class EmailOptions
{
    public const string SectionName = "Email";

    public required string SmtpServer { get; init; }
    public int Port { get; init; } = 587;
    public required string FromAddress { get; init; }
    public bool UseSsl { get; init; } = true;
}

// appsettings.json
{
  "Email": {
    "SmtpServer": "smtp.example.com",
    "Port": 587,
    "FromAddress": "noreply@example.com"
  }
}

// Registration
services.Configure<EmailOptions>(config.GetSection(EmailOptions.SectionName));

// Usage
public class EmailService
{
    private readonly EmailOptions _options;

    public EmailService(IOptions<EmailOptions> options)
    {
        _options = options.Value;
    }
}
```

### Disposable Resources

```csharp
// BAD - Not disposing
public byte[] ReadFile(string path)
{
    var stream = new FileStream(path, FileMode.Open);
    var reader = new BinaryReader(stream);
    return reader.ReadBytes((int)stream.Length);
    // Stream never closed!
}

// GOOD - Using statement
public async Task<byte[]> ReadFileAsync(string path)
{
    await using var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read, 4096, useAsync: true);
    var buffer = new byte[stream.Length];
    await stream.ReadAsync(buffer);
    return buffer;
}

// GOOD - Implement IDisposable properly
public class ResourceManager : IDisposable
{
    private readonly HttpClient _client = new();
    private bool _disposed;

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed) return;

        if (disposing)
        {
            _client.Dispose();
        }

        _disposed = true;
    }
}
```

---

## Quick Reference

| Principle | Remember |
|-----------|----------|
| SRP | One reason to change |
| OCP | Extend, don't modify |
| LSP | Subtypes are substitutable |
| ISP | Small, focused interfaces |
| DIP | Depend on abstractions |
| DRY | Single source of truth |
| KISS | Simple beats clever |
| YAGNI | Build what you need now |

| Pattern | Use When |
|---------|----------|
| Strategy | Multiple algorithms, swap at runtime |
| Factory | Complex object creation |
| Repository | Abstract data access |
| Builder | Complex object construction |
| Decorator | Add behavior dynamically |
| Observer | Event notifications |

| Anti-Pattern | Solution |
|--------------|----------|
| God Class | Split into focused classes |
| Anemic Model | Add behavior to entities |
| Service Locator | Constructor injection |
| Magic Values | Named constants |
| Primitive Obsession | Value objects |
| Boolean Parameters | Enums or options objects |
