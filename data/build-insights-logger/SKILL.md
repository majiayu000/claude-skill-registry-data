---
name: build-insights-logger
description: Automatically log meaningful insights, discoveries, and decisions during coding sessions. Capture non-trivial learnings about edge cases, design decisions, patterns, and implementation details. Activate when building complex code where institutional knowledge should be preserved. Log to .claude/insights/ and help transfer key learnings to CLAUDE.md.
---

# Build Insights Logger

## Overview

Maintain a running log of meaningful insights, discoveries, and decisions made during coding sessions. Capture non-trivial learnings about requirements, edge cases, design considerations, implementation details, and coding patterns that emerge during development.

**Target outcome**: Preserve institutional knowledge and track the evolution of the codebase by logging insights to session files in `.claude/insights/`, then selectively transferring valuable learnings to CLAUDE.md.

## When to Use This Skill

Activate automatically when:
- Working on complex implementations with non-trivial design decisions
- Discovering edge cases or unexpected behaviors
- Making architectural or performance trade-offs
- Implementing security-sensitive features
- Building features where institutional knowledge matters

Do not activate for:
- Simple bug fixes or trivial changes
- Routine refactoring without architectural impact
- Syntax corrections or typos

## File Structure & Session Management

### Directory Structure
```
.claude/
└── insights/
    ├── session-YYYY-MM-DD-HHMMSS.md (current session)
    └── archive/
        └── session-YYYY-MM-DD-HHMMSS.md (archived sessions)
```

### Session File Naming
- **Current session**: `session-YYYY-MM-DD-HHMMSS.md`
- **Format**: Use timestamp in `YYYY-MM-DD-HHMMSS` format
- **Location**: `.claude/insights/` for active sessions
- **Archive location**: `.claude/insights/archive/` for completed sessions

### Session Creation
- Create new session file when first insight is logged in a new Claude Code session
- One file per Claude Code session
- Each session file is independent - no cross-session merging

### Session File Format
Each session file contains insights in markdown format with this structure:
```markdown
# Insights Session: YYYY-MM-DD HH:MM:SS

### [Category]: [Brief Title]
Files: `path/to/file.ts`, `another/file.ts`
Tags: #tag1 #tag2 #tag3
YYYY-MM-DD HH:MM:SS

[Clear, concise description of the insight]

[Optional: Brief code snippet if essential - max 3-5 lines]

---

### [Next insight...]
```

## Logging Insights Workflow

### When to Log Insights

**Automatic logging triggers** (Claude decides these are insight-worthy):
- Discovery of non-trivial edge cases
- New requirements emerging during implementation
- Design decisions and their rationale
- Performance considerations or optimizations
- Security implications discovered
- Dependency choices and trade-offs
- Architectural patterns adopted
- Testing strategies implemented
- Error handling approaches
- API design decisions
- State management patterns
- Data validation rules

**Explicit user requests**:
- User says "log this insight", "remember this", or "capture this learning"
- User asks to note specific discoveries
- User highlights something for future reference

### What NOT to Log
- Trivial or obvious details (e.g., "created a new file")
- Standard boilerplate code
- Common language features
- Syntax corrections or typos
- Routine refactoring without architectural impact
- Self-evident code comments

### Logging Process

**Step 1: Identify the insight**
- Evaluate whether the discovery/decision meets insight criteria
- When in doubt, log it (user can filter during review)

**Step 2: Create or open session file**
- If no session file exists for current session, create `.claude/insights/session-YYYY-MM-DD-HHMMSS.md`
- If session file exists, open it for appending

**Step 3: Format the insight**
Use this template:
```markdown
### [Category]: [Brief Title]
Files: `path/to/file.ts`, `another/file.ts`
Tags: #tag1 #tag2 #tag3
YYYY-MM-DD HH:MM:SS

[Clear, concise description of the insight]

[Optional: Brief code snippet if essential - max 3-5 lines]
```

**Category examples**:
- Architecture, Edge Cases, Performance, Testing, Security
- Dependencies, Patterns, API Design, State Management
- Error Handling, Data Flow, Validation

**Tag guidelines**:
- Use lowercase with hyphens: `#error-handling`, `#api-design`
- 2-4 tags per insight
- Common tags: `#performance`, `#security`, `#edge-cases`, `#patterns`, `#testing`, `#api`, `#architecture`

**Description guidelines**:
- **Clear and concise**: Get to the point quickly
- **Explain WHY**: Why is this valuable? What problem does it solve?
- **Context**: What led to this discovery?
- **Action taken**: What decision was made?
- **1-3 paragraphs maximum**

**Code snippet rules** (optional):
- Only include if essential to understanding
- Maximum 3-5 lines
- Add comments to highlight key points
- Label "good" vs "bad" when comparing approaches
- Prefer conceptual explanation over code

**Step 4: Append to session file**
- Add insight to the end of the session file
- Separate insights with `---` divider

**Step 5: Notify user**
- Show brief notification: `📝 Logged insight about [topic]`
- Keep it one line - don't show full insight content
- Example: `📝 Logged insight about null handling in API responses`

### Logging Frequency
- Add insights progressively as discovered
- Don't wait until end of session
- Multiple insights per session is expected and encouraged

## Review & Selection Workflow

### Initiating Review
- **User-initiated only**: User asks "review insights", "show me what we learned", "summarize insights"
- **No automatic suggestions**: Do not proactively suggest reviewing

### Review Process

**Step 1: Consolidation**
- Read current session insights file from `.claude/insights/session-*.md`
- Identify related or redundant insights
- Consolidate similar insights into cohesive entries
- Refine wording for clarity

**Step 2: Present insights**
Present in this format:
```
Based on this session, here are the key insights captured:

**[Category Group]**

1/ Insight: [Brief title]
   Files: [file paths]
   Explanation: [Why this matters and what was learned]

2/ Insight: [Brief title]
   Files: [file paths]
   Explanation: [Why this matters and what was learned]

**[Another Category Group]**

3/ Insight: [Brief title]
   Files: [file paths]
   Explanation: [Why this matters and what was learned]

Which insights would you like to add to CLAUDE.md? Reply with numbers (e.g., "1, 3" or "all").
```

**Presentation guidelines**:
- Number each insight (1/, 2/, 3/, etc.)
- Group by category when helpful
- Include brief explanation of value for each
- Keep explanations concise (1-2 sentences)

**Step 3: User selection**
- User responds with numbers: "1, 3" or "1,2,3" or "all" or "none"
- Parse user's selection

**Step 4: Add to CLAUDE.md**
- Read existing CLAUDE.md (or create if doesn't exist)
- Add selected insights under appropriate section
- Format appropriately for CLAUDE.md context
- Create new section if needed (e.g., "## Insights & Learnings")
- Confirm what was added to user

**Step 5: Archive session file**
- After adding insights to CLAUDE.md, move session file to archive
- Move from `.claude/insights/session-*.md` to `.claude/insights/archive/session-*.md`
- Create archive directory if it doesn't exist
- Confirm archiving to user

### No Insights Scenario
If user asks to review and no insights were logged:
- Respond: "No insights were captured in this session yet."
- Don't create empty session files

### Multiple Review Requests
- User can request review multiple times per session
- Show all insights logged so far
- If some were previously added to CLAUDE.md, indicate which ones

### CLAUDE.md Doesn't Exist
- If CLAUDE.md doesn't exist, create it when adding insights
- Use standard structure with appropriate sections
- Add insights under "## Insights & Learnings" section

## Archiving & Cleanup

### Automatic Archiving
- **Trigger**: After user selects insights and they're added to CLAUDE.md
- **Action**: Move session file from `.claude/insights/` to `.claude/insights/archive/`
- **Naming**: Keep original filename (e.g., `session-2025-11-17-143022.md`)
- **Directory creation**: Create `.claude/insights/archive/` if it doesn't exist

### Manual Deletion Option
User can request deletion instead of archiving:
- **Trigger phrases**: "delete the insights log", "clear insights instead of archiving", "remove insights file"
- **Confirmation**: Ask for confirmation before deleting
- **Action**: Delete the session file completely instead of archiving

### Cleanup Commands
- "archive current session" - move to archive
- "delete current session" - delete completely (with confirmation)
- "clean up old archives" - user specifies which archived files to remove

## Quality Guidelines

### Insight Quality Criteria
1. **Non-trivial**: Adds genuine value to understanding the codebase
2. **Actionable**: Contains information useful for future development
3. **Specific**: Tied to concrete decisions or discoveries, not generic advice
4. **Contextual**: Explains why this matters for this specific project

### When in Doubt
- **Better to log**: If uncertain whether something is insight-worthy, log it
- **User can filter**: During review, user decides what's valuable for CLAUDE.md
- **Better too many than too few**: Session log is temporary; missing insights are lost

### Writing Style
- **Concise**: Shorter entries are better
- **Clear**: Use plain language, avoid jargon unless necessary
- **Focused**: One insight per entry, don't combine unrelated learnings
- **Practical**: Focus on practical implications, not theoretical concepts

### Category Selection
- Choose specific, descriptive categories
- Create new categories when existing ones don't fit
- Avoid generic categories like "General" or "Miscellaneous"
- Categories should help organize related insights

### Tag Selection
- Use 2-4 tags per insight
- Tags should aid searchability and filtering
- Use consistent tag names (check existing tags in file first)
- Prefer specific tags over broad ones

## Edge Cases & Special Scenarios

### Session File Already Exists
- If timestamp collision (unlikely), append a letter: `session-2025-11-17-143022-a.md`
- Log warning about timestamp collision

### Archive Directory Doesn't Exist
- Create `.claude/insights/archive/` directory when first archiving
- Don't error if it doesn't exist

### Empty Session
- Don't create session file until first insight is logged
- If no insights logged, no file created

### Long Sessions with Many Insights
- No limit on insights per session
- File can grow as large as needed
- Consolidate during review to prevent overwhelming user

## Example Insight Entry

```markdown
### Edge Case: Null handling in API responses
Files: `api/users.ts`, `types/user.ts`
Tags: #api #edge-cases #error-handling
2025-11-17 14:30:22

Discovered that third-party user API can return null for email field even though documentation states it's required. Added validation layer with fallback to 'no-email@placeholder.com' for system processes to prevent downstream crashes.

// Good approach
const email = userData.email ?? 'no-email@placeholder.com';

// Avoid - will crash downstream
const email = userData.email; // assumes always present
```
