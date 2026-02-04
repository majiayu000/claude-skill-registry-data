---
name: claude-code-memory
description: Maintain Claude Code memory hygiene by auditing, organizing, updating, and optimizing memory files in `.claude/memory/`. Use when users request memory cleanup, organization, updates, or want to reduce context pollution. Handles stale content, redundancy, conflicts, and file organization issues.
---

# Claude Code Memory Management

This skill provides systematic workflows for maintaining clean, organized, and effective Claude Code memory files.

## Core Capabilities

1. **Audit memory** - Detect stale files, redundancy, conflicts, size issues
2. **Organize memory** - Structure files in `.claude/memory/` following best practices
3. **Update content** - Keep memory current as projects evolve
4. **Reduce pollution** - Eliminate outdated, redundant, or conflicting information
5. **Optimize context** - Ensure memory files are concise and well-organized
6. **Capture learnings** - Document solutions to prevent repeating struggles in future sessions

## When to Use This Skill

Trigger this skill when users say:
- "Clean up my Claude Code memory"
- "My memory is getting cluttered"
- "Audit/review my memory files"
- "Organize my project memory"
- "Update memory for [recent change]"
- "Memory feels stale/outdated"
- "Reduce context pollution"
- "Help me structure my memory files"
- "Save this solution so you don't struggle with it again"
- "Capture this learning for future sessions"
- "You keep making the same mistake, remember this fix"

## Quick Start

### Step 1: Run Initial Audit

Start by understanding the current state:

```bash
python scripts/audit_memory.py [path/to/.claude/memory]
```

If no path provided, defaults to `.claude/memory` in current directory.

The audit identifies:
- Stale files (not updated in 60+ days)
- Large files (>50KB)
- Redundancy warnings
- Organization issues

### Step 2: Choose Appropriate Workflow

Based on audit results, use the appropriate maintenance workflow from `references/maintenance_workflows.md`:

- **Stale content** → Workflow 2: Stale Content Review
- **Large files** → Workflow 4: Large File Splitting
- **Redundancy** → Workflow 3: Redundancy Consolidation
- **Conflicts** → Workflow 5: Conflict Resolution
- **Major changes** → Workflow 6: Project Context Update

### Step 3: Implement and Verify

1. Execute the chosen workflow
2. Update `.claude/CLAUDE.md` if references changed
3. Re-run audit to verify improvements

## Memory Organization Philosophy

Memory files should be stored in `.claude/memory/` to keep the project root clean:

```
.claude/
├── CLAUDE.md              # Main context (references memory)
└── memory/                # All memory files
    ├── project_overview.md
    ├── architecture/      # Structural design decisions
    ├── conventions/       # Established patterns and standards
    ├── decisions/         # ADRs and key choices (with rationale)
    ├── workflows/         # Process documentation
    └── learnings/         # Solutions from past struggles (temporary→permanent)
```

**Key principles:**
- Each file serves a clear, specific purpose
- Information is current and accurate
- No redundancy or conflicts
- Files are 200-500 lines (split if larger)
- Important info comes first

**Memory types and their purposes:**
- **Learnings** - Troubleshooting tips and gotchas (prevent repeating struggles)
- **Conventions** - Standard practices for this project (follow consistently)
- **Architecture** - System structure and design (rarely changes)
- **Decisions** - Historical record of significant choices (with rationale)

**Lifecycle:** Learnings can be promoted to Conventions/Architecture/Decisions when patterns emerge. See `references/memory_lifecycle.md` for complete framework.

## Common Scenarios

### Scenario 1: Starting Fresh

**User:** "Help me set up memory for my project"

**Action:**
1. Create `.claude/memory/` directory structure
2. Create `project_overview.md` with key context
3. Set up subdirectories: `architecture/`, `conventions/`, `workflows/`
4. Update `.claude/CLAUDE.md` to reference memory files
5. Consult `references/organization_patterns.md` for structure

### Scenario 2: Project Direction Changed

**User:** "We refactored from REST to GraphQL, update memory"

**Action:**
1. Identify affected files (likely in `architecture/`)
2. Update technical details
3. Archive old REST-specific decisions
4. Add new GraphQL conventions
5. Update cross-references
6. Follow Workflow 6 in `references/maintenance_workflows.md`

### Scenario 3: Memory Feels Cluttered

**User:** "My memory is a mess, clean it up"

**Action:**
1. Run `scripts/audit_memory.py` to identify issues
2. Review stale files (Workflow 2)
3. Consolidate redundancy (Workflow 3)
4. Split large files (Workflow 4)
5. Reorganize if needed
6. Generate summary of changes made

### Scenario 4: Routine Maintenance

**User:** "Review my memory"

**Action:**
1. Run audit script
2. Quick check for obvious issues (stale dates, TODOs, conflicts)
3. Suggest specific improvements based on findings
4. Offer to implement if user wants

### Scenario 5: Capture Session Learning

**User:** "You struggled with that import error for a while. Save the solution so you don't repeat it."

**Action:**
1. Identify the problem and solution from recent conversation
2. Run `scripts/capture_learning.py` (or do manual creation)
3. Choose appropriate category (debug, build, test, etc.)
4. Create structured entry in `.claude/memory/learnings/`
5. Optionally update CLAUDE.md to reference critical learnings
6. Follow guidance in `references/session_learnings.md`

**Example learning structure:**
- **Problem:** What Claude struggled with (with symptoms)
- **Solution:** What finally worked (with exact commands)
- **Context:** When to apply this solution

### Scenario 6: Promote Learning to Convention

**User:** "That Python import thing keeps happening. Make it a standard convention."

**Action:**
1. Review the learning(s) to identify the pattern
2. Determine if pattern applies project-wide
3. Create or update convention file (e.g., `conventions/python.md`)
4. Write clear rule with rationale
5. Update learning to reference convention (avoid duplication)
6. Update CLAUDE.md if convention is critical
7. Follow Workflow 10 in `references/maintenance_workflows.md`
8. Consult `references/memory_lifecycle.md` for lifecycle framework

**Example flow:**
- Learning: "Python imports fail → use python -m"
- Recognize pattern after 2-3 occurrences
- Convention: "Always run Python projects as modules"
- Cross-reference between docs

## Best Practices

### Before Making Changes
- Always run audit first to understand current state
- Ask user to confirm destructive actions (deletions)
- Back up important information before major restructuring

### When Updating Content
- Add "Last reviewed: YYYY-MM-DD" to updated files
- Keep historical context at end of files if relevant
- Update all cross-references when moving content

### When Organizing Files
- Group related information together
- Use clear, specific filenames
- Maintain consistent naming conventions
- Keep root `.claude/memory/` clean (use subdirectories)

### Context Optimization
- Prioritize current, actionable information
- Remove outdated TODOs and notes
- Keep files focused on single topics
- Link to external docs instead of copying

### Memory Lifecycle Management
- Start with learnings for new troubleshooting discoveries
- Promote to conventions when pattern appears 2-3+ times
- Cross-reference between learnings and conventions (avoid duplication)
- Review monthly: which learnings should become conventions?
- Consult `references/memory_lifecycle.md` for detailed framework

## Resources

- **Audit script** (`scripts/audit_memory.py`) - Automated memory health check
- **Learning capture script** (`scripts/capture_learning.py`) - Tool for documenting solutions to prevent repeated struggles
- **Organization patterns** (`references/organization_patterns.md`) - File structure and naming best practices
- **Maintenance workflows** (`references/maintenance_workflows.md`) - Step-by-step procedures including Workflow 9 (Capture Learnings) and Workflow 10 (Promote to Convention)
- **Session learnings guide** (`references/session_learnings.md`) - Complete guide to capturing and using learnings from Claude Code sessions
- **Memory lifecycle** (`references/memory_lifecycle.md`) - Framework for when learnings become conventions/architecture/decisions

## Response Pattern

When helping with memory management:

1. **Assess** - Run audit or review current state
2. **Identify** - Point out specific issues found
3. **Recommend** - Suggest appropriate workflow or actions
4. **Execute** - Implement changes if user approves
5. **Verify** - Confirm improvements made

Always be specific about what you're changing and why. Provide clear before/after context for significant updates.
