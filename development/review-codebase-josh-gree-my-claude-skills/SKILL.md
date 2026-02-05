---
name: review-codebase
description: Review overall codebase health, architecture, and patterns using Google's engineering principles. Takes optional focus area. Use when the user wants to review code quality, assess architecture, or says "/review-codebase" or "/review-codebase 'API layer'".
user-invocable: true
arguments:
  - name: focus-area
    description: Optional focus area to review (e.g., "API layer", "tests", "auth system"). Defaults to full codebase if omitted.
---

# Review Codebase

Review overall codebase health, architecture, and patterns following Google's engineering practices.

## Purpose

This skill performs a comprehensive codebase review examining overall code health, architecture, patterns, and adherence to engineering principles across the entire codebase (or a specified subset).

**Key difference from PR review:** There's no diff to examine. Instead of reviewing changes, we review overall structure and health of the codebase.

## Prerequisites

- Git remote must exist (codebase reviews should be on projects with remotes)
- No requirement for clean working tree (we're not making changes)

## When to Use

Use this skill when you want to:
- Assess overall code health and technical debt
- Evaluate architecture and design patterns
- Review code quality and consistency
- Identify areas for improvement across the codebase
- Understand codebase structure and organisation

**Compare to other review skills:**
- **review-codebase**: Overall health, architecture, patterns (this skill)
- **review-pr**: Specific changes in a pull request
- **review**: Ad-hoc file or directory review

## Review Approach

Follow this multi-phase process to produce thorough codebase reviews:

## Workflow

### Phase 1: Initial Review

Conduct a complete codebase review following these steps:

#### Step 1: Verify Environment

Check we have a GitHub remote:

```bash
git remote -v
```

**STOP if:**
- No remote exists → "This skill requires a GitHub remote. Codebase reviews are intended for projects with remotes."

#### Step 2: Determine Review Scope

If a focus area was provided as an argument (e.g., "API layer", "tests", "auth system"):
- Use that to guide exploration
- Example: `/review-codebase "API layer"`

If no argument was provided:
- Review the entire codebase
- Example: `/review-codebase`

#### Step 3: Explore the Codebase

Use the Task tool with `subagent_type: "Explore"` for thorough codebase exploration:

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Explore codebase structure"
  prompt: |
    Explore this codebase to understand its structure, architecture, and key patterns.

    [If focus area provided:]
    Focus area: <focus-area>
    Concentrate your exploration on this area of the codebase.

    [Always:]
    Identify:
    - Overall project structure and organisation
    - Key architectural patterns and decisions
    - Main components and their relationships
    - Testing approach and organisation
    - Documentation quality (README, API docs, etc.)
    - Style and naming conventions
    - Areas of high complexity

    Use thoroughness level: "very thorough"

    Return:
    1. Project structure overview
    2. Key files and directories
    3. Architectural patterns observed
    4. Notable patterns (good and bad)
    5. Areas that warrant closer review
```

The Explore agent will:
- Identify key files, patterns, and architecture decisions
- Understand overall structure and health
- Highlight areas worth closer inspection

#### Step 4: Review the Codebase

Using the exploration results, conduct a systematic review across these categories:

##### Review Categories (Adapted from Google's Principles)

**1. Architecture & Design**
- Overall system structure and component organisation
- Separation of concerns
- Module boundaries and dependencies
- Design patterns and their appropriateness
- Consistency of architectural decisions

**2. Code Health**
- Consistency across the codebase
- Maintainability and readability
- Technical debt patterns
- Code duplication
- Dead code or unused functionality

**3. Testing Strategy**
- Test coverage approach (not just percentage, but what's tested)
- Test quality and usefulness
- Test organisation and structure
- Balance of unit, integration, and e2e tests
- Test maintainability

**4. Naming & Conventions**
- Naming consistency across files and modules
- Clarity of names
- Adherence to project conventions
- Consistency of terminology

**5. Documentation**
- README quality and completeness
- API documentation
- Architectural documentation (ADRs, design docs)
- Code comments (appropriate use of why-not-what)
- Inline documentation

**6. Complexity Patterns**
- Over-engineering (solving hypothetical future problems)
- Under-engineering (missing necessary abstractions)
- Areas of high cyclomatic complexity
- Opportunities for simplification

**7. Style Consistency**
- Adherence to style guides
- Consistency across different parts of codebase
- Formatting and code organisation

**8. Error Handling & Robustness**
- Error handling patterns
- Edge case handling
- Validation at boundaries
- Defensive programming practices

##### Review Approach

- **Sample files** rather than reading everything (balance thoroughness with practicality)
- **Focus on patterns** rather than individual lines
- **Read key files completely** to understand them deeply
- **Use exploration results** to guide which areas to examine closely
- **Identify both problems and good patterns** worth preserving/expanding

#### Step 5: Structure Findings

Organise findings by category with severity levels:

**Severity Levels:**

- **Critical**: Architectural issues, security vulnerabilities, major design problems that impact overall system health
- **Suggestion**: Improvements that would make code cleaner, better patterns, opportunities for simplification
- **Observation**: Patterns noted (can be positive or neutral)

**Include:**
- **Positive Observations**: Good patterns worth preserving and expanding
- **Pattern Examples**: Reference specific files that exemplify patterns (good or bad)

### Phase 2: Critique

After completing the initial review, **launch a subagent using the Task tool** to critique the review. Using a separate agent provides a genuinely fresh perspective.

**You MUST use the Task tool** with `subagent_type: "general-purpose"` to run the critique. Do not attempt to critique your own review directly.

Provide the subagent with:
1. The scope of the review (full codebase or focus area)
2. Key files and areas examined
3. Your complete initial review output
4. Instructions to critique the review

The critique subagent examines the initial review and looks for:

- **Missed patterns** - Systemic issues or good patterns that the initial review didn't identify
- **Incorrect severity** - Findings that should be upgraded or downgraded based on their impact
- **False positives** - Findings that aren't actually problems on closer inspection
- **Incomplete reasoning** - Suggestions that lack proper justification or context
- **Overlooked areas** - Important parts of the codebase that weren't examined

Example Task tool invocation:

```
Tool: Task
Parameters:
  subagent_type: "general-purpose"
  description: "Critique codebase review"
  prompt: |
    Critique this codebase review. You have access to all tools including Read, Glob, and Grep.

    Review scope: [Full codebase / Focus area: "X"]

    Key files/areas examined in initial review:
    - [list files or areas]

    Initial review output:
    ## Summary
    [paste your complete review summary here]

    ## Findings
    [include all findings from your initial review]

    ## Positive Observations
    [include positive observations]

    Your job is to find what the review missed or got wrong:
    1. Use Glob/Grep to explore the codebase yourself
    2. Read key files to verify findings and check for missed patterns
    3. Look for systemic patterns the initial review may have missed
    4. Verify the severity assessments are appropriate
    5. Check if any findings are false positives
    6. Identify overlooked areas that should have been examined

    Return your critique as:
    - New patterns/issues found (with severity and examples)
    - Severity adjustments needed (with justification)
    - False positives to remove (with reasoning)
    - Overlooked areas to examine
```

The subagent has full access to codebase exploration tools. It should independently verify findings and look for missed patterns.

### Phase 3: Synthesis

Combine the initial review with critique findings into a final output:

1. **Merge findings** - Add any new patterns or issues identified during critique
2. **Remove false positives** - If critique determines a finding isn't actually a problem, remove it entirely
3. **Resolve severity conflicts** - When both agree an issue exists but disagree on severity:
   - Prefer higher severity (err on the side of caution)
   - Note disagreements with context when relevant
4. **Annotate critique contributions** - Mark findings that came from the critique phase with `[Critique]`
5. **Mark severity adjustments** - Note when critique changed severity (e.g., `[Upgraded from Suggestion]`)

#### Deciding on Additional Passes

After synthesis, decide whether another critique pass would add value:

- **Run another pass if:** The critique identified any new patterns, severity upgrades, or false positives
- **Stop if:** The critique only confirmed existing findings without adding new ones

Limit to a maximum of 2 critique passes. Beyond this, additional passes rarely surface new insights and the cost outweighs the benefit.

### Phase 4: Final Output

Format the review clearly using the structure below.

## Output Format

```
## Summary

[2-3 sentence overview of codebase health and key findings]

## Findings

### Architecture & Design
- [Severity] Pattern: Description
  - Examples: file1:line, file2:line
- [Critique] [Severity] Pattern: Description (new pattern found by critique)
  - Examples: file1:line, file2:line
- [Upgraded from Suggestion] [Critical] Pattern: Description (severity changed by critique)
  - Examples: file1:line, file2:line

### Code Health
- [Severity] Pattern: Description
  - Examples: file1:line, file2:line

### Testing Strategy
- [Severity] Pattern: Description
  - Examples: file1:line, file2:line

### Naming & Conventions
- [Severity] Pattern: Description
  - Examples: file1:line, file2:line

### Documentation
- [Severity] Pattern: Description
  - Examples: file1:line, file2:line

### Complexity Patterns
- [Severity] Pattern: Description
  - Examples: file1:line, file2:line

### Style Consistency
- [Severity] Pattern: Description
  - Examples: file1:line, file2:line

### Error Handling & Robustness
- [Severity] Pattern: Description
  - Examples: file1:line, file2:line

## Positive Observations

- Good pattern: Description
  - Examples: file1:line, file2:line
- [Critique] Good pattern: Description (new positive pattern found by critique)
  - Examples: file1:line, file2:line

## Overall Assessment

[High-level assessment of codebase health]

[Key areas for improvement]

[Strengths worth preserving]
```

### Annotation Format

- **Initial findings**: Listed without prefix, e.g., `[Critical] Pattern: Description`
- **Critique findings**: Prefixed with `[Critique]`, e.g., `[Critique] [Suggestion] Pattern: Description`
- **Severity adjustments**: Note when critique changed severity, e.g., `[Upgraded from Suggestion] [Critical] Pattern: Description`

Omit empty categories. Focus on patterns and overall health, not individual line-by-line issues.

## Guidelines

**DO:**
- Focus on patterns across the codebase, not individual issues
- Sample representative files rather than reading everything
- Identify both problems and strengths
- Consider architectural decisions and their impact
- Balance thoroughness with practicality
- Use the Explore agent for initial codebase understanding
- **Use the critique loop** - Always launch a critique subagent to verify findings
- Merge critique findings into the final output with appropriate annotations

**DON'T:**
- Review every single file line-by-line
- Focus on trivial style issues unless they're systemic
- Provide implementation-specific fixes (suggest patterns instead)
- Review like a PR (this isn't about specific changes)
- Skip the exploration phase
- Skip the critique phase (it catches missed patterns and false positives)
- Attempt to critique your own review directly (must use Task tool)

## Example Usage

Full codebase review:
```
/review-codebase
```

Focused review:
```
/review-codebase "API layer"
/review-codebase "tests"
/review-codebase "authentication system"
```

## Reference

Based on [Google's Engineering Practices: Code Review Guidelines](https://google.github.io/eng-practices/review/reviewer/), adapted for codebase-level review rather than change-focused review.
