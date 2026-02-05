---
name: dev-swarm-code-development
description: Complete backlog implementation in feature-driven development. Read backlog requirements, reference implemented features, design approach, implement code, and document. Use when implementing features, changes, bug fixes, or improvements.
---

# AI Builder - Code Development

This skill implements backlogs through a structured feature-driven approach. As a Software Engineer expert, you'll read backlog requirements, reference existing features, design implementation approach, write code, and create comprehensive documentation for the features knowledge base.

## When to Use This Skill

- User asks to implement a backlog
- User requests to complete a feature, change, bug fix, or improvement
- User says "develop backlog X"
- User wants to implement work from sprint
- User asks to code a specific backlog item

## Prerequisites

This skill requires:
- `04-prd/` - Product Requirements Document (business requirements and acceptance criteria)
- `07-tech-specs/` - Engineering standards and constraints
- `09-sprints/` folder with active sprint and backlogs
- `features/` folder with features-index.md (existing features knowledge base)
- Understanding of the backlog type: FEATURE, CHANGE, BUG, or IMPROVE

## Feature-Driven Development Workflow

**CRITICAL:** This skill follows a strict feature-driven approach where `feature-name` is the index for the entire project:

**For Each Backlog:**
1. Read `backlog` from `09-sprints/SPRINT-XX-descriptive-name/[BACKLOG_TYPE]-XX-[feature-name]-<sub-feature>.md`
2. Extract the `feature-name` from the backlog file name
3. Read `features/features-index.md` to find the feature file
4. Read feature documentation in this order:
   - `features/[feature-name].md` - Feature definition (WHAT/WHY/SCOPE)
   - `features/flows/[feature-name].md` - User flows and process flows (if exists)
   - `features/contracts/[feature-name].md` - API/data contracts (if exists)
   - `features/impl/[feature-name].md` - Implementation notes (if exists)
5. Locate source code at `src/` using `features/impl/[feature-name].md`
6. Implement the code following `07-tech-specs/`
7. Update `backlog` with development notes

This approach ensures AI developers can work on large projects without reading all code at once.

## Your Roles in This Skill

See `dev-swarm/docs/general-dev-stage-rule.md` for role selection guidance.

## Role Communication

See `dev-swarm/docs/general-dev-stage-rule.md` for the required role announcement format.

## Instructions

Follow these steps in order for coding development:

### Step 0: Verify Prerequisites and Gather Context

**IMPORTANT:** Follow this exact order to efficiently locate all relevant context:

1. **Identify the backlog:**
   - User specifies which backlog to work on
   - Or you select next backlog from `09-sprints/` in order

   ```
   09-sprints/
   └── SPRINT-XX-descriptive-name/
       └── [BACKLOG_TYPE]-XX-[feature-name]-<sub-feature>.md
   ```
   - Locate the sprint README at `09-sprints/SPRINT-XX-descriptive-name/README.md` for required progress log updates

2. **Read the backlog file:**
   - Understand task description and requirements
   - Note backlog type (FEATURE/CHANGE/BUG/IMPROVE)
   - **Extract the `feature-name`** from the file name (CRITICAL)
   - Verify `Feature Name` in backlog metadata matches the file name
   - If they do not match, stop and ask the user to confirm the correct feature name
   - Review test plan requirements
   - Identify acceptance criteria

3. **Read source code structure standards:**
   - Read `dev-swarm/docs/source-code-structure.md` for general guidelines
   - Note file naming conventions and directory structure

4. **Read PRD and tech specs:**
   - Read `04-prd/` (all markdown files) - Product requirements and acceptance criteria for the feature
   - Read `07-tech-specs/` (all markdown files) - Technical specifications and engineering standards
   - Understand the business context and technical constraints

5. **Read feature documentation (using feature-name as index):**
   - Read `features/features-index.md` to confirm feature exists
   - Read `features/[feature-name].md` - Feature definition (WHAT/WHY/SCOPE)
   - Read `features/flows/[feature-name].md` - User flows (if exists)
   - Read `features/contracts/[feature-name].md` - API contracts (if exists)
   - Read `features/impl/[feature-name].md` - Implementation notes (if exists)

6. **Locate existing source code:**
   - Use `features/impl/[feature-name].md` to find code locations
   - Navigate to `src/` directory
   - Review existing code structure and patterns
   - Identify files to modify (CHANGE/BUG/IMPROVE) or create (FEATURE)

7. **Understand codebase patterns:**
   - Review existing code in `src/` using locations from `features/impl/[feature-name].md`
   - Note architectural patterns and integration points

**DO NOT** read the entire codebase. Use `features/impl/[feature-name].md` to find only relevant files in `src/`.

### Step 1: Design the Implementation

Before writing code, create the feature design document:

1. Create/Update file `features/{feature-name}.md`
   - If backlog type is `feature` and the related feature file is not exist, create new feature file
   - If backlog type is `change/bug/improve` or the feature file is exist, update existing feature file
   - Use the provided templates for consistency
2. Create/update `flow` and `contract` files if it is needed

   - `features/flows/{feature-name}.md` - User flows and process flows (when needed)
   - `features/contracts/{feature-name}.md` - API contracts and interfaces (when needed)

3. Present design to user for approval
   - Show the feature design document
   - Explain approach and rationale
   - Highlight any assumptions or decisions
   - Wait for user confirmation before proceeding

### Step 2: Implement the Code (After User Confirms)

Once user approves the design:

1. **Organize code in src/:**
   - Follow `dev-swarm/docs/source-code-structure.md` for file organization guidelines
   - Place code in appropriate locations within `src/`
   - Use file naming conventions defined in source-code-structure.md

2. **Write the code:**
   - Implement according to the approved design
   - Follow coding standards
   - Write clean, modular, maintainable code
   - Include appropriate error handling
   - Avoid over-engineering (keep it simple)

3. **Code quality guidelines:**
   - **Modular**: Break code into small, focused functions/components
   - **Readable**: Clear variable names, self-documenting code
   - **Simple**: Don't add features not in requirements
   - **Consistent**: Match style of existing codebase
   - **Secure**: No XSS, SQL injection, command injection, or OWASP vulnerabilities
   - **Tested**: Code should be testable per backlog test plan

3. **What NOT to do:**
   - Don't add extra features beyond requirements
   - Don't over-abstract or create unnecessary helpers
   - Don't add comments to code you didn't change
   - Don't refactor code outside scope of backlog
   - Don't add hypothetical error handling
   - Don't create backwards-compatibility hacks

4. **For different backlog types:**

   **Feature (new functionality):**
   - Create new files/components
   - Integrate with existing system
   - Follow established patterns

   **Change (modify existing feature):**
   - Update existing code
   - Maintain compatibility where needed
   - Update related code if necessary

   **Bug (fix defect):**
   - Fix the specific issue
   - Avoid changing unrelated code
   - Verify fix matches test plan

   **Improve (optimize existing code):**
   - Refactor/optimize as specified
   - Maintain same functionality
   - Document performance improvements

### Step 3: Create Implementation Documentation

After code is complete, create implementation documentation:

1. Create `features/impl/{feature-name}.md`

   **Files Changed:**
   - List all files created or modified
   - For each file, note key changes
   - Use file paths, function names as keywords (NOT line numbers)

   **Implementation Details:**
   - Describe how the feature was implemented
   - Key functions/components created
   - Integration points with other features
   - Any important implementation decisions

   **Code Structure:**
   - Directory organization
   - Module/component breakdown
   - Dependencies added

   **Key Functions/APIs:**
   - List important functions with descriptions
   - Document key API endpoints
   - Note important classes/components

   **Reference for Developers:**
   - Quick keywords for code search
   - How to find relevant code
   - Common use patterns

2. Update `features/{feature-name}.md` if needed
   - Add any insights discovered during implementation
   - Note if actual implementation differs from design (explain why)
   - Keep it synchronized with current code

3. Update `features/features-index.md` if needed

4. **Update or create `src/README.md` (Project Documentation):**
   - **IMPORTANT**: Developers should maintain project documentation in `src/README.md`, NOT in the root README.md
   - Add or update feature documentation:
     - Feature overview and purpose
     - Installation and setup instructions
     - Usage examples and API documentation
     - Configuration options
     - Troubleshooting tips
   - Keep `src/README.md` as the primary technical reference for developers
   - Include links to `features/` documentation for detailed specs

### Step 4: Verify Against Test Plan

Before marking complete:

1. **Review backlog test plan:**
   - Ensure code meets all test requirements
   - Verify acceptance criteria are met

2. **Self-test (if possible):**
   - Run the code
   - Test key functionality
   - Verify no obvious errors

3. **Document test status:**
   - Note if manual testing was done
   - List any test results
   - Flag anything needing QA attention

### Step 5: Update Backlog with Development Notes

**CRITICAL:** Update the backlog.md file to track development progress:

1. **Update backlog status:**
   - Change status from "Not Started" to "In Code Review"
   - Add a "Development Notes" section if not present

2. **Document development findings:**
   - **Files Created/Modified:** List all files changed with brief descriptions
   - **Implementation Approach:** Summarize how requirements were implemented
   - **Key Decisions:** Note any important technical decisions made
   - **Integration Points:** Document how code integrates with other features
   - **Known Issues:** Flag any potential issues for code review
   - **Test Notes:** Any preliminary testing done during development

3. **Reference documentation created:**
   - Link to `features/[feature-name].md`
   - Link to `features/impl/[feature-name].md`
   - Link to source code files in `src/` (locations documented in features/impl/[feature-name].md)

4. **Notify user:**
   - Summarize what was implemented
   - Reference documentation created
   - Note any important decisions or tradeoffs
   - Suggest next step: "Ready for code review"

5. **Update sprint README (README.md) (CRITICAL):**
   - Update backlog status in the sprint backlog table
   - Append a log entry in the sprint progress log for the Development step

**These backlog.md and sprint README updates create the audit trail for code review and testing phases.**

## Expected File Structure

```
project-root/
├── 09-sprints/
│   └── SPRINT-XX-descriptive-name/
│       └── [BACKLOG_TYPE]-XX-[feature-name]-<sub-feature>.md # Backlog entry point
│
├── features/                                # Features knowledge base
│   ├── features-index.md                   # Index of all features
│   ├── [feature-name].md                   # Feature definition (WHAT/WHY/SCOPE)
│   ├── flows/
│   │   └── [feature-name].md               # User flows (if needed)
│   ├── contracts/
│   │   └── [feature-name].md               # API contracts (if needed)
│   └── impl/
│       └── [feature-name].md               # Implementation notes (code locations)
│
└── src/                                     # Source code
    ├── README.md                            # Project documentation (maintained by developers)
    └── [organized per dev-swarm/docs/source-code-structure.md guidelines]
```

## File Templates

1. `features-index.md`
   
```markdown
# Features Index

- [feature name a](feature-name-a.md)
- [feature name b](feature-name-b.md)
```

2. **feature.md**
```markdown
# Title

## Description

[The overview for this feature's implementation, for approval, codeo review, trouble shooting or further development]

## References
The details of this feature's implementation

* [flow](flows/feature-name.md)
* [contract](contracts/feature-name.md)
* [Implement](impl/feature-name.md)
```

3. `flows/feature-name.md` - help to understand the code logic
   - User flow diagrams (mermaid)
   - Process flows and sequence diagrams
   - State transitions
   - Integration flows

4. `contracts/feature-name.md` - the interface between services, pacakges, workflows
   - REST API used or endpoint definitions
   - Request/response schemas
   - Data models and database schemas
   - Event contracts

5. `impl/feature-name.md` - help to find the code location in the source code file for codeo review, trouble shooting or further development
   - searchable keywords - function name, class name, even comment text in the file
   - file path
   - Dependencies and integration details
   - Avoid citing line numbers in the code file as any code change will affect the line numbers
