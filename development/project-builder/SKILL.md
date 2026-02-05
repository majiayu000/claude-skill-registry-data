---
name: project-builder
description: Guide for setting up new Claude Projects with proper context. Use when Ethan wants to create a new project, mentions setting up a project, uploads the project template, or asks about configuring a new workspace. Triggers Socratic discovery process to fill template sections.
---

# Project Builder

Build new Claude Projects through guided discovery. Don't assume, don't lecture. Ask questions to understand the project, then generate the configuration.

## Process

### Phase 1: Discovery

Ask questions one or two at a time. Use Socratic method to draw out details rather than requesting a spec dump.

**Core questions to uncover:**

1. **What is this?**
   - "What are we making?"
   - "Give me the elevator pitch."

2. **Why does it exist?**
   - "What's the goal here?"
   - "Who's it for?"

3. **Where is it at?**
   - "How far along? Idea, in progress, nearly done?"
   - "What exists already?"

4. **What's the shape of it?**
   - For dev: "What's the stack?"
   - For creative: "What's the format/medium?"
   - For research: "What's the output?"
   - Only ask what's relevant to the project type

5. **What's the current focus?**
   - "What are you working on right now?"
   - "What's next?"

Adapt questions to what Ethan says. If he's brief, probe deeper. If he's detailed, move on. Don't repeat what he's already told you. Don't assume it's a dev project.

### Phase 2: Generate Configuration

Once you have enough context, generate two outputs:

**Output 1: Project Instructions** (for Project Settings)

```markdown
**Project:** [Name]

**Purpose:** [One-line description]

**Current Status:** [Where it's at]

**Key Context:**
- [Essential detail 1]
- [Essential detail 2]
- [Essential detail 3]

**Project Rules:** [OPTIONAL - only include if project needs specific rules beyond global preferences]
- [Project-specific rule if needed]
```

**Output 2: Checklist**

```markdown
## Setup Checklist
- [ ] Create project in Claude
- [ ] Paste Project Instructions into Project Settings
- [ ] Add core memory entries (15 entries from core_memory_for_projects.md)
- [ ] Upload relevant project documentation
```

### Phase 3: Memory Reminder

After generating config, remind Ethan:

"Projects don't inherit global memory. Add the 15 core memory entries or I won't know who you are in the new project."

## Anti-patterns

- Don't ask for a full spec upfront
- Don't generate boilerplate questions, tailor to what's been said
- Don't assume project type (could be dev, creative, research, personal, etc.)
- Don't pad the Project Instructions with unnecessary context
- Don't include Project Rules unless actually needed
- Don't forget the memory reminder

## Reference Files

The project template and core memory file should be stored in this Configuration project:
- `project_template.md` - Full template with all sections
- `core_memory_for_projects.md` - The 15 core memory entries to copy
