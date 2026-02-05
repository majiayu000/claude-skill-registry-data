---
name: Spec Workflow (Write & Implement)
description: Two-phase workflow for technical specifications - WRITING phase creates and commits specs then stops; IMPLEMENTATION phase follows specs, updates status, and commits all changes. Different agents handle each phase.
---

# Spec Workflow: Writing and Implementation

## Overview

This skill supports a **two-phase workflow** where specification writing and implementation are handled by different agents:

1. **WRITING PHASE**: Create spec, commit it, STOP
2. **IMPLEMENTATION PHASE**: Follow spec, implement, update status, commit everything

**CRITICAL**: These are separate tasks. Never write AND implement in the same session.

---

## Phase 1: Writing Specifications

**When to use**: User requests a spec to be written, or you need to document a bug/feature/system change.

**Your responsibilities**:
- ✅ Investigate and write the spec
- ✅ Git add and commit the spec file
- ✅ STOP - Do not implement

**You must NOT**:
- ❌ Implement the spec
- ❌ Write any code beyond the spec itself
- ❌ Update the spec status to "In Progress" or "Completed"

### Writing Workflow

**Step 1: Create timestamped spec file**

```bash
# Generate timestamp and create spec
TIMESTAMP=$(date +"%y%m%d-%H%M%S")
touch specs/${TIMESTAMP}-descriptive-name.md
```

**File naming**: `{YYMMDD-HHMMSS}-{kebab-case-description}.md`
**Location**: `specs/` directory at project root

**Step 2: Investigate thoroughly**

**Before proposing solutions**:

1. **Trace execution**: Use grep/find to follow actual code paths
2. **Verify assumptions**: Check if functionality already exists elsewhere
3. **Confirm the problem**: Ensure issue exists where suspected
4. **Never assume missing**: Always verify before claiming something doesn't exist

**Step 3: Write complete spec**

Use this template:

```markdown
# [Component/Feature] - [Brief Issue]

**Date:** YYYY-MM-DD HH:MM:SS
**Issue:** One-line problem description
**Priority:** [High/Medium/Low]
**Status:** Requires Implementation

## Problem Statement

- Current behavior (what's broken)
- Expected behavior (what should happen)
- Impact on users/system

## Root Cause Analysis

- Technical investigation with code examples
- Why the problem exists
- Comparison with working implementations if available

## Technical Approach

- Proposed solution methodology
- High-level implementation strategy
- Rationale for chosen approach

## Implementation Details

- Specific code changes with file paths
- Step-by-step implementation plan
- Testing strategy
- All commands and dependencies needed
```

**Step 4: Git commit and STOP**

```bash
# Add the spec file only
git add specs/${TIMESTAMP}-descriptive-name.md

# Commit with descriptive message
git commit -m "spec: add specification for [brief description]

Created spec: ${TIMESTAMP}-descriptive-name.md
Status: Requires Implementation"
```

**STOP HERE** - Your work is done. Implementation will be handled by a different agent.

### Writing Quality Checklist

Before committing, verify:

- [ ] Timestamp formatted correctly (YYMMDD-HHMMSS)
- [ ] File in `specs/` directory at project root
- [ ] Status is "Requires Implementation"
- [ ] All required sections present
- [ ] Investigated existing code before proposing changes
- [ ] Problem statement is specific
- [ ] Root cause includes technical investigation
- [ ] Solution fixes only stated problem
- [ ] Implementation details are actionable with full file paths
- [ ] Code examples properly formatted with file:line references
- [ ] No meta-commentary or self-notes
- [ ] Self-contained for fresh agent to implement

---

## Phase 2: Implementing Specifications

**When to use**: User requests implementation of an existing spec.

**Your responsibilities**:
- ✅ Read and understand the spec completely
- ✅ Implement according to the spec
- ✅ Follow all usual best practices
- ✅ Update spec status with commits
- ✅ Git add and commit all changes (spec + implementation)

**You must NOT**:
- ❌ Deviate from the spec without justification
- ❌ Skip updating the spec status
- ❌ Leave uncommitted changes

### Implementation Workflow

**Step 1: Read the spec**

```bash
# Find the spec to implement
ls specs/*.md

# Read it completely
cat specs/{timestamp}-name.md
```

Understand:
- Problem statement
- Root cause
- Technical approach
- All implementation details
- Testing requirements

**Step 2: Update spec status to "In Progress"**

Edit the spec file:

```markdown
**Status:** In Progress
**Started:** YYYY-MM-DD
```

Optional: Move to active directory

```bash
git mv specs/{spec}.md specs/active/{spec}.md
```

**Step 3: Implement according to spec**

Follow the implementation details exactly:
- Make all code changes specified
- Install any required dependencies
- Follow the step-by-step plan
- Test as specified in the spec

**Follow all usual best practices**:
- Write clean, maintainable code
- Add appropriate error handling
- Include comments where helpful
- Ensure type safety
- Test thoroughly

**Step 4: Verify requirements**

```bash
# Test the implementation
npm run dev  # or appropriate test command

# Verify all spec requirements met
# Check each item in Implementation Details section
```

**Step 5: Update spec status to "Completed"**

Edit the spec file:

```markdown
**Status:** Completed
**Implementation:**
- Commit: {hash} - {message}
- Commit: {hash} - {message}
**Completed:** YYYY-MM-DD
```

Optional: Archive the spec

```bash
# Move to implemented archive
git mv specs/active/{spec}.md specs/archive/implemented/{spec}.md
# OR if not in active/
git mv specs/{spec}.md specs/archive/implemented/{spec}.md
```

**Step 6: Git add and commit everything**

```bash
# Add all changes (implementation + updated spec)
git add [files-you-modified]
git add specs/archive/implemented/{spec}.md  # or wherever spec is

# Commit with reference to spec
git commit -m "feat: implement [feature name]

Implements spec: {timestamp}-name.md
- [Brief description of changes]
- [Another change]

Status: Completed"
```

### Implementation Quality Checklist

Before committing, verify:

- [ ] All spec requirements implemented
- [ ] Code follows best practices
- [ ] Tests pass / manual testing complete
- [ ] Spec status updated to "Completed"
- [ ] Spec includes commit hashes
- [ ] Spec includes completion date
- [ ] Spec archived (optional but recommended)
- [ ] All files added to git (implementation + spec)
- [ ] Commit message references spec file
- [ ] No uncommitted changes remain

---

## Directory Structure

```
specs/
├── {timestamp}-name.md           # New specs (Status: Requires Implementation)
├── active/                        # In progress (Status: In Progress)
├── archive/
│   ├── implemented/              # Completed (Status: Completed)
│   └── deprecated/               # Obsolete (Status: Deprecated)
└── drafts/                       # Work-in-progress ideas
```

---

## Content Guidelines

**Content principles** (apply to both phases):
- Write specs as final truth, not drafts
- No meta-commentary or revision history
- Include all context for fresh agent to start work
- Use code examples with file paths and line numbers
- Fix only the stated problem (no scope creep)

**Code examples format**:
```typescript
// src/components/Example.tsx:42
const problematic = () => { /* ... */ };

// Fixed version:
const corrected = () => { /* ... */ };
```

---

## Common Patterns

### Reference existing code

```markdown
## Root Cause Analysis

The issue occurs in `src/components/Button.tsx:87-92`:

\`\`\`typescript
// Current problematic implementation
const handleClick = () => {
  // Missing validation
  processData(data);
};
\`\`\`

Similar functionality in `src/components/Form.tsx:145` handles this correctly.
```

### Provide complete context

```markdown
## Implementation Details

**Files to modify**:
- `src/components/Button.tsx` - Add validation
- `src/types/index.ts` - Add new type definition

**Dependencies**:
\`\`\`bash
npm install zod
\`\`\`

**Testing**:
\`\`\`bash
npm run dev
# Navigate to http://localhost:5173/test-page
# Click button and verify validation works
\`\`\`
```

### Break down complex changes

```markdown
## Implementation Details

**Step 1: Add type definitions**
\`\`\`typescript
// src/types/validation.ts
export interface ValidationRule { /* ... */ }
\`\`\`

**Step 2: Implement validation logic**
\`\`\`typescript
// src/utils/validator.ts:1
export const validateInput = (/* ... */) => { /* ... */ }
\`\`\`

**Step 3: Integrate into component**
\`\`\`typescript
// src/components/Form.tsx:42
import { validateInput } from '@/utils/validator';
// Apply validation before submission
\`\`\`
```

---

## Anti-patterns to Avoid

**❌ Vague problem statements**:
"The form doesn't work right"

**✅ Specific problem statements**:
"Form submission in `src/components/ContactForm.tsx:87` allows invalid email formats to pass validation, causing 400 errors from the API"

**❌ Assumed missing functionality**:
"We need to add validation because there is none"

**✅ Verified gaps**:
"Searched codebase with `grep -r 'emailValidation' src/` - validation exists in `auth/` but not in `contact/` forms"

**❌ Scope creep**:
"Fix email validation AND redesign the form UI AND add analytics"

**✅ Focused solution**:
"Add email validation to contact form using existing validation utilities from `src/auth/validators.ts`"

**❌ Writing and implementing in same session**:
Don't create spec and immediately implement it

**✅ Separate sessions**:
Write spec → commit → stop. Later: implement spec → update status → commit

---

## Status Field Reference

### During Writing Phase

```markdown
**Status:** Requires Implementation
```

### During Implementation Phase

**Starting work**:
```markdown
**Status:** In Progress
**Started:** YYYY-MM-DD
```

**When complete**:
```markdown
**Status:** Completed
**Implementation:**
- Commit: abc123 - feat: implement feature X
- Commit: def456 - fix: handle edge case in feature X
**Completed:** YYYY-MM-DD
```

**If deprecated**:
```markdown
**Status:** Deprecated
**Reason:** [Brief explanation]
**Superseded By:** [Link to replacement]
**Deprecated:** YYYY-MM-DD
```

---

## Quick Reference

### I'm WRITING a spec:
1. Create timestamped file in `specs/`
2. Investigate thoroughly
3. Write complete spec with "Status: Requires Implementation"
4. `git add specs/{spec}.md && git commit`
5. **STOP** - Don't implement

### I'm IMPLEMENTING a spec:
1. Read spec completely
2. Update status to "In Progress"
3. Implement according to spec + best practices
4. Test thoroughly
5. Update spec status to "Completed" with commits
6. `git add [all-files] && git commit`
7. Done

---

## Notes

- Specs are living documents until archived
- Update specs if requirements change (add timestamped note at top)
- Reference spec filename in commit messages
- Self-contained specs enable any agent to implement independently
- Timestamps ensure chronological ordering and uniqueness
- The two-phase approach ensures specs are reviewed before implementation
- Different agents bring fresh perspectives to implementation
