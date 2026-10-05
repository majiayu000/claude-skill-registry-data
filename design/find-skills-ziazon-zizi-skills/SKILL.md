---
name: find-skills
description: Helps users discover and install agent skills, but ONLY on an explicit request for a skill — "find/install a skill for X", "is there a skill that…", "search skills for X", or asking to extend capabilities with a new skill. Do NOT trigger on ordinary "how do I do X" questions — those are normal Q&A or belong to project-config; this skill is for when the user is explicitly shopping for an installable skill, not for answering the underlying task.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## When to Use This Skill

Use this skill only when the user **explicitly** asks for a skill:

- Says "find a skill for X" or "is there a skill for X"
- Asks to "install/search skills for X"
- Explicitly expresses interest in extending agent capabilities with a new skill

Do NOT trigger on a plain "how do I do X" or "can you do X" — answer those directly (or via project-config for how-to-run questions). Reach for this skill only when the user is shopping for an installable skill, not when they just want the task done.

## What is the Skills CLI?

The Skills CLI (`npx skills@1.7.0`, pinned to an exact version) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills@1.7.0 find [query] [--owner <owner>]` - Search for skills interactively or by keyword, optionally scoped to a GitHub owner
- `npx skills@1.7.0 add <package>` - Install a skill from GitHub or other sources
- `npx skills@1.7.0 check` - Check for skill updates
- `npx skills@1.7.0 update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Check the Leaderboard First

Before running a CLI search, check the [skills.sh leaderboard](https://skills.sh/) to see if a well-known skill already exists for the domain. The leaderboard ranks skills by total installs, surfacing the most popular and battle-tested options.

For example, top skills for web development include:
- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs each)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)

### Step 3: Search for Skills

If the leaderboard doesn't cover the user's need, run the find command:

```bash
npx skills@1.7.0 find [query] [--owner <owner>]
```

For example:

- User asks "how do I make my React app faster?" → `npx skills@1.7.0 find react performance`
- User asks "can you help me with PR reviews?" → `npx skills@1.7.0 find pr review`
- User asks "I need to create a changelog" → `npx skills@1.7.0 find changelog`

### Step 4: Verify Quality Before Recommending

**Do not recommend a skill based solely on search results.** Always verify:

1. **Install count** — Prefer skills with 1K+ installs. Be cautious with anything under 100.
2. **Source reputation** — Official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.
3. **GitHub stars** — Check the source repository. A skill from a repo with <100 stars should be treated with skepticism.

### Step 5: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The install count and source
3. The install command they can run
4. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills@1.7.0 add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Step 6: Offer to Install

If the user wants to proceed, you can install the skill for them:

```bash
npx skills@1.7.0 add <owner/repo@skill> -g
```

The `-g` flag installs globally (user-level). Do NOT pass `-y` / auto-confirm — installs into this curated setup should never be silent; let the confirmation prompt run so the user approves each skill.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills@1.7.0 init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills@1.7.0 init my-xyz-skill
```
