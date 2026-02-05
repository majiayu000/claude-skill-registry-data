---
name: list-skills
description: List all available skills in Nexus with descriptions. Load when user says "list skills", "show skills", "what skills", "available skills", "skill list", "all skills", or asks what they can do with Nexus.
---

# List Skills

Display all available skills organized by category with descriptions.

## Purpose

Help users discover available skills in Nexus. Shows both system skills (built-in) and user skills (custom) organized by category.

**Time Estimate**: Instant

---

## Workflow

### Step 1: Run Skill Scanner

```bash
python 00-system/core/nexus-loader.py --list-skills
```

Parse the JSON output to get all skills with their names and descriptions.

---

### Step 2: Organize by Category

Group skills by their folder location:

| Category | Location | Description |
|----------|----------|-------------|
| **Learning** | `00-system/skills/learning/` | Onboarding and tutorials |
| **Projects** | `00-system/skills/projects/` | Project management |
| **Skill Dev** | `00-system/skills/skill-dev/` | Skill creation and sharing |
| **System** | `00-system/skills/system/` | System utilities |
| **Tools** | `00-system/skills/tools/` | Productivity tools |
| **Integrations** | `00-system/skills/notion/`, `airtable/`, `beam/` | External tool connections |
| **User Skills** | `03-skills/` | Your custom skills |

---

### Step 3: Display Skills

Output format:

```
# Available Skills

## Learning (onboarding)
- setup-goals: Personalize Nexus with your goals and role
- setup-workspace: Configure your workspace folder structure
- learn-projects: Tutorial on project system
- learn-skills: Tutorial on skill system
- learn-nexus: Advanced system mastery

## Projects
- create-project: Create a new project with guided planning
- execute-project: Work on a project systematically
- archive-project: Archive completed projects
- bulk-complete: Mark multiple tasks complete

## System
- close-session: Save progress and end session
- list-skills: This skill - show all available skills
- validate-system: Check system health
- validate-workspace-map: Sync workspace documentation

## Tools
- mental-models: 30+ thinking frameworks for decisions
- generate-philosophy-doc: Create best practices documents

## Integrations
- notion-connect: Connect to Notion databases
- airtable-connect: Connect to Airtable bases
- beam-*: Beam.ai agent management (10 skills)

## User Skills
[List any skills in 03-skills/ or "None yet - say 'create skill' to add one!"]

---
Tip: Say the skill name or trigger phrase to use it.
```

---

## Notes

- User skills in `03-skills/` take priority over system skills
- Skill triggers are in the description (e.g., "say 'create project'")
- Some skills are internal (e.g., master skills) and not directly triggered

---

## Success Criteria

- [ ] All system skills listed by category
- [ ] All user skills listed (or "none yet" message)
- [ ] Each skill shows name and brief description
- [ ] Tip provided on how to use skills
