---
name: sorting-algorithms
description: Complete sorting algorithm implementations including quick sort, merge sort, and binary search with complexity analysis and production-ready code.
sasmp_version: "1.3.0"
bonded_agent: 05-sorting-searching
bond_type: PRIMARY_BOND

# Production-Grade Skill Specifications (2025)
atomic_responsibility: sorting_algorithm_execution
version: "2.0.0"

parameter_validation:
  strict: true
  rules:
    - name: arr
      type: list
      required: true
    - name: target
      type: any
      required: false

retry_logic:
  max_attempts: 3
  backoff_ms: [100, 200, 400]
  retryable_errors:
    - stack_overflow
    - timeout

logging_hooks:
  on_start: true
  on_complete: true
  on_error: true
  log_format: "[SRT-SKILL] {timestamp} | {operation} | {status}"

complexity_annotations:
  merge_sort:
    time: "O(n log n)"
    space: "O(n)"
  quick_sort:
    time: "O(n log n) avg, O(n²) worst"
    space: "O(log n)"
  binary_search:
    time: "O(log n)"
    space: "O(1)"
---

# Sorting Algorithms Skill

**Atomic Responsibility**: Execute sorting and searching algorithms efficiently.

## Merge Sort - O(n log n) Guaranteed

```python
from typing import List

def merge_sort(arr: List[int]) -> List[int]:
    """
    Stable, divide-and-conquer sorting.

    Time: O(n log n), Space: O(n)
    Use for: Linked lists, when stability needed
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= for stability
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

## Quick Sort - O(n log n) Average

```python
import random

def quick_sort(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    In-place, cache-friendly sorting.

    Time: O(n log n) avg, O(n²) worst
    Space: O(log n) for recursion stack
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)


def partition(arr: List[int], low: int, high: int) -> int:
    # Randomized pivot to avoid O(n²) on sorted input
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]

    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

## Binary Search Templates

```python
def binary_search(arr: List[int], target: int) -> int:
    """
    Find exact match in sorted array.

    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def find_first(arr: List[int], target: int) -> int:
    """Find first (leftmost) occurrence."""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def find_last(arr: List[int], target: int) -> int:
    """Find last (rightmost) occurrence."""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            left = mid + 1  # Keep searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

## Counting Sort - O(n+k)

```python
def counting_sort(arr: List[int], max_val: int) -> List[int]:
    """
    Linear-time sort for limited range integers.

    Time: O(n+k), Space: O(k)
    """
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    result = []
    for i in range(max_val + 1):
        result.extend([i] * count[i])

    return result
```

## Unit Test Template

```python
import pytest

class TestSortingAlgorithms:
    def test_merge_sort(self):
        assert merge_sort([3, 1, 4, 1, 5, 9]) == [1, 1, 3, 4, 5, 9]

    def test_quick_sort(self):
        arr = [3, 1, 4, 1, 5, 9]
        quick_sort(arr)
        assert arr == [1, 1, 3, 4, 5, 9]

    def test_binary_search(self):
        assert binary_search([1, 2, 3, 4, 5], 3) == 2
        assert binary_search([1, 2, 3, 4, 5], 6) == -1

    def test_find_first_last(self):
        arr = [1, 2, 2, 2, 3]
        assert find_first(arr, 2) == 1
        assert find_last(arr, 2) == 3
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Infinite loop | Wrong binary search bounds | Use `left <= right` consistently |
| Stack overflow | Sorted input to quicksort | Use randomized pivot |
| Off-by-one | Wrong mid calculation | Use `mid = left + (right - left) // 2` |

### Debug Checklist
```
□ Array sorted for binary search?
□ Loop termination correct?
□ Handling duplicates properly?
□ Edge cases: empty, single element?
```
