---
name: review-solution
description: Review coding challenge solutions from LeetCode, GreatFrontEnd, or other platforms. Analyze algorithm correctness, time/space complexity, code quality, identify patterns, explain key insights, and suggest related problems. Use when reviewing DSA solutions, analyzing complexity, or providing educational feedback on coding challenges.
---

# Code Review Skill for Coding Challenges

Provide comprehensive, educational code reviews for LeetCode, GreatFrontEnd, and other coding challenge solutions following established repository guidelines.

## Review Process

### Step 1: Identify the Problem Context

1. Read the problem's README.md to understand:
   - Problem description and constraints
   - Platform (LeetCode, GreatFrontEnd, etc.)
   - Difficulty level
   - Expected inputs/outputs

2. Read the solution file(s) completely before making any suggestions

### Step 2: Algorithm Correctness

Verify the solution is correct:

- **Test Coverage**: Does it handle all test cases mentioned in the problem?
- **Edge Cases**: Check for:
  - Empty arrays/strings
  - Single elements
  - Negative numbers
  - Null/undefined values
  - Minimum/maximum constraint values
  - Duplicate elements
- **Constraint Validation**: Confirm solution handles all problem constraints
- **Logical Correctness**: Walk through the algorithm step-by-step

### Step 3: Time & Space Complexity Analysis

Provide deep complexity analysis with explanations:

- **State the Complexity**: Provide Big O notation for time and space
- **Explain WHY**: Don't just state O(n) - explain the reasoning
  - Example: "O(n) because each element is visited at most twice - once when the right pointer includes it, once when the left pointer excludes it"
- **Amortized Analysis**: If applicable, explain amortized complexity reasoning
- **Optimization Check**: Is there a more efficient approach?
- **Compare to Optimal**: If this isn't optimal, mention what the optimal complexity would be

### Step 4: Pattern Identification (Critical for Learning)

This is essential for interview preparation:

- **Identify the Pattern**: State which algorithmic pattern(s) are used:
  - Two Pointers
  - Sliding Window (fixed or variable)
  - Binary Search
  - BFS/DFS
  - Dynamic Programming
  - Backtracking
  - Union-Find
  - Topological Sort
  - Greedy
  - Divide and Conquer
  - Hash Map/Set
  - Monotonic Stack/Queue
  - Prefix Sum
  - Fast & Slow Pointers
  - And others...

- **Explain WHY**: Explain why this pattern is suitable for this problem type
- **Key Insight**: Every problem has a key insight - identify and explain it clearly
  - Example: "The key insight is using a hash map to achieve O(1) complement lookup instead of O(n) linear search"
  - Example: "The key insight is that exactlyK = atMostK(k) - atMostK(k-1)"

### Step 5: Suggest Related Problems

Help build pattern recognition:

- Suggest 2-3 similar problems that use the same pattern
- Can be from any platform (LeetCode, GreatFrontEnd, HackerRank, etc.)
- Mention if the same problem exists on different platforms
- Group by pattern family when applicable

Examples:

- "Other variable sliding window problems: Longest Substring Without Repeating Characters (LC 3), Minimum Window Substring (LC 76)"
- "Other two-pointer problems: Container With Most Water (LC 11), 3Sum (LC 15)"

### Step 6: Code Quality Review

#### For All Solutions

- **Variable Naming**: Clear, descriptive names (not just `i`, `j`, `k` unless in simple loops)
- **Comments**: Add comments for non-obvious logic or algorithm steps
- **Function Focus**: Keep functions single-purpose
- **Readability**: Prefer readability over cleverness

#### JavaScript/TypeScript Specific

- **Variable Declarations**: Use `const` by default, `let` only when reassignment needed
- **Avoid `var`**: Except for LeetCode solution function definitions (their format requirement)
- **Modern Syntax**: Use ES6+ features where appropriate:
  - Arrow functions
  - Destructuring
  - Spread operators
  - Optional chaining (`?.`)
  - Nullish coalescing (`??`)
- **Array Methods**: Prefer `.map()`, `.filter()`, `.reduce()` when appropriate
- **Strict Equality**: Use `===` over `==`

#### Platform-Specific: GreatFrontEnd

For frontend challenges, also check:

- **Browser APIs**: Correct usage of DOM, Fetch, Storage APIs
- **Event Handling**: Proper event delegation and cleanup
- **Async/Await**: Correct Promise and async/await usage
- **Performance**: Unnecessary DOM manipulations, memory leaks (event listeners, timers)
- **API Design**: Public API clarity, parameter validation, error handling
- **Code Organization**: Functional patterns, separation of concerns

### Step 7: Problem-Specific Pattern Reviews

#### Graph Problems

- Verify proper graph representation (adjacency list/matrix)
- Check for visited tracking to avoid cycles
- Confirm DFS/BFS implementation follows standard patterns
- Look for Union-Find correctness if applicable

#### Array/String Problems

- Check two-pointer technique correctness
- Verify sliding window boundaries
- Confirm hash map usage is optimal

#### Dynamic Programming

- Verify state definition is correct
- Check base cases
- Confirm state transitions are accurate
- Look for space optimization opportunities (1D vs 2D DP)

### Step 8: Common Mistakes

Point out common mistakes people make with the identified pattern:

- Example: "A common mistake with sliding window is forgetting to clean up the frequency map when elements leave the window"
- Example: "A common mistake with two pointers is not handling duplicates correctly"
- Example: "A common mistake with DFS is not properly restoring state during backtracking"

### Step 9: What NOT to Flag

Do not criticize:

- Multiple solution approaches (exploratory learning is encouraged)
- Console.log statements (used for debugging/learning)
- Less optimal solutions if clearly marked as alternative approaches
- Alternative valid patterns for solving the same problem

## Output Format

Structure your review as follows:

```markdown
## Code Review: [Problem Name]

### Correctness

[Verification of correctness and edge case handling]

### Complexity Analysis

**Time Complexity**: O(...)
**Space Complexity**: O(...)

[Detailed explanation of WHY, not just what]

### Pattern Recognition

**Primary Pattern**: [Pattern Name]

**Key Insight**: [The crucial insight that makes the optimal solution possible]

**Why This Pattern**: [Explain why this pattern fits this problem]

### Related Problems

- [Problem 1 with platform]
- [Problem 2 with platform]
- [Problem 3 with platform]

### Code Quality

[Specific feedback on code quality, naming, style]

### Common Mistakes

[Common pitfalls with this pattern]

### Optimizations (if applicable)

[Suggestions for improvements, if any]
```

## Tone

- **Educational**: Explain WHY, not just WHAT
- **Constructive**: Focus on learning and improvement
- **Encouraging**: This is a learning repository
- **Specific**: Reference exact line numbers using `file_path:line_number` format

## Examples

### Example 1: Two Pointers Pattern

```markdown
### Pattern Recognition

**Primary Pattern**: Two Pointers (opposite ends)

**Key Insight**: By starting pointers at both ends and moving them based on the sum comparison, we avoid checking all O(n²) pairs and achieve O(n) time complexity.

**Why This Pattern**: Two pointers works here because the array is sorted, allowing us to make decisions about which pointer to move based on whether the current sum is too large or too small.
```

### Example 2: Complexity Explanation

```markdown
### Complexity Analysis

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why O(n) time**: We traverse the array once with two pointers. Each pointer moves at most n times, and pointer movements never backtrack. Although we have nested operations, each element is processed exactly once.

**Why O(1) space**: We only use a constant number of variables (left, right, result) regardless of input size.
```

## Reference Files

For complete repository guidelines, refer to `/Users/robsimpson/Repos/coding-challenges/CLAUDE.md`
