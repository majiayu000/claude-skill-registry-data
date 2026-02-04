---
name: explain-nexus
description: Explain what Nexus is and how it works. Load when user says "explain nexus", "what is nexus", "how does nexus work", "nexus overview", "about nexus", or asks for help understanding the system.
---

# Explain Nexus

Provide a clear, concise explanation of what Nexus is and how to use it.

## Purpose

Help users understand Nexus quickly without reading extensive documentation. Covers the core concepts, key commands, and how to get started.

**Time Estimate**: 2-3 minutes to explain

---

## Workflow

### Step 1: Load Overview Files

Read both overview files for accurate information:

```
00-system/documentation/product-overview.md
00-system/documentation/framework-overview.md
```

Use product-overview for the "what" and framework-overview for the "how".

### Step 2: Explain Core Concepts

Present this concise explanation:

```
# What is Nexus?

Nexus is your **AI-powered work operating system**. It gives Claude:

1. **Memory** - Your goals, preferences, and learnings persist across sessions
2. **Projects** - Structured work with planning, tasks, and progress tracking
3. **Skills** - Reusable workflows you can trigger with simple phrases

## The Magic

Every session, Claude automatically loads your context. No more re-explaining
who you are or what you're working on.

## Key Commands

| Say This | What Happens |
|----------|--------------|
| "create project" | Start a new project with guided planning |
| "continue [name]" | Resume work on a project |
| "setup goals" | Personalize Nexus with your role and goals |
| "list skills" | See all available skills |
| "done" | Save progress and end session |

## The Decision Rule

- **Projects** = Finite work (has an end)
- **Skills** = Repeating workflows (used again)

Creating "report-jan", "report-feb"? That's a SKILL, not projects!

## Quick Start

1. Say "create project" to start working
2. Say "setup goals" to personalize (optional but recommended)
3. Say "done" when finished to save your progress
```

### Step 3: Offer Next Steps

Based on user's current state (from startup stats):

**If goals not personalized:**
> Want to personalize? Say "setup goals" to teach Nexus about your role and objectives.

**If no projects exist:**
> Ready to start? Say "create project" and I'll guide you through planning.

**If projects exist:**
> You have active projects. Say "continue [name]" to resume, or "list skills" to see what else you can do.

---

## Additional Resources

If user wants more detail, point to:

- **"learn projects"** - Deep dive into project system
- **"learn skills"** - Deep dive into skill system
- **"learn nexus"** - Advanced patterns and tips
- **"list skills"** - See all available capabilities

---

## Success Criteria

- [ ] User understands what Nexus does (memory, projects, skills)
- [ ] User knows the key commands
- [ ] User knows the project vs skill distinction
- [ ] User has clear next steps based on their current state
