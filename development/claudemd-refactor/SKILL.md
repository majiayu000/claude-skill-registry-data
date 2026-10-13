---
name: claudemd-refactor
description: "Refactor and optimize CLAUDE.md files in a repository. Analyzes the existing setup, explores repo structure, proposes splitting CLAUDE.md into a hierarchical directory-scoped structure. Use when: (1) User wants to optimize CLAUDE.md, (2) Root CLAUDE.md is too large, (3) User wants to split CLAUDE.md into directory-scoped files, (4) User mentions 'refactor CLAUDE.md', 'split CLAUDE.md', or 'organize CLAUDE.md'."
---

# Refactor CLAUDE.md

Analyze and refactor CLAUDE.md files in the current repository to optimize how context is delivered to Claude Code.

## Context Loading Reliability Hierarchy

When deciding where to place information, follow this hierarchy (most to least reliable):

| Approach | Reliability | Tradeoff |
|---|---|---|
| Inline in CLAUDE.md | Highest | Larger CLAUDE.md |
| Directory-scoped CLAUDE.md | High | Content must be relevant to that directory |
| Explicit "read before doing X" | Medium | Depends on Claude following the instruction |
| Passive "refer to file" | Low | Claude may or may not read it |

**Key principle**: Claude Code automatically loads CLAUDE.md files based on the working directory. Root CLAUDE.md is always loaded. Subdirectory CLAUDE.md files are loaded when working on files in that directory. Content in CLAUDE.md is always in context — no tool call needed.

## Workflow

### Phase 1: Explore and Analyze

1. **Find all existing CLAUDE.md files** in the repo

   ```
   Glob: **/CLAUDE.md
   ```

2. **Read the root CLAUDE.md** — understand what's currently there, measure its size

3. **Explore the repo structure** — understand the directory layout, identify logical boundaries
- What are the major directories? (src/, docs/, scripts/, tests/, etc.)
- What languages/frameworks are used?
- Are there distinct subsystems with their own conventions?

4. **Categorize the content** in the existing root CLAUDE.md into buckets:
- **Global**: Project-wide info that applies everywhere (project name, tech stack, overall architecture, global conventions)
- **Directory-specific**: Rules that only apply to certain directories (e.g., "use camelCase in src/", "frontmatter required in docs/")
- **Task-specific**: Instructions tied to specific operations (e.g., "before modifying API routes, read api-design.md")
- **Redundant/outdated**: Content that can be removed

### Phase 2: Propose a Plan

Present the user with a concrete proposal. Include:

1. **Current state summary**
- Number of CLAUDE.md files found
- Root CLAUDE.md size (lines/sections)
- Content categories identified

2. **Proposed CLAUDE.md structure** — show a tree like:

   ```
   repo/
   ├── CLAUDE.md              # Global: project overview, tech stack, universal conventions
   ├── src/
   │   └── CLAUDE.md          # Code: naming conventions, import rules, architecture patterns
   ├── docs/
   │   └── CLAUDE.md          # Docs: writing style, frontmatter, formatting rules
   └── tests/
       └── CLAUDE.md          # Tests: testing conventions, fixture locations, coverage rules
   ```

3. **For each proposed CLAUDE.md**, list:
- What content moves there (with specific sections/lines from original)
- What stays in root
- Any new content needed (e.g., cross-references)

4. **Migration of "refer to" patterns** — identify any passive references and propose upgrades:
- Passive → Inline (if content is small and critical)
- Passive → Explicit trigger ("Before modifying X, read Y")
- Keep as passive (only if truly optional background info)

### Phase 3: Ask for User Approval

**IMPORTANT**: Do NOT proceed without explicit user approval. Present the plan and ask:

- Does the proposed structure make sense for this repo?
- Should any content stay in root instead of being split?
- Are there directories that should have their own CLAUDE.md that weren't identified?
- Any content that should be removed entirely?

### Phase 4: Execute the Refactoring

After approval:

1. **Create directory-scoped CLAUDE.md files** with the approved content
2. **Trim the root CLAUDE.md** — remove content that was moved to subdirectories
3. **Upgrade passive references** — replace "refer to X" with inline content or explicit triggers
4. **Add cross-references where needed** — if root CLAUDE.md needs to mention that subdirectory rules exist

### Phase 5: Verify

1. Read each created/modified CLAUDE.md to verify correctness
2. Ensure no critical information was lost
3. Check that the root CLAUDE.md is noticeably smaller but still contains all global info
4. Present a summary of changes to the user

## Content Placement Rules

Use these rules to decide where content belongs:

### Root CLAUDE.md (always loaded)

- Project name and purpose
- Tech stack overview
- Universal coding conventions (applies to ALL code)
- Git/commit conventions
- CI/CD and deployment notes
- Links to key documentation
- Cross-references to subdirectory CLAUDE.md files

### Directory-scoped CLAUDE.md (loaded when working in that directory)

- Language/framework-specific conventions for that directory
- File naming and organization rules specific to that area
- Import/export patterns
- Testing patterns specific to that area
- Build/compilation notes for that subsystem

### What NOT to put in CLAUDE.md

- Content that changes frequently (use external docs with explicit read triggers)
- Very long reference material (keep in separate .md files, use explicit read triggers)
- Information that's obvious from the code itself

## Anti-patterns to Fix

When analyzing existing CLAUDE.md, look for and fix these anti-patterns:

1. **"Refer to X for details"** → Inline the content or use explicit trigger
2. **Duplicate information** across multiple sections → Consolidate
3. **Outdated instructions** referencing files/dirs that don't exist → Remove
4. **Overly verbose explanations** → Condense to actionable rules
5. **Everything in root** when clear directory boundaries exist → Split
6. **Directory-specific rules in root** → Move to appropriate directory CLAUDE.md
