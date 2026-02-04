---
name: Creating Agent Skills
description: Creates or improves Agent Skills following official documentation and best practices. Use when creating new skills, improving existing skills, evaluating skill quality, or ensuring skills follow naming conventions, structure requirements, and discovery patterns. Guides through description writing, progressive disclosure, workflows, and testing.
---

# Creating Agent Skills

Creates or improves Agent Skills following official Claude Code documentation and best practices.

## What you should do

When invoked, help the user create or improve Agent Skills by:

1. **Understanding the goal** - Determine what the user needs:
   - Create a new skill from scratch
   - Improve an existing skill's discovery or structure
   - Evaluate a skill against best practices
   - Convert informal knowledge into a skill
   - Debug why a skill isn't being discovered

2. **Apply best practices** - Follow the official patterns:
   - Use gerund form naming ("Managing X", "Building Y", "Processing Z")
   - Write third-person descriptions with specific trigger words
   - Keep SKILL.md under 500 lines (use progressive disclosure if needed)
   - Include both what the skill does and when to use it
   - Be concise (assume Claude is already smart)

3. **Structure properly** - Ensure correct format:
   - Directory: `skill-name/SKILL.md`
   - YAML frontmatter with `name` and `description`
   - Clear sections and examples
   - Reference files for detailed content (if needed)

4. **Test and iterate** - Validate the skill works:
   - Check description triggers skill discovery
   - Verify structure is valid
   - Test with real scenarios
   - Iterate based on usage

## Skill structure requirements

### YAML frontmatter

```yaml
---
name: Skill Name (64 chars max, use gerund form)
description: What it does and when to use it (1024 chars max, third person)
---
```

### Naming conventions

**Use gerund form** (verb + -ing):

**Good**: "Processing PDFs", "Analyzing Spreadsheets", "Managing Databases"

**Avoid**: "Helper", "Utils", "Tools", "Documents", "Data"

### Writing effective descriptions

**Always write in third person**:

- ✅ "Processes Excel files and generates reports"
- ❌ "I can help you process Excel files"
- ❌ "You can use this to process Excel files"

**Include both what and when**:

```yaml
description: Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Be specific** - include key trigger words that users would mention.

### Progressive disclosure

Keep SKILL.md under 500 lines. Move detailed content to separate files:

```
my-skill/
├── SKILL.md              # Overview and navigation
├── REFERENCE.md          # Detailed API docs
├── EXAMPLES.md           # Usage examples
└── scripts/
    └── helper.py         # Utility scripts
```

Reference from SKILL.md:

```markdown
**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
```

Claude loads additional files only when needed.

## Quick skill creation workflow

When user asks to create a skill:

1. **Understand the domain**:
   - What tasks will this skill help with?
   - What context or knowledge needs to be captured?
   - What are the common patterns or workflows?

2. **Draft the structure**:

```yaml
---
name: [Gerund form name]
description: [Third person, what + when, specific triggers]
---

# [Skill Title]

[Brief overview]

## What you should do

[Step-by-step instructions for Claude]

## [Section 2: Domain-specific content]

[Examples, patterns, or references]
```

3. **Keep it concise**:
   - Challenge every paragraph: "Does Claude really need this?"
   - Remove explanations of common knowledge
   - Focus on domain-specific information

4. **Add progressive disclosure** (if needed):
   - Move detailed reference to separate files
   - Keep SKILL.md as navigation guide
   - Link to details: "See [REFERENCE.md](REFERENCE.md)"

5. **Test discovery**:
   - Does the description trigger the skill when relevant?
   - Test with fresh Claude instance
   - Iterate based on actual usage

## Checklist for effective skills

Before finalizing a skill:

### Core quality
- [ ] Description uses third person voice
- [ ] Description includes both what and when
- [ ] Description has specific trigger keywords
- [ ] Name uses gerund form
- [ ] SKILL.md body under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Concrete examples (not abstract)
- [ ] File references one level deep
- [ ] Forward slashes in all paths (not backslashes)

### Testing
- [ ] Tested with real usage scenarios
- [ ] Description triggers skill appropriately
- [ ] Structure follows official format

## Common patterns by skill type

### Data analysis skills
**Pattern**: Domain-specific schemas + common queries + filters

Example: BigQuery with table schemas, naming conventions, filtering rules

### Document processing skills
**Pattern**: Workflows + validation + utility scripts

Example: PDF form filling with analyze → map → validate → fill

### Code generation skills
**Pattern**: Templates + examples + style guide

Example: Commit messages with format + examples

### Configuration skills
**Pattern**: Project-specific settings + references

Example: GitHub Projects with pre-configured IDs and field options

## Output format

When creating a skill, provide:

1. **Complete SKILL.md content** with proper frontmatter
2. **File structure** showing any additional reference files
3. **Testing suggestions** - scenarios to verify discovery
4. **Usage examples** - how to invoke naturally

Example output:

```
I'll create a skill for [domain]. Here's the structure:

```yaml
---
name: [Gerund form name]
description: [Third person, what + when, specific triggers]
---

# [Skill Title]

[Content following best practices...]
```

**File structure**:
```
skill-name/
├── SKILL.md
└── REFERENCE.md (if needed)
```

**Testing**:
Try these scenarios to verify discovery:
- "[Natural request that should trigger]"
- "[Another scenario]"
```

## Best practices reference

For complete best practices including:
- Degrees of freedom
- Content guidelines
- Anti-patterns to avoid
- Evaluation strategies
- Common skill types
- Detailed examples

See [BEST-PRACTICES.md](BEST-PRACTICES.md)

## Remember

- Skills are **model-invoked** - Claude decides when to use them
- Good descriptions are critical for discovery
- Conciseness preserves context window
- Test with real usage, not just theory
- Iterate based on observed behavior

## Official documentation

For complete details and latest updates:

- **Agent Skills quickstart**: https://docs.claude.com/en/docs/claude-code/skills
- **Best practices guide**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- **Skills overview**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **Claude Code plugins** (for sharing skills): https://docs.claude.com/en/docs/claude-code/plugins