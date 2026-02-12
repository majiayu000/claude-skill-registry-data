---
name: ralph-prd
description: Create Product Requirements Document (PRD) and setup for Ralph autonomous loop. Use when user runs /create-prd command, wants to set up a project for Ralph, mentions "ralph setup", "create prd", "product requirements", or needs to generate tasks for autonomous development.
---

# Ralph PRD Creation

Interactive wizard to create Product Requirements Document and Ralph project setup with task sets.

## Quick Start

```bash
/create-prd                    # Start interactive wizard
/create-prd "Build a todo app" # Start with description
```

## What It Creates

```
project/
├── PROMPT.md                          # Instructions for each iteration
├── ralph.sh                           # Loop runner (executable)
└── .ralph/
    ├── current-taskset -> tasksets/initial  # Symlink to active taskset
    └── tasksets/
        └── initial/                   # Your task set (named during setup)
            ├── tasks.json             # Task list (JSON)
            ├── prd.md                 # Requirements (Markdown)
            ├── memories.md            # Persistent learnings
            ├── config.json            # Ralph settings
            └── activity.log           # Iteration log (empty)
```

## Discovery Questions

Ask these discovery questions:

0. **Task Set Name** - What should this collection be called? (default: "initial")
1. **Problem** - What problem are you solving?
2. **Audience** - Who is the target user?
3. **Features** - What are the 3-5 core features?
4. **Tech Stack** - What technologies to use?
5. **Architecture** - Monolith, microservices, etc.?
6. **UI/UX** - Visual requirements and preferences?
7. **Auth** - Authentication needs?
8. **Integrations** - Third-party services?
9. **Success Criteria** - How do we know it's done?

### Question Specificity for Destructive Operations

When discovery questions involve deleting files, removing dependencies, or other destructive changes:

- **Always include full paths** of items being deleted or modified
- **State size/scope** — file count, line count, component count
- **Explicitly state what will NOT be affected**
- **Frame as confirmation, not open question** — "Deleting X, Y, Z. Proceed?" not "What should be deleted?"

See [EXAMPLES.md](EXAMPLES.md) for vague-vs-specific anti-patterns.

## Task Generation

Convert features into atomic tasks with categories: `setup`, `feature`, `integration`, `styling`, `testing`, `verification`. See [WORKFLOW.md](WORKFLOW.md) for task format and categories.

**Final verification task:** Always include a final task with `verificationTier: "visual"` (UI projects) or `"api"` (API-only projects) that verifies the complete application works end-to-end. This catches issues that individual task verification misses.

## Workflow

See [WORKFLOW.md](WORKFLOW.md) for detailed discovery flow.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for PRD examples.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

## Templates

Use templates from [templates/](templates/) for generating output files:
- `prd.md.template` - PRD document structure
- `tasks.json.template` - Task list format
- `prompt.md.template` - Iteration instructions
- `config.json.template` - Ralph configuration
- `memories.md.template` - Learnings file

## After Setup

```bash
./ralph.sh 20    # Start autonomous loop
```

## Creating Additional Task Sets

After initial setup, create more task sets:

```bash
/ralph taskset new "auth-feature"    # Create new task set
/ralph taskset list                  # See all task sets
/ralph taskset switch "auth-feature" # Switch to it
```
