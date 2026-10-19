---
name: java-development
description: >
  Develop, refactor, and review modern Java applications (Java 17/21 LTS)
  following clean OOP and functional paradigms. Use when writing immutable Records,
  pattern matching with switch, sealed class hierarchies, designing clean generic
  APIs, writing JUnit 5 tests, or configuring Maven/Gradle build manifests.
compatibility: >
  Agent Skills-compatible coding agents operating on Java 17+ codebases
  with Maven or Gradle build tools.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "java, records, pattern-matching, sealed-classes, maven, gradle, junit5"
  topics: "programming-languages, software-development"
---

# Modern Java Development (Java 17 / 21 LTS)

Modern Java has evolved beyond verbose boilerplate into a concise, expressive language featuring immutable **Records**, **Sealed Classes**, **Pattern Matching**, and **Virtual Threads (Project Loom)**. Follow modern Java standards, avoid antiquated getters/setters patterns where records fit, and write robust, type-safe APIs.

## Core Rules

1. **Use Records for transparent data carriers**: Replace boilerplate classes containing private fields, getters, `equals()`, `hashCode()`, and `toString()` with `record`.
2. **Model closed type hierarchies with Sealed Classes**: Use `sealed interface` or `sealed class` to control inheritance and enable exhaustive compiler pattern matching.
3. **Use pattern matching for `instanceof` and `switch`**: Eliminate manual casts after type checks.
4. **Never return `null` for collections**: Return `List.of()`, `Set.of()`, or `Collections.emptyList()` instead of `null`. Use `Optional<T>` for single nullable return values.
5. **Always use try-with-resources**: AutoCloseable resources (streams, connections, files) must be managed within `try (...)` blocks.
6. **Prefer constructor injection**: Avoid field injection (`@Autowired` on private fields); constructor injection enforces immutability and simplifies unit testing.

---

## 1. Immutable Data: Records

Records automatically generate private final fields, canonical constructors, accessor methods, `equals`, `hashCode`, and `toString`:

```java
package com.example.model;

import java.time.Instant;
import java.util.Objects;

public record OrderItem(String sku, int quantity, long unitPriceCents) {
    // Compact constructor for validation
    public OrderItem {
        Objects.requireNonNull(sku, "SKU must not be null");
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive: " + quantity);
        }
        if (unitPriceCents < 0) {
            throw new IllegalArgumentException("Unit price cannot be negative");
        }
    }

    public long totalCents() {
        return (long) quantity * unitPriceCents;
    }
}
```

---

## 2. Sealed Types & Exhaustive Pattern Matching

Sealed interfaces restrict which classes can implement them, allowing the compiler to verify that all possible subclasses are handled:

```java
package com.example.event;

public sealed interface PaymentStatus permits PaymentStatus.Pending, PaymentStatus.Success, PaymentStatus.Failed {
    record Pending(String trackingId) implements PaymentStatus {}
    record Success(String transactionId, long amount) implements PaymentStatus {}
    record Failed(String errorCode, String reason) implements PaymentStatus {}
}
```

Pattern matching switch (exhaustive, no `default` clause needed!):
```java
public String formatStatus(PaymentStatus status) {
    return switch (status) {
        case PaymentStatus.Pending p -> "Processing payment: " + p.trackingId();
        case PaymentStatus.Success s -> "Paid " + s.amount() + " [Tx: " + s.transactionId() + "]";
        case PaymentStatus.Failed f  -> "Declined: " + f.reason() + " (Code: " + f.errorCode() + ")";
    };
}
```

---

## 3. Safe Resource Lifecycles (Try-with-Resources)

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class LogParser {
    public long countErrorLines(String filePath) throws IOException {
        try (var reader = new BufferedReader(new FileReader(filePath))) {
            return reader.lines()
                    .filter(line -> line.contains("[ERROR]"))
                    .count();
        } // reader is automatically closed even if an exception occurs
    }
}
```

---

## 4. Testing with JUnit 5 & AssertJ

```java
package com.example;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.assertj.core.api.Assertions.*;

class OrderItemTest {

    @Test
    @DisplayName("Calculates correct total price for valid items")
    void calculatesTotal() {
        var item = new OrderItem("PROD-01", 3, 1500L);
        assertThat(item.totalCents()).isEqualTo(4500L);
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1, -10})
    @DisplayName("Rejects non-positive quantities with IllegalArgumentException")
    void rejectsInvalidQuantity(int invalidQty) {
        assertThatThrownBy(() -> new OrderItem("PROD-01", invalidQty, 100L))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Quantity must be positive");
    }
}
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| Returning `null` for empty collections | Callers crash with `NullPointerException` | Return `List.of()`, `Set.of()`, or `Collections.emptyList()` |
| Catching generic `Exception` | Catches unchecked runtime bugs (NPE, OOM) unintentionally | Catch specific checked exceptions (`IOException`, `SQLException`) |
| Using `==` on boxed primitives (`Integer`) | Evaluates true for values -128..127, false above | Always use `.equals()` for object comparison |
| Double-Checked Locking without `volatile` | Broken singleton due to instruction reordering | Use static initialization holder or enums |
| Raw types in Generics (`List items`) | Loss of compile-time type safety | Always specify type parameter (`List<String> items`) |

---

## 6. Verification Checklist

- [ ] Immutable data containers authored as `record`.
- [ ] No raw types used in Generics.
- [ ] Resources managed via `try-with-resources`.
- [ ] Code passes SpotBugs or Checkstyle rules without violations.
- [ ] Maven (`mvn clean verify`) or Gradle (`./gradlew check`) passes all tests.
