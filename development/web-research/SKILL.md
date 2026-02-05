---
name: web-research
description: Multi-round web search with low-frequency query generation. Prioritize GitHub/StackOverflow for actionable code, extract AI Overview insights, and perform deep link analysis. Use proactively for complex problems requiring external knowledge or when stuck on implementation challenges.
allowed-tools: WebSearch, Read
---

# Web Research

Apex2's sophisticated multi-round search pipeline implemented as a Claude Code skill. Focuses on finding actionable solutions through strategic web research.

## Instructions

When invoked, perform systematic multi-round web research using low-frequency, highly specific queries:

### 1. Query Generation Strategy
Create targeted, low-frequency search terms that find exact solutions:

**Principles for effective queries:**
- Include specific error messages verbatim (in quotes)
- Combine technology stack + specific problem
- Use version numbers when relevant
- Include "GitHub" or "StackOverflow" keywords
- Add "fix", "solution", "how to", "example"
- Avoid overly generic terms

**Query patterns:**
- `"exact error message" technology-name fix`
- `"library-name" "specific problem" GitHub issue`
- `how to "specific task" in "framework-name" "version"`
- `"function-name" "parameter-problem" "programming-language"`

### 2. Multi-Round Search Process
Execute up to 3 research rounds, refining based on findings:

**Round 1: Direct Problem Solution**
- Search for the exact issue
- Prioritize GitHub issues, StackOverflow answers
- Look for minimal working examples

**Round 2: Alternative Approaches** 
- If Round 1 doesn't yield solutions, search for:
  - Alternative libraries/methods
  - Workarounds and migrations
  - Similar but not identical problems

**Round 3: Deep Context**
- Search for underlying concepts
- Advanced techniques and patterns
- Production deployment considerations

### 3. Source Prioritization
Prioritize sources based on actionability:

**Tier 1: Most Actionable**
- GitHub issues with pull requests/commits
- StackOverflow answers with code examples  
- Official documentation with examples

**Tier 2: High Value**
- Developer blogs with working code
- Tutorial repositories with examples
- Conference presentations with code

**Tier 3: Contextual**
- General documentation pages
- Academic papers (for concepts, not code)
- Vendor product pages

### 4. Google AI Overview Extraction
When Google AI Overview appears in results:
- Extract the synthesized answer first (often most relevant)
- Use Overview as a starting point for deeper exploration
- Follow Overview's suggested links for verification
- Note Overview's confidence indicators

### 5. Deep Link Analysis
For the top 3 most promising links per query:
- Extract key code snippets exactly as shown
- Identify the solution's core approach
- Note prerequisites and dependencies
- Check for compatibility with current environment
- Look for alternative solutions suggested in comments

### 6. Quality Control
Filter out irrelevant results:
- Exclude Terminal Bench mentions (avoid circular references)
- Skip generic tutorials that don't solve specific problems
- Avoid solutions for different technology stacks
- Discount outdated versions (unless applicable)

## Research Categories and Strategies

### Error Recovery Research
- Search exact error messages in quotes
- Look for GitHub issues with resolved problems
- StackOverflow posts with similar stack traces
- Include environment details in queries

### Implementation Guidance  
- Search "how to X in Y" patterns
- Look for GitHub repos with similar functionality
- Find StackOverflow examples with code snippets
- Target specific library combination problems

### Framework Migration
- Search "alternative to X" or "X vs Y"
- Look for migration guides and tools
- Find compatibility matrix information
- Research breaking changes and solutions

### Performance Issues
- Search "X slow performance" + optimization
- Look for profiling tools and techniques
- Research benchmark comparisons
- Find best practices for the specific use case

## Analysis Process

1. Generate 3-5 targeted search queries for Round 1
2. Use WebSearch with specific queries
3. Read top 5-7 results per query
4. Extract actionable code and concepts
5. Determine if additional rounds needed
6. Refine queries based on Round 1 findings
7. Execute Round 2 with adjusted focus
8. Repeat for Round 3 if complex problem persists
9. Synthesize across all rounds

## Output Format

Provide structured research summary:

```
Research Questions:
  Primary: [main problem being solved]
  Secondary: [related issues]

Round 1 Results:
  Query 1: "[search query]"
    Best sources: [list of most helpful links]
    Key solution: [extracted solution]
    Code example: [working code snippet]
  
  Query 2: "[search query]"
    [same structure]

Round 2 Results: (if needed)
  Alternative approaches found
  Workarounds identified
  Related problems solved

Round 3 Results: (if needed)
  Deeper understanding gained
  Advanced techniques discovered

Synthesized Solution:
  Primary Approach: [step-by-step solution]
  Alternative 1: [backup option]
  Alternative 2: [another option]

Implementation Details:
  Required packages: [dependencies]
  Prerequisites: [setup needed]
  Compatibility notes: [version/environment]

Risk Assessment:
  Reliability: [confidence in solution]
  Complexity: [implementation difficulty]
  Side effects: [potential issues]

Recommended Next Steps:
  1. [immediate action]
  2. [follow-up action]
  3. [validation step]
```

## When to Use

This research skill shines when:
- Encountering unfamiliar frameworks or problems
- Stuck on specific error messages
- Needing to compare multiple approaches
- Looking for best practices beyond documentation
- Searching for real-world working examples
- Complex problems requiring research from multiple angles

The goal is to find actionable, tested solutions rather than generic tutorials, with emphasis on code that can be directly applied to solve the specific problem at hand.
