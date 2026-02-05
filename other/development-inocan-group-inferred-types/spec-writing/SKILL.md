---
name: spec-writing
description: Use during Phase 3 of spec creation to create specification document - searches codebase for reusable patterns, presents spec in validated 150-200 word sections, and saves complete specification following template structure
---

# Spec Writing

## What It Does

1. Loads requirements, visuals, product context
2. Searches codebase for reusable patterns
3. Presents spec in sections (150-200 words each)
4. Validates each section before continuing
5. Saves complete spec.md following template

**No code in spec - descriptions only.**

## The Process

### Step 1: Load Requirements

```bash
SPEC="[provided by workflow]"

cat "$SPEC/planning/initialization.md"
cat "$SPEC/planning/requirements.md"
ls -la "$SPEC/planning/visuals/"
cat specs/product/tech-stack.md
```

**Analyze:**
- Feature requirements and scope
- Visual design elements
- Reusability opportunities from user
- Tech stack for search strategy

### Step 2: Search Codebase

Search for patterns to reuse based on requirements.

**Search by tech stack:**

**React/Vue:**
```bash
find src/components -name "*[keyword]*"
grep -r "similar-pattern" src/pages/
find src/hooks src/composables -name "*[keyword]*"
```

**Backend:**
```bash
find app/models src/models -name "*[keyword]*"
grep -r "similar-endpoint" app/controllers/ src/routes/
find app/services src/services -name "*[keyword]*"
```

**Database:**
```bash
ls db/migrate/ | grep -i "[keyword]"
grep -A 10 "create_table.*[keyword]" db/schema.rb
```

**Document findings:**
- Component/file paths
- What they do
- How to reuse/extend
- Patterns to follow

### Step 3: Present Spec Sections

**Announce:**
```
Based on requirements and codebase search,
I'll present the spec section by section.

Let me know if each section looks right.
```

**Section 1: Goal & User Stories (150-200 words)**

```
# Specification: [Feature Name]

## Goal
[1-2 sentences from requirements]

## User Stories
- As a [user], I want to [action] so that [benefit]
- [1-2 more stories]

Capture the purpose?
```

**WAIT. Adjust if needed.**

**Section 2: Specific Requirements (200-250 words)**

```
## Specific Requirements

**[Category 1]**
- [Sub-requirement with approach]
- [Sub-requirement with approach]
- [Up to 8 concise points]

**[Category 2]**
- [Sub-requirement with approach]
- [Up to 8 concise points]

[Up to 10 categories total]

Match your vision?
```

**WAIT. Adjust if needed.**

**Section 3: Visual Design (if visuals exist) (150-200 words)**

```
## Visual Design

**`planning/visuals/homepage-mockup.png`**
- [Layout structure]
- [Key UI components]
- [Colors/typography if high-fi]
- [Interactive elements]
- [Up to 8 bullets]

**`planning/visuals/form-wireframe.jpg`**
- Fidelity: Low-fi wireframe - structure focus
- [Layout and placement]
- [Up to 8 bullets]

Match how you want to interpret visuals?
```

**WAIT. Adjust if needed.**

**Section 4: Existing Code (150-200 words)**

```
## Existing Code to Leverage

[From user-provided reusability notes:]
**[Feature user mentioned]**
- Path: `[path]`
- What it does: [description]
- How to reuse: [approach]

[From codebase search:]
**[Component found]**
- Path: `[path from search]`
- What it does: [description]
- How to reuse: [approach]
- Pattern: [architectural pattern]

[Up to 5 existing code areas]

Capture reusability opportunities?
```

**WAIT. Adjust if needed.**

**Section 5: Out of Scope (100-150 words)**

```
## Out of Scope

[From requirements - what NOT to include:]
- [Feature/capability]
- [Feature/capability]
- [Up to 10 items]

[Inferred from discussion:]
- [Related but future work]
- [Would over-complicate MVP]

Scope boundary correct?
```

**WAIT. Adjust if needed.**

### Step 4: Save Complete Spec

```bash
cat > "$SPEC/spec.md" <<'EOF'
# Specification: [Feature Name]

## Goal
[Approved content]

## User Stories
[Approved content]

## Specific Requirements
[All approved categories]

## Visual Design
[If visuals - approved descriptions]

## Existing Code to Leverage
[All approved reusability notes]

## Out of Scope
[All approved exclusions]
EOF
```

### Step 5: Report Completion

```
✅ Spec complete!

Created: spec.md

Summary:
- Goal and [X] user stories
- [Y] requirement categories
- [Z] visual designs ([or] No visuals)
- [A] existing patterns to leverage
- [B] items scoped out

Spec is:
- Concise (skimmable)
- Actionable (clear requirements)
- Reusability-focused
- Scope-bounded

Ready for Phase 4: Tasks planning
```

**Return to workflow.**

## Search Strategy

**Smart keywords from requirements:**
- Nouns: user, post, comment, payment
- Verbs: create, update, delete, validate
- Concepts: auth, authorization, notification

**Multi-strategy search:**

1. **File names:**
```bash
find . -name "*[keyword]*" -type f | head -20
```

2. **Content:**
```bash
grep -r "[keyword]" --include="*.js" --include="*.ts" -l | head -20
```

3. **Patterns:**
```bash
# React components
grep -r "export.*function [Keyword]" src/

# Classes
grep -r "class [Keyword]" app/models/
```

**Too many results? Narrow:**
```bash
grep -r "User.*authentication" src/
find src/features/auth -name "*.ts"
find . -name "*[keyword]*" -mtime -30
```

**No results? Broaden:**
- Related terms (auth → authentication → login)
- Parent concepts (UserProfile → User)
- Different directories

## Validation Pattern

For each section:
1. Present (150-200 words max)
2. Ask validation question
3. WAIT for response
4. Adjust if needed
5. Continue only when approved

**If major revision:**
```
Let me rethink this section.

[Ask clarifying question]

Revised version:
[Present revision]

Better?
```

## Red Flags

**Never:**
- Write code in spec (descriptions only)
- Present entire spec at once
- Skip codebase search
- Add sections not in template
- Proceed without validation

**Always:**
- Search before writing spec
- Present in small sections
- Wait for validation after each
- Reference existing code when found
- Keep requirements concise

## Integration

**Called by:**
- `spec-creation-workflow` (Phase 3)

**Returns to:**
- `spec-creation-workflow`

**Creates:**
- `[spec]/spec.md`

**Uses:**
- `planning/initialization.md`
- `planning/requirements.md`
- `planning/visuals/*` (if exists)

**Next phase uses:**
- `spec.md` for tasks breakdown
