---
name: ai-output-evaluation
description: Evaluate AI-generated output quality using LLM-as-judge techniques, multi-dimensional rubrics, and bias mitigation. Use when building AI-powered features.
---

# AI Output Evaluation

Specialized expertise in systematically evaluating the quality of AI-generated output (code, documentation, analysis, tests) using structured rubrics, LLM-as-judge patterns, and bias mitigation techniques.

## When to Use This Skill

Use this skill for:

- Evaluating quality of AI-generated code before merging
- Building automated quality gates for AI-powered pipelines
- Designing review rubrics for generated documentation
- Comparing outputs from different models or prompts
- Setting up continuous evaluation for AI-assisted workflows
- Assessing whether AI-generated tests provide real coverage

**Trigger phrases**: "evaluate AI output", "quality rubric", "LLM as judge", "output evaluation", "generated code quality", "review AI work", "evaluation pipeline", "bias in evaluation"

## What This Skill Does

Provides AI output evaluation capabilities including:

- **Rubric Design**: Building multi-dimensional scoring frameworks
- **LLM-as-Judge**: Using AI to evaluate AI output systematically
- **End-State Evaluation**: Evaluating final artifacts rather than intermediate steps
- **Bias Mitigation**: Detecting and correcting systematic evaluation biases
- **Token Economics**: Understanding the cost-quality relationship
- **Evaluation Pipelines**: Automating quality assessment in workflows

## Instructions

### Step 1: Define Evaluation Dimensions

Every evaluation needs explicit dimensions. Without defined criteria, evaluation devolves into subjective "looks good" assessments.

**Multi-Dimensional Rubric Template**:

```markdown
## Evaluation Rubric: [Output Type]

### Dimensions

| Dimension | Weight | 0.0 (Fail) | 0.5 (Partial) | 1.0 (Pass) |
|-----------|--------|-----------|---------------|------------|
| **Correctness** | 30% | Contains errors or wrong logic | Mostly correct with minor issues | Fully correct, handles edge cases |
| **Completeness** | 25% | Missing major components | Covers main cases, misses edges | Comprehensive coverage |
| **Style Adherence** | 15% | Ignores project conventions | Partially follows conventions | Fully consistent with codebase |
| **Security** | 15% | Contains vulnerabilities | No obvious issues, not hardened | Proactively secure (input validation, etc.) |
| **Performance** | 15% | Obvious bottlenecks | Acceptable performance | Optimized for the use case |

### Scoring
- Weighted score: Sum of (dimension_score x weight)
- Pass threshold: >= 0.70
- Requires review: 0.50-0.69
- Fail: < 0.50
```

**Rubric Variants by Output Type**:

| Output Type | Key Dimensions |
|-------------|---------------|
| **Generated code** | Correctness, completeness, style, security, performance |
| **Documentation** | Accuracy, clarity, completeness, structure, audience-appropriateness |
| **Test suites** | Coverage, edge case detection, isolation, maintainability, speed |
| **Analysis reports** | Factual accuracy, completeness, actionability, source quality |
| **Refactoring** | Behavior preservation, code quality improvement, test continuity |

### Step 2: Implement LLM-as-Judge

Use a structured prompt to have an LLM evaluate output against the rubric. The key is requiring **evidence-based justification** for each score (chain-of-thought improves reliability by 15-25%).

**Direct Scoring Prompt Template**:

```markdown
## Evaluation Task

You are evaluating the following [output type] against a quality rubric.

### Output to Evaluate
[The AI-generated output]

### Context
- Task description: [What was requested]
- Project conventions: [Relevant style/patterns]
- Constraints: [Requirements, limitations]

### Rubric
[Paste the rubric from Step 1]

### Instructions
For each dimension:
1. Quote specific evidence from the output (good or bad)
2. Assign a score (0.0-1.0) with justification
3. List specific improvements needed

### Required Output Format
```json
{
  "dimensions": {
    "correctness": {
      "score": 0.8,
      "evidence": ["Line 45: correctly handles null case", "Line 72: missing boundary check for negative values"],
      "improvements": ["Add check for negative input values"]
    },
    // ... other dimensions
  },
  "weighted_score": 0.76,
  "verdict": "PASS",
  "summary": "One-sentence overall assessment"
}
```
```

**Critical rule**: Always require evidence quotes. Without evidence, LLM judges default to generous scores (verbosity bias).

### Step 3: Design End-State Evaluation

Evaluate **final artifacts**, not intermediate steps. AI agents are non-deterministic; two agents may take completely different paths to equally good results. Evaluating the process (number of steps, tools used, approach taken) penalizes valid alternative solutions.

**End-State Evaluation Principles**:

| Principle | Explanation |
|-----------|------------|
| **Evaluate artifacts, not steps** | A working function matters more than how it was written |
| **Allow multiple valid solutions** | Don't penalize creative approaches that achieve the goal |
| **Test behavior, not structure** | Run the code; check the output; verify the tests pass |
| **Measure what matters** | "Does it solve the problem?" over "Does it look like what I expected?" |

**End-State Evaluation Checklist**:

```markdown
## End-State Evaluation: [Task]

### Functional Verification
- [ ] Output compiles/parses without errors
- [ ] All existing tests still pass
- [ ] New functionality works as specified
- [ ] Edge cases handled (or explicitly documented as out of scope)

### Quality Verification
- [ ] Rubric score >= threshold (Step 1)
- [ ] No security vulnerabilities introduced
- [ ] Performance acceptable for the use case
- [ ] Code follows project conventions

### Integration Verification
- [ ] Changes integrate with existing codebase
- [ ] No regressions in dependent components
- [ ] Documentation updated if needed
```

### Step 4: Mitigate Evaluation Bias

LLM judges exhibit systematic biases that skew scores. Recognizing and mitigating the top 3 biases significantly improves evaluation reliability.

**Top 3 Practical Biases**:

| Bias | Description | Mitigation |
|------|-------------|------------|
| **Verbosity bias** | Longer, more detailed outputs receive higher scores regardless of quality. A 100-line function gets rated higher than a correct 10-line function. | Include rubric criterion: "Conciseness: penalize unnecessary complexity." Explicitly state: "A shorter correct solution is better than a longer correct solution." |
| **Position bias** | In pairwise comparisons, the first option is favored. | Evaluate twice with swapped positions; flag inconsistencies. |
| **Self-enhancement bias** | Models rate their own output (or output in their style) higher than alternatives. | Use a different model as judge when possible, or use human spot-checks to calibrate. |

**Bias Mitigation Protocol**:

```markdown
## Bias Mitigation Checklist

### Before Evaluation
- [ ] Rubric explicitly penalizes unnecessary verbosity
- [ ] "Shorter correct > longer correct" stated in instructions
- [ ] Evidence requirement included (no scoring without quotes)

### During Evaluation (for pairwise comparisons)
- [ ] Evaluate with options in original order
- [ ] Evaluate with options in swapped order
- [ ] Flag if scores differ by > 0.2 between orderings
- [ ] Use majority vote across 3 evaluations for high-stakes decisions

### After Evaluation
- [ ] Spot-check 10-20% of scores against human judgment
- [ ] Track score distributions; investigate if average is consistently > 0.8 (calibration drift)
- [ ] Update rubric if a dimension consistently scores too high or too low
```

### Step 5: Track Token Economics

Understanding the relationship between token usage and output quality helps allocate resources effectively.

**Key Finding**: Token usage accounts for approximately **80% of output quality variance** in agent tasks. Tool call frequency contributes ~10%, and model selection ~5%.

**What This Means in Practice**:

| Situation | Implication |
|-----------|------------|
| Agent produces low-quality output | First check if it had enough context (tokens); model switching is rarely the fix |
| Budget is constrained | Invest tokens in context quality (better prompts, relevant file reads) over more turns |
| Evaluation scores are inconsistent | Check if the evaluator has enough context to judge properly |

**Cost-Quality Framework**:

```markdown
## Token Budget for Evaluation Pipeline

### Per-Item Evaluation Cost
- Input: ~2,000 tokens (output + rubric + context)
- Output: ~500 tokens (structured evaluation result)
- Total: ~2,500 tokens per evaluation

### Pipeline Cost Estimate
- Items to evaluate: [N]
- Per-item cost: ~2,500 tokens x [price/1K tokens]
- Total: [N x 2,500 / 1000 x price]
- Budget for re-evaluation (20% of items flagged): + 20%
```

## Best Practices

- **Define rubrics before generating output**: Knowing evaluation criteria shapes better prompts
- **Require evidence for every score**: Unjustified scores are unreliable
- **Evaluate end states, not processes**: Allow creative solutions
- **Calibrate with human judgments**: Spot-check regularly to catch drift
- **Use appropriate granularity**: Binary (pass/fail) for simple checks; 0.0-1.0 for nuanced assessment
- **Track trends over time**: If average scores drift upward, tighten rubrics or re-calibrate
- **Budget for evaluation tokens**: Evaluation is not free; plan token costs into pipelines

## Common Patterns

### Pattern 1: Code Review Rubric

**Situation**: Evaluating AI-generated code before merging to main.

**Solution**:
1. Define rubric: correctness (30%), completeness (25%), style (15%), security (15%), performance (15%)
2. Run end-state checks: compilation, existing tests, new functionality
3. Apply LLM-as-judge with evidence requirement
4. Flag items scoring <0.70 for human review

### Pattern 2: Documentation Quality Gate

**Situation**: Automated documentation generation needs quality assurance.

**Solution**:
1. Define rubric: accuracy (35%), clarity (25%), completeness (20%), structure (10%), audience fit (10%)
2. Evaluate against the actual codebase (does the doc match the code?)
3. Check for common doc failures: outdated API references, missing parameters, wrong examples

### Pattern 3: Generated Test Evaluation

**Situation**: AI-generated test suites need validation that they provide real coverage.

**Solution**:
1. Run the tests (do they pass?)
2. Check coverage metrics (do they cover the target code?)
3. Mutation testing (do they catch intentional bugs?)
4. Review test quality: independence, meaningful assertions, edge cases

## Quality Checklist

- [ ] Evaluation rubric defined with weighted dimensions
- [ ] Scoring scale and pass/fail thresholds established
- [ ] LLM-as-judge prompt includes evidence requirement
- [ ] End-state evaluation (not process evaluation) applied
- [ ] Top 3 biases addressed in evaluation design
- [ ] Token budget estimated for evaluation pipeline
- [ ] Human spot-checks planned for calibration

## Related Skills

- `code-quality` - Code quality standards and review criteria
- `testing-review` - Test quality assessment methodology
- `final-report` - Consolidating review findings into actionable reports
- `context-manager` - Ensuring evaluators have sufficient context

---

**Version**: 1.0.0
**Last Updated**: February 2026
**Author**: DevAI-Hub
**Attribution**: Adapted from [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) (MIT License)


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
