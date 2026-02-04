---
name: validation
description: This skill should be used when validating whether a specific word or phrase is appropriate, commonly used, and correct in academic technical contexts. Use for checking terminology in research papers targeting top-tier computer science conferences.
---

# Academic Word Validator

Assess whether marked words or phrases are appropriate, commonly used, and correct in the context of technical research papers, providing alternatives when needed.

## When to Use This Skill

- Validating word choices in research papers
- Checking if terminology is commonly used in the field
- Assessing appropriateness of technical phrasing
- Verifying idiomatic usage for non-native speakers
- Confirming correctness of academic writing style

## Input Format

The user will provide a sentence with a word or phrase marked using `<>` delimiters.

Example: "The system demonstrates <good> performance under various workloads."

## Assessment Process

Follow this two-step process:

### Step 1: Scoring
Provide a confidence score (0-100) for the current usage based on:
- Grammatical correctness
- Common usage in the field
- Appropriateness for academic writing
- Precision and clarity
- Idiomaticity

### Step 2: Output Based on Score

#### If Score > 80 (Acceptable)
- State that the usage is appropriate
- Provide the sentence with `<>` markers removed
- Optionally note any minor considerations

Example:
```
Score: 85/100 - Usage is appropriate and commonly used in systems research.

Validated sentence: "The system demonstrates good performance under various workloads."
```

#### If Score ≤ 80 (Needs Improvement)
Provide comprehensive feedback:

1. **Explanation** - Why the word/phrase is suboptimal:
   - Awkward phrasing
   - Imprecise meaning
   - Uncommon in the field
   - Grammatically incorrect
   - Too informal/formal

2. **Alternatives** - Provide 2-3 better candidates with:
   - The alternative word/phrase
   - Preference score (0-100)
   - Explanation of advantages
   - Comparison to original

Example:
```
Score: 65/100 - The word "good" is grammatically correct but too informal and imprecise for academic writing.

Alternatives:
- **strong** (90/100): More precise and widely used in performance discussions; conveys solid results without overstatement
- **favorable** (85/100): Formal and appropriate; emphasizes positive aspects; common in academic papers
- **competitive** (80/100): Implies comparison with baselines; suitable if benchmarking against other systems
```

## Scoring Guidelines

- **90-100**: Excellent - precise, common, idiomatic, and perfectly appropriate
- **81-89**: Good - acceptable with very minor issues
- **70-80**: Borderline - usable but better alternatives exist
- **50-69**: Problematic - awkward, uncommon, or imprecise
- **Below 50**: Incorrect - grammatically wrong or highly inappropriate

## Validation Criteria

Assess marked text based on:

### 1. Grammatical Correctness
- Is it grammatically correct?
- Does it fit the sentence structure?

### 2. Common Usage
- Is this terminology commonly used in top-tier conference papers?
- Would reviewers recognize and accept this usage?

### 3. Precision
- Does it convey the exact intended meaning?
- Is it specific enough for technical writing?

### 4. Appropriateness
- Is it suitable for formal academic writing?
- Does it match the tone of research papers?

### 5. Idiomaticity
- Is this how native speakers would phrase it?
- Does it sound natural in technical contexts?

### 6. Sub-field Conventions
- Does it align with terminology used in the specific research area?
- Are there field-specific preferences?

## Target Audience

Graduate students, professors, and researchers in computer science writing for top-tier conferences (e.g., OSDI, NSDI, SOSP, SIGCOMM).

## Important Guidelines

- Be honest about scores - don't artificially inflate or deflate
- Provide actionable alternatives when score ≤ 80
- Consider the specific context and field
- Explain trade-offs between alternatives
- Focus on common usage in the target publication venues
