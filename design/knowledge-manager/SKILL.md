---
name: knowledge-manager
description: Manages a structured knowledge base of patterns, troubleshooting guides, best practices, and workflows. Activates when discovering reusable insights, solving technical problems, or establishing new standards. Records knowledge in categorized files for future reference without bloating global CLAUDE.md.
allowed-tools: [Read, Write, Glob, Grep, AskUserQuestion]
---

# Knowledge Manager Skill

## Purpose

Maintain a structured, searchable knowledge base that captures project learnings without bloating global CLAUDE.md. Uses progressive disclosure: knowledge is referenced only when relevant to the current task.

## Knowledge Categories

### 1. Patterns (`~/.claude/knowledge/patterns/`)

Reusable design patterns, architectural solutions, and code structures.

**When to record**:

- Discovering a reusable solution to a recurring problem
- Implementing a design pattern worth documenting
- Finding a cross-stack applicable approach

### 2. Troubleshooting (`~/.claude/knowledge/troubleshooting/`)

Technical issues, error resolutions, and debugging guides.

**When to record**:

- Solving a non-obvious technical problem
- Resolving environment-specific issues
- Documenting error messages and solutions

### 3. Best Practices (`~/.claude/knowledge/best-practices/`)

Standards, conventions, and quality guidelines.

**When to record**:

- Establishing a new coding standard
- Discovering a performance optimization technique
- Defining security or quality guidelines

### 4. Workflows (`~/.claude/knowledge/workflows/`)

Process documentation, CI/CD patterns, and operational procedures.

**When to record**:

- Defining a new development workflow
- Documenting release processes
- Establishing CI/CD patterns

## Recording Process

### Step 1: Detection

Identify potentially valuable knowledge during development.

### Step 2: Categorization

Determine the appropriate category:

- **Pattern**: Reusable code/architecture structure
- **Troubleshooting**: Problem resolution
- **Best Practice**: Quality/performance guideline
- **Workflow**: Process or operational procedure

### Step 3: Template Selection

Use the appropriate template from `~/.claude/skills/knowledge-manager/templates/`

### Step 4: Documentation

Create or update the knowledge file:

1. Read the category INDEX.md
2. Check for existing related entries
3. Create new file or update existing one
4. Update INDEX.md with new entry
5. Cross-reference related knowledge

### Step 5: Verification

Ask user to review before committing.

## Search and Retrieval

When user asks about a topic:

1. Check relevant INDEX.md files
2. Read only the specific knowledge files needed
3. Provide answer with knowledge source references

## Integration with Existing Systems

### Troubleshooting Migration

Existing `~/.claude/troubleshooting/` files should be:

1. Moved to `~/.claude/knowledge/troubleshooting/`
2. Added to troubleshooting INDEX.md
3. Symlinked from old location for compatibility

### Global CLAUDE.md Optimization

Keep global CLAUDE.md minimal:

- Core principles only
- Reference to knowledge-manager Skill
- No detailed patterns or troubleshooting

## Maintenance

### Regular Tasks

- Review and update INDEX files
- Archive low-value knowledge
- Consolidate duplicate entries
- Update cross-references

### Quality Standards

- Clear, scannable titles
- Consistent template usage
- Proper categorization
- Accurate INDEX entries

## Evaluation Criteria

Assess discoveries against three dimensions:

1. **Reusability**: Can this be applied across different projects and tech stacks?
2. **Impact**: Does it significantly improve code quality, maintainability, or performance?
3. **Learning Value**: Will it elevate the team's technical capabilities?

Score each dimension (Low/Medium/High). Propose for knowledge base if at least 2/3 are Medium or higher.

## Presentation Format

When proposing new knowledge entry:

1. **Summary**: Brief description (1-2 sentences)
2. **Category**: Which category it belongs to
3. **Context**: Where and how it was discovered
4. **Evaluation**: Scores for Reusability, Impact, Learning Value
5. **Proposed Entry**: Show the formatted knowledge entry
6. **Application Examples**: 2-3 scenarios where this applies

Ask user for approval before creating the entry.
