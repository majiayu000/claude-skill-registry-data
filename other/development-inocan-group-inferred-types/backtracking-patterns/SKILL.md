---
name: backtracking-patterns
description: Master backtracking technique with permutations, combinations, and puzzle solving patterns with production-ready implementations.
sasmp_version: "1.3.0"
bonded_agent: 07-greedy-advanced
bond_type: PRIMARY_BOND

# Production-Grade Skill Specifications (2025)
atomic_responsibility: backtracking_execution
version: "2.0.0"

parameter_validation:
  strict: true
  rules:
    - name: candidates
      type: list
      required: true
    - name: n
      type: integer
      required: false
    - name: k
      type: integer
      required: false

retry_logic:
  max_attempts: 3
  backoff_ms: [100, 200, 400]
  retryable_errors:
    - recursion_depth
    - timeout

logging_hooks:
  on_start: true
  on_complete: true
  on_error: true
  log_format: "[BKT-SKILL] {timestamp} | {operation} | {status}"

complexity_annotations:
  permutations:
    time: "O(n!)"
    space: "O(n)"
  combinations:
    time: "O(C(n,k))"
    space: "O(k)"
  n_queens:
    time: "O(n!)"
    space: "O(n)"
  subsets:
    time: "O(2^n)"
    space: "O(n)"
---

# Backtracking Patterns Skill

**Atomic Responsibility**: Execute exhaustive search with intelligent pruning.

## General Template

```python
from typing import List, Any

def backtrack(
    candidates: List[Any],
    path: List[Any],
    result: List[List[Any]],
    start: int = 0
) -> None:
    """
    General backtracking template.

    Pattern: Choose → Explore → Unchoose
    """
    if is_solution(path):
        result.append(path[:])  # Copy path!
        return

    for i in range(start, len(candidates)):
        if not is_valid(candidates[i], path):
            continue

        # Choose
        path.append(candidates[i])

        # Explore
        backtrack(candidates, path, result, i + 1)

        # Unchoose (backtrack)
        path.pop()
```

## Permutations

```python
def permute(nums: List[int]) -> List[List[int]]:
    """
    Generate all permutations.

    Time: O(n!), Space: O(n)
    """
    result = []

    def backtrack(path: List[int], remaining: set):
        if not remaining:
            result.append(path[:])
            return

        for num in list(remaining):
            path.append(num)
            remaining.remove(num)

            backtrack(path, remaining)

            path.pop()
            remaining.add(num)

    backtrack([], set(nums))
    return result


def permute_swap(nums: List[int]) -> List[List[int]]:
    """
    Permutations using in-place swapping.

    Time: O(n!), Space: O(n) for recursion
    """
    result = []

    def backtrack(start: int):
        if start == len(nums):
            result.append(nums[:])
            return

        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]

    backtrack(0)
    return result
```

## Combinations

```python
def combine(n: int, k: int) -> List[List[int]]:
    """
    Generate all k-combinations of 1..n.

    Time: O(C(n,k)), Space: O(k)
    """
    result = []

    def backtrack(start: int, path: List[int]):
        if len(path) == k:
            result.append(path[:])
            return

        # Pruning: need at least (k - len(path)) more elements
        for i in range(start, n - (k - len(path)) + 2):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result
```

## Subsets

```python
def subsets(nums: List[int]) -> List[List[int]]:
    """
    Generate all subsets (power set).

    Time: O(2^n), Space: O(n)
    """
    result = []

    def backtrack(start: int, path: List[int]):
        result.append(path[:])

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def subsets_bitmask(nums: List[int]) -> List[List[int]]:
    """
    Subsets using bit manipulation.

    Time: O(2^n * n), Space: O(n)
    """
    result = []
    n = len(nums)

    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)

    return result
```

## N-Queens

```python
def solve_n_queens(n: int) -> List[List[str]]:
    """
    Solve N-Queens puzzle.

    Time: O(n!), Space: O(n²)
    """
    result = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row: int, queens: List[int]):
        if row == n:
            board = []
            for q in queens:
                board.append('.' * q + 'Q' + '.' * (n - q - 1))
            result.append(board)
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            queens.append(col)

            backtrack(row + 1, queens)

            queens.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0, [])
    return result
```

## Unit Test Template

```python
import pytest

class TestBacktracking:
    def test_permutations(self):
        result = permute([1, 2, 3])
        assert len(result) == 6
        assert [1, 2, 3] in result

    def test_combinations(self):
        result = combine(4, 2)
        assert len(result) == 6
        assert [1, 2] in result

    def test_subsets(self):
        result = subsets([1, 2, 3])
        assert len(result) == 8
        assert [] in result

    def test_n_queens(self):
        result = solve_n_queens(4)
        assert len(result) == 2
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing solutions | Wrong termination | Check base case condition |
| Duplicate solutions | Not skipping duplicates | Sort and skip equal neighbors |
| TLE | No pruning | Add constraint checks early |
| Wrong result | Not copying path | Use `path[:]` when appending |

### Debug Checklist
```
□ Path copied when adding to result?
□ State restored after backtrack?
□ Pruning conditions correct?
□ All branches explored?
```
