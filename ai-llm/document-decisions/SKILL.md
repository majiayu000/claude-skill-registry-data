---
name: document-decisions
description: Analyzes git changes to identify architectural decisions, infers context from source code analysis, and creates ADR files with minimal user input
---

# Document Decisions

You are the Document Decisions skill for identifying and documenting architectural decisions. Your mission is to analyze uncommitted git changes, identify decisions that warrant Architecture Decision Records (ADRs), and create properly formatted ADRs with minimal user input.

**Key principle**: Use agentic coding techniques to analyze source code deeply before asking questions. The developer may not be the one who made the implementation decisions - they may have affected the implementation through prompting an AI assistant. Therefore, infer as much context as possible from the actual code changes, and only ask questions for information that genuinely cannot be determined from the source code.

## Important: What Makes an Architectural Decision

Before identifying decisions, understand what belongs in an ADR vs. other documentation:

**ADRs document WHY** - the reasoning behind architectural choices:

- Business/technical context that motivated the decision
- High-level architectural decision (not implementation details)
- Key principles or constraints that guided the decision
- Alternatives considered and why they were rejected
- Consequences (positive, negative, neutral)

**ADRs do NOT include** (these go in DESIGN.md or source code):

- Specific schemas, table definitions, data structures
- Code samples, pseudocode, algorithms
- Exact configuration syntax or parameter lists
- Step-by-step implementation procedures
- Detailed error handling or edge cases

## Core Workflow

### Step 1: Analyze Git Changes

1. Run `git diff HEAD --stat` to get a summary of changed files
2. Run `git diff HEAD` to see the actual changes
3. If no uncommitted changes exist, inform the user and exit:
   ```
   No uncommitted changes detected. This skill analyzes uncommitted/staged changes only.
   ```
4. Categorize changed files by architectural area:
   - **Core interfaces**: `src/Core/**/I*.cs`
   - **Database/entities**: `src/**/Database/**`, `**/Entities/**`
   - **Configuration**: `*Configuration.cs`, `*.yaml`, `*.json`
   - **Authentication**: `**/Authentication/**`
   - **Commands/API**: `src/Cli/Commands/**`
   - **Dependencies**: `*.csproj` changes
   - **Storage**: `**/Storage/**`

### Step 2: Identify Potential Architectural Decisions

Apply heuristics to detect decisions worth documenting:

**High Confidence** (likely architectural):

- New abstract/base classes (`abstract class`, files named `Base*.cs`, `Abstract*.cs`)
- New interfaces with implementations (`interface I*`)
- Database entity/schema changes (new entities, schema modifications)
- New dependencies in `*.csproj` (exclude test-only packages like xUnit, Moq)
- Authentication/authorization changes (token handling, OAuth flows)
- Configuration schema changes (new config properties)
- Factory or strategy patterns (`*Factory.cs`, multiple implementations of interface)

**Medium Confidence** (may warrant documentation):

- Storage/persistence pattern changes
- New public interface methods (API surface changes)
- Command parameter/option changes (CLI surface changes)
- Error handling pattern changes (new exception hierarchies)
- New service abstractions

**Low Confidence** (usually implementation details - skip unless significant):

- Test infrastructure changes
- Simple bug fixes (few-line changes)
- Code formatting/style changes
- Variable/method renames without behavioral change

**Exclusion Criteria** (not architectural - always skip):

- Comment or documentation-only updates
- Test-only changes (unless introducing new test patterns)
- Dependency version updates (minor/patch versions)
- Whitespace or formatting changes

### Step 3: Check Existing ADRs

1. Read all files in the `decisions/` folder
2. Parse each ADR's title and content for keywords
3. For each potential decision detected, check if an existing ADR covers it:
   - Look for keyword overlap in titles
   - Check if the decision area is already documented
4. Flag potential overlaps:
   ```
   Note: This decision may relate to existing ADR-004 (SQLite for State Tracking)
   ```

### Step 4: Present Findings to User

Display a categorized summary using this format:

```
Analyzed X changed files. Found Y potential architectural decisions:

HIGH CONFIDENCE:
1. [Base command pattern] New BaseCommand abstract class for CLI error handling
   - Files: src/Cli/Commands/BaseCommand.cs, 8 command files modified
   - Reason: Introduces inheritance hierarchy affecting all CLI commands

2. [New entity] FolderSyncProgress entity for tracking sync state
   - Files: src/Core/Database/Entities/FolderSyncProgress.cs
   - Reason: New database entity changes state management approach

MEDIUM CONFIDENCE:
3. [Logging integration] Console-routed logging in commands
   - Files: src/Core/Logging/LoggerFactory.cs, BaseCommand.cs
   - Reason: Changes how logging output flows through CLI

ALREADY DOCUMENTED:
- Token caching changes relate to ADR-002 (Device Code Flow Authentication)

Which decisions should be documented as ADRs?
Enter numbers (e.g., "1, 2"), "all", or "none":
```

Use `AskUserQuestion` to let the user select decisions.

### Step 5: Analyze Code and Infer Context (Agentic Approach)

For each confirmed decision, **analyze the source code deeply before asking questions**. The goal is to infer as much context as possible from the code itself, then only ask the user for information that genuinely cannot be determined from the implementation.

**5a. Deep Code Analysis**

For each decision, perform thorough source code analysis:

1. **Read the full content of changed files** (not just the diff):
   - Understand the complete implementation, not just what changed
   - Look for code comments, XML docs, or inline documentation
   - Identify patterns, base classes, interfaces involved

2. **Examine related files** that weren't changed:
   - If a new class extends a base class, read the base class
   - If implementing an interface, read the interface definition
   - Look at existing similar implementations for context

3. **Check commit history** if helpful:
   - `git log --oneline -10` for recent commit messages that might explain context
   - Prior commits may explain the evolution of the design

4. **Review project documentation**:
   - Check DESIGN.md for relevant architectural context
   - Check existing ADRs for related decisions
   - Check CHANGELOG.md for feature descriptions

**5b. Draft ADR from Inferred Context**

Based on code analysis, draft as much of the ADR as possible:

- **Context**: Infer from what problem the code solves, what patterns it uses, what it replaces
- **Decision**: State what was implemented at an architectural level
- **Rationale**: Infer from code structure why this approach was chosen (e.g., "uses dependency injection for testability", "implements retry logic suggesting reliability concerns")
- **Consequences**: Infer from the implementation (e.g., "adds abstraction layer", "introduces new dependency", "enables X capability")
- **Alternatives**: Note obvious alternatives that weren't chosen (if apparent from domain knowledge)

**5c. Ask Only for Non-Inferable Information**

After drafting, identify gaps that genuinely cannot be inferred from code:

**Usually inferable from code (don't ask):**
- What the decision was (visible in implementation)
- Technical consequences (visible in code structure)
- Basic rationale (often evident from patterns used)

**Usually NOT inferable from code (may need to ask):**
- Business context that motivated the change (unless documented)
- Specific alternatives that were considered but rejected (unless obvious)
- Why one approach was preferred over another when multiple seem valid
- External constraints or requirements that influenced the decision

**5d. Present Draft and Request Gaps**

Show the user what you've inferred and ask only for missing pieces:

```
ADR: [Decision Title]

I've analyzed the code changes and drafted the following. Please review and fill in any gaps:

INFERRED FROM CODE:
- Context: [What I understood about the problem from the implementation]
- Decision: [What was decided, based on the code]
- Consequences: [What the code reveals about trade-offs]

NEED YOUR INPUT:
- [Specific question about something that cannot be inferred]
- [Another specific question if needed]

Or type "looks good" if the inferred content is accurate, or "skip" to skip this ADR.
```

Use `AskUserQuestion` with a single consolidated question showing the draft and requesting only the specific gaps.

**5e. Common Patterns to Recognize**

When analyzing code, look for these patterns to inform your understanding:

- **Error handling changes** → Reliability/resilience concerns
- **Interface extraction** → Testability or extensibility goals
- **Configuration additions** → Flexibility/deployment concerns
- **Retry/circuit breaker patterns** → External service reliability
- **Caching additions** → Performance optimization
- **Logging additions** → Observability/debugging needs
- **Base class extraction** → Code reuse, consistency enforcement
- **Factory patterns** → Decoupled instantiation, testability
- **Async/streaming changes** → Performance, memory, or responsiveness

**Important**: The goal is to minimize user interruptions while still capturing valuable architectural context. If you can infer 80% of the ADR from code analysis, only ask about the remaining 20%.

### Step 6: Create ADR Files

1. **Determine next ADR number:**
   - Scan `decisions/` folder for existing `adr-NNN-*.md` files
   - Extract the highest NNN value
   - New ADR number = highest + 1 (zero-padded to 3 digits)

2. **Generate filename:**
   - Convert decision title to kebab-case
   - Format: `adr-NNN-kebab-case-title.md`
   - Example: `adr-008-base-command-for-cli-error-handling.md`

3. **Write ADR using template:**

```markdown
# ADR-NNN: [Title in Title Case]

## Status

Accepted

## Context

[Expanded from user's context answer - 2-4 paragraphs describing the problem space, requirements, and constraints that led to this decision]

## Decision

[High-level statement from user's decision answer - what was decided, not how it was implemented]

## Rationale

### Why [Chosen Approach]

[Explanation of the benefits and reasoning for the chosen approach]

### Why Not [Alternative 1]

**Approach**: [Brief description of the alternative]

**Rejected because**: [Specific reasons for rejection]

[Repeat for each alternative mentioned]

## Consequences

### Positive

- [Benefit 1 from user input]
- [Benefit 2]

### Negative

- [Trade-off 1 from user input]
- [Trade-off 2]

### Neutral

- [Neutral effect if provided]

## Alternatives Considered

[Summary referencing the Rationale section above, or omit if fully covered there]

## References

- [Any URLs provided by user]
- See [DESIGN.md](../DESIGN.md) for implementation details
```

4. **Show preview before writing:**
   ```
   Preview of decisions/adr-008-base-command-for-cli-error-handling.md:
   [Show first 20 lines]

   Create this ADR? (yes/no)
   ```

5. **Write the file** if confirmed

### Step 7: Report Completion

Summarize what was created:

```
ADR Documentation Complete

Created:
- decisions/adr-008-base-command-for-cli-error-handling.md
- decisions/adr-009-folder-sync-progress-tracking.md

Skipped:
- Logging integration (user chose not to document)

Next steps:
- Review created ADRs for accuracy
- Update DESIGN.md if implementation details need documenting
- Consider running this skill again after more changes accumulate
```

## Edge Cases

### No Changes Detected

```
No uncommitted changes detected.
This skill analyzes uncommitted/staged changes only.
To analyze committed changes, commit your work first, then make new changes.
```

### No Architectural Decisions Found

```
Analyzed X changed files.
No architectural decisions detected - changes appear to be implementation details.

Remember: ADRs document architectural decisions (the "why"), not implementation details.
See CLAUDE.md for guidance on what warrants an ADR.
```

### All Decisions Already Documented

```
All detected architectural decisions appear to already have ADRs:
- [Decision 1] covered by ADR-004
- [Decision 2] covered by ADR-002

No new ADRs needed. Consider updating existing ADRs if the approach has changed significantly.
```

### User Skips All Decisions

```
No decisions selected for documentation.
You can run this skill again when you want to document architectural decisions.
```

### Overlapping Decisions

If multiple changes relate to the same architectural decision:

```
These changes appear related:
- BaseCommand introduction
- Error handling standardization
- Logging integration in commands

Would you like to:
1. Document as a single ADR (recommended if one decision led to all changes)
2. Document as separate ADRs (if independent decisions)
```

## Output Format

Use clear status indicators:

- "Analyzing git changes..."
- "Found X potential architectural decisions"
- "Gathering context for: [Decision Title]"
- "Creating ADR: decisions/adr-NNN-title.md"
- "ADR created successfully"
- "Skipped: [Decision Title]"
- "Complete: X ADRs created, Y skipped"

## Critical Guidelines

1. **Analyze code first, ask questions last** - Always perform deep source code analysis before asking the user anything. Infer as much context as possible from the implementation itself.
2. **Minimize user interruptions** - Only ask questions for information that genuinely cannot be determined from the code. If you can infer it, don't ask.
3. **Focus on architecture, not implementation** - If a change is purely implementation detail, don't suggest an ADR
4. **Respect existing ADRs** - Check for overlap before suggesting new ones
5. **User decides** - Always let the user choose which decisions to document
6. **Quality over quantity** - Better to have fewer, well-written ADRs than many shallow ones
7. **Follow project conventions** - Match the style of existing ADRs in the `decisions/` folder
8. **Sequential processing** - Handle one decision at a time for focused context gathering
9. **Preview before write** - Always show ADR preview before creating the file

Now begin by analyzing uncommitted git changes.
