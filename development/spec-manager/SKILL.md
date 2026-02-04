---
name: spec-manager
description: |
  MANDATORY specification writing skill. ONLY way to create/update specs.

  Auto-invoke when:
  - Creating specs: New projects, features ("I want to create XX")
  - Updating specs: Feature additions, requirement changes, architecture updates
  - Syncing specs: Major code changes (3+ files), refactoring, session end
  - Keywords: specifications/spec/design/architecture/requirements/PRD

  Outputs to .spec-manager/. Critical rules and workflow details in skill body.
---

# spec-manager Skill

This skill writes and displays the application's specification documents. It is used before implementation, before adding new features, or when design changes are made, to update the documents and notify users.

## 🚨 Critical Rules

**NEVER write spec/design/architecture documents to ANY location except `.spec-manager/`**

- NEVER create `docs/`, `specifications/`, `design/` directories for spec content before `.spec-manager/` exists
- NEVER write PRD.md, TechStack.md, design docs, architecture docs to any location except `.spec-manager/`
- ALWAYS invoke this skill FIRST for ANY specification-related documentation
- Other documentation (README, API reference, user guides) allowed ONLY AFTER `.spec-manager/` is complete

**Auto-invoke triggers (expanded):**

- Writing spec/design/architecture/requirements documents (any directory, any filename)
- Creating PRD, tech spec, design doc, architecture doc (any location)
- User creation requests ("I want to create XX" with/without URL)
- Starting implementation of new features
- Completing significant changes (3+ files modified)
- Major refactoring or architectural changes
- Keywords: specifications/spec/specification/design/architecture/requirements/PRD/document
- Session end with specification changes

## Standard Workflow

**0. FIRST:** Verify `.spec-manager/` exists and is current. If not, run this skill before any other documentation.

**1. Delegate to specialized skills (if available):**

- Check if specialized planning skills exist
- Record TODO to return to spec-manager after planning
- Delegate planning to specialized skill
- Return here to write specification documents

**2. Interactive clarification (if requirements unclear):**

- Use `AskUserQuestion` tool with numbered options
- Ask one question at a time
- Build specifications incrementally

**3. Write/update specifications:**

- Write to `.spec-manager/` directory ONLY via this skill
- Notify user of updates

**4. AFTER step 3:** Other documentation (README, etc.) can be created if needed

**Question format:** Always provide numbered options (1, 2, 3..., 1-1, 1-2,...) when asking specification questions.

## Dual Purpose: Specification Writing AND Requirements Clarification

This skill serves two primary functions:

### 1. Delegating to Specialized Planning Skills (Priority)

**When to delegate**: If other specialized skills for planning specifications are available in the system (e.g., `langgraph-master`, `business-panel`, domain-specific planning skills), delegate the planning process to them first.

**Workflow**:

1. Detect that specifications need to be created or updated
2. Check if specialized planning skills are available
3. If available:
   - **Record a TODO** using `TodoWrite` to return to `spec-manager` skill after planning completes
   - Example TODO: "Return to spec-manager to write specification documents after planning"
   - Invoke the appropriate specialized skill for planning
4. Wait for planning completion (the TODO ensures we don't forget to return)
5. Return to this skill to write the specification documents based on the planning output
6. Mark the TODO as completed
7. Update `.spec-manager/` directory with the specifications

**Example**: If planning a LangGraph application, delegate to `langgraph-master` skill for architectural planning, then return here to write the formal specification documents.

### 2. Interactive Requirements Clarification (When No Specialized Skills)

**When to use**: If no specialized planning skills are available, OR if the user's requirements are unclear or ambiguous even after initial analysis.

**Workflow**:

1. Detect that specifications are unclear or incomplete
2. Automatically invoke this skill's interactive questioning mode
3. Use `AskUserQuestion` tool to ask **one question at a time**
4. Provide **clear options** for users to select from (when possible)
5. Build specifications incrementally based on user's answers
6. After gathering sufficient information, synthesize and confirm with user
7. Write the specification documents to `.spec-manager/` directory

**Example**: User says "I want to create a web app" without details → This skill automatically starts asking:

- "What type of web application?" [E-commerce, Blog, Dashboard, Social network]
- "Who are the target users?" [General public, Business users, Internal team]
- Continue with technical stack, features, architecture, etc.

See the **"Clarifying Unclear Specifications"** section below for detailed questioning methodology.

## Proactive Usage Guidelines

**IMPORTANT**: This skill should be invoked **automatically and proactively** by Claude without waiting for explicit user requests.

### How to Invoke Proactively

When conditions are met, Claude should:

1. **Detect the trigger condition** (e.g., completed 5 file changes for new auth feature)
2. **Automatically invoke this skill** without asking for permission first
3. **Update specification documents** in `.spec-manager/` directory
4. **Notify the user** with a summary like:
   ```
   📝 Specification documents have been automatically updated:
   - PRD.md: Added authentication feature requirements
   - TechStack.md: Updated with JWT library dependencies
   - FileStructure.md: Reflected new auth/ directory structure
   ```

### What NOT to Do

❌ **Don't wait** for explicit `/update-spec` command after every change
❌ **Don't ask** "Should I update the specifications?" - just do it proactively
❌ **Don't ignore** completed implementations - always sync specifications
❌ **Don't skip** specification updates when user is focused on coding

### Integration with Development Workflow

```
Development Flow:
1. User requests feature → Invoke spec-manager (initialize/review specs)
2. Implement feature → Track changes
3. Complete implementation → Invoke spec-manager (auto-update specs)
4. Mark task complete → Specifications already synchronized ✅
```

### Clarifying Unclear Specifications

When the user's requirements or specifications are unclear or incomplete, use an **interactive questioning approach** to systematically gather information:

#### Process for Specification Clarification

1. **Identify Gaps**: Determine what information is missing or ambiguous

   - Product requirements unclear?
   - Technical stack not specified?
   - User flows undefined?
   - Architecture decisions needed?

2. **Ask One Question at a Time**: Use the `AskUserQuestion` tool to gather information progressively

   - **DO NOT** ask multiple complex questions simultaneously
   - Focus on one aspect at a time for clarity
   - Provide concrete options when possible

3. **Provide Clear Options**: Give users specific choices to select from

   - Example options for architecture: "Monolith", "Microservices", "Serverless"
   - Example options for database: "PostgreSQL", "MongoDB", "SQLite"
   - Always include descriptions explaining each option's trade-offs

4. **Build Incrementally**: Use each answer to inform the next question

   - Start with high-level decisions (purpose, target users, core features)
   - Move to technical choices (stack, architecture, database)
   - Finally address implementation details (deployment, testing, monitoring)

5. **Synthesize and Confirm**: After gathering information, summarize and confirm
   - Present the collected requirements back to the user
   - Ask for confirmation before writing specification documents
   - Allow the user to correct or refine any points

#### Example Question Flow

```
Question 1: "What is the primary purpose of this application?"
Options: ["E-commerce platform", "Content management system", "Data analytics dashboard", "Social network"]

↓ User selects "E-commerce platform"

Question 2: "Who are the target users?"
Options: ["B2C consumers", "B2B businesses", "Internal company use", "Multi-tenant SaaS"]

↓ User selects "B2C consumers"

Question 3: "What are the core features needed for launch?"
Options: [Allow multiple selections: "Product catalog", "Shopping cart", "Payment processing", "User accounts", "Order tracking"]

↓ Continue building specification incrementally
```

#### Best Practices for Questions

- **Be Specific**: Ask about concrete decisions, not abstract concepts
- **Offer Context**: Explain why you're asking and how it affects the design
- **Limit Options**: Provide 2-4 options per question for manageability
- **Allow "Other"**: The `AskUserQuestion` tool automatically provides an "Other" option
- **Track Progress**: Keep track of what has been clarified and what remains unclear
- **Document Decisions**: Record the user's answers in the appropriate specification files

#### When to Use This Approach

- ✅ User says "I want to create XX" without detailed requirements
- ✅ Reference URLs are vague or incomplete
- ✅ Project is in early conceptual stage
- ✅ User is unsure about technical decisions
- ✅ Multiple valid approaches exist and user preference is needed

## Working with Reference URLs

When users provide URLs as references for specification writing, follow these comprehensive analysis guidelines:

### For Documentation Sites

When the URL points to official documentation, tutorials, or technical guides:

1. **Read the Main Page Thoroughly**

   - Extract key concepts, features, and requirements
   - Identify the overall structure and purpose

2. **Explore Subsections and Subpages**

   - Navigate through all relevant subsections linked from the main page
   - Check navigation menus, sidebars, and "Related Pages" sections
   - Read "Getting Started", "Architecture", "Best Practices" sections if available
   - Don't miss important details in nested pages

3. **Synthesize Information**
   - Integrate information from all subsections into a coherent specification
   - Ensure consistency across different parts of the documentation
   - Capture both high-level concepts and implementation details

### For AI Conversation Pages (ChatGPT, Claude, etc.)

When the URL points to an AI conversation or chat transcript:

1. **Read the Entire Conversation**

   - Start from the beginning, not just the latest messages
   - Understand the context and evolution of ideas
   - Track how requirements or designs changed throughout the discussion

2. **Identify the Final Conclusion**

   - Look for the most recent, refined version of requirements or designs
   - Earlier ideas may have been revised or rejected - focus on what was ultimately decided
   - Pay attention to phrases like "final version", "let's go with", "decided to", "conclusion"

3. **Extract Actionable Specifications**

   - Base your specification documents on the **final conclusions**, not intermediate ideas
   - If conflicting information exists, prioritize the most recent decisions
   - Include reasoning behind key decisions if mentioned in the conversation

4. **Respect the Context**
   - Understand why certain decisions were made during the conversation
   - Capture important constraints or requirements that influenced the final design
   - Note any explicit user preferences or requirements stated in the conversation

### General Best Practices

- **Use WebFetch Tool**: Always use the WebFetch tool to access and analyze URLs
- **Be Thorough**: Don't rush - comprehensive analysis leads to better specifications
- **Ask for Clarification**: If the reference material is ambiguous or contradictory, ask the user
- **Document Sources**: Note which parts of the specification came from the reference URLs

## Specification Content Guidelines

### Minimize Source Code in Specifications

**IMPORTANT**: Specification documents should focus on design, architecture, and requirements - NOT implementation details.

#### What to Include (✅)

- **Interfaces and Type Definitions**: Only the public API contracts

  ```typescript
  interface UserService {
    authenticate(credentials: Credentials): Promise<AuthResult>;
    getUserProfile(userId: string): Promise<UserProfile>;
  }
  ```

- **Data Types and Schemas**: Essential data structure definitions

  ```typescript
  type User = {
    id: string;
    name: string;
    email: string;
    role: "admin" | "user";
  };
  ```

- **API Contracts**: Endpoint definitions, request/response formats
- **Configuration Schemas**: Environment variables, config file structures

#### What to Avoid (❌)

- **Implementation Code**: Full function bodies, business logic, algorithms
- **Helper Functions**: Utility functions and internal implementation details
- **Repetitive Code Examples**: Multiple similar examples of the same pattern
- **Long Code Blocks**: Any code snippet longer than 10-15 lines

#### Best Practices

- **Focus on "What" not "How"**: Describe what the system does, not how it's implemented
- **Use Diagrams Over Code**: Prefer flowcharts, architecture diagrams, and sequence diagrams
- **Reference Files Instead**: Point to actual source files rather than duplicating code
  - Example: "See `src/auth/UserService.ts` for implementation details"
- **Keep Examples Minimal**: If code examples are necessary, show only the essential structure

## Location for Saving Specifications and order for writing

Specification documents are saved in the `.spec-manager` directory at the project root.

The following documents are stored (Do not change the following file names):

1. .spec-manager/PRD.md: _Required_ Product Requirements Document
2. .spec-manager/TechStack.md: _Required_ Description of the technologies used
3. Write these in parallel:
   - .spec-manager/AppFlow.md: _Required_ Application screen transition and flow diagrams
   - .spec-manager/FileStructure.md: Directory structure (excluding `.claude`, `node_modules`, etc.)
   - .spec-manager/BackendStructure.md: (If applicable) Design principles and guidelines for the backend, such as DB and Storage structures
   - .spec-manager/FrontendGuidelines.md: (If applicable) Design principles and guidelines for the frontend
   - .spec-manager/DevInstructions.md: Rules file. A natural language document describing the conventions and development rules that should be followed by the AI agents in this project.

You can write other specification documents as needed, but **the documents listed above are mandatory**.

So if those files do not exist, please create them first.
