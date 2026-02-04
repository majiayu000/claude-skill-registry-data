---
name: maintain-docs
description: Update and maintain documentation to reflect current implementation after code changes, refactoring, or new features. Remove temporal language, verify accuracy against code, and keep docs current. Use when updating docs, syncing documentation, removing outdated info, or after implementing features.
---

# Documentation Maintainer

Maintain clean, accurate, implementation-focused documentation that works seamlessly with the `doc-lookup` skill. Ensure docs always reflect current state, are structured for targeted retrieval, and include stable anchors.

## Core Principles

1. **Present State Focus**: Describe what IS implemented, not what WAS changed. Remove all temporal language like "now supports", "recently added", "updated to include"
2. **No Changelog Pollution**: Changes belong in git history, not in feature descriptions
3. **Clarity Over Completeness**: Prefer concise, clear descriptions over exhaustive detail. Every sentence must add value
4. **Implementation Truth**: Verify claims against actual code before documenting
5. **Single Source of Truth**: Each piece of information should exist in exactly one canonical location. Use cross-references with anchors instead of duplicating content
6. **Retrieval-Ready Structure**: Organize docs with stable anchors and self-contained sections for doc-lookup skill

## Update Workflow

1. **Audit**: Verify what's actually implemented
2. **Add/verify anchors**: Ensure all major sections have stable anchors (see Anchor Guidelines below)
3. **Remove temporal language**: "Recently added", "Now supports", "Updated to", "As of version X"
4. **Consolidate**: Merge duplicates, remove repetition, use anchor cross-references
5. **Verify**: Cross-reference with actual code
6. **Test retrieval**: Verify key sections can be found with doc-lookup skill
7. **Maintain structure**: Preserve organization unless improvement needed

## Helper Scripts {#helper-scripts}

The maintain-docs skill includes helper scripts for anchor management:

```bash
# Add anchors to documentation (dry-run first to preview)
python .claude/skills/maintain-docs/scripts/add_doc_anchors.py <path> --dry-run
python .claude/skills/maintain-docs/scripts/add_doc_anchors.py <path> [--recursive]

# Validate router skill references
python .claude/skills/maintain-docs/scripts/validate_doc_anchors.py

# Or use Makefile shortcuts
make docs-add-anchors-dry    # Preview anchor additions
make docs-add-anchors        # Add anchors to features/formats/projects docs
make docs-validate-anchors   # Validate router skill references
```

See [DOCUMENTATION_MANAGEMENT.md](references/DOCUMENTATION_MANAGEMENT.md) for complete guide.

## Anchor Guidelines {#anchor-guidelines}

To enable effective doc-lookup, follow these anchor requirements:

### When to Add Anchors

Add explicit anchors `{#anchor-id}` to:
- **All ## (level 2) headings**: Primary sections
- **Important ### (level 3) headings**: Key subsections (CLI commands, specific features, patterns)
- **Reference sections**: That router skills or other docs will link to

**Don't anchor**:
- #### (level 4+) headings unless they're frequently referenced
- Example headings or minor subsections
- Temporary or subject-to-change sections

### Anchor Granularity Policy

**Prefer coarser anchors over fine-grained ones** to improve maintainability and usability:

**Good (Coarser anchors)**:
- `#cli-commands` for a section covering all CLI commands
- `#mcp-tools` for a section listing all MCP tools
- `#service-architecture` for service patterns overview

**Avoid (Too granular)**:
- `#cli-run-command`, `#cli-results-command`, `#cli-metrics-command` (separate anchors for each command)
- `#mcp-dipeo-run-tool`, `#mcp-list-diagrams-tool` (separate anchors for each tool)
- `#service-registry-registration`, `#service-registry-lookup` (separate anchors for minor subsections)

**Rationale**:
- **Easier maintenance**: Fewer anchors to manage when content evolves
- **Better doc-lookup**: Router skills can reference one anchor instead of many
- **Natural retrieval**: doc-lookup returns the whole section with context
- **Less coupling**: Documentation structure can change without breaking references

**When fine-grained anchors are acceptable**:
- Distinct, complex subsections with >50 lines each
- Subsections referenced independently across multiple docs
- Different conceptual topics that happen to be in the same parent section

### Anchor Naming Conventions

Follow these patterns for consistency:

**Domain-specific prefixes**:
- `#cli-*`: CLI-related sections (`#cli-commands`, `#cli-flags`, `#cli-background`)
- `#mcp-*`: MCP server sections (`#mcp-tools`, `#mcp-registration`, `#mcp-architecture`)
- `#db-*` or `#database-*`: Database sections (`#database-schema`, `#database-queries`)
- `#handler-*`: Handler implementation (`#handler-patterns`, `#handler-lifecycle`)
- `#codegen-*`: Code generation (`#codegen-typescript`, `#codegen-ir-builders`)

**Generic sections**:
- `#overview`: High-level introduction
- `#core-responsibilities`: Main duties/scope
- `#common-patterns`: Usage patterns and examples
- `#troubleshooting`: Common issues and solutions
- `#escalation`: When to hand off to other agents

**Format rules**:
- Use kebab-case: `#my-section-name`
- Be descriptive but concise: `#cli-flags` not `#flags`, `#background-execution` not `#bg`
- Avoid special characters: Only lowercase letters, numbers, and hyphens
- Keep stable: Don't rename anchors without updating references

### Section Organization for doc-lookup

Structure sections to be **self-contained and independently retrievable**:

**Good section** (works well with doc-lookup):
```markdown
## CLI Flags {#cli-flags}

Common flags for all CLI commands:

- `--light`: Use light diagram format (.light.yaml)
- `--debug`: Enable detailed logging to .dipeo/logs/cli.log
- `--timeout N`: Set execution timeout in seconds (default: 120)

Example:
\`\`\`bash
dipeo run my_diagram --light --debug --timeout=60
\`\`\`

See also: [CLI Commands](#cli-commands)
```

**Bad section** (hard to retrieve independently):
```markdown
## CLI

The CLI has various flags that you can use. Some of them are...
[500 lines of mixed commands, flags, examples, troubleshooting]
```

### Cross-Referencing with Anchors

**Instead of duplicating content**, use anchor links:

```markdown
## Background Execution {#background-execution}

For flag details, see [CLI Flags](#cli-flags).
For status checking, see [CLI Commands](#cli-commands).

The background execution system allows...
```

This enables:
- Single source of truth
- Smaller, focused sections
- Easy doc-lookup navigation

## Content Standards

**Good Documentation** (present tense, anchored, self-contained):
```markdown
## Service Registry {#service-registry}

The EnhancedServiceRegistry provides:
- Type categorization for services
- Audit trails for all registrations
- Production safety checks

Location: `/dipeo/infrastructure/service_registry.py`

See also: [EventBus](#eventbus), [Service Architecture](#service-architecture)
```

**Bad Documentation** (temporal language, no anchors):
```markdown
## Service Registry

The service registry was recently enhanced to add type categorization
and audit trails. We've also improved the production safety features.
```

**Documentation Elements**:
- **Present tense**: "provides", "supports", "uses" (not "was enhanced", "now includes")
- **Explicit anchors**: All major sections have `{#anchor-id}`
- **File paths**: When relevant, include actual file locations
- **Cross-references**: Link to related sections with anchors
- **Self-contained**: Section can be understood independently

## Documentation Types

**Architecture Docs** (`docs/architecture/`):
- Current design, relationships, decisions
- Add anchors for key concepts: `#service-architecture`, `#graphql-layer`, etc.
- Remove completed migration notes

**Agent Guides** (`docs/agents/`):
- Domain-specific guidance for specialized agents
- Must have anchors for all major sections (router skills reference these)
- Self-contained sections for doc-lookup retrieval

**Feature Docs** (`docs/features/`):
- Current functionality and usage instructions
- Anchor important sections: `#mcp-tools`, `#diagram-export`, etc.
- Remove outdated workflows

**API Docs**:
- Current endpoints, parameters, responses
- Remove deprecated APIs unless explicitly marked

**READMEs**:
- Concise setup, usage, and reference
- Add anchors if README is long (>200 lines)

## Quality Checklist

Before finalizing updates:

**Content Quality**:
- ✓ Describes current implementation?
- ✓ Verifiable in codebase?
- ✓ Temporal language removed?
- ✓ Simplest accurate description?
- ✓ Adds unique value?
- ✓ Not duplicating content from elsewhere?

**doc-lookup Compatibility**:
- ✓ Major sections (## headings) have explicit anchors?
- ✓ Anchors follow naming conventions (kebab-case, domain prefixes)?
- ✓ Sections are self-contained and independently retrievable?
- ✓ Cross-references use anchors instead of duplicating content?
- ✓ Can key sections be found with doc-lookup skill?

**Testing Retrieval**:
Test that important sections can be retrieved:
```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "your-anchor-name" \
  --paths docs/your-file.md \
  --top 1
```

## Red Flags

**Remove**:
- Historical narratives ("First we did X, then Y")
- Version notes ("In v2.0 we changed...")
- Redundant examples
- Overly detailed obvious concepts
- Apologetic language ("This might...", "Hopefully...")
- Sections without anchors (for level 2 headings)
- Duplicate content that could be cross-referenced
- Monolithic sections that mix multiple topics

**Warning Signs** (sections that need splitting):
- Section longer than 100 lines
- Multiple topics mixed in one section
- Difficult to describe in a single anchor name
- Can't be retrieved independently

## Anchor Stability & Maintenance

### Renaming Anchors

Anchors are referenced by:
- Router skills (`.claude/skills/dipeo-*/SKILL.md`)
- Cross-references in other docs
- External links

**Before renaming an anchor**:
1. Search for all references: `grep -r "your-anchor" .claude/skills/ docs/`
2. Update all references first
3. Then rename the anchor
4. Test with doc-lookup

### Adding New Sections

When adding a new section:
1. Choose a descriptive anchor following naming conventions
2. Ensure section is self-contained
3. Add cross-references to related sections
4. Consider updating router skills if it's a major addition

### Router Skill Sync

After major documentation updates:
1. Check if router skills need updating (`.claude/skills/dipeo-*/SKILL.md`)
2. Verify anchor references are still valid
3. Add new anchors to router skill indexes if needed

## Examples

### Example 1: Updating CLI Documentation

**Before** (no anchors, temporal language):
```markdown
## CLI

The CLI was recently updated to support background execution.
You can now run diagrams in the background using the --background flag.
We've also added better error handling.
```

**After** (anchored, present tense, cross-referenced):
```markdown
## CLI Commands {#cli-commands}

Core commands:
- `dipeo run`: Execute a diagram
- `dipeo results`: Check execution results
- `dipeo metrics`: Profile execution performance

For flags, see [CLI Flags](#cli-flags).
For background execution, see [Background Execution](#background-execution).

## CLI Flags {#cli-flags}

Common flags for all commands:
- `--light`: Use light diagram format
- `--debug`: Enable detailed logging
- `--timeout N`: Set timeout in seconds

## Background Execution {#background-execution}

Execute diagrams asynchronously:

\`\`\`bash
dipeo run my_diagram --background
# Returns: {"session_id": "exec_...", "status": "started"}
\`\`\`

Check results: `dipeo results <session_id>`
```

### Example 2: Architecture Documentation

**Before** (monolithic, no anchors):
```markdown
## Architecture

DiPeO uses a service registry for managing services. It provides
type categorization and audit trails. We also have an EventBus
for communication...
[200 lines of mixed architecture topics]
```

**After** (split sections, anchored):
```markdown
## Service Architecture {#service-architecture}

DiPeO's service layer uses:
- [Service Registry](#service-registry): Type-safe service management
- [EventBus](#eventbus): Unified event protocol
- [Envelope Pattern](#envelope-pattern): Standardized outputs

## Service Registry {#service-registry}

The EnhancedServiceRegistry provides:
- Type categorization (AI, STANDARD, LLM)
- Audit trails for registrations
- Production safety checks

Location: `/dipeo/infrastructure/service_registry.py`

## EventBus {#eventbus}

Unified event protocol for cross-service communication.

Location: `/dipeo/infrastructure/event_bus.py`
```

## Best Practices Summary

1. **Add anchors** to all level 2 headings and important level 3 headings
2. **Use domain prefixes** (#cli-*, #mcp-*, #handler-*) for consistency
3. **Keep sections self-contained** (20-50 lines ideal)
4. **Cross-reference** instead of duplicating content
5. **Test retrieval** with doc-lookup skill
6. **Maintain anchor stability** (update references before renaming)
7. **Sync router skills** after major documentation changes

The goal is documentation that:
- Serves developers efficiently
- Accurately reflects the current system
- Works seamlessly with doc-lookup skill
- Requires minimal maintenance through stable anchors and single source of truth
