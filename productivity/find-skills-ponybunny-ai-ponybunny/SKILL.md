---
name: find-skills
description: Discover and install skills from skills.sh marketplace
version: 1.0.0
author: ponybunny
tags: [skills, discovery, marketplace]
phases: [intake, elaboration, planning, execution]
user-invocable: true
command-dispatch: tool
command-tool: find_skills
command-arg-mode: raw
---

# Find Skills

Discover and install skills from the skills.sh marketplace to extend PonyBunny's capabilities.

## Usage

This skill helps you:
1. **Search** for skills by keywords, tags, or author
2. **Review** available skills and their capabilities
3. **Install** skills that match your needs
4. **Discover** new ways to accomplish tasks

## When to Use

Use this skill when:
- You need a capability that's not currently available
- You want to explore what skills exist for a specific domain
- You're looking for pre-built solutions to common tasks
- The current task requires specialized knowledge or tools

## Examples

### Search for skills
```
Search skills.sh for "data analysis"
Find skills related to research and documentation
What skills are available for email automation?
```

### Install skills
```
Install the skill "vercel-labs/skills/email-composer"
Add the weather forecast skill to the system
```

## How It Works

1. **Query Construction**: Converts your natural language request into a search query
2. **Marketplace Search**: Queries skills.sh using the find-skills API
3. **Results Presentation**: Shows matching skills with descriptions
4. **Installation**: Downloads and installs selected skills to ~/.ponybunny/skills

## Integration

This skill integrates with:
- **skills.sh marketplace**: Access to hundreds of community-created skills
- **Managed skills directory**: Automatic installation to ~/.ponybunny/skills
- **Skill registry**: Auto-discovery after installation

## Notes

- Skills are installed to the managed directory (~/.ponybunny/skills)
- Installed skills are automatically available in future sessions
- You can review skill details before installation
- Skills can be removed by deleting from the managed directory
