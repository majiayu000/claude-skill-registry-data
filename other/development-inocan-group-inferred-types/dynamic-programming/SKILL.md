---
name: dynamic-programming
description: Master DP patterns with complete implementations for memoization, tabulation, and state design with production-ready solutions.
sasmp_version: "1.3.0"
bonded_agent: 04-dynamic-programming
bond_type: PRIMARY_BOND

# Production-Grade Skill Specifications (2025)
atomic_responsibility: dp_pattern_execution
version: "2.0.0"

parameter_validation:
  strict: true
  rules:
    - name: input_sequence
      type: list
      required: true
    - name: target
      type: integer
      required: false
    - name: memo
      type: dict
      required: false

retry_logic:
  max_attempts: 3
  backoff_ms: [100, 200, 400]
  retryable_errors:
    - recursion_depth
    - memory_exceeded

logging_hooks:
  on_start: true
  on_complete: true
  on_error: true
  log_format: "[DP-SKILL] {timestamp} | {operation} | {status}"

complexity_annotations:
  fibonacci:
    time: "O(n)"
    space: "O(1) optimized"
  knapsack:
    time: "O(n*W)"
    space: "O(W) optimized"
  lcs:
    time: "O(m*n)"
    space: "O(n) optimized"
  coin_change:
    time: "O(n*amount)"
    space: "O(amount)"
---

# Dynamic Programming Skill

**Atomic Responsibility**: Execute DP patterns with optimal time-space complexity.

## DP Framework

```
1. Define state: dp[i] = "what does this represent?"
2. Find recurrence: dp[i] = f(dp[i-1], dp[i-2], ...)
3. Identify base cases: dp[0] = ?, dp[1] = ?
4. Determine order: smaller → larger
5. Optimize space: O(n) → O(1) when possible
```

## Fibonacci Pattern

```python
from typing import List, Dict
from functools import lru_cache

# Memoization (Top-Down)
@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    """
    Fibonacci with memoization.

    Time: O(n), Space: O(n)
    """
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


# Tabulation (Bottom-Up)
def fib_tabulation(n: int) -> int:
    """
    Fibonacci with tabulation.

    Time: O(n), Space: O(n)
    """
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


# Space-Optimized
def fib_optimized(n: int) -> int:
    """
    Fibonacci with O(1) space.

    Time: O(n), Space: O(1)
    """
    if n <= 1:
        return n

    prev2, prev1 = 0, 1

    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr

    return prev1
```

## 0/1 Knapsack Pattern

```python
def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Classic 0/1 Knapsack problem.

    State: dp[i][w] = max value using items 0..i-1 with capacity w

    Time: O(n*W), Space: O(n*W)

    Args:
        weights: Weight of each item
        values: Value of each item
        capacity: Maximum weight capacity

    Returns:
        Maximum achievable value
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i - 1][w]

            # Take item i-1 if possible
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )

    return dp[n][capacity]


def knapsack_optimized(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Space-optimized knapsack using 1D array.

    Time: O(n*W), Space: O(W)

    Key insight: Iterate capacity in reverse to avoid overwriting.
    """
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        # Reverse order to ensure each item used at most once
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]
```

## Longest Common Subsequence (LCS)

```python
def lcs(text1: str, text2: str) -> int:
    """
    Find length of longest common subsequence.

    State: dp[i][j] = LCS of text1[0..i-1] and text2[0..j-1]

    Time: O(m*n), Space: O(m*n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def lcs_optimized(text1: str, text2: str) -> int:
    """
    Space-optimized LCS using two rows.

    Time: O(m*n), Space: O(min(m,n))
    """
    # Ensure text2 is shorter for space optimization
    if len(text1) < len(text2):
        text1, text2 = text2, text1

    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr

    return prev[n]
```

## Coin Change Pattern

```python
def coin_change(coins: List[int], amount: int) -> int:
    """
    Minimum coins to make amount.

    State: dp[i] = minimum coins for amount i
    Recurrence: dp[i] = min(dp[i], dp[i-coin] + 1)

    Time: O(n*amount), Space: O(amount)

    Returns:
        Minimum coins, or -1 if impossible
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins for amount 0

    for coin in coins:
        for i in range(coin, amount + 1):
            if dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def coin_change_ways(coins: List[int], amount: int) -> int:
    """
    Count number of ways to make amount.

    Note: Order of loops matters!
    - Coins outer: combinations (unique ways)
    - Amount outer: permutations (order matters)

    Time: O(n*amount), Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make amount 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

## Longest Increasing Subsequence (LIS)

```python
def lis_dp(nums: List[int]) -> int:
    """
    Find length of LIS using DP.

    State: dp[i] = length of LIS ending at index i

    Time: O(n²), Space: O(n)
    """
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # Each element is LIS of length 1

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def lis_binary_search(nums: List[int]) -> int:
    """
    Find length of LIS using binary search.

    Time: O(n log n), Space: O(n)

    Key insight: Maintain smallest tail of LIS for each length.
    """
    from bisect import bisect_left

    if not nums:
        return 0

    tails = []  # tails[i] = smallest tail of LIS with length i+1

    for num in nums:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    return len(tails)
```

## Unit Test Template

```python
import pytest

class TestDynamicProgramming:
    """Unit tests for DP implementations."""

    def test_fibonacci(self):
        assert fib_optimized(0) == 0
        assert fib_optimized(1) == 1
        assert fib_optimized(10) == 55

    def test_knapsack(self):
        weights = [1, 2, 3]
        values = [10, 15, 40]
        assert knapsack_optimized(weights, values, 6) == 65

    def test_lcs(self):
        assert lcs("abcde", "ace") == 3
        assert lcs("abc", "def") == 0

    def test_coin_change(self):
        assert coin_change([1, 2, 5], 11) == 3
        assert coin_change([2], 3) == -1

    def test_coin_change_ways(self):
        assert coin_change_ways([1, 2, 5], 5) == 4

    def test_lis(self):
        assert lis_binary_search([10, 9, 2, 5, 3, 7, 101, 18]) == 4
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Wrong answer | Incorrect recurrence | Verify with small examples |
| Stack overflow | Deep memoization | Use tabulation instead |
| TLE | Missing memoization | Add @lru_cache or explicit memo |
| MLE | Full 2D table | Apply space optimization |

### Debug Checklist
```
□ State definition clear and complete?
□ Recurrence handles all cases?
□ Base cases cover edge inputs?
□ Computation order respects dependencies?
□ Return value correct (dp[n] vs dp[n-1])?
□ Space optimization maintains correctness?
```
