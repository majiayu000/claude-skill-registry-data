---
created: "2025-10-21 17:45"
description: |
  Interactive skill creation wizard for Claude Code Skills. Guides you through defining skill metadata (name, description), structuring SKILL.md with progressive disclosure patterns, organizing reference files, creating executable scripts, and implementing workflows with feedback loops. Ensures skills follow best practices: concise instructions, appropriate degrees of freedom, third-person descriptions, and proper file organization. Outputs production-ready skill directories with YAML frontmatter and structured markdown.
examples:
  - /create-skill "PDF form processing automation"
  - /create-skill "Supabase database query builder"
  - /create-skill "Daily note content extraction"
---

# Create Skill

This command helps you create effective, well-structured Claude Code Skills by applying best practices from the official Skills authoring guide. Skills are powerful tools that extend Claude's capabilities with domain-specific knowledge, workflows, and executable scripts.

## Usage

```bash
/create-skill [brief description of what the skill should do]
```

## What are Claude Code Skills?

Skills are reusable knowledge packages that Claude can automatically discover and use when relevant. They consist of:
- **SKILL.md**: Main instructions with YAML frontmatter (name, description)
- **Reference files**: Optional supplemental documentation loaded on-demand
- **Scripts**: Optional executable code for deterministic operations
- **Workflows**: Step-by-step processes with feedback loops

## Interactive Process

When you run this command, I will:

1. **Understand your skill requirements**
   - Ask what problem the skill solves
   - Identify when Claude should use this skill
   - Determine if it needs executable scripts or just markdown instructions

2. **Design the skill metadata**
   - Craft a clear, specific name (max 64 characters, gerund form recommended)
   - Write a third-person description (max 1024 characters) that includes:
     - What the skill does
     - When to use it
     - Key trigger words and contexts

3. **Structure the skill content**
   - Determine appropriate degree of freedom (high/medium/low)
   - Organize into progressive disclosure patterns
   - Create workflows with checklists for complex tasks
   - Design validation/feedback loops where needed

4. **Create the skill directory**
   - Generate SKILL.md with proper YAML frontmatter
   - Add reference files for supplemental content (if needed)
   - Include utility scripts with proper error handling (if needed)
   - Organize files for optimal token efficiency

## Skill Design Principles

### 1. Concise is Key
Only add context Claude doesn't already have. Challenge every piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Example - Good (concise):**
```markdown
## Extract PDF text

Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**Example - Bad (too verbose):**
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains text, images, and other content. To extract text from a PDF, you'll need to use a library. There are many libraries available...
```

### 2. Set Appropriate Degrees of Freedom

**High Freedom** (text-based instructions):
- Use when multiple approaches are valid
- Decisions depend on context
- Heuristics guide the approach

**Medium Freedom** (pseudocode/scripts with parameters):
- A preferred pattern exists
- Some variation is acceptable
- Configuration affects behavior

**Low Freedom** (specific scripts, few parameters):
- Operations are fragile and error-prone
- Consistency is critical
- Specific sequence must be followed

### 3. Progressive Disclosure

Keep SKILL.md under 500 lines. Split additional content into separate files:

```
my-skill/
├── SKILL.md              # Main instructions (loaded when triggered)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── validate.py       # Utility script (executed, not loaded)
    └── process.py        # Processing script
```

**Important**: Keep references one level deep from SKILL.md. Avoid nested references.

### 4. Workflows for Complex Tasks

Provide checklists Claude can track:

```markdown
## Task workflow

Copy this checklist and track progress:

\```
Task Progress:
- [ ] Step 1: Analyze input
- [ ] Step 2: Create plan file
- [ ] Step 3: Validate plan (run validate.py)
- [ ] Step 4: Execute plan
- [ ] Step 5: Verify output
\```
```

### 5. Implement Feedback Loops

**Pattern**: Run validator → fix errors → repeat

```markdown
## Validation workflow

1. Make your changes
2. **Validate immediately**: `python scripts/validate.py`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues
   - Run validation again
4. **Only proceed when validation passes**
5. Execute the final operation
```

## YAML Frontmatter Requirements

Every SKILL.md must start with:

```yaml
---
name: Skill Name (max 64 characters, use gerund form)
description: What the skill does and when to use it. Use third person. Include key trigger words and contexts. (max 1024 characters)
---
```

**Good description examples:**

```yaml
# PDF Processing Skill
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.

# Excel Analysis Skill
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.

# Git Commit Helper Skill
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

**Avoid vague descriptions:**
- ❌ "Helps with documents"
- ❌ "Processes data"
- ❌ "Does stuff with files"

## File Organization Best Practices

### Naming Conventions
- Use forward slashes: `reference/guide.md` (not `reference\guide.md`)
- Name files descriptively: `form_validation_rules.md` (not `doc2.md`)
- Use consistent terminology throughout

### Directory Structure
```
skill-name/
├── SKILL.md                    # Main instructions
├── reference/                  # Reference materials (loaded on-demand)
│   ├── api-reference.md
│   └── troubleshooting.md
├── examples/                   # Usage examples
│   └── common-patterns.md
└── scripts/                    # Executable utilities
    ├── validate.py
    └── process.py
```

## Skills with Executable Code

### When to Include Scripts

**Benefits:**
- More reliable than generated code
- Save tokens (no need to include code in context)
- Save time (no code generation required)
- Ensure consistency across uses

### Script Best Practices

**1. Solve, don't punt**
```python
# Good: Handle errors explicitly
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        print(f"Cannot access {path}, using default")
        return ''

# Bad: Just fail and let Claude figure it out
def process_file(path):
    return open(path).read()
```

**2. Self-documenting configuration**
```python
# Good: Explain why
REQUEST_TIMEOUT = 30  # HTTP requests typically complete within 30 seconds
MAX_RETRIES = 3       # Most intermittent failures resolve by second retry

# Bad: Magic numbers
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

**3. Clear execution intent**
```markdown
**analyze_form.py**: Extract all form fields from PDF

Run: `python scripts/analyze_form.py input.pdf > fields.json`

Output format:
\```json
{
  "field_name": {"type": "text", "x": 100, "y": 200}
}
\```
```

## Common Patterns

### Template Pattern
Provide output format templates:

```markdown
## Report structure

ALWAYS use this exact template:

\```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
\```
```

### Examples Pattern
Show input/output pairs:

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
\```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
\```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
\```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
\```
```

### Conditional Workflow Pattern
Guide through decision points:

```markdown
## Task workflow

1. Determine the task type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use library X
   - Build from scratch
   - Export to format Y

3. Editing workflow:
   - Load existing file
   - Modify specific sections
   - Validate changes
   - Save when complete
```

## Testing Your Skill

Before finalizing:

1. **Test with real scenarios**: Use the skill in actual workflows, not test scenarios
2. **Test with all models**: Haiku, Sonnet, and Opus if you plan to use them
3. **Observe behavior**: Note where Claude struggles or succeeds
4. **Iterate based on usage**: Refine based on real behavior, not assumptions

## Skill Creation Checklist

Before completing:

- [ ] Name is clear and uses gerund form (max 64 chars)
- [ ] Description is specific, third-person, includes triggers (max 1024 chars)
- [ ] SKILL.md body is under 500 lines
- [ ] Additional details are in separate reference files (if needed)
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete
- [ ] File references are one level deep
- [ ] Workflows have clear steps with checklists
- [ ] Scripts handle errors explicitly (if applicable)
- [ ] No Windows-style paths (use forward slashes)
- [ ] Validation/feedback loops for critical operations

## Output

I will create:

1. **Skill directory structure** at `.claude/skills/{skill-name}/`
2. **SKILL.md** with proper YAML frontmatter and markdown body
3. **Reference files** (if needed for progressive disclosure)
4. **Utility scripts** (if needed for deterministic operations)
5. **Usage guide** explaining when and how Claude will use the skill

## Example Workflow

**User**: `/create-skill "Extract and categorize daily note content"`

**Claude**:
1. Asks clarifying questions:
   - What sections should be extracted?
   - What categories are needed?
   - Should this use a script or markdown instructions?

2. Designs metadata:
   - Name: "Daily Note Content Extraction"
   - Description: "Extracts diary entries, insights, and context from daily note files. Use when analyzing daily notes, processing journal entries, or extracting specific sections from markdown files with frontmatter."

3. Creates structure:
   ```
   daily-note-extraction/
   ├── SKILL.md              # Main instructions
   ├── examples.md           # Sample extraction patterns
   └── scripts/
       └── extract.py        # Fast extraction script
   ```

4. Generates SKILL.md with:
   - YAML frontmatter
   - Quick start guide
   - Extraction workflow with validation
   - References to examples.md
   - Script usage instructions

---

**Ready to create your skill?**

Describe what problem your skill should solve and I'll guide you through creating a production-ready Claude Code Skill.
