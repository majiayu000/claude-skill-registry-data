---
name: awesome-thinking
description: A structured framework for dynamic and reflective problem-solving through sequential thoughts. Use when tackling complex, multi-step problems that require careful analysis, revision of assumptions, or exploration of alternative approaches. Ideal for algorithm optimization, architectural decisions, debugging complex issues, or any task where initial understanding may need to evolve.
---

# Awesome Thinking: Sequential Reflective Thinking Framework

## Purpose

This skill provides a structured approach to complex problem-solving through sequential, reflective thinking. It enables systematic exploration of problems where understanding deepens progressively, assumptions may need revision, and multiple solution paths should be considered.

Unlike linear problem-solving, this framework embraces:
- Dynamic adjustment of solution complexity as understanding evolves
- Questioning and revising previous conclusions when new insights emerge
- Branching into alternative approaches when uncertainty exists
- Iterative hypothesis generation and verification until a satisfactory solution is reached

## When to Use This Skill

Invoke this skill for:

- **Complex multi-step problems** requiring careful breakdown and analysis
- **Problems with unclear scope** where initial estimates may need adjustment
- **Scenarios requiring course correction** as new information emerges
- **Architectural or design decisions** with multiple viable approaches and trade-offs
- **Algorithm optimization** where multiple strategies should be explored
- **Debugging complex issues** where root cause may not be immediately apparent
- **Tasks needing context maintenance** across multiple analytical steps
- **Situations with irrelevant noise** requiring careful filtering of information

Do NOT use for simple, straightforward tasks with obvious solutions.

## How to Use This Framework

### Core Thinking Process

Structure analysis as a sequence of numbered thoughts, each building toward the solution. Follow these principles:

1. **Start with an Initial Estimate**
   - Begin by estimating total thoughts needed (e.g., "I estimate this will take 5 thoughts")
   - Understand this is flexible and can be adjusted

2. **Progress Through Thoughts Sequentially**
   - Number each thought (1, 2, 3, ...)
   - Focus each thought on a specific aspect of the problem
   - Build on previous insights while remaining open to revision

3. **Types of Thoughts**

   **Regular Analytical Thoughts:**
   - Standard problem-solving steps
   - Information gathering and analysis
   - Logical deduction and inference
   - Example: "Thought 3/7: Analyzing the time complexity of the current approach..."

   **Revision Thoughts:**
   - Question or reconsider previous conclusions
   - Mark with: "Thought 5/7 (Revising Thought 2): Upon further reflection..."
   - Update understanding based on new insights
   - Example: "Thought 6/8 (Revising Thought 3): Actually, the earlier assumption about constant-time lookup was incorrect because..."

   **Branching Thoughts:**
   - Explore alternative approaches
   - Mark with: "Thought 4/7 (Branch A from Thought 2): Exploring alternative approach..."
   - Can have multiple branches: Branch A, Branch B, etc.
   - Example: "Thought 5/9 (Branch A from Thought 3): If we use a hash map instead..."

   **Realizations About Scope:**
   - Recognize when more/fewer thoughts are needed
   - Adjust total count: "Thought 5/7: This is more complex than initially estimated. Adjusting to 10 thoughts."
   - Example: "Thought 3/5: This problem is simpler than expected. Adjusting to 4 thoughts total."

   **Hypothesis Generation:**
   - Propose potential solutions
   - State clearly: "Hypothesis: [solution approach]"
   - Example: "Thought 7/10: Hypothesis: Using a trie data structure will reduce lookup time from O(n) to O(k) where k is key length."

   **Hypothesis Verification:**
   - Test proposed solutions against requirements
   - Identify flaws or confirm validity
   - Example: "Thought 8/10: Verifying hypothesis - checking edge cases... Found issue: doesn't handle Unicode properly."

4. **Iteration and Refinement**
   - If hypothesis fails verification, generate new hypothesis
   - Continue until a satisfactory solution emerges
   - Don't force premature conclusion

5. **Filtering Irrelevant Information**
   - At each thought, focus only on relevant aspects
   - Explicitly ignore tangential details
   - Example: "Thought 4/8: Focusing on the caching layer; ignoring UI concerns for now."

6. **Final Thought**
   - Clearly mark when complete: "Thought 10/10 (Final)"
   - Provide the definitive answer or solution
   - Summarize key insights if helpful

### Formatting Thoughts

Present thoughts in a clear, structured format:

```
Thought [current]/[total]: [Content]
```

For special thought types:

```
Thought [current]/[total] (Revising Thought [number]): [Content]
Thought [current]/[total] (Branch [ID] from Thought [number]): [Content]
Thought [current]/[total] (Final): [Content]
```

### Dynamic Adjustment Examples

**Increasing Scope:**
```
Thought 1/5: Analyzing the problem requirements...
Thought 2/5: Breaking down into components...
Thought 3/5: Wait, there's additional complexity here with concurrency. Adjusting to 8 thoughts.
Thought 4/8: Now examining thread-safety considerations...
```

**Decreasing Scope:**
```
Thought 1/7: Examining all possible approaches...
Thought 2/7: Actually, the built-in library handles this. Adjusting to 3 thoughts.
Thought 3/3 (Final): Use the standard library's XYZ method.
```

**Branching and Comparing:**
```
Thought 3/8: Two viable approaches identified. Exploring both.
Thought 4/8 (Branch A): Using approach A with recursion...
Thought 5/8 (Branch B): Using approach B with iteration...
Thought 6/8: Comparing branches - Branch B is more efficient due to...
Thought 7/8: Selecting Branch B approach.
```

**Revision Based on New Insight:**
```
Thought 4/7: Based on assumption X, the solution is Y...
Thought 5/7 (Revising Thought 4): Assumption X is actually false because Z. Need different approach.
Thought 6/7: New solution considering Z...
```

### Process Termination

Only conclude when:
- A satisfactory solution has been found AND verified
- All critical aspects have been considered
- Confidence in the answer is high

Do NOT conclude prematurely to meet an estimated thought count. Add more thoughts if needed.

### Example: Complete Thought Sequence

```
Thought 1/5: Analyzing the problem - need to find the fastest way to detect duplicates in a stream of integers.

Thought 2/5: Initial approach - use a HashSet for O(1) lookup. Space complexity O(n).

Thought 3/5: Considering constraints - stream is potentially infinite, can't store everything. Adjusting to 7 thoughts.

Thought 4/7 (Branch A from Thought 2): Exploring Bloom filter approach - probabilistic but constant space.

Thought 5/7 (Branch B from Thought 2): Exploring sliding window approach - only track recent N items.

Thought 6/7: Comparing approaches. If false positives acceptable, Bloom filter is optimal. Otherwise, sliding window with configurable size.

Thought 7/7 (Final): Recommendation depends on requirements:
- If no false positives allowed: Sliding window with HashSet (O(1) lookup, O(N) space for window size N)
- If rare false positives acceptable: Bloom filter (O(1) lookup, constant space)
- Recommend option 1 for correctness unless memory is severely constrained.
```

## Best Practices

1. **Be Honest About Uncertainty** - Express when multiple paths exist or understanding is incomplete
2. **Don't Force Linear Progression** - Branch, backtrack, or revise as needed
3. **Adjust Dynamically** - Change estimated thought count based on evolving understanding
4. **Focus Each Thought** - One clear purpose per thought
5. **Verify Before Concluding** - Test hypotheses against requirements and edge cases
6. **Filter Noise** - Ignore irrelevant details at each step
7. **Maintain Context** - Reference previous thoughts when building on them
8. **Embrace Iteration** - Failed hypotheses lead to better solutions

## Output Format

After completing the thought sequence, provide:

1. **The Final Answer** - Clear, actionable solution or recommendation
2. **Key Insights** (optional) - Summary of important discoveries from the thinking process
3. **Next Steps** (if applicable) - What should be done to implement or verify the solution

Present this as normal output after the thought sequence, not as another numbered thought.
