---
# ═══════════════════════════════════════════════════════════════════════════════
# SKILL: OOP Patterns
# Version: 3.0.0 | SASMP v1.3.0 Compliant | Production-Grade
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# IDENTITY
# ─────────────────────────────────────────────────────────────────────────────
name: oop-patterns
version: "3.0.0"
description: >
  Production-grade skill for Object-Oriented Programming in C++. Covers classes,
  inheritance, polymorphism, encapsulation, SOLID principles, and design patterns.

# ─────────────────────────────────────────────────────────────────────────────
# COMPLIANCE
# ─────────────────────────────────────────────────────────────────────────────
sasmp_version: "1.3.0"
skill_version: "3.0.0"

# ─────────────────────────────────────────────────────────────────────────────
# BONDING
# ─────────────────────────────────────────────────────────────────────────────
bonded_agent: cpp-oop-agent
bond_type: PRIMARY_BOND
category: learning

# ─────────────────────────────────────────────────────────────────────────────
# PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
parameters:
  concept:
    type: string
    required: true
    enum: [classes, inheritance, polymorphism, encapsulation, solid, patterns]
  pattern_name:
    type: string
    required: false
    enum: [factory, singleton, observer, strategy, decorator, adapter]
  output_format:
    type: string
    required: false
    enum: [explanation, code_example, uml, refactoring]
    default: code_example

# ─────────────────────────────────────────────────────────────────────────────
# ERROR HANDLING
# ─────────────────────────────────────────────────────────────────────────────
error_handling:
  retry_logic:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 500
    jitter: true
  fallback:
    on_design_error: "suggest_alternative_pattern"
    on_violation: "explain_principle_and_fix"
---

# OOP Patterns Skill

**Production-Grade Learning Skill** | Object-Oriented Design

Master C++ OOP concepts and industry-standard design patterns.

---

## The Four Pillars

### 1. Encapsulation

```cpp
class BankAccount {
private:
    std::string id_;
    double balance_{0.0};  // Default member init

public:
    explicit BankAccount(std::string id) : id_(std::move(id)) {}

    // Read-only access
    [[nodiscard]] double balance() const { return balance_; }
    [[nodiscard]] const std::string& id() const { return id_; }

    // Controlled mutation with validation
    void deposit(double amount) {
        if (amount <= 0) {
            throw std::invalid_argument("Amount must be positive");
        }
        balance_ += amount;
    }

    bool withdraw(double amount) {
        if (amount <= 0 || amount > balance_) return false;
        balance_ -= amount;
        return true;
    }
};
```

### 2. Inheritance

```cpp
// Abstract base class
class Shape {
protected:
    std::string name_;

public:
    explicit Shape(std::string name) : name_(std::move(name)) {}
    virtual ~Shape() = default;  // ALWAYS virtual destructor!

    // Pure virtual functions (interface)
    [[nodiscard]] virtual double area() const = 0;
    [[nodiscard]] virtual double perimeter() const = 0;

    // Non-virtual (shared behavior)
    [[nodiscard]] const std::string& name() const { return name_; }
};

class Circle final : public Shape {  // final prevents further inheritance
    double radius_;
public:
    explicit Circle(double r) : Shape("Circle"), radius_(r) {}

    [[nodiscard]] double area() const override {
        return std::numbers::pi * radius_ * radius_;
    }

    [[nodiscard]] double perimeter() const override {
        return 2 * std::numbers::pi * radius_;
    }
};
```

### 3. Polymorphism

```cpp
// Runtime polymorphism via virtual functions
void printShape(const Shape& shape) {
    std::cout << shape.name() << ": area = " << shape.area() << "\n";
}

// Usage - same function, different behavior
std::vector<std::unique_ptr<Shape>> shapes;
shapes.push_back(std::make_unique<Circle>(5.0));
shapes.push_back(std::make_unique<Rectangle>(3.0, 4.0));

for (const auto& shape : shapes) {
    printShape(*shape);  // Polymorphic dispatch
}
```

### 4. Abstraction

```cpp
// Pure interface (all pure virtual)
class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void log(std::string_view message) = 0;
    virtual void setLevel(int level) = 0;
};

// Multiple implementations
class ConsoleLogger : public ILogger {
public:
    void log(std::string_view message) override {
        std::cout << "[LOG] " << message << "\n";
    }
    void setLevel(int) override { }
};

class FileLogger : public ILogger {
    std::ofstream file_;
public:
    explicit FileLogger(const std::string& path) : file_(path) {}
    void log(std::string_view message) override {
        file_ << message << "\n";
    }
    void setLevel(int) override { }
};
```

---

## SOLID Principles

| Principle | Summary | C++ Example |
|-----------|---------|-------------|
| **S**ingle Responsibility | One class, one reason to change | Separate `User` from `UserSerializer` |
| **O**pen/Closed | Open for extension, closed for modification | Virtual functions, inheritance |
| **L**iskov Substitution | Subtypes must be substitutable | Square shouldn't inherit Rectangle |
| **I**nterface Segregation | Prefer small, specific interfaces | Split `IWorker` into `IWorkable`, `IFeedable` |
| **D**ependency Inversion | Depend on abstractions | Inject `IDatabase&` not `MySQLDatabase` |

---

## Design Patterns

### Factory Pattern

```cpp
class ShapeFactory {
public:
    static std::unique_ptr<Shape> create(std::string_view type, double param) {
        if (type == "circle") {
            return std::make_unique<Circle>(param);
        }
        if (type == "square") {
            return std::make_unique<Square>(param);
        }
        throw std::invalid_argument("Unknown shape type");
    }
};

// Usage
auto shape = ShapeFactory::create("circle", 5.0);
```

### Singleton Pattern (Thread-Safe)

```cpp
class Logger {
private:
    Logger() = default;

public:
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;

    static Logger& instance() {
        static Logger instance;  // Thread-safe in C++11
        return instance;
    }

    void log(std::string_view msg) { std::cout << msg << "\n"; }
};
```

### Observer Pattern

```cpp
class IObserver {
public:
    virtual ~IObserver() = default;
    virtual void onNotify(const std::string& event) = 0;
};

class Subject {
    std::vector<IObserver*> observers_;
public:
    void attach(IObserver* obs) { observers_.push_back(obs); }
    void detach(IObserver* obs) {
        observers_.erase(std::remove(observers_.begin(), observers_.end(), obs),
                        observers_.end());
    }
    void notify(const std::string& event) {
        for (auto* obs : observers_) {
            obs->onNotify(event);
        }
    }
};
```

### Strategy Pattern

```cpp
class ICompressionStrategy {
public:
    virtual ~ICompressionStrategy() = default;
    virtual std::vector<uint8_t> compress(std::span<const uint8_t> data) = 0;
};

class ZipStrategy : public ICompressionStrategy {
public:
    std::vector<uint8_t> compress(std::span<const uint8_t> data) override {
        // ZIP compression
        return {};
    }
};

class Compressor {
    std::unique_ptr<ICompressionStrategy> strategy_;
public:
    void setStrategy(std::unique_ptr<ICompressionStrategy> s) {
        strategy_ = std::move(s);
    }
    std::vector<uint8_t> compress(std::span<const uint8_t> data) {
        return strategy_->compress(data);
    }
};
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Object slicing | Passing by value | Use references/pointers |
| Memory leak | Missing virtual destructor | Add `virtual ~Base() = default;` |
| Diamond problem | Multiple inheritance | Use virtual inheritance |
| Tight coupling | Direct dependencies | Inject interfaces |

---

## Unit Test Template

```cpp
#include <gtest/gtest.h>

TEST(ShapeTest, CircleArea) {
    Circle c(5.0);
    EXPECT_NEAR(c.area(), 78.5398, 0.0001);
}

TEST(ShapeTest, Polymorphism) {
    std::unique_ptr<Shape> shape = std::make_unique<Circle>(1.0);
    EXPECT_EQ(shape->name(), "Circle");
}

TEST(FactoryTest, CreateCircle) {
    auto shape = ShapeFactory::create("circle", 5.0);
    EXPECT_NE(shape, nullptr);
    EXPECT_EQ(shape->name(), "Circle");
}
```

---

*C++ Plugin v3.0.0 - Production-Grade Learning Skill*
