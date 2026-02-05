---
name: selection
description: This skill should be used when suggesting word or phrase alternatives for placeholders in academic research papers. Use when the author needs help selecting appropriate technical terminology for top-tier computer science conferences.
---

# Academic Word Selection

Propose three distinct candidate words or short phrases for placeholders in research paper text, with scoring and justification for each option.

## When to Use This Skill

- Selecting appropriate technical terminology for research papers
- Choosing between multiple word options for academic writing
- Finding the most precise term for a specific context
- Evaluating vocabulary choices for conference submissions
- Helping non-native speakers select idiomatic technical terms

## Input Format

The user will provide a sentence containing a placeholder in the format `[word_to_select]` or `[phrase_to_select]`.

Example: "The system achieves [word_to_select] performance under high load."

## Output Format

For each placeholder, propose three distinct candidates with the following structure:

### Candidate Structure

For each of the three candidates, provide:

1. **The candidate word/phrase** (clearly stated)
2. **Preference score** (0-100, where 100 is most preferred)
3. **Meaning and nuance** - Explain the specific meaning in this context
4. **Suitability reasoning** - Discuss why it is or isn't a good choice
5. **Usage context** - Note if it's common/rare in the sub-field

### Example Output Format

```
**Candidate A: "exceptional"** (90/100)
- Meaning: Performance significantly above average
- Preferred as it precisely conveys high quality without exaggeration
- Common in systems research papers
- Suitable for formal academic writing

**Candidate B: "strong"** (75/100)
- Meaning: Good but not outstanding performance
- Also suitable but slightly less emphatic
- Very common and safe choice
- May be too general for highlighting key contributions

**Candidate C: "adequate"** (40/100)
- Meaning: Satisfactory but not impressive
- Grammatically correct but conveys mediocrity
- Less suitable if highlighting a strength
- Consider only if tempering claims
```

## Selection Criteria

Evaluate candidates based on:

### 1. Precision
- Does the word precisely convey the intended technical meaning?
- Is it specific enough for the context?

### 2. Common Usage
- Is this terminology common in the target sub-field?
- Would reviewers recognize and accept this usage?

### 3. Formality
- Is it appropriate for formal academic writing?
- Does it maintain the right tone for conference papers?

### 4. Clarity
- Will the meaning be immediately clear to readers?
- Does it avoid ambiguity?

### 5. Idiomaticity
- Is this how native speakers would phrase it?
- Does it sound natural in technical writing?

## Target Audience

Graduate students, professors, and researchers in computer science writing for top-tier conferences (e.g., OSDI, NSDI, SOSP, SIGCOMM).

## Scoring Guidelines

- **90-100**: Highly preferred - precise, common, idiomatic, and appropriate
- **70-89**: Suitable - acceptable choice with minor trade-offs
- **50-69**: Acceptable - usable but not ideal for this context
- **Below 50**: Not recommended - better alternatives available

## Important Guidelines

- Prioritize clarity and precision above all
- Consider the specific sub-field and context
- Explain trade-offs between candidates
- Avoid overly complex or obscure terminology unless necessary
- Consider how the choice affects the overall argument or claim
