---
name: Steering Workflow
description: This skill should be used when the user asks about "steering documents", "project steering", "workflow setup", "CLAUDE.md configuration", "AGENTS.md", "AI agent project setup", or needs to understand how to configure steering documentation for AI-driven development workflows.
version: 1.0.0
---

# Steering Workflow Skill

This skill provides comprehensive knowledge for creating and maintaining steering documentation that enables seamless AI-driven software development workflows.

## Overview

The steering workflow establishes project conventions, technical standards, and workflow protocols that guide AI agents in understanding and working with a codebase effectively.

```
Steering Ecosystem
├── .claude/steering/
│   ├── product.md     → Product purpose, features, business rules
│   ├── tech.md        → Tech stack, conventions, commands
│   └── structure.md   → Project organization, key files
├── CLAUDE.md          → Central AI guidance + workflow protocols
└── AGENTS.md          → Jules VM environment setup guide
```

## Workflow Phases

### Phase 1: Pre-flight Validation
```
1. Check .claude/steering/ directory exists
2. Read existing steering files (if any)
3. Read CLAUDE.md (if exists)
4. Determine update strategy:
   - CREATE: File doesn't exist
   - UPDATE: File exists but outdated
   - SKIP: File exists and is current
```

### Phase 2: Codebase Analysis
Execute these tracks in parallel:

| Track | Focus | Key Files |
|-------|-------|-----------|
| Product | Purpose, features | README, package.json description |
| Tech Stack | Dependencies, tools | package.json, tsconfig, build configs |
| Structure | Organization | Directory listing, naming patterns |
| Conventions | Code style | ESLint, Prettier, CONTRIBUTING.md |

### Phase 3: Document Generation
Apply content templates to generate actionable documentation:

```markdown
# Product.md Template
- Product Overview (2-3 sentences)
- Core Features (max 5-7)
- User Value Proposition
- Key Business Logic Rules
- Success Metrics

# Tech.md Template
- Primary Technologies
- Key Dependencies (max 10)
- Build System
- Common Commands (copy-paste ready)
- Code Conventions (max 7-10)
- Testing Strategy
- Environment Variables

# Structure.md Template
- Directory Structure (2-3 levels)
- File Naming Patterns
- Component Architecture
- Key File Locations
- Module Dependencies
```

### Phase 4: Integration
Update CLAUDE.md with:
- Steering document references
- Core workflow instructions
- Lessons section
- Scratchpad section

Create AGENTS.md with:
- Environment setup for Jules VMs
- Build order for monorepos
- Task execution protocol
- Quality gates checklist

### Phase 5: Verification
Quality checklist:
- [ ] Clarity: No ambiguous instructions
- [ ] Completeness: Critical conventions covered
- [ ] Actionability: Commands are copy-paste ready
- [ ] Brevity: No generic advice

## Integration with Other Workflows

```
/steering → /spec → /jules → /reviewer
    │         │        │         │
    │         │        │         └── Review PRs
    │         │        └── Cloud implementation
    │         └── Feature specification
    └── Project setup
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `/steering` | Create/update steering documents |
| `/spec <feature>` | Plan feature (Requirements → Design → Tasks) |
| `/jules <feature>` | Implement via cloud VM |
| `/reviewer` | Code review |

## Best Practices

1. **Selective Updates**: Never overwrite existing content without comparison
2. **Project-Specific**: Eliminate generic advice; focus on actual patterns
3. **Actionable**: Every instruction should be executable
4. **Concise**: Every sentence should add value
5. **Error Markers**: Use ⚠️ TODO for uncertain sections

## Skill Integration Points

When running /steering, these skills enhance specific phases:

| Phase | Skills to Invoke |
|-------|-----------------|
| Tech Discovery | `tech-stack-detector`, language-specific skills |
| Structure Mapping | `xsky-core` for XSky projects |
| Convention Detection | `electron-integration` for Electron apps |
| MCP Configuration | `mcp-development` for MCP-enabled projects |

## Source Files

| File | Purpose |
|------|---------|
| `.claude/commands/steering.md` | Steering command definition |
| `.claude/commands/spec.md` | Spec workflow command |
| `.claude/commands/jules.md` | Jules integration command |
| `.claude/system-prompts/spec-workflow-starter.md` | Spec workflow instructions |
