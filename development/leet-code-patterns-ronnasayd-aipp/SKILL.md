---
name: leet-code-patterns
description: >
  Expert guidance on solving LeetCode and coding interview problems using the 15 most important algorithmic patterns.
  Use this skill whenever the user asks about: solving a LeetCode problem, coding interview prep, algorithm patterns,
  data structure problems, competitive programming, identifying the right approach for a problem, or asks "how do I solve X type of problem".
  Also trigger when user describes a problem and wants to know which technique or pattern to apply. Trigger even
  for vague requests like "help me get better at LeetCode" or "I'm stuck on this array problem".
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# LeetCode Patterns Skill

You are an expert competitive programmer and coding interview coach. Your job is to help users:

1. **Identify** which pattern(s) apply to a given problem
2. **Explain** the pattern clearly with intuition, not just mechanics
3. **Guide** them through the solution step by step
4. **Suggest** practice problems to reinforce the pattern

---

## Pattern Recognition Guide

When the user describes a problem, scan for these signals to pick the right pattern:

| Signal in Problem                     | Likely Pattern               |
| ------------------------------------- | ---------------------------- |
| Sum of subarray / range queries       | Prefix Sum                   |
| Sorted array, find pairs              | Two Pointers                 |
| Contiguous subarray/substring         | Sliding Window               |
| Linked list cycle / middle node       | Fast & Slow Pointers         |
| Reverse part of linked list           | LinkedList In-place Reversal |
| Next greater/smaller element          | Monotonic Stack              |
| Top K largest/smallest/frequent       | Top K Elements (heap)        |
| Merge/insert/count intervals          | Overlapping Intervals        |
| Rotated sorted array, sorted search   | Modified Binary Search       |
| Tree visit order matters              | Binary Tree Traversal        |
| All paths, connected components       | DFS                          |
| Shortest path, level-by-level         | BFS                          |
| 2D grid traversal                     | Matrix Traversal             |
| All combinations/permutations/subsets | Backtracking                 |
| Overlapping subproblems, optimization | Dynamic Programming          |

---

## The 15 Patterns

### 1. Prefix Sum

**When to use:** Multiple sum queries on subarrays; cumulative totals.

**Core idea:** Preprocess array into prefix sums so range sum `[i,j] = P[j] - P[i-1]` in O(1).

**Template:**

```python
P = [0] * (len(nums) + 1)
for i, v in enumerate(nums):
    P[i+1] = P[i] + v
# sum from i to j (0-indexed):
range_sum = P[j+1] - P[i]
```

**Practice:** #303 Range Sum Query, #525 Contiguous Array, #560 Subarray Sum Equals K

---

### 2. Two Pointers

**When to use:** Sorted array; find pairs/triplets meeting a condition; avoid O(n²).

**Core idea:** Left pointer at start, right pointer at end. Move based on comparison to target.

**Template:**

```python
left, right = 0, len(nums) - 1
while left < right:
    curr = nums[left] + nums[right]
    if curr == target: return [left, right]
    elif curr < target: left += 1
    else: right -= 1
```

**Practice:** #167 Two Sum II, #15 3Sum, #11 Container With Most Water

---

### 3. Sliding Window

**When to use:** Contiguous subarray/substring with a constraint (max sum, unique chars, etc.).

**Core idea:** Expand right pointer; shrink left when constraint violated; track best.

**Template (variable window):**

```python
left = 0
window = {}
result = 0
for right in range(len(s)):
    # add s[right] to window
    while window_invalid():
        # remove s[left] from window
        left += 1
    result = max(result, right - left + 1)
```

**Practice:** #643 Maximum Average Subarray I, #3 Longest Substring Without Repeating Characters, #76 Minimum Window Substring

---

### 4. Fast & Slow Pointers (Tortoise & Hare)

**When to use:** Detect cycles; find middle of linked list; find entry of cycle.

**Core idea:** Fast moves 2 steps, slow moves 1. They meet iff there's a cycle.

**Template:**

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True  # cycle detected
return False
```

**Practice:** #141 Linked List Cycle, #202 Happy Number, #287 Find the Duplicate Number

---

### 5. LinkedList In-place Reversal

**When to use:** Reverse entire list or a sublist without extra space.

**Core idea:** Rewire `next` pointers as you walk through; use `prev`, `curr`, `next_node`.

**Template:**

```python
prev = None
curr = head
while curr:
    next_node = curr.next
    curr.next = prev
    prev = curr
    curr = next_node
return prev  # new head
```

**Practice:** #206 Reverse Linked List, #92 Reverse Linked List II, #24 Swap Nodes in Pairs

---

### 6. Monotonic Stack

**When to use:** Next greater/smaller element; span problems; histogram problems.

**Core idea:** Maintain a stack that stays strictly increasing or decreasing. Pop when current element breaks the order — that means a "next greater" event.

**Template (next greater):**

```python
stack = []  # stores indices
result = [-1] * len(nums)
for i, v in enumerate(nums):
    while stack and nums[stack[-1]] < v:
        result[stack.pop()] = v
    stack.append(i)
```

**Practice:** #496 Next Greater Element I, #739 Daily Temperatures, #84 Largest Rectangle in Histogram

---

### 7. Top K Elements

**When to use:** Find k-th largest/smallest; top k frequent; k closest.

**Core idea:** Use a min-heap of size k. Pop the smallest whenever heap exceeds k. Root = k-th largest.

**Template:**

```python
import heapq
heap = []
for num in nums:
    heapq.heappush(heap, num)
    if len(heap) > k:
        heapq.heappop(heap)
return heap[0]  # k-th largest
```

**Practice:** #215 Kth Largest Element, #347 Top K Frequent Elements, #373 Find K Pairs with Smallest Sums

---

### 8. Overlapping Intervals

**When to use:** Merge intervals; insert interval; find gaps; count overlaps.

**Core idea:** Sort by start time. Two intervals `[a,b]` and `[c,d]` overlap if `b >= c`. Merge by extending end to `max(b, d)`.

**Template (merge):**

```python
intervals.sort(key=lambda x: x[0])
merged = [intervals[0]]
for start, end in intervals[1:]:
    if start <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], end)
    else:
        merged.append([start, end])
```

**Practice:** #56 Merge Intervals, #57 Insert Interval, #435 Non-Overlapping Intervals

---

### 9. Modified Binary Search

**When to use:** Sorted, rotated, or monotonic array; find target or boundary condition.

**Core idea:** Classic binary search + extra check. Determine which half is sorted, then check if target falls in that range.

**Template (rotated array):**

```python
left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target: return mid
    if nums[left] <= nums[mid]:  # left half sorted
        if nums[left] <= target < nums[mid]: right = mid - 1
        else: left = mid + 1
    else:  # right half sorted
        if nums[mid] < target <= nums[right]: left = mid + 1
        else: right = mid - 1
return -1
```

**Practice:** #33 Search in Rotated Sorted Array, #153 Find Minimum in Rotated Sorted Array, #240 Search a 2D Matrix II

---

### 10. Binary Tree Traversal

**When to use:** Process nodes in a specific order; serialize/deserialize tree; BST operations.

**Orders:**

- **PreOrder** (root → left → right): copy tree, serialize
- **InOrder** (left → root → right): sorted order in BST
- **PostOrder** (left → right → root): delete tree, evaluate expression

**Template (iterative inorder):**

```python
stack, result = [], []
curr = root
while curr or stack:
    while curr:
        stack.append(curr)
        curr = curr.left
    curr = stack.pop()
    result.append(curr.val)
    curr = curr.right
```

**Practice:** #257 Binary Tree Paths (pre), #230 Kth Smallest in BST (in), #124 Binary Tree Max Path Sum (post)

---

### 11. Depth-First Search (DFS)

**When to use:** Explore all paths; connected components; topological sort; tree problems.

**Core idea:** Go deep into one branch before backtracking. Use recursion or explicit stack.

**Template (graph):**

```python
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
```

**Practice:** #133 Clone Graph, #113 Path Sum II, #210 Course Schedule II

---

### 12. Breadth-First Search (BFS)

**When to use:** Shortest path in unweighted graph; level-order traversal; minimum steps.

**Core idea:** Process level by level using a queue. Guarantees shortest path.

**Template:**

```python
from collections import deque
queue = deque([start])
visited = {start}
steps = 0
while queue:
    for _ in range(len(queue)):
        node = queue.popleft()
        if node == target: return steps
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    steps += 1
```

**Practice:** #102 Binary Tree Level Order Traversal, #994 Rotting Oranges, #127 Word Ladder

---

### 13. Matrix Traversal

**When to use:** 2D grid problems; flood fill; island counting; shortest path in grid.

**Core idea:** Treat grid as graph. Use DFS or BFS with 4-directional (or 8-directional) movement. Mark visited cells.

**Template:**

```python
rows, cols = len(grid), len(grid[0])
directions = [(0,1),(0,-1),(1,0),(-1,0)]

def dfs(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols: return
    if grid[r][c] == '0': return
    grid[r][c] = '0'  # mark visited
    for dr, dc in directions:
        dfs(r + dr, c + dc)
```

**Practice:** #733 Flood Fill, #200 Number of Islands, #130 Surrounded Regions

---

### 14. Backtracking

**When to use:** All permutations/combinations/subsets; constraint satisfaction (N-Queens, Sudoku).

**Core idea:** Build solution incrementally. At each step, try all valid choices. Undo (backtrack) when stuck.

**Template:**

```python
def backtrack(start, path):
    result.append(path[:])  # or check completion
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1, path)
        path.pop()  # undo choice

result = []
backtrack(0, [])
```

**Practice:** #46 Permutations, #78 Subsets, #51 N-Queens

---

### 15. Dynamic Programming

**When to use:** Optimization problems; overlapping subproblems; count ways; yes/no feasibility.

**Sub-patterns to recognize:**

- **Fibonacci-style:** `dp[i] = dp[i-1] + dp[i-2]` → #70 Climbing Stairs
- **0/1 Knapsack:** include or exclude item → #416 Partition Equal Subset Sum
- **LCS:** two sequences, 2D DP table → #1143 Longest Common Subsequence
- **LIS:** increasing subsequence → #300 Longest Increasing Subsequence
- **Unbounded Knapsack:** item can be reused → #322 Coin Change

**Template (bottom-up):**

```python
dp = [0] * (n + 1)
dp[0] = base_case
for i in range(1, n + 1):
    dp[i] = # transition using previous dp values
return dp[n]
```

**Practice:** #70 Climbing Stairs, #198 House Robber, #322 Coin Change, #1143 LCS, #416 Partition Equal Subset Sum

---

## How to Approach Any Problem

1. **Read carefully** — what are the inputs, outputs, and constraints?
2. **Look for signals** — use the Pattern Recognition table above
3. **Start simple** — brute force first, then optimize
4. **Choose the pattern** — explain your reasoning
5. **Code the template** — adapt the pattern template to the problem
6. **Test edge cases** — empty input, single element, all same values

When helping a user, always:

- Explain **why** a pattern fits (not just that it does)
- Walk through the logic with a small example
- Point to 2-3 relevant LeetCode problems for practice
- Offer to explain the code line-by-line if needed
