---
name: marketplace-analysis
description: Use when reviewing plugin quality, auditing plugins, analyzing the marketplace, checking plugins against Anthropic standards, or evaluating plugin architecture - provides systematic analysis methodology with validation framework
---

# Marketplace Analysis

Analyze Claude Code plugins to achieve Anthropic-level quality standards.

## Core Philosophy

**Anthropic Quality Bar**: Same or more functionality with leaner, more efficient implementation.

**Principles:**

- Systems thinking over point fixes
- Elegant simplicity over feature accumulation
- Proven improvements over assumptions
- Deletion over addition

## Analysis Process

### 1. Quick Scan

- Count plugins and components
- Note obvious issues (large files, naming inconsistencies)
- Flag files >500 lines

### 2. Deep Analysis (per plugin)

1. Read SKILL.md files - check trigger phrases, writing style
2. Read agent descriptions - check triggering examples
3. Read commands - check argument handling
4. Check hooks - validate event usage
5. Map interactions - how components work together

### 3. Cross-Plugin Analysis

- Find redundancy across plugins
- Check consistency (naming, patterns, styles)
- Identify gaps and conflicts

### 4. Reference Validation

For each skill, verify bundled references exist:

1. **Extract paths from SKILL.md:**
   - `references/*.md` mentions
   - `scripts/*.sh` or `scripts/*.py` mentions
   - Markdown links: `[text](relative/path)`

2. **Validate each path:**
   - Resolve relative to skill directory
   - Check file exists with Glob
   - Flag missing as "broken reference"

3. **Report:**
   - Missing references = Priority 1 errors
   - Orphaned files (exist but not referenced) = Priority 3 notes

## Anti-Overengineering Checks

Before proposing ANY change:

1. Is this simpler than the original?
2. Does this solve a real problem?
3. Would a new user understand this?
4. Can I remove instead of add?

**Red flags:**

- Adding abstraction for one use case
- "Might need this later" reasoning
- Recommending deletion based on filename alone

## Output Format

```markdown
## Priority 1: High Impact, Low Effort
- [ ] [Change] - [Why] - [Expected impact] - [How to validate]

## Priority 2: Medium Impact
...

## Priority 3: Consider Later
...
```

Each recommendation includes validation approach.

## References

For detailed guidance:

- **`references/skill-design-standards.md`** - **Official Anthropic skill-creator guide** (authoritative source for skill structure, frontmatter, progressive disclosure)
- **`references/quality-standards.md`** - Quality criteria checklist, anti-patterns (includes summary of official standards)
- **`references/measuring-improvements.md`** - Metrics, user testing, validation templates
- **`references/output-patterns.md`** - Template and examples patterns for consistent output
- **`references/workflows.md`** - Sequential and conditional workflow patterns

Use `scripts/analyze-metrics.sh` for consistent metric collection.

## Consulting Documentation

Verify best practices via `claude-code-guide` subagent before claiming something is "wrong."

## Applying Changes

When implementing improvements:

1. **Before any changes:** Create TodoWrite items for each improvement
2. **Apply changes:** Use Edit tool, one logical change at a time
3. **MANDATORY verification:** Use `core:verification` skill before claiming complete
4. **Evidence required:** Run validation commands, report actual output

**Never claim "improved" or "fixed" without verification evidence.**
