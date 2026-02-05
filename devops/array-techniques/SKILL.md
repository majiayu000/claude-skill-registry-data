---
name: array-techniques
description: Master essential array techniques including two pointers, sliding window, and prefix sums for efficient problem solving with O(n) patterns.
sasmp_version: "1.3.0"
bonded_agent: 01-arrays-lists
bond_type: PRIMARY_BOND

# Production-Grade Skill Specifications (2025)
atomic_responsibility: array_pattern_execution
version: "2.0.0"

parameter_validation:
  strict: true
  rules:
    - name: array_input
      type: list
      required: true
      constraints:
        min_length: 0
        max_length: 100000
    - name: target
      type: integer
      required: false
    - name: window_size
      type: integer
      required: false
      constraints:
        min_value: 1

retry_logic:
  max_attempts: 3
  backoff_ms: [100, 200, 400]
  retryable_errors:
    - timeout
    - memory_exceeded

logging_hooks:
  on_start: true
  on_complete: true
  on_error: true
  log_format: "[ARR-SKILL] {timestamp} | {operation} | {status}"

complexity_annotations:
  two_pointers:
    time: "O(n)"
    space: "O(1)"
  sliding_window:
    time: "O(n)"
    space: "O(1)"
  prefix_sum:
    time: "O(n) build, O(1) query"
    space: "O(n)"
---

# Array Techniques Skill

**Atomic Responsibility**: Execute array manipulation patterns with optimal complexity.

## Two Pointers Pattern

### Same Direction (Fast/Slow)
```python
from typing import List

def remove_element(nums: List[int], val: int) -> int:
    """
    Remove all occurrences of val in-place.

    Time: O(n), Space: O(1)

    Args:
        nums: Input array (modified in-place)
        val: Value to remove

    Returns:
        New length of array

    Raises:
        ValueError: If nums is None
    """
    if nums is None:
        raise ValueError("Input array cannot be None")

    write_ptr = 0
    for read_ptr in range(len(nums)):
        if nums[read_ptr] != val:
            nums[write_ptr] = nums[read_ptr]
            write_ptr += 1
    return write_ptr
```

### Opposite Direction (Converging)
```python
def two_sum_sorted(arr: List[int], target: int) -> List[int]:
    """
    Find two indices in sorted array that sum to target.

    Time: O(n), Space: O(1)

    Args:
        arr: Sorted input array
        target: Target sum

    Returns:
        List of two indices, or empty list if not found
    """
    if not arr or len(arr) < 2:
        return []

    left, right = 0, len(arr) - 1

    while left < right:
        total = arr[left] + arr[right]
        if total == target:
            return [left, right]
        elif total < target:
            left += 1
        else:
            right -= 1

    return []
```

## Sliding Window Pattern

### Fixed Window Size
```python
def max_sum_subarray(nums: List[int], k: int) -> int:
    """
    Find maximum sum of contiguous subarray of size k.

    Time: O(n), Space: O(1)

    Args:
        nums: Input array
        k: Window size

    Returns:
        Maximum sum, or 0 if invalid input

    Raises:
        ValueError: If k > len(nums) or k <= 0
    """
    if not nums or k <= 0:
        raise ValueError("Invalid input: empty array or k <= 0")
    if k > len(nums):
        raise ValueError(f"Window size {k} exceeds array length {len(nums)}")

    window_sum = sum(nums[:k])
    max_sum = window_sum

    for i in range(k, len(nums)):
        window_sum = window_sum - nums[i - k] + nums[i]
        max_sum = max(max_sum, window_sum)

    return max_sum
```

### Variable Window Size
```python
def min_subarray_len(target: int, nums: List[int]) -> int:
    """
    Find minimal length of subarray with sum >= target.

    Time: O(n), Space: O(1)

    Args:
        target: Minimum sum required
        nums: Input array of positive integers

    Returns:
        Minimum length, or 0 if no valid subarray
    """
    if not nums:
        return 0

    left = 0
    current_sum = 0
    min_len = float('inf')

    for right in range(len(nums)):
        current_sum += nums[right]

        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= nums[left]
            left += 1

    return min_len if min_len != float('inf') else 0
```

## Prefix Sum Pattern

```python
class PrefixSum:
    """
    Precompute cumulative sums for O(1) range queries.

    Time: O(n) initialization, O(1) query
    Space: O(n)
    """

    def __init__(self, nums: List[int]):
        if nums is None:
            raise ValueError("Input array cannot be None")

        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)

    def range_sum(self, left: int, right: int) -> int:
        """Get sum of elements from left to right (inclusive)."""
        if left < 0 or right >= len(self.prefix) - 1:
            raise IndexError(f"Indices out of bounds: [{left}, {right}]")
        return self.prefix[right + 1] - self.prefix[left]
```

## Unit Test Template

```python
import pytest

class TestArrayTechniques:
    def test_two_sum_sorted_found(self):
        assert two_sum_sorted([1, 2, 3, 4, 5], 9) == [3, 4]

    def test_two_sum_sorted_not_found(self):
        assert two_sum_sorted([1, 2, 3], 10) == []

    def test_sliding_window_basic(self):
        assert max_sum_subarray([1, 2, 3, 4, 5], 2) == 9

    def test_prefix_sum_range(self):
        ps = PrefixSum([1, 2, 3, 4, 5])
        assert ps.range_sum(1, 3) == 9

    def test_min_subarray_len(self):
        assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Off-by-one error | Wrong index bounds | Use `len(arr) - 1` for last valid index |
| Infinite loop | Window never shrinks | Ensure left pointer advances |
| Wrong sum | Missing edge case | Handle empty array, single element |

### Debug Checklist
```
□ Input validation (None, empty, invalid k)?
□ Pointer bounds checked (left < right)?
□ Window sum updated correctly?
□ Edge cases: single element, all same values?
```
