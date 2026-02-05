---
# ═══════════════════════════════════════════════════════════════════════════════
# SKILL: Algorithms
# Version: 3.0.0 | SASMP v1.3.0 Compliant | Production-Grade
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# IDENTITY
# ─────────────────────────────────────────────────────────────────────────────
name: algorithms
version: "3.0.0"
description: >
  Production-grade skill for algorithm design and data structure implementation
  in C++. Covers complexity analysis, sorting, searching, graphs, dynamic
  programming, and STL algorithm mastery.

# ─────────────────────────────────────────────────────────────────────────────
# COMPLIANCE
# ─────────────────────────────────────────────────────────────────────────────
sasmp_version: "1.3.0"
skill_version: "3.0.0"

# ─────────────────────────────────────────────────────────────────────────────
# BONDING
# ─────────────────────────────────────────────────────────────────────────────
bonded_agent: cpp-algorithms-agent
bond_type: PRIMARY_BOND
category: learning

# ─────────────────────────────────────────────────────────────────────────────
# PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
parameters:
  algorithm_type:
    type: string
    required: false
    enum: [sorting, searching, graph, dynamic_programming, greedy, divide_conquer]
    description: "Category of algorithm to focus on"
  complexity_target:
    type: string
    required: false
    enum: [constant, logarithmic, linear, linearithmic, quadratic, exponential]
    description: "Target time complexity"
  data_structure:
    type: string
    required: false
    enum: [array, vector, list, tree, graph, heap, hash_table]
    description: "Data structure to use"
  explanation_depth:
    type: string
    required: false
    enum: [brief, standard, detailed, visual]
    default: standard
    description: "Level of explanation detail"

# ─────────────────────────────────────────────────────────────────────────────
# ERROR HANDLING
# ─────────────────────────────────────────────────────────────────────────────
error_handling:
  retry_logic:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 500
    max_delay_ms: 8000
    jitter: true
  fallback:
    on_complexity_analysis_fail: "use_empirical_measurement"
    on_implementation_error: "provide_pseudocode_first"
    on_optimization_fail: "explain_tradeoffs"
  validation:
    verify_complexity_claims: true
    test_edge_cases: true
    check_algorithm_correctness: true
---

# Algorithms Skill

**Production-Grade Learning Skill** | Algorithms & Data Structures

Master algorithm design and implementation in C++ with complexity analysis.

---

## Complexity Analysis

### Big O Notation Reference

| Complexity | Name | Example | Operations (n=1000) |
|------------|------|---------|---------------------|
| O(1) | Constant | Array access | 1 |
| O(log n) | Logarithmic | Binary search | 10 |
| O(n) | Linear | Linear search | 1,000 |
| O(n log n) | Linearithmic | Merge sort | 10,000 |
| O(n²) | Quadratic | Bubble sort | 1,000,000 |
| O(2^n) | Exponential | Recursive fib | 10^301 |

### Complexity Analysis Framework

```cpp
// Time Complexity Analysis Template
// 1. Count primitive operations
// 2. Express as function of input size n
// 3. Keep highest order term
// 4. Drop constants

// Example: Find maximum
int findMax(const std::vector<int>& v) {  // O(n)
    int max = v[0];                        // O(1)
    for (int i = 1; i < v.size(); ++i) {   // O(n) iterations
        if (v[i] > max) {                  // O(1)
            max = v[i];                    // O(1)
        }
    }
    return max;                            // O(1)
}  // Total: O(1) + O(n) * O(1) = O(n)
```

---

## Sorting Algorithms

### STL Sorting

```cpp
#include <algorithm>
#include <vector>

std::vector<int> v = {5, 2, 8, 1, 9};

// Introsort - O(n log n) guaranteed
std::sort(v.begin(), v.end());

// Stable sort - preserves relative order of equal elements
std::stable_sort(v.begin(), v.end());

// Partial sort - only first k elements sorted
std::partial_sort(v.begin(), v.begin() + 3, v.end());

// Nth element - partition around nth element (O(n) average)
std::nth_element(v.begin(), v.begin() + v.size()/2, v.end());

// Custom comparator (descending order)
std::sort(v.begin(), v.end(), std::greater<int>());

// Sort by projection (C++20)
std::ranges::sort(v, {}, [](int x) { return std::abs(x); });
```

### Sorting Algorithm Comparison

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Tim Sort | O(n) | O(n log n) | O(n log n) | O(n) | Yes |

---

## Searching Algorithms

### Binary Search

```cpp
#include <algorithm>

// STL binary search - O(log n), requires sorted range
std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9};

// Check existence
bool found = std::binary_search(v.begin(), v.end(), 5);

// Find position
auto it = std::lower_bound(v.begin(), v.end(), 5);  // First >= 5
auto it2 = std::upper_bound(v.begin(), v.end(), 5); // First > 5

// Range of equal elements
auto [lo, hi] = std::equal_range(v.begin(), v.end(), 5);

// Custom binary search with predicate
template<typename T, typename Pred>
T binary_search_first_true(T lo, T hi, Pred pred) {
    while (lo < hi) {
        T mid = lo + (hi - lo) / 2;
        if (pred(mid)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}
```

---

## Graph Algorithms

### Graph Representations

```cpp
// Adjacency List (preferred for sparse graphs)
std::vector<std::vector<int>> adj(n);
adj[0].push_back(1);  // Edge 0 -> 1

// Adjacency List with weights
std::vector<std::vector<std::pair<int, int>>> adj(n);
adj[0].push_back({1, weight});  // Edge 0 -> 1 with weight

// Adjacency Matrix (for dense graphs)
std::vector<std::vector<int>> adj(n, std::vector<int>(n, 0));
adj[0][1] = 1;  // Edge 0 -> 1
```

### BFS - Breadth First Search

```cpp
std::vector<int> bfs(int start, const std::vector<std::vector<int>>& adj) {
    std::vector<int> dist(adj.size(), -1);
    std::queue<int> q;

    dist[start] = 0;
    q.push(start);

    while (!q.empty()) {
        int node = q.front();
        q.pop();

        for (int neighbor : adj[node]) {
            if (dist[neighbor] == -1) {
                dist[neighbor] = dist[node] + 1;
                q.push(neighbor);
            }
        }
    }
    return dist;  // Shortest distances from start
}
```

### DFS - Depth First Search

```cpp
void dfs(int node, const std::vector<std::vector<int>>& adj,
         std::vector<bool>& visited, std::vector<int>& result) {
    visited[node] = true;
    result.push_back(node);

    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            dfs(neighbor, adj, visited, result);
        }
    }
}
```

### Dijkstra's Algorithm

```cpp
std::vector<int> dijkstra(int start,
    const std::vector<std::vector<std::pair<int,int>>>& adj) {

    std::vector<int> dist(adj.size(), INT_MAX);
    std::priority_queue<std::pair<int,int>,
        std::vector<std::pair<int,int>>,
        std::greater<>> pq;

    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();

        if (d > dist[u]) continue;  // Skip outdated entries

        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

---

## Dynamic Programming

### DP Framework

```cpp
// 1. Define state: What subproblem does dp[i] represent?
// 2. Define transition: How to compute dp[i] from previous states?
// 3. Define base case: What are the initial values?
// 4. Define answer: Which state(s) give the final answer?

// Example: Longest Increasing Subsequence
int lis(const std::vector<int>& nums) {
    int n = nums.size();
    std::vector<int> dp(n, 1);  // dp[i] = LIS ending at i

    for (int i = 1; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            if (nums[j] < nums[i]) {
                dp[i] = std::max(dp[i], dp[j] + 1);
            }
        }
    }
    return *std::max_element(dp.begin(), dp.end());
}

// Optimized LIS with binary search - O(n log n)
int lisOptimized(const std::vector<int>& nums) {
    std::vector<int> tails;
    for (int x : nums) {
        auto it = std::lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) {
            tails.push_back(x);
        } else {
            *it = x;
        }
    }
    return tails.size();
}
```

### Common DP Patterns

| Pattern | Example | State | Complexity |
|---------|---------|-------|------------|
| Linear | Fibonacci | dp[i] | O(n) |
| 2D Grid | Path count | dp[i][j] | O(n×m) |
| Interval | Matrix chain | dp[i][j] | O(n³) |
| Subset | Knapsack | dp[mask] | O(2^n) |
| Tree | Tree DP | dp[node] | O(n) |

---

## Algorithm Selection Flowchart

```
What type of problem?
├── Searching
│   ├── Sorted data? → Binary Search O(log n)
│   └── Unsorted? → Linear Search O(n) or Hash O(1)
├── Sorting
│   ├── Need stable? → std::stable_sort
│   ├── Partial sort? → std::partial_sort
│   └── General? → std::sort
├── Optimization
│   ├── Overlapping subproblems? → Dynamic Programming
│   └── Greedy choice property? → Greedy Algorithm
├── Graph
│   ├── Shortest path (unweighted)? → BFS
│   ├── Shortest path (weighted)? → Dijkstra/Bellman-Ford
│   ├── All pairs shortest? → Floyd-Warshall
│   └── Minimum spanning tree? → Kruskal/Prim
└── String
    ├── Pattern matching? → KMP/Rabin-Karp
    └── Longest common? → DP
```

---

## Troubleshooting Decision Tree

```
Algorithm not working correctly?
├── Wrong output
│   ├── Check base cases
│   ├── Verify loop bounds
│   ├── Test edge cases (empty, single element)
│   └── Print intermediate values
├── Time Limit Exceeded (TLE)
│   ├── Check complexity matches constraint
│   ├── Look for unnecessary recomputation
│   ├── Consider memoization/DP
│   └── Use better data structure
├── Memory Limit Exceeded (MLE)
│   ├── Reduce DP state dimensions
│   ├── Use rolling array technique
│   └── Clear visited sets between runs
└── Runtime Error
    ├── Check array bounds
    ├── Check integer overflow
    └── Check stack overflow (recursion depth)
```

---

## Unit Test Template

```cpp
#include <gtest/gtest.h>
#include "algorithms.hpp"

class AlgorithmTest : public ::testing::Test {
protected:
    void SetUp() override {
        sorted_vec = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        unsorted_vec = {5, 2, 8, 1, 9, 3, 7, 4, 6, 10};
    }

    std::vector<int> sorted_vec;
    std::vector<int> unsorted_vec;
};

TEST_F(AlgorithmTest, BinarySearchFindsElement) {
    EXPECT_TRUE(std::binary_search(sorted_vec.begin(), sorted_vec.end(), 5));
    EXPECT_FALSE(std::binary_search(sorted_vec.begin(), sorted_vec.end(), 11));
}

TEST_F(AlgorithmTest, SortProducesOrderedOutput) {
    std::sort(unsorted_vec.begin(), unsorted_vec.end());
    EXPECT_TRUE(std::is_sorted(unsorted_vec.begin(), unsorted_vec.end()));
}

TEST_F(AlgorithmTest, BFSFindsShortestPath) {
    std::vector<std::vector<int>> adj = {{1, 2}, {0, 3}, {0, 3}, {1, 2}};
    auto dist = bfs(0, adj);
    EXPECT_EQ(dist[0], 0);
    EXPECT_EQ(dist[1], 1);
    EXPECT_EQ(dist[3], 2);
}

TEST_F(AlgorithmTest, LISHandlesEdgeCases) {
    EXPECT_EQ(lis({}), 0);
    EXPECT_EQ(lis({1}), 1);
    EXPECT_EQ(lis({3, 2, 1}), 1);  // Decreasing
    EXPECT_EQ(lis({1, 2, 3}), 3);  // Increasing
}
```

---

## Integration Points

| Component | Interface |
|-----------|-----------|
| `stl-master` | Container selection |
| `performance-optimizer` | Algorithm optimization |
| `modern-cpp-expert` | Ranges and concepts |
| `cpp-fundamentals-agent` | Basic concepts |

---

*C++ Plugin v3.0.0 - Production-Grade Learning Skill*
