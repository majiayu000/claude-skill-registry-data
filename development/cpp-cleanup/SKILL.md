---
name: cpp-cleanup
description: Modernize to C++17/20, apply RAII patterns, use smart pointers, and clean up C++ codebases. Use when cleaning up C++ projects, modernizing legacy C++ code.
---

# C++ Code Cleanup

Systematically identify and remove dead code, apply modern C++ idioms, and use RAII patterns to maintain a clean, safe, and maintainable codebase.

## When to Use This Skill

Use this skill when you need to:

- Remove unused includes and dead code
- Convert raw pointers to smart pointers
- Apply modern C++ features (11/14/17/20)
- Fix clang-tidy warnings
- Apply RAII patterns
- Clean up before code review

**Trigger phrases**: "cleanup C++", "modernize C++", "smart pointers", "RAII", "C++ refactor", "fix clang-tidy"

## What This Skill Does

### Cleanup Areas

1. **Dead Code Removal**
   - Unused #include directives
   - Unused functions and classes
   - Unreachable code
   - Redundant code

2. **Memory Safety**
   - Raw pointer to smart pointer
   - RAII patterns
   - Move semantics
   - Resource management

3. **Modernization**
   - Modern C++ features
   - STL algorithms
   - Range-based loops
   - constexpr

## Instructions

### Step 1: Run Analysis Tools

```bash
# Run clang-tidy
clang-tidy *.cpp -checks='*' --

# Run cppcheck
cppcheck --enable=all --inconclusive .

# Build with all warnings
g++ -std=c++17 -Wall -Wextra -Wpedantic -Werror *.cpp

# Run sanitizers
g++ -std=c++17 -fsanitize=address,undefined *.cpp
./a.out
```

### Step 2: Apply Modern C++11 Patterns

#### Auto Keyword

```cpp
// Before - verbose type declarations
std::map<std::string, std::vector<int>>::iterator it = myMap.begin();

// After - use auto for clarity
auto it = myMap.begin();

// Use auto for complex return types
auto result = computeComplexResult();

// But be explicit when it aids readability
int count = 0;  // Clear that it's an int
```

#### Range-Based For Loops

```cpp
// Before
for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) {
    process(*it);
}

// After
for (const auto& item : vec) {
    process(item);
}

// For modification
for (auto& item : vec) {
    item.update();
}
```

#### nullptr Instead of NULL

```cpp
// Before
int* ptr = NULL;
if (ptr == 0) { ... }

// After
int* ptr = nullptr;
if (ptr == nullptr) { ... }
```

#### Override and Final

```cpp
// Before
class Derived : public Base {
    virtual void process();  // Is this an override?
};

// After
class Derived : public Base {
    void process() override;  // Compiler verifies override
};

class Final : public Base {
    void process() final;  // Prevent further override
};

class NoInherit final : public Base {
    // Class cannot be inherited
};
```

#### Uniform Initialization

```cpp
// Before - different initialization syntaxes
int x = 5;
std::string s("hello");
std::vector<int> v;
v.push_back(1);
v.push_back(2);

// After - uniform brace initialization
int x{5};
std::string s{"hello"};
std::vector<int> v{1, 2, 3};

// Prevents narrowing conversions
int x{3.14};  // Error! Narrowing conversion
```

### Step 3: Smart Pointers

#### unique_ptr for Ownership

```cpp
// Before - raw pointer ownership
class Manager {
    Widget* widget;
public:
    Manager() : widget(new Widget()) {}
    ~Manager() { delete widget; }  // Must remember to delete
};

// After - unique_ptr
class Manager {
    std::unique_ptr<Widget> widget;
public:
    Manager() : widget(std::make_unique<Widget>()) {}
    // Destructor automatically handles cleanup
};
```

#### shared_ptr for Shared Ownership

```cpp
// Before - manual reference counting
class Resource {
    int refCount;
    // Complex manual management
};

// After - shared_ptr
auto resource = std::make_shared<Resource>();
auto copy = resource;  // Automatic reference counting
// Automatically deleted when last reference goes out of scope
```

#### weak_ptr for Breaking Cycles

```cpp
// Before - circular reference causes leak
struct Node {
    std::shared_ptr<Node> next;
    std::shared_ptr<Node> prev;  // Circular reference!
};

// After - weak_ptr breaks cycle
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;  // Doesn't keep alive

    void accessPrev() {
        if (auto p = prev.lock()) {
            // Use p
        }
    }
};
```

### Step 4: RAII Patterns

#### Resource Management

```cpp
// Before - manual resource management
void process() {
    FILE* f = fopen("data.txt", "r");
    if (!f) return;

    // ... many lines ...

    if (error) {
        fclose(f);  // Must remember
        return;
    }

    fclose(f);  // Must remember
}

// After - RAII wrapper
class FileHandle {
    FILE* f;
public:
    explicit FileHandle(const char* name, const char* mode)
        : f(fopen(name, mode)) {}
    ~FileHandle() { if (f) fclose(f); }
    operator FILE*() { return f; }
    explicit operator bool() const { return f != nullptr; }
};

void process() {
    FileHandle f("data.txt", "r");
    if (!f) return;

    // ... many lines ...

    if (error) return;  // Automatic cleanup

    // Automatic cleanup at end
}
```

#### Lock Guards

```cpp
// Before - manual lock management
void process() {
    mutex.lock();
    // ... work ...
    if (error) {
        mutex.unlock();  // Must remember
        return;
    }
    mutex.unlock();  // Must remember
}

// After - RAII lock guard
void process() {
    std::lock_guard<std::mutex> lock(mutex);
    // ... work ...
    if (error) return;  // Automatic unlock
    // Automatic unlock at end
}

// Or scoped_lock for multiple mutexes (C++17)
void transfer(Account& a, Account& b) {
    std::scoped_lock lock(a.mutex, b.mutex);
    // Both locked, deadlock-free
}
```

### Step 5: Move Semantics

#### Move Constructor and Assignment

```cpp
// Before - expensive copies
class Buffer {
    char* data;
    size_t size;
public:
    Buffer(const Buffer& other) {
        size = other.size;
        data = new char[size];
        memcpy(data, other.data, size);  // Expensive copy
    }
};

// After - move semantics
class Buffer {
    char* data;
    size_t size;
public:
    // Copy constructor
    Buffer(const Buffer& other) : size(other.size), data(new char[size]) {
        memcpy(data, other.data, size);
    }

    // Move constructor - steal resources
    Buffer(Buffer&& other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
    }

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
};
```

#### std::move Usage

```cpp
// Use std::move for explicit moves
std::vector<Buffer> buffers;
Buffer b;
buffers.push_back(std::move(b));  // Move instead of copy

// Return value optimization - don't use std::move
Buffer createBuffer() {
    Buffer b;
    return b;  // RVO applies, don't use std::move
}
```

### Step 6: C++14/17 Features

#### make_unique (C++14)

```cpp
// Before
std::unique_ptr<Widget> w(new Widget(1, 2));

// After
auto w = std::make_unique<Widget>(1, 2);
```

#### Structured Bindings (C++17)

```cpp
// Before
std::pair<int, std::string> result = getResult();
int code = result.first;
std::string message = result.second;

// After
auto [code, message] = getResult();

// Works with arrays, tuples, structs
std::map<std::string, int> m;
for (const auto& [key, value] : m) {
    std::cout << key << ": " << value << "\n";
}
```

#### std::optional (C++17)

```cpp
// Before - using pointer or sentinel value
int* findValue(const std::string& key);

// After - optional
std::optional<int> findValue(const std::string& key) {
    if (auto it = map.find(key); it != map.end()) {
        return it->second;
    }
    return std::nullopt;
}

// Usage
if (auto value = findValue("key"); value) {
    process(*value);
}
```

#### std::string_view (C++17)

```cpp
// Before - string copies
void process(const std::string& s);
process("literal");  // Creates temporary string

// After - string_view for read-only
void process(std::string_view s);
process("literal");  // No copy

// Use for substrings
std::string_view sv = "Hello, World!";
auto hello = sv.substr(0, 5);  // No allocation
```

#### if with Initializer (C++17)

```cpp
// Before
auto it = map.find(key);
if (it != map.end()) {
    process(it->second);
}

// After
if (auto it = map.find(key); it != map.end()) {
    process(it->second);
}
```

### Step 7: C++20 Features

#### Concepts

```cpp
// Before - SFINAE
template<typename T, typename = std::enable_if_t<std::is_integral_v<T>>>
T add(T a, T b) { return a + b; }

// After - concepts
template<std::integral T>
T add(T a, T b) { return a + b; }

// Custom concept
template<typename T>
concept Printable = requires(T t) {
    { std::cout << t } -> std::same_as<std::ostream&>;
};

template<Printable T>
void print(const T& value) {
    std::cout << value << "\n";
}
```

#### Ranges

```cpp
// Before
std::vector<int> result;
std::copy_if(v.begin(), v.end(), std::back_inserter(result),
    [](int x) { return x > 0; });
std::transform(result.begin(), result.end(), result.begin(),
    [](int x) { return x * 2; });

// After - ranges
auto result = v
    | std::views::filter([](int x) { return x > 0; })
    | std::views::transform([](int x) { return x * 2; });
```

#### Three-Way Comparison

```cpp
// Before - implement all comparison operators
bool operator<(const Widget& other) const;
bool operator>(const Widget& other) const;
bool operator<=(const Widget& other) const;
// ... etc

// After - spaceship operator
auto operator<=>(const Widget&) const = default;
```

### Step 8: STL Algorithms

```cpp
// Before - manual loops
bool found = false;
for (const auto& item : items) {
    if (item.matches(criteria)) {
        found = true;
        break;
    }
}

// After - algorithms
bool found = std::any_of(items.begin(), items.end(),
    [&](const auto& item) { return item.matches(criteria); });

// More examples
auto it = std::find_if(v.begin(), v.end(), predicate);
std::transform(v.begin(), v.end(), v.begin(), transform_fn);
std::sort(v.begin(), v.end(), comparator);
auto count = std::count_if(v.begin(), v.end(), predicate);
```

## Tools

- **clang-tidy**: Linting and modernization
- **cppcheck**: Static analysis
- **clang-format**: Code formatting
- **PVS-Studio**: Commercial analyzer
- **AddressSanitizer**: Memory errors
- **UndefinedBehaviorSanitizer**: UB detection
- **Valgrind**: Memory debugging

## Quality Checklist

- [ ] Unused includes removed
- [ ] Raw pointers converted to smart pointers
- [ ] RAII patterns applied
- [ ] Move semantics implemented
- [ ] Modern C++ features used
- [ ] clang-tidy clean
- [ ] No memory leaks (ASan clean)
- [ ] No undefined behavior (UBSan clean)
- [ ] Build clean with -Wall -Wextra
- [ ] Tests pass

## Common Issues and Solutions

### Issue: Raw pointer ownership unclear
**Solution**: Use smart pointers to express ownership:
```cpp
// Unique ownership
std::unique_ptr<Widget> widget;

// Shared ownership
std::shared_ptr<Widget> widget;

// Non-owning reference
Widget* widget;  // or std::reference_wrapper
```

### Issue: Resource leak in exception
**Solution**: Use RAII:
```cpp
// Before
void process() {
    auto* resource = acquire();
    doWork();  // May throw!
    release(resource);
}

// After
void process() {
    auto resource = std::make_unique<Resource>();
    doWork();  // Exception safe
}
```

### Issue: Unnecessary copies
**Solution**: Use references and move semantics:
```cpp
// Pass by const reference
void process(const std::vector<int>& data);

// Return by value (RVO)
std::vector<int> generate();

// Move large objects
container.push_back(std::move(largeObject));
```

## Related Skills

- `code-review-quality` - Code quality assessment
- `security-review` - Security analysis

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates code_cleanup/cpp_cleanup.md


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
