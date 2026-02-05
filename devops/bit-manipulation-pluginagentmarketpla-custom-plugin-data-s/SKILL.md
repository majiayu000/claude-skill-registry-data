---
name: bit-manipulation
description: Bit manipulation tricks and techniques for solving problems efficiently using binary operations and XOR properties.
sasmp_version: "1.3.0"
bonded_agent: 07-greedy-advanced
bond_type: PRIMARY_BOND

# Production-Grade Skill Specifications (2025)
atomic_responsibility: bit_operation_execution
version: "2.0.0"

parameter_validation:
  strict: true
  rules:
    - name: num
      type: integer
      required: true
    - name: bit_index
      type: integer
      required: false

retry_logic:
  max_attempts: 3
  backoff_ms: [100, 200, 400]
  retryable_errors:
    - overflow
    - timeout

logging_hooks:
  on_start: true
  on_complete: true
  on_error: true
  log_format: "[BIT-SKILL] {timestamp} | {operation} | {status}"

complexity_annotations:
  basic_ops:
    time: "O(1)"
    space: "O(1)"
  count_bits:
    time: "O(log n) or O(set bits)"
    space: "O(1)"
  subset_generation:
    time: "O(2^n)"
    space: "O(1) per subset"
---

# Bit Manipulation Skill

**Atomic Responsibility**: Execute bit-level operations for efficient problem solving.

## Essential Bit Operations

```python
def set_bit(num: int, i: int) -> int:
    """Set i-th bit to 1. Time: O(1)"""
    return num | (1 << i)


def clear_bit(num: int, i: int) -> int:
    """Clear i-th bit to 0. Time: O(1)"""
    return num & ~(1 << i)


def toggle_bit(num: int, i: int) -> int:
    """Toggle i-th bit. Time: O(1)"""
    return num ^ (1 << i)


def is_bit_set(num: int, i: int) -> bool:
    """Check if i-th bit is set. Time: O(1)"""
    return (num & (1 << i)) != 0


def is_power_of_two(n: int) -> bool:
    """Check if n is power of 2. Time: O(1)"""
    return n > 0 and (n & (n - 1)) == 0


def get_rightmost_set_bit(num: int) -> int:
    """Isolate rightmost set bit. Time: O(1)"""
    return num & (-num)


def clear_rightmost_set_bit(num: int) -> int:
    """Clear rightmost set bit. Time: O(1)"""
    return num & (num - 1)
```

## Counting Set Bits

```python
def count_bits_naive(n: int) -> int:
    """
    Count set bits by shifting.

    Time: O(log n), Space: O(1)
    """
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def count_bits_kernighan(n: int) -> int:
    """
    Brian Kernighan's algorithm.

    Time: O(set bits), Space: O(1)
    Faster when few bits are set.
    """
    count = 0
    while n:
        n &= n - 1  # Clear rightmost set bit
        count += 1
    return count


def count_bits_builtin(n: int) -> int:
    """Use Python built-in."""
    return bin(n).count('1')
```

## Single Number Problems (XOR)

```python
from typing import List

def single_number(nums: List[int]) -> int:
    """
    Find element appearing once (others appear twice).

    Key insight: a ^ a = 0, a ^ 0 = a

    Time: O(n), Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_two(nums: List[int]) -> int:
    """
    Find element appearing once (others appear 3 times).

    Count bits mod 3 for each position.

    Time: O(32n) = O(n), Space: O(1)
    """
    result = 0
    for i in range(32):
        bit_sum = sum((num >> i) & 1 for num in nums)
        if bit_sum % 3:
            result |= (1 << i)
    # Handle negative numbers in Python
    if result >= (1 << 31):
        result -= (1 << 32)
    return result


def single_number_three(nums: List[int]) -> List[int]:
    """
    Find two elements appearing once (others appear twice).

    Time: O(n), Space: O(1)
    """
    xor_all = 0
    for num in nums:
        xor_all ^= num

    # Get rightmost set bit (differs between the two singles)
    diff_bit = xor_all & (-xor_all)

    a = b = 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]
```

## Hamming Distance

```python
def hamming_distance(x: int, y: int) -> int:
    """
    Count differing bit positions.

    Time: O(log n), Space: O(1)
    """
    xor = x ^ y
    count = 0
    while xor:
        xor &= xor - 1
        count += 1
    return count


def hamming_weight(n: int) -> int:
    """Count number of 1 bits (population count)."""
    return count_bits_kernighan(n)
```

## Subset Generation

```python
def generate_subsets_bitmask(nums: List[int]) -> List[List[int]]:
    """
    Generate all subsets using bitmask enumeration.

    Each integer 0 to 2^n-1 represents a subset.

    Time: O(2^n * n), Space: O(1) per subset
    """
    result = []
    n = len(nums)

    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)

    return result


def iterate_subsets_of_mask(mask: int):
    """
    Iterate all submasks of a bitmask.

    Useful for bitmask DP.
    Time: O(3^popcount(mask))
    """
    submask = mask
    while submask > 0:
        yield submask
        submask = (submask - 1) & mask
    yield 0  # Empty subset
```

## Common Bit Tricks

```python
# Swap without temp variable
def swap(a: int, b: int) -> tuple:
    a ^= b
    b ^= a
    a ^= b
    return a, b

# Check if opposite signs
def opposite_signs(x: int, y: int) -> bool:
    return (x ^ y) < 0

# Get absolute value (for 32-bit)
def abs_bit(n: int) -> int:
    mask = n >> 31
    return (n + mask) ^ mask

# Multiply by 2^k
def multiply_power_of_2(n: int, k: int) -> int:
    return n << k

# Divide by 2^k
def divide_power_of_2(n: int, k: int) -> int:
    return n >> k
```

## Unit Test Template

```python
import pytest

class TestBitManipulation:
    def test_basic_ops(self):
        assert set_bit(0b0000, 2) == 0b0100
        assert clear_bit(0b0111, 1) == 0b0101
        assert toggle_bit(0b1010, 3) == 0b0010

    def test_power_of_two(self):
        assert is_power_of_two(8) == True
        assert is_power_of_two(6) == False

    def test_count_bits(self):
        assert count_bits_kernighan(7) == 3
        assert count_bits_kernighan(0) == 0

    def test_single_number(self):
        assert single_number([2, 2, 1]) == 1
        assert set(single_number_three([1, 2, 1, 3, 2, 5])) == {3, 5}

    def test_hamming_distance(self):
        assert hamming_distance(1, 4) == 2
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Negative result | Signed integer handling | Use mask or explicit conversion |
| Overflow | Exceeding bit width | Use Python's arbitrary precision |
| Wrong shift | Confusion with operator | `<<` is left (multiply), `>>` is right (divide) |

### Debug Checklist
```
□ Bit indices 0-indexed?
□ Handling negative numbers?
□ Operator precedence correct? (& before ==)
□ Using parentheses around bit ops?
```

### Bit Operation Quick Reference
```
x & (x-1)   → Clear rightmost set bit
x & -x      → Isolate rightmost set bit
x | (1<<i)  → Set i-th bit
x & ~(1<<i) → Clear i-th bit
x ^ (1<<i)  → Toggle i-th bit
x & 1       → Check if odd
```
