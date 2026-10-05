---
name: design-pattern-suggestor
description: Analyze code structure and recommend applicable GoF and modern design patterns with implementation guides. Use when code has structural problems, excessive.
---

# Design Pattern Suggestor

Analyzes code structure to identify situations where established design patterns (Gang of Four and modern patterns) can improve flexibility, maintainability, and readability. This skill maps common code problems to appropriate pattern solutions and provides language-specific implementation guides.

## When to Use This Skill

Use this skill for:

- Code with excessive conditional logic (long if/else or switch chains) that could benefit from polymorphism
- Tight coupling between components that need to vary independently
- Object creation logic that is complex, duplicated, or scattered across the codebase
- Systems that need to support extension without modifying existing code
- Callback-heavy code that could benefit from an event-driven architecture
- Cross-cutting concerns (logging, caching, validation) that are duplicated in many places
- Complex state machines or workflow logic
- Code that processes data through multiple transformation stages

**Trigger phrases**: "design pattern", "suggest pattern", "which pattern should I use", "strategy pattern", "factory pattern", "observer pattern", "builder pattern", "too many if-else", "tight coupling", "hard to extend", "code structure improvement"

## What This Skill Does

This skill provides pattern recommendation and implementation guidance:

- **Problem-Pattern Mapping**: Maps common code problems (code smells, structural issues) to the design patterns that solve them
- **Pattern Catalog**: Provides a reference of 23 GoF patterns plus modern patterns (Repository, Specification, Circuit Breaker, etc.) with when-to-use criteria
- **Implementation Guides**: Shows concrete implementations in Python, JavaScript, and Java with explanations of each component
- **Trade-off Analysis**: Explains the benefits and costs of applying each pattern so the developer can make an informed decision
- **Anti-Pattern Warnings**: Identifies situations where a pattern would be over-engineering and simpler solutions are preferable

## Instructions

### Step 1: Identify the Problem Category

Map the structural problem in the code to a pattern category.

| Problem Category | Symptoms | Pattern Category |
|-----------------|----------|-----------------|
| **Complex object creation** | Constructors with many parameters, duplicated creation logic, conditional object assembly | Creational Patterns |
| **Rigid class structure** | Cannot add behavior without modifying existing classes, interface explosion | Structural Patterns |
| **Complex control flow** | Long conditional chains, state-dependent behavior, callback nesting | Behavioral Patterns |
| **Tight coupling** | Classes that directly depend on concrete implementations | Dependency Inversion (Factory, DI, Strategy) |
| **Cross-cutting concerns** | Same logic duplicated across many classes (logging, caching, auth) | Decorator, Proxy, Aspect |
| **Extension without modification** | Need to add new behavior without changing existing code | Open/Closed Principle patterns |

### Step 2: Select the Appropriate Pattern

#### Code Smell to Pattern Mapping

| Code Smell / Problem | Recommended Pattern | Why |
|----------------------|-------------------|-----|
| Long if/else or switch on type | **Strategy** | Encapsulate each branch as an interchangeable algorithm |
| Complex object with many optional fields | **Builder** | Step-by-step construction with validation |
| Multiple related objects created together | **Abstract Factory** | Ensure consistent families of objects |
| Conditional object creation based on input | **Factory Method** | Delegate creation to specialized subclasses |
| Need to notify multiple components of state changes | **Observer / Event Emitter** | Decouple publisher from subscribers |
| Need to add behavior to objects dynamically | **Decorator** | Wrap objects with additional behavior at runtime |
| Complex state-dependent behavior | **State** | Encapsulate state-specific behavior in state objects |
| Need to process requests through a series of handlers | **Chain of Responsibility** | Each handler decides to process or pass along |
| Need to undo/redo operations | **Command** | Encapsulate operations as objects with execute/undo |
| Need to traverse complex structures uniformly | **Iterator / Visitor** | Separate traversal logic from structure |
| Need to simplify a complex subsystem interface | **Facade** | Provide a simplified entry point |
| Need to control access to an object | **Proxy** | Intercept calls for caching, logging, access control |
| Need to adapt incompatible interfaces | **Adapter** | Translate between interfaces |
| Need to share common state across many objects | **Flyweight** | Externalize shared state to reduce memory |

### Step 3: Implement the Pattern

#### Strategy Pattern

**Problem**: Long if/else or switch chains that select behavior based on type or category.

**Python Example**:

```python
# BEFORE: Switch chain on payment type
def process_payment(payment_type, amount, details):
    if payment_type == "credit_card":
        # 20 lines of credit card processing logic
        validate_card_number(details["card_number"])
        response = stripe_api.charge(details["card_number"], amount)
        send_receipt(details["email"], response.transaction_id)
        return response
    elif payment_type == "paypal":
        # 20 lines of PayPal processing logic
        token = paypal_api.create_payment(amount, details["paypal_email"])
        response = paypal_api.execute(token)
        send_receipt(details["email"], response.id)
        return response
    elif payment_type == "bank_transfer":
        # 20 lines of bank transfer logic
        reference = bank_api.initiate_transfer(details["routing"], details["account"], amount)
        return {"reference": reference, "status": "pending"}
    elif payment_type == "crypto":
        # ... yet another branch
        pass
    else:
        raise ValueError(f"Unknown payment type: {payment_type}")


# AFTER: Strategy pattern
from abc import ABC, abstractmethod
from typing import Dict, Any


class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, amount: float, details: Dict[str, Any]) -> Dict[str, Any]:
        pass


class CreditCardPayment(PaymentStrategy):
    def __init__(self, stripe_client):
        self.stripe = stripe_client

    def process(self, amount, details):
        validate_card_number(details["card_number"])
        response = self.stripe.charge(details["card_number"], amount)
        send_receipt(details["email"], response.transaction_id)
        return {"transaction_id": response.transaction_id, "status": "completed"}


class PayPalPayment(PaymentStrategy):
    def __init__(self, paypal_client):
        self.paypal = paypal_client

    def process(self, amount, details):
        token = self.paypal.create_payment(amount, details["paypal_email"])
        response = self.paypal.execute(token)
        send_receipt(details["email"], response.id)
        return {"transaction_id": response.id, "status": "completed"}


class BankTransferPayment(PaymentStrategy):
    def __init__(self, bank_client):
        self.bank = bank_client

    def process(self, amount, details):
        reference = self.bank.initiate_transfer(
            details["routing"], details["account"], amount
        )
        return {"reference": reference, "status": "pending"}


# Strategy registry
PAYMENT_STRATEGIES: Dict[str, PaymentStrategy] = {
    "credit_card": CreditCardPayment(stripe_client),
    "paypal": PayPalPayment(paypal_client),
    "bank_transfer": BankTransferPayment(bank_client),
}


def process_payment(payment_type: str, amount: float, details: dict) -> dict:
    strategy = PAYMENT_STRATEGIES.get(payment_type)
    if not strategy:
        raise ValueError(f"Unknown payment type: {payment_type}")
    return strategy.process(amount, details)
```

**JavaScript Example**:

```javascript
// BEFORE: Switch on notification channel
function sendNotification(channel, recipient, message) {
    switch (channel) {
        case "email":
            return emailClient.send(recipient.email, message);
        case "sms":
            return smsClient.send(recipient.phone, message);
        case "push":
            return pushClient.send(recipient.deviceToken, message);
        case "slack":
            return slackClient.send(recipient.slackId, message);
        default:
            throw new Error(`Unknown channel: ${channel}`);
    }
}

// AFTER: Strategy pattern
class EmailNotifier {
    constructor(emailClient) { this.client = emailClient; }
    send(recipient, message) {
        return this.client.send(recipient.email, message);
    }
}

class SmsNotifier {
    constructor(smsClient) { this.client = smsClient; }
    send(recipient, message) {
        return this.client.send(recipient.phone, message);
    }
}

class PushNotifier {
    constructor(pushClient) { this.client = pushClient; }
    send(recipient, message) {
        return this.client.send(recipient.deviceToken, message);
    }
}

const notifiers = {
    email: new EmailNotifier(emailClient),
    sms: new SmsNotifier(smsClient),
    push: new PushNotifier(pushClient),
};

function sendNotification(channel, recipient, message) {
    const notifier = notifiers[channel];
    if (!notifier) throw new Error(`Unknown channel: ${channel}`);
    return notifier.send(recipient, message);
}
```

#### Builder Pattern

**Problem**: Complex objects with many optional parameters, validation requirements, or multi-step construction.

**Java Example**:

```java
// BEFORE: Constructor with 10 parameters (telescoping constructor anti-pattern)
HttpRequest request = new HttpRequest(
    "POST", "https://api.example.com/users", headers, body,
    30000, 3, true, "application/json", null, authToken
);

// AFTER: Builder pattern
public class HttpRequest {
    private final String method;
    private final String url;
    private final Map<String, String> headers;
    private final String body;
    private final int timeoutMs;
    private final int maxRetries;
    private final boolean followRedirects;
    private final String contentType;
    private final String authToken;

    private HttpRequest(Builder builder) {
        this.method = builder.method;
        this.url = builder.url;
        this.headers = Map.copyOf(builder.headers);
        this.body = builder.body;
        this.timeoutMs = builder.timeoutMs;
        this.maxRetries = builder.maxRetries;
        this.followRedirects = builder.followRedirects;
        this.contentType = builder.contentType;
        this.authToken = builder.authToken;
    }

    public static class Builder {
        // Required
        private final String method;
        private final String url;

        // Optional with defaults
        private Map<String, String> headers = new HashMap<>();
        private String body = null;
        private int timeoutMs = 30_000;
        private int maxRetries = 0;
        private boolean followRedirects = true;
        private String contentType = "application/json";
        private String authToken = null;

        public Builder(String method, String url) {
            this.method = Objects.requireNonNull(method);
            this.url = Objects.requireNonNull(url);
        }

        public Builder header(String key, String value) {
            this.headers.put(key, value);
            return this;
        }

        public Builder body(String body) {
            this.body = body;
            return this;
        }

        public Builder timeout(int timeoutMs) {
            if (timeoutMs <= 0) throw new IllegalArgumentException("Timeout must be positive");
            this.timeoutMs = timeoutMs;
            return this;
        }

        public Builder maxRetries(int maxRetries) {
            this.maxRetries = maxRetries;
            return this;
        }

        public Builder followRedirects(boolean follow) {
            this.followRedirects = follow;
            return this;
        }

        public Builder contentType(String contentType) {
            this.contentType = contentType;
            return this;
        }

        public Builder authToken(String token) {
            this.authToken = token;
            return this;
        }

        public HttpRequest build() {
            // Validation
            if ("POST".equals(method) && body == null) {
                throw new IllegalStateException("POST requests require a body");
            }
            return new HttpRequest(this);
        }
    }
}

// Usage: clear, self-documenting, validated
HttpRequest request = new HttpRequest.Builder("POST", "https://api.example.com/users")
    .body(jsonPayload)
    .authToken(token)
    .timeout(5000)
    .maxRetries(3)
    .header("X-Request-Id", requestId)
    .build();
```

#### Observer / Event Emitter Pattern

**Problem**: Multiple components need to react to state changes, but tight coupling makes the system rigid.

**Python Example**:

```python
# BEFORE: Tight coupling -- OrderService directly calls every dependent service
class OrderService:
    def __init__(self, inventory, email, analytics, audit, notifications):
        self.inventory = inventory
        self.email = email
        self.analytics = analytics
        self.audit = audit
        self.notifications = notifications

    def place_order(self, order):
        self.save(order)
        # Directly coupled to every downstream concern
        self.inventory.reserve(order.items)
        self.email.send_confirmation(order)
        self.analytics.track_purchase(order)
        self.audit.log_order(order)
        self.notifications.notify_warehouse(order)


# AFTER: Observer pattern (event-driven)
from typing import Callable, Dict, List


class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, data):
        for handler in self._handlers.get(event_type, []):
            handler(data)


class OrderService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def place_order(self, order):
        self.save(order)
        self.event_bus.publish("order.placed", order)


# Each concern subscribes independently
event_bus = EventBus()
event_bus.subscribe("order.placed", lambda order: inventory.reserve(order.items))
event_bus.subscribe("order.placed", lambda order: email.send_confirmation(order))
event_bus.subscribe("order.placed", lambda order: analytics.track_purchase(order))
event_bus.subscribe("order.placed", lambda order: audit.log_order(order))
event_bus.subscribe("order.placed", lambda order: notifications.notify_warehouse(order))
```

#### Decorator Pattern

**Problem**: Need to add behavior (logging, caching, validation, retry) to existing objects without modifying their code.

**JavaScript Example**:

```javascript
// BEFORE: Logging, caching, and retry logic mixed into business logic
class UserRepository {
    async findById(id) {
        console.log(`[${new Date().toISOString()}] Finding user ${id}`);

        const cached = this.cache.get(`user:${id}`);
        if (cached) {
            console.log(`Cache hit for user ${id}`);
            return cached;
        }

        let attempts = 0;
        while (attempts < 3) {
            try {
                const user = await this.db.query("SELECT * FROM users WHERE id = ?", [id]);
                this.cache.set(`user:${id}`, user, 300);
                return user;
            } catch (err) {
                attempts++;
                if (attempts >= 3) throw err;
                await new Promise(r => setTimeout(r, 1000 * attempts));
            }
        }
    }
}

// AFTER: Decorator pattern separates cross-cutting concerns
class UserRepository {
    async findById(id) {
        return this.db.query("SELECT * FROM users WHERE id = ?", [id]);
    }
}

// Logging decorator
function withLogging(repository) {
    const original = repository.findById.bind(repository);
    repository.findById = async function(id) {
        console.log(`[${new Date().toISOString()}] Finding user ${id}`);
        const result = await original(id);
        console.log(`[${new Date().toISOString()}] Found user ${id}`);
        return result;
    };
    return repository;
}

// Caching decorator
function withCaching(repository, cache, ttl = 300) {
    const original = repository.findById.bind(repository);
    repository.findById = async function(id) {
        const key = `user:${id}`;
        const cached = cache.get(key);
        if (cached) return cached;
        const result = await original(id);
        cache.set(key, result, ttl);
        return result;
    };
    return repository;
}

// Retry decorator
function withRetry(repository, maxAttempts = 3) {
    const original = repository.findById.bind(repository);
    repository.findById = async function(id) {
        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return await original(id);
            } catch (err) {
                if (attempt >= maxAttempts) throw err;
                await new Promise(r => setTimeout(r, 1000 * attempt));
            }
        }
    };
    return repository;
}

// Compose decorators (order matters: retry wraps cache wraps logging wraps base)
let repo = new UserRepository(db);
repo = withLogging(repo);
repo = withCaching(repo, cache);
repo = withRetry(repo);
```

#### Factory Method Pattern

**Problem**: Object creation logic is conditional and scattered, or new types need to be added without modifying existing code.

**Java Example**:

```java
// BEFORE: Conditional creation scattered across the codebase
public Document parseDocument(String filePath) {
    String extension = getExtension(filePath);
    if ("pdf".equals(extension)) {
        return new PdfDocument(filePath);
    } else if ("docx".equals(extension)) {
        return new WordDocument(filePath);
    } else if ("xlsx".equals(extension)) {
        return new ExcelDocument(filePath);
    } else if ("csv".equals(extension)) {
        return new CsvDocument(filePath);
    }
    throw new UnsupportedFormatException(extension);
}

// AFTER: Factory pattern with registry
public interface DocumentParser {
    Document parse(String filePath);
    boolean supports(String extension);
}

public class PdfParser implements DocumentParser {
    public boolean supports(String ext) { return "pdf".equals(ext); }
    public Document parse(String filePath) { return new PdfDocument(filePath); }
}

public class WordParser implements DocumentParser {
    public boolean supports(String ext) { return "docx".equals(ext); }
    public Document parse(String filePath) { return new WordDocument(filePath); }
}

public class DocumentParserFactory {
    private final List<DocumentParser> parsers;

    public DocumentParserFactory(List<DocumentParser> parsers) {
        this.parsers = parsers;
    }

    public Document parse(String filePath) {
        String ext = getExtension(filePath);
        return parsers.stream()
            .filter(p -> p.supports(ext))
            .findFirst()
            .orElseThrow(() -> new UnsupportedFormatException(ext))
            .parse(filePath);
    }
}

// Adding a new format requires only a new parser class, no modification to existing code
public class MarkdownParser implements DocumentParser {
    public boolean supports(String ext) { return "md".equals(ext); }
    public Document parse(String filePath) { return new MarkdownDocument(filePath); }
}
```

### Step 4: Evaluate Pattern Trade-offs

Before applying a pattern, evaluate whether the added complexity is justified.

| Pattern | Benefits | Costs | Apply When |
|---------|----------|-------|------------|
| **Strategy** | Eliminates conditionals, easy to add variants | More classes, indirection | 3+ variants that change independently |
| **Builder** | Clear construction, validation, immutability | Verbose boilerplate | >4 optional parameters or complex validation |
| **Observer** | Loose coupling, easy to add listeners | Debugging harder, event ordering | 3+ listeners or listeners change at runtime |
| **Decorator** | Composable behavior, single responsibility | Deep wrapping chains, ordering matters | 2+ cross-cutting concerns applied selectively |
| **Factory** | Centralized creation, open/closed principle | Extra abstraction layer | Conditional creation with 3+ types |
| **State** | Eliminates state-checking conditionals | Many small classes | 3+ states with different behaviors |
| **Command** | Undo/redo, queueing, logging operations | Object per operation | Need to undo, queue, or log operations |
| **Facade** | Simplified interface to complex subsystem | Hides capabilities, can become god object | Subsystem has >5 classes clients must coordinate |

### Step 5: Recognize When NOT to Apply a Pattern

Not every problem needs a design pattern. Simpler solutions are preferred when they suffice.

| Situation | Why a Pattern is Overkill | Simpler Alternative |
|-----------|--------------------------|-------------------|
| Only 2 variants in a conditional | Strategy adds unnecessary indirection | Simple if/else |
| Object has 3 required fields, no optionals | Builder adds boilerplate for no benefit | Constructor or factory method |
| One listener for an event | Observer machinery is overhead | Direct method call |
| Cross-cutting concern applies everywhere uniformly | Decorator composition is unnecessary | Middleware or AOP |
| Only one type needs creation | Factory adds abstraction without benefit | Direct instantiation |

## Best Practices

- **Let the problem drive the pattern**: identify the structural problem first, then find the pattern that solves it; do not start with a pattern and look for places to apply it
- **Start simple and refactor toward patterns**: begin with the simplest implementation, then introduce a pattern when the code demonstrates the need (third similar case, or when a change becomes painful)
- **Name classes after the pattern role**: `PaymentStrategy`, `HttpRequestBuilder`, `OrderEventObserver` make the pattern explicit and help future readers understand the design intent
- **Combine patterns judiciously**: patterns compose well (Strategy + Factory, Decorator + Builder), but combining more than 2-3 patterns in one module is a sign of over-engineering
- **Document the pattern choice**: add a brief comment or architecture decision record explaining which pattern was chosen and why, especially if the simpler alternative was considered and rejected
- **Use language idioms over classical patterns**: Python functions as strategies (no need for a Strategy interface), JavaScript closures as commands, Java records as value objects; adapt patterns to the language
- **Prefer composition over inheritance**: most GoF patterns work through composition (Strategy, Decorator, Observer) rather than inheritance; this leads to more flexible designs

## Common Pitfalls

- **Applying patterns prematurely**: introducing a Strategy pattern for a two-branch conditional adds complexity without benefit; wait for the third variant or evidence of change
- **Pattern worship**: treating design patterns as mandatory checkboxes rather than tools to solve specific problems leads to over-engineered code
- **Misidentifying the problem**: applying a Builder when the real issue is a god class, or applying a Strategy when the real issue is unclear requirements; diagnose accurately before prescribing a pattern
- **Ignoring language features**: many patterns exist to work around limitations of certain languages; Python does not need a Singleton class (use a module), JavaScript does not need a classical Iterator (use generators), Java records eliminate the need for some Builder patterns
- **Creating deep decorator chains**: more than 3-4 layers of decoration become difficult to debug and reason about; consider using middleware or pipeline patterns instead
- **Over-abstracting Factory patterns**: if the factory requires as much conditional logic as the original creation code, the abstraction has not simplified anything
- **Forgetting about testability**: design patterns should make code easier to test by enabling mock injection and isolating behavior; if a pattern makes testing harder, reconsider the approach
- **Not considering the team's familiarity**: introducing uncommon patterns (Visitor, Flyweight, Mediator) to a team unfamiliar with them can reduce rather than improve maintainability; choose patterns the team understands or invest in education first
