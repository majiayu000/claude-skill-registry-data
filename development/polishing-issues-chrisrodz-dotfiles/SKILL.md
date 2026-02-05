---
name: polishing-issues
description: Use when GitHub issue lacks scope, has ambiguities, or needs technical definition - researches codebase, identifies gaps, presents options with recommendations, updates issue description (project, gitignored)
---

# Polishing GitHub Issues

## Overview

Transform vague/incomplete GitHub issues into well-scoped, actionable tasks. Works across any tech stack by researching codebase, identifying ambiguities, presenting ALL options with pros/cons, and appending polished description after user confirmation.

## When to Use

- User provides GitHub issue URL needing clarification
- Issue lacks technical details, acceptance criteria, or testing plan
- Multiple implementation approaches possible
- Need to scope out work before starting

**When NOT to use:**

- Issue already well-defined with clear acceptance criteria
- Simple typo fixes or trivial changes
- User just wants to read the issue (not polish it)

## Workflow

### 1. Fetch Issue

```bash
gh issue view <number> --repo <owner/repo> --json title,body,labels,state
```

Extract: title, description, labels, comments for context

### 2. Research Phase

**Conditional based on issue type:**

**Feature requests:**

- Use Explore agent to find related components/files
- Grep for similar patterns/implementations
- Check project structure (routing, state management, etc)

**Bug reports:**

- Find files mentioned in stacktraces/error messages
- Search for related error handling
- Check test coverage in affected areas

**Documentation:**

- Review existing docs structure
- Check for related documentation files

**If frameworks/libraries mentioned:**

- Use web research specialist subagent for discovery
- Check version-specific APIs/patterns

### 3. Analysis

Identify gaps:

- [ ] Missing clear UI/UX definition?
- [ ] Missing technical details?
- [ ] Multiple valid approaches?
- [ ] Unclear requirements?
- [ ] Missing context about existing code?
- [ ] Acceptance criteria absent?
- [ ] No testing strategy?

### 4. Present Findings to User

**MANDATORY STOP POINT - DO NOT PROCEED WITHOUT USER INPUT**

Show in message:

```
## Issue Analysis: [Issue Title]

### Problem Statement
[Concise description of what needs to be done]

### Technical Context
**Related Files:**
- [file.ts:123](path/to/file.ts#L123) - Current implementation
- [component.tsx:45](path/to/component.tsx#L45) - Related component

OR

**Files to Create:**
- `src/features/new-feature/component.tsx` - Main component
- `src/lib/validation.ts` - Add validation schema

### User Story
As [user type]
I want [action]
So that [benefit]

### Ambiguities & Options
[Only if ambiguities exist]

**Option 1: [Approach Name]**
- Pro: [benefit]
- Pro: [benefit]
- Con: [drawback]

**Option 2: [Approach Name]**
- Pro: [benefit]
- Con: [drawback]

**Option 3: [Approach Name]** [if applicable]
- Pro: [benefit]
- Con: [drawback]

### Acceptance Criteria
- [ ] [Specific testable outcome]
- [ ] [Specific testable outcome]

### Testing Plan
- Unit tests: [What to test]
- Integration tests: [What to test]
- Manual testing: [Steps to verify]
```

**Then ask:** "Which option should I use for the polished description?" (if ambiguities exist)

### 5. Wait for User Decision

**IRON LAW: NEVER proceed without explicit user choice on ambiguities**

User must select option OR provide alternative direction

### 6. Generate Polished Description

Based on user's choice, create concise markdown to **APPEND** (not replace):

```markdown
---

## Polished Scope

**Problem:** [1-2 sentence summary]

**User Story:**
As [user] I want [action] so that [benefit]

**Implementation:**

- Modify: [file.ts:123](path#L123) - [description]
- Create: `path/to/new-file.ts` - [description]

**Acceptance Criteria:**

- [ ] [Testable outcome]
- [ ] [Testable outcome]

**Testing:**

- Unit: [What to test]
  - Focus on adding a small amount of high value tests that ensure functionality is sound
  - Avoid adding tests for library code, focus on the project's core business logic

**Technical Notes:**
[Dependencies, constraints, edge cases]
```

**Style rules:**

- Use bullet points, not prose
- Link files with markdown: `[file.ts:123](path#L123)`
- Use checkboxes for criteria
- No fluff or unnecessary words

### 7. Show Preview

Present EXACT content that will be appended:

```
Will append this to existing issue description:

---
[generated content]
---

Confirm to update issue? (yes/no)
```

### 8. Get Confirmation

**IRON LAW: NEVER update without explicit "yes"/"confirm"/"looks good"**

If user says no/wants changes: Go back to step 6

### 9. Update Issue

Append to existing description:

```bash
# Fetch current body
CURRENT_BODY=$(gh issue view <number> --repo <owner/repo> --json body -q .body)

# Append polished content
gh issue edit <number> --repo <owner/repo> --body "$CURRENT_BODY

---

[polished content here]"
```

Confirm success, provide issue URL

## Common Mistakes

| Mistake                               | Why Wrong                     | Do Instead                                     |
| ------------------------------------- | ----------------------------- | ---------------------------------------------- |
| Update without confirmation           | User may disagree             | Always preview, wait for explicit yes          |
| Skip ambiguity presentation           | User needs informed decision  | List ALL options with pros/cons                |
| Only show 1-2 options when more exist | Hides valid alternatives      | Show all reasonable approaches                 |
| Replace description instead of append | Loses original context        | Always append with `---` separator             |
| Choose option automatically           | Assumes user priorities       | Present options, let user decide               |
| Search only one area                  | May miss context              | Search broadly: components, utils, tests, docs |
| Not checking framework docs           | May suggest outdated patterns | WebSearch official docs for latest             |
| Verbose descriptions                  | Wastes time                   | Sacrifice grammar for conciseness              |
| Forget file links                     | Makes navigation harder       | Always use markdown links with line numbers    |
| Skip user story                       | Missing user perspective      | Always include As/I want/So that               |
| No testing plan                       | Incomplete scope              | Always specify unit/integration/manual tests   |

## Red Flags - Stop & Ask User

🚩 **Multiple equally valid approaches** → Present ALL options, don't choose
🚩 **Breaking changes required** → Explicitly call out impact, get approval
🚩 **Missing critical context** (env vars, services) → Ask before proceeding
🚩 **Conflicting project conventions** → Present conflict, ask clarification
🚩 **Issue already well-scoped** → Confirm user wants re-polish or just review
🚩 **More than 3 options** → Group similar approaches or ask user to narrow scope

## Examples

### Example 1: Feature Request

**Before (vague):**

```
Title: Add dark mode
Body: Users want dark mode
```

**After research, present to user:**

```
## Issue Analysis: Add dark mode

### Problem Statement
App needs dark mode toggle with persistent state across sessions

### Technical Context
**Related Files:**
- [Layout.astro:15](src/layouts/Layout.astro#L15) - Main layout, add toggle here
- [global.css:1](src/styles/global.css#L1) - Root CSS vars for theming

**Files to Create:**
- `src/components/ThemeToggle.tsx` - Toggle button component
- `src/lib/theme.ts` - Theme state management

### User Story
As user
I want toggle dark/light mode
So that I can read comfortably in any lighting

### Ambiguities & Options

**Option 1: CSS variables + localStorage**
- Pro: Lightweight, no dependencies
- Pro: Fast, no JS framework needed
- Con: Manual theme variable setup

**Option 2: Theme library (next-themes, etc)**
- Pro: Handles edge cases automatically
- Pro: System preference detection built-in
- Con: Additional dependency
- Con: May conflict with existing CSS

**Option 3: Astro view transitions API**
- Pro: Native Astro integration
- Pro: Smooth transitions between themes
- Con: Requires Astro 3.0+
- Con: More complex setup

### Acceptance Criteria
- [ ] Theme toggle visible in nav
- [ ] Preference persists across sessions
- [ ] Respects system preference on first visit
- [ ] All components support both themes

### Testing Plan
- Unit: Theme state management, localStorage persistence
- Integration: Toggle updates all components correctly
- Manual: Verify all pages render correctly in both modes

Which option should I use?
```

**After user chooses Option 1, show preview:**

```
Will append this to existing issue description:

---

## Polished Scope

**Problem:** App needs dark mode toggle with persistent state

**User Story:**
As user I want toggle dark/light mode so that I can read comfortably in any lighting

**Implementation:**
- Modify: [Layout.astro:15](src/layouts/Layout.astro#L15) - Add ThemeToggle component to nav
- Modify: [global.css:1](src/styles/global.css#L1) - Add CSS custom properties for dark theme
- Create: `src/components/ThemeToggle.tsx` - Toggle button with icon
- Create: `src/lib/theme.ts` - localStorage + system preference detection

**Acceptance Criteria:**
- [ ] Theme toggle visible in nav on all pages
- [ ] Preference persists via localStorage
- [ ] Respects system preference on first visit (prefers-color-scheme)
- [ ] All components styled with CSS vars (no hardcoded colors)
- [ ] Smooth transition between themes
- [ ] Works without JavaScript (defaults to light)

**Testing:**
- Unit: theme.ts state management, localStorage read/write
- Integration: Toggle updates :root CSS vars, all components re-render
- Manual: Test on all pages, verify system preference detection, check localStorage persistence

**Technical Notes:**
- Use CSS custom properties exclusively (never hardcode colors)
- Detect system preference: `window.matchMedia('(prefers-color-scheme: dark)')`
- Store in localStorage key: `theme` (values: "light" | "dark" | "auto")
- Add <script> tag in Layout head to prevent FOUC

---

Confirm to update issue? (yes/no)
```

### Example 2: Bug Report

**Before (incomplete):**

```
Title: Form validation broken
Body: When I submit the contact form, validation doesn't work
```

**After research, present to user:**

```
## Issue Analysis: Form validation broken

### Problem Statement
Contact form allows submission without validation, no error messages shown

### Technical Context
**Related Files:**
- [ContactForm.tsx:45](src/components/ContactForm.tsx#L45) - Form component, validation missing
- [validation.ts:10](src/lib/validation.ts#L10) - Zod schemas defined but not used
- [api/contact.ts:20](src/pages/api/contact.ts#L20) - API endpoint lacks server-side validation

**Existing Patterns:**
Project uses Zod for validation (see validation.ts), but ContactForm not using it

### User Story
As user
I want see validation errors when form invalid
So that I know what to fix before submitting

### Ambiguities & Options

**Option 1: Client-side only (Zod + form state)**
- Pro: Instant feedback, no network delay
- Pro: Reuses existing Zod schemas
- Con: Can be bypassed (not secure)

**Option 2: Server-side only (API validates)**
- Pro: Secure, can't bypass
- Pro: Single source of truth
- Con: Slower feedback (network roundtrip)

**Option 3: Both client + server (recommended)**
- Pro: Instant feedback + security
- Pro: Follows project pattern (other forms use this)
- Con: Duplicate validation logic (but shared schema)

### Acceptance Criteria
- [ ] Invalid email shows error message
- [ ] Empty required fields show error
- [ ] Submit button disabled while invalid
- [ ] Server returns 400 with errors if client bypassed

### Testing Plan
- Unit: Zod schema validation, error message generation
- Integration: Form state updates on input, API rejects invalid data
- Manual: Test all validation rules, try bypassing client validation

Which option should I use?
```

## Quick Reference

1. `gh issue view` → fetch issue
2. Research codebase (conditional: Explore agent for features, Grep for bugs, Read for docs) + check framework docs if needed
3. Identify gaps (tech details, approaches, requirements, context, criteria, testing)
4. **Present findings + ALL options with pros/cons** → WAIT for user
5. User chooses approach
6. Generate concise polished description (problem, user story, implementation, criteria, testing, notes)
7. **Show preview of appended content** → WAIT for confirmation
8. `gh issue edit` with append → confirm success

**Never skip:**

- User decision on ambiguities
- Confirmation before update
- Appending (never replace original description)
