---
name: feature-research
description: Guide interactive research and POC creation to understand features deeply. This skill should be used when planning to implement a new feature and needing to research design patterns, understand integration points in the codebase, consult documentation via MCP Deep Wiki, or create minimal POCs to validate concepts. Can receive CDC.md from feature-specification as input for clear requirements.
---

# Feature Research Skill

## Purpose

Guide interactive research and understanding of features through conversation, documentation consultation, and selective proof-of-concept (POC) creation. This skill transforms feature ideas into well-understood, documented technical specifications ready for implementation planning.

**Note:** This skill focuses on TECHNICAL research (HOW to implement). For requirement clarification (WHAT to implement), use `feature-specification` first.

## Input

This skill can receive:
- **CDC.md** (from `feature-specification`) - Provides clear, validated requirements to guide research
- **Direct feature request** - If requirements are already clear

When CDC.md exists, use it as the source of truth for requirements and focus research on technical implementation.

## IMPORTANT: User Interaction

**ALWAYS use the `AskUserQuestion` tool when asking clarifying questions.**

```
AskUserQuestion:
  questions:
    - question: "Should we create a POC to validate this approach?"
      header: "POC"
      options:
        - label: "Yes, create POC"
          description: "Validate technical feasibility before proceeding"
        - label: "No, skip POC"
          description: "Documentation is sufficient, proceed to planning"
      multiSelect: false
```

This ensures:
- Clear, structured questions
- User can choose from options or provide custom response
- Conversation stays focused on technical decisions

## When to Use This Skill

Use this skill when:

- CDC.md is ready and technical research is needed
- Starting a new feature implementation with clear requirements
- Researching design patterns or architectural approaches for a feature
- Needing to understand how a feature integrates with existing codebase
- Consulting up-to-date documentation for frameworks, libraries, or APIs
- Validating technical feasibility through minimal POCs
- Gathering information before creating an implementation plan

## Research Workflow

### Phase 1: Understand the Feature Request

1. **Initial Analysis**
   - Read the feature request carefully
   - Identify key requirements and constraints
   - List unknowns and areas requiring research

2. **Interactive Questioning**
   - Ask clarifying questions to the user
   - Understand the "why" behind the feature
   - Identify expected behavior and edge cases
   - Determine acceptance criteria

**Example Questions:**
- What problem does this feature solve?
- Who are the end users of this feature?
- What are the expected inputs and outputs?
- Are there performance or scalability requirements?
- Are there security or compliance considerations?

### Phase 2: Codebase Integration Research

1. **Analyze Existing Architecture**
   - Use Glob to find relevant files and patterns
   - Use Grep to search for similar implementations
   - Use Read to understand integration points
   - Identify existing patterns and conventions

2. **Identify Integration Points**
   - Where does this feature fit in the architecture?
   - What existing components will be affected?
   - What new components need to be created?
   - How will data flow through the system?

**Search Strategy:**
```bash
# Example searches (adapt to your project)
# Find similar features
grep -r "pattern:similar-feature" src/

# Find integration points
glob "**/*Controller.cs"  # For .NET APIs
glob "**/*Service.ts"     # For TypeScript services

# Understand patterns
read important-file.ts
```

### Phase 3: Documentation and Design Pattern Research

1. **Use MCP Deep Wiki for Accurate Documentation**
   - Consult MCP Deep Wiki for framework/library documentation
   - Search for design patterns applicable to your use case
   - Get up-to-date best practices and examples

**When to Use Deep Wiki:**
- Need framework-specific implementation details
- Want to understand API capabilities
- Looking for recommended design patterns
- Need examples of proper usage

**Deep Wiki Usage Tips:**
- Be specific in queries: "How to implement authentication in FastAPI"
- Ask for code examples: "Show example of React useEffect with cleanup"
- Request best practices: "Best practices for error handling in .NET Web APIs"

2. **Research Design Patterns**
   - Identify applicable design patterns (Repository, Factory, Observer, etc.)
   - Understand trade-offs of different approaches
   - Consider patterns used elsewhere in codebase

See `references/deep-wiki-usage.md` for detailed Deep Wiki guidance.

### Phase 4: Proof of Concept (POC) Creation

**When to Create a POC:**
- Technical feasibility is uncertain
- Need to validate a new library or framework
- Testing integration between components
- Exploring performance characteristics
- User wants to see a working prototype

**When NOT to Create a POC:**
- Feature is straightforward with clear implementation path
- Similar features already exist in codebase
- Documentation provides sufficient clarity
- User explicitly doesn't need a POC

**POC Creation Guidelines:**

1. **Keep It Minimal**
   - Focus on the core concept being validated
   - Don't build production-ready code
   - Use hardcoded data when possible
   - Skip error handling and edge cases

2. **Adaptive to Project Context**
   - If working within existing project: Create POC in a temporary branch or file
   - If starting from scratch: Create minimal standalone project
   - Use tools available in current environment (React, .NET, Python, etc.)

3. **POC Structure**
   ```
   poc-feature-name/
   ├── README.md           # What is being tested and why
   ├── main.* (or app.*)   # Entry point
   └── [minimal files]     # Only what's needed
   ```

4. **Document POC Results**
   - What was validated?
   - What was learned?
   - What issues were discovered?
   - Recommendations for production implementation

See `references/poc-guidelines.md` for detailed POC creation guidance.

### Phase 5: Document Findings

Create a findings document that captures all research results.

**Findings Document Structure:**
```markdown
# Feature Research: [Feature Name]

## Overview
Brief description of the feature

## Requirements
- Key requirement 1
- Key requirement 2
- ...

## Design Decisions
### Chosen Approach
Description and rationale

### Alternatives Considered
- Alternative 1: Pros/Cons
- Alternative 2: Pros/Cons

## Integration Points
- Component A: How it integrates
- Component B: How it integrates

## Technical Considerations
- Performance implications
- Security considerations
- Scalability concerns

## Dependencies
- External libraries needed
- Internal components required
- API endpoints to create/modify

## POC Results (if applicable)
- What was tested
- Findings
- Recommendations

## References
- Links to Deep Wiki queries
- Relevant documentation
- Similar implementations in codebase

## Next Steps
- Ready for implementation planning
- Additional research needed (if any)
```

See `references/research-template.md` for a complete template.

## Iterative Research Process

Research is iterative. The workflow above may repeat multiple times:

1. **Ask Questions** → **Get Answers** → **Refine Understanding**
2. **Research Docs** → **Find Patterns** → **Adjust Approach**
3. **Build POC** → **Learn from Results** → **Revise Design**

**Don't Rush:** Take time to understand the feature thoroughly. A well-researched feature is faster to implement and has fewer issues.

## Output

The output of this skill is a comprehensive findings document (`findings.md` or `research-notes.md`) that contains:

- Clear understanding of the feature requirements
- Documented design decisions with rationale
- Identified integration points in codebase
- Technical considerations and dependencies
- POC results (if created)
- References to documentation and research
- Clear next steps for implementation planning

This document becomes the input for the `implementation-planner` skill.

## Tips for Effective Research

1. **Ask Before Assuming** - Clarify ambiguities with the user early
2. **Search Before Creating** - Check if similar features exist
3. **Document As You Go** - Capture findings in real-time
4. **Be Thorough** - Better to over-research than under-research
5. **Validate Uncertainty** - Use POCs for technical validation
6. **Think About Integration** - Consider how the feature fits into the system
7. **Use Deep Wiki** - Leverage up-to-date documentation
8. **Communicate** - Keep the user informed throughout the research process

## Example Usage

```
User: "I want to add email notifications when a form is submitted"

Claude (using feature-research skill):
1. "Let me research this feature. A few questions first:
   - Should emails be sent immediately or queued?
   - Are there specific email templates to use?
   - Should we use an external service (SendGrid, etc.) or SMTP?"

2. [Searches codebase for existing email functionality]

3. [Consults Deep Wiki: "How to implement background job queues in .NET"]

4. "I found that we're using Hangfire for background jobs.
   I recommend queuing emails using Hangfire for reliability.
   Should I create a small POC to validate the Microsoft Graph integration?"

5. [Creates minimal POC if user agrees]

6. [Documents findings in findings.md with design decisions,
   integration points, and recommendations]

7. "Research complete! I've documented the approach in findings.md.
   Ready to create the implementation plan?"
```

## Bundled Resources

- `references/research-template.md` - Template for findings document
- `references/deep-wiki-usage.md` - Guide for using MCP Deep Wiki effectively
- `references/poc-guidelines.md` - Detailed POC creation guidelines
