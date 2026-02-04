---
name: skill-optimizer
description: Optimize Claude Code skills for token efficiency using progressive disclosure and content loading order. Use when optimizing skills, reducing token usage, restructuring skill content, improving skill performance, analyzing skill size, applying 500-line rule, implementing progressive disclosure, organizing reference files, optimizing YAML frontmatter, reducing context consumption, improving skill architecture, analyzing token costs, splitting large skills, or working with skill content loading. Covers Level 1 (metadata), Level 2 (instructions), Level 3 (resources) loading optimization.
---

# Skill Optimizer

## Purpose

Optimize existing Claude Code skills to minimize token consumption by leveraging the three-level content loading architecture and progressive disclosure patterns.

## When to Use

Use this skill when:
- Analyzing existing skills for optimization opportunities
- Skills are too large (approaching or exceeding 500 lines)
- Need to reduce context consumption
- Restructuring skills for progressive disclosure
- Converting monolithic skills to multi-file architecture
- Optimizing YAML frontmatter for better discovery
- Improving skill performance and load times
- Auditing skills for token efficiency
- Creating new skills with optimization in mind

---

## Content Loading Architecture

### Three-Level Loading System

**Level 1: Metadata (Always Loaded - ~100 tokens/skill)**
- YAML frontmatter in SKILL.md
- Loaded at startup into system prompt
- Enables skill discovery without context overhead
- **Optimization Target**: Description field (max 1024 chars)

**Level 2: Instructions (Loaded When Triggered - <5,000 tokens)**
- Main SKILL.md content
- Loads dynamically when skill is relevant
- Contains workflows, best practices, guidance
- **Optimization Target**: Keep under 500 lines

**Level 3: Resources (Loaded As Needed - Variable)**
- Additional markdown files (REFERENCE.md, EXAMPLES.md, etc.)
- Code scripts in scripts/ directory
- Templates, schemas, documentation
- **Optimization Target**: No penalty until accessed

### Key Principle

**"Files don't consume context until accessed"** - Bundle comprehensive documentation in reference files without context penalty.

---

## Quick Optimization Workflow

### 1. Analyze Current State

**Check skill size:**
```bash
wc -l .claude/skills/skill-name/SKILL.md
```

**Identify optimization opportunities:**
- [ ] SKILL.md > 500 lines?
- [ ] Detailed API docs in main file?
- [ ] Extensive examples in main file?
- [ ] Long reference tables or schemas?
- [ ] Code snippets that could be scripts?
- [ ] Multiple distinct topics/sections?

### 2. Apply 500-Line Rule

**If SKILL.md > 500 lines:**

✅ **Keep in main file:**
- Purpose and when to use
- Quick start / common workflows
- Critical best practices
- Brief examples (5-10 lines)
- Cross-references to detailed files

❌ **Move to reference files:**
- Comprehensive API documentation
- Extensive code examples (>20 lines)
- Detailed troubleshooting guides
- Pattern libraries
- Schema definitions
- Long reference tables

### 3. Structure Reference Files

**Create organized reference hierarchy:**
```
skill-name/
├── SKILL.md              # <500 lines, workflows & quick ref
├── REFERENCE.md          # Comprehensive documentation
├── EXAMPLES.md           # Detailed code examples
├── PATTERNS.md           # Pattern library
├── TROUBLESHOOTING.md    # Debug guide
└── scripts/              # Executable utilities
    └── helper.sh
```

**Add table of contents to files >100 lines**

### 4. Optimize YAML Frontmatter

**Description optimization (max 1024 chars):**

✅ **Include:**
- All trigger keywords and phrases
- Use cases and scenarios
- File types and technologies
- Common action verbs
- Related concepts

❌ **Avoid:**
- Generic descriptions
- Missing key terms
- Overly verbose explanations

**Example:**
```yaml
---
name: database-development
description: Database development guidance for PostgreSQL including schema design, migrations, RLS policies, indexing strategies, privacy-preserving patterns, query optimization, and Prisma ORM. Use when working with tables, columns, indexes, migrations, RLS, Row-Level Security, database schema, SQL queries, Prisma schema, database optimization, privacy architecture, or PostgreSQL best practices.
---
```

### 5. Implement Progressive Disclosure

**Pattern:**
```markdown
## Topic Overview

Brief explanation (2-3 sentences).

**Key Points:**
- Important consideration 1
- Important consideration 2

**For detailed information**: [REFERENCE.md](REFERENCE.md#topic-details)

**Quick Example:**
\`\`\`typescript
// Minimal working example (5-10 lines)
\`\`\`

**For more examples**: [EXAMPLES.md](EXAMPLES.md#topic-examples)
```

---

## Optimization Patterns Summary

### Pattern 1: Extract API Documentation

**Strategy**: Move detailed API docs to REFERENCE.md

**Before**: 80+ lines of API documentation in SKILL.md
**After**: 10-line summary with link to complete docs
**Savings**: ~70 lines (~1,400 tokens)

**For complete pattern details**: [REFERENCE.md](REFERENCE.md#pattern-1-extract-api-documentation)

### Pattern 2: Extract Pattern Libraries

**Strategy**: Move code patterns to PATTERNS.md

**Before**: 200+ lines of pattern code in SKILL.md
**After**: 18-line summary with quick example
**Savings**: ~182 lines (~3,640 tokens)

**For complete pattern details**: [REFERENCE.md](REFERENCE.md#pattern-2-extract-pattern-libraries)

### Pattern 3: Extract Troubleshooting

**Strategy**: Move debug guides to TROUBLESHOOTING.md

**Before**: 300+ lines of troubleshooting in SKILL.md
**After**: 18-line summary with quick diagnostics
**Savings**: ~282 lines (~5,640 tokens)

**For complete pattern details**: [REFERENCE.md](REFERENCE.md#pattern-3-extract-troubleshooting)

### Pattern 4: Convert Code to Scripts

**Strategy**: Move executable code to scripts/ directory

**Before**: 55+ lines of bash script in SKILL.md
**After**: 7-line reference to executable script
**Savings**: ~48 lines (~960 tokens) + script code never enters context

**For complete pattern details**: [REFERENCE.md](REFERENCE.md#pattern-4-convert-code-to-scripts)

---

## Common Anti-Patterns

Avoid these common mistakes when creating or optimizing skills:

❌ **Anti-Pattern 1: Monolithic Skills**
- Single SKILL.md with 1000+ lines
- Solution: Split into main + reference files

❌ **Anti-Pattern 2: Incomplete References**
- Reference files exist but not linked
- Solution: Link all reference files from SKILL.md

❌ **Anti-Pattern 3: Nested References**
- References pointing to other references (>1 level)
- Solution: Keep hierarchy flat (max 1 level)

❌ **Anti-Pattern 4: Sparse Frontmatter**
- Minimal YAML description missing keywords
- Solution: Rich description with all triggers

❌ **Anti-Pattern 5: Code as Documentation**
- 100+ line scripts embedded in markdown
- Solution: Move to scripts/ directory

**For detailed anti-patterns and solutions**: [REFERENCE.md](REFERENCE.md#common-anti-patterns)

---

## Migration Workflow

### Quick Migration Steps

**Phase 1: Discovery**
```bash
# Check skill size
wc -l .claude/skills/skill-name/SKILL.md

# Identify sections to extract
grep "^##" .claude/skills/skill-name/SKILL.md
```

**Phase 2: Planning**
- Design file hierarchy (SKILL.md + reference files)
- Plan content distribution
- Identify scripts to extract

**Phase 3: Implementation**
```bash
# Create reference files
touch REFERENCE.md EXAMPLES.md
mkdir -p scripts

# Extract content systematically
# 1. Copy section to reference file
# 2. Replace in SKILL.md with summary + link
# 3. Verify link works
# 4. Remove detailed content from SKILL.md
```

**Phase 4: Optimization**
- Trim remaining content
- Optimize frontmatter with trigger keywords
- Add navigation aids (table of contents)

**Phase 5: Validation**
```bash
# Verify under 500 lines
wc -l .claude/skills/skill-name/SKILL.md

# Test links work
grep -o '\[.*\](.*\.md#.*)' SKILL.md
```

**For complete migration workflow**: [REFERENCE.md](REFERENCE.md#complete-migration-workflow)

---

## Advanced Techniques

Quick reference to advanced optimization strategies:

**Technique 1: Conditional Content Loading**
- Structure content so advanced sections load only when needed
- Benefits: Most users don't load advanced content

**Technique 2: Layered Examples**
- Progressive complexity: minimal → production → enterprise
- Benefits: Beginners see simple examples, advanced users access complex ones

**Technique 3: Executable Documentation**
- Scripts that both execute and document
- Benefits: Zero token cost, self-documenting output

**Technique 4: Tabular Compression**
- Use tables to compress structured data
- Benefits: 60%+ space reduction for configurations/options

**Technique 5: Smart Chunking**
- Group related small sections instead of individual extraction
- Benefits: Better narrative flow, fewer cross-references

**For detailed advanced techniques**: [REFERENCE.md](REFERENCE.md#advanced-optimization-techniques)

---

## Optimization Checklist

When optimizing a skill, verify:

### Content Structure
- [ ] SKILL.md is under 500 lines
- [ ] Main file contains quick reference only
- [ ] Detailed docs moved to reference files
- [ ] Reference files have table of contents (if >100 lines)
- [ ] Cross-references use relative links
- [ ] No deeply nested references (max 1 level)

### YAML Frontmatter
- [ ] Description includes all trigger keywords
- [ ] Description is under 1024 characters
- [ ] Description covers use cases and scenarios
- [ ] Description mentions file types/technologies
- [ ] Name follows kebab-case convention

### Progressive Disclosure
- [ ] Overview → Details pattern used
- [ ] Quick examples in main file (5-10 lines)
- [ ] Extensive examples in EXAMPLES.md
- [ ] Brief summaries with references to details
- [ ] Common workflows highlighted in main file

### File Organization
- [ ] Reference files named clearly
- [ ] Scripts in scripts/ directory
- [ ] Scripts are executable (chmod +x)
- [ ] No redundant content across files
- [ ] Each file has single, clear purpose

### Token Efficiency
- [ ] Eliminated verbose explanations
- [ ] Removed duplicate information
- [ ] Used bullet points vs paragraphs
- [ ] Moved large code blocks to reference files
- [ ] Converted reusable code to scripts

---

## Measurement & Validation

### Token Estimation

**Quick estimate:**
```bash
lines=$(wc -l < SKILL.md)
tokens=$((lines * 20))  # Conservative: 20 tokens/line
echo "Estimated tokens: ~$tokens"
```

**Target**: Keep SKILL.md under 10,000 tokens (~500 lines)

### Before/After Comparison

```bash
# Calculate savings
BEFORE=850  # lines before optimization
AFTER=420   # lines after optimization
SAVINGS=$((BEFORE - AFTER))
TOKEN_SAVINGS=$((SAVINGS * 20))

echo "Reduced by $SAVINGS lines"
echo "Estimated token savings: ~$TOKEN_SAVINGS tokens"
```

### Quality Checks

- [ ] All original information preserved
- [ ] Links work correctly
- [ ] Main file comprehensive for common cases
- [ ] Reference files well-organized
- [ ] Navigation intuitive

**For detailed measurement methods**: [REFERENCE.md](REFERENCE.md#measurement--validation)

---

## Best Practices Summary

✅ **DO:**
- Keep SKILL.md minimum but use other reference files to keep the full and detailed knowledge base
- Use progressive disclosure (overview → details)
- Include all trigger keywords in description
- Create clear cross-references to detailed docs
- Add table of contents to reference files >100 lines
- Convert reusable code to scripts
- Test optimization with real usage

❌ **DON'T:**
- Exceed 500 lines in SKILL.md
- Nest references more than 1 level deep
- Include API docs in main file
- Embed long code examples in main file
- Create reference files without linking them
- Use sparse YAML descriptions
- Optimize without preserving critical info

---

## Quick Reference

**File size limits:**
- SKILL.md: <500 lines (strict)
- Reference files: No limit (loaded on-demand)
- YAML description: 1024 chars max

**Optimization priority:**
1. Apply 500-line rule to SKILL.md
2. Extract API docs to REFERENCE.md
3. Move examples to EXAMPLES.md or PATTERNS.md
4. Convert scripts to scripts/ directory
5. Enrich YAML frontmatter description

**Common extractions:**
- API documentation → REFERENCE.md
- Code examples → EXAMPLES.md
- Troubleshooting → TROUBLESHOOTING.md
- Pattern library → PATTERNS.md
- Scripts → scripts/ directory

**Typical token savings:**
- API extraction: ~1,400 tokens
- Pattern library: ~3,640 tokens
- Troubleshooting: ~5,640 tokens
- Scripts: ~960 tokens + no code in context

**For comprehensive optimization patterns and detailed workflows**: [REFERENCE.md](REFERENCE.md)

---

## Real-World Example

**Before optimization:**
```
skill-example/
└── SKILL.md  (850 lines, ~17,000 tokens)
```

**After optimization:**
```
skill-example/
├── SKILL.md              (420 lines, ~8,400 tokens)
├── REFERENCE.md          (350 lines, loaded on-demand)
├── EXAMPLES.md           (180 lines, loaded on-demand)
└── scripts/
    ├── validate.sh       (code never enters context)
    └── setup.sh          (code never enters context)
```

**Result**: 50% token reduction on initial load, comprehensive docs still available on-demand

---

**Next Steps**:
1. Audit existing skills: `wc -l .claude/skills/*/SKILL.md`
2. Identify candidates for optimization (>500 lines)
3. Apply optimization workflow
4. Measure token savings
5. Validate with real usage

**For detailed guidance**: See [REFERENCE.md](REFERENCE.md) for complete optimization patterns, anti-patterns, migration workflows, and advanced techniques.
