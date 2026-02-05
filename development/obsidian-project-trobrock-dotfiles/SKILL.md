---
name: obsidian-project
description: Create or update a project in the Obsidian vault Projects folder
---

# Obsidian Project Management

Manage projects in `~/dev/personal/obsidian/trobrock/Projects/`.

## Create New Project

When asked to create a new project:

1. **Ask for details** (if not provided):
   - Project name
   - Brief description
   - Tech stack (if applicable)
   - Hosting plans (if applicable)
   - URL/domain (if applicable)

2. **Create the file** at `~/dev/personal/obsidian/trobrock/Projects/{Project Name}.md`

3. **Use this template:**

```markdown
---
status: Idea
tech_stack:
  - Technology1
  - Technology2
hosting: []
url: ""
---

# {Project Name}

{Description}

## Ideas

- 

## Tasks

- [ ] 

## Notes

```

## Update Project Status

Valid status values:
- `Idea` → Just a concept
- `Active` → Currently working on it
- `Paused` → On hold
- `Discontinued` → No longer pursuing

To update, modify the `status:` field in the frontmatter.

## Project Lifecycle

```
Idea → Active → Paused (optional) → Discontinued
                    ↓
                 Active (resume)
```

## Linking Projects

When a project relates to goals in `Personal Home.md`, suggest adding a wiki link:
- In the project: `See [[Personal Home#2026 Goals]]`
- In Personal Home: Reference the project name

## Verification

- [ ] File is in `Projects/` folder
- [ ] Frontmatter has status, tech_stack, hosting, url fields
- [ ] Status is one of: Idea, Active, Paused, Discontinued
- [ ] tech_stack and hosting are arrays (even if empty `[]`)
