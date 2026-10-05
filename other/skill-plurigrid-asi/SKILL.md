---
name: skill
description: Comprehensive guide to understanding, writing, validating, and using skills in agent systems. Covers the agentskills.io specification, progressive disclosure patterns, frontmatter validation, directory structure, and tooling. When you need to teach agents how to read skills, validate skill metadata, work with SKILL.md files, or understand skill architecture.
license: Proprietary. See LICENSE.txt for complete terms.
compatibility: Designed for Claude Code, skills-ref CLI, and agentskills.io-compatible agents. Requires Python 3.9+ for skills-ref validation, Go 1.21+ for boxxy skill rendering.
metadata:
  version: 1.0.0
  spec-source: https://agentskills.io/specification
  skills-ref-repo: https://github.com/agentskills/agentskills
  skills-repo: https://github.com/anthropics/skills
allowed-tools: "Read Bash(python:skills-ref*) Bash(go:boxxy*)"
---

# Skills: Formal Specification and Implementation Guide

## What is a Skill?

A **skill** is a self-contained, discoverable unit of agent capability encoded as a directory containing:

- **`SKILL.md`** (required): YAML frontmatter + Markdown instructions
- **`scripts/`** (optional): Executable code
- **`references/`** (optional): Supplementary documentation
- **`assets/`** (optional): Templates, data files, images

Each skill is **identified by its name** (kebab-case) and must be **located in a directory matching that name**.

### Design Philosophy

Skills implement **progressive disclosure**: agents load skill metadata on startup (~100 tokens), full instructions when activated (~5000 tokens), and on-demand resources during execution. This minimizes context bloat while maximizing capability.

---

## Part 1: Frontmatter Specification

The SKILL.md file opens with YAML frontmatter delimited by `---`:

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files. Use when processing documents.
license: MIT
compatibility: Requires Python 3.9, pypdf, pdfplumber
metadata:
  version: 1.0.0
  author: Your Name
allowed-tools: "Bash(python:*) Read"
---
```

### Required Fields

| Field | Type | Constraints |
|-------|------|-------------|
| **name** | string | 1–64 characters. Lowercase alphanumeric + hyphens. No leading/trailing hyphens, no consecutive hyphens (`--`). Must match parent directory name and be NFKC-normalized. |
| **description** | string | 1–1024 characters. Should explain both what the skill does AND when to use it. Include specific keywords for agent matching. |

### Optional Fields

| Field | Type | Constraints |
|-------|------|-------------|
| **license** | string | License name (e.g., `"MIT"`, `"Apache-2.0"`) or reference to a file (e.g., `"Proprietary. LICENSE.txt has full terms"`). |
| **compatibility** | string | 1–500 characters. Environment, system, or product requirements. Examples: `"Requires Node.js 18+, Docker, internet access"` or `"Designed for Claude Code"`. |
| **metadata** | mapping | Arbitrary key-value string pairs. Use unique key names to avoid conflicts. Nested values are converted to strings. Common: `version`, `author`, `updated`. |
| **allowed-tools** | string | Space-delimited tool patterns (experimental). Format: `"ToolName(pattern:*) ..."`. Example: `"Bash(git:*) Read Write"` means only git-related bash commands are pre-approved. |

### Frontmatter Rules

1. **Field whitelist**: Only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` are recognized. Unknown fields cause validation errors.
2. **No duplicate keys** in metadata.
3. **Type checking**: name and description must be strings (not lists or objects).
4. **Case sensitivity**: All field names are lowercase.

---

## Part 2: Name Validation Rules

The **name** field must satisfy these constraints:

### Regex (simplified)
```
^[a-z0-9]+(-[a-z0-9]+)*$
```

### Detailed Rules

1. **Length**: 1–64 characters
2. **Characters**: Lowercase ASCII letters (`a-z`), digits (`0-9`), hyphens (`-`)
3. **No leading hyphen**: `pdf` is valid; `-pdf` is invalid
4. **No trailing hyphen**: `pdf-processing` is valid; `pdf-` is invalid
5. **No consecutive hyphens**: `pdf-processing` is valid; `pdf--processing` is invalid
6. **Must match parent directory**: If SKILL.md is in `pdf-processing/`, the name must be `pdf-processing`
7. **Unicode normalization**: Name is NFKC-normalized (handles accents, ligatures, etc.)

### Valid Examples
- `pdf`
- `pdf-processing`
- `data-analysis`
- `code-review`
- `xlsx`
- `skill-creator`

### Invalid Examples
- `PDF-Processing` (uppercase)
- `-pdf` (leading hyphen)
- `pdf-` (trailing hyphen)
- `pdf--processing` (consecutive hyphens)
- `pdf_processing` (underscore not allowed)
- `` (empty)
- `pdf-processing-and-analysis-suite` (65 characters, exceeds max)

---

## Part 3: Body Content (Markdown Instructions)

After the closing `---`, everything is Markdown. This is **Level 2: Instructions** in progressive disclosure.

### Guidelines

- **Stay under 500 lines** (hard limit in agentskills spec)
- **Estimate under 5000 tokens** (~20,000 characters) (advisory)
- **Include clear structure**: headings, lists, code blocks
- **Document when to use**: What problems does this skill solve? When should agents reach for it?
- **Provide examples**: Show input/output, common patterns, edge cases
- **Link to resources**: Use `[reference guide](references/REFERENCE.md)` or `scripts/extract.py`
- **Avoid boilerplate**: Don't include README.md, CHANGELOG.md, or license text (those live in the root)

### Example Structure

```markdown
# PDF Processing

## Overview
This skill provides tools for extracting text and tables from PDF files...

## Quick Start
1. Load a PDF: `python scripts/extract.py input.pdf`
2. Parse tables: `python scripts/tables.py input.pdf`

## When to Use
- User provides a PDF and wants specific data extracted
- Need OCR for scanned PDFs
- Converting PDF forms to structured data

## When NOT to Use
- User has a simple PDF they can convert to text with `pdftotext`
- Task requires heavy image processing (use image-processing skill)

## Common Tasks

### Extracting Text
See `references/EXTRACTION_GUIDE.md` for detailed steps.

### Parsing Tables
Tables.py handles:
- Bordered tables (Tabula style)
- Grid-based layouts
- Multi-row headers

### Watermarks & Encryption
Scripts provided for removal (see `references/SECURITY.md`).

## References
- [PyPDF docs](https://pypdf.readthedocs.io/)
- [PDFPlumber guide](references/PDFPLUMBER.md)

## Troubleshooting
Common errors and solutions in `references/TROUBLESHOOTING.md`.
```

---

## Part 4: Progressive Disclosure Levels

Skills are loaded in three tiers to manage agent context efficiently.

### Level 1: Metadata (~100 tokens)

Loaded at agent startup. Contains:
- **name**: Skill identifier (kebab-case)
- **description**: What the skill does + when to use
- **role** (boxxy extension): GF(3) trit-based role (Generator, Coordinator, Verifier)
- **color** (boxxy extension): Primary color for UI rendering

**Example XML** (from `skills-ref to-prompt`):
```xml
<skill name="pdf" description="Extract text and tables from PDF files."
        location="/path/to/pdf/SKILL.md" trit="0" role="Coordinator"
        color="#F59E0B" />
```

Agents use this to:
1. Recognize available skills
2. Match skills to user requests (semantic matching on name + description)
3. Decide whether to activate this skill (avoiding context bloat)

### Level 2: Instructions (~5000 tokens recommended, <500 lines hard limit)

Loaded when skill is activated. Contains:
- Full Markdown body after frontmatter
- Step-by-step procedures
- Examples and edge cases
- Links to references and scripts

**Example XML**:
```xml
<skill name="pdf" ...>
[full Markdown body here]
</skill>
```

### Level 3: Resources (on-demand)

Loaded during execution as needed. Contains:
- **`scripts/`**: Executable code (Python, Bash, Go, etc.)
  - Should be self-contained or clearly document dependencies
  - Include helpful error messages
  - Useful for deterministic, fragile operations

- **`references/`**: Supplementary docs (1 level deep from SKILL.md)
  - Individual files per topic (e.g., `REFERENCE.md`, `FORMS.md`)
  - Keep focused and modular
  - Examples: API docs, detailed tutorials, templates

- **`assets/`**: Static resources
  - Templates, images, data files, boilerplate
  - Used for output artifacts (forms, generated code, etc.)

**File referencing** from the body:
```markdown
For details, see [FHIR reference guide](references/FHIR_GUIDE.md).
Run [extraction script](scripts/extract.py) with your PDF.
Use [form template](assets/form-template.txt) as a starting point.
```

---

## Part 5: Directory Structure

```
skill-name/
├── SKILL.md                    # Required: frontmatter + body
├── scripts/                    # Optional: executable code
│   ├── extract.py            # Python script
│   ├── process.sh            # Bash script
│   └── query.go              # Go program
├── references/               # Optional: supplementary docs (1 level deep)
│   ├── EXTRACTION_GUIDE.md
│   ├── FORMS.md
│   ├── API_DOCS.md
│   └── TROUBLESHOOTING.md
└── assets/                    # Optional: static resources
    ├── form-template.txt
    ├── schema.json
    └── icon.png
```

### Conventions

- **SKILL.md** (uppercase preferred, though `skill.md` is accepted)
- **No extraneous files**: Don't include README.md, CHANGELOG.md, or other cruft
- **Scripts self-contained**: Either a single tool with no deps, or clearly documented
- **One level deep references**: Avoid nesting `references/subdir/file.md`
- **Relative paths**: Use `references/GUIDE.md`, not absolute paths or `../`

### What Goes Where?

| Item | Location | Notes |
|------|----------|-------|
| Step-by-step procedures | SKILL.md body | Core instructions |
| API endpoint docs | `references/API.md` | Supplementary detail |
| Code to extract data | `scripts/extract.py` | Executable, deterministic |
| Form template | `assets/form.txt` | Output artifact |
| Troubleshooting tips | `references/TROUBLESHOOTING.md` | Reference material |

---

## Part 6: Validation

Use the **skills-ref** CLI to validate SKILL.md files:

```bash
# Validate a single skill
skills-ref validate ./pdf

# Validate all skills in a directory
skills-ref validate ./skills

# Get structured output
skills-ref read-properties ./pdf
```

### Validation Checklist

1. ✓ SKILL.md exists (case-insensitive)
2. ✓ Frontmatter is valid YAML
3. ✓ **name** field is present and valid (kebab-case, matches directory)
4. ✓ **description** field is present (1–1024 chars)
5. ✓ **compatibility** field is ≤500 chars (if present)
6. ✓ No unknown fields (only whitelisted: name, description, license, compatibility, metadata, allowed-tools)
7. ✓ **Body** is ≤500 lines (hard limit)
8. ✓ **Body** is ~<5000 tokens (advisory, for context efficiency)
9. ✓ No directory traversal in resource references (e.g., no `../../etc/passwd`)
10. ✓ Metadata has no duplicate keys

### Validation Errors

**Hard errors** (prevent use):
- Missing SKILL.md
- Invalid YAML frontmatter
- Missing required fields (name, description)
- Invalid name (wrong characters, too long, doesn't match directory)
- Unknown frontmatter fields
- Body exceeds 500 lines

**Warnings** (advisory):
- Body approaches 5000 tokens
- Compatibility exceeds 500 chars
- Name doesn't match directory (legacy skills)

---

## Part 7: Integration with Agent Systems

### For Agent Builders

To integrate skills into your agent:

1. **Discover** skills in designated directories:
   ```bash
   skills-ref validate ./skills
   ```

2. **Extract metadata** at startup:
   ```python
   from skills_ref import read_properties
   props = read_properties("./pdf")
   # props.name, props.description, props.license, ...
   ```

3. **Match requests** to skills semantically:
   - Use name + description to find relevant skills
   - Filter by allowed-tools if provided

4. **Load instructions** when activated:
   ```python
   from skills_ref import to_prompt
   xml = to_prompt(["./pdf", "./xlsx"])
   # Inject <available_skills>...</available_skills> into system prompt
   ```

5. **Execute resources** on demand:
   - Run scripts in isolated environments
   - Load references as context
   - Retrieve assets for output generation

6. **Log and audit**:
   - Track which skills were loaded and when
   - Validate tool usage against allowed-tools whitelist
   - Maintain execution logs for compliance

### Security Considerations

- **Execute in isolation**: Run skill scripts in sandboxed environments
- **Trust boundaries**: Only execute scripts from trusted skill sources
- **User approval**: Obtain consent before dangerous operations (file deletion, network access)
- **Path traversal**: Validate that resource references don't escape the skill directory
- **Tool whitelisting**: Respect the `allowed-tools` field; don't grant skills access beyond their scope

---

## Part 8: Examples

### Minimal Skill

```yaml
---
name: hello
description: A simple greeting skill for testing agent integration.
---

# Hello Skill

Say hello to the world.

## Usage

Just ask the agent to greet you!
```

### Full-Featured Skill

See the `references/FULL_EXAMPLE.md` for a comprehensive example with all optional fields, metadata, and script references.

---

## Part 9: Best Practices

### For Skill Authors

1. **Keep metadata tight**: Name and description should be ~100 tokens total
2. **Use progressive disclosure**: Don't cram everything into SKILL.md; link to references
3. **Document decision boundaries**: Explain when to use and when NOT to use this skill
4. **Version your skills**: Add `version` to metadata; bump on breaking changes
5. **Test validation**: Run `skills-ref validate` before publishing
6. **Name clearly**: Use kebab-case names that hint at function (e.g., `pdf-extraction` not `doc-proc`)
7. **Include examples**: Show input/output; help agents understand scope
8. **Provide troubleshooting**: Common errors and solutions in a reference

### For Agent Builders

1. **Load metadata at startup**: ~100 tokens per skill is acceptable
2. **Match before loading full instructions**: Use semantic search on name + description
3. **Cache instructions**: Load full SKILL.md body only once per session
4. **Respect allowed-tools**: Don't bypass tool restrictions
5. **Log all skill activations**: For debugging and compliance
6. **Graceful degradation**: If a script fails, provide helpful fallbacks
7. **Document constraints**: Tell users which skills you support

---

## Part 10: Relationship to agentskills.io

This skill **IS** the agentskills.io specification, formatted as a self-referential skill. It teaches agents how to:

- Read and understand SKILL.md files
- Validate skill metadata against the spec
- Integrate skills into agent systems
- Author new skills
- Reason about progressive disclosure and context efficiency

The specification itself is maintained at:
- **Spec site**: https://agentskills.io/specification
- **CLI tool**: https://github.com/agentskills/agentskills (skills-ref)
- **Example skills**: https://github.com/anthropics/skills

---

## Part 11: Tooling

### skills-ref (Python CLI)

```bash
# Installation
pip install skills-ref
# or
uv pip install skills-ref

# Subcommands
skills-ref validate <path>              # Check if valid
skills-ref read-properties <path>       # Output JSON metadata
skills-ref to-prompt <path> [<path>...] # Generate XML for agents
```

### boxxy (Go skill system)

The Boxxy skill system adds:
- **GF(3) trit-based classification**: Each skill gets a color-coded role (Generator, Coordinator, Verifier)
- **Glamour rendering**: Rich terminal output with trit-colored themes
- **Batch operations**: Validate and render multiple skills with `ValidateDir` and `RenderTriadSummary`
- **Conservation laws**: Balanced skill sets satisfy `∑ trits ≡ 0 (mod 3)` for triadic harmony

See `/Users/bob/i/boxxy/internal/skill/` for implementation.

---

## Part 12: Formal Specification (Dafny)

A complete formal specification of the agentskills spec is maintained in **AgentSkills.dfy** with predicates for:
- Name validation (`IsValidSkillName`)
- Description constraints (`IsValidDescription`)
- Frontmatter structure (`IsValidFrontmatter`)
- Directory layout (`IsValidSkillDirectory`)
- Progressive disclosure (`IsValidLevel1`, `IsValidLevel2`, `IsValidLevel3`)
- Complete skill validity (`IsValidCompleteSkill`)

Every predicate translates 1:1 to Go validation logic in `boxxy/internal/skill/skill.go`, verified by exhaustive unit tests.

---

## References

- **Official Spec**: https://agentskills.io/specification
- **Skills CLI**: https://github.com/agentskills/agentskills
- **Example Skills**: https://github.com/anthropics/skills
- **Boxxy Implementation**: https://github.com/bmorphism/boxxy
- **Dafny Spec**: `verified/AgentSkills.dfy` (this repo)

---

## Troubleshooting

### My skill fails validation
1. Check SKILL.md formatting: ensure it starts with `---` on its own line
2. Validate name: lowercase, no leading/trailing/consecutive hyphens, matches directory
3. Check YAML: use `python3 -c "import yaml; yaml.safe_load(open('SKILL.md'))"` to debug
4. Frontmatter fields: only use `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`

### Body exceeds 500 lines
Split content: move detailed guides to `references/GUIDE.md`, scripts to `scripts/`, and keep SKILL.md focused on quick start and key concepts.

### Agents don't find my skill
Ensure the skill directory name matches the **name** field exactly (both kebab-case). Run `skills-ref validate ./your-skill` to confirm.

### Unicode/encoding issues
Ensure SKILL.md is UTF-8 encoded. Use NFKC normalization for the name field.

---

**This skill is self-validating**: it teaches agents to read skills, and it is itself a valid skill according to this specification. ✓
