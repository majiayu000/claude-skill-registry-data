---
name: summarize-session
description: Compact the conversation context by summarizing what was accomplished and updating CLAUDE.md with any learnings. Use when context is getting long or when transitioning between work sessions.
---

# Compact Context Skill

This skill performs **context compaction** - summarizing the current session and persisting valuable learnings to CLAUDE.md.

**Purpose**: Reduce context length while preserving important information for future sessions.

---

## When to Use

Use this skill when:
- Context is getting long (lots of back-and-forth)
- Transitioning between work sessions
- User explicitly asks to compact or summarize
- Before starting a major new task
- After completing significant work

---

## Workflow

### Phase 1: Session Analysis

Review the current conversation and identify:

1. **Work Completed**
   - Files created/modified
   - Features implemented
   - Bugs fixed
   - Refactoring done

2. **Decisions Made**
   - Architectural choices
   - Pattern preferences
   - Naming conventions established
   - Trade-offs chosen

3. **Problems Encountered**
   - Errors and how they were resolved
   - Gotchas discovered
   - Workarounds applied

4. **User Preferences Revealed**
   - Communication style
   - Code style preferences
   - Workflow preferences

5. **Learnings About the Codebase**
   - Patterns not documented in CLAUDE.md
   - Important file locations
   - Integration details
   - Quirks or edge cases

---

### Phase 2: Rule Files Update Evaluation

Rule files in `.claude/rules/` are domain-specific and have a **lower threshold** than CLAUDE.md. They should capture patterns, gotchas, and decisions for specific domains.

**Rule File Locations:**
- `rules/frontend/` - auth, styling, api, routing, state, onboarding, errors
- `rules/backend/` - auth, data, api, validation, services, calculations, llm, errors, middleware, utils, seed
- `rules/components/` - components, styling, charts, forms, storybook, errors
- `rules/e2e/` - testing, auth

**Threshold for Rules: Add if it meets TWO criteria:**

1. **Reusable** - Will apply to future work in that domain
2. **Domain-specific** - Belongs to a specific subsystem (not global)

**Examples that SHOULD go in rule files:**
- "AreaChart requires data sorted by date ascending" → `rules/components/charts.md`
- "Zod schemas strip unknown fields by default" → `rules/backend/validation.md`
- "Modal close button uses absolute positioning top-right" → `rules/components/components.md`
- "Demo login seeds data on every call" → `rules/backend/auth.md`
- "Use formatCurrency from @finans/components for NOK" → `rules/frontend/styling.md`

**Examples that should NOT go in rule files:**
- "Fixed a typo" - not reusable
- "React uses JSX" - too generic

**Rule File Sections:**
Each rule file follows this structure:
- **Stack** - Technologies/libraries used
- **Structure** - File/folder organization
- **Patterns** - Code patterns with examples
- **Decisions** - Architectural choices made
- **Gotchas** - Common pitfalls, edge cases

Add learnings to the appropriate section. If a section doesn't exist, create it.

---

### Phase 3: CLAUDE.md Update Evaluation

CLAUDE.md has a **higher threshold** - only global, project-wide learnings.

**Threshold: Only add if it meets ALL THREE criteria:**

1. **Reusable** - Will apply to future work (not a one-time fix)
2. **Non-obvious** - Not something a senior dev would assume
3. **Project-wide** - Applies globally, not to a specific domain

**Examples that PASS the threshold:**
- "All pages must use usePageTitle hook" - project-wide convention
- "Never use max-width media queries" - affects all styling
- "API base path is /api/v1" - affects all endpoints

**Examples that FAIL (should go in rules instead):**
- "AreaChart needs sorted data" - domain-specific (charts.md)
- "Zod strips unknown fields" - domain-specific (validation.md)
- "Modal uses absolute close button" - domain-specific (components.md)

**When in doubt, put it in a rule file.** CLAUDE.md is for global conventions only.

---

### Phase 4: Update Files

**Step 1: Update Rule Files**

For each domain-specific learning:
1. Identify the correct rule file based on the domain
2. Read the rule file to find the appropriate section
3. Add the learning in the matching section (Stack, Patterns, Decisions, or Gotchas)
4. Keep additions concise and match existing style

**Step 2: Update CLAUDE.md (if warranted)**

For global learnings that pass the higher threshold:
1. Read CLAUDE.md to find the appropriate section
2. Add the learning in the correct location

**CLAUDE.md Placement Guidelines**:

| Learning Type | Where to Add |
|---------------|--------------|
| New tech/dependency | Tech Stack section |
| New pattern/convention | Coding Standards section |
| New page or feature | Pages section |
| New API endpoint | API Design section |
| Security concern | Security section |
| User preference | NOTES FROM THE USER section |
| Development tip | Development Setup section |

---

### Phase 5: Context Summary

Produce a compact summary with this structure:

```markdown
## Session Summary

### Completed
- [Bullet list of work done]

### Files Changed
- [List of significant files modified]

### Decisions
- [Key decisions made during session]

### Open Items
- [Anything left incomplete or for next session]

### Rule Updates
- [Rule file → what was added]

### CLAUDE.md Updates
- [What was added, if anything, or "None"]
```

---

## Output

The skill produces:
1. **Updates to rule files** (lower threshold, domain-specific)
2. **Updates to CLAUDE.md** (higher threshold, global only)
3. **Session summary** (displayed to user)

The summary becomes the new context for continuing work, replacing the long conversation history.

---

## Example Session Summary

```markdown
## Session Summary

### Completed
- Fixed TypeScript strict mode errors in backend/
- Implemented rate limiting middleware
- Added Norwegian number formatting utility
- Created user profile API endpoint

### Files Changed
- backend/src/middleware/rateLimiter.ts (new)
- backend/src/controllers/userController.ts (modified)
- frontend/src/shared/utils/numberFormat.ts (new)
- backend/tsconfig.json (modified - enabled strict)

### Decisions
- Rate limit: 100 req/min general, 10 req/min calculators
- Number format: numeral.js with custom nb locale
- Profile updates require email verification

### Open Items
- E2E test for rate limiting

### Rule Updates
- rules/backend/middleware.md → Added rate limiter configuration pattern
- rules/backend/validation.md → Added profile update validation schema
- rules/frontend/styling.md → Added numeral.js locale setup

### CLAUDE.md Updates
- None (domain-specific learnings went to rule files)
```

---

## Critical Rules

1. **Be concise** - Summaries should be short, not verbose
2. **Preserve essential info** - Don't lose important context
3. **Prefer rule files over CLAUDE.md** - Domain-specific goes to rules
4. **Update CLAUDE.md sparingly** - Only global, project-wide learnings
5. **Match existing style** - Follow the file's formatting conventions
6. **Focus on actionable** - Learnings should help future work
7. **Don't duplicate** - Don't add what's already documented
8. **Add to correct section** - Stack, Patterns, Decisions, or Gotchas

---

## Triggering This Skill

The user can invoke with:
- "compact context"
- "summarize session"
- "what did we accomplish"
- "update claude.md with learnings"
- "compress the context"
- "session summary"
