---
name: github-issue-creator
description: "Creates comprehensive GitHub issues that serve as source of truth for changes. Use when user asks to create a GitHub issue for a bug fix, feature, update, or any other change. Captures all research, analysis, and implementation context for the next developer."
---

# GitHub Issue Creator

## Purpose

This skill helps create detailed, comprehensive GitHub issues that serve as the **source of truth** for all changes to the codebase. When you've completed research, bug investigation, or feature planning, this skill ensures that all your findings, analysis, and implementation context are captured in a GitHub issue.

## Core Principle: Write for the Next Developer

**CRITICAL**: You are writing this issue for another AI developer (or human developer) who will implement the changes. They won't have access to:
- The conversation we just had
- The research you just performed
- The code analysis you just completed
- The decisions and tradeoffs you just considered

**Your job**: Transfer ALL of that knowledge into the issue so they can successfully implement the changes without having to redo your research.

## When to Use This Skill

Activate this skill when the user explicitly asks you to:
- "Create a GitHub issue for this"
- "Add this to GitHub"
- "Document this as an issue"
- "Create an issue for this bug/feature/fix"
- Any variation of requesting a GitHub issue be created

## Guiding Principles

### 1. Benefit from Your Research
Don't just describe WHAT needs to be done. Include:
- **Why** you chose this approach over alternatives
- **What** you discovered during investigation
- **How** existing code patterns informed your decision
- **Where** the relevant code lives (specific file paths and line numbers)
- **What** edge cases or gotchas you identified

### 2. Provide Complete Context
Include everything the next developer needs:
- Background on the problem/feature
- Current state of the system
- Related code/files with specific references (e.g., `src/app/profile/page.tsx:123`)
- Dependencies or prerequisites
- Testing considerations
- Potential risks or concerns

### 3. Be Specific and Actionable
- Reference specific files and line numbers
- Include code snippets showing current vs. desired state
- Link to related issues, PRs, or documentation
- Explain technical decisions with rationale
- Provide enough detail that implementation can begin immediately

### 4. Structure for Clarity
While you have flexibility in structure, organize information logically:
- Start with clear problem statement or feature description
- Provide necessary background and context
- Include research findings and analysis
- Present implementation approach with specific details
- Call out testing requirements and acceptance criteria
- Note any risks, dependencies, or open questions

### 5. ⚠️ MANDATORY: User Integration Section
**CRITICAL - DO NOT SKIP**: Every GitHub issue MUST include a "User Integration" section that traces how users will trigger and experience this feature end-to-end.

This section should answer:
- **Entry point**: How does the user trigger this? (UI button, chat message, CLI command, API call, automated pipeline, etc.)
- **User flow**: Step-by-step from trigger to outcome — what the user does and what they see/receive at each step
- **Feedback**: How does the user know it worked? (Response message, notification, visual change, etc.)
- **Error cases**: What happens when something goes wrong? What does the user see?

**If EVERY user-facing interface is already wired up** (i.e., no new entry points or interactions needed), mark the section as:
```markdown
## User Integration

**No Changes** — All user-facing interfaces already exist. This issue involves [backend/internal] changes only.
```

**⚠️ IMPORTANT**: If this feature adds a new capability (create, update, delete, search, etc.), verify that EVERY interface the user interacts with can access it. A backend capability without a user entry point is incomplete. Common interfaces to check:
- Web/mobile UI (buttons, forms, screens)
- Chat/conversational interfaces (tool definitions, system prompts)
- CLI commands
- API endpoints (if the API is user-facing)
- Automated pipelines (if user-triggered)

### 6. ⚠️ MANDATORY: Proposed Data Model Changes Section
**CRITICAL - DO NOT SKIP**: Every GitHub issue MUST include a "Proposed Data Model Changes" section. This enables the Database Auditor to automatically analyze risks before implementation begins.

**Format:**
```markdown
## Proposed Data Model Changes

### Change Type
- [ ] New table(s)
- [ ] Modified existing table(s)
- [ ] Removed table(s) or column(s)
- [ ] No database changes

### Tables Affected
List each table that will be created, modified, or removed.

**Table:** [table_name]
**Action:** [create | modify | remove]
**Changes:**
- Column: [column_name], Type: [data_type], Nullable: [yes/no], Default: [value]
- [additional columns...]

### Relationships
Describe foreign key relationships to existing tables.

### Migration Strategy
- [ ] Additive only (no breaking changes)
- [ ] Requires data backfill
- [ ] Requires deployment coordination
- [ ] Requires downtime

### Additional Context
[Any other relevant information about the data model changes]
```

**If there are NO database changes**, mark the section as:
```markdown
## Proposed Data Model Changes

### Change Type
- [x] No database changes

This issue involves frontend/UI changes only with no database modifications.
```

**Why This Matters:**
- The Database Auditor GitHub Action automatically triggers when issues contain this section
- Catches breaking changes, migration risks, and tenant isolation issues BEFORE code is written
- Creates a forcing function to think through data implications upfront
- Documents intent - the issue becomes a record of WHY schema changes were made

### 7. ⚠️ MANDATORY: Test-Driven Development (TDD) Requirement
**CRITICAL - DO NOT SKIP**: Every GitHub issue for features, bug fixes, or refactoring MUST include a prominent TDD workflow section.

**From project CLAUDE.md**:
> **`test-driven-development` skill**: MUST BE USED when implementing ANY feature or bugfix. ALWAYS invoke BEFORE writing implementation code. Write test first, watch it fail, then write minimal code to pass. **NEVER skip this - if you write code before tests, delete it and start over.**

**Required in EVERY issue**:
1. **Explicit TDD invocation reminder** at the top of the issue
2. **Phase-by-phase TDD workflow** showing RED-GREEN-REFACTOR cycle
3. **Test-first implementation steps** for each component/feature
4. **Reference to `test-driven-development` skill** that must be invoked

**Format**:
```markdown
## ⚠️ CRITICAL: Test-Driven Development Required

**BEFORE implementing ANY phase of this issue:**

1. **Invoke the `test-driven-development` skill**
2. **Write tests FIRST** (before any implementation code)
3. **Watch tests FAIL** (red phase)
4. **Write minimal code** to make tests pass (green phase)
5. **Refactor** while keeping tests green

### TDD Workflow for This Issue

[Phase-by-phase breakdown showing TDD cycle for each component]
```

This section is NON-NEGOTIABLE and must appear prominently in every issue for code changes.

## Flexible Structure Examples

The structure should match the issue type and context (bug fix, new feature, refactoring, performance). Read the detailed templates for each issue type in `references/templates-and-checklist.md`

## Workflow

When user asks you to create a GitHub issue:

### Step 1: Gather Context
- Review the conversation to capture all relevant research and analysis
- Identify key decisions, tradeoffs, and technical findings
- Note specific file references, code patterns, and implementation details
- Consider what the next developer absolutely needs to know

### Step 2: Assess Complexity

Before drafting, determine whether this is a **single issue** or an **epic with phased issues**.

**Single issue** — when ALL of these are true:
- Touches 1-3 files
- One logical concern (bug fix, small feature, refactor)
- Can be completed in a single branch and PR
- No database migrations required, OR only trivial additive changes

**Epic with phases** — when ANY of these are true:
- Touches 4+ files across multiple modules
- Multiple logical concerns (e.g., schema + processing + API + integration)
- Requires database migrations that other work depends on
- Has natural dependency ordering (Phase 2 can't start until Phase 1 is done)
- Would benefit from parallel work streams

If **single issue**, proceed to Step 3a. If **epic**, proceed to Step 3b.

### Step 3a: Draft a Single Issue
Write a comprehensive issue following these principles:
- **Title**: Clear, specific, action-oriented (e.g., "Fix network page performance issue with profile fetching" not "Network page slow")
- **Body**: Well-structured markdown with all context and details
- **TDD Section**: MANDATORY - Include prominent TDD workflow section (see Guiding Principle #7)
- **Code References**: Use format `file_path:line_number` for easy navigation
- **Links**: Include relevant URLs, PRs, issues, documentation
- **Formatting**: Use markdown effectively (headings, lists, code blocks, emphasis)

Read the TDD section template, epic template, and phase issue requirements in `references/templates-and-checklist.md`

Then proceed to Step 4.

### Step 3b: Draft an Epic with Phase Issues

When complexity warrants it, create a **master epic issue** plus **one issue per phase**. The `test-driven-development` skill's Epic & Phased Workflow section defines the structure — follow it precisely.

1. Draft the epic issue (title prefixed with "Epic: ", label `epic`, phase table, dependency graph, architecture decisions, file-level conflict analysis, success criteria)
2. Draft each phase issue (self-contained, references parent epic, explicit dependencies, all mandatory sections)
3. Present all drafts for approval
4. Create issues in dependency order, then update epic with phase issue numbers

Read the detailed epic template and phase issue requirements in `references/templates-and-checklist.md`

Then proceed to Step 5.

### Step 4: Show for Approval
Present the drafted issue(s) to the user in a readable format:
```markdown
# I've drafted this GitHub issue:

**Title**: [Issue Title]

**Body**:
[Full issue markdown content]

---
Would you like me to create this issue in GitHub?
```

For epics, present the epic and all phase issues, clearly separated.

### Step 5: Detect Repository Info
When user approves, automatically detect:
- Repository owner from git remote (e.g., "MattVOLTA")
- Repository name from git remote (e.g., "builders")
- Use `git remote get-url origin` to extract this information

### Step 6: Create Issue(s) via GitHub CLI
Use `gh issue create` with:
- `--title`: The issue title
- `--body`: The complete markdown body
- `--label`: Add `epic` label for epic issues

For epics: create the epic first, then phase issues, then update the epic with phase issue numbers.

### Step 7: Return Success
After creation, provide the user with:
- Success confirmation
- Direct link to the created issue(s)
- Issue number(s) for reference

For single issues:
```
Issue created successfully!

Issue #123: Fix network page performance issue with profile fetching
https://github.com/owner/repo/issues/123
```

For epics:
```
Epic and phase issues created successfully!

Epic #100: RAG Knowledge System
  Phase 1 #101: Database & Storage Foundation
  Phase 2 #102: Document Processing Pipeline
  Phase 3 #103: Chat Agent Integration

https://github.com/owner/repo/issues/100
```

## Error Handling

If issue creation fails:
1. Show the error message to the user
2. Offer to save the drafted content locally as backup
3. Suggest troubleshooting steps (check permissions, network, etc.)
4. Keep the drafted content available for retry

## Quality Checklist

Before showing the drafted issue(s), verify all mandatory sections are included and the issue is comprehensive enough for another developer to implement without redoing your research.

Read the full quality checklist (single issues and epic-specific) in `references/templates-and-checklist.md`

**Key mandatory sections for every issue:**
- User Integration section (or "No Changes")
- Proposed Data Model Changes section (or "No database changes")
- TDD workflow section with `test-driven-development` skill reference
- Specific file references with paths/line numbers
- WHY (rationale) not just WHAT (tasks)

## Remember

- **Your research has value** - don't let it disappear after this conversation
- **Be thorough, not brief** - the next developer will thank you for details
- **Specific is better than general** - file paths beat vague descriptions
- **Show your work** - explain how you arrived at conclusions
- **Think like a teacher** - you're transferring knowledge to someone who wasn't here

The goal is that another developer can pick up this issue and successfully implement the changes because you've given them everything they need.
