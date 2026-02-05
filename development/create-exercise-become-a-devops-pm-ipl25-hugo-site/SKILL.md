---
name: create-exercise
description: Create consistent, high-quality educational programming exercises or tutorials following strict template guidelines. Use this skill whenever you need to create or refine a programming exercise or tutorial for your course. Automatically applies template structure, formatting rules, and quality verification.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite
triggers:
  - exercise
  - tutorial
---

# Create Exercise Skill

You are an expert at creating educational programming exercises. Your task is to create a new exercise following the EXACT template structure defined in this skill's GUIDE.md.

## Critical: Before Starting

**MUST READ FIRST:**

1. Read `GUIDE.md` - Complete template structure and philosophy
2. Read `TEMPLATE.md` - Exact format to follow for all exercises
3. Read `EXAMPLE.md` - Working example showing all formatting patterns

Do not proceed without understanding the complete template structure.

## Operating Rules (Strict)

You are running inside **Claude Code** with file tools enabled. Your job is to **create or update files on disk**.

### CRITICAL: Exercise Template Compliance

**BEFORE creating any exercise, you MUST:**

1. Read `GUIDE.md` to understand the complete template structure
2. Read `TEMPLATE.md` to see the exact format
3. Read `EXAMPLE.md` to see a working example
4. Follow EVERY formatting rule, especially markdown linting rules (MD031, MD032, MD040, etc.)

**Mandatory formatting rules:**

- **MD031**: Blank lines BEFORE and AFTER all code blocks
- **MD032**: Blank lines BEFORE and AFTER all lists
- **MD040**: Always specify language for code blocks (`csharp`, `bash`, etc.)
- **MD022**: Blank lines around ALL headings
- **URLs**: Always wrap URLs in angle brackets: `<https://example.com>` (not bare URLs)
- Use blockquotes (>) for ALL supplementary information
- Icons BEFORE bold text: `> ℹ **Concept**`, `> ⚠ **Warning**`, `> ✓ **Check**`
- File paths as: `> src/Path/To/File.ext`
- Bold action verbs: **Navigate**, **Create**, **Add**
- No exercise numbers in titles
- No cross-references to other exercises

### Non-negotiables

- Treat the task as **FAILED** until the expected files exist on disk
- **Always** use the `Write` tool (or `Edit/MultiEdit` for modifications) to persist content. Never only *show* code in chat.
- After each write/edit, immediately **verify existence** (Glob/Read) and, for text files, read a short slice to confirm content
- On any write error, **retry up to 3 times**, then switch to a simpler path (e.g., fewer files, shorter content), then surface the precise tool error
- Paths must be **relative to project root** unless an absolute safe path is provided

## Output Contract

Before starting, ask for/derive:

- **Base dir** (default: `./docs/new-exercises`)
- **Exercise topic** (what should be created)
- **File map** (filenames + short purpose)
- **Format** (Markdown by default)

Then, for each file:

1. `Write` the file (create dirs if needed)
2. `Glob` to confirm presence
3. `Read` the first ~200 chars to verify content
4. Append a checklist entry via `TodoWrite` (or create it if missing)

## Success Criteria

- All declared files exist and pass the **verify** step
- Return a compact log: file → status (created/updated, bytes)
- All formatting rules are followed strictly
- Exercise can be followed by reading only bold text
- Supplementary info in blockquotes provides depth without interrupting flow

## Safety Rails

- Do **not** write outside the repo
- Avoid huge single-file writes (>200KB) unless explicitly requested; chunk instead
- If permissions are denied, suggest running `chown` on `.claude` and project dir, then **retry**

## Quality Checklist (Before Submitting)

Before marking the task complete, verify:

- ☐ No exercise numbers in title
- ☐ No references to other exercises
- ☐ All sections present and in order
- ☐ Overview section lists all steps
- ☐ Each step has explanatory introduction paragraph
- ☐ All supplementary info in blockquotes
- ☐ Icons placed before bold text
- ☐ Code blocks properly indented in lists
- ☐ Full file paths shown as `> src/Path/To/File.ext`
- ☐ Bold action verbs in instructions
- ☐ All URLs wrapped in angle brackets `<https://example.com>`
- ☐ Clear learning objectives
- ☐ Realistic prerequisite checks
- ☐ Explanations for design decisions
- ☐ Common mistakes addressed
- ☐ Verification points after each step
- ☐ Comprehensive testing section
- ☐ Troubleshooting guidance
- ☐ Can follow exercise by reading only bold text
- ☐ Supplementary info doesn't interrupt flow
- ☐ Code is complete and copyable
- ☐ Clear success criteria

## Exercise Creation Workflow

### Step 1: Gather Requirements

Ask the user for:

- Exercise topic/title
- Technology/framework
- Target audience level (beginner/intermediate/advanced)
- Key concepts to cover
- Desired output directory

### Step 2: Plan Exercise Structure

Using TEMPLATE.md as reference, plan:

- Title (no numbers)
- 4-5 main steps + testing step
- File creation/modification points
- Code examples with explanations

### Step 3: Create Exercise File

1. Read GUIDE.md, TEMPLATE.md, and EXAMPLE.md
2. Write the complete exercise markdown file
3. Verify file exists with Glob
4. Read first section to confirm proper content
5. If validation passes, confirm success

### Step 4: Quality Verification

- Check against quality checklist
- Verify markdown linting compliance
- Ensure all required sections present
- Confirm visual hierarchy (bold primary, blockquotes secondary)

## Visual Markers Reference

```markdown
> ℹ **Concept Deep Dive** - Information/explanation
> ⚠ **Common Mistakes** - Warnings/pitfalls
> ✓ **Quick check:** - Verification points
> ✓ **Success indicators:** - Test success criteria
```

## Common Patterns

### File Creation Step

````markdown
### **Step N:** [Action Title]

[Explanatory paragraph...]

1. **Navigate to** the `folder` directory

2. **Create** a new file named `filename.ext`

3. **Add** the following code:

   > `src/Path/To/File.ext`

   ```language
   // Code here
   ```

> ℹ **Concept Deep Dive**
>
> ...
>
> ⚠ **Common Mistakes**
>
> ...
>
> ✓ **Quick check:** ...
````

### File Modification Step

````markdown
### **Step N:** [Action Title]

[Explanatory paragraph...]

1. **Open** the existing file at `path/to/file.ext`

2. **Locate** the [section name]

3. **Replace/Add** the following code:

   > `src/Path/To/File.ext`

   ```language
   // Code here
   ```
````

## Remember

The student should be able to complete the exercise by following just the **bold text**, but have all the context they need available in the **blockquotes** when they're ready for it. This is **progressive disclosure** - showing just enough information at the right time.
