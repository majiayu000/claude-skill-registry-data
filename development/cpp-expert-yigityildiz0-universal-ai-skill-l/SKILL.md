---
name: cpp-expert
description: Deep C++ expertise for systems and performance-critical development. Use when writing modern C++ code, implementing RAII and smart pointers, designing.
---

# C++ Expert

Specialized expertise in modern C++ programming, providing deep guidance on RAII, smart pointers, templates, concepts, move semantics, concurrency primitives, memory optimization, and testing with GoogleTest. Covers C++17 through C++23 features with a focus on safety, performance, and idiomatic patterns.

## When to Use This Skill

Use this skill for:

- Writing modern C++ (C++17/20/23) code
- Implementing RAII and smart pointer ownership models
- Designing templates and constraining them with concepts
- Applying move semantics and perfect forwarding
- Building concurrent and parallel applications
- Optimizing memory layout and cache performance
- Testing with GoogleTest and GMock

**Trigger phrases**: "c++", "cpp", "modern c++", "RAII", "smart pointer", "template", "concepts", "move semantics", "constexpr", "std::thread"

## What This Skill Does

Provides C++ expertise including:

- **Modern Fundamentals**: auto, structured bindings, constexpr/consteval/constinit, modules, spaceship operator
- **Ownership**: RAII, unique_ptr, shared_ptr, weak_ptr, custom deleters
- **Generic Programming**: Templates, concepts, variadic templates, fold expressions
- **Value Semantics**: Move constructors, perfect forwarding, Rule of Five/Zero
- **Concurrency**: Threads, mutexes, atomics, latches, barriers, async tasks
- **Performance**: Custom allocators, cache-friendly layouts, SoA vs AoS, PMR
- **Testing**: GoogleTest, GMock, parameterized tests, death tests, sanitizers

## Instructions

### Step 1: Master Modern C++ Fundamentals

**Auto and Structured Bindings**:

```cpp
#include <map>
#include <string>
#include <tuple>

// auto deduces the type from the initializer
auto count = 42;                  // int
auto ratio = 3.14;                // double
auto name  = std::string{"Ada"};  // std::string (not const char*)

// Trailing return type for complex deductions
auto divide(int a, int b) -> std::pair<int, int> {
    return {a / b, a % b};
}

// Structured bindings (C++17) unpack aggregates into named variables
auto [quotient, remainder] = divide(17, 5);

// Iterate a map with structured bindings
std::map<std::string, int> scores{{"Alice", 95}, {"Bob", 87}};
for (const auto& [name, score] : scores) {
    std::println("{}: {}", name, score);  // C++23 print
}

// Structured bindings work with arrays and custom types too
int arr[3] = {10, 20, 30};
auto [x, y, z] = arr;
```

**Constexpr, Consteval, and Constinit**:

```cpp
// constexpr: may be evaluated at compile time or runtime
constexpr int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) result *= i;
    return result;
}

// consteval (C++20): must be evaluated at compile time
consteval int compile_time_square(int n) {
    return n * n;
}
static_assert(compile_time_square(5) == 25);

// constinit (C++20): ensures static/thread-local variable is constant-initialized
// Prevents the "static initialization order fiasco"
constinit int global_limit = factorial(5);  // Initialized at compile time

// if constexpr: compile-time branch elimination
template <typename T>
auto stringify(T value) -> std::string {
    if constexpr (std::is_arithmetic_v<T>) {
        return std::to_string(value);
    } else if constexpr (std::is_same_v<T, std::string>) {
        return value;
    } else {
        static_assert(false, "Unsupported type");
    }
}
```

**Designated Initializers and Spaceship Operator**:

```cpp
// Designated initializers (C++20) make aggregate init self-documenting
struct Config {
    std::string host = "localhost";
    int port         = 8080;
    int max_conns    = 100;
    bool tls         = false;
};

Config cfg{.port = 9090, .tls = true};  // Only override what you need

// Three-way comparison / spaceship operator (C++20)
#include <compare>

struct Version {
    int major;
    int minor;
    int patch;

    auto operator<=>(const Version&) const = default;  // Generates all 6 operators
};

Version v1{2, 1, 0}, v2{2, 3, 0};
bool older = (v1 < v2);  // true, generated automatically
```

**Modules (C++20)**:

```cpp
// math.cppm (module interface unit)
export module math;

export int add(int a, int b) { return a + b; }
export int multiply(int a, int b) { return a * b; }

// main.cpp (consumer)
import math;

int main() {
    return add(2, multiply(3, 4));  // No header needed
}
```

### Step 2: Apply RAII and Smart Pointers

**unique_ptr for Exclusive Ownership**:

```cpp
#include <memory>
#include <vector>

// unique_ptr: exactly one owner, zero overhead over raw pointer
auto widget = std::make_unique<Widget>("example", 42);
widget->activate();

// Transfer ownership with std::move
auto transferred = std::move(widget);
// widget is now nullptr; transferred owns the object

// unique_ptr in containers
std::vector<std::unique_ptr<Shape>> shapes;
shapes.push_back(std::make_unique<Circle>(5.0));
shapes.push_back(std::make_unique<Rectangle>(3.0, 4.0));

for (const auto& shape : shapes) {
    shape->draw();  // Polymorphic call
}

// Factory functions return unique_ptr to express ownership transfer
auto createParser(const std::string& format) -> std::unique_ptr<Parser> {
    if (format == "json") return std::make_unique<JsonParser>();
    if (format == "xml")  return std::make_unique<XmlParser>();
    return nullptr;
}
```

**shared_ptr and weak_ptr**:

```cpp
// shared_ptr: reference-counted shared ownership
auto config = std::make_shared<Config>();  // One allocation for object + control block

auto worker1 = std::thread([config] { config->read(); });
auto worker2 = std::thread([config] { config->read(); });
// config is destroyed when the last shared_ptr goes out of scope

// weak_ptr: non-owning observer that breaks cycles
struct Node {
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> parent;  // weak_ptr prevents circular reference leak
};

// Check if the observed object still exists
std::weak_ptr<Config> observer = config;
if (auto locked = observer.lock()) {
    locked->read();  // Safe access
} else {
    // Object has been destroyed
}
```

**Custom Deleters and RAII Wrappers for C APIs**:

```cpp
// Custom deleter for C library resources (e.g., FILE*, sqlite3*)
auto file_deleter = [](FILE* fp) {
    if (fp) std::fclose(fp);
};
std::unique_ptr<FILE, decltype(file_deleter)> file(
    std::fopen("data.bin", "rb"), file_deleter
);

// Generic RAII wrapper for any C handle
template <typename Handle, auto Deleter>
class UniqueHandle {
    Handle handle_;
public:
    explicit UniqueHandle(Handle h) : handle_(h) {}
    ~UniqueHandle() { if (handle_) Deleter(handle_); }

    UniqueHandle(const UniqueHandle&) = delete;
    UniqueHandle& operator=(const UniqueHandle&) = delete;
    UniqueHandle(UniqueHandle&& other) noexcept : handle_(std::exchange(other.handle_, {})) {}
    UniqueHandle& operator=(UniqueHandle&& other) noexcept {
        if (this != &other) {
            if (handle_) Deleter(handle_);
            handle_ = std::exchange(other.handle_, {});
        }
        return *this;
    }

    Handle get() const { return handle_; }
    explicit operator bool() const { return handle_ != Handle{}; }
};

// Usage with a C library
using UniqueFd = UniqueHandle<int, +[](int fd) { ::close(fd); }>;
UniqueFd socket(::socket(AF_INET, SOCK_STREAM, 0));
```

### Step 3: Design Templates and Concepts

**Function and Class Templates**:

```cpp
// Function template with automatic deduction
template <typename T>
T max_of(T a, T b) {
    return (a > b) ? a : b;
}

auto result = max_of(3.14, 2.71);  // Deduces T = double

// Class template with deduction guide (C++17 CTAD)
template <typename T>
class Stack {
    std::vector<T> data_;
public:
    void push(const T& value) { data_.push_back(value); }
    T pop() {
        T top = std::move(data_.back());
        data_.pop_back();
        return top;
    }
    bool empty() const { return data_.empty(); }
};

Stack s{42};  // CTAD deduces Stack<int>
```

**Variadic Templates and Fold Expressions**:

```cpp
// Variadic template: accept any number of arguments
template <typename... Args>
void log(const std::string& fmt, Args&&... args) {
    std::println(fmt, std::forward<Args>(args)...);
}

// Fold expressions (C++17) collapse parameter packs
template <typename... Args>
auto sum(Args... args) {
    return (args + ...);  // Unary right fold: a1 + (a2 + (a3 + ...))
}

auto total = sum(1, 2, 3, 4, 5);  // 15

// Fold with comma operator for side effects
template <typename... Args>
void print_all(Args&&... args) {
    ((std::cout << args << ' '), ...);
    std::cout << '\n';
}

// Check if all types satisfy a predicate
template <typename... Ts>
constexpr bool all_integral = (std::is_integral_v<Ts> && ...);
static_assert(all_integral<int, long, char>);
```

**C++20 Concepts (Replacing SFINAE)**:

```cpp
#include <concepts>

// Define a concept: a named set of constraints
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

// Use concept as a constraint (cleaner than SFINAE)
template <Numeric T>
T clamp(T value, T lo, T hi) {
    return (value < lo) ? lo : (value > hi) ? hi : value;
}

// Concept with requires-clause for complex constraints
template <typename C>
concept Sortable = requires(C container) {
    { container.begin() } -> std::random_access_iterator;
    { container.size() }  -> std::convertible_to<std::size_t>;
    requires std::totally_ordered<typename C::value_type>;
};

template <Sortable C>
void sort_container(C& c) {
    std::ranges::sort(c);
}

// Abbreviated function template with auto + concept
void process(Numeric auto value) {
    // value is constrained to Numeric types
}

// Template specialization
template <typename T>
struct Serializer {
    static std::string serialize(const T& value) {
        return std::to_string(value);  // Default for arithmetic types
    }
};

template <>
struct Serializer<std::string> {
    static std::string serialize(const std::string& value) {
        return "\"" + value + "\"";  // Strings get quoted
    }
};
```

### Step 4: Apply Move Semantics and Perfect Forwarding

**Rvalue References and std::move**:

```cpp
#include <utility>
#include <vector>
#include <string>

// std::move casts to rvalue reference, enabling move instead of copy
std::string source = "large payload";
std::string dest = std::move(source);
// source is now in a valid but unspecified state (likely empty)

// Moving into containers avoids copies
std::vector<std::string> names;
std::string name = "temporary";
names.push_back(std::move(name));  // Moves instead of copying
```

**Move Constructor and Rule of Five/Zero**:

```cpp
// Rule of Zero: if your class manages no resources, declare nothing
struct Point {
    double x, y, z;
    // Compiler generates copy, move, destructor automatically
};

// Rule of Five: if you manage a resource, declare all five
class Buffer {
    std::size_t size_;
    std::byte* data_;

public:
    explicit Buffer(std::size_t size)
        : size_(size), data_(new std::byte[size]{}) {}

    ~Buffer() { delete[] data_; }

    // Copy constructor
    Buffer(const Buffer& other)
        : size_(other.size_), data_(new std::byte[other.size_]) {
        std::memcpy(data_, other.data_, size_);
    }

    // Copy assignment
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            Buffer tmp(other);       // Copy-and-swap idiom
            swap(*this, tmp);
        }
        return *this;
    }

    // Move constructor (noexcept enables optimizations in containers)
    Buffer(Buffer&& other) noexcept
        : size_(std::exchange(other.size_, 0)),
          data_(std::exchange(other.data_, nullptr)) {}

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = std::exchange(other.size_, 0);
            data_ = std::exchange(other.data_, nullptr);
        }
        return *this;
    }

    friend void swap(Buffer& a, Buffer& b) noexcept {
        std::swap(a.size_, b.size_);
        std::swap(a.data_, b.data_);
    }
};
```

**Perfect Forwarding**:

```cpp
// std::forward preserves the value category (lvalue or rvalue) of arguments
template <typename... Args>
auto make_widget(Args&&... args) -> std::unique_ptr<Widget> {
    return std::make_unique<Widget>(std::forward<Args>(args)...);
}

// Without forward, rvalues would be treated as lvalues inside the function
// With forward, temporaries remain temporaries and trigger move constructors

// Emplace uses perfect forwarding to construct in-place
std::vector<std::pair<std::string, int>> entries;
entries.emplace_back("key", 42);  // Constructs pair directly, no copies

// Forwarding reference vs rvalue reference
template <typename T>
void wrapper(T&& arg) {           // Forwarding reference (deduced context)
    inner(std::forward<T>(arg));  // Preserves lvalue/rvalue
}

void takes_rvalue(std::string&& s);  // Rvalue reference (concrete type)
```

### Step 5: Build Concurrent Applications

**Threads and Joining**:

```cpp
#include <thread>
#include <mutex>
#include <shared_mutex>
#include <atomic>
#include <future>
#include <latch>
#include <barrier>

// std::jthread (C++20) joins automatically on destruction
void parallel_compute(std::span<const double> input, std::span<double> output) {
    auto worker = [&](std::size_t begin, std::size_t end) {
        for (auto i = begin; i < end; ++i) {
            output[i] = expensive_transform(input[i]);
        }
    };

    auto mid = input.size() / 2;
    std::jthread t1(worker, 0, mid);
    std::jthread t2(worker, mid, input.size());
    // Both threads join when t1 and t2 go out of scope
}
```

**Mutexes and Lock Guards**:

```cpp
class ThreadSafeCache {
    mutable std::shared_mutex mutex_;
    std::unordered_map<std::string, std::string> data_;

public:
    // Multiple readers allowed simultaneously
    auto get(const std::string& key) const -> std::optional<std::string> {
        std::shared_lock lock(mutex_);  // Shared (read) lock
        auto it = data_.find(key);
        return (it != data_.end()) ? std::optional{it->second} : std::nullopt;
    }

    // Exclusive access for writes
    void put(const std::string& key, const std::string& value) {
        std::unique_lock lock(mutex_);  // Exclusive (write) lock
        data_[key] = value;
    }

    // Lock multiple mutexes without deadlock
    void merge_from(ThreadSafeCache& other) {
        std::scoped_lock lock(mutex_, other.mutex_);  // Locks both, deadlock-free
        data_.merge(other.data_);
    }
};
```

**Atomics and Async Tasks**:

```cpp
// Atomic for lock-free counters and flags
std::atomic<int> request_count{0};
std::atomic<bool> shutdown_requested{false};

void handle_request() {
    request_count.fetch_add(1, std::memory_order_relaxed);
    // Process request...
}

// std::async for fire-and-forget tasks with futures
auto future_result = std::async(std::launch::async, [] {
    return compute_heavy_result();
});
// Do other work...
auto result = future_result.get();  // Blocks until ready

// std::latch (C++20): single-use countdown barrier
void parallel_init(std::span<Subsystem*> systems) {
    std::latch ready(systems.size());

    for (auto* sys : systems) {
        std::jthread([sys, &ready] {
            sys->initialize();
            ready.count_down();  // Signal completion
        });
    }

    ready.wait();  // Block until all subsystems initialized
}

// std::barrier (C++20): reusable synchronization point
void iterative_solver(int iterations, int num_threads) {
    std::barrier sync_point(num_threads, [] noexcept {
        // Completion function runs once per phase
    });

    auto worker = [&](int id) {
        for (int i = 0; i < iterations; ++i) {
            compute_local(id);
            sync_point.arrive_and_wait();  // All threads synchronize
            exchange_boundaries(id);
            sync_point.arrive_and_wait();  // Synchronize again
        }
    };

    std::vector<std::jthread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back(worker, i);
    }
}
```

**Condition Variables**:

```cpp
template <typename T>
class BoundedQueue {
    std::queue<T> queue_;
    std::mutex mutex_;
    std::condition_variable not_empty_;
    std::condition_variable not_full_;
    std::size_t max_size_;

public:
    explicit BoundedQueue(std::size_t max_size) : max_size_(max_size) {}

    void push(T item) {
        std::unique_lock lock(mutex_);
        not_full_.wait(lock, [&] { return queue_.size() < max_size_; });
        queue_.push(std::move(item));
        not_empty_.notify_one();
    }

    T pop() {
        std::unique_lock lock(mutex_);
        not_empty_.wait(lock, [&] { return !queue_.empty(); });
        T item = std::move(queue_.front());
        queue_.pop();
        not_full_.notify_one();
        return item;
    }
};
```

### Step 6: Optimize Memory and Performance

**Cache-Friendly Data Structures (SoA vs AoS)**:

```cpp
// Array of Structures (AoS): poor cache utilization when accessing one field
struct ParticleAoS {
    float x, y, z;       // position
    float vx, vy, vz;    // velocity
    float mass;
    int   type;
};
std::vector<ParticleAoS> particles_aos(10'000);

// Structure of Arrays (SoA): cache-friendly when iterating one field
struct ParticlesSoA {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;
    std::vector<float> mass;
    std::vector<int>   type;

    explicit ParticlesSoA(std::size_t n)
        : x(n), y(n), z(n), vx(n), vy(n), vz(n), mass(n), type(n) {}
};

// Updating positions touches only x, y, z and vx, vy, vz (contiguous in memory)
void update_positions(ParticlesSoA& p, float dt) {
    for (std::size_t i = 0; i < p.x.size(); ++i) {
        p.x[i] += p.vx[i] * dt;
        p.y[i] += p.vy[i] * dt;
        p.z[i] += p.vz[i] * dt;
    }
}
```

**Custom Allocators and PMR**:

```cpp
#include <memory_resource>
#include <vector>

// Polymorphic Memory Resource (std::pmr) lets you swap allocators at runtime
void process_batch(std::span<const Record> records) {
    // Stack-based buffer for small allocations (no heap, no fragmentation)
    std::array<std::byte, 16'384> buffer;
    std::pmr::monotonic_buffer_resource pool(buffer.data(), buffer.size());

    // Vector uses the stack buffer; falls back to default if exhausted
    std::pmr::vector<Result> results(&pool);
    results.reserve(records.size());

    for (const auto& rec : records) {
        results.push_back(transform(rec));
    }
}

// Placement new: construct an object in pre-allocated memory
alignas(Widget) std::byte storage[sizeof(Widget)];
Widget* w = new (storage) Widget(args...);
// Must call destructor manually
w->~Widget();
```

**Benchmarking with Google Benchmark**:

```cpp
#include <benchmark/benchmark.h>

// Basic benchmark
static void BM_VectorPushBack(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> v;
        for (int i = 0; i < state.range(0); ++i) {
            v.push_back(i);
        }
        benchmark::DoNotOptimize(v.data());  // Prevent dead-code elimination
    }
}
BENCHMARK(BM_VectorPushBack)->Range(8, 1 << 20);

// Compare reserved vs unreserved
static void BM_VectorReserved(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> v;
        v.reserve(state.range(0));
        for (int i = 0; i < state.range(0); ++i) {
            v.push_back(i);
        }
        benchmark::DoNotOptimize(v.data());
    }
}
BENCHMARK(BM_VectorReserved)->Range(8, 1 << 20);

// Benchmark with custom counters
static void BM_StringConcat(benchmark::State& state) {
    std::string base(state.range(0), 'x');
    for (auto _ : state) {
        std::string result = base + base;
        benchmark::DoNotOptimize(result);
    }
    state.SetBytesProcessed(state.iterations() * state.range(0) * 2);
}
BENCHMARK(BM_StringConcat)->RangeMultiplier(4)->Range(64, 1 << 16);

BENCHMARK_MAIN();
```

### Step 7: Test with GoogleTest and GMock

**Basic Tests and Fixtures**:

```cpp
#include <gtest/gtest.h>

// Simple test
TEST(MathTest, Addition) {
    EXPECT_EQ(add(2, 3), 5);
    EXPECT_DOUBLE_EQ(divide(10.0, 3.0), 3.3333333333333335);
}

// EXPECT continues on failure; ASSERT aborts the test
TEST(ParserTest, ParseValidInput) {
    auto result = parse("42");
    ASSERT_TRUE(result.has_value()) << "parse returned nullopt";  // Aborts if false
    EXPECT_EQ(result.value(), 42);  // Only runs if ASSERT passed
}

// Test fixture: shared setup and teardown
class DatabaseTest : public ::testing::Test {
protected:
    void SetUp() override {
        db_ = std::make_unique<Database>(":memory:");
        db_->execute("CREATE TABLE users (id INT, name TEXT)");
    }
    void TearDown() override { db_.reset(); }

    std::unique_ptr<Database> db_;
};

TEST_F(DatabaseTest, InsertAndQuery) {
    db_->execute("INSERT INTO users VALUES (1, 'Alice')");
    auto rows = db_->query("SELECT name FROM users WHERE id = 1");
    ASSERT_EQ(rows.size(), 1u);
    EXPECT_EQ(rows[0]["name"], "Alice");
}

TEST_F(DatabaseTest, EmptyTableReturnsNoRows) {
    auto rows = db_->query("SELECT * FROM users");
    EXPECT_TRUE(rows.empty());
}
```

**Parameterized Tests**:

```cpp
// Value-parameterized tests
class FizzBuzzTest : public ::testing::TestWithParam<std::pair<int, std::string>> {};

TEST_P(FizzBuzzTest, ProducesCorrectOutput) {
    auto [input, expected] = GetParam();
    EXPECT_EQ(fizzbuzz(input), expected);
}

INSTANTIATE_TEST_SUITE_P(
    FizzBuzzCases,
    FizzBuzzTest,
    ::testing::Values(
        std::pair{1, "1"},
        std::pair{3, "Fizz"},
        std::pair{5, "Buzz"},
        std::pair{15, "FizzBuzz"}
    )
);

// Type-parameterized tests for generic code
template <typename T>
class StackTest : public ::testing::Test {
protected:
    Stack<T> stack_;
};

using StackTypes = ::testing::Types<int, double, std::string>;
TYPED_TEST_SUITE(StackTest, StackTypes);

TYPED_TEST(StackTest, PushAndPop) {
    TypeParam value{};  // Default-constructed value of the type under test
    this->stack_.push(value);
    EXPECT_FALSE(this->stack_.empty());
    EXPECT_EQ(this->stack_.pop(), value);
    EXPECT_TRUE(this->stack_.empty());
}
```

**Death Tests and GMock**:

```cpp
// Death tests verify that code terminates as expected
TEST(ContractTest, NullPointerAborts) {
    EXPECT_DEATH(dereference(nullptr), "");  // Expects termination
}

TEST(ContractTest, OutOfRangeThrows) {
    std::vector<int> v{1, 2, 3};
    EXPECT_THROW(v.at(10), std::out_of_range);
    EXPECT_NO_THROW(v.at(0));
}

// GMock for interface mocking
#include <gmock/gmock.h>

class Logger {
public:
    virtual ~Logger() = default;
    virtual void log(const std::string& message) = 0;
    virtual int count() const = 0;
};

class MockLogger : public Logger {
public:
    MOCK_METHOD(void, log, (const std::string& message), (override));
    MOCK_METHOD(int, count, (), (const, override));
};

TEST(ServiceTest, LogsOnStartup) {
    MockLogger logger;
    EXPECT_CALL(logger, log(::testing::HasSubstr("started")))
        .Times(1);
    EXPECT_CALL(logger, count())
        .WillOnce(::testing::Return(1));

    Service service(logger);
    service.start();

    EXPECT_EQ(logger.count(), 1);
}
```

**CMake Integration and Sanitizers**:

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.20)
project(my_project LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Fetch GoogleTest
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
FetchContent_MakeAvailable(googletest)

# Library under test
add_library(mylib src/math.cpp src/parser.cpp)
target_include_directories(mylib PUBLIC include/)

# Test executable
add_executable(tests tests/math_test.cpp tests/parser_test.cpp)
target_link_libraries(tests PRIVATE mylib GTest::gtest_main GTest::gmock)

# Register with CTest
include(GoogleTest)
gtest_discover_tests(tests)

# Sanitizer build type (run with: cmake -DCMAKE_BUILD_TYPE=Sanitize ..)
if(CMAKE_BUILD_TYPE STREQUAL "Sanitize")
    target_compile_options(tests PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
    target_link_options(tests PRIVATE -fsanitize=address,undefined)
endif()
```

```bash
# Build and run tests with sanitizers enabled
cmake -B build -DCMAKE_BUILD_TYPE=Sanitize
cmake --build build
ctest --test-dir build --output-on-failure
```

## Best Practices

- **Prefer the Rule of Zero**: let compiler-generated special members handle copying and moving by using smart pointers and standard containers as members
- **Mark move constructors and move assignment noexcept**: standard containers (such as std::vector) only use move operations during reallocation when they are noexcept
- **Use concepts over SFINAE**: concepts produce clearer error messages and are easier to read and maintain
- **Favour make_unique and make_shared**: they are exception-safe and avoid repeating the type name
- **Prefer scoped_lock over manual lock/unlock**: it locks multiple mutexes atomically and unlocks on scope exit
- **Constrain templates early**: use static_assert or concepts at the point of declaration rather than letting errors propagate into instantiation
- **Enable sanitizers in CI**: AddressSanitizer, UndefinedBehaviorSanitizer, and ThreadSanitizer catch bugs that tests alone miss
- **Profile before optimizing**: use perf, VTune, or Tracy to identify bottlenecks rather than guessing

## Common Patterns

### Pattern 1: Type-Erased Polymorphism (std::function / std::any)

```cpp
#include <functional>
#include <vector>

// Callback registry using std::function
class EventBus {
    std::unordered_map<std::string, std::vector<std::function<void()>>> handlers_;

public:
    void on(const std::string& event, std::function<void()> handler) {
        handlers_[event].push_back(std::move(handler));
    }

    void emit(const std::string& event) {
        if (auto it = handlers_.find(event); it != handlers_.end()) {
            for (auto& handler : it->second) {
                handler();
            }
        }
    }
};
```

### Pattern 2: CRTP for Static Polymorphism

```cpp
template <typename Derived>
class Comparable {
public:
    bool operator!=(const Derived& other) const {
        return !(static_cast<const Derived&>(*this) == other);
    }
    bool operator>(const Derived& other) const {
        return other < static_cast<const Derived&>(*this);
    }
    bool operator<=(const Derived& other) const {
        return !(static_cast<const Derived&>(*this) > other);
    }
    bool operator>=(const Derived& other) const {
        return !(static_cast<const Derived&>(*this) < other);
    }
};

class Temperature : public Comparable<Temperature> {
    double celsius_;
public:
    explicit Temperature(double c) : celsius_(c) {}
    bool operator==(const Temperature& other) const { return celsius_ == other.celsius_; }
    bool operator<(const Temperature& other) const  { return celsius_ < other.celsius_; }
};
```

## Quality Checklist

- [ ] No raw new/delete (use smart pointers or containers)
- [ ] Move constructors and move assignment are noexcept
- [ ] Templates are constrained with concepts
- [ ] All resources are RAII-managed
- [ ] Concurrency uses scoped_lock or unique_lock (no manual lock/unlock)
- [ ] Sanitizers (ASan, UBSan, TSan) pass cleanly
- [ ] GoogleTest suite covers edge cases and error paths
- [ ] Benchmarks exist for performance-critical paths

## Related Skills

- `performance-testing` - C++ benchmarking and profiling
- `cicd-architect` - C++ CI/CD with CMake and sanitizers
- `code-quality` - C++ static analysis and code standards
- `kubernetes-expert` - Deploying C++ services in containers

---

**Version**: 1.0.0
**Last Updated**: March 2026
**Based on**: C++ Core Guidelines, Effective Modern C++, awesome-claude-code-subagents patterns


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
