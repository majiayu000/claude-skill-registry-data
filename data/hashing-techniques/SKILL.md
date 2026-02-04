---
name: hashing-techniques
description: Hash-based data structures and techniques including frequency counting, duplicate detection, and LRU cache implementation.
sasmp_version: "1.3.0"
bonded_agent: 06-hash-tables
bond_type: PRIMARY_BOND

# Production-Grade Skill Specifications (2025)
atomic_responsibility: hash_based_operations
version: "2.0.0"

parameter_validation:
  strict: true
  rules:
    - name: input_data
      type: any
      required: true
    - name: capacity
      type: integer
      required: false

retry_logic:
  max_attempts: 3
  backoff_ms: [100, 200, 400]
  retryable_errors:
    - memory_exceeded
    - key_error

logging_hooks:
  on_start: true
  on_complete: true
  on_error: true
  log_format: "[HSH-SKILL] {timestamp} | {operation} | {status}"

complexity_annotations:
  frequency_count:
    time: "O(n)"
    space: "O(k) unique elements"
  lru_cache:
    time: "O(1) all operations"
    space: "O(capacity)"
  group_anagrams:
    time: "O(n * k log k)"
    space: "O(n * k)"
---

# Hashing Techniques Skill

**Atomic Responsibility**: Execute hash-based lookups and data organization.

## Frequency Counting Pattern

```python
from typing import List
from collections import Counter
import heapq

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Find k most frequent elements.

    Time: O(n log k), Space: O(n)
    """
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)


def top_k_frequent_bucket(nums: List[int], k: int) -> List[int]:
    """
    Bucket sort approach for O(n) time.

    Time: O(n), Space: O(n)
    """
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]

    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result

    return result
```

## Duplicate Detection

```python
def contains_duplicate(nums: List[int]) -> bool:
    """O(n) time, O(n) space using set."""
    return len(nums) != len(set(nums))


def find_duplicates(nums: List[int]) -> List[int]:
    """Find all duplicate elements."""
    seen = set()
    duplicates = []

    for num in nums:
        if num in seen:
            duplicates.append(num)
        else:
            seen.add(num)

    return duplicates


def find_duplicates_inplace(nums: List[int]) -> List[int]:
    """
    Find duplicates with O(1) space using index marking.
    Requires: values in range [1, n]
    """
    result = []

    for num in nums:
        index = abs(num) - 1
        if nums[index] < 0:
            result.append(abs(num))
        else:
            nums[index] = -nums[index]

    return result
```

## LRU Cache Implementation

```python
from collections import OrderedDict

class LRUCache:
    """
    Least Recently Used cache with O(1) operations.

    Time: O(1) for get and put
    Space: O(capacity)
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        """Get value and mark as recently used."""
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """Add/update value and maintain capacity."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

## Group Anagrams

```python
from collections import defaultdict

def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Group strings that are anagrams of each other.

    Time: O(n * k log k) where k = max string length
    Space: O(n * k)
    """
    groups = defaultdict(list)

    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)

    return list(groups.values())


def group_anagrams_count(strs: List[str]) -> List[List[str]]:
    """
    Alternative using character count as key.

    Time: O(n * k), Space: O(n * k)
    """
    groups = defaultdict(list)

    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)
        groups[key].append(s)

    return list(groups.values())
```

## Unit Test Template

```python
import pytest

class TestHashingTechniques:
    def test_top_k_frequent(self):
        assert set(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == {1, 2}

    def test_contains_duplicate(self):
        assert contains_duplicate([1, 2, 3, 1]) == True
        assert contains_duplicate([1, 2, 3]) == False

    def test_lru_cache(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)
        assert cache.get(2) == -1

    def test_group_anagrams(self):
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        assert len(result) == 3
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| KeyError | Missing key access | Use `.get()` with default |
| TypeError | Unhashable type | Convert list to tuple |
| Memory exceeded | Storing full objects | Store indices only |

### Debug Checklist
```
□ Key type is hashable?
□ Using get() with default?
□ Handling empty input?
□ Memory efficient storage?
```
