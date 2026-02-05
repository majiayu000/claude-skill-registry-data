---
name: effective-java
description: Java best practices guide based on Effective Java. Use when reviewing Java code, discussing design patterns, object creation, equals/hashCode, Optional, Stream API, exception handling, or concurrency. Applies Joshua Bloch's principles.
---

# Effective Java Best Practices

IMPORTANT: All output must be in Traditional Chinese.

## Creating Objects

### Item 1: Static Factory Methods over Constructors

```java
// GOOD - Static factory with descriptive name
public static Order createPending(CustomerId customerId, List<OrderItem> items) {
    return new Order(OrderId.generate(), customerId, items, OrderStatus.PENDING);
}

public static Order reconstitute(OrderId id, CustomerId customerId,
        List<OrderItem> items, OrderStatus status) {
    return new Order(id, customerId, items, status);
}

// BAD - Constructor doesn't convey intent
public Order(OrderId id, CustomerId customerId, List<OrderItem> items, OrderStatus status)
```

**Advantages:**
- Descriptive names (`createEmpty`, `valueOf`, `of`, `from`)
- Can return cached instances
- Can return subtypes
- Reduces verbosity with type inference

### Item 2: Builder Pattern for Many Parameters

```java
// GOOD - Builder for complex objects
public class HttpRequest {
    private final String url;
    private final String method;
    private final Map<String, String> headers;
    private final Duration timeout;
    private final int retries;

    private HttpRequest(Builder builder) {
        this.url = builder.url;
        this.method = builder.method;
        this.headers = Map.copyOf(builder.headers);
        this.timeout = builder.timeout;
        this.retries = builder.retries;
    }

    public static Builder builder(String url) {
        return new Builder(url);
    }

    public static class Builder {
        private final String url;
        private String method = "GET";
        private final Map<String, String> headers = new HashMap<>();
        private Duration timeout = Duration.ofSeconds(30);
        private int retries = 3;

        private Builder(String url) {
            this.url = Objects.requireNonNull(url);
        }

        public Builder method(String method) {
            this.method = method;
            return this;
        }

        public Builder header(String key, String value) {
            this.headers.put(key, value);
            return this;
        }

        public Builder timeout(Duration timeout) {
            this.timeout = timeout;
            return this;
        }

        public HttpRequest build() {
            return new HttpRequest(this);
        }
    }
}

// Usage
HttpRequest request = HttpRequest.builder("https://api.example.com")
    .method("POST")
    .header("Content-Type", "application/json")
    .timeout(Duration.ofSeconds(10))
    .build();
```

### Item 6: Avoid Creating Unnecessary Objects

```java
// BAD - Creates new Boolean on each call
Boolean.valueOf("true");  // Fine, but...
new Boolean("true");       // NEVER do this

// BAD - Pattern compiled on every call
public boolean isValidEmail(String email) {
    return email.matches("^[A-Za-z0-9+_.-]+@(.+)$");  // Compiles pattern each time!
}

// GOOD - Compile once, reuse
private static final Pattern EMAIL_PATTERN =
    Pattern.compile("^[A-Za-z0-9+_.-]+@(.+)$");

public boolean isValidEmail(String email) {
    return EMAIL_PATTERN.matcher(email).matches();
}

// BAD - Autoboxing in loop
Long sum = 0L;
for (long i = 0; i < 1_000_000; i++) {
    sum += i;  // Creates ~1M Long objects!
}

// GOOD - Use primitive
long sum = 0L;
for (long i = 0; i < 1_000_000; i++) {
    sum += i;
}
```

---

## Classes and Interfaces

### Item 15: Minimize Accessibility

```java
// BAD - Exposes internal state
public class Order {
    public List<OrderItem> items;  // Mutable field exposed!
}

// GOOD - Proper encapsulation
public class Order {
    private final List<OrderItem> items;

    public List<OrderItem> getItems() {
        return Collections.unmodifiableList(items);
    }
}
```

### Item 17: Minimize Mutability

```java
// GOOD - Immutable Value Object using record
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        Objects.requireNonNull(amount);
        Objects.requireNonNull(currency);
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
    }

    public Money add(Money other) {
        validateSameCurrency(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }
}

// For complex objects, use Builder + private constructor
public final class Transaction {
    private final String id;
    private final Money amount;
    private final LocalDateTime timestamp;

    private Transaction(Builder builder) { /* ... */ }

    // No setters - all fields final
}
```

### Item 18: Favor Composition over Inheritance

```java
// BAD - Inheritance breaks encapsulation
public class InstrumentedHashSet<E> extends HashSet<E> {
    private int addCount = 0;

    @Override
    public boolean add(E e) {
        addCount++;
        return super.add(e);  // Works
    }

    @Override
    public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();
        return super.addAll(c);  // BUG: addAll calls add(), double counting!
    }
}

// GOOD - Composition (Wrapper/Decorator)
public class InstrumentedSet<E> implements Set<E> {
    private final Set<E> delegate;
    private int addCount = 0;

    public InstrumentedSet(Set<E> delegate) {
        this.delegate = delegate;
    }

    @Override
    public boolean add(E e) {
        addCount++;
        return delegate.add(e);
    }

    @Override
    public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();
        return delegate.addAll(c);  // Correct: delegates without calling our add()
    }

    // Delegate all other Set methods...
}
```

---

## Methods Common to All Objects

### Item 10 & 11: equals and hashCode Contract

```java
public class OrderId {
    private final String value;

    public OrderId(String value) {
        this.value = Objects.requireNonNull(value);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof OrderId other)) return false;
        return value.equals(other.value);
    }

    @Override
    public int hashCode() {
        return Objects.hash(value);
    }
}

// Or simply use record (auto-generates equals/hashCode)
public record OrderId(String value) {
    public OrderId {
        Objects.requireNonNull(value);
    }
}
```

**Rules:**
- Override `hashCode` when you override `equals`
- Equal objects must have equal hash codes
- Use `Objects.hash()` for simple cases
- Consider caching hash code for expensive computations

---

## Generics

### Item 26: Don't Use Raw Types

```java
// BAD - Raw type, loses type safety
List orders = new ArrayList();
orders.add("not an order");  // Compiles, fails at runtime

// GOOD - Parameterized type
List<Order> orders = new ArrayList<>();
orders.add("not an order");  // Compile error!
```

### Item 31: Use Bounded Wildcards (PECS)

**Producer Extends, Consumer Super**

```java
// Producer - reads from collection, use extends
public void processOrders(List<? extends Order> orders) {
    for (Order order : orders) {  // Can read as Order
        process(order);
    }
}

// Consumer - writes to collection, use super
public void addOrders(List<? super Order> destination) {
    destination.add(new Order());  // Can write Order
}

// Example: Copying from producer to consumer
public static <T> void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) {
        dest.add(item);
    }
}
```

---

## Lambdas and Streams

### Item 42: Prefer Lambdas to Anonymous Classes

```java
// BAD - Verbose anonymous class
Collections.sort(orders, new Comparator<Order>() {
    @Override
    public int compare(Order o1, Order o2) {
        return o1.getCreatedAt().compareTo(o2.getCreatedAt());
    }
});

// GOOD - Lambda
orders.sort((o1, o2) -> o1.getCreatedAt().compareTo(o2.getCreatedAt()));

// BETTER - Method reference
orders.sort(Comparator.comparing(Order::getCreatedAt));
```

### Item 45: Use Streams Judiciously

```java
// GOOD - Clear, readable stream
List<String> customerNames = orders.stream()
    .filter(o -> o.getStatus() == OrderStatus.CONFIRMED)
    .map(Order::getCustomerId)
    .distinct()
    .map(customerRepository::findById)
    .flatMap(Optional::stream)
    .map(Customer::getName)
    .sorted()
    .toList();

// BAD - Overusing streams, hard to debug
orders.stream()
    .collect(groupingBy(Order::getCustomerId,
        collectingAndThen(
            reducing((o1, o2) -> o1.getTotal() > o2.getTotal() ? o1 : o2),
            opt -> opt.map(Order::getTotal).orElse(Money.ZERO)
        )
    ))
    .entrySet().stream()
    .sorted(Map.Entry.<CustomerId, Money>comparingByValue().reversed())
    .limit(10)
    .forEach(e -> log.info("{}: {}", e.getKey(), e.getValue()));

// GOOD - Use loop when clearer
Map<CustomerId, Order> largestByCustomer = new HashMap<>();
for (Order order : orders) {
    largestByCustomer.merge(order.getCustomerId(), order,
        (existing, current) -> existing.getTotal() > current.getTotal() ? existing : current);
}
```

### Item 46: Prefer Side-Effect-Free Functions

```java
// BAD - Side effects in stream
List<Order> processed = new ArrayList<>();
orders.stream()
    .filter(Order::isPending)
    .forEach(o -> {
        o.confirm();           // Mutating!
        processed.add(o);      // Side effect!
        orderRepository.save(o);  // Side effect!
    });

// GOOD - Collect, then process
List<Order> pendingOrders = orders.stream()
    .filter(Order::isPending)
    .toList();

for (Order order : pendingOrders) {
    order.confirm();
    orderRepository.save(order);
}
```

---

## Exceptions

### Item 69: Use Exceptions for Exceptional Conditions

```java
// BAD - Using exception for flow control
try {
    int i = 0;
    while (true) {
        process(array[i++]);
    }
} catch (ArrayIndexOutOfBoundsException e) {
    // Done
}

// GOOD - Normal control flow
for (int i = 0; i < array.length; i++) {
    process(array[i]);
}
```

### Item 72: Favor Standard Exceptions

| Exception | Use Case |
|-----------|----------|
| `IllegalArgumentException` | Invalid parameter value |
| `IllegalStateException` | Object in wrong state for method |
| `NullPointerException` | Null where prohibited |
| `UnsupportedOperationException` | Method not supported |
| `NoSuchElementException` | No element available |

### Item 73: Throw Appropriate to Abstraction

```java
// BAD - Low-level exception leaks
public Order findOrder(OrderId id) {
    try {
        return jdbcTemplate.queryForObject(...);
    } catch (EmptyResultDataAccessException e) {
        throw e;  // Exposes implementation detail!
    }
}

// GOOD - Translate to domain exception
public Order findOrder(OrderId id) {
    try {
        return jdbcTemplate.queryForObject(...);
    } catch (EmptyResultDataAccessException e) {
        throw new OrderNotFoundException(id, e);
    }
}
```

---

## Code Review Checklist

| Check | Good | Bad |
|-------|------|-----|
| Object creation | Static factory / Builder | Telescoping constructors |
| Value objects | `record` or immutable class | Mutable with setters |
| Collections | `List.of()`, `Map.of()`, `unmodifiableList` | Exposed mutable collections |
| Optional | `orElseThrow()`, `map()`, `filter()` | `get()` without `isPresent()` |
| Streams | Reasonable pipeline, side-effect free | Complex nested collectors, mutations |
| Exceptions | Domain-specific, standard exceptions | Generic Exception, flow control |
| Generics | Bounded wildcards (PECS) | Raw types |

---

## Additional Resources

For detailed explanations:
- **references/object-creation.md** - Items 1-9 complete guide
- **references/classes-and-interfaces.md** - Items 15-25 details
- **references/lambdas-streams.md** - Stream API patterns
- **references/concurrency.md** - Thread safety patterns
