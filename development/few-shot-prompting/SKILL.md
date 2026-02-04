---
name: few-shot-prompting
description: Example-based prompting techniques for in-context learning
sasmp_version: "1.3.0"
bonded_agent: 02-few-shot-specialist-agent
bond_type: PRIMARY_BOND
---

# Few-Shot Prompting Skill

**Bonded to:** `few-shot-specialist-agent`

---

## Quick Start

```bash
Skill("custom-plugin-prompt-engineering:few-shot-prompting")
```

---

## Parameter Schema

```yaml
parameters:
  shot_count:
    type: integer
    range: [0, 20]
    default: 3
    description: Number of examples to include

  example_format:
    type: enum
    values: [input_output, labeled, conversational, structured]
    default: input_output

  ordering_strategy:
    type: enum
    values: [random, similarity, difficulty, recency]
    default: similarity
```

---

## Shot Strategies

| Strategy | Examples | Best For | Trade-offs |
|----------|----------|----------|------------|
| Zero-shot | 0 | Simple, well-defined tasks | Fast but less accurate |
| One-shot | 1 | Format demonstration | Minimal context usage |
| Few-shot | 2-5 | Pattern learning | Balanced accuracy/tokens |
| Many-shot | 6-20 | Complex classifications | High accuracy, high tokens |

---

## Core Patterns

### 1. Standard Input-Output

```markdown
[Task instruction]

Example 1:
Input: [example_input_1]
Output: [example_output_1]

Example 2:
Input: [example_input_2]
Output: [example_output_2]

Example 3:
Input: [example_input_3]
Output: [example_output_3]

Now process:
Input: [actual_input]
Output:
```

### 2. Labeled Classification

```markdown
Classify the following text into categories: [category_list]

"[text_1]" → [category_1]
"[text_2]" → [category_2]
"[text_3]" → [category_3]

"[new_text]" →
```

### 3. Structured Output

```markdown
Extract information in the specified format.

Text: "John Smith, CEO of TechCorp, announced the merger on Monday."
Output: {"name": "John Smith", "title": "CEO", "company": "TechCorp", "action": "announced merger", "date": "Monday"}

Text: "Dr. Sarah Chen presented findings at the 2024 AI Conference."
Output: {"name": "Sarah Chen", "title": "Dr.", "event": "2024 AI Conference", "action": "presented findings"}

Text: "[new_text]"
Output:
```

### 4. Chain-of-Thought Few-Shot

```markdown
Solve the following problems showing your reasoning.

Problem: If a shirt costs $25 and is on 20% sale, what's the final price?
Reasoning: 20% of $25 = $25 × 0.20 = $5 discount. Final price = $25 - $5 = $20.
Answer: $20

Problem: [new_problem]
Reasoning:
Answer:
```

---

## Example Selection Criteria

```yaml
selection_criteria:
  diversity:
    coverage: "Include all output classes/categories"
    variation: "Vary input complexity and length"
    edge_cases: "Include at least one boundary case"

  quality:
    correctness: "All examples must have correct outputs"
    clarity: "Examples should be unambiguous"
    representativeness: "Reflect real-world distribution"

  relevance:
    similarity: "Examples similar to expected inputs"
    domain: "Match the target domain/context"
    recency: "Use recent examples for time-sensitive tasks"
```

---

## Ordering Strategies

| Strategy | Implementation | When to Use |
|----------|---------------|-------------|
| Similarity-based | Most similar to input last | Retrieval-augmented systems |
| Difficulty gradient | Simple → Complex | Learning/educational tasks |
| Random | Shuffled order | Reduce position bias |
| Recency | Most recent last | Time-sensitive tasks |
| Reverse-difficulty | Complex → Simple | Emphasize simple patterns |

---

## Token Optimization

```yaml
optimization_techniques:
  concise_examples:
    description: "Use minimal but complete examples"
    savings: "~25%"
    example:
      verbose: "The customer said 'This product is amazing!' which expresses positive sentiment"
      concise: "'Amazing product!' → positive"

  shared_prefix:
    description: "Factor out common instructions"
    savings: "~15%"
    implementation: "Move repeated text to instruction section"

  dynamic_loading:
    description: "Only load relevant examples"
    savings: "~40%"
    implementation: "Use semantic search to select examples"
```

---

## Validation

```yaml
validation_checklist:
  format:
    - [ ] All examples use identical structure
    - [ ] Separators are consistent
    - [ ] Input/output markers are clear

  content:
    - [ ] Examples cover all output categories
    - [ ] No duplicate examples
    - [ ] Edge cases included

  quality:
    - [ ] All outputs are correct
    - [ ] No example leakage (test data in examples)
    - [ ] Complexity is varied
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Model copies examples | Overfitting | Add more diverse examples |
| Wrong format | Inconsistent examples | Standardize all formats |
| Missing categories | Imbalanced examples | Balance class distribution |
| Poor accuracy | Too few examples | Increase shot count |
| Token overflow | Too many examples | Reduce count, improve quality |

---

## Integration

```yaml
integrates_with:
  - prompt-design: Base prompt structure
  - chain-of-thought: Reasoning examples
  - prompt-evaluation: Test effectiveness

combination_example: |
  # Few-shot + CoT
  [Instruction]

  Example 1:
  Input: [problem]
  Reasoning: [step-by-step]
  Output: [answer]

  Example 2: ...
```

---

## References

See `references/GUIDE.md` for example selection strategies.
See `assets/config.yaml` for configuration options.
