---
name: memory-design
description: Interpretive guidance for Claude Code memory management system. Helps choose between memory locations, organize modular rules, use path-specific rules, and avoid common pitfalls. Use when setting up CLAUDE.md files, organizing .claude/rules/ directories, or deciding where to put project instructions.
---

# Memory Design Skill

This skill provides decision frameworks for organizing Claude Code's 4-tier memory hierarchy, modular rules system, and path-specific loading patterns.

## Fundamentals

**Prerequisites:** This skill builds on box-factory-architecture. Load that skill when choosing between memory vs skills vs other component types.

Core principles of Claude Code memory:

- **4-tier hierarchy**: Enterprise → Project (CLAUDE.md) → Project Rules (.claude/rules/) → User (~/.claude/CLAUDE.md) → Project Local (CLAUDE.local.md)
- **Recursive discovery**: Claude searches up from cwd to root, reading all CLAUDE.md files found
- **Progressive disclosure**: Memory is "always loaded", Skills are "load when relevant"
- **Knowledge delta**: Only document what Claude doesn't know about your specific project/workflow

**Deep dive:** box-factory-architecture skill (Progressive Disclosure, Knowledge Delta Filter sections). **Traverse when:** choosing between memory vs skills, understanding component selection. **Skip when:** clear that content belongs in memory.

## Workflow Selection

| If you need to...                   | Go to...                                                                                                                                                               |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Use path-specific conditional rules | [path-specific-rules.md](path-specific-rules.md) - **Traverse when:** implementing conditional loading, frontend/backend split. **Skip when:** simple monolithic setup |
| Set up file imports with @syntax    | [file-imports.md](file-imports.md) - **Traverse when:** importing existing docs, user-specific instructions. **Skip when:** using .claude/rules/ directory             |
| Choose an organization pattern      | [organization-patterns.md](organization-patterns.md) - **Traverse when:** structuring new project, refactoring memory. **Skip when:** clear pattern already            |
| Avoid common mistakes               | [anti-patterns.md](anti-patterns.md) - **Traverse when:** reviewing existing setup, debugging issues. **Skip when:** creating new setup from scratch                   |
| Validate your setup                 | [Quality Checklist](#quality-checklist) below - **Traverse when:** finalizing memory organization. **Skip when:** still in design phase                                |

## Official Documentation

**Fetch when organizing memory (post-training knowledge):**

- **https://code.claude.com/docs/en/memory.md** - Complete memory hierarchy, rules directory, path-specific rules, import syntax

## The 4-Tier Memory Hierarchy (Official Specification)

Claude Code loads memory in this order (highest to lowest priority):

1. **Enterprise policy** - Organization-wide (system location, managed by IT)
2. **Project memory** - Team-shared via git (`./CLAUDE.md` or `./.claude/CLAUDE.md`)
3. **Project rules** - Modular team-shared (`./.claude/rules/*.md`)
4. **User memory** - Personal cross-project (`~/.claude/CLAUDE.md`)
5. **Project local** - Personal project-specific (`./CLAUDE.local.md`, gitignored)

**Key insight:** Higher tiers provide foundation, lower tiers add specificity. All files load automatically at session start.

### Memory Lookup Behavior

**Recursive search:** Claude starts in cwd, recurses UP to root, reading all CLAUDE.md and CLAUDE.local.md files found.

**Nested discovery:** CLAUDE.md files in subtrees under cwd are discovered but only loaded when Claude reads files in those subtrees.

### The Rules Directory

**Location:** `./.claude/rules/` (project level) or `~/.claude/rules/` (user level)

**Behavior:** All `.md` files discovered recursively, loaded with same priority as `.claude/CLAUDE.md`

## When to Use Each Memory Location (Best Practices)

**Use Project Memory (CLAUDE.md) when:**

- Instructions apply to all team members
- Knowledge should be version-controlled
- Content is project architecture, conventions, workflows
- Single file is sufficient (\<200 lines)

**Use Project Rules (.claude/rules/) when:**

- Project memory would exceed ~200 lines
- Multiple independent topics (testing, API design, security)
- Want modular organization by domain
- Need path-specific conditional rules

**Use User Memory (~/.claude/CLAUDE.md) when:**

- Personal preferences across ALL projects
- Your coding style, preferred tools
- Not project-specific, shouldn't be in version control

**Use Project Local (CLAUDE.local.md) when:**

- Personal preferences for THIS project only
- Sandbox URLs, test credentials, local paths
- Experimental or temporary instructions
- Must not be committed to git (auto-gitignored)

### Monolithic vs Modular Decision

**Keep single CLAUDE.md when:**

- Total content < 200 lines
- Topics are interconnected
- Project is small/simple

**Split into .claude/rules/ when:**

- Total content > 200 lines
- Clear independent topics
- Different team members own different domains
- Want path-specific rules

## Memory vs Skills vs CLAUDE.md (Best Practices)

| Put In...        | When...                                                    |
| ---------------- | ---------------------------------------------------------- |
| Memory (rules/)  | Always relevant in this project, loads at session start    |
| Skills           | Loads progressively when topics arise, 20+ lines expertise |
| Single CLAUDE.md | Simple project, \<200 lines, interconnected content        |

**The boundary:** Memory is "always loaded context", Skills are "load when relevant"

## Quality Checklist

Before finalizing memory organization:

**Memory location:**

- [ ] Project-wide rules in CLAUDE.md or .claude/rules/ (version-controlled)
- [ ] Personal preferences in ~/.claude/CLAUDE.md or CLAUDE.local.md
- [ ] Secrets/credentials only in CLAUDE.local.md (gitignored)
- [ ] Chose monolithic vs modular based on size/complexity (monolithic \<200 lines, modular >200 lines)

**Rules directory:**

- [ ] Each file focuses on one cohesive topic (can describe purpose in one sentence without "and")
- [ ] File has >20 lines of substantive content
- [ ] Subdirectories used for logical grouping by domain
- [ ] No duplicate rules across multiple files (single source of truth)

**Path-specific rules:**

- [ ] `paths` field only when rules truly specific to file subset
- [ ] Glob patterns are clear and maintainable (no overly complex patterns)
- [ ] No overly broad (`**/*`) or overly narrow (single file) patterns
- [ ] No competing/overlapping path patterns across files

**File imports:**

- [ ] Import syntax only in CLAUDE.md content (not in code blocks)
- [ ] No import cycles (design like dependency tree)
- [ ] Import depth < 3 hops (well under 5 limit)
- [ ] Imports point to stable, maintained files

## Documentation References

- https://code.claude.com/docs/en/memory.md - Official memory documentation
- box-factory-architecture skill - Understanding when memory vs skills
- plugin-design skill - Organizing plugin-level CLAUDE.md files
