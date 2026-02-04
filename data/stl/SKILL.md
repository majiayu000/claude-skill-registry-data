---
# ═══════════════════════════════════════════════════════════════════════════════
# SKILL: STL
# Version: 3.0.0 | SASMP v1.3.0 Compliant | Production-Grade
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# IDENTITY
# ─────────────────────────────────────────────────────────────────────────────
name: stl
version: "3.0.0"
description: >
  Production-grade skill for the C++ Standard Template Library. Covers
  containers, algorithms, iterators, and utilities for efficient data
  manipulation.

# ─────────────────────────────────────────────────────────────────────────────
# COMPLIANCE
# ─────────────────────────────────────────────────────────────────────────────
sasmp_version: "1.3.0"
skill_version: "3.0.0"

# ─────────────────────────────────────────────────────────────────────────────
# BONDING
# ─────────────────────────────────────────────────────────────────────────────
bonded_agent: 03-stl-master
bond_type: PRIMARY_BOND
category: learning

# ─────────────────────────────────────────────────────────────────────────────
# PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
parameters:
  topic:
    type: string
    required: true
    enum: [containers, algorithms, iterators, utilities, ranges]
  container_type:
    type: string
    required: false
    enum: [vector, map, set, list, deque, unordered_map]

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
    on_wrong_container: "suggest_better_alternative"
    on_iterator_invalidation: "explain_safe_pattern"
---

# STL Skill

**Production-Grade Learning Skill** | Standard Template Library

Master C++ containers, algorithms, and iterators for efficient programming.

---

## Container Selection Guide

### Decision Flowchart

```
Need to store data?
│
├── Need key-value pairs?
│   ├── Need ordering? → std::map
│   └── Need fast lookup? → std::unordered_map
│
├── Need unique elements only?
│   ├── Need ordering? → std::set
│   └── Need fast lookup? → std::unordered_set
│
└── Need sequence?
    ├── Need random access?
    │   ├── Size changes often? → std::vector (default)
    │   └── Fixed size? → std::array
    ├── Need fast insert at both ends? → std::deque
    └── Need fast insert in middle? → std::list
```

### Complexity Reference

| Container | Access | Search | Insert | Delete |
|-----------|--------|--------|--------|--------|
| `vector` | O(1) | O(n) | O(n)* | O(n) |
| `deque` | O(1) | O(n) | O(1)** | O(1)** |
| `list` | O(n) | O(n) | O(1) | O(1) |
| `set/map` | - | O(log n) | O(log n) | O(log n) |
| `unordered_*` | - | O(1)* | O(1)* | O(1)* |

*amortized **at ends

---

## Containers

### std::vector (Default Choice)

```cpp
#include <vector>

std::vector<int> v;

// Initialization
std::vector<int> v1 = {1, 2, 3, 4, 5};
std::vector<int> v2(10, 0);  // 10 zeros
std::vector<int> v3(v1.begin(), v1.end());  // Copy

// Modification
v.push_back(6);           // Add to end
v.emplace_back(7);        // Construct in place (prefer)
v.pop_back();             // Remove last
v.insert(v.begin(), 0);   // Insert at position
v.erase(v.begin() + 2);   // Remove at position

// Best practices
v.reserve(100);           // Pre-allocate (avoid reallocations)
v.shrink_to_fit();        // Release unused memory
```

### std::map / std::unordered_map

```cpp
#include <map>
#include <unordered_map>

// Ordered map (red-black tree)
std::map<std::string, int> scores;
scores["Alice"] = 95;
scores["Bob"] = 87;

// Unordered map (hash table) - faster lookup
std::unordered_map<std::string, int> cache;
cache["key1"] = 100;

// Safe access
if (auto it = scores.find("Alice"); it != scores.end()) {
    std::cout << it->second << "\n";
}

// C++17 structured bindings
for (const auto& [name, score] : scores) {
    std::cout << name << ": " << score << "\n";
}

// Insert or update (C++17)
scores.insert_or_assign("Charlie", 90);

// Insert if not exists
scores.try_emplace("Dave", 85);
```

---

## Algorithms

### Non-Modifying

```cpp
#include <algorithm>
#include <numeric>

std::vector<int> v = {1, 2, 3, 4, 5};

// Find
auto it = std::find(v.begin(), v.end(), 3);
auto it2 = std::find_if(v.begin(), v.end(), [](int n) { return n > 3; });

// Count
size_t count = std::count_if(v.begin(), v.end(), [](int n) { return n % 2 == 0; });

// All/Any/None
bool allPos = std::all_of(v.begin(), v.end(), [](int n) { return n > 0; });
bool anyNeg = std::any_of(v.begin(), v.end(), [](int n) { return n < 0; });

// Accumulate
int sum = std::accumulate(v.begin(), v.end(), 0);
int product = std::accumulate(v.begin(), v.end(), 1, std::multiplies<>());
```

### Modifying

```cpp
// Transform
std::transform(v.begin(), v.end(), v.begin(), [](int n) { return n * 2; });

// Sort
std::sort(v.begin(), v.end());  // Ascending
std::sort(v.begin(), v.end(), std::greater<>());  // Descending

// Stable sort (preserves relative order of equal elements)
std::stable_sort(v.begin(), v.end());

// Remove (erase-remove idiom)
v.erase(std::remove_if(v.begin(), v.end(), [](int n) { return n < 0; }), v.end());

// C++20: std::erase_if (much cleaner)
std::erase_if(v, [](int n) { return n < 0; });

// Unique (remove consecutive duplicates)
v.erase(std::unique(v.begin(), v.end()), v.end());
```

### Binary Search (Sorted Containers)

```cpp
std::vector<int> sorted = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Check if exists
bool found = std::binary_search(sorted.begin(), sorted.end(), 5);

// Find position
auto lower = std::lower_bound(sorted.begin(), sorted.end(), 5);  // First >= 5
auto upper = std::upper_bound(sorted.begin(), sorted.end(), 5);  // First > 5
auto range = std::equal_range(sorted.begin(), sorted.end(), 5);  // Both
```

---

## C++20 Ranges

```cpp
#include <ranges>
namespace rv = std::views;

std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Lazy pipeline (no intermediate allocations)
auto result = data
    | rv::filter([](int n) { return n % 2 == 0; })  // Keep evens
    | rv::transform([](int n) { return n * n; })   // Square
    | rv::take(3);                                  // First 3

// Materialize when needed
std::vector<int> squares(result.begin(), result.end());
// squares = {4, 16, 36}

// Range algorithms
std::ranges::sort(data);
auto it = std::ranges::find(data, 5);
```

---

## Troubleshooting

### Iterator Invalidation

| Container | Invalidates on |
|-----------|---------------|
| `vector` | Insert/erase (except at end) |
| `deque` | Insert/erase (except at ends) |
| `list` | Never (except erased element) |
| `map/set` | Never (except erased element) |

### Safe Patterns

```cpp
// ❌ BAD: Iterator invalidation
for (auto it = v.begin(); it != v.end(); ++it) {
    if (*it < 0) v.erase(it);  // Invalidates it!
}

// ✅ GOOD: Return new iterator
for (auto it = v.begin(); it != v.end(); ) {
    if (*it < 0) {
        it = v.erase(it);  // erase returns next valid iterator
    } else {
        ++it;
    }
}

// ✅ BETTER: Use algorithm
std::erase_if(v, [](int n) { return n < 0; });
```

---

## Unit Test Template

```cpp
#include <gtest/gtest.h>

TEST(STLTest, VectorOperations) {
    std::vector<int> v = {1, 2, 3};

    v.push_back(4);
    EXPECT_EQ(v.size(), 4);
    EXPECT_EQ(v.back(), 4);

    v.pop_back();
    EXPECT_EQ(v.size(), 3);
}

TEST(STLTest, MapOperations) {
    std::map<std::string, int> m;
    m["a"] = 1;
    m["b"] = 2;

    EXPECT_EQ(m["a"], 1);
    EXPECT_TRUE(m.contains("b"));  // C++20
}

TEST(STLTest, Algorithms) {
    std::vector<int> v = {3, 1, 4, 1, 5, 9};

    std::sort(v.begin(), v.end());
    EXPECT_TRUE(std::is_sorted(v.begin(), v.end()));

    auto it = std::find(v.begin(), v.end(), 5);
    EXPECT_NE(it, v.end());
}
```

---

*C++ Plugin v3.0.0 - Production-Grade Learning Skill*
