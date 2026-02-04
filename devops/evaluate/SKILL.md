---
name: evaluate
description: This skill should be used when evaluating the logical flow, structure, readability, and overall quality of research paper text. Use for assessing academic writing targeting top-tier computer science conferences.
---

# Academic Text Evaluator

Evaluate research paper text for logical flow, structure, clarity, and readability without modifying the original content.

## When to Use This Skill

- Assessing the quality of research paper sections
- Evaluating logical flow and argument structure
- Providing feedback on clarity and readability
- Scoring text quality for academic writing
- Identifying areas for improvement in conference submissions

## Target Audience

Graduate students, professors, and researchers writing for top-tier computer science conferences (e.g., OSDI, NSDI, SOSP, SIGCOMM).

## Evaluation Criteria

Evaluate text across five dimensions:

### 1. Logical Cohesion
- Assess whether arguments progress naturally and convincingly
- Identify logical jumps or gaps in reasoning
- Check if sentences and paragraphs connect smoothly
- Verify effective use of transition words and phrases

### 2. Clarity and Fluency
- Determine if the text is easy to understand
- Check for precise and unambiguous language
- Assess overall reading fluency

### 3. Organization
- Evaluate information structure effectiveness
- Check if paragraphs are well-focused with distinct points
- Assess optimal ordering of ideas

### 4. Pacing and Detail
- Identify content that is too verbose or too terse
- Check appropriate detail level for the target audience

### 5. Reader Engagement
- Assess if readers can easily follow the narrative
- Verify that main points are clear and graspable

## Scoring Guidelines

Provide an overall quality score (0-100) with these requirements:

- **Linear consistency**: Score should linearly reflect quality
- **Proportional scaling**: If one mistake reduces score to 90, nine similar mistakes should not reduce it to 0
- **Impact indication**: For each suggested modification, indicate score impact (e.g., "+5 points")

## Feedback Format

Follow these principles when providing feedback:

### Bad-first Approach
- Focus primarily on weaknesses and areas for improvement
- Only discuss strengths if the text is of very high quality
- Avoid praising adequate or mediocre work

### Self-consistency
- If text previously scored 100 and hasn't changed, do not invent new improvements
- Maintain consistent standards across evaluations

### Actionable Advice
- Provide specific, concrete suggestions
- Include examples when helpful
- Format: "The transition between paragraph 2 and 3 feels abrupt; consider adding a sentence to bridge X with Y. (+3 points)"

## Important Constraints

- **Do not modify** the original content during evaluation
- **Only suggest significant improvements** that meaningfully impact quality
- Avoid pedantic or minor suggestions
- Penalties apply for suggesting non-significant modifications

## Output Structure

1. **Overall Score**: (0-100)
2. **Dimension Scores**: Optional breakdown by the five criteria
3. **Key Issues**: List of significant problems identified
4. **Specific Suggestions**: Actionable improvements with estimated score impact
5. **Strengths**: Only if score > 85
