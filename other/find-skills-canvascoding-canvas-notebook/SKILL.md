---
name: find-skills
description: "Discover and install specialized agent skills from the open ecosystem. ALWAYS use this skill when the user asks 'how do I do X', 'find a skill for X', 'is there a skill for X', wants to extend agent capabilities, or needs help with a specific domain (design, testing, deployment, etc.). Make sure to use this skill whenever the user mentions skills, plugins, extensions, tools, or wants to find new capabilities for the agent. Integrates with the Skills CLI and skills.sh directory."
metadata:
  version: "1.0"
  author: canvas-studios
---

# Find Skills

A skill for discovering and installing new agent skills from the open ecosystem into Canvas Notebook.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

Key commands:

- `npx skills find [query]` — Search for skills interactively or by keyword
- `npx skills add <package>` — Install a skill from GitHub or other sources
- `npx skills list` — List installed skills

Browse skills at: https://skills.sh/

## Canvas Notebook Skill Installation

**IMPORTANT:** Canvas Notebook stores all skills in `/data/skills/<skill-name>/` (the runtime skills directory). When installing a skill, you MUST save it there so the app can load it automatically.

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Check the Leaderboard First

Before running a CLI search, check the skills.sh leaderboard to see if a well-known skill already exists for the domain. The leaderboard ranks skills by total installs, surfacing the most popular and battle-tested options.

For example, top skills for web development often include React, Next.js, design, testing, and document-processing packages from well-known maintainers.

### Step 3: Search for Skills

If the leaderboard doesn't cover the user's need, run the find command:

```bash
npx skills find [query]
```

Examples:

- User asks "how do I make my React app faster?" → `npx skills find react performance`
- User asks "can you help me with PR reviews?" → `npx skills find pr review`
- User asks "I need to create a changelog" → `npx skills find changelog`

### Step 4: Verify Quality Before Recommending

Do not recommend a skill based solely on search results. Always verify:

- **Install count** — Prefer skills with 1K+ installs. Be cautious with anything under 100.
- **Source reputation** — Prefer well-known maintainers, active repositories, and clearly documented provenance over unknown authors.
- **GitHub stars** — Check the source repository. A skill from a repo with <100 stars should be treated with skepticism.

### Step 5: Present Options to the User

When you find relevant skills, present them with:

- The skill name and what it does
- The install count and source
- The install command they can run
- A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills add vercel-labs/agent-skills --skill react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Step 6: Install to /data/skills (Canvas Notebook Only)

**CRITICAL:** In Canvas Notebook, skills MUST be installed to `/data/skills/` (the app's runtime skills directory), NOT to the default `~/.config/opencode/skills/` or other agent-specific folders.

When the user wants to proceed:

1. Clone or download the skill repository to a temporary directory:
   ```bash
   cd /tmp
   git clone https://github.com/owner/repo.git skill-temp
   ```

2. Find the skill directory (look for `SKILL.md`):
   - Root of repo (if it contains `SKILL.md`)
   - `skills/<skill-name>/`
   - `.agents/skills/<skill-name>/`
   - Other standard skill locations

3. Copy the entire skill directory to `/data/skills/`:
   ```bash
   cp -r /tmp/skill-temp/skills/<skill-name> /data/skills/<skill-name>
   ```

4. Ensure the directory name matches the `name:` field in the SKILL.md frontmatter.

5. Verify the skill is in place:
   ```bash
   ls /data/skills/<skill-name>/SKILL.md
   ```

6. Inform the user the skill is now available in the Canvas Notebook settings (Settings → Skills) and can be enabled/disabled there.

### Step 7: Enable the Skill (Optional)

After installing, the new skill may need to be enabled in the Canvas Notebook UI:

1. Go to Settings → Skills
2. Find the newly installed skill
3. Toggle it ON

Alternatively, if the user asks you to enable it, you can guide them or they can do it via the UI.

## Common Skill Categories

| Category | Example Queries |
|----------|----------------|
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Documentation | docs, readme, changelog, api-docs |
| Code Quality | review, lint, refactor, best-practices |
| Design | ui, ux, design-system, accessibility |
| Productivity | workflow, automation, git |

## Tips for Effective Searches

- Use specific keywords: "react testing" is better than just "testing"
- Try alternative terms: If "deploy" doesn't work, try "deployment" or "ci-cd"
- Check popular sources: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```

## Related Skills

- **skill-creator** — Create, test, and publish new skills from within your agent

## Notes

- Canvas Notebook scans `/data/skills/` at startup and loads any directory containing a `SKILL.md` file
- New skills are initially disabled by default; the user must enable them in Settings → Skills
- Skills follow the Canvas Skills format with YAML frontmatter (`name`, `description`, etc.) and optional `agents/canvas.yaml` UI metadata
- No `manifest.json` or `bin/` wrappers are needed in Canvas Notebook — skills are pure instruction files
